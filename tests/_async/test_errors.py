import unittest

from pstream import AsyncStream
from pstream.errors import InfiniteCollectionError
from tests._async.utils import run_to_completion, expect
from tests.sync.test_stream import expect as expect_s


class TestErrors(unittest.TestCase):

    @run_to_completion
    @expect(InfiniteCollectionError)
    async def test_collect(self):
        await AsyncStream().repeat(1).collect()

    @expect_s(ValueError)
    def test_pool(self):
        AsyncStream().pool(0)

    @expect_s(ValueError)
    def test_pool_negative(self):
        AsyncStream().pool(-1)

    @expect_s(ValueError)
    def test_step_by(self):
        AsyncStream().step_by(0)

    @expect_s(InfiniteCollectionError)
    def test_group_by(self):
        AsyncStream().repeat(0).group_by(lambda: True)
