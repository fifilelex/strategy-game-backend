from sqlalchemy import Engine

from app.persistence.tables import metadata


def initialize_db(engine: Engine) -> None:
    metadata.create_all(engine, checkfirst=True)
