from dotenv import load_dotenv

from app.domain.exceptions import FieldIsInvalid
from app.persistence.init_db import engine, text

# Load environment variables from .env file
load_dotenv()
ALLOWED_KEY = {"name", "cost", "income", "description"}


def create_item(name: str, income: int, cost: int, description: str):

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(
                text(
                    """
                            INSERT INTO items(name, income, cost, description)
                            VALUES(:name, :income, :cost, :description)
                            RETURNING id;       
                            """
                ),
                {
                    "name": name,
                    "income": income,
                    "cost": cost,
                    "description": description,
                },
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
            result = conn.execute(
                text(
                    """
                            SELECT * FROM items;
                            """
                )
            )
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
            result = conn.execute(
                text(
                    """
                            SELECT * FROM items
                            WHERE id =:id;
                            """
                ),
                {"id": id},
            )
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
            result = conn.execute(
                text(
                    """
                            SELECT * FROM items
                            WHERE name = :name;
                            """
                ),
                {"name": name},
            )

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

    # unpack dictionary data into two separate lists
    fields = []
    params = {"id": id}

    for key, value in data.items():
        if key not in ALLOWED_KEY:
            raise FieldIsInvalid
        fields.append(f"{key} = :{key}")
        params[key] = value

    query = text(f"UPDATE items SET {','.join(fields)} WHERE id = :id")

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


def delete_item(id: int):

    # establish connection with db
    try:
        with engine.begin() as conn:
            print("Connection established")
            result = conn.execute(
                text(
                    """
                    DELETE FROM items
                    WHERE id = :id;
                    """
                ),
                {"id": id},
            )
            return result.rowcount

    except Exception as e:
        print("Connection failed")
        print(e)

        return None


def read_ownerships(uid: int):
    try:
        with engine.connect() as conn:
            print("Connection established")
            result = conn.execute(
                text(
                    """
                        SELECT * FROM ownership
                        WHERE user_id = :uid;
                        """
                ),
                {"uid": uid},
            )

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
                text(
                    """
                        SELECT * FROM ownership
                        WHERE user_id = :uid AND item_id = :id;
                        """
                ),
                {"uid": uid, "id": id},
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
                text(
                    """
                        INSERT INTO ownership(user_id, item_id)
                        VALUES(:uid, :id)
                        RETURNING user_id, item_id
                        """
                ),
                {"uid": uid, "id": id},
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
                text(
                    """
                        DELETE FROM ownership
                        WHERE user_id = :uid AND item_id = :id
                        """
                ),
                {"uid": uid, "id": id},
            )
            rows_affected = result.rowcount
            return rows_affected
    except Exception as e:

        print("Connection failed")
        print(e)

        return None
