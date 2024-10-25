#!/usr/bin/env python3
import redis
import uuid
from typing import Union, Optional, Callable, Any

"""Module conatains a cache class"""


class Cache:
    """A cache class that Simplifies writing to redis"""
    def __init__(self):
        """Initializes the redis module"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores data in Redis and returns a generated key.

        Args:
            data (str, bytes, int, float): To be passed to the class

        Return 
            (str): Generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Any]] = None):
        """Retrieves the value of the key from Redis and applies an
        optional conversion func

        Args:
            key (str): The key to retireve.
            fn (Optional[Callable[[bytes], Any]): An optional funtion
                to convert

        Return:
            Optional[Any]: The converted value if fn is provided or None
            it doesnt exist
            """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Optional[str]:
        """"Retrieves the value as a string

        Args:
            key (str) : The key to retrive

        Returns:
            Optional[str]: The value converted to a strign or None if it doesnt exist
            """
        return self.get(key, str)

    def get_int(self, key: str) -> Optional[int]:
        """Retrieves the value of the key as a int

        Args:
            key (int): The key to retrieve

        Returns:
            Optional[str]: The value converted to a string or None if it doesnt exist
            """
        return self.get(key, int)
