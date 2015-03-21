import datetime

from dateutil.relativedelta import relativedelta

import shop_user

# We compare VALID_TEST_DATE against dateutil.parser-returned objects, which are truncated datetimes.
VALID_TEST_DATE = str(datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0))
VALID_TEST_DATE_BARELY = str(datetime.date.today() + relativedelta(years=-1, days=+1))
INVALID_TEST_DATE_BARELY = str(datetime.date.today() + relativedelta(years=-1))

USER_POD = shop_user.ShopUser(["POD Joe", VALID_TEST_DATE, "", "email", "1111111", 0, shop_user.IS_PROCTOR])
USER_PROCTOR = shop_user.ShopUser(["Proctor Joe", VALID_TEST_DATE, "", "email", "101010", 0, shop_user.IS_PROCTOR])
USER_CERTIFIED = shop_user.ShopUser(["Joe Schmoe", VALID_TEST_DATE, "", "email", "7777777", 0, shop_user.IS_NOT_PROCTOR])
USER_INVALID = shop_user.ShopUser()

USER_JUST_IN_DATE = shop_user.ShopUser(["Joe Schmoe", VALID_TEST_DATE_BARELY, "", "email", "0", 0, shop_user.IS_NOT_PROCTOR])
USER_JUST_OUT_OF_DATE = shop_user.ShopUser(["Joe Schmoe", INVALID_TEST_DATE_BARELY, "", "email", "0", 0, shop_user.IS_NOT_PROCTOR])
USER_WAY_OUT_OF_DATE = shop_user.ShopUser(["Joe Schmoe", shop_user.INVALID_TEST_DATE, "", "email", "0", 0, shop_user.IS_NOT_PROCTOR])
USER_PROCTOR_OUT_OF_DATE = shop_user.ShopUser(["Joe Schmoe", shop_user.INVALID_TEST_DATE, "", "email", "0", 0, shop_user.IS_PROCTOR])

USER_OWES_MONEY = shop_user.ShopUser(["Joe Schmoe", VALID_TEST_DATE, "", "email", "7777777", 1, shop_user.IS_NOT_PROCTOR])
