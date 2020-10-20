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
from collections import namedtuple, defaultdict
from inspect import iscoroutinefunction

from .._sync.stream import Stream
Enumeration = Stream.Enumeration

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
                'pstream.AsyncStream can only accept either an _async iterator, an iterator, or an iterable. Got {}'.format(type(stream)))

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration


class Functor:

    def __init__(self, stream):
        self.stream = AsyncIterator.new(stream)

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.stream.__anext__()


class HigherOrder(Functor):

    class Factory:

        def __init__(self, async_class, sync_class):
            self.async_class = async_class
            self.sync_class = sync_class

        def __call__(self, f, stream):
            if iscoroutinefunction(f):
                return self.async_class(f, stream)
            return self.sync_class(f, stream)

    def __init__(self, f, stream):
        super(HigherOrder, self).__init__(stream)
        self.f = f


class Chain(Functor):

    def __init__(self, *streams):
        super(Chain, self).__init__(flatten((s for s in streams)))


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


class AsyncFilterFalse(HigherOrder):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if not await self.f(x):
                return x


class SyncFilterFalse(HigherOrder):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if not self.f(x):
                return x


class Flatten(Functor):

    def __init__(self, stream):
        super(Flatten, self).__init__(self.flatten(stream))

    @staticmethod
    async def flatten(streams):
        async for stream in AsyncIterator.new(streams):
            async for element in AsyncIterator.new(stream):
                yield element


class AsyncGroupBy(HigherOrder):

    def __init__(self, f, stream):
        super(AsyncGroupBy, self).__init__(f, self.group(stream))

    async def group(self, stream):
        m = defaultdict(list)
        async for element in stream:
            m[await self.f(element)].append(element)
        for element in m.values():
            yield element


class SyncGroupBy(HigherOrder):

    def __init__(self, f, stream):
        super(SyncGroupBy, self).__init__(f, self.group(stream))

    async def group(self, stream):
        m = defaultdict(list)
        async for element in stream:
            m[self.f(element)].append(element)
        for element in m.values():
            yield element


class AsyncInspect(HigherOrder):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            await self.f(x)
            return x


class Repeat(Functor):

    def __init__(self, element):
        super(Repeat, self).__init__(self)
        self.element = element

    async def __anext__(self):
        return self.element


class SyncInspect(HigherOrder):

    async def __anext__(self):
        x = await self.stream.__anext__()
        self.f(x)
        return x


class AsyncSkipWhile(HigherOrder):

    def __init__(self, f, stream):
        self._inner = stream
        super(AsyncSkipWhile, self).__init__(f, self.skip_while(stream))

    async def skip_while(self, stream):
        async for element in stream:
            if not await self.f(element):
                yield element
                break
        async for element in stream:
            yield element


class SyncSkipWhile(HigherOrder):

    def __init__(self, f, stream):
        super(SyncSkipWhile, self).__init__(f, self.skip_while(stream))

    async def skip_while(self, stream):
        async for element in stream:
            if not self.f(element):
                yield element
                break
        async for element in stream:
            yield element


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

    def __init__(self, stream):
        super(Enumerate, self).__init__(stream)
        self.count = 0

    async def __anext__(self):
        element = await self.stream.__anext__()
        count = self.count
        self.count += 1
        return Enumeration(count, element)


class Skip(Functor):

    def __init__(self, limit: int, stream):
        super(Skip, self).__init__(self.skip(limit, stream))

    @staticmethod
    async def skip(limit, stream):
        for _ in range(limit):
            try:
                await stream.__anext__()
            except StopAsyncIteration:
                break
        async for element in stream:
            yield element


class Take(Functor):

    def __init__(self, limit, stream):
        super(Take, self).__init__(self.take(limit, stream))

    @staticmethod
    async def take(limit, stream):
        for _ in range(limit):
            try:
                yield await stream.__anext__()
            except StopAsyncIteration:
                break


class Zip:

    def __init__(self, *streams):
        self.stream = [AsyncIterator.new(s) for s in streams]

    def __aiter__(self):
        return self

    async def __anext__(self):
        return tuple([await s.__anext__() for s in self.stream])


class Pool(Functor):

    def __init__(self, size, stream):
        super(Pool, self).__init__(self.pool(size, stream))

    @staticmethod
    async def pool(size, stream):
        p = list()
        async for x in stream:
            p.append(x)
            if len(p) == size:
                yield p
                p = list()
        if len(p) != 0:
            yield p


class Sort(Functor):

    def __init__(self, stream):
        super(Sort, self).__init__(self.sort(stream))

    @staticmethod
    async def sort(stream):
        for element in sorted([x async for x in stream]):
            yield element


class Reverse(Functor):

    def __init__(self, stream):
        super(Reverse, self).__init__(self.reverse(stream))

    @staticmethod
    async def reverse(stream):
        for element in reversed([x async for x in stream]):
            yield element


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
filter_false = HigherOrder.Factory(AsyncFilterFalse, SyncFilterFalse)
flatten = Flatten
group_by = HigherOrder.Factory(AsyncGroupBy, SyncGroupBy)
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
