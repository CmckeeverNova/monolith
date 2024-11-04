from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env files.

    Attributes:
        ENV (str): The current environment, e.g., "development" or "production".
        DATABASE_URL (str): The URL used to connect to the database.

    The settings are primarily loaded from a `.env` file (by default `.development.env`),
    but can also be overridden by actual environment variables.
    """

    ENV: str = "development"
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5434/notebook"

    model_config = ConfigDict(env_file=".development.env")


settings = Settings()
