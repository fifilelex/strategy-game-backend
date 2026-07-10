from app.domain.exceptions import (
    DatabaseError,
    FieldIsEmpty,
    ItemDoesExist,
    ItemDoesNotExist,
)
from app.domain.models import IncomeSourceCreate, IncomeSourceUpdate
from app.persistence import item_repository as i_repo


def read_item(id: int):
    db_item = i_repo.read_item(id)
    if not db_item:
        raise ItemDoesNotExist
    return db_item


def create_item(item: IncomeSourceCreate):
    # check if item already exists
    if i_repo.search_item_by_name(item.name):
        raise ItemDoesExist
    # creates item in DB

    new_id = i_repo.create_item(
        name=item.name,
        income=item.income,
        cost=item.cost,
        description=item.description,
    )
    # if creation fails -> raise DB error
    if not new_id:
        raise DatabaseError

    return new_id


def update_item(id: int, item: IncomeSourceUpdate):
    # load item from DB
    db_item = i_repo.read_item(id)

    # unpack item as dictionary
    data = item.model_dump(exclude_unset=True)

    # if item does not exist
    if not db_item:
        raise ItemDoesNotExist
    # check if item with such name already exists
    if item.name:
        if i_repo.search_item_by_name(item.name):
            raise ItemDoesExist

    if not data:
        raise FieldIsEmpty

    if i_repo.update_item(id, data) is None:
        raise DatabaseError


def delete_item(id: int):
    # load item from DB
    db_item = i_repo.read_item(id)
    # if item does not exist
    if not db_item:
        raise ItemDoesNotExist
    if i_repo.delete_item(id) is None:
        raise DatabaseError
