import unittest

from pstream import AsyncStream
from pstream._async.functors import for_each
from tests._async.utils import AF, run_to_completion


class TestInternals(unittest.TestCase):

    def test_bad_function(self):
        try:
            for_each(1, [1, 2])
        except TypeError:
            pass

    def test_bad_stream(self):
        try:
            for_each(AF(lambda x: x), 1)
        except TypeError:
            pass

    def test_none_constructor(self):
        AsyncStream()

    @run_to_completion
    async def test_for_each(self):
        got = list()
        await AsyncStream(range(10)).for_each(lambda x: got.append(x))
        self.assertEqual(got, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])


if __name__ == '__main__':
    unittest.main()
