from typing import Any, Callable

from pydantic import BaseModel, ConfigDict


class EventSubscribeDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    event_name: str
    listener: Callable[..., Any]


class PublishEventDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    event_name: str
    payload: Any


class SuccessResponseDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    status: int
    message: str
    data: Any
