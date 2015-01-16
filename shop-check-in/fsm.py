import threading
import Queue as queue

import winsound

import Application.id_logger as id_logger
import Application.shop_user as shop_user
import Application.shop as shop
import Application.event as event
import Application.error_handler as error_handler

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
        self.shop = shop.Shop()
        self.event_q = event_q
        self.shop_user_database = shop_user_database
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
                              event.BUTTON_CLEAR_USER : self.removing_user_process_clear,
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
            
            new_event = self.event_q.get()

            if new_event.key == event.TERMINATE_PROGRAM:
                return self.state
            
            try:
                (self.state, cargo) = self.state_data[self.state][ACTIONS_DICT][new_event.key](new_event.data, cargo)
            except KeyError:
                self.state = self._error_handler.handle_error(self.state, new_event.key)

    def closed_process_card_swipe(self, user, ignore_me):
        if user.proctor:
            return (OPENING, user)
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignore_me)

    def go_to_closed_state(self, ignore_me, ignore_me_too):
        return (CLOSED, None)

    def go_to_standby_state(self, ignore_me, ignore_me_too):
        return (STANDBY, None)

    def go_to_remove_user_state(self, slot, ignore_me):
        return (REMOVING_USER, slot)
    
    def go_to_clear_money_state(self, ignore_me, ignore_me_too):
        return (CLEARING_DEBT, None)

    def go_to_change_pod_state(self, ignore_me, ignore_me_too):
        return (CHANGING_POD, None)

    def opening_process_switch_flip(self, ignore_me, user):
        self.shop.open = True
        self.shop.pod_list.append(user)
        # TODO: log event
        # TODO: old-school mac startup sound
        return (STANDBY, None)

    def standby_process_card_swipe(self, user, ignore_me):
        if user in self.shop.pod_list:
            return (UNLOCKED, None)
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignore_me)

    def unlocked_process_card_swipe(self, user, ignore_me):
        if user.name == shop_user.UNAUTHORIZED:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignore_me)
        else:
            return (ADDING_USER, user)

    def unlocked_process_closing_shop(self, ignore_me, ignore_me_too):
        if shop.empty():
            self.shop.pod_list.clear()
            return (CLOSED, Null)
        else:
            return (self._error_handler.handle_error(self.state, "shop_occupied"), ignore_me)

    def adding_user_process_card_swipe(self, second_user, first_user):
        if second_user.name == shop_user.UNAUTHORIZED:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), first_user)
        else:
            return (ADDING_USERS, [first_user, second_user])

    def adding_user_s_process_slot(self, slot, users):
        self.shop.occupants[slot].append(users)
        return (STANDBY, None)

    def removing_user_process_slot(self, slot, prev_slot):
        if slot != prev_slot:
            self.shop.occupants[slot] = self.shop.occupants[prev_slot]
            self.shop.occupants[prev_slot] = []

        return (STANDBY, None)
        
    def removing_user_process_clear(self, ignore_me, slot):
        self.shop.occupants[slot] = []
        return (STANDBY, None)

    def removing_user_process_charge(self, slot, ignore_me):
        users = shop.occupants[slot]
        for user in users:
            self.shop_user_database.increase_debt(user)
        # sad trombone
        return (STANDBY, None)

    def clearing_debt_process_card_swipe(self, user, ignore_me):
        #cha-ching
        
        if user.name == shop_user.UNAUTHORIZED:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignore_me)
        else:
            self.shop_user_database.clear_debt(user)
            return (STANDBY, user)

    def changing_pod_process_card_swipe(self, user, ignore_me):
        if user.proctor and not user in self.shop.pod_list:
            self.shop.pod_list.append(user)
            return (STANDBY, None)
        elif user in self.shop.pod_list and len(self.shop.pod_list) > 1:
            self.shop.pod_list.remove(user)
            return (STANDBY, None)
        elif user.proctor:
            return (self._error_handler.handle_error(self.state, "pod_required"), ignore_me)
        else:
            return (self._error_handler.handle_error(self.state, shop_user.UNAUTHORIZED), ignore_me)

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
