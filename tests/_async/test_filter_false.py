import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class FilterFalse(Method):

    def __init__(self, args):
        super(FilterFalse, self).__init__(AsyncStream.filter_false, args)


class TestFilterFalse(unittest.TestCase):

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: x % 2]), want=[2, 4])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: x % 2]), want=[2, 4])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: x % 2]), want=[2, 4])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: x % 2]), want=[2, 4])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    #########################

    @Driver(initial=[], method=FilterFalse(args=[lambda x: x % 2]), want=[])
    def test2__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=FilterFalse(args=[lambda x: x % 2]), want=[])
    def test2__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=FilterFalse(args=[lambda x: x % 2]), want=[])
    def test2__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=FilterFalse(args=[lambda x: x % 2]), want=[])
    def test2__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: True]), want=[])
    def test3__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: True]), want=[])
    def test3__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: True]), want=[])
    def test3__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: True]), want=[])
    def test3__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: False]), want=[1, 2, 3, 4, 5])
    def test4__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: False]), want=[1, 2, 3, 4, 5])
    def test4__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: False]), want=[1, 2, 3, 4, 5])
    def test4__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=FilterFalse(args=[lambda x: False]), want=[1, 2, 3, 4, 5])
    def test4__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###########################

    @Driver(initial=[1, 2, '3', 4, 5], method=FilterFalse(args=[lambda x: isinstance(x, str)]), want=[1, 2, 4, 5])
    def test5__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, '3', 4, 5], method=FilterFalse(args=[lambda x: isinstance(x, str)]), want=[1, 2, 4, 5])
    def test5__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, '3', 4, 5], method=FilterFalse(args=[lambda x: isinstance(x, str)]), want=[1, 2, 4, 5])
    def test5__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, '3', 4, 5], method=FilterFalse(args=[lambda x: isinstance(x, str)]), want=[1, 2, 4, 5])
    def test5__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
