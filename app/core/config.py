from typing import Annotated, Optional
from fastapi import Depends
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    FIRE_BASE_KEY: str
    APY_KEY: str
    AUTH_DOMAIN: str
    PROJECT_ID: str
    STORAGE_BUCKET: str
    MESSAGING_SENDER_ID: str
    APP_ID: str
    MEASUREMENT_ID: str
    DATABASE_URL: Optional[str] = None

    CLOUDINARY_CLOUD_NAME: str
    CLOUDINARY_API_KEY: str
    CLOUDINARY_API_SECRET: str

    def to_dict(self) -> dict:
        return self.model_dump(exclude={"FIRE_BASE_KEY", "DATABASE_URL"})

    class Config:
        env_file = [".env"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDepends = Annotated[Settings, Depends(get_settings)]
