"""
Routers package initialization.
"""
from app.routers import health, indices, stocks, etfs, search, analysis

__all__ = [
    "health",
    "indices",
    "stocks",
    "etfs",
    "search",
    "analysis",
]
