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

from __future__ import absolute_import

import functools
import itertools

from builtins import object
from builtins import map
from builtins import filter
from builtins import enumerate
from builtins import zip
from builtins import reversed
from builtins import sorted

from .defensive import must_be_callable

try:
    # Py3
    from collections.abc import Iterator, Iterable
except ImportError:
    # Py2
    from collections import Iterator, Iterable
from collections import namedtuple

from .errors import InfiniteCollectionError, NotCallableError


class Stream(object):

    def __init__(self, stream=None):
        if stream is None:
            stream = []
        if isinstance(stream, Iterator):
            self._stream = stream
        elif isinstance(stream, Iterable):
            self._stream = (x for x in stream)
        else:
            raise ValueError(
                'pstream.Stream can only accept either an iterator or an iterable. Got {}'.format(type(stream)))
        self._infinite = False

    def chain(self, *others):
        """
        Returns an iterator that links an arbitrary number of iterators to this iterator, in a chain.

        got = Stream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect()
        assert got == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        self._stream = itertools.chain(self._stream, *others)
        return self

    def count(self):
        """
        Evaluates the stream, consuming it and returning a count of the number of elements in the stream.
        """
        if self._infinite:
            raise InfiniteCollectionError('Stream.count')
        count = 0
        for _ in self:
            count += 1
        return count

    def collect(self):
        """
        Evaluates the stream, consuming it and returning a list of the final output.
        """
        if self._infinite:
            raise InfiniteCollectionError('Stream.collect')
        return [_ for _ in self]

    def distinct(self):
        """
        Returns an iterator of distinct elements. Distinction is computed by applying the builtin `hash` function
        to each element. Ordering of elements is maintained.

        numbers = [1, 2, 2, 3, 2, 1, 4, 5, 6, 1]
        got = Stream(numbers).deduplicate().collect()
        assert got == [1, 2, 3, 4, 5, 6]
        """
        seen = set()
        stream = self._stream

        def inner():
            for x in stream:
                if x in seen:
                    continue
                seen.add(x)
                yield x
        self._stream = inner()
        return self

    @must_be_callable
    def distinct_with(self, f):
        """
        Returns an iterator that is distinct. Distinction is computed by applying the provided function `f` to each
        element. `f` must return an object that is itself implements `__hash__` and `__eq__`.
        Ordering of elements is maintained.

        import hashlib

        people = ['Bob', 'Alice', 'Eve', 'Alice', 'Alice', 'Eve', 'Achmed']
        fingerprinter = lambda x: hashlib.sha256(x).digest()
        got = Stream(people).deduplicate_with(fingerprinter).collect()
        assert got == ['Bob', 'Alice', 'Eve', 'Achmed']
        """
        seen = set()
        stream = self._stream

        def inner():
            for x in stream:
                h = f(x)
                if h in seen:
                    continue
                seen.add(h)
                yield x
        self._stream = inner()
        return self

    Enumeration = namedtuple('Enumeration', ['count', 'element'])

    def enumerate(self):
        """
        Returns an iterator that yields the current count and the element during iteration.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).enumerate().collect()
        assert got = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
        """
        self._stream = enumerate(self._stream)
        return self.map(lambda enumeration: Stream.Enumeration(*enumeration))

    @must_be_callable
    def filter(self, predicate):
        """
        Returns an iterator that filters each element with `predicate`.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        odds = lambda x: x % 2
        got = Stream(numbers).filter(odds).collect()
        assert got = [2, 4, 6, 8]
        """
        self._stream = filter(predicate, self._stream)
        return self

    def flatten(self):
        """
        Returns an iterator that flattens one level of nesting in a stream of things that can be turned into iterators.

        # Flatten a two dimensional array to a one dimensional array.
        two_dimensional = [[1, 2, 3], [4, 5, 6]]
        got = Stream(two_dimensional).flatten().collect()
        assert got == [1, 2, 3, 4, 5, 6]

        # Flatten a three dimensional array to a two dimensional array.
        three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        got = Stream(three_dimensional).flatten().collect()
        assert got == [[1, 2, 3], [4, 5, 6]]

        # Flatten a three dimensional array to a one dimensional array.
        three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        got = Stream(three_dimensional).flatten().flatten().collect()
        assert got == [1, 2, 3, 4, 5, 6]
        """
        self._stream = (x for stream in self._stream for x in stream)
        return self

    @must_be_callable
    def for_each(self, f):
        """
        Evaluates the stream, consuming it and calling f for each element in the stream.

        Not that while other stream consumers, such as collect and count, will raise in
        an InfiniteCollectionError if called on an infinite stream (see the documentation
        regarding Stream.repeat and Stream.repeat_with), for_each will not. This makes
        the following...

        Stream().repeat_with(input).for_each(print)

        ...roughly equivalent to:

        while True:
            print(input())
        """
        for x in self:
            f(x)

    @must_be_callable
    def inspect(self, f):
        """
        Returns an iterator that calls the function, `f`, with a reference to each element before yielding it.

        def log(number):
            if number % 2 is not 0:
                print("WARN: {} is not even!".format(number))

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).inspect(log).collect()
        >> WARN: 1 is not even!
        >> WARN: 3 is not even!
        >> WARN: 5 is not even!
        >> WARN: 7 is not even!
        >> WARN: 9 is not even!
        assert got == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        stream = self._stream

        def inner():
            for x in stream:
                f(x)
                yield x
        self._stream = inner()
        return self

    @must_be_callable
    def map(self, f):
        """
        Returns an iterator that maps each value with `f`.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        double = lambda x: x * 2
        got = Stream(numbers).map(double).collect()
        assert got == [2, 4, 6, 8, 10, 12, 14, 16, 18]
        """
        self._stream = map(f, self._stream)
        return self

    @must_be_callable
    def reduce(self, f, accumulator):
        """
        Collects the stream and applies the function `f` to each item in the stream, producing a single value.

        `reduce` takes two arguments: an initial value, and a function with two arguments: an 'accumulator', and an element.
        The function must return the updated accumulator.

        After `f` has been applied to every item in the stream, the accumulator is returned.

        def add(a, b):
            return a + b

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).reduce(add, 0)
        assert got = 45
        """
        return functools.reduce(f, self, accumulator)

    def reverse(self):
        """
        Returns an iterator that is reversed.

        Note that calling `reverse` itself remains lazy, however at time of collecting the stream a reversal
        will incur an internal collection at that particular step. This is due to the reliance of Python's builtin
        `reversed` function which itself requires an object that is indexable.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).reverse().collect()
        assert got == [9, 8, 7, 6, 5, 4, 3, 2, 1]
        """
        stream = self._stream

        def inner():
            return reversed([x for x in stream])
        self._stream = inner()
        return self

    def skip(self, n):
        """
        Returns an iterator that skips over `n` number of elements.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).skip(3).collect()
        assert got == [4, 5, 6, 7, 8, 9]
        """
        stream = self._stream

        def inner():
            for _ in range(n):
                next(stream)
            for x in stream:
                yield x
        self._stream = inner()
        return self

    @must_be_callable
    def skip_while(self, predicate):
        """
        Returns an iterator that rejects elements while `predicate` returns `True`.

        `skip_while` is the complement to `take_while`.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).skip_while(lambda x: x < 5).collect()
        assert got == [5, 6, 7, 8, 9]
        """
        self._stream = itertools.dropwhile(predicate, self._stream)
        return self

    def sort(self):
        """
            Returns an iterator whose elements are sorted.
            """
        return self.sort_with()

    def sort_with(self, key=None):
        """
        Returns an iterator whose elements are sorted using the provided key selection function.
        """
        stream = self._stream

        def inner():
            return sorted(stream, key=key)
        self._stream = inner()
        return self

    def step_by(self, step):
        """
        Returns an iterator for stepping over items by a custom amount. Regardless of the step, the first item
        in the iterator is always returned. `step` must be greater than or equal to one.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).step_by(3)
        assert got == [1, 2, 3, 4, 5, 6]
        """
        self._stream = itertools.islice(self._stream, 0, None, step)
        return self

    def take(self, n):
        """
        Returns an iterator that only iterates over the first `n` iterations.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).take(6).collect()
        assert got == [1, 2, 3, 4, 5, 6]
        """
        stream = self._stream

        def inner():
            for _ in range(n):
                try:
                    yield next(stream)
                except StopIteration:
                    break
        self._stream = inner()
        self._infinite = False
        return self

    @must_be_callable
    def take_while(self, predicate):
        """
        Returns an iterator that only accepts elements while `predicate` returns `True`.

        `take_while` is the complement to `skip_while`.

        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).take_while(lambda x: x < 5).collect()
        assert got == [1, 2, 3, 4]
        """
        self._stream = itertools.takewhile(predicate, self._stream)
        self._infinite = False
        return self

    def tee(self, *others):
        """
        Returns an iterator whose elements will be appended to objects in 'others'.
        All objects in `others` must support an `append` method.

        a = list()
        b = list()
        got = Stream([1, 2, 3, 4]).tee(a, b).map(lambda x: x * 2).collect()
        assert got == [2, 4, 6 ,8]
        assert a == [1, 2, 3, 4]
        assert b == [1, 2, 3, 4]
        """
        stream = self._stream

        def inner():
            for element in stream:
                for other in others:
                    other.append(element)
                yield element
        self._stream = inner()
        return self

    def zip(self, *others):
        """
        Returns an iterator that iterates over one or more iterators simultaneously.

        got = Stream([0, 1, 2]).zip([3, 4, 5]).collect()
        assert got == [(0, 3), (1, 4), (2, 6)]
        """
        self._stream = zip(self._stream, *others)
        return self

    def pool(self, size):
        """
        Returns an iterator that will collect up to `size` elements into a list before
        yielding.

        `size` must be greater than 0.

        got = Stream([1, 2, 3, 4, 5]).pool(3).collect()
        assert = got == [[1, 2, 3], [4, 5]]

        Note that `pool` effectively behaves as the inverse to `flatten` by gradually
        introducing higher levels of dimensionality.

        one = [1, 2, 3, 4, 5, 6, 7, 8]
        two = Stream(one).pool(2).collect()
        two == [[1, 2], [3, 4], [5, 6], [7, 8]]
        three = Stream(two).pool(2).collect()
        three == [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        """
        if size <= 0:
            raise ValueError("pstream.Stream.pool sizes must be greater than 0. Received {}.".format(size))
        stream = self._stream

        def inner():
            pool = list()
            for x in stream:
                pool.append(x)
                if len(pool) == size:
                    yield pool
                    pool = list()
            if len(pool) != 0:
                yield pool
        self._stream = inner()
        return self

    def repeat(self, element):
        """
        Returns an iterator the repeats an element endlessly.

        A call to `repeat` __wipes out__ any previous step in the iterator.
        Unless a terminating step, such as take_while, has been setup after
        a call to `repeat`, `collect` will throw an InfiniteCollectionError.
        """
        return self.repeat_with(lambda: element)

    @must_be_callable
    def repeat_with(self, f):
        """
        Returns an iterator the yields the output of `f` endlessly.

        A call to `repeat_with` __wipes out__ any previous step in the iterator.
        Unless a terminating step, such as take_while, has been setup after
        a call to `repeat_with`, `collect` and `count` will throw an InfiniteCollectionError.
        """

        def inner():
            while True:
                yield f()
        self._stream = inner()
        self._infinite = True
        return self

    def __iter__(self):
        return (x for x in self._stream)

    def __next__(self):
        return next(self._stream)
