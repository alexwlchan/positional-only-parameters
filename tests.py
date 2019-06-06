#!/usr/bin/env python
# -*- encoding: utf-8

import pytest

from posonly_params import positional_only


@positional_only("x")
def adder(x, y, z):
    return x + y + z


@positional_only("y")
def multiplier(x, y, z):
    return x + y + z


@positional_only("x", "y")
def doubler(x, y, z):
    return (x + y + z) * 2


@pytest.mark.parametrize("function, args, kwargs", [
    (adder,         (1, ),          {"y": 2, "z": 3}),
    (adder,         (1, 2, ),       {"z": 3}),
    (adder,         (1, 2, 3, ),    {}),

    (multiplier,    (1, 2, ),       {"z": 3}),
    (multiplier,    (1, 2, 3, ),    {}),

    (doubler,       (1, 2, ),       {"z": 3}),
    (doubler,       (1, 2, 3),       {}),
])
def test_allows_calling_positional_args(function, args, kwargs):
    function(*args, **kwargs)


@pytest.mark.parametrize("function, args, kwargs", [
    (adder,         (),             {"x": 1, "y": 2, "z": 3}),

    (multiplier,    (1, ),          {"y": 2, "z": 3}),
    (multiplier,    (1, ),          {"x": 1, "y": 2, "z": 3}),

    (doubler,       (1, ),          {"y": 2, "z": 3}),
    (doubler,       (1, ),          {"x": 2, "z": 3}),
    (doubler,       (),             {"x": 1, "y": 2, "z": 3}),
])
def test_blocks_calling_positional_only_arg_as_kwarg(function, args, kwargs):
    with pytest.raises(TypeError) as exc:
        function(*args, **kwargs)

    assert exc.value.args[0].startswith("You can only pass")
    assert exc.value.args[0].endswith("as a positional parameter")


def test_errors_if_try_to_define_non_existent_positional_only_arg():

    with pytest.raises(AssertionError):
        @positional_only("a", "b", "c")
        def tupler(x, y, z):  # pragma: no cover
            return (x, y, z)

    with pytest.raises(AssertionError):
        @positional_only("a", "x")
        def lister(x, y, z):  # pragma: no cover
            return [x, y, z]
