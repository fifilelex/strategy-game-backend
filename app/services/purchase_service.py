from app.domain.exceptions import (
    DatabaseError,
    ItemAlreadyBought,
    ItemDoesNotExist,
    ItemNotOwned,
    NotEnoughMoney,
    UserDoesNotExist,
)
from app.domain.models import GameStateUpdate
from app.persistence import game_repository as g_repo
from app.persistence import item_repository as i_repo

# does user exist?
# does item exist?
# user does not have this item?
# does user have enough money?


def buy_item(uid: int, id: int):
    # load data
    gamestate = g_repo.read_gamestate(uid)
    item = i_repo.read_item(id)
    ownership = i_repo.read_ownership(uid, id)

    # does user exist?
    if not gamestate:
        raise UserDoesNotExist

    # does item exist?
    if not item:
        raise ItemDoesNotExist

    # user does not have this item?
    if ownership:
        raise ItemAlreadyBought

    # does user have enough money?
    if item["cost"] > gamestate["money"]:
        raise NotEnoughMoney

    # do DB update - if fails, raise DB error
    if not i_repo.create_ownership(uid, id):
        raise DatabaseError
    new_money = gamestate["money"] - item["cost"]
    new_income = gamestate["income"] + item["income"]
    game = GameStateUpdate(money=new_money, income=new_income)
    data = game.model_dump(exclude_unset=True)
    g_repo.update_gamestate(uid, data)


def check_ownerships(uid: int):
    gamestate = g_repo.read_gamestate(uid)

    if not gamestate:
        raise UserDoesNotExist
    return i_repo.read_ownerships(uid)


def check_ownership(uid: int, id: int):
    gamestate = g_repo.read_gamestate(uid)

    if not gamestate:
        raise UserDoesNotExist

    ownership = i_repo.read_ownership(uid, id)

    if not ownership:
        raise ItemNotOwned

    return ownership


def delete_ownership(uid: int, id: int):
    ownership = check_ownership(uid, id)
    item = i_repo.read_item(id)
    gamestate = g_repo.read_gamestate(uid)
    if not item:
        raise ItemDoesNotExist
    if not gamestate:
        raise UserDoesNotExist
    if not ownership:
        raise ItemNotOwned
    if not i_repo.delete_ownership(uid, id):
        raise DatabaseError
    new_money = gamestate["money"] + int((item["cost"]) * 0.5)
    new_income = gamestate["income"] - item["income"]
    game = GameStateUpdate(money=new_money, income=new_income)
    data = game.model_dump(exclude_unset=True)
    if not g_repo.update_gamestate(uid, data):
        raise DatabaseError
