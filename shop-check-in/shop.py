import shop_user

SLOTS = xrange(30)


class Shop:
    """ Encapsulates all data and operations on the shop.
    """
    def __init__(self, shop_user_database):
        self._shop_user_database = shop_user_database,
        self._open = False
        self._pods = []
        self._occupants = [[] for slot in SLOTS]

    def open_(self, user):
        if user.is_proctor() and not self._open:
            self._open = True
            self._pods.append(user)
        elif not user.is_proctor():
            raise shop_user.UnauthorizedUserError
        elif self._open:
            raise ShopAlreadyOpenError

    def close_(self, user):
        if self.is_pod(user) and self._empty():
            self._pods = [[] for slot in SLOTS]
            self._open = False
        elif not self.is_pod(user):
            raise shop_user.UnauthorizedUserError
        elif not self._empty():
            raise ShopOccupiedError
    
    def is_pod(self, user):
        return user in self._pods

    def add_user_s_to_slot(self, user_s, slot):
        if all(user.is_shop_certified() for user in user_s):
            self._occupants[slot] = user_s
        elif any(not user.is_shop_certified() for user in user_s):
            raise shop_user.UnauthorizedUserError

    def replace_or_transfer_user(self, slot, prev_slot):
        if slot != prev_slot:
            self._occupants[slot] = self._occupants[prev_slot]
            self._occupants[prev_slot] = []
        else:
            pass  # The user(s) remain in their current location.

    def discharge_user_s(self, slot):
        self._occupants[slot] = []

    def charge_user_s(self, slot):
        users = self._occupants[slot]
        for user in users:
            self._shop_user_database.increase_debt(user)

    def change_pod(self, user):
        if user.is_proctor() and not self.is_pod(user):
            self._pods.append(user)
        elif self.is_pod(user) and len(self._pods) > 1:
            self._pods.remove(user)
        elif self.is_pod(user):
            raise PodRequiredError
        else:
            raise shop_user.UnauthorizedUserError

    def _empty(self):
        return self._occupants == [[] for slot in range(30)]


class ShopOccupiedError(Exception):
    pass


class PodRequiredError(Exception):
    pass


class ShopAlreadyOpenError(Exception):
    pass
