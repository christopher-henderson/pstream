import unittest
from collections.abc import Iterator

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

    class AIterable:

        def __init__(self, stream: AI):
            self.stream = stream

        def __aiter__(self):
            return self.stream

    @Driver(initial=[AI(range(3)), AIterable(AI(range(3, 6)))], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test4__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    class SIterable:

        def __init__(self, stream: Iterator):
            self.stream = stream

        def __iter__(self):
            return self.stream

    @Driver(initial=[AI(range(3)), SIterable(range(3, 6))], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test5__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[AI(range(3)), 1], method=Flatten(args=[]), want=[0, 1, 2, 3, 4, 5])
    def test6__s(self, got=None, want=None, exception=None):
        if exception is None:
            raise Exception
        if isinstance(exception, TypeError):
            return
        raise exception


if __name__ == '__main__':
    unittest.main()
