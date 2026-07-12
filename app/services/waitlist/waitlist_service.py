import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.services.waitlist.dto.waitlist_dto import (
    AddToWaitlistData,
    AddToWaitlistDto,
    AddToWaitlistResponseDto,
)
from app.services.waitlist.provider.waitlist_provider import WaitlistProvider


class WaitlistService:
    def __init__(self, async_sessionmaker: async_sessionmaker) -> None:
        self._logger = logging.getLogger(__name__)
        self._provider = WaitlistProvider(async_sessionmaker)

    async def add_user_to_waitlist(self, ctx: AddToWaitlistDto):
        try:
            existing_email = await self._provider.get_waitlist_by_email(ctx.email)

            if existing_email:
                self._logger.error(
                    "Email already exists in waitlist", extra={"email": ctx.email}
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already exists in waitlist",
                )

            waitlist_entry = await self._provider.add_user_to_waitlist(ctx)

            if waitlist_entry is None:
                self._logger.error(
                    "Failed to add user to waitlist",
                    extra={
                        "first_name": ctx.first_name,
                        "last_name": ctx.last_name,
                        "email": ctx.email,
                    },
                )
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to add user to waitlist",
                )

            data = AddToWaitlistData(id=str(waitlist_entry.id))

            return AddToWaitlistResponseDto(
                status=status.HTTP_201_CREATED,
                message="User added to waitlist successfully",
                data=data,
            )

        except SQLAlchemyError as exc:
            self._logger.exception(
                "Error adding user to waitlist",
                extra={
                    "first_name": ctx.first_name,
                    "last_name": ctx.last_name,
                    "email": ctx.email,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error adding user to waitlist",
            )
        except HTTPException as exc:
            self._logger.exception(
                "HTTP error adding user to waitlist",
                extra={
                    "first_name": ctx.first_name,
                    "last_name": ctx.last_name,
                    "email": ctx.email,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc.detail),
                },
            )
            raise exc
        except Exception as exc:
            self._logger.exception(
                "Unexpected error adding user to waitlist",
                extra={
                    "first_name": ctx.first_name,
                    "last_name": ctx.last_name,
                    "email": ctx.email,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                },
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error adding user to waitlist",
            )
