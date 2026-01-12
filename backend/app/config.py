"""
Application configuration loaded from environment variables.
"""
import os
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database - Railway provides DATABASE_URL in postgres:// format
    # We need to convert to postgresql+asyncpg:// for SQLAlchemy async
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/us_invest"
    
    # Redis - Railway provides REDIS_URL
    redis_url: str = "redis://localhost:6379"
    
    # App Config
    environment: str = "development"
    debug: bool = True
    api_prefix: str = "/api"
    
    # CORS
    allowed_origins: str = "http://localhost:3000"
    
    # Yahoo Finance
    yfinance_rate_limit: int = 5
    
    # Admin
    admin_api_key: str = "dev-secret-key"

    # AI
    openai_api_key: str = None
    
    @property
    def async_database_url(self) -> str:
        """Convert DATABASE_URL to async format for SQLAlchemy."""
        url = self.database_url
        # Railway uses postgres:// but SQLAlchemy async needs postgresql+asyncpg://
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse comma-separated origins into list."""
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
