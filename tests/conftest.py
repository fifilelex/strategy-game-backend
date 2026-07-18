import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import text

from app.application import create_app
from app.database.database import create_db_engine
from app.persistence.game_repository import GameRepository
from app.persistence.item_repository import ItemRepository
from app.services.gamestate_service import GameService
from app.services.item_service import ItemService
from app.services.purchase_service import PurchaseService

load_dotenv()
url = os.environ["TEST_DATABASE_URL"]

test_engine = create_db_engine(url)


@pytest.fixture
def game_repository():
    return GameRepository(test_engine)


@pytest.fixture
def item_repository():
    return ItemRepository(test_engine)


@pytest.fixture
def game_service(game_repository):
    return GameService(game_repository)


@pytest.fixture
def item_service(item_repository):
    return ItemService(item_repository)


@pytest.fixture
def purchase_service(game_repository, item_repository):
    return PurchaseService(game_repository, item_repository)


@pytest.fixture(autouse=True)
def reset_db():

    with test_engine.begin() as conn:

        conn.execute(text("DELETE FROM ownership"))
        conn.execute(text("DELETE FROM items"))
        conn.execute(text("DELETE FROM gamestate"))


@pytest.fixture
def app(game_service, item_service, purchase_service):

    app = create_app(
        url,
        game_service=game_service,
        item_service=item_service,
        purchase_service=purchase_service,
    )
    return app


@pytest.fixture
def client(app):
    return TestClient(app)
