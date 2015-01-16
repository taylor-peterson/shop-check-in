import threading
import Queue as queue

import winsound

import id_logger
import shop_user
import shop
import event
import error_handler

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

class BoardFsm():

    def __init__(self, event_q, shop_user_database):
        self.state = CLOSED
        self.shop = shop.Shop(shop_user_database)
        self.shop_user_database = shop_user_database # TODO: should this class have this?
        self.event_q = event_q
        self._error_handler = error_handler.ErrorHandler(event_q)

        self.state_data = {
            CLOSED : ("Shop closed.\nProctor swipe to open.",
                      {event.CARD_SWIPE : self.closed_process_card_swipe}),
            
            OPENING : ("Starting up!\n\rType BUTTON_CANCEL or flip_switch_off.",
                       {event.BUTTON_CANCEL : self.go_to_closed_state,
                        event.SWITCH_FLIP_OFF : self.opening_process_switch_flip}),

            STANDBY : ("Shop open. Board locked\n\rPOD swipe to unlock.",
                      {event.CARD_SWIPE : self.standby_process_card_swipe}),

            UNLOCKED : ("Board Unlcked.\n\rAll inputs available.",
                        {event.BUTTON_CANCEL : self.go_to_standby_state,
                         event.CARD_SWIPE : self.unlocked_process_card_swipe,
                         event.CARD_REMOVE : self.go_to_remove_user_state,
                         event.BUTTON_MONEY : self.go_to_clear_money_state,
                         event.BUTTON_CHANGE_POD : self.go_to_change_pod_state,
                         event.SWITCH_FLIP_ON : self.unlocked_process_closing_shop}),

            ADDING_USER : ("Adding user.\n\rSwipe another card, insert into slot, or BUTTON_CANCEL.",
                           {event.CARD_SWIPE : self.adding_user_process_card_swipe,
                            event.CARD_INSERT : self.adding_user_s_process_slot,
                            event.BUTTON_CANCEL : self.go_to_standby_state}),

            ADDING_USERS : ("Adding users.\n\rInsert both cards into slot or BUTTON_CANCEL.",
                            {event.CARD_INSERT : self.adding_user_s_process_slot,
                             event.BUTTON_CANCEL : self.go_to_standby_state}),

            REMOVING_USER : ("Removing user(s).\n\rreinsert or insert card; or press clear or charge.",
                             {event.CARD_INSERT : self.removing_user_process_slot,
                              event.BUTTON_DISCHARGE_USER : self.removing_user_process_discharge,
                              event.BUTTON_MONEY : self.removing_user_process_charge}),

            CLEARING_DEBT : ("Clearing user debt.\n\rSwipe user card or BUTTON_CANCEL.",
                             {event.CARD_SWIPE : self.clearing_debt_process_card_swipe,
                              event.BUTTON_CANCEL : self.go_to_standby_state}),

            CHANGING_POD : ("Changing POD status.\n\rSwipe proctor card or BUTTON_CANCEL.",
                            {event.CARD_SWIPE : self.changing_pod_process_card_swipe,
                             event.BUTTON_CANCEL : self.go_to_standby_state}),
            }

    def run_fsm(self):
        cargo = None
        
        while True:
            print
            print self.state_data[self.state][MESSAGE]
            
            next_event = self.event_q.get()

            if next_event.key == event.TERMINATE_PROGRAM:
                return self.state
            
            try:
                (self.state, cargo) = self.state_data[self.state][ACTIONS_DICT][next_event.key](next_event.data, cargo)
            except KeyError:
                self.state = self._error_handler.handle_error(self.state, next_event.key)

    def go_to_closed_state(self, ignored_event_data, ignored_cargo):
        return (CLOSED, None)

    def go_to_standby_state(self, ignored_event_data, ignored_cargo):
        return (STANDBY, None)

    def go_to_remove_user_state(self, slot, ignored_cargo):
        return (REMOVING_USER, slot)
    
    def go_to_clear_money_state(self, ignored_event_data, ignored_cargo):
        return (CLEARING_DEBT, None)

    def go_to_change_pod_state(self, ignored_event_data, ignored_cargo):
        return (CHANGING_POD, None)

    def closed_process_card_swipe(self, user, ignored_cargo):
        if user.is_proctor():
            return (OPENING, user)
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignored_cargo)

    def opening_process_switch_flip(self, ignored_event_data, pod):
        self.shop.open_()
        # TODO: log event
        # TODO: old-school mac startup sound
        return (STANDBY, None)

    def standby_process_card_swipe(self, user, ignored_cargo):
        if shop.is_pod(user):
            return (UNLOCKED, None)
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignored_cargo)

    def unlocked_process_card_swipe(self, user, ignored_cargo):
        if user.is_shop_certified():
            return (ADDING_USER, user)
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignored_cargo)

    def unlocked_process_closing_shop(self, ignored_event_data, ignore_me_too):
        try:
            shop.close_()
            return (CLOSED, Null)
        except:
            return (self._error_handler.handle_error(self.state, "shop_occupied"), ignored_cargo)

    def adding_user_process_card_swipe(self, second_user, first_user):
        if second_user.is_shop_certified():
            return (ADDING_USERS, [first_user, second_user])
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), first_user)

    def adding_user_s_process_slot(self, slot, user_s):
        self.shop.add_user_s_to_slot(user_s, slot)
        return (STANDBY, None)

    def removing_user_process_slot(self, slot, prev_slot):
        self.shop.replace_or_transfer_user(slot, prev_slot)
        return (STANDBY, None)
        
    def removing_user_process_discharge(self, ignored_event_data, slot):
        self.shop.discharge_user_s(slot)
        return (STANDBY, None)

    def removing_user_process_charge(self, ignored_event_data, slot):
        self.shop.charge_user_s(slot)
        # TODO: sad trombone
        return (STANDBY, None)

    def clearing_debt_process_card_swipe(self, user, ignored_cargo):       
        if user.is_shop_certified():
            self.shop_user_database.clear_debt(user)
            # TODO: cha-ching
            return (STANDBY, user)
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignored_cargo)

    def changing_pod_process_card_swipe(self, user, ignored_cargo):
        try:
            self.shop.change_pod(user)
            return (STANDBY, None)
        except: # requires at least one proctor
            return (self._error_handler.handle_error(self.state, "pod_required"), ignored_cargo)
        except: #invalid user
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignored_cargo)

def main():
    # Create a single input and a single output queue for all threads.
    dir_q = queue.Queue()
    event_q = queue.Queue()

    shop_user_database = shop_user.ShopUserDatabase(event_q, "Python Testing")
    board = BoardFsm(event_q, shop_user_database)

    thread = id_logger.IdLogger(shop_user_database)
    thread.start()

    while True:
        board.run_fsm()

if __name__== "__main__":
    main()
