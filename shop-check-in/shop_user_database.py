import gspread  # Google Spreadsheets Python API

import dateutil.parser

import event
import shop_user

COL_NAME = 1
COL_TEST_DATE = 2
COL_EMAIL = 4
COL_ID = 5
COL_DEBT = 6
COL_PROCTOR = 7

# TODO: make this work without internet or at least fail gracefully.
# TODO: error handling on inputs
# TODO: have increase_debt and clear_debt return new users?
# TODO: gspread exceptions raised for other reasons than nonexistent user!


class ShopUserDatabase():
    """ Interface for Google Spreadsheets. 
    """
    def __init__(self, event_q, spreadsheet="Shop Users"):
        self._event_q = event_q

        google_account = gspread.login('hmc.machine.shop@gmail.com', 'orangecow')
        self._worksheet = google_account.open(spreadsheet).worksheet("Sorted")

    def get_shop_user(self, id_number):
        user = shop_user.ShopUser(id_number, shop_user.NONEXISTENT_USER)
        try:
            id_num = self._worksheet.find(id_number)
            row = id_num.row

            name = self._worksheet.cell(row, COL_NAME).value
            email = self._worksheet.cell(row, COL_EMAIL).value
            test_date_str = self._worksheet.cell(row, COL_TEST_DATE).value  # TODO: remove str from name?
            debt = int(float(self._worksheet.cell(row, COL_DEBT).value))
            proctor = (self._worksheet.cell(row, COL_PROCTOR).value == "Yes")

            test_date = dateutil.parser.parse(test_date_str)  # invalid date raises ValueError

            user = shop_user.ShopUser(id_number, name, email, test_date, debt, proctor)
        except gspread.GSpreadException:
            pass
    
        card_swipe_event = event.Event(event.CARD_SWIPE, user)
        self._event_q.put(card_swipe_event)

    def increase_debt(self, user):
        try:
            id_num = self._worksheet.find(user.id_number)
        except gspread.GSpreadException:
            raise NonexistentUserError
        else:
            user._debt += 3
            self._worksheet.update_cell(id_num.row, COL_DEBT, user._debt)

        return user

    def clear_debt(self, user):
        try:
            id_num = self._worksheet.find(user.id_number)
        except gspread.GSpreadException:
            raise NonexistentUserError
        else:
            user._debt = 0
            self._worksheet.update_cell(id_num.row, COL_DEBT, user._debt)

        return user        

# TODO: if the actual class can't work without internet, make this work on a local copy of the spreadsheet


class ShopUserDatabaseSpoof(ShopUserDatabase):
    """ For testing purposes only.
        Having this allows for quicker tests by avoiding the need to
        unnecessarily connect to Google Drive.
    """

    def __init__(self):
        pass

    def get_shop_user(self, id_number):
        pass

    def increase_debt(self, user):
        pass

    def clear_debt(self, user):
        pass


class NonexistentUserError(Exception):
    pass