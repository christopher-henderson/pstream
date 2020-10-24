import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Reverse(Method):

    def __init__(self, args):
        super(Reverse, self).__init__(AsyncStream.reverse, args)


class TestReverse(unittest.TestCase):

    @Driver(initial=range(10), method=Reverse(args=[]), want=[9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Reverse(args=[]), want=[9, 8, 7, 6, 5, 4, 3, 2, 1, 0])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(0), method=Reverse(args=[]), want=[])
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(0), method=Reverse(args=[]), want=[])
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
