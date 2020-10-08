from inspect import iscoroutinefunction
from collections import namedtuple
from builtins import enumerate as builtin_enumerate


def isasynciterator(obj):
    return callable(getattr(obj, '__aiter__', None)) and callable(getattr(obj, '__anext__', None))


class Step:

    def __init__(self, stream):
        self.stream = stream

    async def __aiter__(self):
        while True:
            yield await self.__anext__()

    async def __anext__(self):
        return await self.stream.__anext__()


class Functor(Step):

    class Factory:

        def __init__(self, async_class, sync):
            self.async_class = async_class
            self.sync = sync

        def __call__(self, f, stream):
            if iscoroutinefunction(f):
                return self.async_class(f, stream)
            return self.sync(f, stream)

    def __init__(self, f, stream):
        super(Functor, self).__init__(stream)
        self.f = f


class AsyncMap(Functor):

    async def __anext__(self):
        return await self.f(await self.stream.__anext__())


class SyncMap(Functor):

    async def __anext__(self):
        return self.f(await self.stream.__anext__())


class AsyncFilter(Functor):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if await self.f(x):
                return x


class SyncFilter(Functor):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if self.f(x):
                return x


class AsyncInspect(Functor):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            await self.f(x)
            yield x


class SyncInspect(Functor):

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            self.f(x)
            yield x


class AsyncSkipWhile(Functor):

    def __init__(self, f, stream):
        super(AsyncSkipWhile, self).__init__(f, stream)
        self.skipping = True

    async def __anext__(self):
        if not self.skipping:
            return self.stream.__anext__()
        while True:
            x = await self.stream.__anext__()
            if await self.f(x):
                continue
            self.skipping = True
            return x


class SyncSkipWhile(Functor):

    def __init__(self, f, stream):
        super(SyncSkipWhile, self).__init__(f, stream)
        self.skipping = True

    async def __anext__(self):
        if not self.skipping:
            return self.stream.__anext__()
        while True:
            x = await self.stream.__anext__()
            if self.f(x):
                continue
            self.skipping = True
            return x


class AsyncTakeWhile(Functor):

    async def __anext__(self):
        x = await self.stream.__anext__()
        if await self.f(x):
            return x
        raise StopAsyncIteration()


class SyncTakeWhile(Functor):

    async def __anext__(self):
        x = await self.stream.__anext__()
        if self.f(x):
            return x
        raise StopAsyncIteration()


class Enumerate(Step):

    Enumeration = namedtuple("Enumeration", ["count", "element"])

    def __init__(self, stream):
        super(Enumerate, self).__init__(stream)
        self.count = 0

    async def __anext__(self):
        element = await self.stream.__anext__()
        count = self.count
        self.count += 1
        return Enumerate.Enumeration(count, element)


class Skip(Step):

    def __init__(self, skip: int, stream):
        stream = skip_while(lambda elem: elem.count < skip, enumerate(stream))
        stream = map(lambda x: x.element, stream)
        super(Skip, self).__init__(stream)


class Take(Step):

    def __init__(self, num, stream):
        stream = take_while(lambda elem: elem.count < num, enumerate(stream))
        stream = map(lambda x: x.element, stream)
        super(Take, self).__init__(stream)


class Zip:

    def __init__(self, *streams):
        self.streams = [s for s in streams]

    async def __aiter__(self):
        while True:
            yield self.__anext__()

    async def __anext__(self):
        zipped = list()
        for i, stream in builtin_enumerate([s for s in self.streams]):
            try:
                zipped.append(await stream.__anext__())
            except StopAsyncIteration:
                self.streams[i] = Empty()
        if len(zipped) is 0:
            raise StopAsyncIteration()
        return tuple(zipped)


class Empty:

    def __anext__(self):
        raise StopAsyncIteration()




map = Functor.Factory(AsyncMap, SyncMap)
filter = Functor.Factory(AsyncFilter, SyncFilter)
inspect = Functor.Factory(AsyncInspect, SyncInspect)
skip_while = Functor.Factory(AsyncSkipWhile, SyncSkipWhile)
take_while = Functor.Factory(AsyncTakeWhile, SyncTakeWhile)
skip = Skip
take = Take
enumerate = Enumerate
zip = Zip