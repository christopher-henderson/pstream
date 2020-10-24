import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Sort(Method):

    def __init__(self, args):
        super(Sort, self).__init__(AsyncStream.sort, args)


class TestSort(unittest.TestCase):

    random = [123, 5, 1245, 6, 2, 56, 0, 8, 2, 78, 4, -1]

    @Driver(initial=random, method=Sort(args=[]), want=[-1, 0, 2, 2, 4, 5, 6, 8, 56, 78, 123, 1245])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=random, method=Sort(args=[]), want=[-1, 0, 2, 2, 4, 5, 6, 8, 56, 78, 123, 1245])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(0), method=Sort(args=[]), want=[])
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(0), method=Sort(args=[]), want=[])
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
