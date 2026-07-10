import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env file
load_dotenv()
url = os.getenv("DATABASE_URL")
assert url is not None
engine = create_engine(url)


def init_db(engine):

    try:
        with engine.begin() as conn:
            print("Connection established")

            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS gamestate(
                uid SERIAL PRIMARY KEY,
                username VARCHAR(128) NOT NULL,
                turn INT NOT NULL,                        
                money INT NOT NULL,            
                income INT NOT NULL,
                is_active BOOLEAN NOT NULL
                        );
                

            """
                )
            )

            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS items(
                id SERIAL PRIMARY KEY,
                name VARCHAR(128) NOT NULL,
                income INT NOT NULL,
                cost INT NOT NULL,
                description VARCHAR(1024) NOT NULL DEFAULT('')
                );
            """
                )
            )

            conn.execute(
                text(
                    """
                CREATE TABLE IF NOT EXISTS ownership(
                user_id INT REFERENCES gamestate(uid),
                item_id INT REFERENCES items(id),
                PRIMARY KEY(user_id, item_id)
                );
            """
                )
            )

    except Exception as e:
        print("Connection failed")
        print(e)
