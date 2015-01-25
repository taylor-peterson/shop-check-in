import shop_user
import event

import winsound

DEFAULT_ERROR_MESSAGE = "Action not recognized."


class ErrorHandler(object):
    def __init__(self, event_q):
        self._event_q = event_q

        self._messages_to_display = {
            "default": DEFAULT_ERROR_MESSAGE,
            shop_user.NONEXISTENT_USER: "User does not have permissions for that action.",
            event.CARD_SWIPE: "ERR - Ignoring swipe. Please confirm.",
            event.CARD_REMOVE: "ERR - Reinsert card(s), or confirm students have left.",  # send tsk email
            "shop_occupied": "ERR - Shop occupied. Please confirm.",
            "pod_required": "ERR - There must be a proctor on duty."
            }

    def handle_error(self, current_state, error):
        # winsound.PlaySound('SystemExclamation', winsound.SND_ALIAS)

        print self._messages_to_display.get(error, DEFAULT_ERROR_MESSAGE)
        print "Confirm to return to current state."

        new_event = self._event_q.get()

        if new_event.key != event.BUTTON_CONFIRM:
            print "oh no! things are screwed up!"
        
        return current_state
