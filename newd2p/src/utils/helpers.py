"""
newd2p - General Helpers
"""

import time
import functools
from src.utils.logger import get_logger

logger = get_logger("helpers")


def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        logger.info(f"{func.__name__} completed in {elapsed:.2f}s")
        return result
    return wrapper


def safe_get(dictionary: dict, key: str, default=None):
    keys = key.split(".")
    value = dictionary
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k, default)
        else:
            return default
    return value
