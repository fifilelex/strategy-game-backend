class UserDoesNotExistError(Exception):
    pass


class UserDoesExistError(Exception):
    pass


class ItemDoesNotExistError(Exception):
    pass


class ItemNotOwnedError(Exception):
    pass


class ItemDoesExistError(Exception):
    pass


class ItemAlreadyBoughtError(Exception):
    pass


class NotEnoughMoneyError(Exception):
    pass


class DatabaseError(Exception):
    pass


class FieldIsEmptyError(Exception):
    pass


class FieldIsInvalidError(Exception):
    pass
