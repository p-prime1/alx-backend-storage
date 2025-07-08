#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Optional, Any
from functools import wraps

"""Module to test and practice working with redis in python"""


def count_calls(method: Callable) -> Callable:
    """A decorator function"""

    @wraps(method)
    def increment(self, *args, **kwargs):
        """Function increments each time the method is called"""
        self._redis.incr(method.__qualname__, 1)
        return method(self, *args, **kwargs)

    return increment


def call_history(method: Callable) -> Callable:
    """A decorator function"""

    @wraps(method)
    def history(self, *args, **kwargs):
        self._redis.rpush(method.__qualname__":inputs", str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(method.__qualname__":ouputs", str(output))
        return output
    return history


class Cache:
    """Cache clase used to store data in a redis-server"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method stores data and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: string, fn: Optional[Callable]) -> Any:
        """Retrieves the value of the key from Redis, and
        applies an optional converstion function"""
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """Method converts return value to a string"""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Optional[int]:
        """Method converts return value to an int"""
        return self.get(key, lambda d: int(d))
