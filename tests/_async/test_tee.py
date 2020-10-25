import unittest

from pstream import AsyncStream
from tests._async.utils import run_to_completion


class TestTee(unittest.TestCase):

    @run_to_completion
    async def test_tee(self):
        a = list()
        b = list()
        got = await AsyncStream(range(5)).map(lambda x: x * 2).tee(a, b).collect()
        self.assertEqual(got, a)
        self.assertEqual(got, b)


if __name__ == '__main__':
    unittest.main()
