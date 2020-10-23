import asyncio
import collections
from functools import wraps, partial

from pstream import AsyncStream
from pstream._async.shim import AsyncShim


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


class AI(AsyncShim):

    def __init__(self, stream):
        super(AI, self).__init__(stream)

    async def __anext__(self):
        await asyncio.sleep(0.001)
        return await super(AI, self).__anext__()

    def __eq__(self, other):
        return self is other


class Method:

    def __init__(self, method, args):
        self.method = method
        self.args = args


class Driver:

    def __init__(self, initial=None, method=None, want=None, evaluator=AsyncStream.collect):
        if want is None:
            want = []
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
            s = self.method.method(s, *self.method.args)
        evaluator = partial(self.evaluator, s)
        want = self.want

        @wraps(fn)
        @run_to_completion
        async def test_inner(self):
            try:
                got = await evaluator()
            except Exception as e:
                fn(self, exception=e)
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
            arg = args[i]
            if arg == 'a' and callable(arg):
                self.method.args[i] = AF(arg)
            elif directives == 'a':
                self.method.args[i] = AI(arg)
