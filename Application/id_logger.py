import Queue as queue # Synchronized, multi-producer, multi-consumer queues
import re # Regular expressions
import threading

import gspread # Google Spreadsheets Python API
import pyHook # Callbacks for keyboard events
import pythoncom # Tie in to Windows events

import shop_user

COL_NAME = 1
COL_TEST_DATE = 2
COL_EMAIL= 4
COL_MONEY_OWED = 6


class IdLogger(threading.Thread):
    """ A thread that listens to keyboard input for properly formatted
        IDs, looks up the ID in the Shop User Google Spreadsheet, and
        reports the result.

        Input is done by swiping a ID card.

        Output is done by placing student objects into the Queue passed in result_q.
    """
    def __init__(self, result_q):        
        super(IdLogger, self).__init__()
        self.result_q = result_q

        self.googleAccount =gspread.login(
            'hmc.machine.shop@gmail.com', 'orangecow')
        self.worksheet = self.googleAccount.open("Shop Users").worksheet("Sorted")
        self.idBuffer = []

        if not self.isDaemon():
            print "You really should be running this as a daemon thread."
        
    def run(self):
        hook_manager = pyHook.HookManager()
        hook_manager.KeyDown = self.OnKeyboardEvent
        hook_manager.HookKeyboard()
        pythoncom.PumpMessages()

    def join(self, timeout=None):
        super(IdLogger, self).join(timeout)

    def OnKeyboardEvent(self, event):
        self.addCharToBuffer(chr(event.Ascii))

        idCheck = re.search(";[0-9]{10}\x00", ''.join(map(str, self.idBuffer)))
        if idCheck != None:
            id_number = idCheck.group()[2:-2]
            
            t = threading.Thread(target = self.getShopUser, args = (id_number, self.result_q, ))
            t.start()
            
        return True

    def getShopUser(self, id_number, result_q):
        idnum = self.worksheet.find(id_number)
        row = idnum.row

        name = self.worksheet.cell(row, COL_NAME).value
        email = self.worksheet.cell(row, COL_EMAIL).value
        test_date = self.worksheet.cell(row, COL_TEST_DATE).value
        money_owed = self.worksheet.cell(row, COL_MONEY_OWED).value

        user = shop_user.ShopUser(id_number, name, email, test_date, money_owed)
        self.result_q.put(user)

    def addCharToBuffer(self, char):
        if len(self.idBuffer) >= 12:
            del self.idBuffer[0]
        self.idBuffer.append(char)

def main():
    result_q = queue.Queue() 
    
    thread = IdLogger(result_q=result_q)
    thread.start()

    while True:
        try:
            result = result_q.get()
            print "ID number is %s, name is %s, email is %s, test date is %s, money owed: %s." % (
                result.id_number, result.name, result.email, result.test_date, result.money_owed)
        except queue.Empty:
            continue        

if __name__ == '__main__':
    main()


