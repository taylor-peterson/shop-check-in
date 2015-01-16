import shop_user

# Add check for valid slot and other inputs
class Shop:
    """ Encapsulates all data and operations on the shop.
    """
    def __init__(self,
                 shop_user_database,
                 open_for_business = False,
                 pod_list = [shop_user.ShopUser()]):
        self.shop_user_databse = shop_user_database,
        self.open = open_for_business
        self.pod_list = pod_list
        self.occupants = [[] for num in range(30)]

    def open_(self, pod):
        self.open = True
        self.shop.pod_list.append(pod)

    def close_(self):
        if self._empty():
            self.pod_list.clear()
        else:
            # throw shop_not_empty error
    
    def is_pod(self, pod):
        return pod in self.pod_list

    def add_user_s_to_slot(self, user_s, slot):
        self.occupants[slot].append(user_s)

    def replace_or_transfer_user(slot, prev_slot):
        if slot != prev_slot:
            self.occupants[slot] = self.shop.occupants[prev_slot]
            self.occupants[prev_slot] = []

    def discharge_user_s(slot):
        self.shop.occupants[slot] = []

    def charge_user_s(slot):
        users = self.occupants[slot]
        for user in users:
            self.shop_user_database.increase_debt(user)

    def change_pod(user):
        if user.is_proctor and not self.is_pod(user):
            self.pod_list.append(user)
        elif self.is_pod(user) and len(self.pod_list) > 1:
            self.pod_list.remove(user)
        elif self.is_pod(user):
            # throw need at least one proctor error
        else:
            # throw invalid user error

    def _empty(self):
        return self.occupants == [None]*30
