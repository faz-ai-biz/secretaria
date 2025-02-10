from pydantic_settings import BaseSettings
from functools import lru_cache
from urllib.parse import quote_plus
import os
from typing import List
import json

class Settings(BaseSettings):
    # Database settings
    DB_NAME: str = "agente"
    DB_USER: str = "teste"
    DB_PASSWORD: str = "teste"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_RECYCLE: int = 3600

    # API settings
    API_VERSION: str = "1.0.0"
    API_TITLE: str = "API de Clientes"
    API_DESCRIPTION: str = "API para gerenciamento de clientes"
    API_PREFIX: str = "/api"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Secretaria API"

    # Security
    SECRET_KEY: str = "chave-secreta-muito-segura-123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_METHODS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # Google Calendar
    GOOGLE_CALENDAR_CLIENT_ID: str = os.getenv("GOOGLE_CALENDAR_CLIENT_ID", "")
    GOOGLE_CALENDAR_CLIENT_SECRET: str = os.getenv("GOOGLE_CALENDAR_CLIENT_SECRET", "")
    GOOGLE_CALENDAR_REDIRECT_URI: str = os.getenv(
        "GOOGLE_CALENDAR_REDIRECT_URI", 
        "http://localhost:8000/api/v1/calendar/oauth2callback"
    )

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{quote_plus(self.DB_USER)}:{quote_plus(self.DB_PASSWORD)}@{quote_plus(self.DB_HOST)}:{self.DB_PORT}/{quote_plus(self.DB_NAME)}"

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Permite campos extras

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 