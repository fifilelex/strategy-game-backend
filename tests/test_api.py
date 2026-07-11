from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_read_items():

    response = client.get("/api/items")
    assert response.status_code == 200
    assert response.json() == []


def test_create_item():
    item = {"name": "Filip", "income": 40, "cost": 400, "description": ""}
    response = client.post("/api/item/", json=item)
    data = response.json()

    assert response.status_code == 200
    assert "id" in data
    assert isinstance(data["id"], int)


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

    assert "detail" in data
    assert data["detail"]["error"] == "Item not found"


def test_read_item_id_string():
    response = client.get("/api/item/chivas")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    print(data)
    assert data["detail"] == "Not Found"


def test_read_item():
    item = {"name": "Filip", "income": 40, "cost": 400, "description": ""}
    response = client.post("/api/item/", json=item)
    data = response.json()
    id = data["id"]
    tested_response = client.get(f"/api/item/{id}")
    assert tested_response.status_code == 200
    data = tested_response.json()
    assert id == data["id"]
    assert item["name"] == data["name"]
    assert item["income"] == data["income"]
    assert item["cost"] == data["cost"]
    assert item["description"] == data["description"]
