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

import unittest

from pstream import AsyncStream
from pstream._async.functors import binary_function_stream_factory
from pstream._async.shim import AsyncShim
from tests._async.utils import run_to_completion
from tests.sync.test_stream import expect


class TestShim(unittest.TestCase):
    class AsyncIterable:

        def __init__(self, iterator):
            self.iterator = iterator

        def __aiter__(self):
            iterator = self.iterator

            async def inner():
                for x in iterator:
                    yield x

            return inner()

    class Iterable:
        def __init__(self, iterator):
            self.iterator = iterator

        def __iter__(self):
            iterator = self.iterator

            def inner():
                for x in iterator:
                    yield x

            return inner()

    @run_to_completion
    async def test_async_iterable(self):
        stream = AsyncStream(TestShim.AsyncIterable(range(10)))
        self.assertFalse(isinstance(stream.stream, AsyncShim))
        got = await stream.filter(lambda x: x % 2).collect()
        self.assertEqual(got, [1, 3, 5, 7, 9])

    @run_to_completion
    async def test_iterable(self):
        stream = AsyncStream(TestShim.Iterable(range(10)))
        self.assertTrue(isinstance(stream.stream, AsyncShim))
        got = await stream.filter(lambda x: x % 2).collect()
        self.assertEqual(got, [1, 3, 5, 7, 9])

    @run_to_completion
    async def test_shim_iterable(self):
        stream = AsyncShim(TestShim.Iterable(range(10)))
        i = 0
        async for x in stream:
            self.assertEqual(x, i)
            i += 1

    @run_to_completion
    async def test_async_iterator(self):
        stream = AsyncStream(TestShim.AsyncIterable(range(10)).__aiter__())
        self.assertFalse(isinstance(stream.stream, AsyncShim))
        got = await stream.filter(lambda x: x % 2).collect()
        self.assertEqual(got, [1, 3, 5, 7, 9])

    @run_to_completion
    async def test_iterator(self):
        stream = AsyncStream(TestShim.Iterable(range(10)).__iter__())
        self.assertTrue(isinstance(stream.stream, AsyncShim))
        got = await stream.filter(lambda x: x % 2).collect()
        self.assertEqual(got, [1, 3, 5, 7, 9])

    @expect(TypeError)
    def test_value_error(self):
        AsyncShim(1)

    @expect(TypeError)
    def test_factory_value_error(self):
        AsyncShim.new(1)

    @expect(TypeError)
    def test_factory_error(self):
        binary_function_stream_factory(1, 2, 3, 4)(1, 2)
