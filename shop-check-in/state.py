import event

DEFAULT_ERROR_MESSAGE = "Action not recognized."


class State():
    def __init__(self,
                 actions_dict = {},
                 message = ""):
        self.actions_dict = actions_dict
        self.message = message

        self.unauthorized_messages = {
            "default" : DEFAULT_ERROR_MESSAGE,
            "invalid user" : "User does not have permissions for that action.",
            "invalid card swipe" : "ERR - Ignoring swipe. Please confirm."}

    def unauthorized(self, error_message = "default"):
        print self.unauthorized_messages.get(error_message, DEFAULT_ERROR_MESSAGE)
        
        userInput = raw_input("    press enter to return to standby.")
        return self

class ShopClosed(State):

    def __init__(self):
        shop_closed_actions = {
            event.CARD_SWIPE_EVENT_KEY : self.process_card_swipe}

        shop_closed_message = "Shop closed."
  
        State.__init__(self, shop_closed_actions, shop_closed_message)
                       
    def process_card_swipe(self, user):
        if user.proctor:
            return self.openShop(user)
        else:
            return self.unauthorized("invalid user")
