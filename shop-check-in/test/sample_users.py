import datetime

from dateutil.relativedelta import relativedelta

import shop_user

VALID_TEST_DATE = datetime.date.today()
VALID_TEST_DATE_BARELY = datetime.date.today() + relativedelta(years=-1, days=+1)
INVALID_TEST_DATE_BARELY = datetime.date.today() + relativedelta(years=-1)

USER_POD = shop_user.ShopUser(1, "POD Joe", "email", VALID_TEST_DATE, 0, True)
USER_PROCTOR = shop_user.ShopUser(0, "Proctor Joe", "email", VALID_TEST_DATE, 0, True)
USER_CERTIFIED = shop_user.ShopUser(7777777, "Joe Schmoe", "email", VALID_TEST_DATE, 0, False)
USER_INVALID = shop_user.ShopUser(0000000, shop_user.NONEXISTENT_USER, "email", shop_user.INVALID_TEST_DATE, 0, False)

USER_JUST_IN_DATE = shop_user.ShopUser(0, "Joe Schmoe", "email", VALID_TEST_DATE_BARELY, 0, False)
USER_JUST_OUT_OF_DATE = shop_user.ShopUser(0, "Joe Schmoe", "email", INVALID_TEST_DATE_BARELY, 0, False)
USER_WAY_OUT_OF_DATE = shop_user.ShopUser(0, "Joe Schmoe", "email", shop_user.INVALID_TEST_DATE, 0, False)
USER_PROCTOR_OUT_OF_DATE = shop_user.ShopUser(0, "Joe Schmoe", "email", shop_user.INVALID_TEST_DATE, 0, True)
