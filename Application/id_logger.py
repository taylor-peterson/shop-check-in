import Queue
import re # Regular expressions
import threading

import gspread # Google Spreadsheets Python API

import pyHook # Callbacks for keyboard events
import pythoncom # Tie in to Windows events


class IdLogger(threading.Thread):
    """ A thread that listens to keyboard input for properly formatted
        IDs, looks up the ID in the Shop User Google Spreadsheet, and
        reports the result.

        Input is done by swiping a ID card.

        Output is done by placing tuples into the Queue passed in result_q.
        Each tuple is (user ID, eligibility to work). 
    """
    def __init__(self, result_q):
        super(IdLogger, self).__init__()
        self.result_q = result_q
        self.stoprequest = threading.Event()

        self.googleAccount =gspread.login(
            'hmc.machine.shop@gmail.com', 'orangecow')
        self.worksheet = self.googleAccount.open("Shop Users").sheet1
        self.idBuffer = []
        
    def run(self):
        hook_manager = pyHook.HookManager()
        hook_manager.KeyDown = self.OnKeyboardEvent
        hook_manager.HookKeyboard()
        
        pythoncom.PumpMessages()

    def join(self, timeout=None):
        self.stoprequest.set()
        super(IdLogger, self).join(timeout)

    def OnKeyboardEvent(self, event):
        self.addCharToBuffer(chr(event.Ascii))

        idCheck = re.search(";[0-9]{10}\x00", ''.join(map(str, self.idBuffer)))
        if idCheck != None:
            idNumber = idCheck.group()[2:-2]
            print "Your ID number is: " + idNumber

            t = threading.Thread(target = self.getShopUser, args = (idNumber, ))
            t.start()        
            
        return True

    def getShopUser(self, idNumber):
        shopUser = self.worksheet.find(idNumber)
        shopUserName = self.worksheet.cell(shopUser.row, 2).value
        print shopUserName

    def addCharToBuffer(self, char):
        if len(self.idBuffer) >= 12:
            del self.idBuffer[0]
        self.idBuffer.append(char)

def main():
    result_q = Queue.Queue() 
    
    thread = IdLogger(result_q=result_q)
    thread.start()

    while True:      
        pass

if __name__ == '__main__':
    main()

    
