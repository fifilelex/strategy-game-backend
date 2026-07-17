from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    UserDoesExistError,
    UserDoesNotExistError,
)
from app.domain.models import GameState, GameStateCreate, GameStateUpdate
from app.persistence.game_repository import GameRepository


class GameService:
    def __init__(self, game_repo: GameRepository):
        self.game_repo = game_repo

    def read_gamestate(self, user_id: int) -> GameState:
        data = self.game_repo.read_gamestate(user_id)
        if not data:
            raise UserDoesNotExistError
        return GameState(**data)

    def create_gamestate(self, game: GameStateCreate) -> int:
        if game.username and game.turn:
            if self.game_repo.search_gamestate_by_name(game.username, game.turn):
                raise UserDoesExistError
        else:
            raise FieldIsEmptyError
        try:
            new_id = self.game_repo.create_gamestate(
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

    def update_gamestate(self, user_id: int, game: GameStateUpdate) -> int:
        gamestate = self.game_repo.read_gamestate(user_id)
        # if gamestate not found in DB
        if not gamestate:
            raise UserDoesNotExistError

        data = game.model_dump(exclude_unset=True, exclude_none=True)

        rowcount = self.game_repo.update_gamestate(user_id, data)
        if rowcount is None:
            raise DatabaseError
        return user_id

    def delete_gamestate(self, user_id: int) -> int:
        gamestate = self.game_repo.read_gamestate(user_id)
        if not gamestate:
            raise UserDoesNotExistError
        rowcount = self.game_repo.delete_gamestate(user_id)
        if rowcount is None:
            raise DatabaseError
        return user_id
