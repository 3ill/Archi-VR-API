import asyncio
import logging
import os

import pytest

from app.shared.service.resend.dto.resend_dto import SendEmailDto
from app.shared.service.resend.resend_service import ResendService
from app.shared.templates.dto.template_dto import WaitlistTemplateDto
from app.shared.templates.template_provider import TemplateProvider

logger = logging.getLogger(__name__)


def _require_env_vars(*names: str) -> dict[str, str]:
    missing = [name for name in names if not os.getenv(name)]
    if missing:
        pytest.skip(f"Missing required env vars: {', '.join(missing)}")
    return {name: os.getenv(name, "") for name in names}


def test_send_email_with_html(monkeypatch):
    async def _test():
        env = _require_env_vars(
            "RESEND_API_KEY",
            "RESEND_FROM_EMAIL",
            "RESEND_TO_EMAIL",
        )

        monkeypatch.setenv("RESEND_API_KEY", env["RESEND_API_KEY"])

        service = ResendService()
        template_provider = TemplateProvider()

        html = template_provider.get_waitlist_template(
            ctx=WaitlistTemplateDto(first_name="chikezie", url="")
        )

        payload = SendEmailDto(
            email_from=env["RESEND_FROM_EMAIL"],
            email_to=env["RESEND_TO_EMAIL"],
            subject="Resend service HTML email test",
            html=html,
        )

        response = await service.send_email_with_html(payload)
        logger.info("Resend HTML email response: %s", response)
        print("Resend HTML email response:", response)

        assert response.success is True
        assert response.id

    asyncio.run(_test())
