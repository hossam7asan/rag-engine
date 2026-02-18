from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    OPENAI_API_KEY: str

    FILE_ALLOWED_TYPES: list
    FILE_MAX_SIZE: int

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    return Settings()  # type: ignore[call-arg]
