from functools import lru_cache

from fastapi import APIRouter, Depends, status

from app.db.db import async_session_maker
from app.services.waitlist.dto.waitlist_dto import (
    AddToWaitlistDto,
    AddToWaitlistResponseDto,
)
from app.services.waitlist.waitlist_service import WaitlistService

router = APIRouter()


@lru_cache(maxsize=1)
def get_waitlist_service():
    return WaitlistService(async_session_maker)


@router.post(
    "",
    response_model=AddToWaitlistResponseDto,
    status_code=status.HTTP_201_CREATED,
    summary="Add a user to the waitlist",
    description=(
        "Adds a new user to the waitlist using their email, first name, and "
        "last name. Fails if the email already exists in the waitlist."
    ),
    responses={
        status.HTTP_201_CREATED: {
            "description": "User was successfully added to the waitlist.",
            "model": AddToWaitlistResponseDto,
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "The provided email already exists in the waitlist.",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already exists in waitlist"}
                }
            },
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": (
                "An unexpected error occurred while adding the user to the "
                "waitlist (e.g. database error or entry could not be created)."
            ),
            "content": {
                "application/json": {
                    "example": {"detail": "Error adding user to waitlist"}
                }
            },
        },
    },
)
async def add_user_to_waitlist(
    payload: AddToWaitlistDto,
    waitlist_service: WaitlistService = Depends(get_waitlist_service),
) -> AddToWaitlistResponseDto:
    return await waitlist_service.add_user_to_waitlist(payload)


@router.get(
    "/verify",
    response_model=bool,
    status_code=status.HTTP_200_OK,
    summary="Verify if an email is in the waitlist",
    description="Checks if a user's email already exists in the waitlist.",
    responses={
        status.HTTP_200_OK: {
            "description": "True if email exists, False otherwise.",
            "model": bool,
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "An error occurred while verifying the waitlist entry.",
            "content": {
                "application/json": {
                    "examples": {
                        "database_error": {
                            "summary": "Database/SQLAlchemy Error",
                            "value": {"detail": "Error verifying waitlist entry"},
                        },
                        "unexpected_error": {
                            "summary": "Unexpected Error",
                            "value": {"detail": "Unexpected error verifying waitlist entry"},
                        },
                    }
                }
            },
        },
    },
)
async def verify_waitlist_entry(
    email: str,
    waitlist_service: WaitlistService = Depends(get_waitlist_service),
) -> bool:
    return await waitlist_service.verify_waitlist_entry(email)

