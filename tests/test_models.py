from app.domain.models import (
    GameState,
    GameStateCreate,
    GameStateUpdate,
    IncomeSource,
    IncomeSourceCreate,
    IncomeSourceUpdate,
)


def test_income_source_success():
    item = IncomeSource(id_gamestate=1, item_id=4, name="Factory", income=400, cost=40)
    assert item.id_gamestate == 1
    assert item.item_id == 4
    assert item.name == "Factory"
    assert item.income == 400
    assert item.cost == 40


def test_incomesourcecreate_success():
    item = IncomeSourceCreate(name="maciek", income=10, cost=100)
    assert item.name == "maciek"
    assert item.income == 10
    assert item.cost == 100
    assert item.description == ""


def test_incomesourceupdate_partial_update():
    item = IncomeSourceUpdate(name="Krzysiu", cost=40)
    assert item.name == "Krzysiu"
    assert item.income is None
    assert item.cost == 40
    assert item.description is None


def test_gamestatesucces():
    game = GameState(
        user_id=4,
        username="kayle",
        turn=40,
        money=7325,
        income=230,
        is_active=True,
    )
    assert game.user_id == 4
    assert game.username == "kayle"
    assert game.turn == 40
    assert game.money == 7325
    assert game.income == 230
    assert game.is_active


def test_gamestatecreate_success():
    game = GameStateCreate(
        username="kayle",
        turn=40,
        money=7325,
        income=230,
        is_active=True,
    )

    assert game.username == "kayle"
    assert game.turn == 40
    assert game.money == 7325
    assert game.income == 230
    assert game.is_active


def test_gamestateupdate_success():
    game = GameStateUpdate(
        turn=40,
        money=7325,
        income=230,
    )

    assert game.username is None
    assert game.turn == 40
    assert game.money == 7325
    assert game.income == 230
    assert game.is_active is None
