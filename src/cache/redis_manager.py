import redis
import json
from typing import Optional, Any
from config.settings import get_settings

settings = get_settings()

class CacheManager:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
        self.ttl = settings.REDIS_CACHE_TTL
    
    def get(self, key: str) -> Optional[Any]:
        try:
            value = self.client.get(key)
            return json.loads(value) if value else None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        try:
            serialized = json.dumps(value)
            expire_time = ttl if ttl else self.ttl
            self.client.setex(key, expire_time, serialized)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str):
        try:
            self.client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        return self.client.exists(key) > 0
    
    def increment(self, key: str, amount: int = 1) -> int:
        return self.client.incrby(key, amount)
    
    def get_metrics(self, pattern: str = "metric:*"):
        keys = self.client.keys(pattern)
        metrics = {}
        for key in keys:
            value = self.get(key)
            if value:
                metrics[key] = value
        return metrics
    
    def clear_all(self):
        self.client.flushdb()

def get_cache() -> CacheManager:
    return CacheManager()
