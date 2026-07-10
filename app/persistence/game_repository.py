from dotenv import load_dotenv

from app.domain.exceptions import DatabaseError, FieldIsInvalid
from app.persistence.init_db import engine, text

# Load environment variables from .env file
load_dotenv()

ALLOWED_FIELDS = {"username", "turn", "money", "income", "is_active"}


def read_gamestate(uid: int):

    # establish connection with db
    try:
        with engine.connect() as conn:
            print("Connection established")

            result = conn.execute(
                text(
                    """
                SELECT * FROM gamestate
                WHERE uid = :uid;
                """
                ),
                {"uid": uid},
            )

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
                text(
                    """
                    SELECT * FROM gamestate
                    WHERE username = :username AND turn = :turn;
                    """
                ),
                {"username": name, "turn": turn},
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
                text(
                    """
                INSERT INTO gamestate(username, turn, money, income, is_active)
                VALUES(:username, :turn, :money, :income, :is_active)
                RETURNING uid;
                """
                ),
                {
                    "username": username,
                    "turn": turn,
                    "money": money,
                    "income": income,
                    "is_active": is_active,
                },
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

    # unpack dictionary data into two separate lists
    fields = []
    params = {"uid": uid}

    for key, value in data.items():
        if key not in ALLOWED_FIELDS:
            raise FieldIsInvalid
        fields.append(f"{key} = :{key}")
        params[key] = value
    query = text(
        f"""UPDATE gamestate
                SET {", ".join(fields)}
                WHERE uid = :uid"""
    )

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")

            result = conn.execute(query, params)
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
            result = conn.execute(
                text("DELETE FROM gamestate WHERE uid = :uid;"), {"uid": uid}
            )
            return result.rowcount
    except Exception as e:
        print("Connection failed")
        print(e)
        return None
