import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class Repeat(Method):

    def __init__(self, args):
        super(Repeat, self).__init__(AsyncStream.repeat, args)


class TestRepeat(unittest.TestCase):

    @Driver(initial=[], method=Repeat(args=[1]), want=1, evaluator=AsyncStream.__anext__)
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=Repeat(args=[1]), want=1, evaluator=AsyncStream.__anext__)
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
