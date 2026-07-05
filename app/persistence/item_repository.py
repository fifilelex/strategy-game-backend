from dotenv import load_dotenv

from app.persistence.init_db import get_connection

# Load environment variables from .env file
load_dotenv()


def create_item(name: str, income: int, cost: int, description: str):

    # establish connection with db
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(
                    """
                            INSERT INTO items(name, income, cost, description)
                            VALUES(%s, %s, %s, %s)
                            RETURNING id;       
                            """,
                    (name, income, cost, description),
                )
                # return ID of new item
                id = cur.fetchone()[0]  # type: ignore

                return id

    except Exception as e:
        print("Connection failed")
        print(e)


def read_items():

    # establish connection with db
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                # select all rows from items table
                cur.execute(
                    """
                            SELECT * FROM items;
                            """
                )
                rows = cur.fetchall()

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
        with get_connection() as conn:
            print("Connection established")

            # create cursor
            with conn.cursor() as cur:

                # get item with matching id
                cur.execute(
                    (
                        """
                            SELECT * FROM items
                            WHERE id =%s;
                            """
                    ),
                    [id],
                )
                row = cur.fetchone()

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
        with get_connection() as conn:
            print("Connection established")

            # create cursor
            with conn.cursor() as cur:
                # get item with matching name
                cur.execute(
                    (
                        """
                            SELECT * FROM items
                            WHERE name = %s;
                            """
                    ),
                    [name],
                )
                row = cur.fetchone()

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
    values = []

    for key, value in data.items():
        fields.append(f"{key} = %s")
        values.append(value)
    sql = "UPDATE items SET " + ", ".join(fields) + " WHERE id = %s;"

    values.append(id)

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


def delete_item(id: int):

    # establish connection with db
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(
                    (
                        """
                    DELETE FROM items
                    WHERE id = %s;
                    """
                    ),
                    [id],
                )
                rows_affected = cur.rowcount
                return rows_affected

    except Exception as e:
        print("Connection failed")
        print(e)

        return None


def read_ownerships(uid: int):
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(
                    (
                        """
                        SELECT * FROM ownership
                        WHERE user_id = %s;
                        """
                    ),
                    [uid],
                )
                rows = cur.fetchall()
                return [{"uid": row[0], "id": row[1]} for row in rows]
    except Exception as e:
        print("Connection failed")
        print(e)
        return None


def read_ownership(uid: int, id: int):
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(
                    (
                        """
                        SELECT * FROM ownership
                        WHERE user_id = %s AND item_id = %s;
                        """
                    ),
                    [uid, id],
                )
                row = cur.fetchone()

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
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(
                    (
                        """
                        INSERT INTO ownership(user_id, item_id)
                        VALUES(%s, %s)
                        RETURNING user_id, item_id
                        """
                    ),
                    (uid, id),
                )
                row = cur.fetchone()
            return {"uid": row[0], "id": row[1]} if row else None

    except Exception as e:
        print("Connection failed")
        print(e)

        return None


def delete_ownership(uid: int, id: int):
    # establish connection with db
    try:
        with get_connection() as conn:
            print("Connection established")
            # create cursor
            with conn.cursor() as cur:
                cur.execute(
                    (
                        """
                        DELETE FROM ownership
                        WHERE user_id = %s AND item_id = %s
                        """
                    ),
                    [uid, id],
                )
                rows_affected = cur.rowcount
                return rows_affected
    except Exception as e:

        print("Connection failed")
        print(e)

        return None
