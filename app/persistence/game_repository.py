from dotenv import load_dotenv
from sqlalchemy import and_, delete, insert, select, update

from app.domain.exceptions import DatabaseError, FieldIsInvalid
from app.persistence.tables import engine, gamestate

# Load environment variables from .env file
load_dotenv()

ALLOWED_FIELDS = {"username", "turn", "money", "income", "is_active"}


def read_gamestate(uid: int):

    # establish connection with db
    try:
        with engine.connect() as conn:
            print("Connection established")
            result = conn.execute(select(gamestate).where(gamestate.c.uid == uid))

            for row in result:

                if row is None:
                    return None

            return {
                "uid": row[0],
                "username": row[1],
                "turn": row[2],
                "money": row[3],
                "income": row[4],
                "is_active": row[5],
            }
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def search_gamestate_by_name(name: str, turn: int):

    # establish connection with db
    try:
        with engine.connect() as conn:
            print("Connection established")
            result = conn.execute(
                select(gamestate).where(
                    and_(gamestate.c.name == name, gamestate.c.turn == turn)
                )
            )

            for row in result:

                if row is None:
                    return None
            # present gamestate as a dictionary
            return {
                "uid": row[0],
                "username": row[1],
                "turn": row[2],
                "money": row[3],
                "income": row[4],
                "is_active": row[5],
            }
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def create_gamestate(
    username: str, turn: int, money: int, income: int, is_active: bool
):

    # establish connection with db
    try:
        with engine.begin() as conn:
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
                .returning(gamestate.c.uid)
            )

            row = result.fetchone()
            if row is None:
                raise DatabaseError
            return row[0]
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def update_gamestate(uid: int, data: dict):

    for key in data.keys():
        if key not in ALLOWED_FIELDS:
            raise FieldIsInvalid

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")

            result = conn.execute(
                update(gamestate).where(gamestate.c.uid == uid).values(data)
            )
            return result.rowcount
    except Exception as e:
        print("Connection failed")
        print(e)
    return None


def delete_gamestate(uid: int):

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(delete(gamestate).where(gamestate.c.uid == uid))

            return result.rowcount
    except Exception as e:
        print("Connection failed")
        print(e)
        return None
