from typing import Optional

from pydantic_settings.main import BaseSettings


class ResendConfig(BaseSettings):
    RESEND_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        extra = "ignore"

    def get_api_key(self):
        if not self.RESEND_API_KEY:
            raise ValueError("RESEND_API_KEY is required")

        return self.RESEND_API_KEY
