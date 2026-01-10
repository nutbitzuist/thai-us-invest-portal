"""
Application configuration loaded from environment variables.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql+asyncpg://user:password@localhost:5432/us_invest"
    
    # Redis
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
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse comma-separated origins into list."""
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
