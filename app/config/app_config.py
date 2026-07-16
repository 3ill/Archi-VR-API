from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    APP_UPLOAD_URL: str = "https://archivr-visualizer.vercel.app/upload"
