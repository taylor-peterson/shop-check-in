import threading

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



REAL_USER_ROW = 7
REAL_USER_ID = "7777777"
REAL_USER_NAME = "Testy the Testee"
REAL_USER_DEBT = 3

FAKE_USER_ROW = 6
FAKE_USER_ID = "666"

class TestShopUserDatabase:

    def setup_method(self, method):
        event_q = queue.Queue()
        shop_user_database = ShopUserDatabase(event_q, "Python Testing")
        
        #try: except?
        shop_user_database.worksheet.update_cell(REAL_USER_ROW, COL_ID, REAL_USER_ID)
        shop_user_database.worksheet.update_cell(REAL_USER_ROW, COL_NAME, REAL_USER_NAME)
        shop_user_database.worksheet.update_cell(REAL_USER_ROW, COL_DEBT, REAL_USER_DEBT)

        # add check to make sure fake person isn't there
        # self.worksheet.find(FAKE_USER_ID)

        # make the above series of updates run as one operation

    def test_get_real_user(self):
        event_q = queue.Queue()
        shop_user_database = ShopUserDatabase(event_q, "Python Testing")

        shop_user_database.getShopUser(REAL_USER_ID)
        user = event_q.get().data
        assert user.name == REAL_USER_NAME

    def test_get_nonexistent_user(self):
        event_q = queue.Queue()
        shop_user_database = ShopUserDatabase(event_q, "Python Testing")
        
        shop_user_database.getShopUser(FAKE_USER_ID)
        assert event_q.get().data.name == UNAUTHORIZED

    def test_increase_debt(self):
        event_q = queue.Queue()
        shop_user_database = ShopUserDatabase(event_q, "Python Testing")

        shop_user_database.getShopUser(REAL_USER_ID)
        user = event_q.get().data

        user_debt = user.debt + 3
        user = shop_user_database.increase_debt(user)
        assert user_debt == user.debt

    def test_clear_debt(self):
        event_q = queue.Queue()
        shop_user_database = ShopUserDatabase(event_q, "Python Testing")

        shop_user_database.getShopUser(REAL_USER_ID)
        user = event_q.get().data

        user = shop_user_database.clear_debt(user)
        assert user.debt == 0
