import unittest

from pstream import AsyncStream
from tests._async.utils import Driver, Method, expect, AF, AI, run_to_completion


class SortWith(Method):

    def __init__(self, args):
        super(SortWith, self).__init__(AsyncStream.sort_with, args)


class TestSortWith(unittest.TestCase):

    random = ['123', '5', '1245', '6', '2', '56', '0', '8', '2', '78', '4', '-1']

    @Driver(initial=random, method=SortWith(args=[lambda x: int(x)]), want=['-1', '0', '2', '2', '4', '5', '6', '8', '56', '78', '123', '1245'])
    def test__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=random, method=SortWith(args=[lambda x: int(x)]), want=['-1', '0', '2', '2', '4', '5', '6', '8', '56', '78', '123', '1245'])
    def test__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    ###############################

    @run_to_completion
    @expect(TypeError)
    async def test1__a_s(self):
        AsyncStream([3, 4, 2, 1]).sort_with(AF(lambda x: x))

    @run_to_completion
    @expect(TypeError)
    async def test1__a_a(self):
        AsyncStream(AI([3, 4, 2, 1])).sort_with(AF(lambda x: x))

    ###############################

    @Driver(initial=[], method=SortWith(args=[lambda x: int(x)]), want=[])
    def test2__s_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)

    @Driver(initial=[], method=SortWith(args=[lambda x: int(x)]), want=[])
    def test2__a_s(self, got=None, want=None, exception=None):
        if exception is not None:
            raise exception
        self.assertEqual(got, want)


if __name__ == '__main__':
    unittest.main()
