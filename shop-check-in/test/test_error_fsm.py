import Queue as queue
from test import sample_users
from test import timeout

timeout = timeout.timeout

import signal
import shop
import event
import error_handler
import shop_check_in_exceptions

CARD_SWIPE_POD = event.Event(event.CARD_SWIPE, sample_users.USER_POD.id_number)
CARD_SWIPE_PROCTOR = event.Event(event.CARD_SWIPE, sample_users.USER_PROCTOR.id_number)
CARD_SWIPE_CERTIFIED = event.Event(event.CARD_SWIPE, sample_users.USER_CERTIFIED.id_number)
CARD_SWIPE_INVALID = event.Event(event.CARD_SWIPE, sample_users.USER_INVALID.id_number)

CARD_INSERT = event.Event(event.CARD_INSERT, 5)
CARD_REMOVE = event.Event(event.CARD_REMOVE, 5)

CARD_INSERT_OTHER = event.Event(event.CARD_INSERT, 10)
CARD_REMOVE_OTHER = event.Event(event.CARD_REMOVE, 10)

SWITCH_FLIP_ON = event.Event(event.SWITCH_FLIP_ON, "")
SWITCH_FLIP_OFF = event.Event(event.SWITCH_FLIP_OFF, "")

BUTTON_CANCEL = event.Event(event.BUTTON_CANCEL, "")
BUTTON_CONFIRM = event.Event(event.BUTTON_CONFIRM)
BUTTON_MONEY = event.Event(event.BUTTON_MONEY, "")
BUTTON_CHANGE_POD = event.Event(event.BUTTON_CHANGE_POD, "")
BUTTON_DISCHARGE_USER = event.Event(event.BUTTON_DISCHARGE_USER, "")

TERMINATE_PROGRAM = event.Event(event.TERMINATE_PROGRAM)

STATE_IN = "state-in"

class ErrorHarness:
    def __init__(self):
        self._event_q = queue.Queue()
        self._message_q = queue.Queue()
        self._shop = shop.Shop()
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
        assert exit_state == STATE_IN

    @timeout
    def handle_error(self, error, error_data = None):
        return self._handler.handle_error(STATE_IN, error, error_data)

    def has_messages(self):
        return not self._message_q.empty()


class TestErrorFSMTransition:

    def test_non_proctor_error_confirm(self):
        print
        harness = ErrorHarness()

        harness.test_events(shop_check_in_exceptions.NonProctorError,
                            None,
                            [BUTTON_CONFIRM])

        assert harness.has_messages()
        print

    def test_non_proctor_error_insert(self):
        print

        harness = ErrorHarness()

        harness.test_events(shop_check_in_exceptions.NonProctorError,
                            None,
                            [CARD_INSERT, CARD_REMOVE, BUTTON_CONFIRM])

        assert harness.has_messages()
        print

    def test_insert_insert_remove_remove(self):
        harness = ErrorHarness()

        harness.add_event(CARD_INSERT_OTHER)
        harness.add_event(CARD_REMOVE_OTHER)
        harness.add_event(CARD_REMOVE)

        end_state = harness.handle_error(CARD_INSERT.key, CARD_INSERT.data)

        print
        assert end_state == STATE_IN
        assert harness.has_messages()
        print

