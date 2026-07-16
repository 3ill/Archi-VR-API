from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    APP_UPLOAD_URL: str = "https://archivr-visualizer.vercel.app/upload"
    INSTAGRAM_URL: str = "https://www.instagram.com/polarbear_xr"
    LINKEDIN_URL: str = "https://www.linkedin.com/company/polar-bear-vr/"
