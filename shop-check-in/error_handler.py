import shop
import fsm
import shop_user
import shop_check_in_exceptions
import event
from mailer import Mailer
import winsound

DEFAULT_ERROR_MESSAGE = "\0Action not recognized."
ERROR_RESOLVED = "error_resolved"
ERROR_NOT_RESOLVED = "error_not_resolved"


class ErrorHandler(object):
    def __init__(self, event_q, message_q, shop_):
        self._event_q = event_q
        self._message_q = message_q
        self._shop = shop_
        self._mailer = Mailer()

        # TODO: Right now errors are sometimes passed in as events, sometimes errors. Homogenize.
        self._messages_to_display = {
            shop_check_in_exceptions.MoneyOwedError: "\0User owes money.",
            shop_check_in_exceptions.NonProctorError: "\0User is not a proctor.",
            shop_check_in_exceptions.ShopOccupiedError: "\0Shop is currently occupied.",
            shop_check_in_exceptions.OutOfDateTestError: "\0Out-of-date safety test.",
            shop_check_in_exceptions.ShopAlreadyOpenError: "\0Shop is already open.",
            shop_check_in_exceptions.PodRequiredError: "\0Only Proctor can't sign out",
            shop_user.DEFAULT_NAME: "\0User does not have permissions for that action.",
            event.CARD_SWIPE: "\0ERR - Ignoring swipe. Please confirm.",
            event.CARD_REMOVE: "\0ERR - Reinsert card(s) or confirm. Slot: ",
            event.CARD_INSERT: "\0ERR - Remove card(s)",
            }

        self._no_confirm_state_error_combos = [
            (fsm.CLOSED, shop_check_in_exceptions.ShopUserError),
            (fsm.CLOSED, shop_check_in_exceptions.NonexistentUserError),
            (fsm.STANDBY, shop_check_in_exceptions.UnauthorizedUserError)
        ]

        self._default_event_to_action_map = {
            event.CARD_INSERT: self._handle_card_insert_default,
            event.CARD_REMOVE: self._handle_card_remove_default,
            event.BUTTON_CONFIRM: self._handle_confirm_default
        }

        self._error_specific_event_to_action_map = {
            event.CARD_REMOVE: {
                event.CARD_INSERT: self._handle_card_reinsert,
                event.BUTTON_CONFIRM: self._handle_card_removed_not_reinserted
            },
            event.CARD_INSERT: {
                event.CARD_REMOVE: self._handle_card_uninsert,
                event.BUTTON_CONFIRM: self._handle_unrecognized_event
            }
        }

    def _requires_no_confirmation(self, state, error):
        for (no_confirm_state, no_confirm_error) in self._no_confirm_state_error_combos:
            if state == no_confirm_state and self._same_error(error, no_confirm_error):
                print "The error %s from state %s requires no confirmation" % (str(error), str(state))
                return True
        return False

    @staticmethod
    def _same_error(e, template_e):
        """
        Determines if e is an instance of error class template_e OR if e equals template_e
        """
        print "Same error:", str(e), str(template_e)
        try:
            return isinstance(e, template_e)
        except TypeError:
            return e == template_e

    def handle_error(self, return_state, error, error_data=None):
        # winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)

        self._store_error_frame(return_state, error, error_data)

        while True:

            self._report_error()

            if self._requires_no_confirmation(return_state, error):
                return return_state

            next_event = self._event_q.get()
            if next_event.key == event.TERMINATE_PROGRAM:
                # TODO: Find better way to termiinate prgm from error, currently need 2 signals
                self._event_q.put(event.Event(event.TERMINATE_PROGRAM))
                return return_state

            action = self._get_action(error, next_event)

            result = action(next_event.data, error_data)

            if result == ERROR_RESOLVED:
                return return_state

    def _store_error_frame(self, return_state, error, error_data):
        self._return_state = return_state
        self._error = error
        self._error_data = error_data

    def _report_error(self):
        error_msg = self._messages_to_display.get(self._error, DEFAULT_ERROR_MESSAGE)
        error_msg += str(self._error_data) if self._error_data else ""
        self._message_q.put(error_msg)

    def _get_action(self, error, next_event):
        try:
            action = self._error_specific_event_to_action_map[error][next_event.key]
        except KeyError:
            try:
                action = self._default_event_to_action_map[next_event.key]
            except KeyError:
                action = self._handle_unrecognized_event

        return action

    def _handle_card_reinsert(self, new_slot, old_slot):
        if new_slot == old_slot:
            return ERROR_RESOLVED
        else:
            self.handle_error(None, event.CARD_INSERT, new_slot)
            return ERROR_NOT_RESOLVED

    def _handle_card_uninsert(self, new_slot, old_slot):
        if new_slot == old_slot:
            return ERROR_RESOLVED
        else:
            self.handle_error(None, event.CARD_REMOVE, new_slot)
            return ERROR_NOT_RESOLVED

    def _handle_card_removed_not_reinserted(self, unused_data=None, old_slot=None):
        assert old_slot is not None
        self._message_q.put("User %s, left the shop!" %
                            (str(self._shop.get_user_s_name_and_email(old_slot))))
        users = self._shop.get_user_s(old_slot)
        self._mailer._send_id_card_email_s(users)
        self._shop.discharge_user_s(old_slot)

    def _handle_card_insert_default(self, new_slot, unused_error_data=None):
        self.handle_error(None, event.CARD_INSERT, new_slot)
        return ERROR_NOT_RESOLVED

    def _handle_card_remove_default(self, new_slot, unused_error_data=None):
        self.handle_error(None, event.CARD_REMOVE, new_slot)
        return ERROR_NOT_RESOLVED

    def _handle_confirm_default(self, unused_data=None, unused_error_data=None):
        return ERROR_RESOLVED

    def _handle_unrecognized_event(self, unused_data=None, unused_error_data=None):
        return ERROR_NOT_RESOLVED
