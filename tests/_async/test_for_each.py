import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class ForEach(Method):

    def __init__(self, args):
        super(ForEach, self).__init__(AsyncStream.for_each, args)


class TestForEach(unittest.TestCase):

    @Driver(initial=range(10), method=ForEach(args=[lambda x: x % 2]), want=None, evaluator=None)
    def test__a_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=ForEach(args=[lambda x: x % 2]), want=None, evaluator=None)
    def test__s_a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=ForEach(args=[lambda x: x % 2]), want=None, evaluator=None)
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=ForEach(args=[lambda x: x % 2]), want=None, evaluator=None)
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
