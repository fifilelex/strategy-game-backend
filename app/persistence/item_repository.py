from typing import Any, cast

from sqlalchemy import CursorResult, Engine, and_, delete, insert, select, update
from sqlalchemy.exc import DBAPIError, SQLAlchemyError
from sqlalchemy.orm import sessionmaker

from app.domain.exceptions import DatabaseError, FieldIsInvalidError
from app.persistence.tables import items, ownership

ALLOWED_KEY = {"name", "cost", "income", "description"}


class ItemRepository:
    def __init__(self, engine: Engine):
        self.engine = engine
        self.session_factory = sessionmaker(engine)

    def create_item(
        self, name: str, income: int, cost: int, description: str
    ) -> int | None:
        try:
            with self.session_factory.begin() as session:
                result = session.execute(
                    insert(items)
                    .values(
                        name=name, income=income, cost=cost, description=description
                    )
                    .returning(items.c.item_id)
                )

                row = result.fetchone()
                if row is None:
                    return None
                return row.item_id

        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def read_items(self) -> list[dict[str, Any]]:
        try:
            with self.session_factory.begin() as session:
                result = session.execute(select(items))
                rows = result.fetchall()
                if rows is None:
                    return []
                # present every item as a dictionary
                return [
                    {
                        "item_id": r[0],
                        "name": r[1],
                        "income": r[2],
                        "cost": r[3],
                        "description": r[4],
                    }
                    for r in rows
                ]
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def read_item(self, item_id: int) -> dict[str, Any] | None:
        try:
            with self.session_factory.begin() as session:
                print("Connection established")

                # get item with matching item_id
                result = session.execute(
                    select(items).where(items.c.item_id == item_id)
                )

                row = result.fetchone()

                if row is None:  # item not found -> return None
                    return None

                # present item as a dictionary
                return {
                    "item_id": row[0],
                    "name": row[1],
                    "income": row[2],
                    "cost": row[3],
                    "description": row[4],
                }
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def search_item_by_name(self, name: str) -> dict[str, Any] | None:
        try:
            with self.session_factory.begin() as session:
                print("Connection established")

                # get item with matching name
                result = session.execute(select(items).where(items.c.name == name))

                row = result.fetchone()

                if row is None:
                    return None

                # present item as a dictionary
                return {
                    "item_id": row[0],
                    "name": row[1],
                    "income": row[2],
                    "cost": row[3],
                    "description": row[4],
                }
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def update_item(self, item_id: int, data: dict) -> int:

        for key in data:
            if key not in ALLOWED_KEY:
                raise FieldIsInvalidError

        try:
            with self.session_factory.begin() as session:
                print("Connection established")
                result = cast(
                    CursorResult,
                    session.execute(
                        update(items).values(data).where(items.c.item_id == item_id)
                    ),
                )
                return result.rowcount

        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def delete_item(self, item_id: int) -> int:
        try:
            with self.session_factory.begin() as session:

                result = cast(
                    CursorResult,
                    session.execute(delete(items).where(items.c.item_id == item_id)),
                )

                return result.rowcount

        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def read_ownerships(self, user_id: int) -> list[dict[str, Any]]:
        try:
            with self.session_factory.begin() as session:
                result = session.execute(
                    select(ownership).where(ownership.c.user_id == user_id)
                )

                rows = result.fetchall()
                return [{"user_id": row[0], "item_id": row[1]} for row in rows]
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def read_ownership(self, user_id: int, item_id: int) -> dict[str, int] | None:
        try:
            with self.session_factory.begin() as session:
                result = session.execute(
                    select(ownership).where(
                        and_(
                            ownership.c.user_id == user_id,
                            ownership.c.item_id == item_id,
                        )
                    )
                )

                row = result.fetchone()

                if row is None:  # ownership not found -> return None
                    return None

                return {"user_id": row[0], "item_id": row[1]}
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def create_ownership(self, user_id: int, item_id: int) -> dict[str, int]:

        try:
            with self.session_factory.begin() as session:
                result = session.execute(
                    insert(ownership)
                    .values(user_id=user_id, item_id=item_id)
                    .returning(ownership.c.user_id, ownership.c.item_id)
                )

                row = result.fetchone()
                return {"user_id": row[0], "item_id": row[1]} if row else {}

        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def delete_ownership(self, user_id: int, item_id: int) -> int:
        try:
            with self.session_factory.begin() as session:
                result = cast(
                    CursorResult,
                    session.execute(
                        delete(ownership).where(
                            and_(
                                ownership.c.user_id == user_id,
                                ownership.c.item_id == item_id,
                            )
                        )
                    ),
                )

                return result.rowcount
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError
