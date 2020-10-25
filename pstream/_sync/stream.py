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

from collections import namedtuple, defaultdict

try:
    # Py3
    from collections.abc import Iterator, Iterable
except ImportError:  # pragma: no cover
    # Py2
    from collections import Iterator, Iterable

from pstream.errors import InfiniteCollectionError
from pstream.utils.defensive import must_be_callable


class Stream(object):

    def __init__(self, initial=None):
        """
        :param initial: An optional initial value for the stream. `Must` be either an iterator or an iterable.
                        If `initial` is `None` then the stream with be initialized to be empty.

        :Raises: :class:`ValueError` if `initial` is neither an iterator nor an iterable.
        """
        if initial is None:
            initial = []
        if isinstance(initial, Iterator):
            self._stream = initial
        elif isinstance(initial, Iterable):
            self._stream = (x for x in initial)
        else:
            raise ValueError(
                'pstream.Stream can only accept either an iterator or an iterable. Got {}'.format(type(initial)))
        self._infinite = False

    def chain(self, *iterables):
        """
        Returns a stream that links an arbitrary number of iterators to this iterator, in a chain.

        :param iterables: Zero or more iterable objects. These iterables will be chained to the stream
                            in a left-to-right fashion.

        :Returns: :class:`Stream`

        :Example:
        >>> got = Stream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect()
        >>> assert got == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        self._stream = itertools.chain(self._stream, *iterables)
        return self

    def count(self):
        """
        Evaluates the stream, consuming it and returning a count of the number of elements in the stream.

        :Returns: :class:`int`

        :Raises: :class:`errors.InfiniteCollectionError`

        :Example:
        >>> count = Stream(range(100)).filter(lambda x: x % 2 is 0).count()
        >>> assert count == 50
        """
        if self._infinite:
            raise InfiniteCollectionError(Stream.count)
        count = 0
        for _ in self:
            count += 1
        return count

    def collect(self):
        """
        Evaluates the stream, consuming it and returning a list of the final output.

        :Returns: :class:`list`

        :Raises: :class:`errors.InfiniteCollectionError`

        :Example:
        >>> stream = Stream([1, 2, 3, 4]).map(lambda x: x * 2)
        >>> got = stream.collect()
        >>> assert got == [2, 4, 6, 8]
        """
        if self._infinite:
            raise InfiniteCollectionError(Stream.collect)
        return [_ for _ in self]

    def distinct(self):
        """
        Returns a stream of distinct elements. Distinction is computed by applying the builtin `hash` function
        to each element. Ordering of elements in the stream is maintained.

        This functor incurs an additional allocation in the form of a hashset in order to keep track of
        the elements in the stream.

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 2, 3, 2, 1, 4, 5, 6, 1]
        >>> got = Stream(numbers).distinct().collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]
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
    def distinct_with(self, key):
        """
        Returns a stream of distinct elements. Distinction is computed by applying the builtin `hash` function
        to each item generated by the provided `key(element)`. Ordering of elements in the stream is maintained.

        This functor incurs an additional allocation in the form of a hashset in order to keep track of
        the elements in the stream.

        :param key: A function such that `key(element) -> T` where `T` must be hashable.

        :Returns: :class:`Stream`

        :Example:
        >>> import hashlib
        >>>
        >>> people = ['Bob', 'Alice', 'Eve', 'Alice', 'Alice', 'Eve', 'Achmed']
        >>> fingerprinter = lambda x: hashlib.sha256(x.encode('UTF-8')).digest()
        >>> got = Stream(people).distinct_with(fingerprinter).collect()
        >>> assert got == ['Bob', 'Alice', 'Eve', 'Achmed']
        """
        seen = set()
        stream = self._stream

        def inner():
            for x in stream:
                h = key(x)
                if h in seen:
                    continue
                seen.add(h)
                yield x
        self._stream = inner()
        return self

    Enumeration = namedtuple('Enumeration', ['count', 'element'])

    def enumerate(self):
        """
        Returns a stream that yields the current count and the element during iteration.

        :Returns: :class:`Stream`

        :Example:
        >>> got = Stream(range(1, 10)).enumerate().collect()
        >>> assert got == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]

        The constructed tuple is the namedtuple, :class:`Stream.Enumeration`, which provides
        the names `count` and `element`.

        :Example:
        >>> def count(enumeration):
        ...     print(enumeration.count, enumeration.element)
        >>> got = Stream(range(1, 5)).enumerate().inspect(count).map(lambda e: e.element).collect()
        0 1
        1 2
        2 3
        3 4
        >>> assert got == [1, 2, 3, 4]
        """
        self._stream = enumerate(self._stream)
        return self.map(lambda enumeration: Stream.Enumeration(*enumeration))

    @must_be_callable
    def filter(self, predicate):
        """
        Returns a stream that filters each element using `predicate`. Only elements for which `predicate`
        returns `True` are passed through the stream.

        :param predicate: A function such that `predicate(element) -> bool`.

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> odds = lambda x: x % 2 != 0
        >>> got = Stream(numbers).filter(odds).collect()
        >>> assert got == [1, 3, 5, 7, 9]
        """
        self._stream = filter(predicate, self._stream)
        return self

    @must_be_callable
    def filter_false(self, predicate):
        """
        Returns a stream that filters each element using `predicate`. Only elements for which `predicate`
        returns `False` are passed through the stream.

        :param predicate: A function such that `predicate(element) -> bool`.

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> odds = lambda x: x % 2 != 0
        >>> got = Stream(numbers).filter_false(odds).collect()
        >>> assert got == [2, 4, 6, 8]
        """
        return self.filter(lambda x: not predicate(x))

    def flatten(self):
        """
        Returns a stream that flattens one level of nesting in a stream of elements that are themselves iterators.

        :Returns: :class:`Stream`

        :Example:
        >>> # Flatten a two dimensional array to a one dimensional array.
        >>> two_dimensional = [[1, 2, 3], [4, 5, 6]]
        >>> got = Stream(two_dimensional).flatten().collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]

        >>> # Flatten a three dimensional array to a two dimensional array.
        >>> three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        >>> got = Stream(three_dimensional).flatten().collect()
        >>> assert got == [[1, 2, 3], [4, 5, 6]]

        >>> # Flatten a three dimensional array to a one dimensional array.
        >>> three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        >>> got = Stream(three_dimensional).flatten().flatten().collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]
        """
        self._stream = (x for stream in self._stream for x in stream)
        return self

    @must_be_callable
    def for_each(self, f):
        """
        Evaluates the stream, consuming it and calling `f` for each element in the stream.

        Note that while other stream consumers, such as :meth:`Stream.collect` and :meth:`Stream.count`, will raise an
        an :class:`errors.InfiniteCollectionError` if called on an infinite stream (see the documentation
        regarding :meth:`Stream.repeat` and :meth:`Stream.repeat_with`), `for_each` will not.

        This makes the following...

        >>> Stream().repeat_with(input).for_each(print)  # doctest: +SKIP

        ...roughly equivalent to:

        >>> while True:  # doctest: +SKIP
        ...   print(input())  # doctest: +SKIP

        :param f: A function such that `f(element)`. Any value returned is ignored.

        :Example:
        >>> Stream(range(1, 5)).for_each(print)
        1
        2
        3
        4
        """
        for x in self:
            f(x)

    def group_by(self, key):
        """
        Returns a stream that groups elements together using the provided `key` function.

        The ordering of the groups is non-deterministic.

        :param key: A function such that `f(element) -> T` where `T` will be used to group elements together.

        :Returns: :class:`Stream`

        :Example:
        >>> # Group people by how long their names are.
        >>> names = ['Alice', 'Bob', 'Eve', 'Chris', 'Arjuna', 'Zack']
        >>> got = Stream(names).group_by(len).collect()
        >>> len(got) == 4
        True
        >>> ['Alice', 'Chris'] in got
        True
        >>> ['Bob', 'Eve'] in got
        True
        >>> ['Arjuna'] in got
        True
        >>> ['Zack'] in got
        True

        :Example:
        >>> # Group the numbers [0, 10) by evens and odds.
        >>> got = Stream(range(10)).group_by(lambda x: x % 2).collect()
        >>> len(got) == 2
        True
        >>> [1, 3, 5, 7, 9] in got
        True
        >>> [0, 2, 4, 6, 8] in got
        True
        """
        stream = self._stream

        def inner():
            m = defaultdict(list)
            for element in stream:
                m[key(element)].append(element)
            for grouping in m.values():
                yield grouping
        self._stream = inner()
        return self

    @must_be_callable
    def inspect(self, f):
        """
        Returns a stream that calls the function, `f`, with a reference to each element before yielding it.

        :param f: A function such that `f(element)`. Any value returned is ignored.

        :Returns: :class:`Stream`

        :Example:
        >>> def log(number):
        ...     if number % 2 != 0:
        ...         print("WARNING: {} is not even!".format(number))
        >>>
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).inspect(log).collect()
        WARNING: 1 is not even!
        WARNING: 3 is not even!
        WARNING: 5 is not even!
        WARNING: 7 is not even!
        WARNING: 9 is not even!
        >>> assert got == [1, 2, 3, 4, 5, 6, 7, 8, 9]
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
        Returns a stream that maps each value using `f`.

        :param f: A function such that `f(A) -> B`.

        :Returns: :class:`Stream`

        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> double = lambda x: x * 2
        >>> got = Stream(numbers).map(double).collect()
        >>> assert got == [2, 4, 6, 8, 10, 12, 14, 16, 18]
        """
        self._stream = map(f, self._stream)
        return self

    @must_be_callable
    def reduce(self, f, accumulator):
        """
        Evaluates the stream, consuming it and applying the function `f` to each item in the stream,
        producing a single value.

        After `f` has been applied to every item in the stream, the updated `accumulator` is returned.

        :param f: A function such that `f(accumulator: T, element) -> T`.
        :param accumulator: The initial value provided to `f`.

        :Returns: `T` such that `f(accumulator: T, element) -> T`.

        Example:

        >>> def stringify(accumulator, element):
        ...    return accumulator + str(element)
        >>>
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).reduce(stringify, '')
        >>> assert got == '123456789'
        """
        return functools.reduce(f, self, accumulator)

    def reverse(self):
        """
        Returns a stream whose elements are reversed.

        Note that calling `reverse` itself remains lazy, however at time of collecting the stream a reversal
        will incur an internal collection at that particular step. This is due to the reliance of Python's builtin
        `reversed` function which itself requires an object that is indexable.

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).reverse().collect()
        >>> assert got == [9, 8, 7, 6, 5, 4, 3, 2, 1]
        """
        stream = self._stream

        def inner():
            return reversed([x for x in stream])
        self._stream = inner()
        return self

    def skip(self, n):
        """
        Returns a stream that skips over `n` number of elements.

        :param n: :class:`int`

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).skip(3).collect()
        >>> assert got == [4, 5, 6, 7, 8, 9]
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
        Returns a stream that rejects elements while `predicate` returns `True`.

        `skip_while` is the complement to :meth:`Stream.take_while`.

        :param predicate: A function such that `f(element) -> bool`.

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).skip_while(lambda x: x < 5).collect()
        >>> assert got == [5, 6, 7, 8, 9]
        """
        self._stream = itertools.dropwhile(predicate, self._stream)
        return self

    def sort(self):
        """
        Returns a stream whose elements are sorted.

        Note that calling `sort` itself remains lazy, however at time of collecting the stream a sort
        will incur an internal collection at that particular step.

        :Returns: :class:`Stream`

        :Example:
        >>> arr = [12, 233, 4567, 344523, 7, 567, 34, 5678, 456, 23, 4, 7, 63, 45, 345]
        >>> got = Stream(arr).sort().collect()
        >>> assert got == [4, 7, 7, 12, 23, 34, 45, 63, 233, 345, 456, 567, 4567, 5678, 344523]
        """
        return self.sort_with(None)

    def sort_with(self, key):
        """
        Returns a stream whose elements are sorted using the provided key selection function.

        Note that calling `sort_with` itself remains lazy, however at time of collecting the stream a sort
        will incur an internal collection at that particular step.

        :param key: A function such that `key(element) -> T` where `T` is the type used for comparison.

        :Returns: :class:`Stream`

        :Example:
        >>> arr = ['12', '233', '4567', '344523', '7', '567', '34', '5678', '456', '23', '4', '7', '63', '45', '345']
        >>> got = Stream(arr).sort_with(len).collect()
        >>> assert got == ['7', '4', '7', '12', '34', '23', '63', '45', '233', '567', '456', '345', '4567', '5678', '344523']
        """
        stream = self._stream

        def inner():
            return sorted(stream, key=key)
        self._stream = inner()
        return self

    def step_by(self, step):
        """
        Returns a stream which steps over items by a custom amount. Regardless of the step, the first item
        in the stream is always returned.

        :param step: :class:`int`. `Must` be greater than or equal to one.

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).step_by(3).collect()
        >>> assert got == [1, 4, 7]
        """
        self._stream = itertools.islice(self._stream, 0, None, step)
        return self

    def take(self, n):
        """
        Returns a stream that only iterates over the first `n` elements.

        :param n: :class:`int`

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).take(6).collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]
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
        Returns a stream that only accepts elements while `predicate` returns `True`.

        `take_while` is the complement to :meth:`Stream.skip_while`.

        :param predicate: A function such that `predicate(element) -> bool`.

        :Returns: :class:`Stream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = Stream(numbers).take_while(lambda x: x < 5).collect()
        >>> assert got == [1, 2, 3, 4]
        """
        self._stream = itertools.takewhile(predicate, self._stream)
        self._infinite = False
        return self

    def tee(self, *receivers):
        """
        Returns a stream whose elements will be appended to objects in `receivers`.

        `tee` behaves similarly to the `Unix tee command <https://man7.org/linux/man-pages/man1/tee.1.html>`_.

        :param receivers: Zero or more objects that `must` support an `append` method.

        :Returns: :class:`Stream`

        :Example:
        >>> a = list()
        >>> b = list()
        >>> got = Stream([1, 2, 3, 4]).tee(a, b).map(lambda x: x * 2).collect()
        >>> assert got == [2, 4, 6 ,8]
        >>> assert a == [1, 2, 3, 4]
        >>> assert b == [1, 2, 3, 4]
        """
        stream = self._stream

        def inner():
            for element in stream:
                for other in receivers:
                    other.append(element)
                yield element
        self._stream = inner()
        return self

    def zip(self, *iterables):
        """
        Returns a stream that iterates over one or more iterators simultaneously.

        :param iterables: Zero or more iterable objects.

        :Returns: :class:`Stream`

        :Example:
        >>> got = Stream([0, 1, 2]).zip([3, 4, 5]).collect()
        >>> assert got == [(0, 3), (1, 4), (2, 5)]
        """
        self._stream = zip(self._stream, *iterables)
        return self

    def pool(self, size):
        """
        Returns a stream that will collect up to `size` elements into a list before yielding.

        :param size: :class:`int`. `Must` be greater than 0.

        :Returns: :class:`Stream`

        :Example:
        >>> got = Stream([1, 2, 3, 4, 5]).pool(3).collect()
        >>> assert got == [[1, 2, 3], [4, 5]]

        Note that `pool` effectively behaves as the inverse to :meth:`Stream.flatten` by gradually
        introducing higher levels of dimensionality.

        :Example:
        >>> one = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> two = Stream(one).pool(2).collect()
        >>> assert two == [[1, 2], [3, 4], [5, 6], [7, 8]]
        >>> three = Stream(two).pool(2).collect()
        >>> assert three == [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
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
        Returns a stream that repeats an element endlessly.

        :param element: Any object. This exact object will be yieled repeatedly.

        :Returns: :class:`Stream`

        :Example:
        >>> got = Stream().repeat(1).take(5).collect()
        >>> assert got == [1, 1, 1, 1, 1]

        A call to `repeat` wipes out any previous step in the iterator.

        :Example:
        >>> # The initial range, enumeration, and chain are completely lost
        >>> # and the stream returns 1 indefinitely.
        >>> s = Stream(range(10)).enumerate().chain(range(10, 20)).repeat(1)

        Unless a limiting step, such as :meth:`Stream.take_while` or :meth:`Stream.take`, has been setup after
        a call to `repeat`, the consumers :meth:`Stream.collect` and :meth:`Stream.count`
        will throw an :class:`errors.InfiniteCollectionError`.

        :Example:
        >>> try:
        ...     Stream().repeat(1).collect()
        ... except InfiniteCollectionError as error:
        ...     print(error)
        Stream.collect was called on an infinitely repeating iterator. If you use Stream.repeat, then you MUST include either a Stream.take or a Stream.take_while if you wish to call Stream.collect
        """
        return self.repeat_with(lambda: element)

    @must_be_callable
    def repeat_with(self, f):
        """
        Returns a stream that yields the output of `f` endlessly.

        :param f: A function such that `f() -> T`.

        :Returns: :class:`Stream`

        :Example:
        >>> got = Stream().repeat_with(lambda: 1).take(5).collect()
        >>> assert got == [1, 1, 1, 1, 1]

        A call to `repeat` wipes out any previous step in the iterator.

        :Example:
        >>> # The initial range, enumeration, and chain are completely lost
        >>> # and the stream returns 1 indefinitely.
        >>> s = Stream(range(10)).enumerate().chain(range(10, 20)).repeat_with(lambda: 1)

        Unless a limiting step, such as :meth:`Stream.take_while` or :meth:`Stream.take`, has been setup after
        a call to `repeat`, the consumers :meth:`Stream.collect` and :meth:`Stream.count`
        will throw an :class:`errors.InfiniteCollectionError`.

        :Example:
        >>> try:
        ...     Stream().repeat_with(lambda: 1).collect()
        ... except InfiniteCollectionError as error:
        ...     print(error)
        Stream.collect was called on an infinitely repeating iterator. If you use Stream.repeat, then you MUST include either a Stream.take or a Stream.take_while if you wish to call Stream.collect
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


if __name__ == "__main__":  # pragma: no cover
    import doctest
    doctest.testmod()
