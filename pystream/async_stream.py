from collections import namedtuple

import inspect
inspect.iscoroutinefunction(object)
import asyncio



class AsyncIterator:

    def __init__(self, stream):
        self.stream = stream

    async def __aiter__(self):
        for element in self.stream:
            yield element

    async def __anext__(self):
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration()


class Step:

    def __init__(self, stream):
        self.stream = stream

    async def __aiter__(self):
        while True:
            yield await self.__anext__()

    def __anext__(self):
        return self.stream.__anext__()


class Functor(Step):

    def __init__(self, f, stream):
        super(Functor, self).__init__(stream)
        self.f = f


class Map(Functor):

    @staticmethod
    def new(f, stream):
        return Map(f, stream) if inspect.iscoroutinefunction(f) else Map.Sync(f, stream)

    async def __anext__(self):
        return await self.f(await self.stream.__anext__())

    class Sync(Functor):

        async def __anext__(self):
            return self.f(await self.stream.__anext__())


class Filter(Functor):

    @staticmethod
    def new(f, stream):
        return Filter(f, stream) if inspect.iscoroutinefunction(f) else Filter.Sync(f, stream)

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            if await self.f(x):
                return x

    class Sync(Functor):

        async def __anext__(self):
            while True:
                x = await self.stream.__anext__()
                if self.f(x):
                    return x


class Inspect(Functor):

    @staticmethod
    def new(f, stream):
        return Inspect(f, stream) if inspect.iscoroutinefunction(f) else Inspect.Sync(f, stream)

    async def __anext__(self):
        while True:
            x = await self.stream.__anext__()
            await self.f(x)
            yield x

    class Sync(Functor):

        async def __anext__(self):
            while True:
                x = await self.stream.__anext__()
                self.f(x)
                yield x


class Skip(Step):

    def __init__(self, skip: int, stream):
        stream = SkipWhile.new(lambda elem: elem.count < skip, Enumerate(stream))
        stream = Map.new(lambda x: x.element, stream)
        super(Skip, self).__init__(stream)


class SkipWhile(Functor):

    def __init__(self, f, stream):
        super(SkipWhile, self).__init__(f, stream)
        self.skipping = True

    @staticmethod
    def new(f, stream):
        return SkipWhile(f, stream) if inspect.iscoroutinefunction(f) else SkipWhile.Sync(f, stream)

    async def __anext__(self):
        if not self.skipping:
            return self.stream.__anext__()
        while True:
            x = await self.stream.__anext__()
            if await self.f(x):
                continue
            self.skipping = True
            return x

    class Sync(Functor):

        def __init__(self, f, stream):
            super(SkipWhile.Sync, self).__init__(f, stream)
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

class Take(Step):

    def __init__(self, take, stream):
        stream = TakeWhile.new(lambda elem: elem.count < take, Enumerate(stream))
        stream = Map.new(lambda x: x.element, stream)
        super(Take, self).__init__(stream)

class TakeWhile(Functor):

    @staticmethod
    def new(f, stream):
        return TakeWhile(f, stream) if inspect.iscoroutinefunction(f) else TakeWhile.Sync(f, stream)

    async def __anext__(self):
        x = await self.stream.__anext__()
        if await self.f(x):
            return x
        raise StopAsyncIteration()

    class Sync(Functor):

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

class AsyncStream:

    def __init__(self, stream):
        self.stream = AsyncIterator(stream)

    async def collect(self):
        return [x async for x in self]

    def enumerate(self):
        self.stream = Enumerate(self.stream)
        return self

    def filter(self, predicate):
        self.stream = Filter.new(predicate, self.stream)
        return self

    def map(self, f):
        self.stream = Map.new(f, self.stream)
        return self

    def skip(self, skip):
        self.stream = Skip(skip, self.stream)
        return self

    def skip_while(self, predicate):
        self.stream = SkipWhile(predicate, self.stream)
        return self

    def step_by(self, step):
        if step is 1:
            return self
        if step < 1:
            raise ValueError("step_by must be a positive integer, received {}".format(step))
        self.stream = Map.new(lambda e: e.element, Filter.new(lambda e: e.count % step is 0, Enumerate(self.stream)))
        return self

    def take(self, take):
        self.stream = Take(take, self.stream)
        return self

    def take_while(self, predicate):
        self.stream = TakeWhile.new(predicate, self.stream)
        return self

    async def __aiter__(self):
        return self.stream

    async def __anext__(self):
        return self.stream.__anext__()





async def double(num):
    return num * 2

async def odd(num):
    return num % 2

async def main():
    print(await AsyncStream((x for x in range(1, 10))).step_by(2).collect())
    # print(await AsyncStream((x for x in range(10))).map(double).collect())
    # print(await AsyncStream((x for x in range(10))).map(lambda x: x*2).collect())
    #
    # print(await AsyncStream((x for x in range(10))).filter(lambda x: x % 2).map(double).collect())
    # print(await AsyncStream((x for x in range(10))).filter(odd).map(lambda x: x * 2).collect())
    #
    # print(await AsyncStream((x for x in range(10))).filter(odd).map(lambda x: x * 2).enumerate().collect())

    # print(await AsyncStream((x for x in range(10))).filter(odd).skip(2).map(lambda x: x * 2).take(4).collect())
    # print(await AsyncStream((x for x in range(10))).filter(odd).skip(2).map(lambda x: x * 2).take_while(lambda e: e < 0).collect())
    # numbers = await Mine(numbers).filter(lambda x: x % 2).map(lambda x: x * 2).collect()

# inspect.isawaitable()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# loop.run_until_complete(lol(derp))
# loop.run_until_complete(lol(herp))
loop.close()