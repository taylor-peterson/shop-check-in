import gspread # Google Spreadsheets Python API
import Queue as queue # Synchronized, multi-producer, multi-consumer queues
import datetime

import dateutil.parser

import event
import shop_user

COL_NAME = 1
COL_TEST_DATE = 2
COL_EMAIL= 4
COL_ID = 5
COL_DEBT = 6
COL_PROCTOR = 7

# TODO: make this work without internet or at least fail gracefully.
# TODO: error handling on inputs
class ShopUserDatabase():
    """ Interface for Google Spreadsheets. 
    """
    def __init__(self, event_q, spreadsheet = "Shop Users"):
        self.event_q = event_q
        self.googleAccount =gspread.login(
            'hmc.machine.shop@gmail.com', 'orangecow')
        self.worksheet = self.googleAccount.open(spreadsheet).worksheet("Sorted")

    def getShopUser(self, id_number):
        user = ShopUser(id_number, UNAUTHORIZED)
        try:
            idnum = self.worksheet.find(id_number)
            row = idnum.row

            name = self.worksheet.cell(row, COL_NAME).value
            email = self.worksheet.cell(row, COL_EMAIL).value
            test_date_str = self.worksheet.cell(row, COL_TEST_DATE).value
            debt = int(float(self.worksheet.cell(row, COL_DEBT).value))
            proctor = (self.worksheet.cell(row, COL_PROCTOR).value == "Yes")

            test_date = dateutil.parser.parse(test_date_str) # invalid date raises ValueError

            user = ShopUser(id_number, name, email, test_date, debt, proctor)
        except gspread.GSpreadException:
            pass
    
        card_swipe_event = event.Event(event.CARD_SWIPE, user)
        self.event_q.put(card_swipe_event)

    def increase_debt(self, user):
        try:
            idnum = self.worksheet.find(user.id_number)
            row = idnum.row

            user.debt += 3
            self.worksheet.update_cell(row, COL_DEBT, user.debt)
        except gspread.GSpreadException:
            raise shop_user.UnauthorizedUserError

        return user

    def clear_debt(self, user):
        try:
            idnum = self.worksheet.find(user.id_number)
            row = idnum.row

            user.debt = 0
            self.worksheet.update_cell(row, COL_DEBT, user.debt)
        except gspread.GSpreadException:
            raise shop_user.UnauthorizedUserError

        return user        

# if the actual class can't work without internet, make this
# work on a local copy of the spreadsheet
class ShopUserDatabaseSpoof(ShopUserDatabase):
    ''' For testing purposes only.
        Having this allows for quicker tests by avoiding the need to
        unnecessarily connect to Google Drive.
    '''

    def __init__(self):
        pass

    def getShopUser(self, id_number):
        pass

    def increase_debt(self, user):
        pass

    def clear_debt(self, user):
        pass
