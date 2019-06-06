# positional-only-arguments

This is a proof-of-concept decorator that lets you specify positional-only parameters in Python.

For example:

```python
from posonly_params import positional_only


@positional_only("x")
def adder(x, y, z):
    return x + y + z


adder(1, 2, 3)
// 6

adder(x=1, y=2, z=3)
// TypeError: You can only pass x as a positional parameter
```



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




## Tests

You can run the tests with pytest and coverage:

```console
$ pip install pytest-cov
$ coverage run -m py.test tests.py; coverage report
```



## License

MIT.
