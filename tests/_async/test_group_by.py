import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class GroupBy(Method):

    def __init__(self, args):
        super(GroupBy, self).__init__(AsyncStream.group_by, args)


class TestGroupBy(unittest.TestCase):

    @Driver(initial=range(10), method=GroupBy(args=[lambda x: x % 2]), want=[[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=GroupBy(args=[lambda x: x % 2]), want=[[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=GroupBy(args=[lambda x: x % 2]), want=[[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=GroupBy(args=[lambda x: x % 2]), want=[[0, 2, 4, 6, 8], [1, 3, 5, 7, 9]])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    #########################

    @Driver(initial=[], method=GroupBy(args=[lambda x: x % 2]), want=[])
    def test2__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=GroupBy(args=[lambda x: x % 2]), want=[])
    def test2__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=GroupBy(args=[lambda x: x % 2]), want=[])
    def test2__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=GroupBy(args=[lambda x: x % 2]), want=[])
    def test2__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, 3, 4, 5], method=GroupBy(args=[lambda x: True]), want=[[1, 2, 3, 4, 5]])
    def test3__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=GroupBy(args=[lambda x: True]), want=[[1, 2, 3, 4, 5]])
    def test3__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=GroupBy(args=[lambda x: True]), want=[[1, 2, 3, 4, 5]])
    def test3__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=GroupBy(args=[lambda x: True]), want=[[1, 2, 3, 4, 5]])
    def test3__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
