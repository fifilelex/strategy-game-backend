from os import getenv

from dotenv import load_dotenv
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    create_engine,
)

load_dotenv()
url = getenv("DATABASE_URL")
assert url is not None
engine = create_engine(url)
metadata = MetaData()

gamestate = Table(
    "gamestate",
    metadata,
    Column("user_id", Integer, primary_key=True),
    Column("username", String(128), nullable=False),
    Column("turn", Integer, nullable=False),
    Column("money", Integer, nullable=False),
    Column("income", Integer, nullable=False),
    Column("is_active", Boolean, nullable=False),
)

items = Table(
    "items",
    metadata,
    Column("item_id", Integer, primary_key=True),
    Column("name", String(128), nullable=False),
    Column("income", Integer, nullable=False),
    Column("cost", Integer, nullable=False),
    Column("description", String(1024), nullable=False, default=""),
)

ownership = Table(
    "ownership",
    metadata,
    Column("user_id", Integer, ForeignKey("gamestate.user_id"), primary_key=True),
    Column("item_id", Integer, ForeignKey("items.item_id"), primary_key=True),
)
