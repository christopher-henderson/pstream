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

import asyncio
import hashlib
import unittest

from builtins import zip as builtin_zip
from functools import wraps

from pstream import AsyncStream
from pstream.errors import InfiniteCollectionError, NotCallableError


def run_to_completion(f):
    @wraps(f)
    def wrapper(self):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(f(self))
        loop.close()

    return wrapper


def async_lambda(f):
    @wraps(f)
    async def inner(*args, **kwargs):
        await asyncio.sleep(0.01)
        return f(*args, *kwargs)

    return inner


class TestAsyncAsyncStream(unittest.TestCase):

    @run_to_completion
    async def test_from_iterator(self):
        got = await AsyncStream((_ for _ in range(10))).collect()
        self.assertEqual(got, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    @run_to_completion
    async def test_value_error(self):
        try:
            AsyncStream(1)
        except ValueError:
            pass

    @run_to_completion
    async def test_empty(self):
        self.assertEqual(await AsyncStream([]).collect(), [])
        self.assertEqual(await AsyncStream().collect(), [])

    @run_to_completion
    async def test_single(self):
        self.assertEqual(await AsyncStream([1]).collect(), [1])

    @run_to_completion
    async def test_chain_single(self):
        self.assertEqual(await AsyncStream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect(),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9])

    @run_to_completion
    async def test_chain_empty(self):
        self.assertEqual(await AsyncStream([1, 2, 3]).chain([]).collect(), [1, 2, 3])

    @run_to_completion
    async def test_chain_multiple(self):
        self.assertEqual(await AsyncStream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect(),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9])

    @run_to_completion
    async def test_chain_repeated_call(self):
        self.assertEqual(await AsyncStream([1, 2, 3]).chain([4, 5, 6]).chain([7, 8, 9]).collect(),
                         [1, 2, 3, 4, 5, 6, 7, 8, 9])

    @run_to_completion
    async def test_count(self):
        self.assertEqual(await AsyncStream([1, 2, 3]).count(), 3)

    @run_to_completion
    async def test_count_empty(self):
        self.assertEqual(await AsyncStream().count(), 0)

    @run_to_completion
    async def test_count_filtered(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).filter(lambda x: x % 2 == 0).count(), 2)

    @run_to_completion
    async def test_count_filtered_a(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).filter(async_lambda(lambda x: x % 2 == 0)).count(), 2)

    @run_to_completion
    async def test_distinct(self):
        self.assertEqual(await AsyncStream([1, 2, 2, 3, 2, 1, 4, 5, 6, 1]).distinct().collect(), [1, 2, 3, 4, 5, 6])

    @run_to_completion
    async def test_distinct_with(self):
        def fingerprint(name):
            return hashlib.sha256(name.encode('utf-8')).digest()
        people = ['Bob', 'Alice', 'Eve', 'Alice', 'Alice', 'Eve', 'Achmed']
        got = await AsyncStream(people).distinct_with(fingerprint).collect()
        self.assertEqual(got, ['Bob', 'Alice', 'Eve', 'Achmed'])

    @run_to_completion
    async def test_distinct_with_a(self):
        def fingerprint(name):
            return hashlib.sha256(name.encode('utf-8')).digest()
        people = ['Bob', 'Alice', 'Eve', 'Alice', 'Alice', 'Eve', 'Achmed']
        got = await AsyncStream(people).distinct_with(async_lambda(fingerprint)).collect()
        self.assertEqual(got, ['Bob', 'Alice', 'Eve', 'Achmed'])

    @run_to_completion
    async def test_enumerate(self):
        self.assertEqual(await AsyncStream([0, 1, 2]).enumerate().collect(), [(0, 0), (1, 1), (2, 2)])

    @run_to_completion
    async def test_enumerate_empty(self):
        self.assertEqual(await AsyncStream([]).enumerate().collect(), [])

    @run_to_completion
    async def test_filter(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).filter(lambda x: x % 2 == 0).collect(), [2, 4])

    @run_to_completion
    async def test_filter_empty(self):
        self.assertEqual(await AsyncStream([]).filter(lambda x: x % 2 == 0).collect(), [])

    @run_to_completion
    async def test_filter_async(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).filter(async_lambda(lambda x: x % 2 == 0)).collect(), [2, 4])

    @run_to_completion
    async def test_filter_empty_async(self):
        self.assertEqual(await AsyncStream([]).filter(async_lambda(lambda x: x % 2 == 0)).collect(), [])

    @run_to_completion
    async def test_flatten(self):
        self.assertEqual(await AsyncStream([[1, 2, 3], [4, 5, 6]]).flatten().collect(), [1, 2, 3, 4, 5, 6])

    @run_to_completion
    async def test_flatten2(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).map(lambda x: [x]).flatten().collect(), [1, 2, 3, 4])

    @run_to_completion
    async def test_flatten_empty_left(self):
        self.assertEqual(await AsyncStream([[], [4, 5, 6]]).flatten().collect(), [4, 5, 6])

    @run_to_completion
    async def test_flatten_empty_right(self):
        self.assertEqual(await AsyncStream([[1, 2, 3], []]).flatten().collect(), [1, 2, 3])

    @run_to_completion
    async def test_flatten_three_dimensional(self):
        arr = [[[1, 2, 3]], [[4, 5, 6]]]
        want = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(await AsyncStream(arr).flatten().collect(), want)

    @run_to_completion
    async def test_flatten_three_to_one(self):
        three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        got = await AsyncStream(three_dimensional).flatten().flatten().collect()
        self.assertEqual(got, [1, 2, 3, 4, 5, 6])

    class Inspector(object):
        def __init__(self):
            self.copy = list()

        def visit(self, item):
            self.copy.append(item)

    @run_to_completion
    async def test_for_each(self):
        class Counter:
            def __init__(self):
                self.count = 0

            def increment(self, element):
                self.count += element

        count = Counter()
        await AsyncStream([1, 2, 3, 4, 5]).for_each(count.increment)
        self.assertEqual(count.count, 15)

    @run_to_completion
    async def test_for_each_empty(self):
        class Called:
            def __init__(self):
                self.called = False

            def __call__(self, _):
                self.called = True

        called = Called()
        await AsyncStream().for_each(called)
        self.assertFalse(called.called)

    @run_to_completion
    async def test_for_each_a(self):
        class Counter:
            def __init__(self):
                self.count = 0

            def increment(self, element):
                self.count += element

        count = Counter()
        await AsyncStream([1, 2, 3, 4, 5]).for_each(async_lambda(count.increment))
        self.assertEqual(count.count, 15)

    @run_to_completion
    async def test_for_each_empty_a(self):
        class Called:
            def __init__(self):
                self.called = False

            def __call__(self, _):
                self.called = True

        called = Called()
        await AsyncStream().for_each(async_lambda(called))
        self.assertFalse(called.called)

    @run_to_completion
    async def test_inspect(self):
        inspector = self.Inspector()
        got = await AsyncStream([1, 2, 3, 4]).filter(lambda x: x % 2 == 0).inspect(inspector.visit).collect()
        self.assertEqual(got, inspector.copy)

    @run_to_completion
    async def test_inspect_then(self):
        inspector = self.Inspector()
        got = await AsyncStream([1, 2, 3, 4]).filter(lambda x: x % 2 == 0).inspect(inspector.visit).map(
            lambda x: x * 2).collect()
        self.assertEqual([2, 4], inspector.copy)
        self.assertEqual(got, [4, 8])

    @run_to_completion
    async def test_inspect_a(self):
        inspector = self.Inspector()
        got = await AsyncStream([1, 2, 3, 4]).filter(async_lambda(lambda x: x % 2 == 0)).inspect(
            async_lambda(inspector.visit)).collect()
        self.assertEqual(got, inspector.copy)

    @run_to_completion
    async def test_inspect_then_a(self):
        inspector = self.Inspector()
        got = await AsyncStream([1, 2, 3, 4]).filter(async_lambda(lambda x: x % 2 == 0)).inspect(
            async_lambda(inspector.visit)).map(async_lambda(lambda x: x * 2)).collect()
        self.assertEqual([2, 4], inspector.copy)
        self.assertEqual(got, [4, 8])

    @run_to_completion
    async def test_map(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).map(lambda x: x * 2).collect(), [2, 4, 6, 8])

    @run_to_completion
    async def test_map_empty(self):
        self.assertEqual(await AsyncStream([]).map(lambda x: x * 2).collect(), [])

    @run_to_completion
    async def test_map_async(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).map(async_lambda(lambda x: x * 2)).collect(), [2, 4, 6, 8])

    @run_to_completion
    async def test_map_empty_async(self):
        self.assertEqual(await AsyncStream([]).map(async_lambda(lambda x: x * 2)).collect(), [])

    @run_to_completion
    async def test_next(self):
        s = AsyncStream([1, 2, 3, 4, 5]).map(lambda x: x * 2)
        for i in range(1, 4):
            self.assertEqual(await s.__anext__(), i * 2)
        self.assertEqual(await s.collect(), [8, 10])

    @run_to_completion
    async def test_pool_even_even(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).pool(2).collect(), [[1, 2], [3, 4]])

    @run_to_completion
    async def test_pool_odd_even(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5]).pool(2).collect(), [[1, 2], [3, 4], [5]])

    @run_to_completion
    async def test_pool_even_odd(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).pool(3).collect(), [[1, 2, 3], [4]])

    @run_to_completion
    async def test_pool_odd_odd(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5]).pool(3).collect(), [[1, 2, 3], [4, 5]])

    @run_to_completion
    async def test_pool_empty(self):
        self.assertEqual(await AsyncStream([]).pool(5).collect(), [])

    @run_to_completion
    async def test_pool_single(self):
        self.assertEqual(await AsyncStream([1]).pool(5).collect(), [[1]])

    @run_to_completion
    async def test_pool_value_error(self):
        try:
            AsyncStream().pool(0)
        except ValueError:
            return
        raise Exception()

    @run_to_completion
    async def test_reduce(self):
        def add(a, b):
            return a + b
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = await AsyncStream(numbers).reduce(add, 0)
        assert got == 45

    @run_to_completion
    async def test_reduce_a(self):
        def add(a, b):
            return a + b
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = await AsyncStream(numbers).reduce(async_lambda(add), 0)
        assert got == 45

    @run_to_completion
    async def test_repeat(self):
        s = AsyncStream().repeat(5)
        for _ in range(100):
            self.assertEqual(await s.__anext__(), 5)

    @run_to_completion
    async def test_repeat_break_up(self):
        s = AsyncStream([1, 2, 3]).repeat(5)
        for _ in range(100):
            self.assertEqual(await s.__anext__(), 5)

    @run_to_completion
    async def test_repeat_terminator(self):
        self.assertEqual(await AsyncStream().repeat(5).take(5).collect(), [5, 5, 5, 5, 5])

    @run_to_completion
    async def test_repeat_collection(self):
        try:
            await AsyncStream().repeat(1).collect()
        except InfiniteCollectionError:
            pass

    @run_to_completion
    async def test_repeat_count(self):
        try:
            await AsyncStream().repeat(1).count()
        except InfiniteCollectionError:
            pass

    @run_to_completion
    async def test_repeat_take_flatten(self):
        self.assertEqual(await AsyncStream().repeat([1, 2, 3, 4]).take(1).flatten().collect(), [1, 2, 3, 4])

    @run_to_completion
    async def test_reverse(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4]).reverse().collect(), [4, 3, 2, 1])

    @run_to_completion
    async def test_skip(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).skip(4).collect(), [5, 6, 7, 8, 9])

    @run_to_completion
    async def test_skip_while(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).skip_while(lambda x: x < 5).collect(),
                         [5, 6, 7, 8, 9])

    @run_to_completion
    async def test_skip_while_async(self):
        self.assertEqual(
            await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).skip_while(async_lambda(lambda x: x < 5)).collect(),
            [5, 6, 7, 8, 9])

    @run_to_completion
    async def test_sort(self):
        arr = [12, 233, 4567, 344523, 7, 567, 34, 5678, 456, 23, 4, 7, 63, 45, 345]
        got = await AsyncStream(arr).sort().collect()
        self.assertEqual(got, [4, 7, 7, 12, 23, 34, 45, 63, 233, 345, 456, 567, 4567, 5678, 344523])

    @run_to_completion
    async def test_sort_complex(self):
        # sort and reverse incur collections, and sort itself returns a physical list rather than
        # and iterator, so this == just a bit of whacking around to smoke test the interactions
        # between the pipelines.
        arr = [12, 233, 4567, 344523, 7, 567, 34, 5678, 456, 23, 4, 7, 63, 45, 345]
        got = await AsyncStream(arr).\
            filter(lambda x: x % 2).\
            sort().\
            reverse().\
            filter(lambda x: x < 1000).\
            distinct().\
            collect()
        self.assertEqual(got, [567, 345, 233, 63, 45, 23, 7])

    @run_to_completion
    async def test_step_by_even(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).step_by(4).collect(), [1, 5, 9])

    @run_to_completion
    async def test_step_by_odd(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).step_by(3).collect(), [1, 4, 7])

    @run_to_completion
    async def test_step_by_too_few(self):
        self.assertEqual(await AsyncStream([1, 2, 3]).step_by(3).collect(), [1])

    @run_to_completion
    async def test_step_by_one(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5]).step_by(1).collect(), [1, 2, 3, 4, 5])

    @run_to_completion
    async def test_step_by_value_error(self):
        try:
            AsyncStream([1, 2, 3, 4, 5]).step_by(0)
        except ValueError:
            return
        raise Exception("did not raise value error")

    @run_to_completion
    async def test_step_single(self):
        self.assertEqual(await AsyncStream([1]).step_by(3).collect(), [1])

    @run_to_completion
    async def test_step_empty(self):
        self.assertEqual(await AsyncStream([]).step_by(3).collect(), [])

    @run_to_completion
    async def test_take(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).take(4).collect(), [1, 2, 3, 4])

    @run_to_completion
    async def test_take_more_than_there_are(self):
        self.assertEqual(await AsyncStream([1, 2]).take(4).collect(), [1, 2])

    @run_to_completion
    async def test_take_while(self):
        self.assertEqual(await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).take_while(lambda x: x < 5).collect(),
                         [1, 2, 3, 4])

    @run_to_completion
    async def test_take_while_async(self):
        self.assertEqual(
            await AsyncStream([1, 2, 3, 4, 5, 6, 7, 8, 9]).take_while(async_lambda(lambda x: x < 5)).collect(),
            [1, 2, 3, 4])

    @run_to_completion
    async def test_tee(self):
        a = list()
        b = list()
        got = await AsyncStream([1, 2, 3, 4]).tee(a, b).map(lambda x: x * 2).collect()
        self.assertEqual(got, [2, 4, 6, 8])
        self.assertEqual(a, [1, 2, 3, 4])
        self.assertEqual(b, [1, 2, 3, 4])

    @run_to_completion
    async def test_tee_a(self):
        class Alist(list):
            async def append(self, obj) -> None:
                await asyncio.sleep(0.001)
                super(Alist, self).append(obj)
        a = list()
        b = Alist()
        got = await AsyncStream([1, 2, 3, 4]).tee(a, b).map(async_lambda(lambda x: x * 2)).collect()
        self.assertEqual(got, [2, 4, 6, 8])
        self.assertEqual(a, [1, 2, 3, 4])
        self.assertEqual(b, [1, 2, 3, 4])

    @run_to_completion
    async def test_zip(self):
        data = ((0, 1, 2), (3, 4, 5))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_sizes_left(self):
        data = ((0, 1), (3, 4, 5))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_sizes_right(self):
        data = ((0, 1, 2), (3, 4))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_empty_left(self):
        data = ((), (3, 4, 5))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_empty_right(self):
        data = ((0, 1, 2), ())
        self.assertEqual(await AsyncStream(data[0]).zip(data[1]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_empty_far_right(self):
        data = ((0, 1, 2), (3, 4, 5), ())
        self.assertEqual(await AsyncStream(data[0]).zip(data[1], data[2]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_single_far_right(self):
        data = ((0, 1, 2), (3, 4, 5), (6,))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1], data[2]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_empty_far_left(self):
        data = ((), (3, 4, 5), (6, 7, 8))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1], data[2]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_single_far_left(self):
        data = ((0,), (3, 4, 5), (6, 7, 8))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1], data[2]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_empty_middle(self):
        data = ((0, 1, 2), (), (6, 7, 8))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1], data[2]).collect(), [_ for _ in builtin_zip(*data)])

    @run_to_completion
    async def test_zip_different_single_middle(self):
        data = ((0, 1, 2), (3,), (6, 7, 8))
        self.assertEqual(await AsyncStream(data[0]).zip(data[1], data[2]).collect(), [_ for _ in builtin_zip(*data)])


if __name__ == '__main__':
    unittest.main()
