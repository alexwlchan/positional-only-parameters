#!/usr/bin/env python
# -*- encoding: utf-8

from posonly_params import positional_only


@positional_only("x")
def adder(x, y, z):
    return x + y + z


print(adder(1, 2, 3)  // 6)
print(adder(x=1, y=2, z=3))
