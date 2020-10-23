import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Skip(Method):

    def __init__(self, args):
        super(Skip, self).__init__(AsyncStream.skip, args)


class TestSkip(unittest.TestCase):

    @Driver(initial=range(10), method=Skip(args=[5]), want=[5, 6, 7, 8, 9])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Skip(args=[5]), want=[5, 6, 7, 8, 9])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=Skip(args=[10]), want=[])
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Skip(args=[10]), want=[])
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=[], method=Skip(args=[1]), want=[])
    def test2__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Skip(args=[1]), want=[])
    def test2__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=Skip(args=[0]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test3__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Skip(args=[0]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test3__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
