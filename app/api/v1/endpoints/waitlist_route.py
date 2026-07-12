from functools import lru_cache

from fastapi import APIRouter

router = APIRouter()


@lru_cache(maxsize=1)
def get_waitlist_service():
    return None
