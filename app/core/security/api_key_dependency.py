import logging
import secrets
from functools import lru_cache
from typing import Annotated

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import Field

from app.config.api_key_config import ApiKeyConfig

logger: logging.Logger = Field(default_factory=lambda: logging.getLogger(__name__))
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


@lru_cache(maxsize=1)
def get_api_key_config() -> ApiKeyConfig:
    return ApiKeyConfig()


def verify_api_key(
    api_key: Annotated[str | None, Security(api_key_header)],
) -> None:
    expected_key = get_api_key_config().get_api_key()
    if not api_key or not secrets.compare_digest(api_key, expected_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
