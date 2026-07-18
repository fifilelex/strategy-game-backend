from unittest.mock import patch

import pytest
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    UserDoesExistError,
    UserDoesNotExistError,
)
from app.domain.models import GameStateCreate, GameStateUpdate


class TestGameService:
    @pytest.fixture
    def user_id(self, game_repository):
        user_id = game_repository.create_gamestate(
            username="fifilelex", turn=10, money=1000, income=1000, is_active=True
        )
        return user_id

    def test_read_gamestate(self, game_service, user_id):
        data = game_service.read_gamestate(user_id)
        assert data.model_dump() == {
            "user_id": user_id,
            "username": "fifilelex",
            "turn": 10,
            "money": 1000,
            "income": 1000,
            "is_active": True,
        }

    def test_update_gamestate_success(self, game_service, user_id):

        game = GameStateUpdate(username="kazik", money=999)
        game_service.update_gamestate(user_id, game)

        game_updated = game_service.read_gamestate(user_id)
        assert game_updated.username == "kazik"
        assert game_updated.money == 999

    def test_delete_gamestate_success(self, game_service, user_id):
        game_service.delete_gamestate(user_id)
        with pytest.raises(UserDoesNotExistError):
            game_service.read_gamestate(user_id)

    def test_create_gamestate_empty_field(self, game_service):
        game = GameStateCreate.model_construct(
            username=None, turn=None, money=424, income=100, is_active=True
        )
        with pytest.raises(FieldIsEmptyError):
            game_service.create_gamestate(game)

    def test_create_gamestate_exists(self, game_service):

        game = GameStateCreate(
            username="krzys", turn=1, money=424, income=100, is_active=True
        )
        game_service.create_gamestate(game)
        with pytest.raises(UserDoesExistError):
            game_service.create_gamestate(game)

    def test_create_gamestate_db_error(self, game_service):
        with patch.object(game_service.game_repo.engine, "begin") as mock_connect:
            mock_connect.side_effect = SQLAlchemyError
            game = GameStateCreate(
                username="krzys", turn=1, money=424, income=100, is_active=True
            )
            with pytest.raises(DatabaseError):
                game_service.create_gamestate(game)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )
            with pytest.raises(DatabaseError):
                game_service.create_gamestate(game)

    def test_create_gamestate_none(self, game_service):
        with patch.object(game_service.game_repo.engine, "begin") as mock_connect:
            mock_conn = mock_connect.return_value.__enter__.return_value
            mock_conn.execute.return_value.fetchone.return_value = None

            game = GameStateCreate(
                username="krzys", turn=1, money=424, income=100, is_active=True
            )
            with pytest.raises(DatabaseError):
                game_service.create_gamestate(game)

    def test_update_gamestate_no_user(self, game_service):

        game = GameStateUpdate(username="kazik", money=999)
        with pytest.raises(UserDoesNotExistError):
            game_service.update_gamestate(4, game)

    def test_update_gamestate_failed(self, user_id, game_service):
        uid = user_id
        with patch.object(game_service.game_repo, "update_gamestate") as mock_update:
            mock_update.return_value = None
            game = GameStateUpdate(username="kazik", money=999)
            with pytest.raises(DatabaseError):
                game_service.update_gamestate(uid, game)

    def test_update_gamestate_db_error(self, user_id, game_service):
        uid = user_id
        with patch.object(game_service.game_repo.engine, "begin") as mock_connect:
            mock_connect.side_effect = SQLAlchemyError
            game = GameStateUpdate(username="kazik", money=999)
            with pytest.raises(DatabaseError):
                game_service.update_gamestate(uid, game)
            mock_connect.side_effect = DBAPIError(
                "patch", {}, Exception("Database is down")
            )
            with pytest.raises(DatabaseError):
                game_service.update_gamestate(uid, game)

    def test_delete_gamestate_no_user(self, game_service):
        with patch.object(game_service.game_repo.engine, "begin") as mock_connect:
            mock_conn = mock_connect.return_value.__enter__.return_value
            mock_conn.execute.return_value.fetchone.return_value = None

            with pytest.raises(UserDoesNotExistError):
                game_service.delete_gamestate(4)

    def test_delete_gamestate_db_error(self, user_id, game_service):
        uid = user_id
        with patch.object(game_service.game_repo.engine, "begin") as mock_connect:
            mock_connect.side_effect = SQLAlchemyError
            with pytest.raises(DatabaseError):
                game_service.delete_gamestate(uid)
            mock_connect.side_effect = DBAPIError(
                "delete", {}, Exception("Database is down")
            )
            with pytest.raises(DatabaseError):
                game_service.delete_gamestate(uid)

    def test_delete_gamestate_failed(self, user_id, game_service):
        uid = user_id
        with patch.object(game_service.game_repo, "delete_gamestate") as mock_delete:
            mock_delete.return_value = None
            with pytest.raises(DatabaseError):
                game_service.delete_gamestate(uid)
