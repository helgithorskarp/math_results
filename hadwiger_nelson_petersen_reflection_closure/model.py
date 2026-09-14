"""Producer-side exact model for the Petersen reflection closure."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction


DEG = 8
ZERO = (Fraction(0),) * DEG
ONE = (Fraction(1),) + (Fraction(0),) * (DEG - 1)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def scale(a, q):
    q = Fraction(q)
    return tuple(q * x for x in a)


def mul(a, b):
    c = [Fraction(0)] * 15
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    c[i + j] += x * y
    # Reduce by Phi_20(x)=x^8-x^6+x^4-x^2+1.
    for k in range(14, 7, -1):
        q = c[k]
        if q:
            c[k] = 0
            c[k - 2] += q
            c[k - 4] -= q
            c[k - 6] += q
            c[k - 8] -= q
    return tuple(c[:DEG])


def power(a, n):
    if n < 0:
        raise ValueError("negative exponent")
    out = ONE
    base = a
    while n:
        if n & 1:
            out = mul(out, base)
        base = mul(base, base)
        n >>= 1
    return out


X = (Fraction(0), Fraction(1)) + (Fraction(0),) * 6
XPOW = [power(X, k) for k in range(20)]


def conjugate(a):
    out = ZERO
    for k, q in enumerate(a):
        if q:
            out = add(out, scale(XPOW[(-k) % 20], q))
    return out


def is_unit_delta(a):
    return mul(a, conjugate(a)) == ONE


def petersen_points():
    """Return outer 0..4 followed by inner 0..4 in Q(zeta_20)."""
    zeta = XPOW[4]
    # c=1/(zeta-1)=-(4+3*zeta+2*zeta^2+zeta^3)/5.
    c = scale(
        add(
            add(scale(ONE, -4), scale(zeta, -3)),
            add(scale(power(zeta, 2), -2), scale(power(zeta, 3), -1)),
        ),
        Fraction(1, 5),
    )
    if mul(c, sub(zeta, ONE)) != ONE:
        raise RuntimeError("bad inverse")
    phi = add(XPOW[2], XPOW[18])
    inv_phi = sub(phi, ONE)
    if mul(phi, inv_phi) != ONE:
        raise RuntimeError("bad golden-ratio identity")
    outer = [mul(c, power(zeta, k)) for k in range(5)]
    inner = [mul(mul(mul(XPOW[5], c), inv_phi), power(zeta, k)) for k in range(5)]
    return outer + inner


def strict_edges(points):
    return [
        (i, j)
        for i in range(len(points))
        for j in range(i + 1, len(points))
        if is_unit_delta(sub(points[i], points[j]))
    ]


def reflect_round(points):
    edges = strict_edges(points)
    neighbours = [[] for _ in points]
    for u, v in edges:
        neighbours[u].append(v)
        neighbours[v].append(u)
    out = set(points)
    wedge_count = 0
    for r, ns in enumerate(neighbours):
        for p, q in itertools.combinations(ns, 2):
            x = sub(add(points[p], points[q]), points[r])
            if not is_unit_delta(sub(x, points[p])) or not is_unit_delta(sub(x, points[q])):
                raise RuntimeError("reflection identity failed")
            out.add(x)
            wedge_count += 1
    return sorted(out), edges, wedge_count


def qstr(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def point_word(p):
    return [qstr(q) for q in p]


def stream_hash(rows):
    raw = json.dumps(rows, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def restricted_growth_partitions(n, max_blocks=4):
    word = [0] * n

    def rec(pos, used):
        if pos == n:
            yield tuple(word)
            return
        for c in range(min(used + 1, max_blocks)):
            word[pos] = c
            yield from rec(pos + 1, max(used, c + 1))

    word[0] = 0
    yield from rec(1, 1)
