

class ShopCheckInError(Exception):
    pass


# region Shop Errors

class ShopError(ShopCheckInError):
    pass


class PodRequiredError(ShopError):
    pass


class ShopAlreadyOpenError(ShopError):
    pass


class UnauthorizedUserError(ShopError):
    pass


class ShopOccupiedError(ShopError):
    pass

# endregion


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


# region Shop User Database Errors

class ShopUserDatabaseError(ShopCheckInError):
    pass


class NonexistentUserError(ShopUserDatabaseError):
    pass


class CannotAccessGoogleSpreadsheetsError(ShopUserDatabaseError):
    pass

# endregion

