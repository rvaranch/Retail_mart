import os
import pymysql
from dotenv import load_dotenv

load_dotenv(override=True)


def get_connection():
    """
    Creates and returns a MySQL database connection.
    Database details are taken from the .env file.
    """
    connection = pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Welcome123"),
        database=os.getenv("DB_NAME", "retail_mart_db"),
        port=int(os.getenv("DB_PORT", 3306)),
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection
