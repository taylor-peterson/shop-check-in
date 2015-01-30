

class ShopCheckInError(Exception):
    pass


# region Shop User Errors

class ShopUserError(ShopCheckInError):
    pass


class InvalidUserError(ShopUserError):
    pass


class MoneyOwedError(ShopUserError):
    pass


class OutOfDateTestError(ShopUserError):
    pass


class NonProctorError(ShopUserError):
    pass

# endregion
