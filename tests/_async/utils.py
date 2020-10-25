import asyncio
from collections.abc import Iterable, Iterator
from functools import wraps, partial

from pstream import AsyncStream


def expect(exception):
    def wrapper(fn):
        @wraps(fn)
        async def inner(self, *args, **kwargs):
            try:
                await fn(self, *args, **kwargs)
            except Exception as e:
                if not isinstance(e, exception):
                    raise e
                return
            raise RuntimeError('expected {}'.format(exception))
        return inner
    return wrapper


def run_to_completion(f):
    @wraps(f)
    def wrapper(self, *args, **kwargs):
        loop = asyncio.new_event_loop()
        loop.run_until_complete(f(self, *args, **kwargs))
        loop.close()

    return wrapper


def AF(f):
    @wraps(f)
    async def inner(*args, **kwargs):
        await asyncio.sleep(0.01)
        return f(*args, *kwargs)

    return inner


class AI:

    def __init__(self, stream):
        if isinstance(stream, Iterator):
            self.stream = stream
        elif isinstance(stream, Iterable):
            self.stream = stream.__iter__()
        else:
            raise TypeError

    def __aiter__(self):
        return self

    async def __anext__(self):
        await asyncio.sleep(0.001)
        try:
            return next(self.stream)
        except StopIteration:
            raise StopAsyncIteration

    def __eq__(self, other):
        return self is other


class Method:

    def __init__(self, method, args):
        self.method = method
        self.args = args


class Driver:

    def __init__(self, initial=None, method=None, want=None, evaluator=AsyncStream.collect):
        if initial is None:
            initial = []
        self.initial = initial
        self.method = method
        self.want = want
        self.evaluator = evaluator

    def __call__(self, fn):
        self.figure(fn.__name__)
        s = AsyncStream(self.initial)
        if self.method is not None:
            if self.method.args:
                s = self.method.method(s, *self.method.args)
            else:
                s = self.method.method(s)
        if self.evaluator is None:
            evaluator = s
        else:
            evaluator = partial(self.evaluator, s)
        want = self.want

        @wraps(fn)
        @run_to_completion
        async def test_inner(self):
            try:
                if callable(evaluator):
                    got = await evaluator()
                else:
                    got = await evaluator
            except Exception as e:
                return fn(self, exception=e)
            fn(self, got=got, want=want)

        return test_inner

    def figure(self, name: str):
        if self.method is None:
            return
        directives: list = name.split('__')[-1].split('_')
        initial = directives[0]
        if initial == 'a':
            self.initial = AI(self.initial)
        if len(directives) == 1:
            return
        args = directives[1]
        for i, arg in enumerate(self.method.args):
            if i >= len(args):
                break
            directive = args[i]
            if directive == 'a' and callable(arg):
                self.method.args[i] = AF(arg)
            elif directive == 'a':
                self.method.args[i] = AI(arg)
