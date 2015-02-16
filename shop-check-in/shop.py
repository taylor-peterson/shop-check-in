from datetime import datetime

import shop_check_in_exceptions
import logger.usage as usage_logger


NO_TIME = None
SLOTS = xrange(30)
SLOT_TO_MACHINE_MAP = { 0 : 'Slot 0',
    1 : 'Slot 1',
    2 : 'Slot 2',
    3 : 'Slot 3',
    4 : 'Slot 4',
    5 : 'Slot 5',
    6 : 'Slot 6',
    7 : 'Slot 7',
    8 : 'Slot 8',
    9 : 'Slot 9',
    10 : 'Slot 10',
    11 : 'Slot 11',
    12 : 'Slot 12',
    13 : 'Slot 13',
    14 : 'Slot 14',
    15 : 'Slot 15',
    16 : 'Slot 16',
    17 : 'Slot 17',
    18 : 'Slot 18',
    19 : 'Slot 19',
    20 : 'Slot 20',
    21 : 'Slot 21',
    22 : 'Slot 22',
    23 : 'Slot 23',
    24 : 'Slot 24',
    25 : 'Slot 25',
    26 : 'Slot 26',
    27 : 'Slot 27',
    28 : 'Slot 28',
    29 : 'Slot 29'
}

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
        if all(user.is_shop_certified() for user in user_s):
            self._occupants[slot] = user_s
            self._start_times[slot] = datetime.now()

    def replace_or_transfer_user(self, slot, prev_slot):
        if slot != prev_slot:
            self.log_exit(slot)
            self._occupants[slot] = self._occupants[prev_slot]
            self._start_times[slot] = NO_TIME
            self._occupants[prev_slot] = []
            self._start_times[slot] = datetime.now()
        else:
            pass  # The user(s) remain in their current location.

    def discharge_user_s(self, slot):
        occupants = self._occupants[slot]
        self.log_exit(slot)
        self._occupants[slot] = []
        self._start_times[slot] = NO_TIME
        return occupants

    def get_user_s(self, slot):
        return self._occupants[slot]

    def get_user_s_name_and_email(self, slot):
        return [user.get_name_and_email() for user in self._occupants[slot]]

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
            usage_logger.log_user_exit(user, self._start_times[slot], SLOT_TO_MACHINE_MAP[slot])

