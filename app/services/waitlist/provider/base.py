from abc import ABC, abstractmethod

from app.models.waitlist import Waitlist
from app.services.waitlist.dto.waitlist_dto import AddToWaitlistDto


class BaseWaitlistProvider(ABC):
    @abstractmethod
    async def add_user_to_waitlist(self, ctx: AddToWaitlistDto) -> Waitlist | None:
        pass

    @abstractmethod
    async def get_waitlist(self) -> list[Waitlist]:
        pass

    @abstractmethod
    async def get_waitlist_by_email(self, email: str) -> Waitlist | None:
        pass
