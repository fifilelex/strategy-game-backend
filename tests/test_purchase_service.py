from unittest.mock import patch

import pytest

from app.domain.exceptions import (
    DatabaseError,
    ItemAlreadyBoughtError,
    ItemDoesNotExistError,
    ItemNotOwnedError,
    NotEnoughMoneyError,
    UserDoesNotExistError,
)


class TestPurchaseService:

    @pytest.fixture
    def user_id(self, game_repository):
        user_id = game_repository.create_gamestate(
            username="fifilelex",
            turn=3,
            money=99999,
            income=999999,
            is_active=True,
        )
        return user_id

    @pytest.fixture
    def item_id(self, item_repository):
        item_id = item_repository.create_item(
            name="Factory",
            income=400,
            cost=10000,
            description="Produces various goods",
        )
        return item_id

    @pytest.fixture
    def ownership(self, item_repository, user_id, item_id):

        if user_id and item_id:
            item_repository.create_ownership(user_id, item_id)

    def test_buy_item_succcess(self, purchase_service, user_id, item_id):
        purchase_service.buy_item(user_id, item_id)

        ownership = purchase_service.check_ownership(user_id, item_id)
        assert ownership.user_id == user_id
        assert ownership.item_id == item_id

    def test_buy_item_read_gamestate_database_error(
        self, purchase_service, user_id, item_id
    ):
        with patch.object(purchase_service.game_repo, "read_gamestate") as mock_read:
            mock_read.side_effect = DatabaseError

            with pytest.raises(DatabaseError):
                purchase_service.buy_item(user_id, item_id)

    def test_buy_item_read_item_database_error(
        self, purchase_service, user_id, item_id
    ):
        with patch.object(
            purchase_service.game_repo, "read_gamestate"
        ) as mock_game, patch.object(
            purchase_service.item_repo, "read_item"
        ) as mock_item:

            mock_game.return_value = {
                "money": 100,
                "income": 10,
            }
            mock_item.side_effect = DatabaseError

            with pytest.raises(DatabaseError):
                purchase_service.buy_item(user_id, item_id)

    def test_buy_item_create_ownership_database_error(
        self, purchase_service, user_id, item_id
    ):
        with patch.object(
            purchase_service.game_repo, "read_gamestate"
        ) as mock_game, patch.object(
            purchase_service.item_repo, "read_item"
        ) as mock_item, patch.object(
            purchase_service.item_repo, "read_ownership"
        ) as mock_ownership, patch.object(
            purchase_service.item_repo, "create_ownership"
        ) as mock_create:

            mock_game.return_value = {
                "money": 100,
                "income": 10,
            }
            mock_item.return_value = {
                "cost": 50,
                "income": 5,
            }
            mock_ownership.return_value = None
            mock_create.return_value = False

            with pytest.raises(DatabaseError):
                purchase_service.buy_item(user_id, item_id)

    def test_buy_item_update_gamestate_database_error(
        self, purchase_service, user_id, item_id
    ):
        with patch.object(
            purchase_service.game_repo, "read_gamestate"
        ) as mock_game, patch.object(
            purchase_service.item_repo, "read_item"
        ) as mock_item, patch.object(
            purchase_service.item_repo, "read_ownership"
        ) as mock_ownership, patch.object(
            purchase_service.item_repo, "create_ownership"
        ) as mock_create, patch.object(
            purchase_service.game_repo, "update_gamestate"
        ) as mock_update:

            mock_game.return_value = {
                "money": 100,
                "income": 10,
            }
            mock_item.return_value = {
                "cost": 50,
                "income": 5,
            }
            mock_ownership.return_value = None
            mock_create.return_value = True
            mock_update.return_value = None

            with pytest.raises(DatabaseError):
                purchase_service.buy_item(user_id, item_id)

    def test_check_ownerships_none(self, purchase_service, user_id):
        with patch.object(purchase_service.item_repo, "read_ownerships") as mock_read:
            mock_read.return_value = None
            assert purchase_service.check_ownerships(user_id) == []

    def test_delete_ownership_item_not_owned(self, purchase_service, user_id, item_id):
        with patch.object(purchase_service.game_repo, "read_gamestate") as mock_read:
            mock_read.return_value = {"a": 1}

        with patch.object(purchase_service.item_repo, "read_item") as mock_read:
            mock_read.return_value = {"a": 1}
        with patch.object(purchase_service, "check_ownership") as mock_check:
            mock_check.return_value = None
            with pytest.raises(ItemNotOwnedError):
                purchase_service.delete_ownership(user_id, item_id)

    def test_delete_ownership_db_error(self, purchase_service, user_id, item_id):
        with patch.object(
            purchase_service.game_repo, "read_gamestate"
        ) as mock_gamestate, patch.object(
            purchase_service.item_repo, "read_item"
        ) as mock_item, patch.object(
            purchase_service, "check_ownership"
        ) as mock_check, patch.object(
            purchase_service.item_repo, "delete_ownership"
        ) as mock_delete:

            mock_gamestate.return_value = {
                "money": 100,
                "income": 10,
            }

            mock_item.return_value = {
                "cost": 50,
                "income": 5,
            }

            mock_check.return_value = True
            mock_delete.return_value = False

            with pytest.raises(DatabaseError):
                purchase_service.delete_ownership(user_id, item_id)

    def test_delete_ownership_no_change_error(self, purchase_service, user_id, item_id):
        with patch.object(
            purchase_service.game_repo, "read_gamestate"
        ) as mock_gamestate, patch.object(
            purchase_service.item_repo, "read_item"
        ) as mock_item, patch.object(
            purchase_service, "check_ownership"
        ) as mock_check, patch.object(
            purchase_service.item_repo, "delete_ownership"
        ) as mock_delete, patch.object(
            purchase_service.game_repo, "update_gamestate"
        ) as mock_update:

            mock_gamestate.return_value = {
                "money": 100,
                "income": 10,
            }

            mock_item.return_value = {
                "cost": 50,
                "income": 5,
            }

            mock_check.return_value = True
            mock_delete.return_value = True
            mock_update.return_value = None

            with pytest.raises(DatabaseError):
                purchase_service.delete_ownership(user_id, item_id)

    def test_buy_item_no_gamestate(self, purchase_service, item_id):
        with pytest.raises(UserDoesNotExistError):
            purchase_service.buy_item(user_id=9999999, item_id=item_id)

    def test_buy_no_item(self, purchase_service, user_id):
        with pytest.raises(ItemDoesNotExistError):
            purchase_service.buy_item(user_id=user_id, item_id=99999999)

    def test_buy_already_owned(self, purchase_service, user_id, item_id, ownership):
        with pytest.raises(ItemAlreadyBoughtError):
            purchase_service.buy_item(user_id, item_id)

    def test_buy_not_enough_money(self, purchase_service, game_repository, item_id):
        user_id = game_repository.create_gamestate(
            username="fifilelex", turn=4, money=0, income=100, is_active=True
        )
        if user_id and item_id:
            with pytest.raises(NotEnoughMoneyError):
                purchase_service.buy_item(user_id, item_id)

    def test_check_ownerships_success(
        self, purchase_service, user_id, item_id, ownership
    ):
        ownership = purchase_service.check_ownerships(user_id)
        for relation in ownership:
            assert relation.user_id == user_id
            assert relation.item_id == item_id

    def test_check_ownerships_empty(self, purchase_service, user_id):
        ownerships = purchase_service.check_ownerships(user_id)
        assert ownerships == []

    def test_check_ownerships_no_user(
        self, purchase_service, user_id, item_id, ownership
    ):
        with pytest.raises(UserDoesNotExistError):
            purchase_service.check_ownerships(4444444444444444)

    def test_check_ownership_success(
        self, purchase_service, user_id, item_id, ownership
    ):
        ownership = purchase_service.check_ownership(user_id, item_id)
        assert ownership.user_id == user_id
        assert ownership.item_id == item_id

    def test_check_ownership_no_user(
        self, purchase_service, user_id, item_id, ownership
    ):
        with pytest.raises(UserDoesNotExistError):
            purchase_service.check_ownership(4444444444444444, item_id)

    def test_check_ownership_not_owned(self, purchase_service, user_id, item_id):
        with pytest.raises(ItemNotOwnedError):
            purchase_service.check_ownership(user_id, item_id)

    def test_delete_ownership_success(
        self, purchase_service, user_id, item_id, ownership
    ):
        ownership = purchase_service.check_ownership(user_id, item_id)
        assert ownership.user_id == user_id
        assert ownership.item_id == item_id
        purchase_service.delete_ownership(user_id, item_id)
        with pytest.raises(ItemNotOwnedError):
            purchase_service.check_ownership(user_id, item_id)

    def test_delete_ownership_no_item(self, purchase_service, user_id):
        with pytest.raises(ItemDoesNotExistError):
            purchase_service.delete_ownership(user_id, 410000000073)

    def test_delete_ownership_no_user(self, purchase_service, item_id):
        with pytest.raises(UserDoesNotExistError):
            purchase_service.delete_ownership(4385751551555, item_id)

    def test_delete_ownership_not_owned(self, purchase_service, user_id, item_id):
        with pytest.raises(ItemNotOwnedError):
            purchase_service.delete_ownership(user_id, item_id)
