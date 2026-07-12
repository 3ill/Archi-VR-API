from pydantic_settings import BaseSettings


class ApiKeyConfig(BaseSettings):
    APP_API_KEY: str | None = None
    APP_API_KEY_HEADER_NAME: str = "x-api-key"

    class Config:
        env_file = ".env"
        extra = "ignore"

    def get_api_key(self) -> str:
        if not self.APP_API_KEY:
            raise ValueError("APP_API_KEY is required")

        return self.APP_API_KEY
