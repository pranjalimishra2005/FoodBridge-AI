from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    JWT_SECRET: str
    JWT_ALGORITHM: str

    SECRET_KEY: str

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        extra="ignore"
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()