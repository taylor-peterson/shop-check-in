# Key logging derived from
# http://antihackingtutorials.blogspot.com/2012/06/in-this-tutorial-we-will-show-you-how.html

import gspread
import pyHook
import pythoncom
import re
import win32api
import win32con
import win32console
import win32gui

idBuffer = []

# Login with your Google account
gc = gspread.login('hmc.machine.shop@gmail.com', 'orangecow')

# Open a worksheet from spreadsheet with one shot
wks = gc.open("Python Testing").sheet1

def OnKeyboardEvent(event):
    addCharToBuffer(chr(event.Ascii))

    idCheck = re.search(";[0-9]{10}\x00", ''.join(map(str, idBuffer)))
    if idCheck != None:
        idNumber = idCheck.group()[2:-2]
        print "Your ID number is: " + idNumber

        #shopUser = wks.find(idNumber)
        #print "Welcome, " + (wks.cell(shopUser.row, shopUser.col - 1).value)
        
    return True 

def addCharToBuffer(char):
    if len(idBuffer) >= 12:
        del idBuffer[0]
    idBuffer.append(char)


hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()
pythoncom.PumpMessages()







