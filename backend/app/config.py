"""App configuration, loaded from environment variables / .env.

Boilerplate - not core logic.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql+psycopg2://shelflife:shelflife@localhost:5432/shelflife"
    anthropic_api_key: str = ""
    upload_dir: str = "./uploads"
    expiring_soon_days: int = 3


settings = Settings()
