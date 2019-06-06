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
])
def test_blocks_calling_positional_only_arg_as_kwarg(function, args, kwargs):
    with pytest.raises(TypeError) as exc:
        function(*args, **kwargs)

    assert exc.value.args[0].startswith("You can only pass")
    assert exc.value.args[0].endswith("as a positional parameter")


@pytest.mark.parametrize("function, args, kwargs", [
    (doubler,       (),             {"x": 1, "y": 2, "z": 3}),
])
def test_blocks_calling_multiple_positional_only_arg_as_kwarg(function, args, kwargs):
    with pytest.raises(TypeError) as exc:
        function(*args, **kwargs)

    assert exc.value.args[0].startswith("You can only pass")
    assert exc.value.args[0].endswith("as positional parameters")


@pytest.mark.parametrize("function, args, kwargs", [
    (multiplier,    (1, 2, ),       {"x": 1}),
    (multiplier,    (1, 2, ),       {"x": 1, "z": 3}),
])
def test_other_weirdness_is_still_typeerror(function, args, kwargs):
    with pytest.raises(TypeError):
        function(*args, **kwargs)


def test_errors_if_try_to_define_non_existent_positional_only_arg():

    with pytest.raises(AssertionError):
        @positional_only("a", "b", "c")
        def tupler(x, y, z):  # pragma: no cover
            return (x, y, z)

    with pytest.raises(AssertionError):
        @positional_only("a", "x")
        def lister(x, y, z):  # pragma: no cover
            return [x, y, z]


def test_attributes_preserved():
    def setter(x, y, z):  # pragma: no cover
        """Combine the arguments into a set."""
        return {x, y, z}

    pos_only_setter = positional_only("x")(setter)

    assert setter.func_defaults == pos_only_setter.func_defaults
    assert setter.func_dict == pos_only_setter.func_dict
    assert setter.func_doc == pos_only_setter.func_doc
    assert setter.func_name == pos_only_setter.func_name
