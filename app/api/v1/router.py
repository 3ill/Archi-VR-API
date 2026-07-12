from fastapi import APIRouter

from app.api.v1.endpoints import waitlist_route

api_router = APIRouter()


api_router.include_router(waitlist_route.router, prefix="/waitlist", tags=["waitlist"])
