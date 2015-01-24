import csv
import datetime

import gspread  # Google Spreadsheets Python API
import gspread.exceptions
import dateutil.parser

import event
import shop_user

COL_NAME = 1
COL_TEST_DATE = 2
COL_EMAIL = 4
COL_ID = 5
COL_DEBT = 6
COL_PROCTOR = 7

PROCTOR = "Yes"

DEBT_INCREMENT = 3

# TODO: make this work without internet or at least fail gracefully.
# If catch AuthenticationError or RequestError assume no internet and default to local copy?
    # gspread.AuthenticationError if login attempt fails
    # gspread.RequestError

# TODO: don't assume that the spreadsheet has valid data
    # If not, need to catch ValueError for the reformatting  in get_shop_user and do checks on all values
    # Raise invalid user error?


class ShopUserDatabase():

    def __init__(self, event_q):
        self._event_q = event_q
        self._shop_user_database = {}

        self._initialize_database()

    def _initialize_database(self):
        try:
            # populate dictionary using gspread
            pass
        except:  # internet down/spread failure
            # pull in version from csv
            pass
        else:
            # make list of users with unsynced flags in .csv
            # update dictionary accordingly
            self._synchronize_databases()
            # rewrite .csv from dictionary

    def _update_database(self):
        # same as initialize, but no need to overwrite if fail gspread
        pass

    def get_shop_user(self, id_number):
        try:
            return self._shop_user_database(id_number)
        except KeyError:
            try:
                # lookup in google spreadsheet
                pass
            except:  # internet down/gspread failure
                pass
            else:
                # add to user dictionar
                # add to .csv (on separate thread?)
                pass

    def _change_debt(self, user, new_debt):
        # change debt value in dictionary
        # spawn threads to change value in .csv and gspread
            # if fails to write to gspread, flag value in dictionary and .csv
        pass

    def _synchronize_databases(self, unsynced_users):
            try:
                # update gspread with unsynced users
                pass
            except: # gspread/internet failure
                pass
            else:
                # remove flag(s) from dictionary and .csv
                pass


class _ShopUserDatabaseExternal:

    def __init__(self):
        pass

    def get_shop_user_database(self):
        pass

    def update_user(self, id_number):
        pass



class ShopUserDatabaseGoogleSpreadsheet(_ShopUserDatabaseExternal):
    """ Interface for Google Spreadsheets. 
    """
    def __init__(self, event_q, spreadsheet="Shop Users", worksheet="Raw Data"):
        self._event_q = event_q

        try:
            google_account = gspread.login('hmc.machine.shop@gmail.com', 'orangecow')
        except gspread.AuthenticationError:
            raise gspread.AuthenticationError  # No internet access.
        else:
            self._worksheet = google_account.open(spreadsheet).worksheet(worksheet)

    def get_shop_user_database(self):
        pass

    def get_shop_user(self, id_number):
        try:
            cell_id_number = self._worksheet.find(id_number)
        except gspread.exceptions.CellNotFound:
            user = shop_user.ShopUser(id_number)
        else:
            row = cell_id_number.row

            name = self._worksheet.cell(row, COL_NAME).value
            email = self._worksheet.cell(row, COL_EMAIL).value
            cell_value_test_date = self._worksheet.cell(row, COL_TEST_DATE).value
            cell_value_debt = self._worksheet.cell(row, COL_DEBT).value
            proctorliness = self._worksheet.cell(row, COL_PROCTOR).value

            test_date = dateutil.parser.parse(cell_value_test_date)
            debt = int(float(cell_value_debt))
            proctor = (proctorliness == PROCTOR)

            user = shop_user.ShopUser(id_number, name, email, test_date, debt, proctor)

        card_swipe_event = event.Event(event.CARD_SWIPE, user)  # TODO: make user into list?
        self._event_q.put(card_swipe_event)

    def increase_debt(self, user):
        self._change_debt(user, user.debt + DEBT_INCREMENT)

    def clear_debt(self, user):
        self._chnage_debt(user, 0)

    def _change_debt(self, user, new_debt):
        try:
            id_num = self._worksheet.find(user.id_number)
        except gspread.exceptions.CellNotFound:
            raise NonexistentUserError
        else:
            try:
                self._worksheet.update_cell(id_num.row, COL_DEBT, new_debt)
            except gspread.UpdateCellError:
                raise gspread.UpdateCellError  # TODO: what to do here?
            else:
                user.debt = new_debt


class ShopUserDatabaseLocal(_ShopUserDatabaseExternal):

    def __init__(self):
        pass

    def get_shop_user_database(self):
        pass

    def get_shop_user(self, id_number):
        pass

    def increase_debt(self, user):
        pass

    def clear_debt(self, user):
        pass

class CsvTesting():


    def stripper(self, value):
        # Strip any whitespace from the left and right
        return value.strip()

    def to_float(self, value):
        return float(value)

    def to_date(self, value):
        # We expect dates like: "2013/05/23"
        datetime.datetime.strptime(value, '%Y/%m/%d').date()

    OPERATIONS = {
        'Product Name': [stripper],
        'Release Date': [stripper, to_date],
        'Price': [stripper, to_float]
    }

    def parse_csv(self, filepath):
        with open(filepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for column in row:
                    operations = CsvTesting.OPERATIONS[column]
                    value = row[column]
                    for op in operations:
                        value = op(value)
                    # Print the cleaned value or store it somewhere
                    print value


class NonexistentUserError(Exception):
    pass