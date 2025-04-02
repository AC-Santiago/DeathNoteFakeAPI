from typing import Annotated
from fastapi import Depends
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USERNAME: str
    DB_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    def to_dict(self) -> dict:
        return self.model_dump(exclude={"DB_PASSWORD", "SECRET_KEY"})

    class Config:
        env_file = [".env"]


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDepends = Annotated[Settings, Depends(get_settings)]
