import gspread

import shop_user_database
import sample_users

REAL_USER_ROW = 7
FAKE_USER_ROW = 6


class TestShopUserDatabase(object):

    # TODO: add tests for __init__ without internet - how to test this automatically?
        #

    def setup_class(cls):
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        
        try:
            shop_user_db._worksheet.update_cell(
                REAL_USER_ROW, shop_user_database.COL_ID, sample_users.USER_CERTIFIED.id_number)
            shop_user_db._worksheet.update_cell(
                REAL_USER_ROW, shop_user_database.COL_NAME, sample_users.USER_CERTIFIED._name)
            shop_user_db._worksheet.update_cell(
                REAL_USER_ROW, shop_user_database.COL_EMAIL, sample_users.USER_CERTIFIED._email)
            shop_user_db._worksheet.update_cell(
                REAL_USER_ROW, shop_user_database.COL_TEST_DATE, sample_users.USER_CERTIFIED._test_date)
            shop_user_db._worksheet.update_cell(
                REAL_USER_ROW, shop_user_database.COL_DEBT, sample_users.USER_CERTIFIED.debt)
            shop_user_db._worksheet.update_cell(
                REAL_USER_ROW, shop_user_database.COL_PROCTOR, sample_users.USER_CERTIFIED._proctor)
        except gspread.UpdateCellError:
            assert False  # Failed to initialize database.

    def test_get_real_user(self):
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()

        shop_user_db.get_shop_user(sample_users.USER_CERTIFIED.id_number)
        user = event_q.get().data

        assert user == sample_users.USER_CERTIFIED

    def test_get_nonexistent_user(self):
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        
        shop_user_db.get_shop_user(sample_users.USER_INVALID.id_number)
        user = event_q.get().data

        assert user == sample_users.USER_INVALID

    def test_increase_debt_success(self):
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()

        shop_user_db.get_shop_user(sample_users.USER_CERTIFIED.id_number)
        user = event_q.get().data

        user_debt = user.debt + shop_user_database.DEBT_INCREMENT
        shop_user_db.increase_debt(user)

        assert user_debt == user.debt

    def test_increase_debt_failure(self):
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()

        shop_user_db.get_shop_user(sample_users.USER_INVALID.id_number)
        user = event_q.get().data

        try:
            shop_user_db.increase_debt(user)
        except shop_user_database.NonexistentUserError:
            assert True
        else:
            assert False

    def test_clear_debt_success(self):
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()

        shop_user_db.get_shop_user(sample_users.USER_CERTIFIED.id_number)
        user = event_q.get().data
        shop_user_db.increase_debt(user)
        shop_user_db.clear_debt(user)

        assert user.debt == 0

    def test_clear_debt_failure(self):
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()

        shop_user_db.get_shop_user(sample_users.USER_INVALID.id_number)
        user = event_q.get().data

        try:
            shop_user_db.clear_debt(user)
        except shop_user_database.NonexistentUserError:
            assert True
        else:
            assert False