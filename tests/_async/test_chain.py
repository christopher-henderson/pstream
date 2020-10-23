import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Chain(Method):

    def __init__(self, args):
        super(Chain, self).__init__(AsyncStream.chain, args)


class TestChain(unittest.TestCase):

    @Driver(initial=range(5), method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4, 0, 1, 2, 3, 4])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(2), method=Chain(args=[range(2, 6), range(6, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__a_aa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Chain(args=[range(2, 6), range(6, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__a_as(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Chain(args=[range(2, 6), range(6, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__a_sa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Chain(args=[range(2, 6), range(6, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__a_ss(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Chain(args=[range(2, 6), range(6, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__s_aa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Chain(args=[range(2, 5), range(5, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__s_as(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Chain(args=[range(2, 5), range(5, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__s_sa(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(2), method=Chain(args=[range(2, 5), range(5, 8)]), want=[0, 1, 2, 3, 4, 5, 6, 7])
    def test2__s_ss(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(5), method=Chain(args=[]), want=[0, 1, 2, 3, 4])
    def test3__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Chain(args=[]), want=[0, 1, 2, 3, 4])
    def test3__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Chain(args=[]), want=[0, 1, 2, 3, 4])
    def test3__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(5), method=Chain(args=[]), want=[0, 1, 2, 3, 4])
    def test3__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=[], method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4])
    def test4__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4])
    def test4__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4])
    def test4__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Chain(args=[range(5)]), want=[0, 1, 2, 3, 4])
    def test4__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
