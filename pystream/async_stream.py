from collections import Iterator, Iterable

from pystream.functors import *


import asyncio


class AsyncIterator:

    def __init__(self, stream):
        if isinstance(stream, Iterator):
            self.stream = stream
        elif isinstance(stream, Iterable):
            self.stream = (x for x in stream)
        else:
            raise ValueError(
                'pystream.AsyncStream can only accept either an async iterator, an iterator, or an iterable. Got {}'.format(type(stream)))

    async def __aiter__(self):
        for element in self.stream:
            yield element

    async def __anext__(self):
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration()


class AsyncStream:

    def __init__(self, stream):
        self.stream = stream if isasynciterator(stream) else AsyncIterator(stream)

    async def collect(self):
        return [x async for x in self]

    def enumerate(self):
        self.stream = Enumerate(self.stream)
        return self

    def filter(self, predicate):
        self.stream = filter(predicate, self.stream)
        return self

    def map(self, f):
        self.stream = map(f, self.stream)
        return self

    def skip(self, num):
        self.stream = skip(num, self.stream)
        return self

    def skip_while(self, predicate):
        self.stream = skip_while(predicate, self.stream)
        return self

    def step_by(self, step):
        if step is 1:
            return self
        if step < 1:
            raise ValueError("step_by must be a positive integer, received {}".format(step))
        return self.enumerate().filter(lambda e: e.count % step is 0).map(lambda e: e.element)

    def take(self, num):
        self.stream = take(num, self.stream)
        return self

    def take_while(self, predicate):
        self.stream = take_while(predicate, self.stream)
        return self

    def zip(self, *streams):
        self.stream = zip(self.stream, *streams)
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
    print(await AsyncStream((x for x in range(10))).map(double).collect())
    print(await AsyncStream((x for x in range(10))).map(lambda x: x*2).collect())

    print(await AsyncStream((x for x in range(10))).filter(lambda x: x % 2).map(double).collect())
    print(await AsyncStream((x for x in range(10))).filter(odd).map(lambda x: x * 2).collect())

    print(await AsyncStream((x for x in range(10))).filter(odd).map(lambda x: x * 2).enumerate().collect())

    print(await AsyncStream((x for x in range(10))).filter(odd).skip(2).map(lambda x: x * 2).take(3).collect())
    print(await AsyncStream((x for x in range(10))).filter(odd).skip(2).map(lambda x: x * 2).take_while(lambda x: x < 18).collect())
    print(await AsyncStream((x for x in range(10))).zip(AsyncIterator((x for x in range(10, 20)))).collect())

# inspect.isawaitable()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
a = AsyncIterator([1, 2, 3, 4])
import inspect as binspect
print(isasynciterator(a))
print(isasynciterator(range(10)))
# loop.run_until_complete(lol(derp))
# loop.run_until_complete(lol(herp))
loop.close()
