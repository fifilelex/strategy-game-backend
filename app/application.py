from fastapi import FastAPI

from app.api.api import create_router
from app.api.exception_handlers import create_handlers
from app.depedencies import init_services_and_db
from app.services.gamestate_service import GameService
from app.services.item_service import ItemService
from app.services.purchase_service import PurchaseService


def create_app(
    database_url: str,
    *,
    game_service: GameService | None = None,
    item_service: ItemService | None = None,
    purchase_service: PurchaseService | None = None
) -> FastAPI:

    if game_service is None and item_service is None and purchase_service is None:
        services = init_services_and_db(database_url)
        game_service = services["game_service"]
        item_service = services["item_service"]
        purchase_service = services["purchase_service"]

    app = FastAPI()
    if game_service is None or item_service is None or purchase_service is None:
        raise ValueError
    router = create_router(game_service, item_service, purchase_service)

    app.include_router(router)

    create_handlers(app)

    return app
