# MIT License
#
# Copyright (c) 2020 Christopher Henderson
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

from builtins import object
from builtins import map
from builtins import filter
from builtins import enumerate
from builtins import zip
from builtins import reversed
from builtins import sorted

from collections import Iterable
from collections import Iterator

import itertools
import functools


class Stream(object):

    def __init__(self, stream):
        if isinstance(stream, Iterator):
            self.stream = stream
        elif isinstance(stream, Iterable):
            self.stream = (x for x in stream)
        else:
            raise ValueError(
                'pystream.Stream can only accept either an iterator or an iterable, got {}'.format(type(stream)))

    """
    Returns an iterator that links an arbitrary number of iterators to this iterator, in a chain.
    
    got = Stream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect()
    assert got == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    def chain(self, *others):
        self.stream = itertools.chain(self.stream, *others)
        return self

    """
    Evaluates the stream, consuming it and returning a list of the final output.
    """
    def collect(self):
        return [_ for _ in self]

    """
    Returns an iterator that is deduplicated. Deduplication is computed by applying the builtin `hash` function
    to each element. Ordering of elements is maintained.
    
    numbers = [1, 2, 2, 3, 2, 1, 4, 5, 6, 1]
    got = Stream(numbers).deduplicate().collect()
    assert got == [1, 2, 3, 4, 5, 6]
    """
    def deduplicate(self):
        return self.deduplicate_with(hash)

    """
    Returns an iterator that is deduplicated. Deduplication is computed by applying the provided function `f` to each
    element. `f` must return an object that is itself implements `__hash__` and `__eq__`. 
    Ordering of elements is maintained.

    import hashlib
    
    people = ['Bob', 'Alice', 'Eve', 'Alice', 'Alice', 'Eve', 'Achmed']
    fingerprinter = lambda x: hashlib.sha256(x).digest()
    got = Stream(people).deduplicate_with(fingerprinter).collect()
    assert got == ['Bob', 'Alice', 'Eve', 'Achmed']
    """
    def deduplicate_with(self, f):
        seen = set()
        stream = self.stream

        def inner():
            for x in stream:
                h = f(x)
                if h in seen:
                    continue
                seen.add(h)
                yield x
        self.stream = inner()
        return self

    """
    Returns an iterator that yields the current count and the element during iteration.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).enumerate().collect()
    assert got = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]
    """
    def enumerate(self):
        self.stream = enumerate(self.stream)
        return self

    """
    Returns an iterator that filters each element with `predicate`.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    odds = lambda x: x % 2
    got = Stream(numbers).filter(odds).collect()
    assert got = [2, 4, 6, 8]
    """
    def filter(self, predicate):
        self.stream = filter(predicate, self.stream)
        return self

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
    def flatten(self):
        self.stream = (x for stream in self.stream for x in stream)
        return self

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
    def inspect(self, f):
        stream = self.stream

        def inner():
            for x in stream:
                f(x)
                yield x
        self.stream = inner()
        return self

    """
    Returns an iterator that maps each value with `f`.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    double = lambda x: x * 2
    got = Stream(numbers).map(double).collect()
    assert got == [2, 4, 6, 8, 10, 12, 14, 16, 18]
    """
    def map(self, f):
        self.stream = map(f, self.stream)
        return self

    """
    Collects the stream and applies the function `f` to each item in the stream, producing a single value.

    `reduce` takes two arguments: an initial value, and a function with two arguments: an 'accumulator', and an element.
    The function must return the updated accumulator.

    After `f` has been applied to every item in the stream, the accumulator is returned.

    def add(a, b):
        return a + b

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).reduce(0, add)
    assert got = 45
    """
    def reduce(self, accumulator, f):
        return functools.reduce(f, self, accumulator)

    """
    Returns an iterator that is reversed.
    
    Note that calling `reverse` itself remains lazy, however at time of collecting the stream a reversal
    will incur an internal collection at that particular step. This is due to the reliance of Python's builtin
    `reversed` function which itself requires an object that is indexable.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).reverse().collect()
    assert got == [9, 8, 7, 6, 5, 4, 3, 2, 1]
    """
    def reverse(self):
        stream = self.stream

        def inner():
            return reversed([x for x in stream])
        self.stream = inner()
        return self

    """
    Returns an iterator that skips over `n` number of elements.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).skip(3).collect()
    assert got == [4, 5, 6, 7, 8, 9]
    """
    def skip(self, n):
        self.enumerate().skip_while(lambda x: x[0] < n).map(lambda x: x[1])
        return self

    """
    Returns an iterator that rejects elements while `predicate` returns `True`.
    
    `skip_while` is the complement to `take_while`.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).skip_while(lambda x: x < 5).collect()
    assert got == [5, 6, 7, 8, 9]
    """
    def skip_while(self, predicate):
        self.stream = itertools.dropwhile(predicate, self.stream)
        return self

    """
    Returns an iterator whose elements are sorted.
    """
    def sort(self):
        return self.sort_with()

    """
    Returns an iterator whose elements are sorted using the provided comparator function and key selection function.
    """
    def sort_with(self, comparator=None, key=None):
        stream = self.stream

        def inner():
            return sorted(stream, cmp=comparator, key=key)
        self.stream = inner()
        return self

    """
    Returns an iterator for stepping over items by a custom amount. Regardless of the step, the first item
    in the iterator is always returned. `step` must be greater than or equal to one.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).step_by(3)
    assert got == [1, 2, 3, 4, 5, 6]
    """
    def step_by(self, step):
        self.stream = itertools.islice(self.stream, 0, None, step)
        return self

    """
    Returns an iterator that only iterates over the first `n` iterations.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).take(6).collect()
    assert got == [1, 2, 3, 4, 5, 6]
    """
    def take(self, n):
        self.enumerate().take_while(lambda x: x[0] < n).map(lambda x: x[1])
        return self

    """
    Returns an iterator that only accepts elements while `predicate` returns `True`.
    
    `take_while` is the complement to `skip_while`.
    
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    got = Stream(numbers).take_while(lambda x: x < 5).collect()
    assert got == [1, 2, 3, 4]
    """
    def take_while(self, predicate):
        self.stream = itertools.takewhile(predicate, self.stream)
        return self

    """
    Returns an iterator that iterates over one or more iterators simultaneously.
    
    got = Stream([0, 1, 2]).zip([3, 4, 5]).collect()
    assert got == [(0, 3), (1, 4), (2, 6)]
    """
    def zip(self, *others):
        self.stream = zip(self.stream, *others)
        return self

    def __iter__(self):
        return (x for x in self.stream)



