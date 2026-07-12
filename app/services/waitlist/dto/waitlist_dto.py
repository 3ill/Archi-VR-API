from pydantic import BaseModel, ConfigDict

from app.shared.dto.shared_dto import SuccessResponseDto


class BaseWaitlistDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AddToWaitlistDto(BaseWaitlistDto):
    email: str
    first_name: str
    last_name: str


class AddToWaitlistData(BaseWaitlistDto):
    id: str


class AddToWaitlistResponseDto(SuccessResponseDto):
    data: AddToWaitlistData
