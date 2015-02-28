import shop_check_in_exceptions
import shop_user

SLOTS = xrange(30)


class Shop(object):
    def __init__(self):
        self._open = False
        self._pods = []
        self._occupants = [[] for slot in SLOTS]

    def open_(self, user):
        if user.is_proctor() and not self._open:
            self._open = True
            self._pods.append(user)
        elif user.is_proctor():
            raise shop_check_in_exceptions.ShopAlreadyOpenError
        else:
            raise shop_check_in_exceptions.NonProctorError

    def close_(self, user):
        if self.is_pod(user) and self._empty():
            self._pods = []
            self._open = False
        elif not self.is_pod(user):
            raise shop_check_in_exceptions.UnauthorizedUserError
        else:
            raise shop_check_in_exceptions.ShopOccupiedError
    
    def is_pod(self, user):
        return user in self._pods

    def add_user_s_to_slot(self, user_s, slot):
        slot = int(slot)
        if all(user.is_shop_certified() for user in user_s):
            self._occupants[slot] = user_s

    def replace_or_transfer_user(self, slot, prev_slot):
        slot = int(slot)
        prev_slot = int(prev_slot)

        if slot != prev_slot:
            self._occupants[slot] = self._occupants[prev_slot]
            self._occupants[prev_slot] = []
        else:
            pass  # The user(s) remain in their current location.

    def discharge_user_s(self, slot):
        slot = int(slot)
        occupants = self._occupants[slot]
        self._occupants[slot] = []
        return occupants

    def get_user_s(self, slot):
        slot = int(slot)
        return self._occupants[slot]

    def get_user_s_name_and_email(self, slot):
        slot = int(slot)
        return [user.get_name_and_email() for user in self._occupants[slot]]

    def change_pod(self, user):
        if user.is_proctor() and not self.is_pod(user):
            self._pods.append(user)
        elif self.is_pod(user) and len(self._pods) > 1:
            self._pods.remove(user)
        elif self.is_pod(user):
            raise shop_check_in_exceptions.PodRequiredError

    def _empty(self):
        return all(self._occupants[slot] == [] for slot in SLOTS)