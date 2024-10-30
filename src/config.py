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
    DATABASE_URL: str = "sqlite:///:memory:"

    class Config:
        """
        Configuration for the Settings class.

        Attributes:
            env_file (str): The name of the environment file to load variables from.
        """
        env_file = f".development.env"


settings = Settings()
