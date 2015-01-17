import shop
import shop_user
import shop_user_database

class TestShop:

    def test_open(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)

        assert machine_shop.open == False
        
        user = shop_user.ShopUser()
        machine_shop.open_(user)
        
        assert machine_shop.open
        assert machine_shop.is_pod(user)

    def test_close_failure(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        user = shop_user.ShopUser()
        machine_shop.open_(user)
        machine_shop.add_user_s_to_slot(user, 5)

        try:
            machine_shop.close_()
        except shop.ShopOccupiedError:
            assert machine_shop.open
            assert machine_shop.is_pod(user)
            assert not machine_shop._empty()
            
    def test_close_success(self):
        assert True == False

    def test_is_pod_failure(self):
        assert True == False

    def test_is_pod_success(self):
        assert True == False

    def test_add_user_s_to_slot_single_user(self):
        assert True == False

    def test_add_user_s_to_slot_two_users(self):
        assert True == False

    def test_replace_or_transfer_user_replace(self):
        assert True == False

    def test_replace_or_transfer_user_transfer(self):
        assert True == False

    def test_discharge_user_s_single_user(self):
        assert True == False

    def test_discharch_user_s_two_users(self):
        assert True == False

    def test_charge_user_s_single_user(self):
        assert True == False

    def test_charge_user_s_two_users(self):
        assert True == False

    def test_change_pod_non_pod_proctor(self):
        assert True == False

    def test_change_pod_remove_pod(self):
        assert True == False

    def test_change_pod_failure_only_pod(self):
        assert True == False

    def test_change_pod_failure_not_proctor(self):
        assert True == False

    def test_empty_false(self):
        assert True == False

    def test_empty_true(self):
        assert True == False
