from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmptyError,
    ItemDoesExistError,
    ItemDoesNotExistError,
)
from app.domain.models import (
    IncomeSourceCreate,
    IncomeSourceRead,
    IncomeSourceUpdate,
)
from app.persistence.item_repository import ItemRepository


class ItemService:
    def __init__(self, item_repo: ItemRepository):
        self.item_repo = item_repo

    def read_item(self, item_id: int) -> IncomeSourceRead:
        db_item = self.item_repo.read_item(item_id)
        if not db_item:
            raise ItemDoesNotExistError
        return IncomeSourceRead(**db_item)

    def read_items(self) -> list[IncomeSourceRead] | None:
        db_items = self.item_repo.read_items()
        if db_items == []:
            return []
        return [IncomeSourceRead(**item) for item in db_items]

    def create_item(self, item: IncomeSourceCreate) -> int:
        # check if item already exists
        if self.item_repo.search_item_by_name(item.name):
            raise ItemDoesExistError
        # creates item in DB

        new_id = self.item_repo.create_item(
            name=item.name,
            income=item.income,
            cost=item.cost,
            description=item.description,
        )
        # if creation fails -> raise DB error
        if not new_id:
            raise DatabaseError

        return new_id

    def update_item(self, item_id: int, item: IncomeSourceUpdate) -> int:
        # load item from DB
        db_item = self.item_repo.read_item(item_id)

        # unpack item as dictionary
        data = item.model_dump(exclude_unset=True)

        # if item does not exist
        if not db_item:
            raise ItemDoesNotExistError
        # check if item with such name already exists
        if item.name and self.item_repo.search_item_by_name(item.name):
            raise ItemDoesExistError

        if not data:
            raise FieldIsEmptyError

        rowcount = self.item_repo.update_item(item_id, data)

        if rowcount is None:
            raise DatabaseError
        return item_id

    def delete_item(self, item_id: int) -> int:
        # load item from DB
        db_item = self.item_repo.read_item(item_id)
        # if item does not exist
        if not db_item:
            raise ItemDoesNotExistError
        rowcount = self.item_repo.delete_item(item_id)
        if rowcount is None:
            raise DatabaseError
        return item_id
