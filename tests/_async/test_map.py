import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Map(Method):

    def __init__(self, args):
        super(Map, self).__init__(AsyncStream.map, args)


class TestMap(unittest.TestCase):

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: x * 2]), want=[2, 4, 6, 8, 10])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: x * 2]), want=[2, 4, 6, 8, 10])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: x * 2]), want=[2, 4, 6, 8, 10])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: x * 2]), want=[2, 4, 6, 8, 10])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ####################

    @Driver(initial=[], method=Map(args=[lambda x: x * 2]), want=[])
    def test2__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Map(args=[lambda x: x * 2]), want=[])
    def test2__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Map(args=[lambda x: x * 2]), want=[])
    def test2__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Map(args=[lambda x: x * 2]), want=[])
    def test2__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ####################

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: str(x)]), want=['1', '2', '3', '4', '5'])
    def test3__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: str(x)]), want=['1', '2', '3', '4', '5'])
    def test3__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: str(x)]), want=['1', '2', '3', '4', '5'])
    def test3__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: str(x)]), want=['1', '2', '3', '4', '5'])
    def test3__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ####################

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: isinstance(x, int)]), want=[True, True, True, True, True])
    def test4__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: isinstance(x, int)]), want=[True, True, True, True, True])
    def test4__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: isinstance(x, int)]), want=[True, True, True, True, True])
    def test4__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[1, 2, 3, 4, 5], method=Map(args=[lambda x: isinstance(x, int)]), want=[True, True, True, True, True])
    def test4__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
