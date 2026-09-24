#!/usr/bin/env python3
"""Exact universal identities in Q(phi)[X^+-1,Y^+-1,Z^+-1].

phi^2=phi+1, with the real embedding phi>1 used only for positivity.
There is no SymPy dependency and no numerical zero test.
"""

from fractions import Fraction as F
from hashlib import sha256
import json


def qadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def qmul(x, y):
    a, b = x
    c, d = y
    return a * c + b * d, a * d + b * c + b * d


def qpow(x, power):
    if power < 0:
        a, b = x
        norm = a * a + a * b - b * b
        if not norm:
            raise ZeroDivisionError("zero quadratic-field element")
        x = ((a + b) / norm, -b / norm)
        power = -power
    result = (F(1), F(0))
    while power:
        if power & 1:
            result = qmul(result, x)
        x = qmul(x, x)
        power //= 2
    return result


ZERO = (F(0), F(0))
ONE = (F(1), F(0))
PHI = (F(0), F(1))
ROOT5 = (F(-1), F(2))


class P:
    def __init__(self, value=0):
        if isinstance(value, dict):
            self.terms = {k: v for k, v in value.items() if v != ZERO}
        else:
            c = value if isinstance(value, tuple) else (F(value), F(0))
            self.terms = {} if c == ZERO else {(0, 0, 0): c}

    def __add__(self, other):
        other = other if isinstance(other, P) else P(other)
        result = self.terms.copy()
        for k, v in other.terms.items():
            result[k] = qadd(result.get(k, ZERO), v)
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({k: (-v[0], -v[1]) for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + -(other if isinstance(other, P) else P(other))

    def __mul__(self, other):
        other = other if isinstance(other, P) else P(other)
        result = {}
        for k, x in self.terms.items():
            for ell, y in other.terms.items():
                key = tuple(a + b for a, b in zip(k, ell))
                result[key] = qadd(result.get(key, ZERO), qmul(x, y))
        return P(result)

    __rmul__ = __mul__

    def __pow__(self, power):
        if type(power) is not int or power < 0:
            raise ValueError("polynomial exponent must be nonnegative")
        result = P(1)
        for _ in range(power):
            result = result * self
        return result


def monomial(powers, coefficient=ONE):
    return P({tuple(powers): coefficient})


def fib(expr, offset=0):
    """F_(2*(expr[0]*r+expr[1]*s+expr[2]*t+expr[3])+offset)."""
    degree = 2 * expr[3] + offset
    positive = monomial(expr[:3], qpow(PHI, degree))
    negative = monomial(tuple(-x for x in expr[:3]), qpow(PHI, -degree))
    sign = 1 if degree % 2 == 0 else -1
    return (positive - sign * negative) * P(qpow(ROOT5, -1))


def lucas(expr, offset=0):
    degree = 2 * expr[3] + offset
    sign = 1 if degree % 2 == 0 else -1
    return monomial(expr[:3], qpow(PHI, degree)) + sign * monomial(
        tuple(-x for x in expr[:3]), qpow(PHI, -degree)
    )


def k_matrix(expr):
    return [[fib(expr, 3), fib(expr, 1)], [fib(expr, 1), fib(expr, -1)]]


def multiply(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(2)), P())
             for j in range(2)] for i in range(2)]


def score(r, s, t):
    return multiply(multiply(k_matrix(r), k_matrix(s)), k_matrix(t))[1][0]


def shifted(expr, delta):
    return (*expr[:3], expr[3] + delta)


def difference(a, b):
    return tuple(x - y for x, y in zip(a, b))


def zero(label, polynomial):
    if polynomial.terms:
        raise ArithmeticError(f"unproved identity: {label}: {polynomial.terms}")


# Coefficients of UV^2, UV, U, V^2, V, 1 in the two boundary certificates.
# Entries are (rational part, phi part); all are strictly positive for phi>1.
BOUNDARY = (
    ((15, 23), (33, 54), (15, 25), (24, 17), (40, 50), (-25, 50)),
    ((38, 61), (78, 129), (40, 65), (41, 58), (75, 130), (-65, 130)),
)


def audit():
    if qmul(PHI, PHI) != (F(1), F(1)) or qpow(PHI, -1) != (F(-1), F(1)):
        raise ArithmeticError("quadratic-field arithmetic self-check")
    if qmul(ROOT5, ROOT5) != (F(5), F(0)):
        raise ArithmeticError("sqrt(5) representation self-check")
    x, y, z = (1, 0, 0, 0), (0, 1, 0, 0), (0, 0, 1, 0)
    d = difference(x, y)
    records = []

    def check(label, left, right):
        zero(label, left - right)
        records.append(label)

    check("swap first two runs", score(y, x, z) - score(x, y, z),
          2 * fib(d) * fib(z, 3))
    check("swap last two runs", score(x, z, y) - score(x, y, z),
          2 * fib(difference(y, z)) * fib(x, -1))
    check("canonical adjacent drop",
          score(x, y, z) - score(shifted(x, -1), shifted(y, 1), z),
          2 * (fib(d, -4) * fib(z, 3) + fib(d, -2) * fib(z, 1)))
    check("positive branch adjacent drop",
          score(x, z, y) - score(shifted(x, -1), z, shifted(y, 1)),
          6 * fib(d, -4) * fib(z, 1))
    check("negative branch crossing",
          score(x, y, z) - score(shifted(y, 1), shifted(x, -1), z),
          2 * fib(d, -2) * fib(z, 1))

    # Here X=lambda^z, Y=lambda^n; epsilon=1,2 and n>=1 in the proof.
    for epsilon in (1, 2):
        delta = score((1, 2, 0, epsilon), x, (1, 1, 0, 0)) - score(
            (1, 3, 0, epsilon - 1), shifted(x, 1), x)
        rhs = (2 * fib(x, 1) * (4 * lucas((0, 3, 0, 0), 2 * epsilon - 5)
                               + 3 * lucas(y, 2 * epsilon - 2))
               + 10 * fib(x) * fib((0, 3, 0, 0), 2 * epsilon - 4))
        check(f"long bridge epsilon={epsilon}", 5 * delta, rhs)

    # Now X=lambda^z and Y=lambda^(d-2), so U=X^2-1,V=Y^2-1 are nonnegative.
    U = monomial((2, 0, 0)) - 1
    V = monomial((0, 2, 0)) - 1
    basis = (U * V**2, U * V, U, V**2, V, P(1))
    for parity, coefficients in enumerate(BOUNDARY):
        delta = score((1, 1, 0, 2 + parity), (1, 1, 0, 2), x) - score(
            (1, 2, 0, 2 + parity), shifted(x, 1), shifted(x, 1))
        scaled = delta * monomial((1, 2, 0)) * P(qmul((F(5, 2), F(0)), ROOT5))
        expected = sum((term * P((F(a), F(b)))
                        for term, (a, b) in zip(basis, coefficients)), P())
        check(f"layer boundary parity={parity}", scaled, expected)
        if not all(b >= 0 and a + b > 0 for a, b in coefficients):
            raise ArithmeticError("boundary positivity certificate fails")

    # A corrupted identity must fail, including under python -O.
    try:
        zero("deliberately corrupt", P(1))
    except ArithmeticError:
        pass
    else:
        raise ArithmeticError("zero checker accepts a nonzero polynomial")
    data = {"identities": records, "boundary_coefficients": BOUNDARY}
    digest = sha256(json.dumps(data, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"universal_identities": len(records), "positive_boundary_terms": 12,
            "certificate_sha256": digest}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True, indent=2))
