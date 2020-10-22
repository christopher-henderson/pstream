from collections.abc import AsyncIterator, AsyncIterable, Iterator, Iterable
from functools import wraps


def shim(fn):
    @wraps(fn)
    def inner(self, *args):
        if isinstance(self.stream, AsyncShim):
            self.stream = self.stream.stream
        try:
            ret = fn(self, *args)
        finally:
            self.stream = AsyncShim.new(self.stream)
        return ret
    return inner


class AsyncShim:

    @staticmethod
    def new(stream):
        if isinstance(stream, AsyncIterator):
            return stream
        if isinstance(stream, AsyncIterable):
            async def iterator():
                while True:
                    try:
                        yield await stream.__anext__()
                    except StopAsyncIteration:
                        break
            return iterator()
        if isinstance(stream, Iterator):
            return AsyncShim(stream)
        return AsyncShim((_ for _ in stream))

    def __init__(self, stream):
        self.stream = stream

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration
