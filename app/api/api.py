from fastapi import APIRouter

from app.depedencies import game_service, item_service, purchase_service
from app.domain.models import (
    GameState,
    GameStateCreate,
    GameStateUpdate,
    IncomeSourceCreate,
    IncomeSourceRead,
    IncomeSourceUpdate,
    Ownership,
)

router = APIRouter()


@router.post("/api/item/")
def create_item(item: IncomeSourceCreate) -> dict[str, int]:

    new_id = item_service.create_item(item)

    return {"Item_created": new_id}


@router.get("/api/items")
def read_items() -> list[IncomeSourceRead] | None:
    rows = item_service.read_items()

    return rows


@router.get("/api/item/{item_id:int}")
def read_item(item_id: int) -> IncomeSourceRead:
    item = item_service.read_item(item_id)
    return item


@router.patch("/api/item/")
def update_item(item_id: int, item: IncomeSourceUpdate) -> dict[str, int]:
    updated_id = item_service.update_item(item_id, item)

    return {"Item_updated": updated_id}


@router.delete("/api/item/")
def delete_item(item_id: int) -> dict[str, int]:
    deleted_id = item_service.delete_item(item_id)

    return {"Item_deleted": deleted_id}


@router.get("/api/user/{user_id:int}")
def read_gamestate(user_id: int) -> GameState:
    gamestate = game_service.read_gamestate(user_id)

    return gamestate


@router.post("/api/user/")
def create_gamestate(game: GameStateCreate) -> dict[str, int]:

    new_id = game_service.create_gamestate(game)

    return {"Gamestate_created": new_id}


@router.patch("/api/user/")
def update_gamestate(user_id: int, game: GameStateUpdate) -> dict[str, int]:
    updated_id = game_service.update_gamestate(user_id, game)

    return {"Gamestate_updated": updated_id}


@router.delete("/api/user/")
def delete_gamestate(user_id: int) -> dict[str, int]:

    deleted_id = game_service.delete_gamestate(user_id)

    return {"Gamestate_deleted": deleted_id}


@router.get("/api/user/ownerships/{user_id:int}")
def read_ownerships(user_id: int) -> list[Ownership]:

    ownerships = purchase_service.check_ownerships(user_id)

    return ownerships


@router.get("/api/user/ownership")
def read_ownership(user_id: int, item_id: int) -> Ownership:
    ownership = purchase_service.check_ownership(user_id, item_id)

    return ownership


@router.post("/api/user/ownership")
def create_ownership(ownership: Ownership) -> dict[str, str]:
    purchase_service.buy_item(ownership.user_id, ownership.item_id)

    return {"Ownership_created": "OK"}


@router.delete("/api/user/ownership")
def delete_ownership(ownership: Ownership) -> dict[str, str]:

    purchase_service.delete_ownership(ownership.user_id, ownership.item_id)

    return {"Ownership_deleted": "OK"}
