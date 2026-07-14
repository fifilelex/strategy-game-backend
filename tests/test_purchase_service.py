from unittest.mock import patch

import pytest

from app.domain.exceptions import (
    DatabaseError,
    ItemAlreadyBoughtError,
    ItemDoesNotExistError,
    ItemNotOwnedError,
    NotEnoughMoneyError,
    UserDoesNotExistError,
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
def user_id():
    user_id = create_gamestate(
        username="fifilelex",
        turn=3,
        money=99999,
        income=999999,
        is_active=True,
    )
    return user_id


@pytest.fixture
def item_id():
    item_id = create_item(
        name="Factory",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    return item_id


@pytest.fixture
def ownership(user_id, item_id):

    if user_id and item_id:
        create_ownership(user_id, item_id)


def test_buy_item_succcess(user_id, item_id):
    buy_item(user_id, item_id)

    ownership = check_ownership(user_id, item_id)
    assert ownership.user_id == user_id
    assert ownership.item_id == item_id


def test_buy_item_read_gamestate_database_error(user_id, item_id):
    with patch("app.services.purchase_service.g_repo.read_gamestate") as mock_read:
        mock_read.side_effect = DatabaseError

        with pytest.raises(DatabaseError):
            buy_item(user_id, item_id)


def test_buy_item_read_item_database_error(user_id, item_id):
    with patch(
        "app.services.purchase_service.g_repo.read_gamestate"
    ) as mock_game, patch(
        "app.services.purchase_service.i_repo.read_item"
    ) as mock_item:

        mock_game.return_value = {
            "money": 100,
            "income": 10,
        }
        mock_item.side_effect = DatabaseError

        with pytest.raises(DatabaseError):
            buy_item(user_id, item_id)


def test_buy_item_create_ownership_database_error(user_id, item_id):
    with patch(
        "app.services.purchase_service.g_repo.read_gamestate"
    ) as mock_game, patch(
        "app.services.purchase_service.i_repo.read_item"
    ) as mock_item, patch(
        "app.services.purchase_service.i_repo.read_ownership"
    ) as mock_ownership, patch(
        "app.services.purchase_service.i_repo.create_ownership"
    ) as mock_create:

        mock_game.return_value = {
            "money": 100,
            "income": 10,
        }
        mock_item.return_value = {
            "cost": 50,
            "income": 5,
        }
        mock_ownership.return_value = None
        mock_create.return_value = False

        with pytest.raises(DatabaseError):
            buy_item(user_id, item_id)


def test_buy_item_update_gamestate_database_error(user_id, item_id):
    with patch(
        "app.services.purchase_service.g_repo.read_gamestate"
    ) as mock_game, patch(
        "app.services.purchase_service.i_repo.read_item"
    ) as mock_item, patch(
        "app.services.purchase_service.i_repo.read_ownership"
    ) as mock_ownership, patch(
        "app.services.purchase_service.i_repo.create_ownership"
    ) as mock_create, patch(
        "app.services.purchase_service.g_repo.update_gamestate"
    ) as mock_update:

        mock_game.return_value = {
            "money": 100,
            "income": 10,
        }
        mock_item.return_value = {
            "cost": 50,
            "income": 5,
        }
        mock_ownership.return_value = None
        mock_create.return_value = True
        mock_update.return_value = None

        with pytest.raises(DatabaseError):
            buy_item(user_id, item_id)


def test_check_ownerships_none(user_id):
    with patch("app.services.purchase_service.i_repo.read_ownerships") as mock_read:
        mock_read.return_value = None
        assert check_ownerships(user_id) == []


def test_delete_ownership_item_not_owned(user_id, item_id):
    with patch("app.services.purchase_service.g_repo.read_gamestate") as mock_read:
        mock_read.return_value = {"a": 1}

    with patch("app.services.purchase_service.i_repo.read_item") as mock_read:
        mock_read.return_value = {"a": 1}
    with patch("app.services.purchase_service.check_ownership") as mock_check:
        mock_check.return_value = None
        with pytest.raises(ItemNotOwnedError):
            delete_ownership(user_id, item_id)


def test_delete_ownership_db_error(user_id, item_id):
    with patch(
        "app.services.purchase_service.g_repo.read_gamestate"
    ) as mock_gamestate, patch(
        "app.services.purchase_service.i_repo.read_item"
    ) as mock_item, patch(
        "app.services.purchase_service.check_ownership"
    ) as mock_check, patch(
        "app.services.purchase_service.i_repo.delete_ownership"
    ) as mock_delete:

        mock_gamestate.return_value = {
            "money": 100,
            "income": 10,
        }

        mock_item.return_value = {
            "cost": 50,
            "income": 5,
        }

        mock_check.return_value = True
        mock_delete.return_value = False

        with pytest.raises(DatabaseError):
            delete_ownership(user_id, item_id)


def test_delete_ownership_no_change_error(user_id, item_id):
    with patch(
        "app.services.purchase_service.g_repo.read_gamestate"
    ) as mock_gamestate, patch(
        "app.services.purchase_service.i_repo.read_item"
    ) as mock_item, patch(
        "app.services.purchase_service.check_ownership"
    ) as mock_check, patch(
        "app.services.purchase_service.i_repo.delete_ownership"
    ) as mock_delete, patch(
        "app.services.purchase_service.g_repo.update_gamestate"
    ) as mock_update:

        mock_gamestate.return_value = {
            "money": 100,
            "income": 10,
        }

        mock_item.return_value = {
            "cost": 50,
            "income": 5,
        }

        mock_check.return_value = True
        mock_delete.return_value = True
        mock_update.return_value = None

        with pytest.raises(DatabaseError):
            delete_ownership(user_id, item_id)


def test_buy_item_no_gamestate(item_id):
    with pytest.raises(UserDoesNotExistError):
        buy_item(user_id=9999999, item_id=item_id)


def test_buy_no_item(user_id):
    with pytest.raises(ItemDoesNotExistError):
        buy_item(user_id=user_id, item_id=99999999)


def test_buy_already_owned(user_id, item_id, ownership):
    with pytest.raises(ItemAlreadyBoughtError):
        buy_item(user_id, item_id)


def test_buy_not_enough_money(item_id):
    user_id = create_gamestate(
        username="fifilelex", turn=4, money=0, income=100, is_active=True
    )
    if user_id and item_id:
        with pytest.raises(NotEnoughMoneyError):
            buy_item(user_id, item_id)


def test_check_ownerships_success(user_id, item_id, ownership):
    ownership = check_ownerships(user_id)
    for relation in ownership:
        assert relation.user_id == user_id
        assert relation.item_id == item_id


def test_check_ownerships_empty(user_id):
    ownerships = check_ownerships(user_id)
    assert ownerships == []


def test_check_ownerships_no_user(user_id, item_id, ownership):
    with pytest.raises(UserDoesNotExistError):
        check_ownerships(4444444444444444)


def test_check_ownership_success(user_id, item_id, ownership):
    ownership = check_ownership(user_id, item_id)
    assert ownership.user_id == user_id
    assert ownership.item_id == item_id


def test_check_ownership_no_user(user_id, item_id, ownership):
    with pytest.raises(UserDoesNotExistError):
        check_ownership(4444444444444444, item_id)


def test_check_ownership_not_owned(user_id, item_id):
    with pytest.raises(ItemNotOwnedError):
        check_ownership(user_id, item_id)


def test_delete_ownership_success(user_id, item_id, ownership):
    ownership = check_ownership(user_id, item_id)
    assert ownership.user_id == user_id
    assert ownership.item_id == item_id
    delete_ownership(user_id, item_id)
    with pytest.raises(ItemNotOwnedError):
        check_ownership(user_id, item_id)


def test_delete_ownership_no_item(user_id):
    with pytest.raises(ItemDoesNotExistError):
        delete_ownership(user_id, 410000000073)


def test_delete_ownership_no_user(item_id):
    with pytest.raises(UserDoesNotExistError):
        delete_ownership(4385751551555, item_id)


def test_delete_ownership_not_owned(user_id, item_id):
    with pytest.raises(ItemNotOwnedError):
        delete_ownership(user_id, item_id)
