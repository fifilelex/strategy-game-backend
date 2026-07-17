from app.persistence.game_repository import GameRepository
from app.persistence.item_repository import ItemRepository
from app.persistence.tables import engine
from app.services.gamestate_service import GameService
from app.services.item_service import ItemService
from app.services.purchase_service import PurchaseService

item_repository = ItemRepository(engine)
game_repository = GameRepository(engine)
purchase_service = PurchaseService(game_repository, item_repository)
item_service = ItemService(item_repository)
game_service = GameService(game_repository)
