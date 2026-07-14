from unittest.mock import patch

import pytest
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

import app.persistence.game_repository as g_repo
from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    UserDoesExistError,
    UserDoesNotExistError,
)
from app.domain.models import GameStateCreate, GameStateUpdate
from app.services.gamestate_service import (
    create_gamestate,
    delete_gamestate,
    read_gamestate,
    update_gamestate,
)


@pytest.fixture
def user_id():
    user_id = g_repo.create_gamestate(
        username="fifilelex", turn=10, money=1000, income=1000, is_active=True
    )
    return user_id


def test_read_gamestate(user_id):
    data = read_gamestate(user_id)
    assert data.model_dump() == {
        "user_id": user_id,
        "username": "fifilelex",
        "turn": 10,
        "money": 1000,
        "income": 1000,
        "is_active": True,
    }


def test_update_gamestate_success(user_id):

    game = GameStateUpdate(username="kazik", money=999)
    update_gamestate(user_id, game)

    game_updated = read_gamestate(user_id)
    assert game_updated.username == "kazik"
    assert game_updated.money == 999


def test_delete_gamestate_success(user_id):
    delete_gamestate(user_id)
    with pytest.raises(UserDoesNotExistError):
        read_gamestate(user_id)


def test_create_gamestate_empty_field():
    game = GameStateCreate.model_construct(
        username=None, turn=None, money=424, income=100, is_active=True
    )
    with pytest.raises(FieldIsEmptyError):
        create_gamestate(game)


def test_create_gamestate_exists():

    game = GameStateCreate(
        username="krzys", turn=1, money=424, income=100, is_active=True
    )
    create_gamestate(game)
    with pytest.raises(UserDoesExistError):
        create_gamestate(game)


def test_create_gamestate_db_error():
    with patch("app.persistence.game_repository.engine.begin") as mock_connect:
        mock_connect.side_effect = SQLAlchemyError
        game = GameStateCreate(
            username="krzys", turn=1, money=424, income=100, is_active=True
        )
        with pytest.raises(DatabaseError):
            create_gamestate(game)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))
        with pytest.raises(DatabaseError):
            create_gamestate(game)


def test_create_gamestate_none():
    with patch("app.persistence.game_repository.engine.begin") as mock_connect:
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchone.return_value = None

        game = GameStateCreate(
            username="krzys", turn=1, money=424, income=100, is_active=True
        )
        with pytest.raises(DatabaseError):
            create_gamestate(game)


def test_update_gamestate_no_user():

    game = GameStateUpdate(username="kazik", money=999)
    with pytest.raises(UserDoesNotExistError):
        update_gamestate(4, game)


def test_update_gamestate_failed(user_id):
    uid = user_id
    with patch("app.services.gamestate_service.g_repo.update_gamestate") as mock_update:
        mock_update.return_value = None
        game = GameStateUpdate(username="kazik", money=999)
        with pytest.raises(DatabaseError):
            update_gamestate(uid, game)


def test_update_gamestate_db_error(user_id):
    uid = user_id
    with patch("app.persistence.game_repository.engine.begin") as mock_connect:
        mock_connect.side_effect = SQLAlchemyError
        game = GameStateUpdate(username="kazik", money=999)
        with pytest.raises(DatabaseError):
            update_gamestate(uid, game)
        mock_connect.side_effect = DBAPIError(
            "patch", {}, Exception("Database is down")
        )
        with pytest.raises(DatabaseError):
            update_gamestate(uid, game)


def test_delete_gamestate_no_user():
    with patch("app.persistence.game_repository.engine.begin") as mock_connect:
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchone.return_value = None

        with pytest.raises(UserDoesNotExistError):
            delete_gamestate(4)


def test_delete_gamestate_db_error(user_id):
    uid = user_id
    with patch("app.persistence.game_repository.engine.begin") as mock_connect:
        mock_connect.side_effect = SQLAlchemyError
        with pytest.raises(DatabaseError):
            delete_gamestate(uid)
        mock_connect.side_effect = DBAPIError(
            "delete", {}, Exception("Database is down")
        )
        with pytest.raises(DatabaseError):
            delete_gamestate(uid)


def test_delete_gamestate_failed(user_id):
    uid = user_id
    with patch("app.services.gamestate_service.g_repo.delete_gamestate") as mock_delete:
        mock_delete.return_value = None
        with pytest.raises(DatabaseError):
            delete_gamestate(uid)
