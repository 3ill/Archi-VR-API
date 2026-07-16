from pydantic import BaseModel, ConfigDict

from app.shared.dto.shared_dto import SuccessResponseDto


class BaseAssetDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class UploadAssetDto(BaseAssetDto):
    name: str
    url: str
    email: str


class FetchAssetDto(BaseAssetDto):
    email: str


class UploadAssetResponseDto(SuccessResponseDto):
    data: UploadAssetDto


class AssetData(BaseAssetDto):
    name: str
    url: str


class FetchAssetResponseDto(SuccessResponseDto):
    data: list[AssetData]
