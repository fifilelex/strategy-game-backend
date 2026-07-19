from unittest.mock import patch

import pytest
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from app.domain.exceptions import (
    DatabaseError,
    FieldIsInvalidError,
)


class TestItemRepository:
    @pytest.fixture
    def post_item(self, item_repository):
        item_id = item_repository.create_item(
            "Dockyard", 1000, 100000, "Produces ships"
        )
        return item_id

    @pytest.fixture
    def post_item_data(self, item_repository):
        item = {
            "name": "Dockyard",
            "income": 1000,
            "cost": 100000,
            "description": "Produces ships",
        }
        item_repository.create_item("Dockyard", 1000, 100000, "Produces ships")
        return item

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

    def test_create_item_failed(self, item_repository):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            mock_conn = mock_connect.return_value.__enter__.return_value
            mock_conn.execute.return_value.fetchone.return_value = None
            assert (
                item_repository.create_item("Dockyard", 1000, 100000, "Produces ships")
                is None
            )

    def test_create_item_db_error(self, item_repository):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:

            mock_connect.side_effect = SQLAlchemyError

            with pytest.raises(DatabaseError):
                item_repository.create_item("Dockyard", 1000, 100000, "Produces ships")

            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.create_item("Dockyard", 1000, 100000, "Produces ships")

    def test_read_items_empty(self, item_repository):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            mock_conn = mock_connect.return_value.__enter__.return_value
            mock_conn.execute.return_value.fetchall.return_value = None
            assert item_repository.read_items() == []

    def test_read_items_db_error(self, item_repository):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:

            mock_connect.side_effect = SQLAlchemyError

            with pytest.raises(DatabaseError):
                item_repository.read_items()
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.read_items()

    def test_read_item_db_error(self, item_repository, post_item):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            item_id = post_item
            mock_connect.side_effect = SQLAlchemyError

            with pytest.raises(DatabaseError):
                item_repository.read_item(item_id)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.read_item(item_id)

    def test_search_item_by_name_db_error(self, item_repository, post_item_data):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            item_name = post_item_data["name"]
            mock_connect.side_effect = SQLAlchemyError

            with pytest.raises(DatabaseError):
                item_repository.search_item_by_name(item_name)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.search_item_by_name(item_name)

    def test_update_item_invalid_key(self, item_repository, post_item, post_item_data):
        data = post_item_data
        item_id = post_item
        data["smth"] = "someone"
        with pytest.raises(FieldIsInvalidError):
            item_repository.update_item(item_id, data)

    def test_update_item_db_error(self, item_repository, post_item, post_item_data):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            mock_connect.side_effect = SQLAlchemyError
            item_id = post_item
            data = post_item_data
            with pytest.raises(DatabaseError):
                item_repository.update_item(item_id, data)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.update_item(item_id, data)

    def test_delete_item_db_error(self, item_repository, post_item):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            mock_connect.side_effect = SQLAlchemyError
            item_id = post_item
            with pytest.raises(DatabaseError):
                item_repository.delete_item(item_id)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.delete_item(item_id)

    def test_read_ownerships_db_error(self, item_repository, user):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            user_id = user["user_id"]
            mock_connect.side_effect = SQLAlchemyError
            with pytest.raises(DatabaseError):
                item_repository.read_ownerships(user_id)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.read_ownerships(user_id)

    def test_read_ownership_db_error(self, item_repository, user, post_item):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            user_id = user["user_id"]
            mock_connect.side_effect = SQLAlchemyError
            item_id = post_item
            with pytest.raises(DatabaseError):
                item_repository.read_ownership(user_id, item_id)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.read_ownership(user_id, item_id)

    def test_create_ownership_db_error(self, item_repository, user, post_item):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            user_id = user["user_id"]
            mock_connect.side_effect = SQLAlchemyError
            item_id = post_item
            with pytest.raises(DatabaseError):
                item_repository.create_ownership(user_id, item_id)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.create_ownership(user_id, item_id)

    def test_delete_ownership_db_error(self, item_repository, user, post_item):
        with patch.object(item_repository.session_factory, "begin") as mock_connect:
            user_id = user["user_id"]
            mock_connect.side_effect = SQLAlchemyError
            item_id = post_item
            with pytest.raises(DatabaseError):
                item_repository.delete_ownership(user_id, item_id)
            mock_connect.side_effect = DBAPIError(
                "post", {}, Exception("Database is down")
            )

            with pytest.raises(DatabaseError):
                item_repository.delete_ownership(user_id, item_id)
