import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Enum(Method):

    def __init__(self, args):
        super(Enum, self).__init__(AsyncStream.enumerate, args)


class TestEnum(unittest.TestCase):

    @Driver(initial=range(5, 10), method=Enum(args=[]), want=[(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5, 10), method=Enum(args=[]), want=[(0, 5), (1, 6), (2, 7), (3, 8), (4, 9)])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(0), method=Enum(args=[]), want=[])
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(0), method=Enum(args=[]), want=[])
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
