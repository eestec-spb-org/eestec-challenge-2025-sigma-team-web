# app/core/config.py
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "your_default_secret_key"  # Лучше хранить в .env
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_PATH: Path = Path("./data/users.db")  # Изменено с DATABASE_URL на DATABASE_PATH

    class Config:
        env_file = ".env"


settings = Settings()
