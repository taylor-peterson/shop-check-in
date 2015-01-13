import gspread # Google Spreadsheets Python API
import pyHook # Provides callbacks for keyboard events
import pythoncom
import re # Regular expressions

import win32api
import win32con
import win32console
import win32gui

import threading

googleAccount = gspread.login('hmc.machine.shop@gmail.com', 'orangecow')
worksheet = googleAccount.open("Python Testing").sheet1
idBuffer = []

def OnKeyboardEvent(event):
    addCharToBuffer(chr(event.Ascii))

    idCheck = re.search(";[0-9]{10}\x00", ''.join(map(str, idBuffer)))
    if idCheck != None:
        idNumber = idCheck.group()[2:-2]
        print "Your ID number is: " + idNumber

        t = threading.Thread(target = getShopUser, args = (idNumber, ))
        t.start()        
        
    return True

def getShopUser(idNumber):
    shopUser = worksheet.find(idNumber)
    shopUserName = worksheet.cell(shopUser.row, shopUser.col - 1).value
    print shopUserName

def addCharToBuffer(char):
    if len(idBuffer) >= 12:
        del idBuffer[0]
    idBuffer.append(char)

def main():
    # Start up the key logger
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()

if __name__ == "__main__":
    main()

# Todo: write unit tests
