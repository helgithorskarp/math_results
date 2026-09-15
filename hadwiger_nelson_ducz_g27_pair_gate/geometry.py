"""Exact physical geometry of the displayed G_27 in arXiv:2606.12325v1."""

from fractions import Fraction as F
from itertools import combinations
import hashlib

V = tuple[F, F, F, F]  # basis 1, sqrt(3), sqrt(11), sqrt(33)
ZERO: V = (F(0), F(0), F(0), F(0))
ONE: V = (F(1), F(0), F(0), F(0))


def add(a: V, b: V) -> V:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def scale(a: V, q: F) -> V:
    return tuple(q * x for x in a)  # type: ignore[return-value]


def multiply(a: V, b: V) -> V:
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (
        a0*b0 + 3*a1*b1 + 11*a2*b2 + 33*a3*b3,
        a0*b1 + a1*b0 + 11*(a2*b3 + a3*b2),
        a0*b2 + a2*b0 + 3*(a1*b3 + a3*b1),
        a0*b3 + a3*b0 + a1*b2 + a2*b1,
    )


def rational(n: int, d: int = 1) -> V:
    return (F(n, d), F(0), F(0), F(0))


SQ3: V = (F(0), F(1), F(0), F(0))
SQ11: V = (F(0), F(0), F(1), F(0))
SQ33: V = (F(0), F(0), F(0), F(1))

# omega_1=(1+i sqrt(3))/2; omega_3=(5+i sqrt(11))/6.
W1 = (rational(1, 2), scale(SQ3, F(1, 2)))
W3 = (rational(5, 6), scale(SQ11, F(1, 6)))
W13 = (
    add(rational(5, 12), scale(SQ33, F(-1, 12))),
    add(scale(SQ3, F(5, 12)), scale(SQ11, F(1, 12))),
)

# The four rows of the 4x27 integer matrix displayed in Dúcz, section 3.
ROWS = (
    (1,0,2,2,1,2,1,1,1,0,3,3,1,2,2,1,0,0,0,3,2,3,1,2,1,2,3),
    (4,4,3,3,3,3,4,2,3,4,3,2,3,3,2,3,2,3,2,0,1,1,1,1,2,2,1),
    (2,3,0,1,2,2,2,3,3,3,0,1,1,1,2,2,3,3,4,1,1,1,2,2,2,2,0),
    (0,0,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,4),
)


def point(a: int, b: int, c: int, d: int) -> tuple[V, V]:
    x = add(add(rational(a), scale(W1[0], F(b))),
            add(scale(W3[0], F(c)), scale(W13[0], F(d))))
    y = add(scale(W1[1], F(b)),
            add(scale(W3[1], F(c)), scale(W13[1], F(d))))
    return x, y


POINTS = tuple(point(*(row[j] for row in ROWS)) for j in range(27))


def squared_distance(i: int, j: int) -> V:
    dx = add(POINTS[i][0], scale(POINTS[j][0], F(-1)))
    dy = add(POINTS[i][1], scale(POINTS[j][1], F(-1)))
    return add(multiply(dx, dx), multiply(dy, dy))


EDGES = tuple((i, j) for i, j in combinations(range(27), 2)
              if squared_distance(i, j) == ONE)


def edge_sha256() -> str:
    data = "".join(f"{a} {b}\n" for a, b in EDGES).encode()
    return hashlib.sha256(data).hexdigest()
