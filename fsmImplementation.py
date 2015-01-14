import winsound

sampleID = ";0401551811?"
shopState = "closed"
proctorOnDuty = False

def standby(input):
    print "\nStanding by. The shop is currently " + shopState + "."
    while True:
        userInput = raw_input("    proctorSwipe or podSwipe: ")
        
        if userInput == "proctorSwipe" and shopState == "closed":
            return openShop(input)
        elif userInput == "podSwipe" and shopState == "open":
            return unlockBoard(input)
        else:
            return unauthorized(input)

def unauthorized(input):
    print "\nUnauthorized use!"
    winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)
    while True:
        userInput = raw_input("    press enter to return to standby.")
        return standby(input)

def openShop(input):
    global shopState
    global proctorOnDuty
    
    print "\nStarting up"
    while True:
        userInput = raw_input("    Type cancel or switch: ")
        if userInput == "cancel": # press cancel
            return standby(input)
        elif userInput == "switch": # flip missile switch to off
            global shopState
            shopState = "open"
            proctorOnDuty = True
            print "    Shop now open with proctor now on duty."
            # log event
            winsound.Beep(500,250) # old-school mac startup sound
            return standby(input)
        else:
            return unauthorized(input)

def unlockBoard(input):
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
        elif userInput == "offDutyProctor" and shopState == "open":
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

if __name__== "__main__":
    standby("")
