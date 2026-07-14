from unittest.mock import patch

import pytest

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    ItemDoesExistError,
    ItemDoesNotExistError,
)
from app.domain.models import IncomeSourceCreate, IncomeSourceUpdate
from app.persistence import item_repository as i_repo
from app.services.item_service import (
    create_item,
    delete_item,
    read_item,
    read_items,
    update_item,
)


@pytest.fixture
def item_id():
    item_id = i_repo.create_item(
        name="Factory",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    return item_id


@pytest.fixture
def id2():
    id2 = i_repo.create_item(
        name="Factory_2",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    return id2


def test_read_item_success(item_id):
    item = read_item(item_id)

    assert item.name == "Factory"
    assert item.income == 400
    assert item.cost == 10000
    assert item.description == "Produces various goods"


def test_read_item_no_item():
    with pytest.raises(ItemDoesNotExistError):
        read_item(999999999)


def test_read_items_no_items():
    items = read_items()
    assert items == []


def test_read_items_success(item_id, id2):
    test_item = read_item(item_id)
    test_item_2 = read_item(id2)

    list_of_items = read_items()

    assert list_of_items is not None
    assert test_item, test_item_2 in list_of_items


def test_create_item_success():
    item = IncomeSourceCreate(
        name="Factory",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    item_id = create_item(item)

    item_data = read_item(item_id)

    assert item_data.name == "Factory"
    assert item_data.income == 400
    assert item_data.cost == 10000
    assert item_data.description == "Produces various goods"


def test_create_item_already_exists(item_id):
    item = IncomeSourceCreate(
        name="Factory",
        income=4000,
        cost=100020,
        description="Produces various goods",
    )
    with pytest.raises(ItemDoesExistError):
        create_item(item)


def test_create_item_db_error():
    item = IncomeSourceCreate(
        name="Factory",
        income=4000,
        cost=100020,
        description="Produces various goods",
    )
    with patch("app.services.item_service.i_repo.create_item") as mock_create:
        mock_create.return_value = None
        with pytest.raises(DatabaseError):
            create_item(item)


def test_update_item_success(item_id):
    item_data = IncomeSourceUpdate(cost=2137)
    update_item(item_id, item_data)

    updated_data = read_item(item_id)

    assert updated_data.cost == 2137


def test_update_item_does_not_exist(item_id):
    with pytest.raises(ItemDoesNotExistError):
        update_item(900000000000000, IncomeSourceUpdate(income=4))


def test_update_item_name_exists(item_id, id2):
    with pytest.raises(ItemDoesExistError):
        update_item(id2, IncomeSourceUpdate(name="Factory"))


def test_update_item_empty_data(item_id):
    with pytest.raises(FieldIsEmptyError):
        update_item(item_id, IncomeSourceUpdate())


def test_update_item_db_error(item_id):
    item = IncomeSourceUpdate(
        income=40000,
    )
    with patch("app.services.item_service.i_repo.update_item") as mock_update:
        mock_update.return_value = None
        with pytest.raises(DatabaseError):
            update_item(item_id, item)


def test_delete_item_success(item_id):
    assert read_item(item_id) != {}

    delete_item(item_id)

    with pytest.raises(ItemDoesNotExistError):
        read_item(item_id)


def test_delete_item_does_not_exist():
    with pytest.raises(ItemDoesNotExistError):
        delete_item(99999999999)


def test_delete_item_db_error(item_id):

    with patch("app.services.item_service.i_repo.delete_item") as mock_delete:
        mock_delete.return_value = None
        with pytest.raises(DatabaseError):
            delete_item(item_id)
