from pydantic import BaseModel, ConfigDict


class BaseAssetDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class UploadAssetDto(BaseAssetDto):
    name: str
    url: str
    email: str


class FetchAssetDto(BaseAssetDto):
    email: str
