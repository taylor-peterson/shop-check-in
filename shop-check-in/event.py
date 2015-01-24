CARD_SWIPE = "card_swipe"
CARD_INSERT = "M1"
CARD_REMOVE = "M0"

SWITCH_FLIP_ON = "S1"
SWITCH_FLIP_OFF = "S0"

BUTTON_CANCEL = "B0"
BUTTON_CONFIRM = "B1"
BUTTON_MONEY = "B2"
BUTTON_CHANGE_POD = "B3"
BUTTON_DISCHARGE_USER = "B4"

TERMINATE_PROGRAM = "halt"


class Event():
    def __init__(self,
                 key="",
                 data=[]):
        self.key = key
        self.data = data
