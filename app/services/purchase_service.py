from app.domain.exceptions import (
    DatabaseError,
    ItemAlreadyBoughtError,
    ItemDoesNotExistError,
    ItemNotOwnedError,
    NotEnoughMoneyError,
    UserDoesNotExistError,
)
from app.domain.models import GameStateUpdate, Ownership
from app.persistence import game_repository as g_repo
from app.persistence import item_repository as i_repo


def buy_item(user_id: int, item_id: int) -> int:
    # load data
    try:
        gamestate = g_repo.read_gamestate(user_id)
    except DatabaseError:
        raise DatabaseError
    try:
        item = i_repo.read_item(item_id)
    except DatabaseError:
        raise DatabaseError
    # does user exist?
    if not gamestate:
        raise UserDoesNotExistError

    # does item exist?
    if not item:
        raise ItemDoesNotExistError

    ownership = i_repo.read_ownership(user_id, item_id)
    # user does not have this item?
    if ownership:
        raise ItemAlreadyBoughtError

    # does user have enough money?
    if item["cost"] > gamestate["money"]:
        raise NotEnoughMoneyError

    # do DB update - if fails, raise DB error
    if not i_repo.create_ownership(user_id, item_id):
        raise DatabaseError

    # calculate new data
    new_money = gamestate["money"] - item["cost"]
    new_income = gamestate["income"] + item["income"]

    game = GameStateUpdate(money=new_money, income=new_income)
    data = game.model_dump(exclude_unset=True)

    rowcount = g_repo.update_gamestate(user_id, data)
    if rowcount is None:
        raise DatabaseError
    return rowcount


def check_ownerships(user_id: int) -> list[Ownership]:
    # does user exist
    gamestate = g_repo.read_gamestate(user_id)

    if not gamestate:
        raise UserDoesNotExistError

    ownerships_repo = i_repo.read_ownerships(user_id)
    if ownerships_repo is None:
        return []
    output = []
    for ownership in ownerships_repo:
        output.append(Ownership(**ownership))
    return output


def check_ownership(user_id: int, item_id: int) -> Ownership:
    gamestate = g_repo.read_gamestate(user_id)

    if not gamestate:
        raise UserDoesNotExistError

    ownership = i_repo.read_ownership(user_id, item_id)

    if not ownership:
        raise ItemNotOwnedError

    return Ownership(**ownership)


def delete_ownership(user_id: int, item_id: int) -> int:
    # load data
    gamestate = g_repo.read_gamestate(user_id)
    item = i_repo.read_item(item_id)

    if not gamestate:
        raise UserDoesNotExistError

    if not item:
        raise ItemDoesNotExistError

    ownership = check_ownership(user_id, item_id)

    if not ownership:
        raise ItemNotOwnedError

    if not i_repo.delete_ownership(user_id, item_id):
        raise DatabaseError

    new_money = gamestate["money"] + int((item["cost"]) * 0.5)
    new_income = gamestate["income"] - item["income"]
    game = GameStateUpdate(money=new_money, income=new_income)
    data = game.model_dump(exclude_unset=True)
    rowcount = g_repo.update_gamestate(user_id, data)
    if rowcount is None:
        raise DatabaseError
    return rowcount
