import contextvars
import inspect
from contextlib import contextmanager
from typing import List


class Provider:
    def __init__(self, name):
        self.contextvar = contextvars.ContextVar(name)

    @contextmanager
    def use(self, spark):
        token = self.contextvar.set(spark)
        try:
            yield None
        finally:
            self.contextvar.reset(token)

    def get(self):
        return self.contextvar.get()


def provide(*providers: List[Provider]):
    def provide_inner(fn):
        # No good way to detect whether the decorated method is an instance method
        # Instead we just check to see if the first argument has name "self"
        params = inspect.signature(fn).parameters
        should_keep_first_arg_in_place = len(params) and next(iter(params)) == "self"

        def wrapped(*args, **kwargs):
            prepended = tuple(provider.get() for provider in providers)
            if not should_keep_first_arg_in_place:
                new_args = prepended + args
            else:
                new_args = args[:1] + prepended + args[1:]
            return fn(*new_args, **kwargs)

        return wrapped

    return provide_inner
