from functools import lru_cache

from fastapi import APIRouter

from app.db.db import async_session_maker
from app.services.waitlist.waitlist_service import WaitlistService

router = APIRouter()


@lru_cache(maxsize=1)
def get_waitlist_service():
    return WaitlistService(async_session_maker)
