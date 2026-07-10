class UserDoesNotExist(Exception):
    pass


class UserDoesExist(Exception):
    pass


class ItemDoesNotExist(Exception):
    pass


class ItemNotOwned(Exception):
    pass


class ItemDoesExist(Exception):
    pass


class ItemAlreadyBought(Exception):
    pass


class NotEnoughMoney(Exception):
    pass


class DatabaseError(Exception):
    pass


class FieldIsEmpty(Exception):
    pass


class FieldIsInvalid(Exception):
    pass
