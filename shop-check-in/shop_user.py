import datetime

from dateutil.relativedelta import relativedelta
import dateutil.parser

NONEXISTENT_USER = "nonexistent_user"
INVALID_TEST_DATE = dateutil.parser.parse("1970-03-22")


class ShopUser:
    """ Stores and processes a shop user's data.
        Note that all changes to shop users must go through the database.
    """
    def __init__(self,
                 id_number=0,
                 name=NONEXISTENT_USER,
                 email="null",
                 test_date=INVALID_TEST_DATE,
                 debt=0,
                 proctor=False):
        self.id_number = id_number
        self._name = name
        self._email = email
        self._test_date = test_date
        self._debt = debt
        self._proctor = proctor

    def is_shop_certified(self):
        return self._name is not NONEXISTENT_USER and self._has_valid_safety_test()

    def is_proctor(self):
        return self.is_shop_certified() and self._proctor

    def _has_valid_safety_test(self):
        today = datetime.date.today()
        difference_in_years = relativedelta(today, self._test_date).years
        return difference_in_years == 0

    def __eq__(self, other):
        if (self.__class__ == other.__class__ and
                self.id_number == other.id_number and
                self._name == other._name and
                self._email == other._email and
                self._test_date == other._test_date and
                self._debt == other._debt and
                self._proctor == other._proctor):
            return True
        else:
            return False