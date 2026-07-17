from typing import Any

from sqlalchemy import Engine, and_, delete, insert, select, update
from sqlalchemy.exc import DBAPIError, SQLAlchemyError

from app.domain.exceptions import DatabaseError, FieldIsInvalidError
from app.persistence.tables import gamestate

# Load environment variables from .env file

ALLOWED_FIELDS = {"username", "turn", "money", "income", "is_active"}


class GameRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def read_gamestate(self, user_id: int) -> dict[str, Any] | None:

        # establish connection with db
        try:
            with self.engine.connect() as conn:
                print("Connection established")
                result = conn.execute(
                    select(gamestate).where(gamestate.c.user_id == user_id)
                )
                row = result.fetchone()
                if row is None:
                    return None

                return {
                    "user_id": row[0],
                    "username": row[1],
                    "turn": row[2],
                    "money": row[3],
                    "income": row[4],
                    "is_active": row[5],
                }
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def search_gamestate_by_name(self, name: str, turn: int) -> dict[str, Any] | None:

        # establish connection with db
        try:
            with self.engine.connect() as conn:
                print("Connection established")
                result = conn.execute(
                    select(gamestate).where(
                        and_(gamestate.c.username == name, gamestate.c.turn == turn)
                    )
                )

                row = result.fetchone()
                if row is None:
                    return None
                # present gamestate as a dictionary
                return {
                    "user_id": row[0],
                    "username": row[1],
                    "turn": row[2],
                    "money": row[3],
                    "income": row[4],
                    "is_active": row[5],
                }
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def create_gamestate(
        self, username: str, turn: int, money: int, income: int, is_active: bool
    ) -> int | None:

        # establish connection with db
        try:
            with self.engine.begin() as conn:
                print("Connection established")
                result = conn.execute(
                    insert(gamestate)
                    .values(
                        username=username,
                        turn=turn,
                        money=money,
                        income=income,
                        is_active=is_active,
                    )
                    .returning(gamestate.c.user_id)
                )

                row = result.fetchone()
                if row is None:
                    return None
                return row[0]
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def update_gamestate(self, user_id: int, data: dict) -> int | None:

        for key in data:
            if key not in ALLOWED_FIELDS:
                raise FieldIsInvalidError

        # establish connection with db
        try:
            with self.engine.begin() as conn:
                print("Connection established")

                result = conn.execute(
                    update(gamestate).where(gamestate.c.user_id == user_id).values(data)
                )
                return result.rowcount
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError

    def delete_gamestate(self, user_id: int) -> int | None:

        # establish connection with db
        try:
            with self.engine.begin() as conn:
                print("Connection established")
                result = conn.execute(
                    delete(gamestate).where(gamestate.c.user_id == user_id)
                )

                return result.rowcount
        except (SQLAlchemyError, DBAPIError):
            raise DatabaseError
