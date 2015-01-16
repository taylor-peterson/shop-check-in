import gspread # Google Spreadsheets Python API
import Queue as queue # Synchronized, multi-producer, multi-consumer queues

import event

COL_NAME = 1
COL_TEST_DATE = 2
COL_EMAIL= 4
COL_ID = 5
COL_DEBT = 6
COL_PROCTOR = 7

UNAUTHORIZED = "unauthorized_user"

class ShopUser():
    """ A struct to store a shop user's data.
        Note that all actions on shop users must go through the database.
    """
    def __init__(self,
                 id_number = 0,
                 name = "null",
                 email = "null",
                 test_date = 0,
                 debt = 0,
                 proctor = False):
        self.id_number = id_number
        self.name = name
        self.email = email
        self.test_date = test_date
        self.debt = debt
        self.proctor = proctor

        
# TODO: make this work without internet or at least fail gracefully. 
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
            test_date = self.worksheet.cell(row, COL_TEST_DATE).value
            debt = int(float(self.worksheet.cell(row, COL_DEBT).value))
            proctor = (self.worksheet.cell(row, COL_PROCTOR).value == "Yes")

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
            user = ShopUser(id_number, UNAUTHORIZED)

        return user

    def clear_debt(self, user):
        try:
            idnum = self.worksheet.find(user.id_number)
            row = idnum.row

            user.debt = 0
            self.worksheet.update_cell(row, COL_DEBT, user.debt)
        except gspread.GSpreadException:
            user = ShopUser(id_number, UNAUTHORIZED)

        return user

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
