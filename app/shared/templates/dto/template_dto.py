from pydantic import BaseModel, ConfigDict


class BaseTemplateDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class WaitlistTemplateDto(BaseTemplateDto):
    first_name: str
    url: str
