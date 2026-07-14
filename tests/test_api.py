import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


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


def test_read_items():

    response = client.get("/api/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item():
    item = {"name": "Filip", "income": 40, "cost": 400, "description": ""}
    response = client.post("/api/item/", json=item)
    data = response.json()

    assert response.status_code == 200
    assert "Item_created" in data
    assert isinstance(data["Item_created"], int)


def test_create_item_no_name():
    item = {"income": 40, "cost": 400, "description": ""}
    response = client.post("/api/item/", json=item)

    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "name"]
    assert data["detail"][0]["type"] == "missing"


def test_create_item_empty_name():
    item = {"name": "", "income": 40, "cost": 400, "description": ""}
    response = client.post("/api/item/", json=item)
    assert response.status_code == 422

    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "name"]
    assert data["detail"][0]["type"] == "string_too_short"


def test_create_item_negative_income():
    item = {"name": "Filip", "income": -40, "cost": 400, "description": ""}
    response = client.post("/api/item/", json=item)
    assert response.status_code == 422
    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "income"]
    assert data["detail"][0]["type"] == "greater_than"


def test_create_item_changed_field():
    item = {"name": "Filip", "income": 40, "cost": 400, "other_field": "hey"}
    response = client.post("/api/item/", json=item)
    assert response.status_code == 422
    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "other_field"]
    assert data["detail"][0]["type"] == "extra_forbidden"


def test_create_item_additional_field():
    item = {
        "name": "Filip",
        "income": 40,
        "cost": 400,
        "description": "nothing here",
        "other_field": "hey",
    }
    response = client.post("/api/item/", json=item)
    assert response.status_code == 422
    data = response.json()

    assert "detail" in data
    assert data["detail"][0]["loc"] == ["body", "other_field"]
    assert data["detail"][0]["type"] == "extra_forbidden"


def test_read_item_does_not_exist():

    response = client.get("/api/item/2137")
    assert response.status_code == 404
    data = response.json()

    assert "error" in data
    assert data["error"] == "Item not found"


def test_read_item_id_string():
    response = client.get("/api/item/chivas")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    print(data)
    assert data["detail"] == "Not Found"


def test_read_item(post_item):
    item = post_item

    response = client.get(f"/api/item/{item['item_id']}")
    assert response.status_code == 200
    data = response.json()
    assert item["item_id"] == data["item_id"]
    assert item["name"] == data["name"]
    assert item["income"] == data["income"]
    assert item["cost"] == data["cost"]
    assert item["description"] == data["description"]


def test_update_item(post_item):
    item = post_item
    item["name"] = "Kristof"
    item["description"] = "Columbus"
    item_id = item["item_id"]
    item.pop("item_id")
    response = client.patch("/api/item/", params={"item_id": item_id}, json=item)

    assert response.json() == {"Item_updated": item_id}
    assert response.status_code == 200
    test_effect_response = client.get(f"/api/item/{item_id}")
    data = test_effect_response.json()
    assert item_id == data["item_id"]
    assert item["name"] == data["name"]
    assert item["description"] == data["description"]


def test_delete_item(post_item):
    item = post_item
    item_id = item["item_id"]
    response = client.delete("/api/item/", params={"item_id": item_id})
    assert response.json() == {"Item_deleted": item_id}
    assert response.status_code == 200


def test_read_gamestate(post_gamestate):
    gamestate = post_gamestate
    user_id = gamestate["user_id"]
    response = client.get(f"/api/user/{user_id}")
    data = response.json()
    assert gamestate["user_id"] == data["user_id"]
    assert gamestate["username"] == data["username"]
    assert gamestate["turn"] == data["turn"]
    assert gamestate["money"] == data["money"]
    assert gamestate["income"] == data["income"]
    assert gamestate["is_active"] == data["is_active"]


def test_patch_gamestate(post_gamestate):
    gamestate = post_gamestate
    user_id = gamestate["user_id"]
    gamestate["turn"] = 94
    gamestate.pop("user_id")
    response = client.patch("/api/user/", params={"user_id": user_id}, json=gamestate)
    assert response.json() == {"Gamestate_updated": user_id}
    assert response.status_code == 200


def test_delete_gamestate(post_gamestate):
    gameestate = post_gamestate
    user_id = gameestate["user_id"]
    response = client.delete("/api/user/", params={"user_id": user_id})
    assert response.json() == {"Gamestate_deleted": user_id}
    assert response.status_code == 200


def test_create_ownership(post_gamestate, post_item):
    user_id = post_gamestate["user_id"]
    item_id = post_item["item_id"]

    ownership = {"user_id": user_id, "item_id": item_id}
    response = client.post("/api/user/ownership", json=ownership)
    assert response.json() == {"Ownership_created": "OK"}
    assert response.status_code == 200


def test_read_ownership(post_gamestate, post_item):
    user_id = post_gamestate["user_id"]
    item_id = post_item["item_id"]

    ownership = {"user_id": user_id, "item_id": item_id}
    client.post("/api/user/ownership", json=ownership)
    response = client.get(
        "/api/user/ownership/", params={"user_id": user_id, "item_id": item_id}
    )
    data = response.json()
    assert data["user_id"] == user_id
    assert data["item_id"] == item_id
    assert response.status_code == 200


def test_read_ownerships(post_gamestate, post_item):
    user_id = post_gamestate["user_id"]
    item_id = post_item["item_id"]

    ownership = {"user_id": user_id, "item_id": item_id}
    client.post("/api/user/ownership", json=ownership)
    response = client.get(
        f"/api/user/ownerships/{user_id}", params={"user_id": user_id}
    )
    data = response.json()
    assert data == [{"user_id": user_id, "item_id": item_id}]


def test_delete_ownership(post_gamestate, post_item):
    user_id = post_gamestate["user_id"]
    item_id = post_item["item_id"]

    ownership = {"user_id": user_id, "item_id": item_id}
    client.post("/api/user/ownership", json=ownership)
    response = client.request(
        method="DELETE", url="/api/user/ownership", json=ownership
    )
    data = response.json()
    assert data == {"Ownership_deleted": "OK"}
