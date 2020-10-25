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
from .shim import AsyncShim, shim, async_shim, not_infinite_a, not_infinite_s
from pstream.errors import InfiniteCollectionError
from pstream._async.functors import *

from typing import TypeVar, Generic, List, Collection, Callable

T = TypeVar('T')
U = TypeVar('U')


class AsyncStream(Generic[T]):
    """The API for an AsyncStream has a 1:1 correspondence with the API for a :class:`Stream`.

    The difference is that an AsyncStream may accept asynchronous iterators/iterables
    and asynchronous functions at all opportunities (with the notable exception of :meth:`AsyncStream.sort_with`
    which cannot take in an asynchronous key function).

    However, it is not `mandatory` that the provided iterators and functions be all asynchronous. The two runtime
    characteristics may be mixed and matched. The correct implementation for all combinations is selected at the time
    of `building`the stream, rather than being dispatched during the stream's evaluation. The result is that at the time
    of evaluatiom, each step in your stream is exactly as precise, and as minimal, as you would expect from a
    manual implementation.

    >>> async def consult(element):
    ...     # Ask some remote microservice whether
    ...     # or not the given element is valid.
    ...     asyncio.sleep(1)
    ...     return True
    >>> def double(element):
    ...     return element * 2
    >>> # Mix-and-match async and sync at your leisure.
    >>> await AsyncStream([1, 2, 3, 4]).filter(consult).map(double).collect()
    """

    def __init__(self, initial: Collection[T] = None):
        """
        :param initial: An optional initial value for the stream. `Must` be either an iterator, an iterable, or an
                        asynchronous iterator (supports an `__anext__` method). If `initial` is `None` then the stream
                        with be initialized to be empty.

        :Raises: :class:`ValueError` if `initial` is neither an iterator nor, an iterable, nor an asynchronous iterator.
        """
        if initial is None:
            initial = []
        self.stream = AsyncShim.new(initial)
        self._infinite = False

    @not_infinite_a
    @async_shim
    async def collect(self) -> List[T]:
        """
        Evaluates the stream, consuming it and returning a list of the final output.

        :Returns: :class:`list`

        :Raises: :class:`errors.InfiniteCollectionError`

        :Example:
        >>> stream = AsyncStream([1, 2, 3, 4]).map(lambda x: x * 2)
        >>> got = await stream.collect()
        >>> assert got == [2, 4, 6, 8]
        """
        return await collect(self.stream)

    @shim
    def chain(self, *iterables: Collection[T]):
        """
        Returns a stream that links an arbitrary number of iterators to this iterator, in a chain.

        :param iterables: Zero or more iterable objects. These iterables will be chained to the stream
                            in a left-to-right fashion.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> got = await AsyncStream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect()
        >>> assert got == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        self.stream = chain(self.stream, *iterables)
        return self

    @not_infinite_a
    @async_shim
    async def count(self):
        """
        Evaluates the stream, consuming it and returning a count of the number of elements in the stream.

        :Returns: :class:`int`

        :Raises: :class:`errors.InfiniteCollectionError`

        :Example:
        >>> count = await AsyncStream(range(100)).filter(lambda x: x % 2 is 0).count()
        >>> assert count == 50
        """
        return await count(self.stream)

    @shim
    def distinct(self):
        """
        Returns a stream of distinct elements. Distinction is computed by applying the builtin `hash` function
        to each element. Ordering of elements in the stream is maintained.

        This functor incurs an additional allocation in the form of a hashset in order to keep track of
        the elements in the stream.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 2, 3, 2, 1, 4, 5, 6, 1]
        >>> got = await AsyncStream(numbers).distinct().collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]
        """
        self.stream = distinct(self.stream)
        return self

    @shim
    def distinct_with(self, key: Callable[[T], U]):
        """
        Returns a stream of distinct elements. Distinction is computed by applying the builtin `hash` function
        to each item generated by the provided `key(element)`. Ordering of elements in the stream is maintained.

        This functor incurs an additional allocation in the form of a hashset in order to keep track of
        the elements in the stream.

        :param key: A function such that `key(element) -> T` where `T` must be hashable. `key` may be either
                    asynchronous or synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> import hashlib
        >>>
        >>> people = ['Bob', 'Alice', 'Eve', 'Alice', 'Alice', 'Eve', 'Achmed']
        >>> fingerprinter = lambda x: hashlib.sha256(x.encode('UTF-8')).digest()
        >>> got = await AsyncStream(people).distinct_with(fingerprinter).collect()
        >>> assert got == ['Bob', 'Alice', 'Eve', 'Achmed']
        """
        self.stream = distinct_with(key, self.stream)
        return self

    @shim
    def enumerate(self):
        """
        Returns a stream that yields the current count and the element during iteration.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> got = await AsyncStream(range(1, 10)).enumerate().collect()
        >>> assert got == [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9)]

        The constructed tuple is the namedtuple, :class:`Stream.Enumeration`, which provides
        the names `count` and `element`.

        :Example:
        >>> def count(enumeration):
        ...     print(enumeration.count, enumeration.element)
        >>> got = await AsyncStream(range(1, 5)).enumerate().inspect(count).map(lambda e: e.element).collect()
        0 1
        1 2
        2 3
        3 4
        >>> assert got == [1, 2, 3, 4]
        """
        self.stream = enumerate(self.stream)
        return self

    @shim
    def flatten(self):
        """
        Returns a stream that flattens one level of nesting in a stream of elements that are themselves iterators.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> # Flatten a two dimensional array to a one dimensional array.
        >>> two_dimensional = [[1, 2, 3], [4, 5, 6]]
        >>> got = await AsyncStream(two_dimensional).flatten().collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]

        >>> # Flatten a three dimensional array to a two dimensional array.
        >>> three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        >>> got = await AsyncStream(three_dimensional).flatten().collect()
        >>> assert got == [[1, 2, 3], [4, 5, 6]]

        >>> # Flatten a three dimensional array to a one dimensional array.
        >>> three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        >>> got = await AsyncStream(three_dimensional).flatten().flatten().collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]
        """
        self.stream = flatten(self.stream)
        return self

    @shim
    def filter(self, predicate: Callable[[T], bool]):
        """
        Returns a stream that filters each element using `predicate`. Only elements for which `predicate`
        returns `True` are passed through the stream.

        :param predicate: A function such that `predicate(element) -> bool`. `predicate` may be either asynchronous or
                            synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> odds = lambda x: x % 2 != 0
        >>> got = await AsyncStream(numbers).filter(odds).collect()
        >>> assert got == [1, 3, 5, 7, 9]
        """
        self.stream = filter(predicate, self.stream)
        return self

    @shim
    def filter_false(self, predicate: Callable[[T], bool]):
        """
        Returns a stream that filters each element using `predicate`. Only elements for which `predicate`
        returns `False` are passed through the stream.

        :param predicate: A function such that `predicate(element) -> bool`. `predicate` may be either asynchronous or
                            synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> odds = lambda x: x % 2 != 0
        >>> got = await AsyncStream(numbers).filter_false(odds).collect()
        >>> assert got == [2, 4, 6, 8]
        """
        self.stream = filter_false(predicate, self.stream)
        return self

    @not_infinite_a
    @async_shim
    async def for_each(self, f: Callable[[T], None]):
        """
        Evaluates the stream, consuming it and calling `f` for each element in the stream.

        Note that while other stream consumers, such as :meth:`Stream.collect` and :meth:`Stream.count`, will raise an
        an :class:`errors.InfiniteCollectionError` if called on an infinite stream (see the documentation
        regarding :meth:`Stream.repeat` and :meth:`Stream.repeat_with`), `for_each` will not.

        This makes the following...

        >>> await AsyncStream().repeat_with(input).for_each(print)  # doctest: +SKIP

        ...roughly equivalent to:

        >>> while True:  # doctest: +SKIP
        ...   print(input())  # doctest: +SKIP

        :param f: A function such that `f(element)`. Any value returned is ignored. `f` may be either asynchronous or
                    synchronous.

        :Example:
        >>> await AsyncStream(range(1, 5)).for_each(print)
        1
        2
        3
        4
        """
        await for_each(f, self.stream)

    @not_infinite_s
    @shim
    def group_by(self, key: Callable[[T], U]):
        """
        Returns a stream that groups elements together using the provided `key` function.

        The ordering of the groups is non-deterministic.

        :param key: A function such that `f(element) -> T` where `T` will be used to group elements together. `key`
                    may be either asynchronous or synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> # Group people by how long their names are.
        >>> names = ['Alice', 'Bob', 'Eve', 'Chris', 'Arjuna', 'Zack']
        >>> got = await AsyncStream(names).group_by(len).collect()
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
        >>> got = await AsyncStream(range(10)).group_by(lambda x: x % 2).collect()
        >>> len(got) == 2
        True
        >>> [1, 3, 5, 7, 9] in got
        True
        >>> [0, 2, 4, 6, 8] in got
        True
        """
        self.stream = group_by(key, self.stream)
        return self

    @shim
    def inspect(self, f: Callable[[T], None]):
        """
        Returns a stream that calls the function, `f`, with a reference to each element before yielding it.

        :param f: A function such that `f(element)`. Any value returned is ignored. `f` may be either asynchronous or
                            synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> def log(number):
        ...     if number % 2 != 0:
        ...         print("WARNING: {} is not even!".format(number))
        >>>
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).inspect(log).collect()
        WARNING: 1 is not even!
        WARNING: 3 is not even!
        WARNING: 5 is not even!
        WARNING: 7 is not even!
        WARNING: 9 is not even!
        >>> assert got == [1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        self.stream = inspect(f, self.stream)
        return self

    @shim
    def map(self, f: Callable[[T], U]):
        """
        Returns a stream that maps each value using `f`.

        :param f: A function such that `f(A) -> B`. `f` may be either asynchronous or synchronous.

        :Returns: :class:`AsyncStream`

        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> double = lambda x: x * 2
        >>> got = await AsyncStream(numbers).map(double).collect()
        >>> assert got == [2, 4, 6, 8, 10, 12, 14, 16, 18]
        """
        self.stream = map(f, self.stream)
        return self

    @shim
    def pool(self, size: int):
        """
        Returns a stream that will collect up to `size` elements into a list before yielding.

        :param size: :class:`int`. `Must` be greater than 0.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> got = await AsyncStream([1, 2, 3, 4, 5]).pool(3).collect()
        >>> assert got == [[1, 2, 3], [4, 5]]

        Note that `pool` effectively behaves as the inverse to :meth:`Stream.flatten` by gradually
        introducing higher levels of dimensionality.

        :Example:
        >>> one = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> two = await AsyncStream(one).pool(2).collect()
        >>> assert two == [[1, 2], [3, 4], [5, 6], [7, 8]]
        >>> three = await AsyncStream(two).pool(2).collect()
        >>> assert three == [[[1, 2], [3, 4]], [[5, 6], [7, 8]]]
        """
        if size <= 0:
            raise ValueError("pstream.AsyncStream.pool sizes must be greater than 0. Received {}.".format(size))
        self.stream = pool(self.stream, size)
        return self

    @shim
    def skip(self, n: int):
        """
        Returns a stream that skips over `n` number of elements.

        :param n: :class:`int`

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).skip(3).collect()
        >>> assert got == [4, 5, 6, 7, 8, 9]
        """
        self.stream = skip(self.stream, n)
        return self

    @shim
    def skip_while(self, predicate: Callable[[T], bool]):
        """
        Returns a stream that rejects elements while `predicate` returns `True`.

        `skip_while` is the complement to :meth:`AsyncStream.take_while`.

        :param predicate: A function such that `f(element) -> bool`. `predicate` may be either asynchronous or synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).skip_while(lambda x: x < 5).collect()
        >>> assert got == [5, 6, 7, 8, 9]
        """
        self.stream = skip_while(predicate, self.stream)
        return self

    @not_infinite_s
    @shim
    def sort(self):
        """
        Returns a stream whose elements are sorted.

        Note that calling `sort` itself remains lazy, however at time of collecting the stream a sort
        will incur an internal collection at that particular step.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> arr = [12, 233, 4567, 344523, 7, 567, 34, 5678, 456, 23, 4, 7, 63, 45, 345]
        >>> got = await AsyncStream(arr).sort().collect()
        >>> assert got == [4, 7, 7, 12, 23, 34, 45, 63, 233, 345, 456, 567, 4567, 5678, 344523]
        """
        self.stream = sort(self.stream)
        return self

    @not_infinite_s
    @shim
    def sort_with(self, key: Callable[[T], U]):
        """
        Returns a stream whose elements are sorted using the provided key selection function.

        Note that calling `sort_with` itself remains lazy, however at time of collecting the stream a sort
        will incur an internal collection at that particular step.

        :param key: A function such that `key(element) -> T` where `T` is the type used for comparison. `key` MAY NOT
        be asynchronous! This is due to a limitation in the builtin `sorted` function which does not support
        asynchronous key functions.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> arr = ['12', '233', '4567', '344523', '7', '567', '34', '5678', '456', '23', '4', '7', '63', '45', '345']
        >>> got = await AsyncStream(arr).sort_with(len).collect()
        >>> assert got == ['7', '4', '7', '12', '34', '23', '63', '45', '233', '567', '456', '345', '4567', '5678', '344523']
        """
        self.stream = sort_with(key, self.stream)
        return self

    @shim
    def step_by(self, step: int):
        """
        Returns a stream which steps over items by a custom amount. Regardless of the step, the first item
        in the stream is always returned.

        :param step: :class:`int`. `Must` be greater than or equal to one.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).step_by(3).collect()
        >>> assert got == [1, 4, 7]
        """
        if step == 1:
            return self
        if step < 1:
            raise ValueError("step_by must be a positive integer, received {}".format(step))
        self.stream = step_by(self.stream, step)
        return self

    @not_infinite_s
    @async_shim
    async def reduce(self, f: Callable[[T], U], accumulator: U) -> U:
        """
        Evaluates the stream, consuming it and applying the function `f` to each item in the stream,
        producing a single value.

        After `f` has been applied to every item in the stream, the updated `accumulator` is returned.

        :param f: A function such that `f(accumulator: T, element) -> T`. `f` may be either asynchronous or synchronous.
        :param accumulator: The initial value provided to `f`.

        :Returns: `T` such that `f(accumulator: T, element) -> T`.

        Example:

        >>> def stringify(accumulator, element):
        ...    return accumulator + str(element)
        >>>
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).reduce(stringify, '')
        >>> assert got == '123456789'
        """
        return await reduce(f, self.stream, accumulator)

    @shim
    def repeat(self, element: T):
        """
        Returns a stream that repeats an element endlessly.

        :param element: Any object. This exact object will be yieled repeatedly.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> got = await AsyncStream().repeat(1).take(5).collect()
        >>> assert got == [1, 1, 1, 1, 1]

        A call to `repeat` wipes out any previous step in the iterator.

        :Example:
        >>> # The initial range, enumeration, and chain are completely lost
        >>> # and the stream returns 1 indefinitely.
        >>> s = await AsyncStream(range(10)).enumerate().chain(range(10, 20)).repeat(1)

        Unless a limiting step, such as :meth:`AsyncStream.take_while` or :meth:`AsyncStream.take`, has been setup after
        a call to `repeat`, the consumers :meth:`AsyncStream.collect` and :meth:`AsyncStream.count`
        will throw an :class:`errors.InfiniteCollectionError`.

        :Example:
        >>> try:
        ...     await AsyncStream().repeat(1).collect()
        ... except InfiniteCollectionError as error:
        ...     print(error)
        AsyncStream.collect was called on an infinitely repeating iterator. If you use Stream.repeat, then you MUST include either a Stream.take or a Stream.take_while if you wish to call Stream.collect
        """
        self.stream = repeat(element)
        self._infinite = True
        return self

    @shim
    def repeat_with(self, f: Callable[[], T]):
        """
        Returns a stream that yields the output of `f` endlessly.

        :param f: A function such that `f() -> T`. `f` may be either asynchronous or synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> got = await AsyncStream().repeat_with(lambda: 1).take(5).collect()
        >>> assert got == [1, 1, 1, 1, 1]

        A call to `repeat` wipes out any previous step in the iterator.

        :Example:
        >>> # The initial range, enumeration, and chain are completely lost
        >>> # and the stream returns 1 indefinitely.
        >>> s = await AsyncStream(range(10)).enumerate().chain(range(10, 20)).repeat_with(lambda: 1)

        Unless a limiting step, such as :meth:`AsyncStream.take_while` or :meth:`AsyncStream.take`, has been setup after
        a call to `repeat`, the consumers :meth:`AsyncStream.collect` and :meth:`AsyncStream.count`
        will throw an :class:`errors.InfiniteCollectionError`.

        :Example:
        >>> try:
        ...     await AsyncStream().repeat_with(lambda: 1).collect()
        ... except InfiniteCollectionError as error:
        ...     print(error)
        AsyncStream.collect was called on an infinitely repeating iterator. If you use Stream.repeat, then you MUST include either a Stream.take or a Stream.take_while if you wish to call Stream.collect
        """
        self.stream = repeat_with(f)
        self._infinite = True
        return self

    @not_infinite_s
    @shim
    def reverse(self):
        """
        Returns a stream whose elements are reversed.

        Note that calling `reverse` itself remains lazy, however at time of collecting the stream a reversal
        will incur an internal collection at that particular step. This is due to the reliance of Python's builtin
        `reversed` function which itself requires an object that is indexable.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).reverse().collect()
        >>> assert got == [9, 8, 7, 6, 5, 4, 3, 2, 1]
        """
        self.stream = reverse(self.stream)
        return self

    @shim
    def take(self, n: int):
        """
        Returns a stream that only iterates over the first `n` elements.

        :param n: :class:`int`

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).take(6).collect()
        >>> assert got == [1, 2, 3, 4, 5, 6]
        """
        self.stream = take(self.stream, n)
        self._infinite = False
        return self

    @shim
    def take_while(self, predicate: Callable[[T], bool]):
        """
        Returns a stream that only accepts elements while `predicate` returns `True`.

        `take_while` is the complement to :meth:`AsyncStream.skip_while`.

        :param predicate: A function such that `predicate(element) -> bool`. `predicate` may be either asynchronous or
                            synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> got = await AsyncStream(numbers).take_while(lambda x: x < 5).collect()
        >>> assert got == [1, 2, 3, 4]
        """
        self.stream = take_while(predicate, self.stream)
        self._infinite = False
        return self

    @shim
    def tee(self, *receivers):
        """
        Returns a stream whose elements will be appended to objects in `receivers`.

        `tee` behaves similarly to the `Unix tee command <https://man7.org/linux/man-pages/man1/tee.1.html>`_.

        :param receivers: Zero or more objects that `must` support an `append` method. The `append` method may be
                            either asynchronous or synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> a = list()
        >>> b = list()
        >>> got = await AsyncStream([1, 2, 3, 4]).tee(a, b).map(lambda x: x * 2).collect()
        >>> assert got == [2, 4, 6 ,8]
        >>> assert a == [1, 2, 3, 4]
        >>> assert b == [1, 2, 3, 4]
        """
        for other in receivers:
            self.stream = inspect(other.append, self.stream)
        return self

    @shim
    def zip(self, *iterables: Collection[T]):
        """
        Returns a stream that iterates over one or more iterators simultaneously.

        :param iterables: Zero or more iterable objects. The iterables may be heterogeneous of either asynchronous or
                            synchronous.

        :Returns: :class:`AsyncStream`

        :Example:
        >>> got = Stream([0, 1, 2]).zip([3, 4, 5]).collect()
        >>> assert got == [(0, 3), (1, 4), (2, 5)]
        """
        self.stream = zip(self.stream, *iterables)
        return self

    def __aiter__(self):
        return self

    async def __anext__(self):
        return await self.stream.__anext__()
