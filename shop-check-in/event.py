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


EVENT_CODE_TO_NAME_MAP = {
    CARD_SWIPE : "Card Swipe",
    CARD_INSERT : "Card Insert",
    CARD_REMOVE : "Card Remove",
    SWITCH_FLIP_ON : "Switch Flipped On",
    SWITCH_FLIP_OFF : "Switch Flipped Off",
    BUTTON_CANCEL : "Cancel Button",
    BUTTON_CONFIRM : "Confirm Button",
    BUTTON_MONEY : "Money Button",
    BUTTON_CHANGE_POD : "Change POD Button",
    BUTTON_DISCHARGE_USER : "Discharge User Button",
    TERMINATE_PROGRAM : "Terminate Program Signal",
}


class Event():
    def __init__(self,
                 key="",
                 data=[]):
        self.key = key
        self.data = data

    def __repr__(self):
        return "Key is: %s; data is %s." % (self.key, self.data)