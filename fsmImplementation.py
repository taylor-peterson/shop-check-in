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
                      {event.CARD_SWIPE_KEY : self.closed_process_card_swipe}),
            
            OPENING : ("Starting up!\n\rType cancel or flip_switch_off: ",
                       {"cancel" : self.standby_state,
                        "flip_switch_off" : self.on_shop_open}),

            STANDBY : ("Shop open. Board locked\n\rPOD swipe to unlock.",
                      {event.CARD_SWIPE_KEY : self.standby_process_card_swipe}),

            UNLOCKED : ("Board Unlcked.\n\rAll inputs available.",
                        {"cancel" : self.standby_state,
                         event.CARD_SWIPE_KEY : self.addUser,
                         "card_remove" : self.removeUser,
                         "clear_money" : self.clearMoney,
                         "change_pod" : self.changePod,
                         "flip_switch_on" : self.closeShop}),

            ADDING_USER

            REMOVING_USER

            CLEARING_DEBT

            CHANGING_POD

            CLOSING


        self.unauthorized_messages = {
            "default" : DEFAULT_ERROR_MESSAGE,
            "invalid user" : "User does not have permissions for that action.",
            "invalid card swipe" : "ERR - Ignoring swipe. Please confirm."}

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

    def closed_process_card_swipe(self, user, ignore_me):
        if user.proctor:
            return (OPENING, user)
        else:
            return self.unauthorized("invalid user")

    def on_shop_open(self, ignore_me, user):
        self.shop.state = "open"
        self.shop.pod_list.append(user)
        print "    Shop now open with proctor now on duty."
        # log event
        winsound.Beep(500,250) # old-school mac startup sound
        return self.standby_state()
    

    def standby_process_card_swipe(self, user):
        if user.proctor and self.shop.state == "closed":
            return self.openShop(user)
        elif user in self.shop.pod_list:
            return self.unlockBoard(input)
        else:
            return self.unauthorized("invalid user")

    # ========================================   

    def unauthorized(self, error_message = "default"):
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)

        print self.unauthorized_messages.get(error_message, DEFAULT_ERROR_MESSAGE)
        
        userInput = raw_input("    press enter to return to standby.")
        return self.standby_state()



                
    def addUser(input):
        print "\nAdding user to shop"
        while True:
            userInput = raw_input("    error, cleared: ")

            if userInput == "error": # user not shop certified or owes money
                winsound.Beep(500, 250)
                # display error)
                return unauthorized(input)
            elif userInput == "cleared":
                return addUserOrAssignMachine(input)
            else:
                print "        invalid input, try again"

    def addUserOrAssignMachine(input):
        print "\nAdding another user or assigning user to machine"
        while True:
            userInput = raw_input("    cancel, slot, cardRemoved, unauthorizedSwipe, verifiedSwipe: ")
            if userInput == "cancel":
                return standby_state()
            elif userInput == "slot":
                print "    User added to spot"
                return standby_state()
            elif userInput == "cardRemoved":
                # buzz
                print "        display error - reinsert card"
                input = raw_input("    confirm, reinsert: ")
                if input == "confirm":
                    print "        silly user - send tsk email"
                elif input == "reinsert":
                    print "        continuing..."
            elif userInput == "unauthorizedSwipe":
                #buzz
                print "unauthorized user"
                raw_input("    press enter to continue")
            elif userInput == "verifiedSwipe":
                print "         additional shop user added"
                return assignTwoUsersToMachine(input)    
            else:
                print "        invalid input, try again"

    def assignTwoUsersToMachine(input):
        print "\nAssigning two users"
        while True:
            userInput = raw_input("    cancel, slot")
            if userInput == "cancel":
                return standby_state()
            elif userInput == "slot":
                print "        two users in spot"
                # chime
                return standby_state()
            else:
                print "        invalid input, try again"       

    def removeUser(input):
        print "\nRemoving user from shop"
        while True:
            userInput = raw_input("    reinsert, insert, clear, charge: ")
            if userInput == "reinsert": ## Card reinserted in same slot
                return standby_state() # abort removal
            elif userInput == "insert": ## Card inserted in different slot 
                print "        User changed machines" # Transfer user(s) to new machine
                return standby_state()
            elif userInput == "clear": # press clear
                print "        User allowed to leave shop" # discharge user from system
                # chime
                return standby_state()
            elif userInput == "charge": # press charge
                print "        Adding money owed to user account"
                # sad trombone
                return standby_state()
            else:
                print "        invalid, try again"

    def clearMoney(input):
        print "\nClearing user debt"
        while True:
            userInput = raw_input("    cancel, swipe: ")
            if userInput == "cancel":
                return standby_state()
            elif userInput == "swipe":
                print "        User account zeroed"
                # chaching sound effect
                return standby_state()
            else:
                print "        invalid, try again"

    def changePod(input):
        print "\nModifying proctor on duty status"
        while True:
            userInput = raw_input("    cancel, offDutyProctor, onDutyProctor: ")
            if userInput == "cancel":
                return standby_state()
            elif userInput == "offDutyProctor" and self.shop.state == "open":
                print "        proctor is now on duty"
                return standby_state()
            elif userInput == "onDutyProctor": # and another proctor on duty or shop closed
                print "        proctor is now off duty"
                return standby_state()
            elif userInput == "onDutyProctor": # and no other proctors and shop is open
                #Denied, buzz, display error "Shop must have proctor", wait for confirmation, return to process
                return standby_state()
            else:
                print "        invalid input, try again"

    def closeShop(input):
        print "\nClosing the shop"
        userInput = raw_input("    clear, occupied: ")
        if userInput == "clear":
            print "        Entering sleep mode... goodbye"
            return standby_state()
        elif userInput == "occupied":
            print "        You can't close the shop! Shop users still present!"
            return standby_state()

    # add clarification as to whether a state is automated or user-driven?
        # state changes occur only after user input
    
    # Todo: write unit tests
# Need to use daemon threads?
    # need to joing non-keylogging threads?
    # have proctor safety test update the proctorness column

    # wrap state handlers back in while trues, then add a third data member to the tuples
    # that details how to get back to the desired state should things be done out of order. 


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


                              
                            

##        self.shop_closed_actions = {
##            "card_swipe" : self.shop_closed_process_card_swipe}
##
##        self.standby_actions = {
##            "card_swipe" : self.standby_process_card_swipe}
        
##        self.open_shop_actions = {
##            "cancel" : self.standby_state,
##            "flip_switch_off" : self.on_shop_open}

##        self.unlock_board_actions = {
##            "cancel" : self.standby_state,
##            "card_swipe" : self.addUser,
##            "card_remove" : self.removeUser,
##            "clear_money" : self.clearMoney,
##            "change_pod" : self.changePod,
##            "flip_switch_on" : self.closeShop}
                        

    # =====================================

##    def openShop(self, input):
##        userInput = raw_input("\nStarting up! Type cancel or flip_switch_off: ")
##        return self.open_shop_actions.get(userInput, self.unauthorized)()
                


    # ========================================

##    def standby_state(self):
##        print "\nStanding by. The shop is currently."
##
##        event = self.event_q.get()
##
##        try:
##            self.standby_actions[event.key](event.data)
##        except KeyError:
##            self.unauthorized(event.error_msg)

##    def unlockBoard(self, input):
##        print "\nUnlocking  Board"
##        userInput = raw_input(
##            "You can: cancel, card_swipe, card_remove, clear_money, change_pod, or flip_switch_on")
##        return self.unlock_board_actions.get(userInput, self.unauthorized)()
