import threading

import gspread # Google Spreadsheets Python API
import Queue as queue # Synchronized, multi-producer, multi-consumer queues

import event

COL_NAME = 1
COL_TEST_DATE = 2
COL_EMAIL= 4
COL_MONEY_OWED = 6
COL_PROCTOR = 7

UNAUTHORIZED = "unauthorized_user"

class ShopUserDatabase():
    """ Wrapper for getting data from the Google Spreadsheets Python API
    """
    def __init__(self, event_q):
        self.event_q = event_q
        self.googleAccount =gspread.login(
            'hmc.machine.shop@gmail.com', 'orangecow')
        self.worksheet = self.googleAccount.open("Shop Users").worksheet("Sorted")

    def getShopUser(self, id_number):
        user = ShopUser(id_number, UNAUTHORIZED)
        try:
            idnum = self.worksheet.find(id_number)
            row = idnum.row

            name = self.worksheet.cell(row, COL_NAME).value
            email = self.worksheet.cell(row, COL_EMAIL).value
            test_date = self.worksheet.cell(row, COL_TEST_DATE).value
            money_owed = self.worksheet.cell(row, COL_MONEY_OWED).value
            proctor = (self.worksheet.cell(row, COL_PROCTOR).value == "Yes")

            user = ShopUser(id_number, name, email, test_date, money_owed, proctor)
        except gspread.GSpreadException:
            pass
    
        card_swipe_event = event.Event(event.CARD_SWIPE, user)
        self.event_q.put(card_swipe_event)

class ShopUser():
    """ Encapsulates all data and operations on a shop user
    """
    def __init__(self,
                 id_number = 0,
                 name = "null",
                 email = "null",
                 test_date = 0,
                 money_owed = 0,
                 proctor = False):
        self.id_number = id_number
        self.name = name
        self.email = email
        self.test_date = test_date
        self.money_owed = money_owed
        self.proctor = proctor


        
