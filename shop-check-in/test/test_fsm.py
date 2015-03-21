import Queue as queue
import shop_user_database
import fsm
from test_events import *


class TestFsmDataOperations(object):

    def test_opening_process_switch_flip(self):
        assert True is False
        # should be the proctor on duty
        # log should have correct information

    def test_unlocked_process_closing_shop_success(self):
        assert True is False
        # should be no pod
        # log should have correct info

    def test_unlocked_process_closing_shop_failure(self):
        assert True is False
        # should still be pod
        # should be at least one user in shop
        # log should have correct info

    def test_adding_user_s_process_slot_one_user(self):
        assert True is False
        # should have a user in the correct slot
        # log should have correct info

    def test_adding_user_s_process_slot_two_users(self):
        assert True is False
        # should have two users in the correct slot
        # log should have correct info

    def test_removing_user_process_slot_reinsert_user(self):
        assert True is False
        # shop state should not change
        # log should have correct info

    def test_removing_user_process_slot_transfer_user(self):
        assert True is False
        # should have user(s) transfered to new slot
        # log should have correct info

    def test_removing_using_process_discharge(self):
        assert True is False
        # should empty slot
        # log should have correct info

    def test_clearing_debt_process_card_swipe_single_user(self):
        assert True is False
        # user debt should increase by fixed amount
        # log should have correct info

    def test_clearing_debt_process_card_swipe_two_users(self):
        assert True is False
        # both user debts should increase by fixed amount
        # log should have correct info

    def test_clearing_debt_process_card_swipe(self):
        assert True is False
        # user debt should be zeroed
        # log should have correct info

    def test_changing_pod_process_add_pod(self):
        assert True is False
        # should be an additional pod
        # log should have correct info

    def test_changing_pod_process_remove_pod_success(self):
        assert True is False
        # should remove correct proctor
        # log should have correct info


class TestFsmStateTransitions:

    # TODO: make sure the sample users are in the test spreadsheet
    # TODO: add timeouts as the state machine won't terminate if it is broken

    def test_closed_invalid_events(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)

        event_q.put(CARD_INSERT)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(CARD_REMOVE)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_CANCEL)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_MONEY)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_DISCHARGE_USER)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.CLOSED
        print

    def test_cancel_opening(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.CLOSED
        print

    def test_open_shop(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_fail(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(CARD_SWIPE_PROCTOR)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_shop(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.UNLOCKED
        print

    def test_cancel_unlock(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_swipe_user(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.ADDING_USER
        print

    def test_unlock_swipe_proctor(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.UNLOCKED
        print

    def test_unlock_swipe_invalid(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_INVALID)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.UNLOCKED
        print

    def test_unlock_remove(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.REMOVING_USER
        print

    def test_unlock_money(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_MONEY)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.CLEARING_DEBT
        print

    def test_unlock_change_pod(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.CHANGING_POD
        print

    def test_unlock_close(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_OFF)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.CLOSED
        print

    def test_unlock_add_user_cancel(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_try_add_pod_to_machine(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)

        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.UNLOCKED
        print


    def test_unlock_add_user(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_INSERT)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_add_user_swipe(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_PROCTOR)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.ADDING_USERS
        print

    def test_unlock_add_user_try_re_add_same_user(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)

        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.ADDING_USER
        print

    def test_unlock_add_user_try_add_pod(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)

        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.ADDING_USER
        print

    def test_unlock_add_users_insert(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_INSERT)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_add_two_users_cancel(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_remove_cancel(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE)
        event_q.put(CARD_INSERT)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_remove_clear(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE)
        event_q.put(BUTTON_DISCHARGE_USER)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_remove_money(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE)
        event_q.put(BUTTON_MONEY)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_clearing_debt_cancel(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_MONEY)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_clearing_debt_valid_swipe(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_MONEY)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_clearing_debt_invalid_swipe(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_MONEY)
        event_q.put(CARD_SWIPE_INVALID)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.CLEARING_DEBT
        print

    def test_unlock_change_pod_cancel(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_change_pod_add_proctor(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(CARD_SWIPE_PROCTOR)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_change_pod_remove_pod_fail(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_change_pod_remove_pod(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(CARD_SWIPE_PROCTOR)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_unlock_change_pod_err(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)
        
        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(BUTTON_CHANGE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(BUTTON_CONFIRM)
        event_q.put(BUTTON_CANCEL)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_signin_signout(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)

        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_INSERT)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE)
        event_q.put(BUTTON_DISCHARGE_USER)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_signin_signout_partners(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)

        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_INSERT)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE)
        event_q.put(BUTTON_DISCHARGE_USER)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print

    def test_signin_signout_separate(self):
        event_q = queue.Queue()
        message_q = queue.Queue()
        shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        board = fsm.BoardFsm(event_q, message_q, shop_user_db)

        event_q.put(CARD_SWIPE_POD)
        event_q.put(SWITCH_FLIP_ON)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_INSERT)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_SWIPE_CERTIFIED)
        event_q.put(CARD_INSERT_OTHER)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE)
        event_q.put(BUTTON_DISCHARGE_USER)
        event_q.put(CARD_SWIPE_POD)
        event_q.put(CARD_REMOVE_OTHER)
        event_q.put(BUTTON_DISCHARGE_USER)
        event_q.put(TERMINATE_PROGRAM)

        print "\n"
        end_state = board.run_fsm()
        assert end_state == fsm.STANDBY
        print