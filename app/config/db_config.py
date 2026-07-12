import logging
from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class ENV(str, Enum):
    PROD = "PROD"
    STAGING = "STAGING"
    LOCAL = "LOCAL"


class DBConfig(BaseSettings):
    NODE_ENV: Optional[ENV] = ENV.LOCAL
    POSTGRES_DB_LOCAL_URL: Optional[str] = None
    POSTGRES_DB_PROD_URL: Optional[str] = None
    POSTGRES_DB_STAGING_URL: Optional[str] = None
    POSTGRES_USER: Optional[str] = "postgres"
    POSTGRES_HOST: Optional[str] = "localhost"
    POSTGRES_PORT: Optional[str] = "5432"
    POSTGRES_DB: Optional[str] = "pnocDB"
    POSTGRES_PASSWORD: Optional[str] = "postgres"

    logger: logging.Logger = Field(default_factory=lambda: logging.getLogger(__name__))
    _db_url: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

    def get_docker_postgres(self):
        self._db_url = (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
        return self._db_url

    def get_db_url(self):
        if self._db_url:
            return self._db_url

        env = self.NODE_ENV
        if env == ENV.PROD.value:
            self._db_url = self.POSTGRES_DB_PROD_URL
        elif env == ENV.STAGING.value:
            self._db_url = self.POSTGRES_DB_STAGING_URL
        else:
            self._db_url = self.POSTGRES_DB_LOCAL_URL

        if not self._db_url:
            self.logger.warning(
                "No database URL found for environment",
                extra={
                    "environment": env,
                },
            )
            raise ValueError(f"No database URL found for environment: {env}")

        return self._db_url
