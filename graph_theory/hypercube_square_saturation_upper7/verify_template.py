#!/usr/bin/env python3
"""Audit the finite quotient and exact endpoint arithmetic, without imports
from construct.py. Finite checks supplement the universal proof in proof.md.
"""
import itertools
import json
from fractions import Fraction


def audit(q):
    chosen = {frozenset((0, v)) for v in range(1, q)}
    chosen.add(frozenset((1, 3)))
    for v in range(4, q):
        chosen.add(frozenset((1 if v % 4 in (0, 3) else 2, v)))
    cycles = []
    covered = set()
    for a, b, c in itertools.combinations(range(q), 3):
        d = a ^ b ^ c
        if d <= c:
            continue
        for order in ((a, b, c, d), (a, b, d, c), (a, c, b, d)):
            cycle = {frozenset((order[i], order[(i + 1) % 4])) for i in range(4)}
            count = len(cycle & chosen)
            if count == 4:
                raise AssertionError(("affine square", q, order))
            if count == 3:
                covered.update(cycle - chosen)
            cycles.append(count)
    boundary_missing = {frozenset((u, v)) for u in (0, 1, 2)
                        for v in range(q) if u != v} - chosen
    assert boundary_missing <= covered
    assert len(boundary_missing) == q - 2
    assert len(chosen) == 2 * q - 4
    assert len(cycles) == q * (q - 1) * (q - 2) // 8
    for dominating in ({0}, {1, 2}):
        assert not any(edge <= dominating for edge in chosen)
        assert all(v in dominating or any(frozenset((v, w)) in chosen for w in dominating)
                   for v in range(q))
    return {"q": q, "edges": len(chosen), "affine_cycles_checked": len(cycles),
            "boundary_nonedges_checked": len(boundary_missing), "status": "VERIFIED"}


def arithmetic():
    for exponent in range(2, 61):
        q = 1 << exponent
        for p, n, expected in (
            (q, 3 * q - 3, 7 + Fraction(16, q) - Fraction(27, q * q)),
            (2 * q, 4 * q - 3, 7 + Fraction(39, 4 * q) - Fraction(27, 2 * q * q)),
        ):
            direct = (Fraction(5, 2) + Fraction(3 * n - 13, 4)
                      * (Fraction(1, p) + Fraction(1, q)) + Fraction(9 * n, p * q))
            assert direct == expected
            assert direct < 7 + Fraction(48, n + 2)
        n = 2 * q - 2
        diagonal = (Fraction(5, 2) + Fraction(3 * n - 13, 2 * q)
                    + Fraction(9 * n, q * q))
        assert diagonal == Fraction(11, 2) + Fraction(17, 2 * q) - Fraction(18, q * q)
    return {"dyadic_exponents_checked": [2, 60], "endpoint_cases": 118,
            "diagonal_cases": 59, "status": "VERIFIED"}


if __name__ == "__main__":
    print(json.dumps({"quotients": [audit(1 << t) for t in range(2, 8)],
                      "arithmetic": arithmetic(), "status": "VERIFIED"},
                     sort_keys=True, indent=2))
