import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Take(Method):

    def __init__(self, args):
        super(Take, self).__init__(AsyncStream.take, args)


class TestTake(unittest.TestCase):

    @Driver(initial=range(10), method=Take(args=[5]), want=[0, 1, 2, 3, 4])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Take(args=[5]), want=[0, 1, 2, 3, 4])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=Take(args=[10]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Take(args=[10]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=[], method=Take(args=[1]), want=[])
    def test2__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Take(args=[1]), want=[])
    def test2__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=Take(args=[0]), want=[])
    def test3__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Take(args=[0]), want=[])
    def test3__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
