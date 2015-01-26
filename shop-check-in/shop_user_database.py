import cPickle

import gspread
import gspread.exceptions

import shop_user

DEBT_INCREMENT = 3


class ShopUserDatabase(object):

    def __init__(self):
        self._shop_user_database = {}
        self._out_of_sync_users = []

        self._shop_user_database_google_worksheet = None
        self._connect_to_google_spreadsheet()

        self._shop_user_database_local = _ShopUserDatabaseLocal()

        self._initialize_database()

    def __del__(self):
        self._shop_user_database_local.dump_shop_user_database(self._shop_user_database)
        self._shop_user_database_local.dump_out_of_sync_users(self._out_of_sync_users)

    def get_shop_user(self, id_number):
        try:
            return self._shop_user_database[id_number]
        except KeyError:
            return self._get_shop_user_from_google_spreadsheet()  # Raises NonexistentUserError if not found.

    def increase_debt(self, user):
        self._change_debt(user, user.debt + DEBT_INCREMENT)

    def clear_debt(self, user):
        self._change_debt(user, 0)

    def _change_debt(self, user, new_debt):
        try:
            self._shop_user_database[user.id_number][shop_user.DEBT] = new_debt
        except KeyError:
            raise NonexistentUserError
        else:
            self._out_of_sync_users.append(user)
            self._synchronize_databases()

    def _connect_to_google_spreadsheet(self):
        if self._shop_user_database_google_worksheet is None:
            try:
                self._shop_user_database_google_worksheet = _ShopUserDatabaseGoogleWorksheet()
            except (gspread.AuthenticationError, IOError):
                raise _CannotAccessGoogleSpreadsheetsError
        else:
            try:
                self._shop_user_database_google_worksheet.test_connection()
            except IOError:
                self._shop_user_database_google_worksheet = None
                self._connect_to_google_spreadsheet()

    def _get_shop_user_from_google_spreadsheet(self, id_number):
        try:
            self._connect_to_google_spreadsheet()
        except _CannotAccessGoogleSpreadsheetsError:
            raise NonexistentUserError

        try:
            user_data = self._shop_user_database_google_worksheet.get_shop_user_data(id_number)
        except (gspread.exceptions.CellNotFound, IOError):
            raise NonexistentUserError
        else:
            user = shop_user.ShopUser(user_data)
            self._shop_user_database[user.id_number] = user

        return user

    def _initialize_database(self):
        try:
            self._connect_to_google_spreadsheet()
            self._shop_user_database = self._shop_user_database_google_worksheet.load_shop_user_database()
        except (gspread.GSpreadException, _CannotAccessGoogleSpreadsheetsError):
            self._shop_user_database = self._shop_user_database_local.load_shop_user_database()
        else:
            self._out_of_sync_users = self._shop_user_database_local.load_out_of_sync_users()
            self._synchronize_databases()

    def _synchronize_databases(self):
            try:
                for user in self._out_of_sync_users:
                    self._shop_user_database_google_worksheet.update_user(user)
            except (gspread.GSpreadException, IOError):
                pass
            else:
                self._out_of_sync_users = []


class ShopUserDatabaseTesting(ShopUserDatabase):

    def __init__(self):
        super(ShopUserDatabaseTesting, self).__init__()
        self._shop_user_database_google_worksheet = _ShopUserDatabaseGoogleWorksheet("Python Testing")


class _ShopUserDatabaseGoogleWorksheet(object):

    def __init__(self, spreadsheet="Shop Users", worksheet="Raw Data"):
        google_account = gspread.login('hmc.machine.shop@gmail.com', 'orangecow')
        self._worksheet = google_account.open(spreadsheet).worksheet(worksheet)

    def get_shop_user_database(self):
        raw_data = self._worksheet.get_all_values()
        shop_users = [shop_user.ShopUser(shop_user_data) for shop_user_data in raw_data]
        shop_user_database = {user.id_number: user for user in shop_users}
        return shop_user_database

    def get_shop_user_data(self, id_number):
        cell_id_number = self._worksheet.find(id_number)
        return self._worksheet.row_values(cell_id_number.row)

    def test_connection(self):
        self._worksheet.cell(0, 0)

    def update_user(self, user):
        self._change_debt(user)

    def _change_debt(self, id_number, new_debt):
        row = self._worksheet.find(id_number).row
        col = shop_user.DEBT + 1  # gspread is 1-indexed, shop_users are 0-indexed.
        self._worksheet.update_cell(row, col, new_debt)


class _ShopUserDatabaseLocal(object):

    def __init__(self,
                 database_file_path="shop_user_database_local.pkl",
                 out_of_date_users_file_path="out_of_date_users.pkl"):
        self._database_file_path = database_file_path
        self._out_of_date_users_file_path = out_of_date_users_file_path

    def load_shop_user_database(self):
        return self._load_file(self._database_file_path)

    def load_out_of_sync_users(self):
        return self._load_file(self._out_of_date_users_file_path)

    def dump_shop_user_database(self, database):
        self._dump_file(self._database_file_path, database)

    def dump_out_of_sync_users(self, out_of_sync_users):
        self._dump_file(self._out_of_date_users_file_path, out_of_sync_users)

    def _load_file(self, file_path):
        with open(file_path, 'rb') as file_:
            return cPickle.load(file_)

    def _dump_file(self, file_path, dumpee):
        self._erase_file(file_path)

        with open(file_path, 'wb') as file_:
            cPickle.dump(dumpee, file_)

    def _erase_file(self, file_path):
        with open(file_path, "wb") as file_:
            file_.truncate()


class NonexistentUserError(Exception):
    pass


class _CannotAccessGoogleSpreadsheetsError(Exception):
    pass