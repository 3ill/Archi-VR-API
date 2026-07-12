import logging

from fastapi import HTTPException

from app.shared.service.email.dto.email_dto import SendWaitlistEmailDto
from app.shared.service.resend.dto.resend_dto import SendEmailDto
from app.shared.service.resend.resend_service import ResendService
from app.shared.templates.dto.template_dto import WaitlistTemplateDto
from app.shared.templates.template_provider import TemplateProvider


class EmailService:
    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._template_provider = TemplateProvider()
        self._resend_service = ResendService()

    async def send_waitlist_email(self, ctx: SendWaitlistEmailDto):
        html = self._template_provider.get_waitlist_template(
            WaitlistTemplateDto(first_name=ctx.first_name, url=ctx.url)
        )
        try:
            return await self._resend_service.send_email_with_html(
                SendEmailDto(email_to=ctx.email_to, subject=ctx.subject, html=html)
            )
        except HTTPException as e:
            self._logger.exception(
                "Error sending waitlist email",
                extra={
                    "email_to": ctx.email_to,
                    "url": ctx.url,
                    "subject": ctx.subject,
                },
            )
            raise e
        except Exception:
            self._logger.exception(
                "Unexpected error sending waitlist email",
                extra={
                    "email_to": ctx.email_to,
                    "url": ctx.url,
                    "subject": ctx.subject,
                },
            )
            raise HTTPException(
                status_code=500, detail="Unexpected error sending waitlist email"
            )
