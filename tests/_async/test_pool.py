import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method
from tests.sync.test_stream import expect


class Pool(Method):

    def __init__(self, args):
        super(Pool, self).__init__(AsyncStream.pool, args)


class TestPool(unittest.TestCase):

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[2]), want=[[1, 2], [3, 4], [5]])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[2]), want=[[1, 2], [3, 4], [5]])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[6]), want=[[1, 2, 3, 4, 5]])
    def test2__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[6]), want=[[1, 2, 3, 4, 5]])
    def test2__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ############################

    @Driver(initial=[1, 2, 3, 4, 5, 6], method=Pool(args=[2]), want=[[1, 2], [3, 4], [5, 6]])
    def test3__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5, 6], method=Pool(args=[2]), want=[[1, 2], [3, 4], [5, 6]])
    def test3__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ############################

    @Driver(initial=[], method=Pool(args=[2]), want=[])
    def test4__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Pool(args=[2]), want=[])
    def test4__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ############################

    @Driver(initial=[], method=Pool(args=[1]), want=[])
    def test5__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Pool(args=[1]), want=[])
    def test5__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ############################

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[4]), want=[[1, 2, 3, 4], [5]])
    def test6__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[4]), want=[[1, 2, 3, 4], [5]])
    def test6__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[1]), want=[[1], [2], [3], [4], [5]])
    def test7__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Pool(args=[1]), want=[[1], [2], [3], [4], [5]])
    def test7__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
