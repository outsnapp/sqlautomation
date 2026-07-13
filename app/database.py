from langchain_community.utilities import SQLDatabase

from app.config import settings


def get_database() -> SQLDatabase:
    database = SQLDatabase.from_uri(
        settings.DATABASE_URL
    )

    return database


db = get_database()