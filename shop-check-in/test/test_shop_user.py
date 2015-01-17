import datetime

import dateutil.parser
from dateutil.relativedelta import relativedelta

import shop_user

class TestShopUser:

    def test_is_shop_certified_unauthorized(self):
        user = shop_user.ShopUser()
        assert user.is_shop_certified() == False

    def test_is_shop_certified_invalid_test(self):
        user = shop_user.ShopUser()
        user.name = "Bob"
        assert user.is_shop_certified() == False

    def test_is_shop_certified_succeed(self):
        user = shop_user.ShopUser()
        user.name = "Bob"
        user.test_date = datetime.date.today()
        assert user.is_shop_certified() == True

    def test_is_proctor_not_certified(self):
        user = shop_user.ShopUser()
        assert user.is_proctor() == False

    def test_is_proctor_not_proctor(self):
        user = shop_user.ShopUser()
        user.name = "Bob"
        user.test_date = datetime.date.today()
        assert user.is_proctor() == False

    def test_is_proctor_succeed(self):
        user = shop_user.ShopUser()
        user.name = "Bob"
        user.test_date = datetime.date.today()
        user.proctor = True
        assert user.is_proctor() == True

    def test_has_valid_safety_test_out_of_date(self):
        user = shop_user.ShopUser()
        assert user.has_valid_safety_test() == False

        user.test_date = datetime.date.today() + relativedelta(years=-1)
        assert user.has_valid_safety_test() == False

    def test_has_valid_safety_test_succeed(self):
        user = shop_user.ShopUser()
        user.test_date = datetime.date.today()
        assert user.has_valid_safety_test() == True

        user.test_date = datetime.date.today() + relativedelta(years=-1, days=+1)
        assert user.has_valid_safety_test() == True
