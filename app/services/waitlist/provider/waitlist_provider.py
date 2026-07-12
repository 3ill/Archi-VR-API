import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.models.waitlist import Waitlist
from app.services.waitlist.dto.waitlist_dto import AddToWaitlistDto
from app.services.waitlist.provider.base import BaseWaitlistProvider


class WaitlistProvider(BaseWaitlistProvider):
    def __init__(self, async_sessionmaker: async_sessionmaker) -> None:
        self._sessionmaker = async_sessionmaker
        self._logger = logging.getLogger(__name__)
        super().__init__()

    async def add_user_to_waitlist(self, ctx: AddToWaitlistDto) -> Waitlist | None:
        async with self._sessionmaker() as session:
            waitlist = Waitlist(
                first_name=ctx.first_name, last_name=ctx.last_name, email=ctx.email
            )

            session.add(waitlist)
            await session.commit()
            await session.refresh(waitlist)

            return waitlist

    async def get_waitlist_by_email(self, email: str) -> Waitlist | None:
        async with self._sessionmaker() as session:
            stmt = select(Waitlist).where(Waitlist.email == email)
            result = await session.execute(stmt)
            waitlist = result.scalar_one_or_none()
            return waitlist

    async def get_waitlist(self) -> list[Waitlist]:
        async with self._sessionmaker() as session:
            stmt = select(Waitlist)
            result = await session.execute(stmt)
            waitlist = result.scalars().all()
            return waitlist
