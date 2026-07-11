from dotenv import load_dotenv
from sqlalchemy import and_, delete, insert, select, update

from app.domain.exceptions import FieldIsInvalid
from app.persistence.tables import engine, items, ownership

# Load environment variables from .env file
load_dotenv()
ALLOWED_KEY = {"name", "cost", "income", "description"}


def create_item(name: str, income: int, cost: int, description: str):

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(
                insert(items)
                .values(name=name, income=income, cost=cost, description=description)
                .returning(items.c.id)
            )

            row = result.fetchone()
            if row is None:
                return None
        return row.id

    except Exception as e:
        print("Connection failed")
        print(e)


def read_items():

    # establish connection with db
    try:
        with engine.connect() as conn:
            print("Connection established")

            # select all rows from items table
            result = conn.execute(select(items))
            rows = result.fetchall()

            # present every item as a dictionary
            return [
                {
                    "id": r[0],
                    "name": r[1],
                    "income": r[2],
                    "cost": r[3],
                    "description": r[4],
                }
                for r in rows
            ]
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def read_item(id: int):

    # establish connection with db
    try:
        with engine.connect() as conn:
            print("Connection established")

            # get item with matching id
            result = conn.execute(select(items).where(items.c.id == id))

            row = result.fetchone()

            if row is None:  # item not found -> return None
                return None

            # present item as a dictionary
            return {
                "id": row[0],
                "name": row[1],
                "income": row[2],
                "cost": row[3],
                "description": row[4],
            }
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def search_item_by_name(name: str):

    # establish connection with db
    try:
        with engine.connect() as conn:
            print("Connection established")

            # get item with matching name
            result = conn.execute(select(items).where(items.c.name == name))

        row = result.fetchone()

        if row is None:
            return None
            # present item as a dictionary
        return {
            "id": row[0],
            "name": row[1],
            "income": row[2],
            "cost": row[3],
            "description": row[4],
        }
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def update_item(id: int, data: dict):

    for key in data.keys():
        if key not in ALLOWED_KEY:
            raise FieldIsInvalid

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(update(items).values(data).where(items.c.id == id))
            return result.rowcount

    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def delete_item(id: int):

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(delete(items).where(items.c.id == id))

            return result.rowcount

    except Exception as e:
        print("Connection failed")
        print(e)

        return None


def read_ownerships(uid: int):
    try:
        with engine.connect() as conn:
            print("Connection established")
            result = conn.execute(select(ownership).where(ownership.c.user_id == uid))

            rows = result.fetchall()
            return [{"uid": row[0], "id": row[1]} for row in rows]
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def read_ownership(uid: int, id: int):
    try:
        with engine.connect() as conn:
            print("Connection established")
            result = conn.execute(
                select(ownership).where(
                    and_(ownership.c.user_id == uid, ownership.c.item_id == id)
                )
            )

            row = result.fetchone()

            if row is None:  # ownership not found -> return None
                return None

            return {"uid": row[0], "id": row[1]}
    except Exception as e:
        print("Connection failed!")
        print(e)
        return None


def create_ownership(uid: int, id: int):

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(
                insert(ownership)
                .values(user_id=uid, item_id=id)
                .returning(ownership.c.user_id, ownership.c.item_id)
            )

            row = result.fetchone()
        return {"uid": row[0], "id": row[1]} if row else None

    except Exception as e:
        print("Connection failed")
        print(e)

        return None


def delete_ownership(uid: int, id: int):
    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(
                delete(ownership).where(
                    and_(ownership.c.user_id == uid, ownership.c.item_id == id)
                )
            )

            rows_affected = result.rowcount
            return rows_affected
    except Exception as e:

        print("Connection failed")
        print(e)

        return None
