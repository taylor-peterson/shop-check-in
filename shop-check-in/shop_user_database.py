import cPickle
import os
import sys

import json
from oauth2client.client import SignedJwtAssertionCredentials

import gspread
import gspread.exceptions

import shop_user
import shop_check_in_exceptions

DEBT_INCREMENT = 3

SPREADSHEET = "Shop Users"
SPREADSHEET_TESTING = "Shop Users Testing"
WORKSHEET = "Raw Data"

PATH_LOCAL_DATABASE = "resources\\shop_user_database_local_test.pkl"
PATH_OUT_OF_SYNC_USERS = "resources\\out_of_sync_users_test.pkl"
PATH_TESTING_LOCAL_DATABASE = "resources\\shop_user_database_local_test.pkl"
PATH_TESTING_OUT_OF_SYNC_USERS = "resources\\out_of_sync_users_test.pkl"
PATH_LOGIN_INFO = "resources\\sensitive_info.txt"


class ShopUserDatabase(object):

    def __init__(self, spreadsheet_name=SPREADSHEET,
                 path_local_database=PATH_LOCAL_DATABASE,
                 path_out_of_sync_users=PATH_OUT_OF_SYNC_USERS):
        self._shop_user_database = {}
        self._out_of_sync_users = []
        self._spreadsheet_name = spreadsheet_name

        self._shop_user_database_google_worksheet = None
        self._shop_user_database_local = _ShopUserDatabaseLocal(path_local_database, path_out_of_sync_users)

        self._initialize_database()

    def __del__(self):
        self._shop_user_database_local.dump_data(self._shop_user_database, self._out_of_sync_users)

    def get_shop_user(self, id_number):
        try:
            return self._shop_user_database[id_number]
        except KeyError:
            return self._get_shop_user_from_google_spreadsheet(id_number)

    def increase_debt(self, user):
        self._change_debt(user, user.debt + DEBT_INCREMENT)

    def clear_debt(self, user):
        self._change_debt(user, 0)

    def _change_debt(self, user, new_debt):
        try:
            self._shop_user_database[user.id_number].debt = new_debt
        except KeyError:
            exc_traceback = sys.exc_traceback
            raise shop_check_in_exceptions.NonexistentUserError, None, exc_traceback
        else:
            self._out_of_sync_users.append(user)
            self._synchronize_databases()

    def _connect_to_google_spreadsheet(self):
        if self._shop_user_database_google_worksheet is None:
            try:
                print "Trying to load the spreadsheet",self._spreadsheet_name
                self._shop_user_database_google_worksheet = _ShopUserDatabaseGoogleWorksheet(self._spreadsheet_name)
                print "Spreadsheet loaded!"
            except (gspread.AuthenticationError, IOError):
                print "Authentication/IOError"
                exc_traceback = sys.exc_traceback
                raise shop_check_in_exceptions.CannotAccessGoogleSpreadsheetsError, None, exc_traceback
        else:
            print "Okay, testing connection"
            try:
                self._shop_user_database_google_worksheet.test_connection()
            except (IOError, Exception):
                self._shop_user_database_google_worksheet = None
                self._connect_to_google_spreadsheet()

    def _get_shop_user_from_google_spreadsheet(self, id_number):
        try:
            self._connect_to_google_spreadsheet()
            user_data = self._shop_user_database_google_worksheet.get_shop_user_data(id_number)
        except (shop_check_in_exceptions.CannotAccessGoogleSpreadsheetsError, gspread.exceptions.CellNotFound, IOError):
            exc_traceback = sys.exc_traceback
            raise shop_check_in_exceptions.NonexistentUserError, None, exc_traceback
        else:
            user = shop_user.ShopUser(user_data)
            self._shop_user_database[user.id_number] = user
            return user

    def _initialize_database(self):
        print "Trying to connect to spreadsheet"
        try:
            self._connect_to_google_spreadsheet()
            print "Successfully connected to spreadsheet"
            self._shop_user_database = self._shop_user_database_google_worksheet.load_shop_user_database()
        except (gspread.GSpreadException, shop_check_in_exceptions.CannotAccessGoogleSpreadsheetsError):
            self._shop_user_database = self._shop_user_database_local.load_shop_user_database()
        else:
            self._out_of_sync_users = self._shop_user_database_local.load_out_of_sync_users()
            self._synchronize_databases()

    def _synchronize_databases(self):
            try:
                self._connect_to_google_spreadsheet()
                for user in self._out_of_sync_users:
                    self._shop_user_database_google_worksheet.update_user(user)
            except (gspread.GSpreadException, IOError):
                pass
            else:
                self._out_of_sync_users = []


class ShopUserDatabaseTesting(ShopUserDatabase):

    def __init__(self):
        super(ShopUserDatabaseTesting, self).__init__(SPREADSHEET_TESTING,
                                                      PATH_TESTING_LOCAL_DATABASE,
                                                      PATH_TESTING_OUT_OF_SYNC_USERS)


class _ShopUserDatabaseGoogleWorksheet(object):

    def __init__(self, spreadsheet=SPREADSHEET, worksheet=WORKSHEET):
        #login_info = self._get_login_info()
        #username = login_info["GOOGLE_USERNAME"]
        #password = login_info["GOOGLE_PASSWORD"]


        print "Attempting to login via gspread"

        json_key = json.load(open('oauth2.json'))
        scope = ['https://spreadsheets.google.com/feeds']
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'], scope)
        google_account = gspread.authorize(credentials)

        print "good!"
        self._worksheet = google_account.open(spreadsheet).worksheet(worksheet)

    def load_shop_user_database(self):
        raw_data = self._worksheet.get_all_values()
        shop_users = [shop_user.ShopUser(shop_user_data) for shop_user_data in raw_data]
        for user in shop_users:
            if user.validation_required_changes():
                print 'Need to update:', user.name
		try:
                   self.update_user(user)
		except:
		   print 'Update for %s failed' % user.name
                print 'Updates done'
        shop_user_database = {user.id_number: user for user in shop_users}
        return shop_user_database

    def get_shop_user_data(self, id_number):
        cell_id_number = self._worksheet.find(id_number)
        return self._worksheet.row_values(cell_id_number.row)

    def test_connection(self):
        self._worksheet.cell(1, 1)

    def update_user(self, user):
        self._change_debt(user.id_number, user.debt)
        self._update_proctorliness(user)

    def _get_login_info(self):
        with open(PATH_LOGIN_INFO, "r") as login_info:
            return dict([line.split() for line in login_info])

    def _change_debt(self, id_number, new_debt):
        row = self._worksheet.find(id_number).row
        col = shop_user.DEBT + 1  # gspread is 1-indexed, shop_users are 0-indexed.
        self._worksheet.update_cell(row, col, new_debt)

    def _update_proctorliness(self, user):
        row = self._worksheet.find(user.id_number).row
        col = shop_user.PROCTOR + 1  # gspread is 1-indexed, shop_users are 0-indexed.
        proctorliness = shop_user.IS_PROCTOR if user._proctor else shop_user.IS_NOT_PROCTOR
        self._worksheet.update_cell(row, col, proctorliness)


class _ShopUserDatabaseLocal(object):

    def __init__(self, database_file_path, out_of_date_users_file_path):
        self._database_file_path = database_file_path
        self._out_of_date_users_file_path = out_of_date_users_file_path

    def load_shop_user_database(self):
        return self._load_file(self._database_file_path)

    def load_out_of_sync_users(self):
        return self._load_file(self._out_of_date_users_file_path)

    def dump_data(self, database, out_of_sync_users):
        self._dump_file(self._database_file_path, database)
        self._dump_file(self._out_of_date_users_file_path, out_of_sync_users)

    def _correct_current_working_directory(self):
        absolute_path = os.path.abspath(__file__)
        directory_name = os.path.dirname(absolute_path)
        os.chdir(directory_name)

    def _load_file(self, file_path):
        self._correct_current_working_directory()
        with open(file_path, 'rb') as file_:
            return cPickle.load(file_)

    def _dump_file(self, file_path, dumpee):
        self._correct_current_working_directory()
        self._erase_file(file_path)

        with open(file_path, 'wb') as file_:
            cPickle.dump(dumpee, file_)

    def _erase_file(self, file_path):
        self._correct_current_working_directory()
        with open(file_path, "wb") as file_:
            file_.truncate()
