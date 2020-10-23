import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Filter(Method):

    def __init__(self, args):
        super(Filter, self).__init__(AsyncStream.filter, args)


class TestFilter(unittest.TestCase):

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: x % 2]), want=[1, 3, 5])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: x % 2]), want=[1, 3, 5])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: x % 2]), want=[1, 3, 5])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: x % 2]), want=[1, 3, 5])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    #########################

    @Driver(initial=[], method=Filter(args=[lambda x: x % 2]), want=[])
    def test2__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Filter(args=[lambda x: x % 2]), want=[])
    def test2__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Filter(args=[lambda x: x % 2]), want=[])
    def test2__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Filter(args=[lambda x: x % 2]), want=[])
    def test2__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: True]), want=[1, 2, 3, 4, 5])
    def test3__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: True]), want=[1, 2, 3, 4, 5])
    def test3__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: True]), want=[1, 2, 3, 4, 5])
    def test3__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: True]), want=[1, 2, 3, 4, 5])
    def test3__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: False]), want=[])
    def test4__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: False]), want=[])
    def test4__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: False]), want=[])
    def test4__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Filter(args=[lambda x: False]), want=[])
    def test4__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, '3', 4, 5], method=Filter(args=[lambda x: isinstance(x, str)]), want=['3'])
    def test5__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, '3', 4, 5], method=Filter(args=[lambda x: isinstance(x, str)]), want=['3'])
    def test5__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, '3', 4, 5], method=Filter(args=[lambda x: isinstance(x, str)]), want=['3'])
    def test5__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, '3', 4, 5], method=Filter(args=[lambda x: isinstance(x, str)]), want=['3'])
    def test5__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
