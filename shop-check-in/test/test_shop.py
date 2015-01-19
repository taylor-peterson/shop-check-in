import Queue as queue

import shop
import shop_user
import shop_user_database

USER_POD = shop_user.ShopUser("1", "POD Joe", "email", shop_user.VALID_TEST_DATE, 0, True)
USER_PROCTOR = shop_user.ShopUser("0", "Proctor Joe", "email", shop_user.VALID_TEST_DATE, 0, True)
USER_CERTIFIED = shop_user.ShopUser("0", "Joe Schmoe", "email", shop_user.VALID_TEST_DATE, 0, False)
USER_INVALID = shop_user.ShopUser("0000000000", shop_user.UNAUTHORIZED, "email", shop_user.INVALID_TEST_DATE)

FIRST_SLOT = 0
LAST_SLOT = 29

# TODO: split up tests so they only have one assert?


class TestShop:

    def test_open_failure_not_proctor(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)

        try:
            machine_shop.open_(USER_CERTIFIED)
        except shop_user.UnauthorizedUserError:
            assert not machine_shop._open
            assert not machine_shop.is_pod(USER_CERTIFIED)
        else:
            assert False

    def test_open_success(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)

        machine_shop.open_(USER_POD)

        assert machine_shop._open
        assert machine_shop.is_pod(USER_POD)

    def test_open_failure_already_open(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)

        machine_shop.open_(USER_POD)

        try:
            machine_shop.open_(USER_POD)
        except shop.ShopAlreadyOpenError:
            assert machine_shop._open
            assert machine_shop.is_pod(USER_POD)
        else:
            assert False

    def test_close_failure_not_empty(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)
        machine_shop.add_user_s_to_slot([USER_CERTIFIED], FIRST_SLOT)

        try:
            machine_shop.close_(USER_POD)
        except shop.ShopOccupiedError:
            assert machine_shop._open
            assert machine_shop.is_pod(USER_POD)
            assert not machine_shop._empty()

    def test_close_failure_not_pod(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)
        machine_shop.add_user_s_to_slot([USER_CERTIFIED], FIRST_SLOT)

        try:
            machine_shop.close_(USER_PROCTOR)
        except shop_user.UnauthorizedUserError:
            assert machine_shop._open
            assert machine_shop.is_pod(USER_POD)
            assert not machine_shop._empty()
            
    def test_close_success(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)
        machine_shop.close_(USER_POD)

        assert not machine_shop._open
        assert machine_shop._empty()

    def test_is_pod_failure(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        assert not machine_shop.is_pod(USER_PROCTOR)

    def test_is_pod_success(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)
        machine_shop.change_pod(USER_PROCTOR)

        assert machine_shop.is_pod(USER_POD)
        assert machine_shop.is_pod(USER_PROCTOR)
        assert not machine_shop.is_pod(USER_CERTIFIED)

    def test_add_user_s_to_slot_single_user(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.add_user_s_to_slot([USER_CERTIFIED], FIRST_SLOT)
        assert machine_shop._occupants[FIRST_SLOT] == [USER_CERTIFIED]

    def test_add_user_s_to_slot_two_users(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.add_user_s_to_slot([USER_CERTIFIED, USER_PROCTOR], FIRST_SLOT)

        assert machine_shop._occupants[FIRST_SLOT] == [USER_CERTIFIED, USER_PROCTOR]

    def test_add_user_s_to_slot_one_invalid(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        try:
            machine_shop.add_user_s_to_slot([USER_INVALID], FIRST_SLOT)
        except shop_user.UnauthorizedUserError:
            assert machine_shop._empty
        else:
            assert False

    def test_add_user_s_to_slot_one_valid_one_invalid(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        try:
            machine_shop.add_user_s_to_slot([USER_CERTIFIED, USER_INVALID], FIRST_SLOT)
        except shop_user.UnauthorizedUserError:
            assert machine_shop._empty
        else:
            assert False

    def test_add_user_s_to_slot_two_invalid(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        try:
            machine_shop.add_user_s_to_slot([USER_INVALID, USER_INVALID], FIRST_SLOT)
        except shop_user.UnauthorizedUserError:
            assert machine_shop._empty
        else:
            assert False

    def test_replace_or_transfer_user_replace(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)
        
        machine_shop.add_user_s_to_slot([USER_CERTIFIED], FIRST_SLOT)
        machine_shop.replace_or_transfer_user(FIRST_SLOT, FIRST_SLOT)
        
        assert machine_shop._occupants[FIRST_SLOT] == [USER_CERTIFIED]        

    def test_replace_or_transfer_user_transfer(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.add_user_s_to_slot([USER_CERTIFIED], FIRST_SLOT)
        machine_shop.replace_or_transfer_user(LAST_SLOT, FIRST_SLOT)

        assert machine_shop._occupants[FIRST_SLOT] == []
        assert machine_shop._occupants[LAST_SLOT] == [USER_CERTIFIED]

    def test_discharge_user_s_single_user(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.add_user_s_to_slot([USER_CERTIFIED], FIRST_SLOT)
        machine_shop.discharge_user_s(FIRST_SLOT)

        assert machine_shop._empty()

    def test_discharge_user_s_two_users(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.add_user_s_to_slot([USER_CERTIFIED, USER_PROCTOR], FIRST_SLOT)
        machine_shop.discharge_user_s(FIRST_SLOT)

        assert machine_shop._empty()

    def test_charge_user_s_single_user(self):
        assert True is False # Need better way to test this.

    def test_charge_user_s_two_users(self):
        assert True is False # Need better way to test this.

    def test_change_pod_non_pod_proctor(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.change_pod(USER_PROCTOR)
        assert machine_shop.is_pod(USER_PROCTOR)

    def test_change_pod_remove_pod(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.change_pod(USER_PROCTOR)
        machine_shop.change_pod(USER_POD)

        assert not machine_shop.is_pod(USER_POD)
        assert machine_shop.is_pod(USER_PROCTOR)

    def test_change_pod_failure_only_pod(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        try:
            machine_shop.change_pod(USER_POD)
        except shop.PodRequiredError:
            assert machine_shop.is_pod(USER_POD)
        else:
            assert False

    def test_change_pod_failure_not_proctor(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        try:
            machine_shop.change_pod(USER_CERTIFIED)
        except shop_user.UnauthorizedUserError:
            assert not machine_shop.is_pod(USER_CERTIFIED)
        else:
            assert False

    def test_empty_false(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)
        machine_shop.open_(USER_POD)

        machine_shop.add_user_s_to_slot([USER_CERTIFIED], FIRST_SLOT)

        assert not machine_shop._empty()

    def test_empty_true(self):
        db = shop_user_database.ShopUserDatabaseSpoof()
        machine_shop = shop.Shop(db)

        assert machine_shop._empty()

        machine_shop.open_(USER_POD)
        machine_shop.close_(USER_POD)

        assert machine_shop._empty()
