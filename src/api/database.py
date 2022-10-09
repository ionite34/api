from collections.abc import Callable
from functools import cache, wraps

from google.cloud import datastore


class Database(datastore.Client):
    """Database Operations."""

    def cache(self, key: str):
        def wrapper(func: Callable):
            @wraps(func)
            async def wrapped(*args, **kwargs):
                return await func(*args, **kwargs)

            return wrapped

        return wrapper


db = Database()
