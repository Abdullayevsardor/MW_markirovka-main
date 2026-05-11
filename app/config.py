from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

    # Railway uchun (agar mavjud bo‘lsa)
    DATABASE_URL: Optional[str] = None

    # Local fallback
    DB_USER: Optional[str] = None
    DB_PASSWORD: Optional[str] = None
    DB_HOST: Optional[str] = "localhost"
    DB_PORT: Optional[str] = "5432"
    DB_NAME: Optional[str] = None

    SECRET_KEY: str
    ADMIN_PASSWORD: str


    @property
    def database_url(self):
        # Railway bo‘lsa
        if self.DATABASE_URL:
            return self.DATABASE_URL.replace(
                "postgres://",
                "postgresql+psycopg://"
            )

        # Local bo‘lsa
        return (
            f"postgresql+psycopg://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


settings = Settings()
