import logging
from enum import Enum
from typing import Optional
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from pydantic import Field
from pydantic_settings import BaseSettings

# Query params accepted by libpq/psycopg (e.g. sslmode, channel_binding) but not
# understood by asyncpg's connect(), which raises TypeError if they're passed
# through as connection kwargs. Strip them from the URL and translate them to
# asyncpg's own `ssl` connect arg instead.
_UNSUPPORTED_ASYNCPG_PARAMS = {"sslmode", "channel_binding"}


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
    _connect_args: dict = {}

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

        self._db_url = self._normalize_db_url(self._db_url)
        return self._db_url

    def _normalize_db_url(self, db_url: str) -> str:
        """Strip trailing junk, force the asyncpg driver, and move any
        libpq-only query params (sslmode, channel_binding) into connect_args,
        since asyncpg's connect() rejects unknown keyword arguments."""
        db_url = db_url.strip().strip("'\"")

        parts = urlsplit(db_url)
        scheme = parts.scheme
        if scheme in ("postgres", "postgresql"):
            scheme = "postgresql+asyncpg"

        query_pairs = parse_qsl(parts.query, keep_blank_values=True)
        kept_pairs = []
        for key, value in query_pairs:
            if key.lower() == "sslmode":
                self._connect_args["ssl"] = value.lower() not in ("disable", "allow")
            elif key.lower() in _UNSUPPORTED_ASYNCPG_PARAMS:
                continue
            else:
                kept_pairs.append((key, value))

        new_query = urlencode(kept_pairs)
        return urlunsplit((scheme, parts.netloc, parts.path, new_query, parts.fragment))

    def get_connect_args(self) -> dict:
        self.get_db_url()
        return self._connect_args
