import datetime
import sys

from dateutil.relativedelta import relativedelta
import dateutil.parser

import shop_check_in_exceptions

NAME = 0
TEST_DATE = 1
EMAIL = 3
ID = 4
DEBT = 5
PROCTOR = 6

DEFAULT_NAME = "nonexistent_user"
INVALID_TEST_DATE = "1970-03-22"
IGNORED_DATA = "ignored_data"
DEFAULT_EMAIL = "nope"
DEFAULT_ID_NUMBER = "0000000"
DEFAULT_DEBT = 0
DEFAULT_PROCTORLINESS = False

IS_PROCTOR = "Yes"
IS_NOT_PROCTOR = "No"


class ShopUser(object):
    """ Stores and processes a shop user's data.
        Note that all changes to shop users must go through the database.
    """
    def __init__(self,
                 user_data=(DEFAULT_NAME,
                            INVALID_TEST_DATE,
                            IGNORED_DATA,
                            DEFAULT_DEBT,
                            DEFAULT_ID_NUMBER,
                            DEFAULT_DEBT,
                            DEFAULT_PROCTORLINESS),):
        self.validated_user_data = self._validate_user_data(user_data)

        self.id_number = self.validated_user_data[ID]
        self.name = self.validated_user_data[NAME]
        self.email = self.validated_user_data[EMAIL]
        self._test_date = self.validated_user_data[TEST_DATE]
        self.debt = self.validated_user_data[DEBT]
        self._proctor = self.validated_user_data[PROCTOR]

    def is_shop_certified(self):
        if self.name is DEFAULT_NAME:
            raise shop_check_in_exceptions.InvalidUserError
        elif not self._has_valid_safety_test():
            raise shop_check_in_exceptions.OutOfDateTestError
        elif self.debt != 0:
            raise shop_check_in_exceptions.MoneyOwedError
        else:
            return True

    def is_proctor(self):
        if not self._proctor:
            raise shop_check_in_exceptions.NonProctorError
        return self.is_shop_certified()

    def _has_valid_safety_test(self):
        today = datetime.date.today()
        difference_in_years = relativedelta(today, self._test_date).years
        return difference_in_years == 0

    # TODO: error handling/further validation?
    def _validate_user_data(self, user_data):
        validated_user_data = []
        for datum in user_data:
            validated_user_data.append(datum)

        try:
            validated_user_data[TEST_DATE] = dateutil.parser.parse(user_data[TEST_DATE])
            validated_user_data[DEBT] = int(float(user_data[DEBT]))
            validated_user_data[PROCTOR] = user_data[PROCTOR] == IS_PROCTOR
            validated_user_data[ID] = user_data[ID].lstrip('0')[:8]
        except ValueError:
            exc_traceback = sys.exc_traceback
            raise shop_check_in_exceptions.InvalidUserError, None, exc_traceback  # TODO: where to catch this error?
        else:
            return validated_user_data

    def __eq__(self, other):
        if (self.__class__ == other.__class__ and
                self.id_number == other.id_number and
                self.name == other._name and
                self.email == other._email and
                self._test_date == other._test_date and
                self.debt == other.debt and
                self._proctor == other._proctor):
            return True
        else:
            return False


