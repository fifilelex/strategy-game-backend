from psycopg2.errors import NotNullViolation

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmpty,
    UserDoesExist,
    UserDoesNotExist,
)
from app.domain.models import GameStateCreate, GameStateUpdate
from app.persistence import game_repository as g_repo


def read_gamestate(uid: int):
    gamestate = g_repo.read_gamestate(uid)
    if not gamestate:
        raise UserDoesNotExist
    return gamestate


def create_gamestate(game: GameStateCreate):
    if game.username and game.turn:
        if g_repo.search_gamestate_by_name(game.username, game.turn):
            raise UserDoesExist
    else:
        raise FieldIsEmpty
    try:
        new_id = g_repo.create_gamestate(
            username=game.username,
            turn=game.turn,
            money=game.money,
            income=game.income,
            is_active=game.is_active,
        )
    except NotNullViolation:
        raise DatabaseError

    if new_id is None:
        raise DatabaseError
    return new_id


def update_gamestate(uid: int, game: GameStateUpdate):
    gamestate = g_repo.read_gamestate(uid)
    # if gamestate not found in DB
    if not gamestate:
        raise UserDoesNotExist

    data = game.model_dump(exclude_unset=True)

    if g_repo.update_gamestate(uid, data) is None:
        raise DatabaseError


def delete_gamestate(uid: int):
    gamestate = g_repo.read_gamestate(uid)
    if not gamestate:
        raise UserDoesNotExist
    if g_repo.delete_gamestate(uid) is None:
        raise DatabaseError
