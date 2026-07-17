from app.persistence.tables import metadata


def initialize_db(engine):
    metadata.create_all(engine, checkfirst=True)
