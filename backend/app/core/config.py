from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent 

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )

    SECRET_KEY: str = ""
    ACCESS_TOKEN_TTL_MINUTES: int = 0
    REFRESH_TOKEN_TTL_DAYS: int = 0
    SQLALCHEMY_DATABASE_URI: str = f"sqlite:///{BASE_DIR}/database.db"

settings = Settings()    