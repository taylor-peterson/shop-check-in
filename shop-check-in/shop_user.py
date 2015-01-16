UNAUTHORIZED = "unauthorized_user"

class ShopUser:
    """ Stores and processes a shop user's data.
        Note that all changes to shop users must go through the database.
    """
    def __init__(self,
                 id_number = 0,
                 name = UNAUTHORIZED,
                 email = "null",
                 test_date = 0,
                 debt = 0,
                 proctor = False):
        self.id_number = id_number
        self.name = name
        self.email = email
        self.test_date = test_date
        self.debt = debt
        self.proctor = proctor

    def is_shop_certified(self):
        return self.name is not UNAUTHORIZED and self.has_valid_safety_test()

    def is_proctor(self):
        return self.is_shop_certified() and self.proctor

    def has_valid_safety_test(self):
        # passed in last year
        return True


class UnauthorizedUserError(Exception): pass
