# MIT License
#
# Copyright (c) 2020 Christopher Henderson
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import unittest
import hashlib

from pystream import Stream


class TestStream(unittest.TestCase):

    def test_from_iterator(self):
        got = Stream((_ for _ in range(10))).collect()
        self.assertEqual(got, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_value_error(self):
        try:
            Stream(1)
        except ValueError:
            pass

    def test_empty(self):
        self.assertEqual(Stream([]).collect(), [])

    def test_single(self):
        self.assertEqual(Stream([1]).collect(), [1])

    def test_chain_single(self):
        self.assertEqual(Stream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect(), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_chain_empty(self):
        self.assertEqual(Stream([1, 2, 3]).chain([]).collect(), [1, 2, 3])

    def test_chain_multiple(self):
        self.assertEqual(Stream([1, 2, 3]).chain([4, 5, 6], [7, 8, 9]).collect(), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_chain_repeated_call(self):
        self.assertEqual(Stream([1, 2, 3]).chain([4, 5, 6]).chain([7, 8, 9]).collect(), [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_deduplicate(self):
        self.assertEqual(Stream([1, 2, 2, 3, 2, 1, 4, 5, 6, 1]).deduplicate().collect(), [1, 2, 3, 4, 5, 6])

    def test_deduplicate_with(self):
        fingerprinter = lambda name: hashlib.sha256(name.encode('utf-8')).digest()
        people = ['Bob', 'Alice', 'Eve', 'Alice', 'Alice', 'Eve', 'Achmed']
        got = Stream(people).deduplicate_with(fingerprinter).collect()
        self.assertEqual(got, ['Bob', 'Alice', 'Eve', 'Achmed'])

    def test_enumerate(self):
        self.assertEqual(Stream([0, 1, 2]).enumerate().collect(), [(0, 0), (1, 1), (2, 2)])

    def test_enumerate_empty(self):
        self.assertEqual(Stream([]).enumerate().collect(), [])

    def test_filter(self):
        self.assertEqual(Stream([1, 2, 3, 4]).filter(lambda x: x % 2 is 0).collect(), [2, 4])

    def test_filter_empty(self):
        self.assertEqual(Stream([]).filter(lambda x: x % 2 is 0).collect(), [])

    def test_flatten(self):
        self.assertEqual(Stream([[1, 2, 3], [4, 5, 6]]).flatten().collect(), [1, 2, 3, 4, 5, 6])

    def test_flatten_empty_left(self):
        self.assertEqual(Stream([[], [4, 5, 6]]).flatten().collect(), [4, 5, 6])

    def test_flatten_empty_right(self):
        self.assertEqual(Stream([[1, 2, 3], []]).flatten().collect(), [1, 2, 3])

    def test_flatten_three_dimensional(self):
        arr = [[[1, 2, 3]], [[4, 5, 6]]]
        want = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(Stream(arr).flatten().collect(), want)

    def test_flatten_three_to_one(self):
        three_dimensional = [[[1, 2, 3]], [[4, 5, 6]]]
        got = Stream(three_dimensional).flatten().flatten().collect()
        self.assertEqual(got, [1, 2, 3, 4, 5, 6])

    class Inspector(object):
        def __init__(self):
            self.copy = list()

        def visit(self, item):
            self.copy.append(item)

    def test_inspect(self):
        inspector = TestStream.Inspector()
        got = Stream([1, 2, 3, 4]).filter(lambda x: x % 2 is 0).inspect(inspector.visit).collect()
        self.assertEqual(got, inspector.copy)

    def test_inspect_then(self):
        inspector = TestStream.Inspector()
        got = Stream([1, 2, 3, 4]).filter(lambda x: x % 2 is 0).inspect(inspector.visit).map(lambda x: x * 2).collect()
        self.assertEqual([2, 4], inspector.copy)
        self.assertEqual(got, [4, 8])

    def test_map(self):
        self.assertEqual(Stream([1, 2, 3, 4]).map(lambda x: x * 2).collect(), [2, 4, 6, 8])

    def test_map_empty(self):
        self.assertEqual(Stream([]).map(lambda x: x * 2).collect(), [])

    def test_reduce(self):
        add = lambda a, b: a + b
        numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        got = Stream(numbers).reduce(0, add)
        assert got == 45

    def test_reverse(self):
        self.assertEqual(Stream([1, 2, 3, 4]).reverse().collect(), [4, 3, 2, 1])

    def test_skip(self):
        self.assertEqual(Stream([1, 2, 3, 4, 5, 6, 7, 8, 9]).skip(4).collect(), [5, 6, 7, 8, 9])

    def test_skip_while(self):
        self.assertEqual(Stream([1, 2, 3, 4, 5, 6, 7, 8, 9]).skip_while(lambda x: x < 5).collect(), [5, 6, 7, 8, 9])

    def test_sort(self):
        arr = [12, 233, 4567, 344523, 7, 567, 34, 5678, 456, 23, 4, 7, 63, 45, 345]
        got = Stream(arr).sort().collect()
        self.assertEqual(got, [4, 7, 7, 12, 23, 34, 45, 63, 233, 345, 456, 567, 4567, 5678, 344523])

    def test_sort_complex(self):
        # sort and reverse incur collections, and sort itself returns a physical list rather than
        # and iterator, so this is just a bit of whacking around to smoke test the interactions
        # between the pipelines.
        arr = [12, 233, 4567, 344523, 7, 567, 34, 5678, 456, 23, 4, 7, 63, 45, 345]
        got = Stream(arr).filter(lambda x: x % 2).sort().reverse().filter(lambda x: x < 1000).deduplicate().collect()
        self.assertEqual(got, [567, 345, 233, 63, 45, 23, 7])

    def test_step_by_even(self):
        self.assertEqual(Stream([1, 2, 3, 4, 5, 6, 7, 8, 9]).step_by(4).collect(), [1, 5, 9])

    def test_step_by_odd(self):
        self.assertEqual(Stream([1, 2, 3, 4, 5, 6, 7, 8, 9]).step_by(3).collect(), [1, 4, 7])

    def test_step_too_few(self):
        self.assertEqual(Stream([1, 2, 3]).step_by(3).collect(), [1])

    def test_step_single(self):
        self.assertEqual(Stream([1]).step_by(3).collect(), [1])

    def test_step_empty(self):
        self.assertEqual(Stream([]).step_by(3).collect(), [])

    def test_take(self):
        self.assertEqual(Stream([1, 2, 3, 4, 5, 6, 7, 8, 9]).take(4).collect(), [1, 2, 3, 4])

    def test_take_more_than_there_are(self):
        self.assertEqual(Stream([1, 2]).take(4).collect(), [1, 2])

    def test_take_while(self):
        self.assertEqual(Stream([1, 2, 3, 4, 5, 6, 7, 8, 9]).take_while(lambda x: x < 5).collect(), [1, 2, 3, 4])

    def test_zip(self):
        self.assertEqual(Stream([0, 1, 2]).zip([3, 4, 5]).collect(), [(0, 3), (1, 4), (2, 5)])

if __name__ == '__main__':
    unittest.main()