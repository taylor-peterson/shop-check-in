from datetime import datetime
from slots import SLOTS, get_machine_name

import shop_check_in_exceptions
import logger.usage as usage_logger


NO_TIME = None

class Shop(object):
    def __init__(self):
        self._open = False
        self._pods = []
        self._occupants = [[] for slot in SLOTS]
        self._start_times = [NO_TIME for slot in SLOTS]

    def open_(self, user):
        if user.is_proctor() and not self._open:
            self._open = True
            self._pods.append(user)
            usage_logger.log_pod_opens_shop(user)
        elif user.is_proctor():
            raise shop_check_in_exceptions.ShopAlreadyOpenError
        else:
            raise shop_check_in_exceptions.NonProctorError

    def close_(self, user):
        if self.is_pod(user) and self._empty():
            self._pods = []
            self._open = False
            usage_logger.log_pod_closes_shop(user)
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
            self._start_times[slot] = datetime.now()

    def replace_or_transfer_user(self, slot, prev_slot):
        slot = int(slot)
        prev_slot = int(prev_slot)

        if slot != prev_slot:
            self.log_exit(slot)
            self._occupants[slot] = self._occupants[prev_slot]
            self._start_times[slot] = NO_TIME
            self._occupants[prev_slot] = []
            self._start_times[slot] = datetime.now()
        else:
            pass  # The user(s) remain in their current location.

    def discharge_user_s(self, slot):
        slot = int(slot)
        occupants = self._occupants[slot]
        self.log_exit(slot)
        self._occupants[slot] = []
        self._start_times[slot] = NO_TIME
        return occupants

    def get_user_s(self, slot):
        slot = int(slot)
        return self._occupants[slot]

    def get_user_s_name(self, slot):
        slot = int(slot)
        return [user.name for user in self._occupants[slot]]

    def change_pod(self, user):
        if user.is_proctor() and not self.is_pod(user):
            self._pods.append(user)
            usage_logger.log_pod_arrives_at_shop(user)
        elif self.is_pod(user) and len(self._pods) > 1:
            self._pods.remove(user)
            usage_logger.log_pod_exits_shop(user)
        elif self.is_pod(user):
            raise shop_check_in_exceptions.PodRequiredError

    def _empty(self):
        return all(self._occupants[slot] == [] for slot in SLOTS)

    def log_exit(self, slot):
        users = self._occupants[slot]
        for user in users:
            print "USER EXIT"
            usage_logger.log_user_exit(user, self._start_times[slot], get_machine_name(slot))

    def machine_name(self, slot):
        return get_machine_name(slot)

    def current_machine_user_s(self, slot):
        return self._occupants[slot]

    def current_machine_start_time(self, slot):
        return self._start_times[slot]

    def is_machine_in_use(self, slot):
        return self._occupants[slot] != []

    def is_open(self):
        return self._open

    def pods(self):
        return self._pods
