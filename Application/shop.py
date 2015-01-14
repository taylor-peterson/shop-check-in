import shop_user

class Shop():
    """ Encapsulates all data and operations on the shop.
    """
    def __init__(self,
                 state = "closed",
                 pod_list = [shop_user.ShopUser()]):
        self.state = state
        self.pod_list = pod_list
        print self.pod_list
