from unittest.mock import patch

import pytest
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from app.domain.exceptions import (
    DatabaseError,
    FieldIsInvalidError,
)


class TestGameRepository:
    @pytest.fixture
    def user(self, game_repository):
        user_id = game_repository.create_gamestate(
            username="fifilelex", turn=10, money=1000, income=1000, is_active=True
        )
        model = {
            "user_id": user_id,
            "username": "fifilelex",
            "turn": 10,
            "money": 1000,
            "income": 1000,
            "is_active": True,
        }
        return model

    def test_read_gamestate_db_error(self, game_repository):
        with patch.object(game_repository.engine, "connect") as mock_connect:
            mock_connect.side_effect = SQLAlchemyError

            with pytest.raises(DatabaseError):
                game_repository.read_gamestate(5)
            mock_connect.side_effect = DBAPIError(
                "select", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                game_repository.read_gamestate(5)

    def test_search_gamestate_by_name(self, game_repository, user):
        model = user
        db_model = game_repository.search_gamestate_by_name(
            model["username"], model["turn"]
        )
        assert db_model is not None
        assert model["user_id"] == db_model["user_id"]
        assert model["username"] == db_model["username"]
        assert model["turn"] == db_model["turn"]
        assert model["money"] == db_model["money"]
        assert model["income"] == db_model["income"]
        assert model["is_active"] == db_model["is_active"]

    def test_search_gamestate_by_name_db_error(self, game_repository):
        with patch.object(game_repository.engine, "connect") as mock_connect:

            mock_connect.side_effect = SQLAlchemyError

            with pytest.raises(DatabaseError):
                game_repository.search_gamestate_by_name("katy", 5)

            mock_connect.side_effect = DBAPIError(
                "select", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                game_repository.search_gamestate_by_name("katy", 5)

    def test_create_gamestate_db_error(self, game_repository):
        with patch.object(game_repository.engine, "connect") as mock_connect:

            mock_connect.side_effect = SQLAlchemyError

            with pytest.raises(DatabaseError):
                game_repository.create_gamestate(
                    username="fifilelex",
                    turn=10,
                    money=1000,
                    income=1000,
                    is_active=True,
                )

            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                game_repository.create_gamestate(
                    username="fifilelex",
                    turn=10,
                    money=1000,
                    income=1000,
                    is_active=True,
                )

    def test_update_gamestate_invalid_key(self, user, game_repository):
        model = user
        user_id = model["user_id"]
        data = {"username": "Cris", "A bad key": 14}
        with pytest.raises(FieldIsInvalidError):
            game_repository.update_gamestate(user_id, data)

    def test_update_gamestate_db_error(self, user, game_repository):
        model = user
        user_id = model["user_id"]
        data = {"username": "Cris"}
        with patch.object(game_repository.engine, "connect") as mock_connect:

            mock_connect.side_effect = SQLAlchemyError
            with pytest.raises(DatabaseError):
                game_repository.update_gamestate(user_id, data)
            mock_connect.side_effect = DBAPIError(
                "patch", {}, Exception("Database is down")
            )
            with pytest.raises(DatabaseError):
                game_repository.update_gamestate(user_id, data)

    def test_delete_gamestate_db_error(self, user, game_repository):
        model = user
        user_id = model["user_id"]
        with patch.object(game_repository.engine, "connect") as mock_connect:

            mock_connect.side_effect = SQLAlchemyError
            with pytest.raises(DatabaseError):
                game_repository.delete_gamestate(user_id)
            mock_connect.side_effect = DBAPIError(
                "delete", {}, Exception("Database is down")
            )
            with pytest.raises(DatabaseError):
                game_repository.delete_gamestate(user_id)

    def test_create_gamestate_row_is_none(self, game_repository):
        with patch.object(game_repository.engine, "connect") as mock_connect:
            mock_conn = mock_connect.return_value.__enter__.return_value
            mock_conn.execute.return_value.fetchone.return_value = None

            assert (
                game_repository.create_gamestate(
                    username="fifilelex",
                    turn=10,
                    money=1000,
                    income=1000,
                    is_active=True,
                )
                is None
            )
