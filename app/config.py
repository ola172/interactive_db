from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, Field


class Settings(BaseSettings):
    # Database URL with type validation
    DATABASE_URL: PostgresDsn = Field(
        default="postgresql+psycopg2://postgres:postgres@localhost:5432/zedny_product",)
    STORAGE_URL: str
    STORAGE_KEY: str
    # Debug mode
    DEBUG: bool = Field(default=False)

    # Example for future expansion
    APP_NAME: str = Field(default="Zedny Product API")

    class Config:
        # Automatically read from .env file
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton settings object
settings = Settings()
