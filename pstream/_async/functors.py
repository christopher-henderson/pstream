# MIT License
#
# Copyright (c) 2020 Christopher Henderson, chris@chenderson.org
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

from collections.abc import Iterable, Iterator, AsyncIterable, AsyncIterator as AsyncIter
from collections import defaultdict
from inspect import iscoroutinefunction

from .._sync.stream import Stream

Enumeration = Stream.Enumeration


# @TODO heck yeah! Typing!
# import typing


class AsyncIterator:

    @staticmethod
    def new(stream):
        if isinstance(stream, AsyncIterable):
            return stream
        elif isinstance(stream, AsyncIter):
            return stream.__aiter__()
        return AsyncIterator(stream)

    def __init__(self, stream):
        if isinstance(stream, Iterator):
            self.stream = stream
        elif isinstance(stream, Iterable):
            self.stream = (x for x in stream)
        else:
            raise ValueError(
                'pstream.AsyncStream can only accept either an _async iterator, an iterator, or an iterable. Got {}'.format(
                    type(stream)))

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration


def coerce(stream):
    if isinstance(stream, Iterator) or isinstance(stream, AsyncIter):
        return stream
    elif isinstance(stream, Iterable):
        def iterator():
            for x in stream:
                yield x

        return iterator()
    elif isinstance(stream, AsyncIterable):
        return Adaptor(stream)
    else:
        raise ValueError('not an iterable of any kind {}'.format(type(stream)))


class Adaptor:

    def __init__(self, stream):
        self.stream = stream

    def __aiter__(self):
        return self

    async def __anext__(self):
        return self.stream.__anext__()


def higher_order_factory(ss, sa, _as, aa):
    def inner(f, stream):
        stream = coerce(stream)
        f_is_async = iscoroutinefunction(f)
        stream_is_async = isinstance(stream, AsyncIter)
        if not f_is_async and not stream_is_async:
            return ss(f, stream)
        elif not f_is_async and stream_is_async:
            return sa(f, stream)
        elif f_is_async and not stream_is_async:
            return _as(f, stream)
        elif f_is_async and stream_is_async:
            return aa(f, stream)
        else:
            ValueError('{}'.format(type(f)))

    return inner


def factory(s, a):
    def inner(stream, *args):
        stream = coerce(stream)
        if isinstance(stream, AsyncIter):
            return a(stream, *args)
        return s(stream, *args)

    return inner

##############################
# MAP
##############################


def ss_map(f, stream):
    for x in stream:
        yield f(x)


async def sa_map(f, stream):
    async for x in stream:
        yield f(x)


async def as_map(f, stream):
    for x in stream:
        yield await f(x)


async def aa_map(f, stream):
    async for x in stream:
        yield await f(x)


##############################
# FILTER
##############################

def ss_filter(f, stream):
    for x in stream:
        if f(x):
            yield x


async def sa_filter(f, stream):
    async for x in stream:
        if f(x):
            yield x


async def as_filter(f, stream):
    for x in stream:
        if await f(x):
            yield x


async def aa_filter(f, stream):
    async for x in stream:
        if await f(x):
            yield x


##############################
# FILTER_FALSE
##############################

def ss_filter_false(f, stream):
    for x in stream:
        if not f(x):
            yield x


async def sa_filter_false(f, stream):
    async for x in stream:
        if not f(x):
            yield x


async def as_filter_false(f, stream):
    for x in stream:
        if not await f(x):
            yield x


async def aa_filter_false(f, stream):
    async for x in stream:
        if not await f(x):
            yield x


##############################
# CHAIN
##############################

async def chain(*streams):
    async for x in flatten(streams):
        yield x


##############################
# FLATTEN
##############################

async def a_flatten(streams):
    async for stream in streams:
        stream = coerce(stream)
        if isinstance(stream, AsyncIter):
            async for element in stream:
                yield element
        else:
            for element in stream:
                yield element


async def s_flatten(streams):
    for stream in streams:
        stream = coerce(stream)
        if isinstance(stream, AsyncIter):
            async for element in stream:
                yield element
        else:
            for element in stream:
                yield element


##############################
# GROUP_BY
##############################

def ss_group_by(f, stream):
    groups = defaultdict(list)
    for x in stream:
        groups[f(x)].append(x)
    for group in groups.values():
        yield group


async def sa_group_by(f, stream):
    groups = defaultdict(list)
    async for x in stream:
        groups[f(x)].append(x)
    for group in groups.values():
        yield group


async def as_group_by(f, stream):
    groups = defaultdict(list)
    for x in stream:
        groups[await f(x)].append(x)
    for group in groups.values():
        yield group


async def aa_group_by(f, stream):
    groups = defaultdict(list)
    async for x in stream:
        groups[await f(x)].append(x)
    for group in groups.values():
        yield group


##############################
# INSPECT
##############################

def ss_inspect(f, stream):
    for x in stream:
        f(x)
        yield x


async def sa_inspect(f, stream):
    async for x in stream:
        f(x)
        yield x


async def as_inspect(f, stream):
    for x in stream:
        await f(x)
        yield x


async def aa_inspect(f, stream):
    async for x in stream:
        await f(x)
        yield x


##############################
# REPEAT
##############################

def repeat(x):
    while True:
        yield x


##############################
# SKIP_WHILE
##############################

def ss_skip_while(f, stream):
    for x in stream:
        if not f(x):
            yield x
    for x in stream:
        yield x


async def sa_skip_while(f, stream):
    async for x in stream:
        if not f(x):
            yield x
    async for x in stream:
        yield x


async def as_skip_while(f, stream):
    for x in stream:
        if not await f(x):
            yield x
    for x in stream:
        yield x


async def aa_skip_while(f, stream):
    async for x in stream:
        if not await f(x):
            yield x
    async for x in stream:
        yield x


##############################
# TAKE_WHILE
##############################

def ss_take_while(f, stream):
    for x in stream:
        if f(x):
            yield x
        else:
            break


async def sa_take_while(f, stream):
    async for x in stream:
        if f(x):
            yield x
        else:
            break


async def as_take_while(f, stream):
    for x in stream:
        if await f(x):
            yield x
        else:
            break


async def aa_take_while(f, stream):
    async for x in stream:
        if await f(x):
            yield x
        else:
            break


##############################
# ENUMERATE
##############################

def s_enumerate(stream):
    count = 0
    for element in stream:
        yield Enumeration(count, element)
        count += 1


async def a_enumerate(stream):
    count = 0
    async for element in stream:
        yield Enumeration(count, element)
        count += 1

##############################
# SKIP
##############################


def s_skip(stream, limit):
    for _ in range(limit):
        try:
            next(stream)
        except StopIteration:
            break
    for x in stream:
        yield x


async def a_skip(stream, limit):
    for _ in range(limit):
        try:
            await stream.__anext__()
        except StopAsyncIteration:
            break
    async for x in stream:
        yield x


##############################
# TAKE
##############################


def s_take(stream, limit):
    for _ in range(limit):
        try:
            yield next(stream)
        except StopIteration:
            break


async def a_take(stream, limit):
    for _ in range(limit):
        try:
            yield await stream.__anext__()
        except StopAsyncIteration:
            break

##############################
# ZIP
##############################


async def zip(*streams):
    streams = [coerce(stream) for stream in streams]
    while True:
        try:
            group = list()
            for stream in streams:
                group.append(await stream.__anext__() if isinstance(stream, AsyncIter) else next(stream))
            yield tuple(group)
        except StopIteration:
            break
        except StopAsyncIteration:
            break

##############################
# POOL
##############################


def s_pool(stream, size):
    p = list()
    for x in stream:
        p.append(x)
        if len(p) == size:
            yield p
            p = list()
    if len(p) != 0:
        yield p


async def a_pool(stream, size):
    p = list()
    async for x in stream:
        p.append(x)
        if len(p) == size:
            yield p
            p = list()
    if len(p) != 0:
        yield p


##############################
# SORT
##############################

def s_sort(stream):
    for x in sorted(stream):
        yield x


async def a_sort(stream):
    for x in sorted([x async for x in stream]):
        yield x


##############################
# REVERSE
##############################

def s_reverse(stream):
    for x in reversed([x for x in stream]):
        yield x


async def a_reverse(stream):
    for x in reversed([x async for x in stream]):
        yield x


##############################
# DISTINCT
##############################

def s_distinct(stream):
    seen = set()
    for x in stream:
        if x in seen:
            continue
        seen.add(x)
        yield x


async def a_distinct(stream):
    seen = set()
    async for x in stream:
        if x in seen:
            continue
        seen.add(x)
        yield x


##############################
# DISTINCT_WITH
##############################

def ss_distinct_with(f, stream):
    seen = set()
    for x in stream:
        h = f(x)
        if h in seen:
            continue
        seen.add(h)
        yield x


async def sa_distinct_with(f, stream):
    seen = set()
    async for x in stream:
        h = f(x)
        if h in seen:
            continue
        seen.add(h)
        yield x


async def as_distinct_with(f, stream):
    seen = set()
    for x in stream:
        h = await f(x)
        if h in seen:
            continue
        seen.add(h)
        yield x


async def aa_distinct_with(f, stream):
    seen = set()
    async for x in stream:
        h = await f(x)
        if h in seen:
            continue
        seen.add(h)
        yield x


##############################
# FOR_EACH
##############################

def ss_for_each(f, stream):
    for x in stream:
        f(x)
        yield


async def as_for_each(f, stream):
    for x in stream:
        await f(x)
        yield


async def sa_for_each(f, stream):
    async for x in stream:
        f(x)
        yield


async def aa_for_each(f, stream):
    async for x in stream:
        await f(x)
        yield


def step_by(step, stream):
    s = enumerate(stream)
    s = filter(lambda e:  e.count % step == 0, s)
    s = map(lambda e: e.element, s)
    return s


distinct = factory(s_distinct, a_distinct)
distinct_with = higher_order_factory(ss_distinct_with, sa_distinct_with, as_distinct_with, aa_distinct_with)
map = higher_order_factory(ss_map, sa_map, as_map, aa_map)
filter = higher_order_factory(ss_filter, sa_filter, as_filter, aa_filter)
filter_false = higher_order_factory(ss_filter_false, sa_filter_false, as_filter_false, aa_filter_false)
flatten = factory(s_flatten, a_flatten)
group_by = higher_order_factory(ss_group_by, sa_group_by, as_group_by, aa_group_by)

inspect = higher_order_factory(ss_inspect, sa_inspect, as_inspect, aa_inspect)
skip_while = higher_order_factory(ss_skip_while, sa_skip_while, as_skip_while, aa_skip_while)
take_while = higher_order_factory(ss_take_while, sa_take_while, as_take_while, aa_take_while)
skip = factory(s_skip, a_skip)
take = factory(s_take, a_take)
enumerate = factory(s_enumerate, a_enumerate)
pool = factory(s_pool, a_pool)
sort = factory(s_sort, a_sort)
reverse = factory(s_reverse, a_reverse)
for_each = higher_order_factory(ss_for_each, sa_for_each, as_for_each, aa_for_each)
