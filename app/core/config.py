from functools import lru_cache
from typing import (
    Any,
    Dict,
    Optional,
)
from pydantic import PostgresDsn, field_validator, ConfigDict, ValidationInfo

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI School Management System"
    API_V1_STR: str = "/api/v1"

    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    TEST_DB_NAME: str

    TEST_DB_URI: Optional[PostgresDsn] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    model_config = ConfigDict(case_sensitive=True, env_file = ".env")

    @field_validator("TEST_DB_URI", mode="before")
    @classmethod
    def assemble_test_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("DB_USER"),
            password=info.data.get("DB_PASSWORD"),
            host=info.data.get("DB_HOST"),
            path=info.data.get("TEST_DB_NAME") or "",
        )

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("DB_USER"),
            password=info.data.get("DB_PASSWORD"),
            host=info.data.get("DB_HOST"),
            path=info.data.get("DB_NAME") or "",
        )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
