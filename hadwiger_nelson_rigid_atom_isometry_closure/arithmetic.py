"""Exact arithmetic in Q(sqrt(33), i*sqrt(3), i*sqrt(11))."""

from fractions import Fraction as F

ZERO = (F(0),) * 4
ONE = (F(1), F(0), F(0), F(0))


def add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def scale(x, scalar):
    return tuple(scalar * a for a in x)


def sub(x, y):
    return add(x, scale(y, -1))


def conj(x):
    return x[0], x[1], -x[2], -x[3]


def mul(x, y):
    a, b, c, d = x
    A, B, C, D = y
    return (
        a * A + 33 * b * B - 3 * c * C - 11 * d * D,
        a * B + b * A - c * D - d * C,
        a * C + c * A + 11 * (b * D + d * B),
        a * D + d * A + 3 * (b * C + c * B),
    )


def norm(x):
    return mul(x, conj(x))


def inverse_real(x):
    a, b, c, d = x
    if c or d:
        raise ValueError("inverse_real received a nonreal element")
    denominator = a * a - 33 * b * b
    if not denominator:
        raise ZeroDivisionError
    return a / denominator, -b / denominator, F(0), F(0)
