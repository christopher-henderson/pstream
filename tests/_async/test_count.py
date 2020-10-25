import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Count(Method):

    def __init__(self, args):
        super(Count, self).__init__(AsyncStream.count, args)


class TestCount(unittest.TestCase):

    @Driver(initial=range(10), method=Count([]), want=10, evaluator=None)
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Count([]), want=10, evaluator=None)
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(0), method=Count([]), want=0, evaluator=None)
    def test1__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(0), method=Count([]), want=0, evaluator=None)
    def test1__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
