import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method


class StepBy(Method):

    def __init__(self, args):
        super(StepBy, self).__init__(AsyncStream.step_by, args)


class TestStepBy(unittest.TestCase):

    @Driver(initial=range(10), method=StepBy(args=[2]), want=[0, 2, 4, 6, 8])
    def test__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=StepBy(args=[2]), want=[0, 2, 4, 6, 8])
    def test__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=StepBy(args=[3]), want=[0, 3, 6, 9])
    def test2__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=StepBy(args=[3]), want=[0, 3, 6, 9])
    def test2__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=StepBy(args=[1]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test3__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=StepBy(args=[1]), want=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    def test3__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(0), method=StepBy(args=[10]), want=[])
    def test4__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(0), method=StepBy(args=[10]), want=[])
    def test4__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @Driver(initial=range(10), method=StepBy(args=[11]), want=[0])
    def test5__a(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=range(10), method=StepBy(args=[11]), want=[0])
    def test5__s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
