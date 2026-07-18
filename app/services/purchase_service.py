from app.domain.exceptions import (
    DatabaseError,
    ItemAlreadyBoughtError,
    ItemDoesNotExistError,
    ItemNotOwnedError,
    NotEnoughMoneyError,
    UserDoesNotExistError,
)
from app.domain.models import GameStateUpdate, Ownership
from app.persistence.game_repository import GameRepository
from app.persistence.item_repository import ItemRepository


class PurchaseService:
    def __init__(self, game_repo: GameRepository, item_repo: ItemRepository):
        self.game_repo = game_repo
        self.item_repo = item_repo

    def buy_item(self, user_id: int, item_id: int) -> int:
        # load data
        try:
            gamestate = self.game_repo.read_gamestate(user_id)
        except DatabaseError:
            raise DatabaseError
        try:
            item = self.item_repo.read_item(item_id)
        except DatabaseError:
            raise DatabaseError
        # does user exist?
        if not gamestate:
            raise UserDoesNotExistError

        # does item exist?
        if not item:
            raise ItemDoesNotExistError

        ownership = self.item_repo.read_ownership(user_id, item_id)
        # user does not have this item?
        if ownership:
            raise ItemAlreadyBoughtError

        # does user have enough money?
        if item["cost"] > gamestate["money"]:
            raise NotEnoughMoneyError

        # do DB update - if fails, raise DB error
        if not self.item_repo.create_ownership(user_id, item_id):
            raise DatabaseError

        # calculate new data
        new_money = gamestate["money"] - item["cost"]
        new_income = gamestate["income"] + item["income"]

        game = GameStateUpdate(money=new_money, income=new_income)
        data = game.model_dump(exclude_unset=True)

        rowcount = self.game_repo.update_gamestate(user_id, data)
        if rowcount is None:
            raise DatabaseError
        return rowcount

    def check_ownerships(self, user_id: int) -> list[Ownership]:
        # does user exist
        gamestate = self.game_repo.read_gamestate(user_id)

        if not gamestate:
            raise UserDoesNotExistError

        ownerships_repo = self.item_repo.read_ownerships(user_id)
        if ownerships_repo is None:
            return []
        output = []
        for ownership in ownerships_repo:
            output.append(Ownership(**ownership))
        return output

    def check_ownership(self, user_id: int, item_id: int) -> Ownership:
        gamestate = self.game_repo.read_gamestate(user_id)

        if not gamestate:
            raise UserDoesNotExistError

        ownership = self.item_repo.read_ownership(user_id, item_id)

        if not ownership:
            raise ItemNotOwnedError

        return Ownership(**ownership)

    def delete_ownership(self, user_id: int, item_id: int) -> int:
        # load data
        gamestate = self.game_repo.read_gamestate(user_id)
        item = self.item_repo.read_item(item_id)

        if not gamestate:
            raise UserDoesNotExistError

        if not item:
            raise ItemDoesNotExistError

        ownership = self.check_ownership(user_id, item_id)

        if not ownership:
            raise ItemNotOwnedError

        if not self.item_repo.delete_ownership(user_id, item_id):
            raise DatabaseError

        new_money = gamestate["money"] + int((item["cost"]) * 0.5)
        new_income = gamestate["income"] - item["income"]
        game = GameStateUpdate(money=new_money, income=new_income)
        data = game.model_dump(exclude_unset=True)
        rowcount = self.game_repo.update_gamestate(user_id, data)
        if rowcount is None:
            raise DatabaseError
        return rowcount
