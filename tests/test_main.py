from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    ItemAlreadyBoughtError,
    ItemNotOwnedError,
    NotEnoughMoneyError,
    UserDoesExistError,
    UserDoesNotExistError,
)
from app.main import app

client = TestClient(app)


@pytest.fixture
def item():
    return {"name": "Filip", "income": 40, "cost": 400, "description": ""}


@pytest.fixture
def post_item():
    item = {"name": "Filip", "income": 40, "cost": 400, "description": ""}
    response = client.post("/api/item", json=item)
    data = response.json()
    item_id = data["Item_created"]
    item_returned = {
        "item_id": item_id,
        "name": "Filip",
        "income": 40,
        "cost": 400,
        "description": "",
    }
    return item_returned


@pytest.fixture
def post_gamestate():
    gamestate = {
        "username": "fifilelex",
        "turn": 3,
        "money": 1000,
        "income": 999,
        "is_active": True,
    }
    response = client.post("/api/user", json=gamestate)
    data = response.json()
    user_id = data["Gamestate_created"]
    gamestate = {
        "user_id": user_id,
        "username": "fifilelex",
        "turn": 3,
        "money": 1000,
        "income": 999,
        "is_active": True,
    }
    return gamestate


def test_create_item_duplicate(item):
    client.post("/api/item/", json=item)

    response = client.post("/api/item/", json=item)

    assert response.status_code == 409
    assert response.json()["error"] == "Item with such name already exists"


def test_create_item_db_error(item):
    with patch("app.api.api.i_service.create_item") as mock_create:
        mock_create.side_effect = DatabaseError
        response = client.post("/api/item/", json=item)
        assert response.status_code == 500
        assert response.json()["error"] == "Database error"


def test_update_item_field_is_empty(post_item):
    item_id = post_item["item_id"]
    with patch("app.api.api.i_service.update_item") as mock_update:
        mock_update.side_effect = FieldIsEmptyError
        empty_item = {}
        response = client.patch(
            "/api/item/", params={"item_id": item_id}, json=empty_item
        )
        assert response.status_code == 400
        assert response.json()["error"] == "No fields to update"


def test_create_ownership_already_bought():
    with patch("app.api.api.p_service.buy_item") as mock_create:
        mock_create.side_effect = ItemAlreadyBoughtError
        ownership_data = {"user_id": 4, "item_id": 6}
        response = client.post("/api/user/ownership", json=ownership_data)
        assert response.status_code == 409
        assert response.json()["error"] == "Item already bought"


def test_delete_ownership_item_not_owned():
    with patch("app.api.api.p_service.delete_ownership") as mock_delete:
        mock_delete.side_effect = ItemNotOwnedError
        ownership_data = {"user_id": 4, "item_id": 4}
        response = client.request("delete", "/api/user/ownership", json=ownership_data)
        assert response.status_code == 404
        assert response.json()["error"] == "Item not owned"


def test_create_ownership_no_money():
    with patch("app.api.api.p_service.buy_item") as mock_create:
        mock_create.side_effect = NotEnoughMoneyError
        ownership_data = {"user_id": 4, "item_id": 6}
        response = client.post("/api/user/ownership", json=ownership_data)
        assert response.status_code == 409
        assert response.json()["error"] == "User has not enough money"


def test_create_gamestate(post_gamestate):
    with patch("app.api.api.g_service.create_gamestate") as mock_create:
        mock_create.side_effect = UserDoesExistError
        post_gamestate.pop("user_id")
        response = client.post("/api/user/", json=post_gamestate)
        assert response.status_code == 409
        assert response.json()["error"] == "User already exists"


def test_delete_gamestate():
    with patch("app.api.api.g_service.create_gamestate") as mock_create:
        mock_create.side_effect = UserDoesNotExistError

        response = client.request("delete", "/api/user/", params={"user_id": 4})
        assert response.status_code == 404
        assert response.json()["error"] == "User not found"
