import resend

from app.config.resend_config import ResendConfig


class ResendProvider:
    def __init__(self) -> None:
        self._config = ResendConfig()
        self.api_key = self._config.get_api_key()

    def instantiate_resend(self):
        resend.api_key = self.api_key
        return resend
