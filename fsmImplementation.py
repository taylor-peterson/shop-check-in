import threading
import Queue as queue

import winsound

import Application.id_logger as id_logger
import Application.shop_user as shop_user
import Application.shop as shop



class BoardFsm():

    def __init__(self, event_q):
        self.shop = shop.Shop()
        self.event_q = event_q
        
    def standby(self, input):
        print "\nStanding by. The shop is currently " + self.shop.state + "."
        while True:
            event = self.event_q.get()

            if event[0] == "swipe":
                user = event[1]
                if user.proctor and self.shop.state == "closed":
                    return self.openShop(input)
                elif user in self.shop.pod_list:
                    return self.unlockBoard(input)
                else:
                    return self.unauthorized(input)
            elif event[0] == "button":
                pass
            else:
                return self.unauthorized(input)

    def unauthorized(self, input):
        print "\nUnauthorized use!"
        winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
        while True:
            userInput = raw_input("    press enter to return to standby.")
            return self.standby(input)

    def openShop(self, input):
        
        print "\nStarting up"
        while True:
            userInput = raw_input("    Type cancel or switch: ")
            if userInput == "cancel": # press cancel
                return self.standby(input)
            elif userInput == "switch": # flip missile switch to off
                self.shop.state = "open"
                self.shop.pod = True
                print "    Shop now open with proctor now on duty."
                # log event
                winsound.Beep(500,250) # old-school mac startup sound
                return self.standby(input)
            else:
                return self.unauthorized(input)

    def unlockBoard(self, input):
        print "\nUnlocking  Board"
        while True:
            userInput = raw_input("    cancel, swipe, remove, clear, pod, switch: ")
            if userInput == "cancel":
                return standby(input)
            elif userInput == "swipe": # swipe user id
                return addUser(input)
            elif userInput == "remove":
                return removeUser(input)
            elif userInput == "clear":
                return clearMoney(input)
            elif userInput == "pod":
                return changePod(input)
            elif userInput == "switch":
                return closeShop(input)
            else:
                print "        invalid input, try again"
                
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
                return standby(input)
            elif userInput == "slot":
                print "    User added to spot"
                return standby(input)
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
                return standby(input)
            elif userInput == "slot":
                print "        two users in spot"
                # chime
                return standby(input)
            else:
                print "        invalid input, try again"       

    def removeUser(input):
        print "\nRemoving user from shop"
        while True:
            userInput = raw_input("    reinsert, insert, clear, charge: ")
            if userInput == "reinsert": ## Card reinserted in same slot
                return standby(input) # abort removal
            elif userInput == "insert": ## Card inserted in different slot 
                print "        User changed machines" # Transfer user(s) to new machine
                return standby(input)
            elif userInput == "clear": # press clear
                print "        User allowed to leave shop" # discharge user from system
                # chime
                return standby(input)
            elif userInput == "charge": # press charge
                print "        Adding money owed to user account"
                # sad trombone
                return standby(input)
            else:
                print "        invalid, try again"

    def clearMoney(input):
        print "\nClearing user debt"
        while True:
            userInput = raw_input("    cancel, swipe: ")
            if userInput == "cancel":
                return standby(input)
            elif userInput == "swipe":
                print "        User account zeroed"
                # chaching sound effect
                return standby(input)
            else:
                print "        invalid, try again"

    def changePod(input):
        print "\nModifying proctor on duty status"
        while True:
            userInput = raw_input("    cancel, offDutyProctor, onDutyProctor: ")
            if userInput == "cancel":
                return standby(input)
            elif userInput == "offDutyProctor" and self.shop.state == "open":
                print "        proctor is now on duty"
                return standby(input)
            elif userInput == "onDutyProctor": # and another proctor on duty or shop closed
                print "        proctor is now off duty"
                return standby(input)
            elif userInput == "onDutyProctor": # and no other proctors and shop is open
                #Denied, buzz, display error "Shop must have proctor", wait for confirmation, return to process
                return standby(input)
            else:
                print "        invalid input, try again"

    def closeShop(input):
        print "\nClosing the shop"
        userInput = raw_input("    clear, occupied: ")
        if userInput == "clear":
            print "        Entering sleep mode... goodbye"
            return standby(input)
        elif userInput == "occupied":
            print "        You can't close the shop! Shop users still present!"
            return standby(input)

    # add clarification as to whether a state is automated or user-driven?
    # Todo: write unit tests
# Need to use daemon threads?
    # need to joing non-keylogging threads?
    # have proctor safety test update the proctorness column

##    def run(self):
##        # As long as we weren't asked to stop, try to take new tasks from the
##        # queue. The tasks are taken with a blocking 'get', so no CPU
##        # cycles are wasted while waiting.
##        # Also, 'get' is given a timeout, so stoprequest is always checked,
##        # even if there's nothing in the queue.
##        while not self.stoprequest.isSet():
##            try:
##                dirname = self.dir_q.get(True, 0.05) 
##                filenames = list(self._files_in_dir(dirname))
##                self.result_q.put((self.name, dirname, filenames))
##            except Queue.Empty:
##                continue


def main():
    # Create a single input and a single output queue for all threads.
    dir_q = queue.Queue()
    event_q = queue.Queue()

    shop_user_database = shop_user.ShopUserDatabase(event_q)
    board = BoardFsm(event_q)

    thread = id_logger.IdLogger(shop_user_database)
    thread.start()

    while True:
        board.standby("")
##        try:
##            result = result_q.get()
##            result = result[1]
##            print "ID number is %s, name is %s, email is %s, test date is %s, money owed: %s." % (
##                result.id_number, result.name, result.email, result.test_date, result.money_owed)
##        except queue.Empty:
##            continue 

if __name__== "__main__":
    main()

        
