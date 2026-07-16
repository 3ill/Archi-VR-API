from abc import ABC, abstractmethod

from app.models.asset import Asset
from app.services.asset.dto.asset_dto import FetchAssetDto, UploadAssetDto


class BaseAssetProvider(ABC):
    @abstractmethod
    async def upload_asset(self, ctx: UploadAssetDto) -> Asset | None:
        pass

    @abstractmethod
    async def get_user_assets(self, ctx: FetchAssetDto) -> list[Asset] | None:
        pass
