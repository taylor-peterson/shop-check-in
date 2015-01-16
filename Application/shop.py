import shop_user

class Shop():
    """ Encapsulates all data and operations on the shop.
    """
    def __init__(self,
                 open_for_business = False,
                 pod_list = [shop_user.ShopUser()]):
        self.open = open_for_business
        self.pod_list = pod_list
        self.occupants = [[] for num in range(30)]

    def empty():
        return self.occupants == [None]*30


