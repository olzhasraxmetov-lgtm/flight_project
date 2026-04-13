from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    MODE: Literal["TEST", "LOCAL", "DEV", "PROD"]

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    DATABASE_URL: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    YOOKASSA_SHOP_ID: str
    YOOKASSA_API_SECRET_KEY: str
    YOOKASSA_RETURN_URL: str

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    APP_NAME: str = 'Flight API Project'
    APP_DESCRIPTION: str = 'Flight API Project'
    APP_VERSION: str = '0.0.1'

    @property
    def REDIS_URL(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    model_config = SettingsConfigDict(
        env_file='.env',
        extra='ignore',
        env_file_encoding='utf-8',
    )

settings = Settings()