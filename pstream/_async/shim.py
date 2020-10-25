# MIT License
#
# Copyright (c) 2020 Christopher Henderson, chris@chenderson.org
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from collections.abc import AsyncIterator, AsyncIterable, Iterator, Iterable
from functools import wraps

from pstream.errors import InfiniteCollectionError


def not_infinite_a(fn):
    async def inner(self, *args, **kwargs):
        if self._infinite:
            raise InfiniteCollectionError(fn)
        return await fn(self, *args, **kwargs)
    return inner


def not_infinite_s(fn):
    def inner(self, *args, **kwargs):
        if self._infinite:
            raise InfiniteCollectionError(fn)
        return fn(self, *args, **kwargs)
    return inner


def shim(fn):
    @wraps(fn)
    def inner(self, *args):
        if isinstance(self.stream, AsyncShim):
            self.stream = self.stream.stream
        try:
            return fn(self, *args)
        finally:
            self.stream = AsyncShim.new(self.stream)
    return inner


def async_shim(fn):
    @wraps(fn)
    async def inner(self, *args):
        if isinstance(self.stream, AsyncShim):
            self.stream = self.stream.stream
        try:
            return await fn(self, *args)
        finally:
            self.stream = AsyncShim.new(self.stream)
    return inner


class AsyncShim:

    @staticmethod
    def new(stream):
        if isinstance(stream, AsyncIterator):
            return stream
        if isinstance(stream, AsyncIterable):
            return stream.__aiter__()
        if isinstance(stream, Iterator):
            return AsyncShim(stream)
        if isinstance(stream, Iterable):
            return AsyncShim(stream.__iter__())
        raise TypeError

    def __init__(self, stream):
        if isinstance(stream, Iterator):
            self.stream = stream
        elif isinstance(stream, Iterable):
            self.stream = stream.__iter__()
        else:
            raise TypeError

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration
