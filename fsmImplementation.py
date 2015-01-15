import threading
import Queue as queue

import winsound

import Application.id_logger as id_logger
import Application.shop_user as shop_user
import Application.shop as shop
import Application.event as event
import Application.state as state

DEFAULT_ERROR_MESSAGE = "Action not recognized."

MESSAGE = 0
ACTIONS_DICT = 1

CLOSED = "closed"
OPENING = "opening"
STANDBY = "opening"
UNLOCKED = "unlocked"

class BoardFsm():

    def __init__(self, event_q):
        self.state = CLOSED
        self.shop = shop.Shop()
        self.event_q = event_q

        self.state_data = {
            CLOSED : ("Shop closed.\nProctor swipe to open.",
                      {event.CARD_SWIPE : self.closed_process_card_swipe}),
            
            OPENING : ("Starting up!\n\rType cancel or flip_switch_off: ",
                       {"cancel" : self.standby_state,
                        "flip_switch_off" : self.opening_process_switch_flip}),

            STANDBY : ("Shop open. Board locked\n\rPOD swipe to unlock.",
                      {event.CARD_SWIPE : self.standby_process_card_swipe}),

            UNLOCKED : ("Board Unlcked.\n\rAll inputs available.",
                        {"cancel" : self.standby_state,
                         event.CARD_SWIPE : self.unlocked_process_card_swipe,
                         "card_remove" : self.remove_user_state,
                         "clear_money" : self.clearMoney,
                         "change_pod" : self.changePod,
                         "flip_switch_on" : self.closeShop}),

            ADDING_USER : ("Adding user.\n\rSwipe another card, insert into slot, or cancel.",
                           {event.CARD_SWIPE : self.adding_user_process_card_swipe,
                            "card_insert" : self.adding_user_s_process_slot,
                            "cancel" : self.standby_state}),

            ADDING_USERS : ("Adding users.\n\rInsert both cards into slot or cancel.",
                            {"card_insert" : self.adding_user_s_process_slot,
                             "cancel" : self.standby_state}),

            REMOVING_USER : ("Removing user(s).\n\rreinsert or insert card; or press clear or charge.",
                             {"card_insert" : removing_user_process_slot,
                              "clear" : removing_user_process_clear,
                              "charge" : removing_user_process_charge}),

            CLEARING_DEBT : ("Clearning user debt.\n\rSwipe user card or cancel.",
                             {event.CARD_SWIPE : self.clearing_debt_process_card_swipe,
                              "cancel" : self.standby_state}),

            CHANGING_POD : ("Changing POD status.\n\rSwipe proctor card or cancel.",
                            {event.CARD_SWIPE : self.changing_pod_process_card_swipe,
                             "cancel" : self.standby_state}),

            CLOSING


        self.unauthorized_messages = {
            "default" : DEFAULT_ERROR_MESSAGE,
            "invalid user" : "User does not have permissions for that action.",
            "invalid card swipe" : "ERR - Ignoring swipe. Please confirm.",
            "invalid card removal" : "ERR - Reinsert card(s), or confirm students have left." # send tsk email
            }

    def run_fsm(self):
        cargo = None
        
        while True:
            print self.state_data[self.state][MESSAGE]

            event = self.event_q.get()

            try:
                (self.state, cargo) =
                    self.state_data[self.state][ACTIONS_DICT][event.key](event.data, cargo)
            except KeyError:
                self.state = self.unauthorized(event.error_msg)
                #cargo = None
            

    # =====================================

    def unauthorized(self, error_message = "default"):
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)

        print self.unauthorized_messages.get(error_message, DEFAULT_ERROR_MESSAGE)
        
        userInput = raw_input("    press enter to return to standby.")
        return self.standby_state()

    def closed_process_card_swipe(self, user, ignore_me):
        if user.proctor:
            return (OPENING, user)
        else:
            return self.unauthorized("invalid user")

    def opening_process_switch_flip(self, ignore_me, user):
        self.shop.open = True
        self.shop.pod_list.append(user)
        print "    Shop now open with proctor now on duty."
        # log event
        winsound.Beep(500,250) # old-school mac startup sound
        return self.standby_state()
    

    def standby_process_card_swipe(self, user, ignore_me):
        if user in self.shop.pod_list:
            return self.unlockBoard(input)
        else:
            return self.unauthorized("invalid user")

    def unlocked_process_card_swipe(self, user, ignore_me):
        if user.name == "Unauthorized":
            return self.unauthorized("invalid user")
        else:
            return (ADD_USER_OR_ASSIGN_SLOT, user)

    def unlocked_process_closing_shop(self, ignore_me, ignore_me):
        # close shop if clear
        # error otherwise

    def adding_user_process_card_swipe(self, second_user, first_user):
        if user.name == "Unauthorized":
            return self.unauthorized("invalid user")
        else:
            return (ASSIGN_SLOT, (first_user, second_user))

    def adding_user_s_process_slot(self, slot, users):
        pass
        # add users to correct slot

    def removing_user_process_slot(self, slot, prev_slot):
        pass
        # return to standby or move user(s) to correct slot
        
    def removing_user_process_clear(self, slot, ignore_me):
        pass
        # discharge user from system

    def removing_user_process_charge(self, slot, ignore_me):
        pass
        # add money owed to user account
        # sad trombone

    def clearing_debt_process_card_swipe(self, user, ignore_me):
        pass
        #chaching
        #clear user account

    def changing_pod_process_card_swipe(self, user, ignore_me):
        if user.proctor and not user in shop.pod_list:
            shop.pod_list.append(user)
            return self.standby_state
        elif user in shop.pod_list and len(shop.pod_list) > 1:
            shop.pod_list.remove(user)
            return self.standby_state
        elif user.proctor:
            return unauthorized("shop must have proctors")
        else:
            return unauthorized("invalid user")

    def closing_shop

def main():
    # Create a single input and a single output queue for all threads.
    dir_q = queue.Queue()
    event_q = queue.Queue()

    shop_user_database = shop_user.ShopUserDatabase(event_q)
    board = BoardFsm(event_q)

    thread = id_logger.IdLogger(shop_user_database)
    thread.start()

    while True:
        board.run_fsm()
        #board.standby_state()

if __name__== "__main__":
    main()                       
