import shop_user

class Shop():
    """ Encapsulates all data and operations on the shop.
    """
    def __init__(self,
                 open = False,
                 pod_list = [shop_user.ShopUser()]):
        self.open = open
        self.pod_list = pod_list


