import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Zip(Method):

    def __init__(self, args):
        super(Zip, self).__init__(AsyncStream.zip, args)


class TestZip(unittest.TestCase):

    @Driver(initial=range(5), method=Zip(args=[range(5)]), want=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Zip(args=[range(5)]), want=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Zip(args=[range(5)]), want=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Zip(args=[range(5)]), want=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4)])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__a_aa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__a_as(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__a_sa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__a_ss(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__s_aa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__s_as(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__s_sa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Zip(args=[range(3, 5), range(6, 8)]), want=[(0, 3, 6), (1, 4, 7)])
    def test2__s_ss(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(5), method=Zip(args=[]), want=[(0,), (1,), (2,), (3,), (4,)])
    def test3__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Zip(args=[]), want=[(0,), (1,), (2,), (3,), (4,)])
    def test3__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Zip(args=[]), want=[(0,), (1,), (2,), (3,), (4,)])
    def test3__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Zip(args=[]), want=[(0,), (1,), (2,), (3,), (4,)])
    def test3__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=[], method=Zip(args=[range(5)]), want=[])
    def test4__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Zip(args=[range(5)]), want=[])
    def test4__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Zip(args=[range(5)]), want=[])
    def test4__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Zip(args=[range(5)]), want=[])
    def test4__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
