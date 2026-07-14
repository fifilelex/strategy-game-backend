from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    UserDoesExistError,
    UserDoesNotExistError,
)
from app.domain.models import GameState, GameStateCreate, GameStateUpdate
from app.persistence import game_repository as g_repo


def read_gamestate(user_id: int) -> GameState:
    data = g_repo.read_gamestate(user_id)
    if not data:
        raise UserDoesNotExistError
    return GameState(**data)


def create_gamestate(game: GameStateCreate) -> int:
    if game.username and game.turn:
        if g_repo.search_gamestate_by_name(game.username, game.turn):
            raise UserDoesExistError
    else:
        raise FieldIsEmptyError
    try:
        new_id = g_repo.create_gamestate(
            username=game.username,
            turn=game.turn,
            money=game.money,
            income=game.income,
            is_active=game.is_active,
        )
    except DatabaseError:
        raise DatabaseError

    if new_id is None:
        raise DatabaseError
    return new_id


def update_gamestate(user_id: int, game: GameStateUpdate) -> int:
    gamestate = g_repo.read_gamestate(user_id)
    # if gamestate not found in DB
    if not gamestate:
        raise UserDoesNotExistError

    data = game.model_dump(exclude_unset=True, exclude_none=True)

    rowcount = g_repo.update_gamestate(user_id, data)
    if rowcount is None:
        raise DatabaseError
    return user_id


def delete_gamestate(user_id: int) -> int:
    gamestate = g_repo.read_gamestate(user_id)
    if not gamestate:
        raise UserDoesNotExistError
    rowcount = g_repo.delete_gamestate(user_id)
    if rowcount is None:
        raise DatabaseError
    return user_id
