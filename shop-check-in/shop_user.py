import datetime

from dateutil.relativedelta import relativedelta
import dateutil.parser

UNAUTHORIZED = "unauthorized_user"
INVALID_TEST_DATE = dateutil.parser.parse("1970-03-22")
VALID_TEST_DATE = datetime.date.today()

# TODO: Make attributes private.


class ShopUser:
    """ Stores and processes a shop user's data.
        Note that all changes to shop users must go through the database.
    """
    def __init__(self,
                 id_number=0,
                 name=UNAUTHORIZED,
                 email="null",
                 test_date=INVALID_TEST_DATE,
                 debt=0,
                 proctor=False):
        self.id_number = id_number
        self.name = name
        self.email = email
        self.test_date = test_date
        self.debt = debt
        self.proctor = proctor

    def is_shop_certified(self):
        return self.name is not UNAUTHORIZED and self._has_valid_safety_test()

    def is_proctor(self):
        return self.is_shop_certified() and self.proctor

    def _has_valid_safety_test(self):
        today = datetime.date.today()
        difference_in_years = relativedelta(today, self.test_date).years
        return difference_in_years == 0

    def __eq__(self, other):
        if (self.__class__ == other.__class__ and
                self.id_number == other.id_number and
                self.name == other.name and
                self.email == other.email and
                self.test_date == other.test_date and
                self.debt == other.debt and
                self.proctor == other.proctor):
            return True
        else:
            return False


class UnauthorizedUserError(Exception):
    pass