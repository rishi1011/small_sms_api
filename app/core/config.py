from functools import lru_cache
from typing import Any, Optional

from pydantic import ConfigDict, PostgresDsn, ValidationInfo, field_validator

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

    model_config = ConfigDict(case_sensitive=True, env_file=".env")

    @classmethod
    def _build_postgres_dsn(cls, db_name: Optional[str], info: ValidationInfo) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql",
            username=info.data.get("DB_USER"),
            password=info.data.get("DB_PASSWORD"),
            host=info.data.get("DB_HOST"),
            path=db_name or "",
        )

    @field_validator("TEST_DB_URI", "SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        db_name_field = "TEST_DB_NAME" if info.field_name == "TEST_DB_URI" else "DB_NAME"
        return cls._build_postgres_dsn(info.data.get(db_name_field), info)


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
