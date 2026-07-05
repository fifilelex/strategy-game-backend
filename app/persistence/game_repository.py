from dotenv import load_dotenv

from app.persistence.init_db import get_connection

# Load environment variables from .env file
load_dotenv()


def read_gamestate(uid: int):

    # establish connection with db
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(
                    (
                        """
                SELECT * FROM gamestate
                WHERE uid = %s;
                """
                    ),
                    [uid],
                )
                # fetch single gamestate
                row = cur.fetchone()

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
        with get_connection() as conn:
            print("Connection established")

            # create cursor
            with conn.cursor() as cur:
                # get gamestate with matching username
                cur.execute(
                    """
                    SELECT * FROM gamestate
                    WHERE username = %s AND turn = %s;
                    """,
                    [name, turn],
                )
                row = cur.fetchone()

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
        with get_connection() as conn:
            print("Connection established")
            with conn.cursor() as cur:
                cur.execute(
                    """
                INSERT INTO gamestate(username, turn, money, income, is_active)
                VALUES(%s, %s, %s, %s, %s)
                RETURNING uid;
                """,
                    (username, turn, money, income, is_active),
                )
                uid = cur.fetchone()[0]  # type: ignore

                return uid
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def update_gamestate(uid: int, data: dict):

    # unpack dictionary data into two separate lists
    fields = []
    values = []

    for key, value in data.items():
        fields.append(f"{key} = %s")
        values.append(value)
    sql = "UPDATE gamestate SET " + ", ".join(fields) + " WHERE uid = %s;"

    values.append(uid)
    # establish connection with db
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(sql, values)
                rows_affected = cur.rowcount
                return rows_affected

    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def delete_gamestate(uid: int):

    # establish connection with db
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(("DELETE FROM gamestate WHERE uid = %s;"), [uid])
                rows_affected = cur.rowcount
                return rows_affected
    except Exception as e:
        print("Connection failed")
        print(e)
        return None
