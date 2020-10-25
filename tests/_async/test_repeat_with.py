import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class RepeatWith(Method):

    def __init__(self, args):
        super(RepeatWith, self).__init__(AsyncStream.repeat_with, args)


class TestRepeatWith(unittest.TestCase):

    @Driver(initial=[], method=RepeatWith(args=[lambda: 1]), want=1, evaluator=AsyncStream.__anext__)
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=RepeatWith(args=[lambda: 1]), want=1, evaluator=AsyncStream.__anext__)
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=RepeatWith(args=[lambda: 1]), want=1, evaluator=AsyncStream.__anext__)
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=RepeatWith(args=[lambda: 1]), want=1, evaluator=AsyncStream.__anext__)
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
