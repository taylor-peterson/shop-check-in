import datetime

from dateutil.relativedelta import relativedelta
import dateutil.parser

NAME = 0
TEST_DATE = 1
EMAIL = 3
ID = 4
DEBT = 5
PROCTOR = 6

NONEXISTENT_USER = "nonexistent_user"
INVALID_TEST_DATE = dateutil.parser.parse("1970-03-22")


class ShopUser:
    """ Stores and processes a shop user's data.
        Note that all changes to shop users must go through the database.
    """
    def __init__(self, user_data=(NONEXISTENT_USER, INVALID_TEST_DATE, "ignored_data", "null", "0000000", 0, False)):
        self.validated_user_data = self._validate_user_data(user_data)

        self.id_number = self.validated_user_data[ID]
        self._name = self.validated_user_data[NAME]
        self._email = self.validated_user_data[EMAIL]
        self._test_date = self.validated_user_data[TEST_DATE]
        self.debt = self.validated_user_data[DEBT]
        self._proctor = self.validated_user_data[PROCTOR]

    def is_shop_certified(self):
        return self._name is not NONEXISTENT_USER and self._has_valid_safety_test()  # TODO: break out money owed vs. no safety test

    def is_proctor(self):
        return self.is_shop_certified() and self._proctor

    def _has_valid_safety_test(self):
        today = datetime.date.today()
        difference_in_years = relativedelta(today, self._test_date).years
        return difference_in_years == 0

    def _validate_user_data(self, user_data):

        # TODO: strip whitespace
        try:
            test_date = dateutil.parser.parse(cell_value_test_date)
            debt = int(float(cell_value_debt))
            proctor = (proctorliness == PROCTOR)
        except ValueError:
            # TODO: raise invalid user error
            # TODO: where to catch said error?
            pass
        else:
            pass

        return []

    def __eq__(self, other):
        if (self.__class__ == other.__class__ and
                self.id_number == other.id_number and
                self._name == other._name and
                self._email == other._email and
                self._test_date == other._test_date and
                self.debt == other.debt and
                self._proctor == other._proctor):
            return True
        else:
            return False


class InvalidUserError(Exception):
    pass