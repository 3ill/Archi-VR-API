from pydantic import BaseModel, ConfigDict


class BaseTemplateDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class WelcomeTemplateDto(BaseTemplateDto):
    first_name: str
    url: str
