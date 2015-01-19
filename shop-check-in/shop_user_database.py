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


class ShopUserDatabase():
    """ Interface for Google Spreadsheets. 
    """
    def __init__(self, event_q, spreadsheet="Shop Users"):
        self._event_q = event_q

        googleAccount = gspread.login('hmc.machine.shop@gmail.com', 'orangecow')
        self._worksheet = googleAccount.open(spreadsheet).worksheet("Sorted")

    def get_shop_user(self, id_number):
        user = shop_user.ShopUser(id_number, shop_user.UNAUTHORIZED)
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
            row = id_num.row

            user.debt += 3
            self._worksheet.update_cell(row, COL_DEBT, user.debt)
        except gspread.GSpreadException:
            raise shop_user.UnauthorizedUserError

        return user

    def clear_debt(self, user):
        try:
            id_num = self._worksheet.find(user.id_number)
            row = id_num.row

            user.debt = 0
            self._worksheet.update_cell(row, COL_DEBT, user.debt)
        except gspread.GSpreadException:
            raise shop_user.UnauthorizedUserError

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
