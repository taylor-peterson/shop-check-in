import Queue as queue

import winsound

import error_handler
import event
import id_logger
import shop
import shop_user
import shop_user_database
import io_moderator

MESSAGE = 0
ACTIONS_DICT = 1

CLOSED = "closed"
OPENING = "opening"
STANDBY = "standby"
UNLOCKED = "unlocked"
ADDING_USER = "adding_user"
ADDING_USERS = "adding_users"
REMOVING_USER = "removing_user"
CLEARING_DEBT = "clearing debt"
CHANGING_POD = "changing pod"

# TODO: refactor FSM logic into separate class? (e.g. state, run_fsm)
# TODO: any clean way to avoid unused function parameters?
# TODO: get rid of unauthorized user error catching?
# TODO: clarify exceptions for proctors - either no safety test or not hired asproctor?


class BoardFsm():

    def __init__(self, event_q, shop_user_db):
        self._state = CLOSED
        self._shop = shop.Shop()
        self._shop_user_database = shop_user_db
        self._event_q = event_q
        self._error_handler = error_handler.ErrorHandler(event_q)

        self._state_data = {
            CLOSED: ("\nShop closed.\nProctor swipe to open.",
                     {event.CARD_SWIPE: self._closed_process_card_swipe}),
            
            OPENING: ("\nStarting up!\n\rType BUTTON_CANCEL or flip_switch_off.",
                      {event.BUTTON_CANCEL: self._go_to_closed_state,
                       event.SWITCH_FLIP_OFF: self._opening_process_switch_flip}),

            STANDBY: ("\nShop open. Board locked\n\rPOD swipe to unlock.",
                      {event.CARD_SWIPE: self._standby_process_card_swipe}),

            UNLOCKED: ("\nBoard Unlcked.\n\rAll inputs available.",
                       {event.BUTTON_CANCEL: self._go_to_standby_state,
                        event.CARD_SWIPE: self._unlocked_process_card_swipe,
                        event.CARD_REMOVE: self._go_to_remove_user_state,
                        event.BUTTON_MONEY: self._go_to_clear_money_state,
                        event.BUTTON_CHANGE_POD: self._go_to_change_pod_state,
                        event.SWITCH_FLIP_ON: self._unlocked_process_closing_shop}),

            ADDING_USER: ("\nAdding user.\n\rSwipe another card, insert into slot, or BUTTON_CANCEL.",
                          {event.CARD_SWIPE: self._adding_user_process_card_swipe,
                           event.CARD_INSERT: self._adding_user_s_process_slot,
                           event.BUTTON_CANCEL: self._go_to_standby_state}),

            ADDING_USERS: ("\nAdding users.\n\rInsert both cards into slot or BUTTON_CANCEL.",
                           {event.CARD_INSERT: self._adding_user_s_process_slot,
                            event.BUTTON_CANCEL: self._go_to_standby_state}),

            REMOVING_USER: ("\nRemoving user(s).\n\rreinsert or insert card; or press clear or charge.",
                            {event.CARD_INSERT: self._removing_user_process_slot,
                             event.BUTTON_DISCHARGE_USER: self._removing_user_process_discharge,
                             event.BUTTON_MONEY: self._removing_user_process_charge}),

            CLEARING_DEBT: ("\nClearing user debt.\n\rSwipe user card or BUTTON_CANCEL.",
                            {event.CARD_SWIPE: self._clearing_debt_process_card_swipe,
                             event.BUTTON_CANCEL: self._go_to_standby_state}),

            CHANGING_POD: ("\nChanging POD status.\n\rSwipe proctor card or BUTTON_CANCEL.",
                           {event.CARD_SWIPE: self._changing_pod_process_card_swipe,
                            event.BUTTON_CANCEL: self._go_to_standby_state})
            }

    def run_fsm(self):
        cargo = None
        
        while True:
            state_message = self._state_data[self._state][MESSAGE]
            state_actions = self._state_data[self._state][ACTIONS_DICT]
            
            print state_message
            
            next_event = self._event_q.get()

            if next_event.key == event.TERMINATE_PROGRAM:
                return self._state
            
            try:
                (self._state, cargo) = state_actions[next_event.key](next_event.data, cargo)
            except KeyError:
                self._state = self._error_handler.handle_error(self._state, next_event.key)

    def _go_to_closed_state(self, ignored_event_data, ignored_cargo):
        return CLOSED, None

    def _go_to_standby_state(self, ignored_event_data, ignored_cargo):
        return STANDBY, None

    def _go_to_remove_user_state(self, slot, ignored_cargo):
        return REMOVING_USER, slot
    
    def _go_to_clear_money_state(self, ignored_event_data, ignored_cargo):
        return CLEARING_DEBT, None

    def _go_to_change_pod_state(self, ignored_event_data, ignored_cargo):
        return CHANGING_POD, None

    def _closed_process_card_swipe(self, user, ignored_cargo):
        if user.is_proctor():
            return OPENING, user
        else:
            return self._error_handler.handle_error(self._state, shop_user.NONEXISTENT_USER), ignored_cargo

    def _opening_process_switch_flip(self, ignored_event_data, user):
        self._shop.open_(user)
        # TODO: old-school mac startup sound
        return STANDBY, None

    def _standby_process_card_swipe(self, user, ignored_cargo):
        if self._shop.is_pod(user):
            return UNLOCKED, user
        else:
            return self._error_handler.handle_error(self._state, shop_user.NONEXISTENT_USER), ignored_cargo

    def _unlocked_process_card_swipe(self, user, ignored_cargo):
        if user.is_shop_certified():
            return ADDING_USER, [user]
        else:
            return self._error_handler.handle_error(self._state, shop_user.NONEXISTENT_USER), ignored_cargo

    def _unlocked_process_closing_shop(self, ignored_event_data, user):
        try:
            self._shop.close_(user)
        except shop.ShopOccupiedError:
            return self._error_handler.handle_error(self._state, "shop_occupied"), user
        else:
            return CLOSED, None

    def _adding_user_process_card_swipe(self, second_user, first_user):
        if second_user.is_shop_certified():
            return ADDING_USERS, first_user + [second_user]
        else:
            return self._error_handler.handle_error(self._state, shop_user.NONEXISTENT_USER), first_user

    def _adding_user_s_process_slot(self, slot, user_s):
        self._shop.add_user_s_to_slot(user_s, slot)
        return STANDBY, None

    def _removing_user_process_slot(self, slot, prev_slot):
        self._shop.replace_or_transfer_user(slot, prev_slot)
        return STANDBY, None
        
    def _removing_user_process_discharge(self, ignored_event_data, slot):
        self._shop.discharge_user_s(slot)
        return STANDBY, None

    def _removing_user_process_charge(self, ignored_event_data, slot):
        user_s = self._shop.discharge_user_s(slot)
        for user in user_s:
            self._shop_user_database.increase_debt(user)
        # TODO: sad trombone
        return STANDBY, None

    def _clearing_debt_process_card_swipe(self, user, ignored_cargo):
        try:
            self._shop_user_database.clear_debt(user)
        except shop_user_database.NonexistentUserError:
            return self._error_handler.handle_error(self._state, shop_user.NONEXISTENT_USER), ignored_cargo
        else:
            return STANDBY, user

    def _changing_pod_process_card_swipe(self, user, ignored_cargo):
        try:
            self._shop.change_pod(user)
        except shop.PodRequiredError:
            return self._error_handler.handle_error(self._state, "pod_required"), ignored_cargo
        except shop.UnauthorizedUserError:
            return self._error_handler.handle_error(self._state, shop_user.NONEXISTENT_USER), ignored_cargo
        else:
            return STANDBY, None


def main():
    event_q = queue.Queue()
    message_q = queue.Queue()

    shop_user_db = shop_user_database.ShopUserDatabaseGspread(event_q, "Python Testing")
    board = BoardFsm(event_q, shop_user_db)

    thread_id_logger = id_logger.IdLogger(shop_user_db)
    thread_io_moderator = io_moderator.IoModerator(event_q, message_q)
    thread_id_logger.start()
    thread_io_moderator.start()

    while True:
        board.run_fsm()

if __name__ == "__main__":
    main()
