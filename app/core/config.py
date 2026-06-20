from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    SECRET_KEY: str = "change-me-in-production"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    # Database (Postgres via SQLAlchemy)
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/honeybook_ai"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["*"]

    # Zapier webhook secret (optional but recommended)
    ZAPIER_WEBHOOK_SECRET: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
