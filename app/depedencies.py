from typing import Any

from app.database.database import create_db_engine
from app.persistence.game_repository import GameRepository
from app.persistence.init_db import initialize_db
from app.persistence.item_repository import ItemRepository
from app.services.gamestate_service import GameService
from app.services.item_service import ItemService
from app.services.purchase_service import PurchaseService


def init_services_and_db(database_url: str) -> dict[str, Any]:
    engine = create_db_engine(database_url)
    initialize_db(engine)
    item_repository = ItemRepository(engine)
    game_repository = GameRepository(engine)
    return {
        "game_service": GameService(game_repository),
        "item_service": ItemService(item_repository),
        "purchase_service": PurchaseService(game_repository, item_repository),
    }
