from pydantic import BaseModel, ConfigDict


class BaseEmailDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class SendWaitlistEmailDto(BaseEmailDto):
    email_to: str
    first_name: str
    subject: str = "You're on the waitlist!"
    url: str
