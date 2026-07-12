import logging

from fastapi import HTTPException, status

from app.shared.service.resend.dto.resend_dto import EmailResponse, SendEmailDto
from app.shared.service.resend.provider.resend_provider import ResendProvider


class ResendService:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._provider = ResendProvider()
        self._resend = self._provider.instantiate_resend()

    async def send_email_with_html(self, ctx: SendEmailDto):
        try:
            result = self._resend.Emails.send(
                {
                    "from": ctx.email_from,
                    "to": [ctx.email_to],
                    "subject": ctx.subject,
                    "html": ctx.html,
                }
            )

            return EmailResponse(success=True, id=result["id"])
        except Exception:
            self._logger.exception("Error sending email")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to send email",
            )
