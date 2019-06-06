# positional-only-arguments

This is a proof-of-concept decorator that lets you specify positional-only parameters in Python.

For example:

```python
from posonly_params import positional_only


@positional_only("x")
def adder(x, y, z):
    return x + y + z


adder(1, 2, 3)
# 6

adder(x=1, y=2, z=3)
# TypeError: You can only pass x as a positional parameter
```

I've tested it with Python 2.7 and 3.6.



## Why?

PEP 570 adds [positional-only arguments](https://www.python.org/dev/peps/pep-0570/) in Python 3.8, using a slash.

In Python 3.8, you can define functions as follows:

```python
def multiplier(a, b, /, c, d, *, e, f):
    ...
```

Here:

*   `a` and `b` are positional-only; you can't use them as keyword arguments
*   `c` and `d` can be positional or keyword arguments
*   `e` and `f` must be keyword arguments (using the existing star syntax added [in Python 3](https://www.python.org/dev/peps/pep-3102/))

At first I thought this was a bit odd (I still think it's a weird choice of syntax), but a few people on Twitter persuaded me that positional-only arguments can be useful sometimes.
So now I think it's a reasonable idea, why not wait for the feature to land in Python 3.8?

A couple of reasons:

*   **A lot of libraries will have to wait for this feature.**

    One of the touted benefits of PEP 570 is that third-party libraries can use positional-only arguments, similar to the standard library.
    But a library can't assume a Python 3.8 feature until 3.8 is the oldest version it supports.

    If the library already exists, that could mean waiting until 3.7 is completely out of support.
    According to the [release schedule](https://www.python.org/dev/peps/pep-0537/), the last bugfix release is a year away, and security fixes will be coming for three years after that.

    Plus, there are plenty of codebases still stuck on earlier versions of Python 3, and lots of Python 2 still in the world.

    You can use this decorator *right now*.

*   **This lets you deprecate using keywords with positional-only arguments, without breaking them immediately.**

    Changing an existing function to use positional-only arguments is a breaking change, and it would be nice to emit deprecation warnings for a while before turning it on.

    This is inspired by the [Hypothesis deprecation policy](https://hypothesis.readthedocs.io/en/latest/healthchecks.html#deprecations) -- deprecated features emit a warning for at least six months before they're removed.
    It would be nice to the same for positional-only arguments.

    We used to do something similar when changing parameter names (which is mentioned in the PEP), with [the renamed_arguments() decorator](https://github.com/HypothesisWorks/hypothesis/blob/8431a80dcaea2c4302d725540a1ff486be52cf23/hypothesis-python/src/hypothesis/internal/renaming.py).
    It worked with both the new and old parmeter names, and dropped a deprecation warning if you used the old name.

*   **It doesn't mean mucking about with \*args and tuple unpacking.**

    You can replicate this feature if you change your function signature to take `*args` and unpack them in the body, but that always felt fiddly and weird to me.

    Plus, when you do eventually get to Python 3.8, taking that out is a bit harder.
    Moving from this decorator to the Python 3.8 syntax is a two-line change.

*   **The 3.8 slash syntax looks weird to me.**

    Until it's more common, I'm going to be confused whenever I see it.
    (I still do a double-take at the star sometimes.)

    A named decorator gives a bigger clue about what it's doing.

*   **Fun!**

    I thought this would a neat challenge (and I thought it would involve more mucking around with the [inspect module](https://docs.python.org/3/library/inspect.html)).

    I know, I'm a bit weird.

What this is:

*   Scratching an intellectual itch
*   A possible deprecation path for positional-only arguments pre-3.8

What this is not:

*   Me trying to say "this is how PEP 570 should have been implemented".
    There's a section in the PEP about why [they rejected decorators](https://www.python.org/dev/peps/pep-0570/#decorators).




## Usage

Copy the contents of `posonly_params.py` into your codebase.
It's a single file.

To use it, import `positional_only` and apply the decorator to a function you want to use with positional-only arguments.
Pass the list of parameter names you want to be positional-only as string arguments to the decorator:

```python
from posonly_params import positional_only


@positional_only("x", "y")
def doubler(x, y, z):
    return (x + y + z) * 2
```

You can see more examples in `tests.py`.



## Tests

You can run the tests with pytest and coverage:

```console
$ pip install pytest-cov
$ coverage run -m py.test tests.py; coverage report
```



## Possible improvements

See the [issues list](https://github.com/alexwlchan/positional-only-parameters/issues).



## Support

This was a fun experiment I wrote on my commute and my lunch break, and I spent two hours on it, tops.

I'm not planning to spend lots more time on it.



## License

MIT.
