import os
from typing import Optional

import psycopg2
from psycopg2.extensions import connection


# Simple PostgreSQL connection setup for the project.
# We read values from environment variables so credentials are not hardcoded.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pharmafind")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")


def get_db_connection() -> Optional[connection]:
    """
    Create and return a PostgreSQL connection.
    Returns None if connection fails.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        return conn
    except Exception as error:
        print(f"Database connection error: {error}")
        return None
