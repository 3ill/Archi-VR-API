from pydantic import BaseModel, ConfigDict


class BaseWaitlistDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AddToWaitlistDto(BaseWaitlistDto):
    email: str
    first_name: str
    last_name: str
