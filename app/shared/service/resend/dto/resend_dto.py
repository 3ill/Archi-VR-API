from pydantic import BaseModel, ConfigDict


class BaseResendDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class SendEmailDto(BaseResendDto):
    email_from: str = "athanasius@polarbearxr.com"
    email_to: str
    subject: str
    html: str


class EmailResponse(BaseModel):
    success: bool
    id: str
