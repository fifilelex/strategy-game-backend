import pytest

from app.persistence.init_db import get_connection


@pytest.fixture(autouse=True)
def reset_db():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM ownership;")
    cur.execute("DELETE FROM items;")
    cur.execute("DELETE FROM gamestate;")

    conn.commit()
    conn.close()
