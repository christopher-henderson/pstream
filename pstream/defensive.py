from functools import wraps

from pstream.errors import NotCallableError


def must_be_callable(fn):
    @wraps(fn)
    def inner(self, f, *args):
        if not callable(f):
            raise NotCallableError(fn.__qualname__, f)
        return fn(self, f, *args)
    return inner
