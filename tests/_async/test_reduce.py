import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Reduce(Method):

    def __init__(self, args):
        super(Reduce, self).__init__(AsyncStream.reduce, args)


class TestReduce(unittest.TestCase):

    @Driver(initial=range(10), method=Reduce(args=[lambda x, acc: x + acc, 0]), want=45, evaluator=None)
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Reduce(args=[lambda x, acc: x + acc, 0]), want=45, evaluator=None)
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Reduce(args=[lambda x, acc: x + acc, 0]), want=45, evaluator=None)
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=Reduce(args=[lambda x, acc: x + acc, 0]), want=45, evaluator=None)
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
