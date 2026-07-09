import pytest
from fastapi.testclient import TestClient

import app.persistence.game_repository as g_repo
from app.api.api import app
from app.domain.exceptions import UserDoesNotExist
from app.domain.models import GameStateUpdate
from app.persistence.init_db import get_connection
from app.services.gamestate_service import (
    delete_gamestate,
    read_gamestate,
    update_gamestate,
)

# pyright: reportCallIssue=false
# pyright: reportArgumentType=false


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM ownership;")
    cur.execute("DELETE FROM items;")
    cur.execute("DELETE FROM gamestate;")

    conn.commit()
    conn.close()


@pytest.fixture
def uid():
    uid = g_repo.create_gamestate(
        username="fifilelex", turn=10, money=1000, income=1000, is_active=True
    )
    return uid


def test_read_gamestate(uid):

    assert read_gamestate(uid) == {
        "uid": uid,
        "username": "fifilelex",
        "turn": 10,
        "money": 1000,
        "income": 1000,
        "is_active": True,
    }


def test_update_gamestate_success(uid):

    game = GameStateUpdate(username="kazik", money=999)
    update_gamestate(uid, game)

    game_updated = read_gamestate(uid)
    assert game_updated["username"] == "kazik"
    assert game_updated["money"] == 999


def test_delete_gamestate_success(uid):
    delete_gamestate(uid)
    with pytest.raises(UserDoesNotExist):
        read_gamestate(uid)
