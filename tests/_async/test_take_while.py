import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class TakeWhile(Method):

    def __init__(self, args):
        super(TakeWhile, self).__init__(AsyncStream.take_while, args)


class TestTakeWhile(unittest.TestCase):

    @Driver(initial=range(10), method=TakeWhile(args=[lambda x: x != 5]), want=[0, 1, 2, 3, 4])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda x: x != 5]), want=[0, 1, 2, 3, 4])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda x: x != 5]), want=[0, 1, 2, 3, 4])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda x: x != 5]), want=[0, 1, 2, 3, 4])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: True]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test1__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: True]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test1__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: True]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test1__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: True]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test1__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=[], method=TakeWhile(args=[lambda _: False]), want=[])
    def test2__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=TakeWhile(args=[lambda _: False]), want=[])
    def test2__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=TakeWhile(args=[lambda _: False]), want=[])
    def test2__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=TakeWhile(args=[lambda _: False]), want=[])
    def test2__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: False]), want=[])
    def test3__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: False]), want=[])
    def test3__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: False]), want=[])
    def test3__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=TakeWhile(args=[lambda _: False]), want=[])
    def test3__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
