import pytest

from app.domain.exceptions import (
    ItemAlreadyBought,
    ItemDoesNotExist,
    ItemNotOwned,
    NotEnoughMoney,
    UserDoesNotExist,
)
from app.persistence.game_repository import create_gamestate
from app.persistence.item_repository import create_item, create_ownership
from app.services.purchase_service import (
    buy_item,
    check_ownership,
    check_ownerships,
    delete_ownership,
)


@pytest.fixture
def uid():
    uid = create_gamestate(
        username="fifilelex",
        turn=3,
        money=99999,
        income=999999,
        is_active=True,
    )
    return uid


@pytest.fixture
def id():
    id = create_item(
        name="Factory",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    return id


@pytest.fixture
def ownership(uid, id):

    if uid and id:
        create_ownership(uid, id)


def test_buy_item_succcess(uid, id):
    buy_item(uid, id)

    assert check_ownership(uid, id) == {"uid": uid, "id": id}


def test_buy_item_no_gamestate(id):
    with pytest.raises(UserDoesNotExist):
        buy_item(uid=9999999, id=id)


def test_buy_no_item(uid):
    with pytest.raises(ItemDoesNotExist):
        buy_item(uid=uid, id=99999999)


def test_buy_already_owned(uid, id, ownership):
    with pytest.raises(ItemAlreadyBought):
        buy_item(uid, id)


def test_buy_not_enough_money(id):
    uid = create_gamestate(
        username="fifilelex", turn=4, money=0, income=100, is_active=True
    )
    if uid and id:
        with pytest.raises(NotEnoughMoney):
            buy_item(uid, id)


def test_check_ownerships_success(uid, id, ownership):
    assert check_ownerships(uid) == [{"uid": uid, "id": id}]


def test_check_ownerships_no_user(uid, id, ownership):
    with pytest.raises(UserDoesNotExist):
        check_ownerships(4444444444444444)


def test_check_ownership_success(uid, id, ownership):
    assert check_ownership(uid, id) == {"uid": uid, "id": id}


def test_check_ownership_no_user(uid, id, ownership):
    with pytest.raises(UserDoesNotExist):
        check_ownership(4444444444444444, id)


def test_check_ownership_not_owned(uid, id):
    with pytest.raises(ItemNotOwned):
        check_ownership(uid, id)


def test_delete_ownership_success(uid, id, ownership):
    assert check_ownership(uid, id) == {"uid": uid, "id": id}
    delete_ownership(uid, id)
    with pytest.raises(ItemNotOwned):
        check_ownership(uid, id)


def test_delete_ownership_no_item(uid):
    with pytest.raises(ItemDoesNotExist):
        delete_ownership(uid, 410000000073)


def test_delete_ownership_no_user(id):
    with pytest.raises(UserDoesNotExist):
        delete_ownership(4385751551555, id)


def test_delete_ownership_not_owned(uid, id):
    with pytest.raises(ItemNotOwned):
        delete_ownership(uid, id)
