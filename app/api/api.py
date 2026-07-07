from fastapi import FastAPI, HTTPException

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmpty,
    ItemAlreadyBought,
    ItemDoesExist,
    ItemDoesNotExist,
    ItemNotOwned,
    NotEnoughMoney,
    UserDoesExist,
    UserDoesNotExist,
)
from app.domain.models import (
    GameState,
    GameStateCreate,
    GameStateUpdate,
    IncomeSourceCreate,
    IncomeSourceUpdate,
)
from app.persistence import init_db as db
from app.persistence import item_repository as i_repo
from app.services import gamestate_service as g_service
from app.services import item_service as i_service
from app.services import purchase_service as p_service

app = FastAPI()

db.init_db()
game = GameState(
    uid=0, username="filip", turn=0, money=999, income=1000, is_active=True
)


@app.post("/api/item/")
def create_item(item: IncomeSourceCreate):

    try:
        new_id = i_service.create_item(item)
    except ItemDoesExist:
        raise HTTPException(
            status_code=409,
            detail={"error": "Item with such name already exists"},
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )

    return {"id": new_id}


@app.get("/api/items")
def read_items():
    rows = i_repo.read_items()

    return rows


@app.get("/api/item/{id:int}")
def read_item(id: int):
    try:
        item = i_service.read_item(id)
    except ItemDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Item not found"}
        )
    return item


@app.patch("/api/item/{id:int}")
def update_item(id: int, item: IncomeSourceUpdate):
    try:
        i_service.update_item(id, item)

    except ItemDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Item not found"}
        )
    except FieldIsEmpty:
        raise HTTPException(
            status_code=400, detail={"error": "No fields to update"}
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )
    except ItemDoesExist:
        raise HTTPException(
            status_code=409,
            detail={"error": "Item with such name already exists"},
        )

    return {"status": "ok"}


@app.delete("/api/item/{id:int}")
def delete_item(id: int):
    try:
        i_service.delete_item(id)
    except ItemDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Item not found"}
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )

    return {"status": "deleted"}


@app.get("/api/user/{uid:int}")
def read_gamestate(uid: int):
    try:
        gamestate = g_service.read_gamestate(uid)
    except UserDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Gamestate not found"}
        )
    return gamestate


@app.post("/api/user/")
def create_gamestate(game: GameStateCreate):
    try:
        new_id = g_service.create_gamestate(game)
    except FieldIsEmpty:
        raise HTTPException(
            status_code=400, detail={"error": "Field is empty"}
        )
    except UserDoesExist:
        raise HTTPException(
            status_code=404, detail={"error": "User already exists"}
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )
    return {"id": new_id}


@app.patch("/api/user/")
def update_gamestate(uid: int, game: GameStateUpdate):
    try:
        g_service.update_gamestate(uid, game)

    # if gamestate not found in DB
    except UserDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Gamestate not found"}
        )
    # if DB update fails - raise HTTP 500
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )

    return {"status": "ok"}


@app.delete("/api/user/")
def delete_gamestate(uid):
    try:
        g_service.delete_gamestate(uid)
    except UserDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Gamestate not found"}
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )
    return {"status": "deleted"}


@app.get("/api/user/ownerships/{uid:int}")
def read_ownerships(uid: int):
    try:
        ownerships = p_service.check_ownerships(uid)

    except UserDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Gamestate not found"}
        )

    return ownerships


@app.get("/api/user/ownership")
def read_ownership(uid: int, id: int):
    try:
        ownership = p_service.check_ownership(uid, id)

    except UserDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Gamestate not found"}
        )

    except ItemNotOwned:
        raise HTTPException(
            status_code=404, detail={"error": "Item not owned"}
        )

    return ownership


@app.post("/api/user/ownership")
def create_ownership(uid: int, id: int):
    try:
        p_service.buy_item(uid, id)

    except UserDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Gamestate not found"}
        )
    except ItemDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Item not found"}
        )
    except ItemAlreadyBought:
        raise HTTPException(
            status_code=409, detail={"error": "Item already bought"}
        )
    except NotEnoughMoney:
        raise HTTPException(
            status_code=409, detail={"error": "User has not enough money"}
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )

    return {"status": "ok"}


@app.delete("/api/user/ownership")
def delete_ownership(uid: int, id: int):
    try:
        p_service.delete_ownership(uid, id)
    except UserDoesNotExist:
        raise HTTPException(
            status_code=404, detail={"error": "Gamestate not found"}
        )
    except ItemNotOwned:
        raise HTTPException(
            status_code=404, detail={"error:": "No such ownership"}
        )
    except DatabaseError:
        raise HTTPException(
            status_code=500, detail={"error": "Database error"}
        )
    return {"status": "ok"}
