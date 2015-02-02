import shop
import fsm
import shop_user
import shop_check_in_exceptions
import event
import Queue as queue

import winsound

DEFAULT_ERROR_MESSAGE = "\0Action not recognized."
ERROR_RESOLVED = "error_resolved"
ERROR_NOT_RESOLVED = "error_not_resolved"


class ErrorHandler(object):
    def __init__(self, event_q, message_q, shop_):
        self._event_q = event_q
        self._message_q = message_q
        self._shop = shop_
        self._errors = queue.LifoQueue()

        self._messages_to_display = {
            shop_check_in_exceptions.MoneyOwedError: "\0User owes money.",
            shop_check_in_exceptions.NonProctorError: "\0User is not a proctor.",
            shop_check_in_exceptions.ShopOccupiedError: "\0Shop is currently occupied.",
            shop_check_in_exceptions.OutOfDateTestError: "\0Out-of-date safety test.",
            shop_check_in_exceptions.ShopAlreadyOpenError: "\0Shop is already open.",
            shop_check_in_exceptions.PodRequiredError: "\0Only Proctor can't sign out",
            shop_user.DEFAULT_NAME: "\0User does not have permissions for that action.",
            event.CARD_SWIPE: "\0ERR - Ignoring swipe. Please confirm.",
            event.CARD_REMOVE: "\0ERR - Reinsert card(s) or confirm",
            event.CARD_INSERT: "\0ERR - Remove card(s)",
            }

        self._no_confirm_state_error_combos = [
            (fsm.CLOSED, shop_check_in_exceptions.NonProctorError)
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
                event.CARD_REMOVE: self._handle_card_uninsert
            }
        }

    def handle_error(self, current_state, error, error_data=None):
        # winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)

        while True:

            error_msg = self._messages_to_display.get(error, DEFAULT_ERROR_MESSAGE)
            self._message_q.put(error_msg)

            if (current_state, error) in self._no_confirm_state_error_combos:
                return current_state

            next_event = self._event_q.get()

            if next_event.key == event.TERMINATE_PROGRAM:
                # TODO: Find better way to term. from error, currently need 2 signals
                self._event_q.put(event.Event(event.TERMINATE_PROGRAM))
                return current_state

            action = self._get_action(error, next_event)

            result = action(next_event.data, error_data)

            if result == ERROR_RESOLVED:
                return current_state
        
        return current_state

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

    def _handle_card_removed_not_reinserted(self, unused_data = None, old_slot = None):
        assert old_slot is not None
        print "User %s, left the shop!" % (str(self._shop.get_user_s_name_and_email(old_slot)))
        # TODO: Send angry email
        self._shop.discharge_user_s(old_slot)

    def _handle_card_insert_default(self, new_slot, unused_error_data = None):
        self.handle_error(None, event.CARD_INSERT, new_slot)
        return ERROR_NOT_RESOLVED

    def _handle_card_remove_default(self, new_slot, unused_error_data = None):
        self.handle_error(None, event.CARD_INSERT, new_slot)
        return ERROR_NOT_RESOLVED

    def _handle_confirm_default(self, unused_data = None, unused_error_data = None):
        return ERROR_RESOLVED

    def _handle_unrecognized_event(self, unused_data = None, unused_error_data = None):
        return ERROR_NOT_RESOLVED

# Button Errors - Explain error, request acknowledge, return
# Physical Errors
#    Card removed - Explain (Reinsert OR Acknowledge w/ card swipe -> Email)
#    Card inserted - Explain (Remove)
