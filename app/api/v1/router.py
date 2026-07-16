from fastapi import APIRouter

from app.api.v1.endpoints import asset_route, waitlist_route

api_router = APIRouter()


api_router.include_router(waitlist_route.router, prefix="/waitlist", tags=["waitlist"])
api_router.include_router(asset_route.router, prefix="/asset", tags=["asset"])
