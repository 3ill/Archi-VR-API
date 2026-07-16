import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.asset import Asset
from app.services.asset.dto.asset_dto import FetchAssetDto, UploadAssetDto
from app.services.asset.provider.base import BaseAssetProvider


class AssetProvider(BaseAssetProvider):
    def __init__(self, async_sessionmaker: async_sessionmaker) -> None:
        self._session_maker = async_sessionmaker
        self._logger = logging.getLogger(__name__)
        super().__init__()

    async def upload_asset(self, ctx: UploadAssetDto) -> Asset | None:
        async with self._session_maker() as session:
            asset = Asset(name=ctx.name, url=ctx.url, email=ctx.email)

            session.add(asset)
            await session.commit()
            await session.refresh(asset)

            return asset

    async def get_user_assets(self, ctx: FetchAssetDto) -> list[Asset] | None:
        async with self._session_maker() as session:
            stmt = select(Asset).where(Asset.email == ctx.email)
            result = await session.execute(stmt)
            assets = result.scalars().all()

            if not assets:
                self._logger.warning(
                    "No assets found for user",
                    extra={"email": ctx.email},
                )
                return None

            return assets
