import Queue as queue
import timeout
from test_events import *
import fsm
import shop
import sample_users
import error_handler
import shop_user_database
import shop_check_in_exceptions

STATE_IN = "state-in"


class ErrorHandlerHarness:
    def __init__(self, state=STATE_IN):
        self._event_q = queue.Queue()
        self._message_q = queue.Queue()
        self._shop = shop.Shop()
        self._start_state = state
        self._handler = error_handler.ErrorHandler(self._event_q, self._message_q, self._shop)

    def set_initial_state(self, state):
        self._start_state = state

    def add_event(self, an_event):
        self._event_q.put(an_event)

    def test_events(self, error, error_data, events):
        """
        Triggers an error, and then submits events afterwards.
        Checks that input state = output state
        """
        for e in events:
            self.add_event(e)
        exit_state = self.handle_error(error, error_data)
        assert exit_state == self._start_state

    @timeout.make_timeout(2)
    def handle_error(self, error, error_data=None):
        return self._handler.handle_error(self._start_state, error, error_data)

    def has_messages(self):
        return not self._message_q.empty()

    def no_more_events(self):
        return self._event_q.empty()


class ErrorAndFSMHarness:
    def __init__(self):
        self._event_q = queue.Queue()
        self._message_q = queue.Queue()
        self._shop_user_db = shop_user_database.ShopUserDatabaseTesting()
        self._board = fsm.BoardFsm(self._event_q, self._message_q, self._shop_user_db)

    def test_events_expect_state(self, events, state):
        assert state == self.test_events(events)

    def test_events_expect_timeout(self, events):
        assert timeout.is_timeout(self.test_events(events))

    def test_events(self, events):
        for e in events:
            self._event_q.put(e)

        return self.run()

    def add_event(self, event_):
        self._event_q.put(event_)

    @timeout.make_timeout(10)
    def run(self):
        return self._board.run_fsm()

    def has_messages(self):
        return not self._message_q.empty()

    def no_more_events(self):
        return self._event_q.empty()


class TestErrorFSMIntegration:

    def test_nonproctor_open_then_open(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_CERTIFIED,
             CARD_SWIPE_INVALID,

             CARD_INSERT,
             CARD_REMOVE,
             CARD_SWIPE_PROCTOR,
             SWITCH_FLIP_ON,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )
        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_terminate_from_error_state(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_PROCTOR,
             SWITCH_FLIP_ON,
             CARD_SWIPE_PROCTOR,
             CARD_SWIPE_CERTIFIED,
             CARD_INSERT,
             CARD_REMOVE,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_in_and_out_errors(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_PROCTOR,
             SWITCH_FLIP_ON,
             CARD_SWIPE_PROCTOR,
             CARD_SWIPE_INVALID,
             CARD_SWIPE_CERTIFIED,
             CARD_SWIPE_PROCTOR,
             CARD_INSERT,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_email(self):

        print
        harness = ErrorHandlerHarness()
        harness._handler._mailer._send_id_card_email_s([sample_users.USER_CERTIFIED])
        print

    def test_non_proctor_error_confirm(self):
        print
        harness = ErrorAndFSMHarness()


        harness.test_events_expect_state(
            [CARD_SWIPE_CERTIFIED,
             TERMINATE_PROGRAM],
            fsm.CLOSED
        )

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_insert_insert_fix_fix(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_POD,
             SWITCH_FLIP_ON,
             CARD_INSERT,
             CARD_INSERT_OTHER,
             CARD_REMOVE_OTHER,
             CARD_REMOVE,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_insert_remove_other_fix_fix(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_POD,
             SWITCH_FLIP_ON,
             CARD_SWIPE_POD,
             CARD_SWIPE_CERTIFIED,
             CARD_INSERT_OTHER,
             CARD_INSERT,
             CARD_REMOVE_OTHER,
             CARD_INSERT_OTHER,
             CARD_REMOVE,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_remove_insert_other_fix_fix(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_POD,
             SWITCH_FLIP_ON,
             CARD_SWIPE_POD,
             CARD_SWIPE_CERTIFIED,
             CARD_INSERT_OTHER,
             CARD_REMOVE_OTHER,
             CARD_INSERT,
             CARD_REMOVE,
             CARD_INSERT_OTHER,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_remove_remove_fix_fix(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_POD,
             SWITCH_FLIP_ON,
             CARD_SWIPE_POD,
             CARD_SWIPE_CERTIFIED,
             CARD_INSERT_OTHER,
             CARD_SWIPE_POD,
             CARD_SWIPE_PROCTOR,
             CARD_INSERT,
             CARD_REMOVE_OTHER,
             CARD_REMOVE,
             CARD_INSERT,
             CARD_INSERT_OTHER,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )


        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_no_confirm_closed_nonproctor(self):
        print
        harness = ErrorHandlerHarness()
        harness.set_initial_state(fsm.CLOSED)

        harness.test_events(shop_check_in_exceptions.NonProctorError(),
                            None,
            [])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_default_insert_remove_confirm(self):
        print
        harness = ErrorAndFSMHarness()

        harness.test_events_expect_state(
            [CARD_SWIPE_POD,
             SWITCH_FLIP_ON,
             CARD_SWIPE_POD,
             CARD_SWIPE_CERTIFIED,
             CARD_INSERT_OTHER,
             CARD_REMOVE_OTHER,
             CARD_SWIPE_CERTIFIED,
             CARD_SWIPE_POD,
             TERMINATE_PROGRAM],
            fsm.STANDBY
        )


        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_timeout_on_unresolved_error(self):
        print
        harness = ErrorHandlerHarness()

        harness.add_event(BUTTON_CANCEL)
        harness.add_event(BUTTON_CHANGE_POD)
        harness.add_event(BUTTON_DISCHARGE_USER)

        assert timeout.is_timeout(harness.handle_error("Default Error"))
        print