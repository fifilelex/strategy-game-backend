from os import getenv

from dotenv import load_dotenv

load_dotenv()


def get_production_db_url() -> str:
    url = getenv("DATABASE_URL")
    if url is None:
        raise ValueError
    return url
