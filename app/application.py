from fastapi import FastAPI

from app.api.api import create_router
from app.api.exception_handlers import create_handlers
from app.depedencies import create_services


def create_app(
    database_url: str, *, game_service=None, item_service=None, purchase_service=None
):

    if game_service is None and item_service is None and purchase_service is None:
        services = create_services(database_url)
        game_service = services["game_service"]
        item_service = services["item_service"]
        purchase_service = services["purchase_service"]

    app = FastAPI()

    router = create_router(game_service, item_service, purchase_service)

    app.include_router(router)

    create_handlers(app)

    return app
