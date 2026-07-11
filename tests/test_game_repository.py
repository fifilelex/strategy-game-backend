import pytest
from conftest import test_engine
from sqlalchemy import text

from app.persistence.game_repository import (
    read_gamestate,
    search_gamestate_by_name,
)


@pytest.fixture
def gamestate_uid():
    with test_engine.begin() as conn:
        result = conn.execute(
            text(
                """INSERT INTO gamestate(username, turn, money, income, is_active)
                VALUES('name', 4, 100, 10, true)
                RETURNING uid"""
            )
        )
        row = result.fetchone()
        if row is None:
            pytest.fail(reason="Failed to create test gamestate")
        uid = row[0]
    return uid


def get_gamestate_from_db(uid):
    with test_engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM gamestate WHERE uid = :uid"), {"uid": uid}
        )
        row = result.mappings().fetchone()
        return row


def test_read_gamestate_success(gamestate_uid):
    assert read_gamestate(gamestate_uid) == {
        "uid": gamestate_uid,
        "username": "name",
        "turn": 4,
        "money": 100,
        "income": 10,
        "is_active": True,
    }


def test_read_gamestate_fail():
    assert read_gamestate(9999999999) is None


def test_search_gamestate_by_name_success(gamestate_uid):
    assert search_gamestate_by_name("name", 4) == {
        "uid": gamestate_uid,
        "username": "name",
        "turn": 4,
        "money": 100,
        "income": 10,
        "is_active": True,
    }


def test_search_gamestate_by_bad_name(gamestate_uid):
    assert search_gamestate_by_name("definietly not name", 4) is None


def test_search_gamestate_by_name_wrong_turn(gamestate_uid):
    assert search_gamestate_by_name("ame", 6) is None
