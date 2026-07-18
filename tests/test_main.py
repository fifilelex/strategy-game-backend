from unittest.mock import patch

import pytest

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    ItemAlreadyBoughtError,
    ItemNotOwnedError,
    NotEnoughMoneyError,
    UserDoesExistError,
    UserDoesNotExistError,
)


@pytest.fixture
def item():
    return {"name": "Filip", "income": 40, "cost": 400, "description": ""}


@pytest.fixture
def post_item(client):
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
def post_gamestate(client):
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


def test_create_item_duplicate(client, item):
    client.post("/api/item/", json=item)

    response = client.post("/api/item/", json=item)

    assert response.status_code == 409
    assert response.json()["error"] == "Item with such name already exists"


def test_create_item_db_error(client, item_service, item):
    with patch.object(item_service, "create_item") as mock_create:
        mock_create.side_effect = DatabaseError
        response = client.post("/api/item/", json=item)
        response = client.post("/api/item/", json=item)
        print("fixture", id(item_service))
        print(response.status_code)
        print(response.json())
        assert response.status_code == 500
        assert response.json()["error"] == "Database error"


def test_update_item_field_is_empty(client, item_service, post_item):
    item_id = post_item["item_id"]
    with patch.object(item_service, "update_item") as mock_update:
        mock_update.side_effect = FieldIsEmptyError
        empty_item = {}
        response = client.patch(
            "/api/item/", params={"item_id": item_id}, json=empty_item
        )
        assert response.status_code == 400
        assert response.json()["error"] == "No fields to update"


def test_create_ownership_already_bought(
    client, post_gamestate, post_item, purchase_service
):
    item_id = post_item["item_id"]
    user_id = post_gamestate["user_id"]
    with patch.object(purchase_service.item_repo, "read_ownership") as mock_create:
        mock_create.side_effect = ItemAlreadyBoughtError
        ownership_data = {"user_id": user_id, "item_id": item_id}
        response = client.post("/api/user/ownership", json=ownership_data)
        assert response.status_code == 409
        assert response.json()["error"] == "Item already bought"


def test_delete_ownership_item_not_owned(
    client, post_gamestate, post_item, purchase_service
):
    item_id = post_item["item_id"]
    user_id = post_gamestate["user_id"]
    with patch.object(purchase_service, "delete_ownership") as mock_delete:
        mock_delete.side_effect = ItemNotOwnedError
        ownership_data = {"user_id": user_id, "item_id": item_id}
        response = client.request("delete", "/api/user/ownership", json=ownership_data)
        assert response.status_code == 404
        assert response.json()["error"] == "Item not owned"


def test_create_ownership_no_money(client, post_gamestate, post_item, purchase_service):
    item_id = post_item["item_id"]
    user_id = post_gamestate["user_id"]
    with patch.object(purchase_service, "buy_item") as mock_create:
        mock_create.side_effect = NotEnoughMoneyError
        ownership_data = {"user_id": user_id, "item_id": item_id}
        response = client.post("/api/user/ownership", json=ownership_data)
        assert response.status_code == 409
        assert response.json()["error"] == "User has not enough money"


def test_create_gamestate(client, post_gamestate, game_service):
    with patch.object(game_service, "create_gamestate") as mock_create:
        mock_create.side_effect = UserDoesExistError
        post_gamestate.pop("user_id")
        response = client.post("/api/user/", json=post_gamestate)
        assert response.status_code == 409
        assert response.json()["error"] == "User already exists"


def test_delete_gamestate(client, game_service):
    with patch.object(game_service, "create_gamestate") as mock_create:
        mock_create.side_effect = UserDoesNotExistError

        response = client.request("delete", "/api/user/", params={"user_id": 4})
        assert response.status_code == 404
        assert response.json()["error"] == "User not found"
