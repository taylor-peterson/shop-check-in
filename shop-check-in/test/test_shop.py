from test import sample_users

import shop
import shop_check_in_exceptions


FIRST_SLOT = 0
LAST_SLOT = 29


class TestShop(object):

    def test_open_failure_not_proctor(self):
        machine_shop = shop.Shop()

        try:
            machine_shop.open_(sample_users.USER_CERTIFIED)
        except shop_check_in_exceptions.NonProctorError:
            assert not machine_shop._open
            assert not machine_shop.is_pod(sample_users.USER_CERTIFIED)
        else:
            assert False

    def test_open_success(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        assert machine_shop._open
        assert machine_shop.is_pod(sample_users.USER_POD)

    def test_open_failure_already_open(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        try:
            machine_shop.open_(sample_users.USER_POD)
        except shop_check_in_exceptions.ShopAlreadyOpenError:
            assert machine_shop._open
            assert machine_shop.is_pod(sample_users.USER_POD)
        else:
            assert False

    def test_close_failure_not_empty(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED], FIRST_SLOT)

        try:
            machine_shop.close_(sample_users.USER_POD)
        except shop_check_in_exceptions.ShopOccupiedError:
            assert machine_shop._open
            assert machine_shop.is_pod(sample_users.USER_POD)
            assert not machine_shop._empty()

    def test_close_failure_not_pod(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED], FIRST_SLOT)

        try:
            machine_shop.close_(sample_users.USER_PROCTOR)
        except shop_check_in_exceptions.UnauthorizedUserError:
            assert machine_shop._open
            assert machine_shop.is_pod(sample_users.USER_POD)
            assert not machine_shop._empty()
            
    def test_close_success(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.close_(sample_users.USER_POD)

        assert not machine_shop._open
        assert machine_shop._pods == []
        assert machine_shop._empty()

    def test_is_pod_failure(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        assert not machine_shop.is_pod(sample_users.USER_PROCTOR)

    def test_is_pod_success(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        assert machine_shop.is_pod(sample_users.USER_POD)

    def test_is_pod_success_additional_pod(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.change_pod(sample_users.USER_PROCTOR)

        assert machine_shop.is_pod(sample_users.USER_PROCTOR)

    def test_add_user_s_to_slot__success_single_user(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED], FIRST_SLOT)

        assert machine_shop._occupants[FIRST_SLOT] == [sample_users.USER_CERTIFIED]

    def test_add_user_s_to_slot_success_two_users(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED, sample_users.USER_PROCTOR], FIRST_SLOT)

        assert machine_shop._occupants[FIRST_SLOT] == [sample_users.USER_CERTIFIED, sample_users.USER_PROCTOR]

    def test_add_user_s_to_slot_failure_one_invalid(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        try:
            machine_shop.add_user_s_to_slot([sample_users.USER_INVALID], FIRST_SLOT)
        except shop_check_in_exceptions.InvalidUserError:
            assert machine_shop._empty
        else:
            assert False

    def test_add_user_s_to_slot_one_failure_valid_one_invalid(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        try:
            machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED, sample_users.USER_INVALID], FIRST_SLOT)
        except shop_check_in_exceptions.InvalidUserError:
            assert machine_shop._empty
        else:
            assert False

    def test_add_user_s_to_slot_failure_two_invalid(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        try:
            machine_shop.add_user_s_to_slot([sample_users.USER_INVALID, sample_users.USER_INVALID], FIRST_SLOT)
        except shop_check_in_exceptions.InvalidUserError:
            assert machine_shop._empty
        else:
            assert False

    def test_replace_or_transfer_user_replace(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED], FIRST_SLOT)
        machine_shop.replace_or_transfer_user(FIRST_SLOT, FIRST_SLOT)
        
        assert machine_shop._occupants[FIRST_SLOT] == [sample_users.USER_CERTIFIED]        

    def test_replace_or_transfer_user_transfer(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED], FIRST_SLOT)
        machine_shop.replace_or_transfer_user(LAST_SLOT, FIRST_SLOT)

        assert machine_shop._occupants[FIRST_SLOT] == []
        assert machine_shop._occupants[LAST_SLOT] == [sample_users.USER_CERTIFIED]

    def test_discharge_user_s_single_user(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED], FIRST_SLOT)

        discharged_user = machine_shop.discharge_user_s(FIRST_SLOT)

        assert machine_shop._empty()
        assert discharged_user == [sample_users.USER_CERTIFIED]

    def test_discharge_user_s_two_users(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED, sample_users.USER_PROCTOR], FIRST_SLOT)

        discharged_users = machine_shop.discharge_user_s(FIRST_SLOT)

        assert machine_shop._empty()
        assert discharged_users == [sample_users.USER_CERTIFIED, sample_users.USER_PROCTOR]

    def test_change_pod_success_non_pod_proctor(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.change_pod(sample_users.USER_PROCTOR)

        assert machine_shop.is_pod(sample_users.USER_PROCTOR)

    def test_change_pod_success_remove_pod(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.change_pod(sample_users.USER_PROCTOR)
        machine_shop.change_pod(sample_users.USER_POD)

        assert not machine_shop.is_pod(sample_users.USER_POD)
        assert machine_shop.is_pod(sample_users.USER_PROCTOR)

    def test_change_pod_failure_only_pod(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        try:
            machine_shop.change_pod(sample_users.USER_POD)
        except shop_check_in_exceptions.PodRequiredError:
            assert machine_shop.is_pod(sample_users.USER_POD)
        else:
            assert False

    def test_change_pod_failure_not_proctor(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)

        try:
            machine_shop.change_pod(sample_users.USER_CERTIFIED)
        except shop_check_in_exceptions.NonProctorError:
            assert not machine_shop.is_pod(sample_users.USER_CERTIFIED)
        else:
            assert False

    def test_empty_false(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.add_user_s_to_slot([sample_users.USER_CERTIFIED], FIRST_SLOT)

        assert not machine_shop._empty()

    def test_empty_true(self):
        machine_shop = shop.Shop()
        machine_shop.open_(sample_users.USER_POD)
        machine_shop.close_(sample_users.USER_POD)

        assert machine_shop._empty()
