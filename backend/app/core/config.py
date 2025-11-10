from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, field_validator


class Settings(BaseSettings):
    PROJECT_NAME: str = "Repositorio Comercial"
    API_V1_STR: str = "/api"

    # AGORA: default é sqlite local
    DATABASE_URL: str = "sqlite:///./app.db"

    API_DEBUG: bool = True
    API_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("API_CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
