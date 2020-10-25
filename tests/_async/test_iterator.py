import unittest

from pstream import AsyncStream
from tests._async.utils import run_to_completion


class TestIteraor(unittest.TestCase):

    @run_to_completion
    async def test_tee(self):
        i = 0
        async for x in AsyncStream(range(5)).__aiter__():
            self.assertEqual(x, i)
            i += 1


if __name__ == '__main__':
    unittest.main()
