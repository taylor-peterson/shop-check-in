import Queue as queue

import shop_user
import shop_user_database

REAL_USER_ROW = 7
REAL_USER_ID = "7777777"
REAL_USER_NAME = "Testy the Testee"
REAL_USER_EMAIL = "testy@gmail.com"
REAL_USER_TEST_DATE = "5/25/07"
REAL_USER_DEBT = 3
REAL_USER_PROCTOR = "No"

FAKE_USER_ROW = 6
FAKE_USER_ID = "666"

class TestShopUserDatabase:

    # TODO: add tests for other branching possibilities. 

    def setup_method(self, method):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")
        
        #try: except?
        # TODO: add missing column data. 
        shop_user_db.worksheet.update_cell(REAL_USER_ROW, shop_user_database.COL_ID, REAL_USER_ID)
        shop_user_db.worksheet.update_cell(REAL_USER_ROW, shop_user_database.COL_NAME, REAL_USER_NAME)
        shop_user_db.worksheet.update_cell(REAL_USER_ROW, shop_user_database.COL_DEBT, REAL_USER_DEBT)

        # add check to make sure fake person isn't there
        # self.worksheet.find(FAKE_USER_ID)

        # make the above series of updates run as one operation

    def test_get_real_user(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.getShopUser(REAL_USER_ID)
        user = event_q.get().data
        assert user.name == REAL_USER_NAME

    def test_get_nonexistent_user(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")
        
        shop_user_db.getShopUser(FAKE_USER_ID)
        assert event_q.get().data.name == UNAUTHORIZED

    def test_increase_debt_success(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.getShopUser(REAL_USER_ID)
        user = event_q.get().data

        user_debt = user.debt + 3
        user = shop_user_db.increase_debt(user)
        assert user_debt == user.debt

    def test_increase_debt_failure(self):
        assert True == False

    def test_clear_debt_success(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.getShopUser(REAL_USER_ID)
        user = event_q.get().data

        user = shop_user_db.clear_debt(user)
        assert user.debt == 0

    def test_clear_debt_failure(self):
        assert True == False
