import Queue as queue
import timeout
from test_events import *
import fsm
import shop
import error_handler
import shop_check_in_exceptions



STATE_IN = "state-in"


class ErrorHarness:
    def __init__(self, state = STATE_IN):
        self._event_q = queue.Queue()
        self._message_q = queue.Queue()
        self._shop = shop.Shop()
        self._start_state = state
        self._handler = error_handler.ErrorHandler(self._event_q, self._message_q, self._shop)

    def add_event(self, event):
        self._event_q.put(event)

    def test_events(self, error, error_data, events):
        """
        Triggers an error, and then submits events afterwards
        """
        for e in events:
            self.add_event(e)
        exit_state = self.handle_error(error, error_data)
        assert exit_state == self._start_state

    @timeout.timeout
    def handle_error(self, error, error_data = None):
        return self._handler.handle_error(self._start_state, error, error_data)

    def has_messages(self):
        return not self._message_q.empty()

    def no_more_events(self):
        return self._event_q.empty()


class TestErrorFSMTransition:

    def test_non_proctor_error_confirm(self):
        print
        harness = ErrorHarness()

        harness.test_events(shop_check_in_exceptions.NonProctorError,
                            None,
                            [BUTTON_CONFIRM])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_non_proctor_error_insert(self):
        print
        harness = ErrorHarness()

        harness.test_events(shop_check_in_exceptions.NonProctorError,
                            None,
                            [CARD_INSERT, CARD_REMOVE, BUTTON_CONFIRM])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_insert_insert_fix_fix(self):
        print
        harness = ErrorHarness()

        harness.test_events(CARD_INSERT.key,
                            CARD_INSERT.data,
                            [CARD_INSERT_OTHER, CARD_REMOVE_OTHER, CARD_REMOVE])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_insert_remove_other_fix_fix(self):
        print
        harness = ErrorHarness()

        harness.test_events(CARD_INSERT.key,
                            CARD_INSERT.data,
                            [CARD_REMOVE_OTHER, CARD_INSERT_OTHER, CARD_REMOVE])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_remove_insert_other_fix_fix(self):
        print
        harness = ErrorHarness()

        harness.test_events(CARD_REMOVE.key,
                            CARD_REMOVE.data,
                            [CARD_INSERT_OTHER, CARD_REMOVE_OTHER, CARD_INSERT])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_remove_remove_fix_fix(self):
        print
        harness = ErrorHarness()

        harness.test_events(CARD_REMOVE.key,
                            CARD_REMOVE.data,
                            [CARD_REMOVE_OTHER, CARD_INSERT_OTHER, CARD_INSERT])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_no_confirm_closed_nonproctor(self):
        print
        harness = ErrorHarness(fsm.CLOSED)

        harness.test_events(shop_check_in_exceptions.NonProctorError,
                            None,
                            [])

        assert harness.has_messages()
        assert harness.no_more_events()
        print

    def test_default_insert_remove_confirm(self):
        print
        harness = ErrorHarness()

        harness.test_events("default error",
                            None,
                            [CARD_INSERT, CARD_REMOVE, BUTTON_CONFIRM, CARD_SWIPE_PROCTOR])

        assert harness.has_messages()
        assert not harness.no_more_events()
        print

    def test_timeout_on_unresolved_error(self):
        print
        harness = ErrorHarness()

        harness.add_event(BUTTON_CANCEL)
        harness.add_event(BUTTON_CHANGE_POD)
        harness.add_event(BUTTON_DISCHARGE_USER)

        assert timeout.is_timeout(harness.handle_error("Default Error"))
        print
