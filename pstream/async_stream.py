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

from .defensive import must_be_callable
from .errors import InfiniteCollectionError
from .functors import *


class AsyncStream:

    def __init__(self, stream=None):
        if stream is None:
            stream = []
        self.stream = AsyncIterator.new(stream)
        self._infinite = False

    async def collect(self):
        if self._infinite:
            raise InfiniteCollectionError('AsyncStream.collect')
        return [x async for x in self]

    def chain(self, *others):
        self.stream = chain(self.stream, *others)
        return self

    async def count(self):
        if self._infinite:
            raise InfiniteCollectionError('AsyncStream.count')
        count = 0
        async for _ in self:
            count += 1
        return count

    def distinct(self):
        self.stream = distinct(self.stream)
        return self

    @must_be_callable
    def distinct_with(self, f):
        self.stream = distinct_with(f, self.stream)
        return self

    def enumerate(self):
        self.stream = enumerate(self.stream)
        return self

    def flatten(self):
        self.stream = flatten(self.stream)
        return self

    @must_be_callable
    def filter(self, predicate):
        self.stream = filter(predicate, self.stream)
        return self

    @must_be_callable
    async def for_each(self, f):
        if iscoroutinefunction(f):
            async for x in self:
                await f(x)
        else:
            async for x in self:
                f(x)

    @must_be_callable
    def inspect(self, f):
        self.stream = inspect(f, self.stream)
        return self

    @must_be_callable
    def map(self, f):
        self.stream = map(f, self.stream)
        return self

    def pool(self, size):
        if size <= 0:
            raise ValueError("pstream.AsyncStream.pool sizes must be greater than 0. Received {}.".format(size))
        self.stream = pool(size, self.stream)
        return self

    def skip(self, num):
        self.stream = skip(num, self.stream)
        return self

    @must_be_callable
    def skip_while(self, predicate):
        self.stream = skip_while(predicate, self.stream)
        return self

    def sort(self):
        self.stream = sort(self.stream)
        return self

    def step_by(self, step):
        if step == 1:
            return self
        if step < 1:
            raise ValueError("step_by must be a positive integer, received {}".format(step))
        return self.enumerate().filter(lambda e: e.count % step == 0).map(lambda e: e.element)

    @must_be_callable
    async def reduce(self, f, accumulator):
        if iscoroutinefunction(f):
            async for x in self:
                accumulator = await f(accumulator, x)
        else:
            async for x in self:
                accumulator = f(accumulator, x)
        return accumulator

    def repeat(self, element):
        self.stream = repeat(element)
        self._infinite = True
        return self

    def reverse(self):
        self.stream = reverse(self.stream)
        return self

    def take(self, num):
        self.stream = take(num, self.stream)
        self._infinite = False
        return self

    @must_be_callable
    def take_while(self, predicate):
        self.stream = take_while(predicate, self.stream)
        self._infinite = False
        return self

    def tee(self, *others):
        for other in others:
            self.stream = inspect(other.append, self.stream)
        return self

    def zip(self, *streams):
        self.stream = zip(self.stream, *streams)
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.stream.__anext__()
