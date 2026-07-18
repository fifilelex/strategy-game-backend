from unittest.mock import patch

import pytest

from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    ItemDoesExistError,
    ItemDoesNotExistError,
)
from app.domain.models import IncomeSourceCreate, IncomeSourceUpdate


class TestItemService:
    @pytest.fixture
    def item_id(self, item_repository):
        item_id = item_repository.create_item(
            name="Factory",
            income=400,
            cost=10000,
            description="Produces various goods",
        )
        return item_id

    @pytest.fixture
    def id2(self, item_repository):
        id2 = item_repository.create_item(
            name="Factory_2",
            income=400,
            cost=10000,
            description="Produces various goods",
        )
        return id2

    def test_read_item_success(self, item_service, item_id):
        item = item_service.read_item(item_id)

        assert item.name == "Factory"
        assert item.income == 400
        assert item.cost == 10000
        assert item.description == "Produces various goods"

    def test_read_item_no_item(self, item_service):
        with pytest.raises(ItemDoesNotExistError):
            item_service.read_item(999999999)

    def test_read_items_no_items(self, item_service):
        items = item_service.read_items()
        assert items == []

    def test_read_items_success(self, item_service, item_id, id2):
        test_item = item_service.read_item(item_id)
        test_item_2 = item_service.read_item(id2)

        list_of_items = item_service.read_items()

        assert list_of_items is not None
        assert test_item, test_item_2 in list_of_items

    def test_create_item_success(self, item_service):
        item = IncomeSourceCreate(
            name="Factory",
            income=400,
            cost=10000,
            description="Produces various goods",
        )
        item_id = item_service.create_item(item)

        item_data = item_service.read_item(item_id)

        assert item_data.name == "Factory"
        assert item_data.income == 400
        assert item_data.cost == 10000
        assert item_data.description == "Produces various goods"

    def test_create_item_already_exists(self, item_service, item_id):
        item = IncomeSourceCreate(
            name="Factory",
            income=4000,
            cost=100020,
            description="Produces various goods",
        )
        with pytest.raises(ItemDoesExistError):
            item_service.create_item(item)

    def test_create_item_db_error(self, item_service):
        item = IncomeSourceCreate(
            name="Factory",
            income=4000,
            cost=100020,
            description="Produces various goods",
        )
        with patch.object(item_service.item_repo, "create_item") as mock_create:
            mock_create.return_value = None
            with pytest.raises(DatabaseError):
                item_service.create_item(item)

    def test_update_item_success(self, item_service, item_id):
        item_data = IncomeSourceUpdate(cost=2137)
        item_service.update_item(item_id, item_data)

        updated_data = item_service.read_item(item_id)

        assert updated_data.cost == 2137

    def test_update_item_does_not_exist(self, item_service, item_id):
        with pytest.raises(ItemDoesNotExistError):
            item_service.update_item(900000000000000, IncomeSourceUpdate(income=4))

    def test_update_item_name_exists(self, item_service, item_id, id2):
        with pytest.raises(ItemDoesExistError):
            item_service.update_item(id2, IncomeSourceUpdate(name="Factory"))

    def test_update_item_empty_data(self, item_service, item_id):
        with pytest.raises(FieldIsEmptyError):
            item_service.update_item(item_id, IncomeSourceUpdate())

    def test_update_item_db_error(self, item_service, item_id):
        item = IncomeSourceUpdate(
            income=40000,
        )
        with patch.object(item_service.item_repo, "update_item") as mock_update:
            mock_update.return_value = None
            with pytest.raises(DatabaseError):
                item_service.update_item(item_id, item)

    def test_delete_item_success(self, item_service, item_id):
        assert item_service.read_item(item_id) != {}

        item_service.delete_item(item_id)

        with pytest.raises(ItemDoesNotExistError):
            item_service.read_item(item_id)

    def test_delete_item_does_not_exist(self, item_service):
        with pytest.raises(ItemDoesNotExistError):
            item_service.delete_item(99999999999)

    def test_delete_item_db_error(self, item_service, item_id):

        with patch.object(item_service.item_repo, "delete_item") as mock_delete:
            mock_delete.return_value = None
            with pytest.raises(DatabaseError):
                item_service.delete_item(item_id)
