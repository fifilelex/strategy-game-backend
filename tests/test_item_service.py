import pytest

from app.domain.exceptions import FieldIsEmpty, ItemDoesExist, ItemDoesNotExist
from app.domain.models import IncomeSourceCreate, IncomeSourceUpdate
from app.persistence import item_repository as i_repo
from app.services.item_service import (
    create_item,
    delete_item,
    read_item,
    update_item,
)


@pytest.fixture
def id():
    id = i_repo.create_item(
        name="Factory",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    return id


@pytest.fixture
def id2():
    id2 = i_repo.create_item(
        name="Factory_2",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    return id2


def test_read_item_success(id):
    item = read_item(id)
    assert isinstance(read_item(id), dict)
    assert item["name"] == "Factory"
    assert item["income"] == 400
    assert item["cost"] == 10000
    assert item["description"] == "Produces various goods"


def test_read_item_no_item():
    with pytest.raises(ItemDoesNotExist):
        read_item(999999999)


def test_create_item_success():
    item = IncomeSourceCreate(
        name="Factory",
        income=400,
        cost=10000,
        description="Produces various goods",
    )
    id = create_item(item)
    assert isinstance(id, int)

    item_data = read_item(id)

    assert item_data["name"] == "Factory"
    assert item_data["income"] == 400
    assert item_data["cost"] == 10000
    assert item_data["description"] == "Produces various goods"


def test_create_item_already_exists(id):
    item = IncomeSourceCreate(
        name="Factory",
        income=4000,
        cost=100020,
        description="Produces various goods",
    )
    with pytest.raises(ItemDoesExist):
        create_item(item)


def test_update_item_success(id):
    item_data = IncomeSourceUpdate(cost=2137)
    update_item(id, item_data)

    updated_data = read_item(id)

    assert updated_data["cost"] == 2137


def test_update_item_does_not_exist(id):
    with pytest.raises(ItemDoesNotExist):
        update_item(900000000000000, IncomeSourceUpdate(income=4))


def test_update_item_name_exists(id, id2):
    with pytest.raises(ItemDoesExist):
        update_item(id2, IncomeSourceUpdate(name="Factory"))


def test_update_item_empty_data(id):
    with pytest.raises(FieldIsEmpty):
        update_item(id, IncomeSourceUpdate())


def test_delete_item_success(id):
    assert read_item(id) != {}

    delete_item(id)

    with pytest.raises(ItemDoesNotExist):
        read_item(id)


def test_delete_item_does_not_exist():
    with pytest.raises(ItemDoesNotExist):
        delete_item(99999999999)
