CARD_SWIPE = "card_swipe"
CARD_INSERT = "card_insert"
CARD_REMOVE = "card_remove"

SWITCH_FLIP_ON = "flip_switch_on"
SWITCH_FLIP_OFF = "flip_switch_off"

BUTTON_CANCEL = "cancel"
BUTTON_CONFIRM = "confirm"
BUTTON_MONEY = "money"
BUTTON_CHANGE_POD = "change_pod"
BUTTON_CLEAR_USER = "clear_user"

TERMINATE_PROGRAM = "halt"

class Event():
    def __init__(self,
                  key = "",
                  data = None):
        self.key = key
        self.data = data
