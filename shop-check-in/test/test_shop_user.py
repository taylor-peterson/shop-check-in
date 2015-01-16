import shop_user

class TestShopUser:

    def test_is_shop_certified_unauthorized(self):
        user = shop_user.ShopUser()
        assert user.is_shop_certified() == False

    def test_is_shop_certified_invalid_test(self):
        assert True == False

    def test_is_shop_certified_succeed(self):
        assert True == False

    def test_is_proctor_not_certified(self):
        assert True == False

    def test_is_proctor_not_proctor(self):
        assert True == False

    def test_is_proctor_succeed(self):
        assert True == False

    def test_has_valid_safety_test_out_of_date(self):
        assert True == False

    def test_has_valid_safety_test_succeed(self):
        assert True == False
