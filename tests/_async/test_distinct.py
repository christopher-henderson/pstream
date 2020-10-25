import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Distinct(Method):

    def __init__(self, args):
        super(Distinct, self).__init__(AsyncStream.distinct, args)


class TestDistinct(unittest.TestCase):

    @Driver(initial=[1, 2, 1, 3, 2, 0, 5], method=Distinct(args=[]), want=[1, 2, 3, 0, 5])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 1, 3, 2, 0, 5], method=Distinct(args=[]), want=[1, 2, 3, 0, 5])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(0), method=Distinct(args=[]), want=[])
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(0), method=Distinct(args=[]), want=[])
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
