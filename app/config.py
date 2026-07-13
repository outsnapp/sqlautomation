import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME")
    DATABASE_URL = os.getenv("DATABASE_URL")


settings = Settings()