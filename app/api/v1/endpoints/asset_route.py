from functools import lru_cache

from fastapi import APIRouter, Depends, status

from app.db.db import async_session_maker
from app.services.asset.asset_service import AssetService
from app.services.asset.dto.asset_dto import (
    FetchAssetDto,
    FetchAssetResponseDto,
    UploadAssetDto,
    UploadAssetResponseDto,
)

router = APIRouter()


@lru_cache(maxsize=1)
def get_asset_service():
    return AssetService(async_session_maker)


@router.post(
    "",
    response_model=UploadAssetResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Upload an asset",
    description="Uploads a new asset with a name, URL, and associated user email.",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Asset uploaded successfully.",
            "model": UploadAssetResponseDto,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "An error occurred while uploading the asset.",
            "content": {
                "application/json": {
                    "examples": {
                        "upload_failed": {
                            "summary": "Upload Failed",
                            "value": {"detail": "Failed to upload asset"},
                        },
                        "database_error": {
                            "summary": "Database Error",
                            "value": {
                                "detail": "An error occurred while uploading the asset. Please try again later."
                            },
                        },
                        "unexpected_error": {
                            "summary": "Unexpected Error",
                            "value": {
                                "detail": "An unexpected error occurred while uploading the asset. Please try again later."
                            },
                        },
                    }
                }
            },
        },
    },
)
async def upload_asset(
    payload: UploadAssetDto,
    asset_service: AssetService = Depends(get_asset_service),
) -> UploadAssetResponseDto:
    return await asset_service.upload_asset(payload)


@router.get(
    "",
    response_model=FetchAssetResponseDto,
    status_code=status.HTTP_200_OK,
    summary="Get user assets",
    description="Fetches all assets associated with the user's email.",
    responses={
        status.HTTP_200_OK: {
            "description": "User assets fetched successfully.",
            "model": FetchAssetResponseDto,
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "No assets found for the user.",
            "model": FetchAssetResponseDto,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "An error occurred while fetching user assets.",
            "content": {
                "application/json": {
                    "examples": {
                        "database_error": {
                            "summary": "Database Error",
                            "value": {
                                "detail": "An error occurred while fetching user assets. Please try again later."
                            },
                        },
                        "unexpected_error": {
                            "summary": "Unexpected Error",
                            "value": {
                                "detail": "An unexpected error occurred while fetching user assets. Please try again later."
                            },
                        },
                    }
                }
            },
        },
    },
)
async def get_user_assets(
    email: str,
    asset_service: AssetService = Depends(get_asset_service),
) -> FetchAssetResponseDto:
    return await asset_service.get_user_assets(FetchAssetDto(email=email))
