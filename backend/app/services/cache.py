"""
Redis caching service.
"""
import json
from datetime import timedelta
from typing import Any, Optional
import logging

logger = logging.getLogger(__name__)

# Cache TTL settings (in seconds)
CACHE_TTL = {
    'quote': 300,           # 5 minutes
    'stock': 3600,          # 1 hour
    'etf': 3600,            # 1 hour
    'index_components': 86400,  # 24 hours
    'etf_holdings': 86400,  # 24 hours
    'search': 900,          # 15 minutes
}


class CacheService:
    """
    Redis caching service.
    Falls back to in-memory cache if Redis is not available.
    """
    
    def __init__(self):
        self._redis = None
        self._memory_cache = {}
        self._connected = False
    
    async def connect(self, redis_url: str):
        """Connect to Redis."""
        try:
            import redis.asyncio as redis
            self._redis = redis.from_url(redis_url, decode_responses=True)
            await self._redis.ping()
            self._connected = True
            logger.info("Connected to Redis")
        except Exception as e:
            logger.warning(f"Redis not available, using memory cache: {e}")
            self._connected = False
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self._redis:
            await self._redis.close()
            self._connected = False
    
    def _get_ttl(self, cache_type: str) -> int:
        """Get TTL for cache type."""
        return CACHE_TTL.get(cache_type, 3600)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            if self._connected and self._redis:
                value = await self._redis.get(key)
                if value:
                    return json.loads(value)
            else:
                return self._memory_cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
        return None
    
    async def set(self, key: str, value: Any, cache_type: str = 'stock'):
        """Set value in cache with TTL."""
        try:
            ttl = self._get_ttl(cache_type)
            serialized = json.dumps(value, default=str)
            
            if self._connected and self._redis:
                await self._redis.setex(key, ttl, serialized)
            else:
                self._memory_cache[key] = value
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    async def delete(self, key: str):
        """Delete key from cache."""
        try:
            if self._connected and self._redis:
                await self._redis.delete(key)
            else:
                self._memory_cache.pop(key, None)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    async def delete_pattern(self, pattern: str):
        """Delete keys matching pattern."""
        try:
            if self._connected and self._redis:
                keys = await self._redis.keys(pattern)
                if keys:
                    await self._redis.delete(*keys)
            else:
                keys_to_delete = [k for k in self._memory_cache if pattern.replace('*', '') in k]
                for k in keys_to_delete:
                    del self._memory_cache[k]
        except Exception as e:
            logger.error(f"Cache delete pattern error: {e}")


# Singleton instance
_cache_service: Optional[CacheService] = None


async def get_cache_service() -> CacheService:
    """Get cache service singleton."""
    global _cache_service
    if _cache_service is None:
        from app.config import get_settings
        _cache_service = CacheService()
        settings = get_settings()
        await _cache_service.connect(settings.redis_url)
    return _cache_service


# Helper functions for common cache keys
def quote_key(symbol: str) -> str:
    return f"quote:{symbol.upper()}"

def stock_key(symbol: str) -> str:
    return f"stock:{symbol.upper()}"

def etf_key(symbol: str) -> str:
    return f"etf:{symbol.upper()}"

def index_components_key(index_symbol: str) -> str:
    return f"index_components:{index_symbol.upper()}"

def etf_holdings_key(symbol: str) -> str:
    return f"etf_holdings:{symbol.upper()}"

def search_key(query: str) -> str:
    return f"search:{query.lower()}"
