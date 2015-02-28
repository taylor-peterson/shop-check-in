import event
import sample_users

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