import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.services.asset.dto.asset_dto import (
    AssetData,
    FetchAssetDto,
    FetchAssetResponseDto,
    UploadAssetDto,
    UploadAssetResponseDto,
)
from app.services.asset.provider.asset_provider import AssetProvider


class AssetService:
    def __init__(self, async_sessionmaker: async_sessionmaker) -> None:
        self._provider = AssetProvider(async_sessionmaker)
        self._logger = logging.getLogger(__name__)

    async def upload_asset(self, ctx: UploadAssetDto):
        try:
            asset = await self._provider.upload_asset(ctx)

            if asset is None:
                self._logger.error(
                    "Failed to upload asset",
                    extra={
                        "name": ctx.name,
                        "url": ctx.url,
                        "email": ctx.email,
                    },
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to upload asset",
                )

            return UploadAssetResponseDto(
                status=status.HTTP_201_CREATED,
                message="Asset uploaded successfully",
                data=ctx,
            )
        except SQLAlchemyError as exc:
            self._logger.exception(
                "Database error occurred while uploading asset",
                extra={
                    "ctx": ctx.model_dump(),
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while uploading the asset. Please try again later.",
            )
        except HTTPException as exc:
            self._logger.exception(
                "HTTP error occurred while uploading asset",
                extra={
                    "ctx": ctx.model_dump(),
                    "error_type": type(exc).__name__,
                    "error_message": str(exc.detail),
                },
            )
            raise exc
        except Exception as exc:
            self._logger.exception(
                "Unexpected error occurred while uploading asset",
                extra={
                    "ctx": ctx.model_dump(),
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while uploading the asset. Please try again later.",
            )

    async def get_user_assets(self, ctx: FetchAssetDto):
        try:
            assets = await self._provider.get_user_assets(ctx)

            if assets is None:
                self._logger.info(
                    "No assets found for user",
                    extra={"email": ctx.email},
                )
                return FetchAssetResponseDto(
                    status=status.HTTP_404_NOT_FOUND,
                    message="No assets found for the user",
                    data=[],
                )

            return FetchAssetResponseDto(
                status=status.HTTP_200_OK,
                message="User assets fetched successfully",
                data=[
                    AssetData(name=str(data.name), url=str(data.url)) for data in assets
                ],
            )
        except SQLAlchemyError as exc:
            self._logger.exception(
                "Database error occurred while fetching user assets",
                extra={
                    "email": ctx.email,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while fetching user assets. Please try again later.",
            )
        except HTTPException as exc:
            self._logger.exception(
                "HTTP error occurred while fetching user assets",
                extra={
                    "email": ctx.email,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc.detail),
                },
            )
            raise exc
        except Exception as exc:
            self._logger.exception(
                "Unexpected error occurred while fetching user assets",
                extra={
                    "email": ctx.email,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while fetching user assets. Please try again later.",
            )
