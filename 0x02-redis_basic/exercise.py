#!/usr/bin/env python3
import redis
import uuid
from typing import Union
"""Module to test and practice working with redis in python"""


class Cache():
    """Cache clase used to store data in a redis-server"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()


    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method stores data and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key