#!/usr/bin/env python3
"""Exact algebra and scope checks for PROOF.md; no numerical quadrature.

Python >=3.10, standard library only. The analytic theorem is the written
proof, not a finite search. Deliberate failures remain active under -O.
"""

from fractions import Fraction as F
from itertools import combinations, product
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


# A sparse polynomial ring over Q in r,q,R,Q,c,t.
NVAR = 6
ZERO = (0,) * NVAR


class P:
    def __init__(self, terms=0):
        if isinstance(terms, P):
            self.a = terms.a.copy()
        elif isinstance(terms, dict):
            self.a = {m: F(v) for m, v in terms.items() if v}
        else:
            self.a = {ZERO: F(terms)} if terms else {}

    def __add__(self, other):
        out = self.a.copy()
        for m, v in P(other).a.items():
            out[m] = out.get(m, F(0)) + v
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({m: -v for m, v in self.a.items()})

    def __sub__(self, other):
        return self + (-P(other))

    def __rsub__(self, other):
        return P(other) + (-self)

    def __mul__(self, other):
        out = {}
        for a, x in self.a.items():
            for b, y in P(other).a.items():
                m = tuple(i + j for i, j in zip(a, b))
                out[m] = out.get(m, F(0)) + x * y
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, "invalid polynomial power")
        out = P(1)
        for _ in range(n):
            out = out * self
        return out

    def dt(self):
        out = {}
        for m, a in self.a.items():
            if m[-1]:
                key = m[:-1] + (m[-1] - 1,)
                out[key] = a * m[-1]
        return P(out)


def variable(i):
    return P({tuple(int(j == i) for j in range(NVAR)): 1})


def equal_polynomials(a, b, name):
    require(not (a - b).a, "polynomial identity failed: " + name)


def symbolic_checks():
    r, q, R, Q, c, t = [variable(i) for i in range(NVAR)]
    A, B = (1-t)*r+t*R, (1-t)*q+t*Q
    direct = A**2+B**2-2*c*A*B+t*(1-t)*((r-R)-(q-Q))**2
    split = (1-t)*(r-q)**2+t*(R-Q)**2+2*A*B*(1-c)
    derivative = (R-Q)**2-(r-q)**2-2*(1-c)*((r-R)*B+(q-Q)*A)
    equal_polynomials(direct, split, "distance (5)")
    equal_polynomials(direct.dt(), derivative, "derivative (6)")
    # Distinguish a genuine identity check from a vacuous equality test.
    try:
        equal_polynomials(direct, split+t*(1-t), "intentional mutation")
    except ValueError:
        return 2, 1
    raise ValueError("mutated distance identity was accepted")


def norm2(x):
    return sum(v*v for v in x)


def minus(x, y):
    return tuple(a-b for a, b in zip(x, y))


def rank(rows):
    a = [[F(v) for v in row] for row in rows]
    if not a:
        return 0
    k = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(k, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        scale = a[k][j]
        a[k] = [v/scale for v in a[k]]
        for i in range(len(a)):
            if i != k:
                v = a[i][j]
                a[i] = [x-v*y for x, y in zip(a[i], a[k])]
        k += 1
        if k == len(a):
            break
    return k


def inversion_fold(x):
    scale = max(F(1), norm2(x))
    return tuple(v/scale for v in x)


def fixture_checks():
    zero = (F(0),)*3
    x = [zero] + [tuple(r*int(i == j) for j in range(3))
                  for i in range(3) for r in (F(1), F(3, 2), F(2))]
    y = [inversion_fold(v) for v in x]
    require(len(set(x)) == len(set(y)) == 10, "fixture not injective")
    pairs = list(combinations(range(len(x)), 2))
    old = [norm2(minus(x[i], x[j])) for i, j in pairs]
    new = [norm2(minus(y[i], y[j])) for i, j in pairs]
    require(all(a >= b for a, b in zip(old, new)), "fixture not contracting")
    pr = rank([a+b for a, b in zip(x[1:], y[1:])])
    dr = rank([minus(a, b) for a, b in zip(x, y)])
    require((pr, dr) == (6, 3), "fixture rank mismatch")
    factors = sorted({norm2(b)/norm2(a) for a, b in zip(x[1:], y[1:])})
    require(factors == [F(1,16), F(16,81), F(1)], "radial factor mismatch")
    require(min(old) == F(1,4) and max(new) == 2, "uniform boundary mismatch")
    drop = F(1,2)**2-F(1,3)**2
    scalar_bound = drop/(F(1,2)+F(1,3))**2
    require(drop == F(5,36) and scalar_bound == F(1,5), "defect arithmetic")
    require(3*scalar_bound < 1, "scalar criterion not excluded")
    return {"sites": len(x), "pairs": len(pairs), "paired_rank": pr,
            "displacement_rank": dr, "scalar_coordinate_square_bound": str(scalar_bound),
            "min_source_distance_squared": str(min(old)),
            "max_target_distance_squared": str(max(new))}


def validate_pair(r, q, R, Q):
    require(min(r, q, R, Q) >= 0, "negative radius")
    require(R <= r and Q <= q, "outward radial movement")
    require(abs(R-Q) <= abs(r-q), "radial Lipschitz condition")


def triangular(r):
    z = r % 2
    return min(z, 2-z)


def profile_checks():
    profiles = [lambda r: r, lambda r: F(0), lambda r: r/3,
                lambda r: r if r <= 1 else 1/r, triangular]
    radii = [F(i,4) for i in range(17)]
    angles = [F(-1), F(-1,2), F(0), F(1,2), F(1)]
    times = [F(0), F(1,4), F(1,2), F(3,4), F(1)]
    count = 0
    for rho, r, q in product(profiles, radii, radii):
        R, Q = rho(r), rho(q)
        validate_pair(r, q, R, Q)
        for c, t in product(angles, times):
            A, B = (1-t)*r+t*R, (1-t)*q+t*Q
            derivative = (R-Q)**2-(r-q)**2-2*(1-c)*((r-R)*B+(q-Q)*A)
            require(derivative <= 0, "positive derivative in valid profile")
            count += 1
    rejected = 0
    for values in [(F(1),F(2),F(-1),F(0)),
                   (F(1),F(2),F(2),F(1)),
                   (F(1),F(2),F(0),F(2))]:
        try:
            validate_pair(*values)
        except ValueError:
            rejected += 1
        else:
            raise ValueError("false scalar hypothesis was accepted")
    return count, rejected


def main():
    identities, mutations = symbolic_checks()
    fixture = fixture_checks()
    samples, rejected = profile_checks()
    print(json.dumps({"status": "PASS", "polynomial_identities": identities,
                      "fixture": fixture, "rational_derivative_checks": samples,
                      "intentional_rejections": mutations+rejected}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
