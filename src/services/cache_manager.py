import redis
from typing import Any, Dict, Optional, Union
import pickle
import json
import hashlib
import time
from functools import wraps

class CacheManager:
    """Handle complex caching operations."""
    
    def __init__(
        self,
        redis_url: str,
        default_ttl: int = 3600
    ):
        self.redis_client = redis.from_url(redis_url)
        self.default_ttl = default_ttl

    def _generate_key(self, base_key: str, params: Dict) -> str:
        """Generate unique cache key."""
        param_str = json.dumps(params, sort_keys=True)
        hash_str = hashlib.md5(param_str.encode()).hexdigest()
        return f"{base_key}:{hash_str}"

    def get(
        self,
        key: str,
        deserialize: bool = True
    ) -> Optional[Any]:
        """Retrieve data from cache."""
        data = self.redis_client.get(key)
        if data and deserialize:
            return pickle.loads(data)
        return data

    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        serialize: bool = True
    ) -> bool:
        """Store data in cache."""
        ttl = ttl or self.default_ttl
        if serialize:
            value = pickle.dumps(value)
        return self.redis_client.setex(key, ttl, value)

    def delete(self, key: str) -> bool:
        """Remove data from cache."""
        return bool(self.redis_client.delete(key))

    def cache_decorator(
        self,
        prefix: str,
        ttl: Optional[int] = None
    ):
        """Decorator for automatic caching."""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_key(
                    prefix,
                    {'args': args, 'kwargs': kwargs}
                )
                
                # Try to get from cache
                cached_result = self.get(cache_key)
                if cached_result is not None:
                    return cached_result
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                self.set(cache_key, result, ttl=ttl)
                return result
            return wrapper
        return decorator

    def invalidate_pattern(self, pattern: str) -> int:
        """Invalidate all keys matching pattern."""
        keys = self.redis_client.keys(pattern)
        if keys:
            return self.redis_client.delete(*keys)
        return 0

    def get_or_compute(
        self,
        key: str,
        compute_func: callable,
        ttl: Optional[int] = None
    ) -> Any:
        """Get from cache or compute and store."""
        result = self.get(key)
        if result is None:
            result = compute_func()
            self.set(key, result, ttl=ttl)
        return result