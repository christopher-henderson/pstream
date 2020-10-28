from functools import wraps

from pstream.errors import InfiniteCollectionError


def not_infinite(fn):
    @wraps(fn)
    def inner(self, *args, **kwargs):
        if self._infinite:
            raise InfiniteCollectionError(fn)
        return fn(self, *args, **kwargs)
    return inner
