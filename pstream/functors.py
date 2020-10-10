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

from collections.abc import Iterable, Iterator
from collections import namedtuple
from inspect import iscoroutinefunction


# @TODO heck yeah! Typing!
# import typing


def isasynciterator(obj):
    return callable(getattr(obj, '__anext__', None))


class AsyncIterator:

    @staticmethod
    def new(stream):
        return stream if isasynciterator(stream) else AsyncIterator(stream)

    def __init__(self, stream):
        if isinstance(stream, Iterator):
            self.stream = stream
        elif isinstance(stream, Iterable):
            self.stream = (x for x in stream)
        else:
            raise ValueError(
                'pstream.AsyncStream can only accept either an async iterator, an iterator, or an iterable. Got {}'.format(type(stream)))

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration


class Functor:

    def __init__(self, stream):
        self.stream = stream

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.stream.__anext__()


class HigherOrder(Functor):

    class Factory:

        def __init__(self, async_class, sync):
            self.async_class = async_class
            self.sync = sync

        def __call__(self, f, stream):
            if iscoroutinefunction(f):
                return self.async_class(f, stream)
            return self.sync(f, stream)

    def __init__(self, f, stream):
        super(HigherOrder, self).__init__(stream)
        self.f = f


class Chain(Functor):

    def __init__(self, *streams):
        super(Chain, self).__init__(flatten(AsyncIterator.new((s for s in streams))))


class AsyncMap(HigherOrder):

    async def __anext__(self):
        return await self.f(await self.stream.__anext__())


class SyncMap(HigherOrder):

    async def __anext__(self):
        return self.f(await self.stream.__anext__())


class AsyncFilter(HigherOrder):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if await self.f(x):
                return x


class SyncFilter(HigherOrder):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if self.f(x):
                return x


class Flatten(Functor):

    def __init__(self, stream):
        super(Flatten, self).__init__(stream)
        self._next = self._lazy_init

    async def __anext__(self):
        return await self._next()

    async def _lazy_init(self):
        self._next = (x async for stream in self.stream async for x in AsyncIterator.new(stream)).__anext__
        return await self.__anext__()


class AsyncInspect(HigherOrder):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            await self.f(x)
            return x


class SyncInspect(HigherOrder):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            self.f(x)
            return x


class AsyncSkipWhile(HigherOrder):

    def __init__(self, f, stream):
        super(AsyncSkipWhile, self).__init__(f, stream)
        self._next = self.__next

    async def __anext__(self):
        return await self._next()

    async def __next(self):
        while True:
            x = await self.stream.__anext__()
            if await self.f(x):
                continue
            self._next = self.stream.__anext__
            return x


class Repeat(Functor):

    def __init__(self, element):
        super(Repeat, self).__init__(self)
        self.element = element

    async def __anext__(self):
        return self.element


class SyncSkipWhile(HigherOrder):

    def __init__(self, f, stream):
        super(SyncSkipWhile, self).__init__(f, stream)
        self._next = self.__next

    async def __anext__(self):
        return await self._next()

    async def __next(self):
        while True:
            x = await self.stream.__anext__()
            if self.f(x):
                continue
            self._next = self.stream.__anext__
            return x


class AsyncTakeWhile(HigherOrder):

    async def __anext__(self):
        x = await self.stream.__anext__()
        if await self.f(x):
            return x
        raise StopAsyncIteration()


class SyncTakeWhile(HigherOrder):

    async def __anext__(self):
        x = await self.stream.__anext__()
        if self.f(x):
            return x
        raise StopAsyncIteration()


class Enumerate(Functor):

    Enumeration = namedtuple("Enumeration", ["count", "element"])

    def __init__(self, stream):
        super(Enumerate, self).__init__(stream)
        self.count = 0

    async def __anext__(self):
        element = await self.stream.__anext__()
        count = self.count
        self.count += 1
        return Enumerate.Enumeration(count, element)


class Skip(Functor):

    def __init__(self, limit: int, stream):
        super(Skip, self).__init__(stream)
        self._limit = limit
        self._next = self._consume

    async def __anext__(self):
        return await self._next()

    async def _consume(self):
        for _ in range(self._limit):
            await self.stream.__anext__()
        self._next = self.stream.__anext__
        return await self.__anext__()


class Take(Functor):

    def __init__(self, limit, stream):
        super(Take, self).__init__(stream)
        self.limit = limit
        self.count = 0

    async def __anext__(self):
        if self.count >= self.limit:
            raise StopAsyncIteration
        self.count += 1
        return await self.stream.__anext__()


class Zip(Functor):

    def __init__(self, *streams):
        super(Zip, self).__init__([AsyncIterator.new(s) for s in streams])

    async def __anext__(self):
        return tuple([await s.__anext__() for s in self.stream])


class Pool(Functor):

    def __init__(self, size, stream):
        super(Pool, self).__init__(stream)
        self.size = size

    async def __anext__(self):
        p = list()
        async for x in self.stream:
            p.append(x)
            if len(p) == self.size:
                return p
        if len(p) != 0:
            return p
        raise StopAsyncIteration


class Sort(Functor):

    def __init__(self, stream):
        super(Sort, self).__init__(stream)
        self._next = self._lazy_init

    async def __anext__(self):
        return await self._next()

    async def _lazy_init(self):
        self._next = AsyncIterator.new(sorted([x async for x in self.stream])).__anext__
        return await self.__anext__()


class Reverse(Functor):

    def __init__(self, stream):
        super(Reverse, self).__init__(stream)
        self._next = self._lazy_init

    async def __anext__(self):
        return await self._next()

    async def _lazy_init(self):
        self._next = AsyncIterator.new(reversed([x async for x in self.stream])).__anext__
        return await self.__anext__()


class Distinct(Functor):

    def __init__(self, stream):
        super(Distinct, self).__init__(stream)
        self.seen = set()

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if x in self.seen:
                continue
            self.seen.add(x)
            return x


class SyncDistinctWith(HigherOrder):

    def __init__(self, f, stream):
        super(SyncDistinctWith, self).__init__(f, stream)
        self.seen = set()

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            h = self.f(x)
            if h in self.seen:
                continue
            self.seen.add(h)
            return x


class AsyncDistinctWith(HigherOrder):

    def __init__(self, f, stream):
        super(AsyncDistinctWith, self).__init__(f, stream)
        self.seen = set()

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            h = await self.f(x)
            if h in self.seen:
                continue
            self.seen.add(h)
            return x


chain = Chain
distinct = Distinct
distinct_with = HigherOrder.Factory(AsyncDistinctWith, SyncDistinctWith)
map = HigherOrder.Factory(AsyncMap, SyncMap)
filter = HigherOrder.Factory(AsyncFilter, SyncFilter)
flatten = Flatten
inspect = HigherOrder.Factory(AsyncInspect, SyncInspect)
skip_while = HigherOrder.Factory(AsyncSkipWhile, SyncSkipWhile)
take_while = HigherOrder.Factory(AsyncTakeWhile, SyncTakeWhile)
repeat = Repeat
skip = Skip
take = Take
enumerate = Enumerate
zip = Zip
pool = Pool
sort = Sort
reverse = Reverse
