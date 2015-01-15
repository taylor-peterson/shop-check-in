CARD_SWIPE_KEY = "card_swipe"
CARD_SWIPE_EVENT_ERROR_MSG = "invalid card swipe"

class Event():
    def __init__(self,
                  key = "",
                  data = None,
                  error_msg = ""):
        self.key = key
        self.data = data
        self.error_msg = error_msg

class CardSwipeEvent(Event):
    def __init__(self,
                 data = None):
        Event.__init__(self,
                       CARD_SWIPE_KEY,
                       data,
                       CARD_SWIPE_EVENT_ERROR_MSG)
