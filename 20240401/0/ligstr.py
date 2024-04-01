"""Yammy module."""
from math import *


def genarray():
    """Is this a function? Yes, it is."""
    Array = [[
        f"This is a string {sin(i)} in the pattern {sin(j)}" for i in range(10)
    ] for j in range(10)]
    print("\n".join(Array))
