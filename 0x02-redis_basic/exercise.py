#!/usr/bin/env python3
import redis
import uuid
from typing import Union

"""Module conatains a cache class"""


class Cache:
    """A cache class that Simplifies writing to redis"""
    def __init__(self):
        """Initializes the redis module"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method generates a key sets it to the _redis obeject
        Args:
            data (str, bytes, int, float): To be passed to the class
        Return (str): Generated key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
