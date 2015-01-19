import Queue as queue

import shop_user
import shop_user_database
import sample_users

REAL_USER_ROW = 7
REAL_USER_ID = "7777777"
REAL_USER_NAME = "Joe Schmoe"
REAL_USER_EMAIL = "email"
REAL_USER_TEST_DATE = sample_users.VALID_TEST_DATE
REAL_USER_DEBT = 0
REAL_USER_PROCTOR = "No"

FAKE_USER_ROW = 6
FAKE_USER_ID = "666"


class TestShopUserDatabase:

    # TODO: add tests for other branching possibilities. 

    def setup_method(self, method):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")
        
        # TODO: try: except?
        # TODO: add missing column data. 
        shop_user_db._worksheet.update_cell(REAL_USER_ROW, shop_user_database.COL_ID, REAL_USER_ID)
        shop_user_db._worksheet.update_cell(REAL_USER_ROW, shop_user_database.COL_NAME, REAL_USER_NAME)
        shop_user_db._worksheet.update_cell(REAL_USER_ROW, shop_user_database.COL_DEBT, REAL_USER_DEBT)

        # TODO: add check to make sure fake person isn't there
        # TODO: self.worksheet.find(FAKE_USER_ID)

        # TODO: make the above series of updates run as one operation

    def test_get_real_user(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.get_shop_user(REAL_USER_ID)
        user = event_q.get().data
        assert user._name == REAL_USER_NAME

    def test_get_nonexistent_user(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")
        
        shop_user_db.get_shop_user(FAKE_USER_ID)
        assert event_q.get().data._name == shop_user.NONEXISTENT_USER

    def test_increase_debt_success(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.get_shop_user(REAL_USER_ID)
        user = event_q.get().data

        user_debt = user._debt + 3
        user = shop_user_db.increase_debt(user)
        assert user_debt == user._debt

    def test_increase_debt_failure(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.get_shop_user(FAKE_USER_ID)
        user = event_q.get().data

        try:
            shop_user_db.increase_debt(user)
        except shop_user_database.NonexistentUserError:
            assert True
        else:
            assert False

    def test_clear_debt_success(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.get_shop_user(REAL_USER_ID)
        user = event_q.get().data

        user = shop_user_db.clear_debt(user)
        assert user._debt == 0

    def test_clear_debt_failure(self):
        event_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabase(event_q, "Python Testing")

        shop_user_db.get_shop_user(FAKE_USER_ID)
        user = event_q.get().data

        try:
            shop_user_db.clear_debt(user)
        except shop_user_database.NonexistentUserError:
            assert True
        else:
            assert False