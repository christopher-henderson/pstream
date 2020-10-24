import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method, AI


class Flatten(Method):

    def __init__(self, args):
        super(Flatten, self).__init__(AsyncStream.flatten, args)


class TestFlatten(unittest.TestCase):

    @Driver(initial=[range(3), range(3, 6)], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[AI(range(3)), range(3, 6)], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[range(3), AI(range(3, 6))], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test2__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[AI(range(3)), AI(range(3, 6))], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test3__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[range(3), range(3, 6)], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[AI(range(3)), range(3, 6)], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[range(3), AI(range(3, 6))], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test2__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[AI(range(3)), AI(range(3, 6))], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test3__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
