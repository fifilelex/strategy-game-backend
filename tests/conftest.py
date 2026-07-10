import os

import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

from app.persistence.init_db import init_db

load_dotenv()
url = os.getenv("DATABASE_URL")
assert url is not None
test_engine = create_engine(url)


@pytest.fixture(autouse=True)
def reset_db():
    init_db(test_engine)
    with test_engine.begin() as conn:

        conn.execute(text("DELETE FROM ownership"))
        conn.execute(text("DELETE FROM items"))
        conn.execute(text("DELETE FROM gamestate"))
