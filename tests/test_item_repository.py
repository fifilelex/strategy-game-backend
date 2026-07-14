from unittest.mock import patch

import pytest
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from app.domain.exceptions import (
    DatabaseError,
    FieldIsInvalidError,
)
from app.persistence.game_repository import create_gamestate
from app.persistence.item_repository import (
    create_item,
    create_ownership,
    delete_item,
    delete_ownership,
    read_item,
    read_items,
    read_ownership,
    read_ownerships,
    search_item_by_name,
    update_item,
)


@pytest.fixture
def post_item():
    item_id = create_item("Dockyard", 1000, 100000, "Produces ships")
    return item_id


@pytest.fixture
def post_item_data():
    item = {
        "name": "Dockyard",
        "income": 1000,
        "cost": 100000,
        "description": "Produces ships",
    }
    create_item("Dockyard", 1000, 100000, "Produces ships")
    return item


@pytest.fixture
def user():
    user_id = create_gamestate(
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


def test_create_item_failed():
    with patch("app.persistence.item_repository.engine.begin") as mock_connect:
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchone.return_value = None
        assert create_item("Dockyard", 1000, 100000, "Produces ships") is None


def test_create_item_db_error():
    with patch("app.persistence.item_repository.engine.connect") as mock_connect:

        mock_connect.side_effect = SQLAlchemyError

        with pytest.raises(DatabaseError):
            create_item("Dockyard", 1000, 100000, "Produces ships")

        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            create_item("Dockyard", 1000, 100000, "Produces ships")


def test_read_items_empty():
    with patch("app.persistence.item_repository.engine.connect") as mock_connect:
        mock_conn = mock_connect.return_value.__enter__.return_value
        mock_conn.execute.return_value.fetchall.return_value = None
        assert read_items() == []


def test_read_items_db_error():
    with patch("app.persistence.item_repository.engine.connect") as mock_connect:

        mock_connect.side_effect = SQLAlchemyError

        with pytest.raises(DatabaseError):
            read_items()
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            read_items()


def test_read_item_db_error(post_item):
    with patch("app.persistence.item_repository.engine.connect") as mock_connect:
        item_id = post_item
        mock_connect.side_effect = SQLAlchemyError

        with pytest.raises(DatabaseError):
            read_item(item_id)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            read_item(item_id)


def test_search_item_by_name_db_error(post_item_data):
    with patch("app.persistence.item_repository.engine.connect") as mock_connect:
        item_name = post_item_data["name"]
        mock_connect.side_effect = SQLAlchemyError

        with pytest.raises(DatabaseError):
            search_item_by_name(item_name)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            search_item_by_name(item_name)


def test_update_item_invalid_key(post_item, post_item_data):
    data = post_item_data
    item_id = post_item
    data["smth"] = "someone"
    with pytest.raises(FieldIsInvalidError):
        update_item(item_id, data)


def test_update_item_db_error(post_item, post_item_data):
    with patch("app.persistence.item_repository.engine.begin") as mock_connect:
        mock_connect.side_effect = SQLAlchemyError
        item_id = post_item
        data = post_item_data
        with pytest.raises(DatabaseError):
            update_item(item_id, data)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            update_item(item_id, data)


def test_delete_item_db_error(post_item):
    with patch("app.persistence.item_repository.engine.begin") as mock_connect:
        mock_connect.side_effect = SQLAlchemyError
        item_id = post_item
        with pytest.raises(DatabaseError):
            delete_item(item_id)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            delete_item(item_id)


def test_read_ownerships_db_error(user):
    with patch("app.persistence.item_repository.engine.connect") as mock_connect:
        user_id = user["user_id"]
        mock_connect.side_effect = SQLAlchemyError
        with pytest.raises(DatabaseError):
            read_ownerships(user_id)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            read_ownerships(user_id)


def test_read_ownership_db_error(user, post_item):
    with patch("app.persistence.item_repository.engine.connect") as mock_connect:
        user_id = user["user_id"]
        mock_connect.side_effect = SQLAlchemyError
        item_id = post_item
        with pytest.raises(DatabaseError):
            read_ownership(user_id, item_id)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            read_ownership(user_id, item_id)


def test_create_ownership_db_error(user, post_item):
    with patch("app.persistence.item_repository.engine.begin") as mock_connect:
        user_id = user["user_id"]
        mock_connect.side_effect = SQLAlchemyError
        item_id = post_item
        with pytest.raises(DatabaseError):
            create_ownership(user_id, item_id)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            create_ownership(user_id, item_id)


def test_delete_ownership_db_error(user, post_item):
    with patch("app.persistence.item_repository.engine.begin") as mock_connect:
        user_id = user["user_id"]
        mock_connect.side_effect = SQLAlchemyError
        item_id = post_item
        with pytest.raises(DatabaseError):
            delete_ownership(user_id, item_id)
        mock_connect.side_effect = DBAPIError("post", {}, Exception("Database is down"))

        with pytest.raises(DatabaseError):
            delete_ownership(user_id, item_id)
