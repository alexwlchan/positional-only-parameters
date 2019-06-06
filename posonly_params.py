# -*- encoding: utf-8

# This file is part of https://github.com/alexwlchan/positional-only-parameters
#
# This source code is released under the MIT licence.

import functools
import inspect


try:
    getfullargspec = inspect.getfullargspec
except AttributeError:  # pragma: no cover
    getfullargspec = inspect.getargspec


def positional_only(*positional_only_args):
    positional_only_args = set(positional_only_args)

    def inner(f):
        argspec = getfullargspec(f)
        assert all(arg in argspec.args for arg in positional_only_args)

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            bad_args = set(kwargs.keys()) & positional_only_args

            if bad_args:
                if len(bad_args) == 1:
                    message = "You can only pass %s as a positional parameter"
                else:
                    message = "You can only pass %s as positional parameters"

                raise TypeError(message % ", ".join(bad_args))

            return f(*args, **kwargs)

        return wrapper

    return inner
