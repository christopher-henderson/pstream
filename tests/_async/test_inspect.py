import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Inspect(Method):

    def __init__(self, args):
        super(Inspect, self).__init__(AsyncStream.inspect, args)


class TestInspect(unittest.TestCase):

    @Driver(initial=range(10), method=Inspect(args=[lambda x: x % 2]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Inspect(args=[lambda x: x % 2]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Inspect(args=[lambda x: x % 2]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Inspect(args=[lambda x: x % 2]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
