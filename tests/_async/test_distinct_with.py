import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class DistinctWith(Method):

    def __init__(self, args):
        super(DistinctWith, self).__init__(AsyncStream.distinct_with, args)


class TestDistinctWith(unittest.TestCase):

    @Driver(initial=[1, 2, 3, 4, 5], method=DistinctWith(args=[lambda x: x % 2]), want=[1, 2])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=DistinctWith(args=[lambda x: x % 2]), want=[1, 2])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=DistinctWith(args=[lambda x: x % 2]), want=[1, 2])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=DistinctWith(args=[lambda x: x % 2]), want=[1, 2])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    #########################

    @Driver(initial=[], method=DistinctWith(args=[lambda x: x % 2]), want=[])
    def test2__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=DistinctWith(args=[lambda x: x % 2]), want=[])
    def test2__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=DistinctWith(args=[lambda x: x % 2]), want=[])
    def test2__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=DistinctWith(args=[lambda x: x % 2]), want=[])
    def test2__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
