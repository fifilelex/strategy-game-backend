import os

import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_connection():
    conn_string = os.getenv("DATABASE_URL")
    conn = psycopg2.connect(conn_string)
    return conn


def init_db():

    try:
        with get_connection() as conn:
            print("Connection established")

            cur = conn.cursor()
            cur.execute(
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

            cur.execute(
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

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS ownership(
                user_id INT REFERENCES gamestate(uid),
                item_id INT REFERENCES items(id),
                PRIMARY KEY(user_id, item_id)
                );
            """
            )

    except Exception as e:
        print("Connection failed")
        print(e)
