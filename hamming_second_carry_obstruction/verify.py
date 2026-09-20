#!/usr/bin/env python3
"""Exact arithmetic audit for the thin Hamming second-carry theorem.

The universal proof is PROOF.md.  This program checks the displayed infinite
family, its majority-threshold map, the second-carry identities, and the
three possible nonlinear-core size budgets.  It deliberately performs no
box, colouring, residue-table, or normal-form enumeration.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FamilyInstance:
    s: int
    A: int
    n1: int
    m: int
    n: int
    p: int
    h: int
    Q: int


def majority_threshold(*orders: int) -> int:
    """Return ceil(degree/2) for a Hamming product with these orders."""
    degree = sum(order - 1 for order in orders)
    return (degree + 1) // 2


def make_instance(s: int, A: int) -> FamilyInstance:
    if s < 8 or s % 2:
        raise ValueError("s must be even and at least 8")
    if A < 2:
        raise ValueError("A must be at least 2")

    n1 = 2 * A * s - s // 2 + 5
    m = (A + 1) * s + 1
    n = A * s + 4
    p = s // 2
    h = majority_threshold(n1, m, n, p)
    Q = p * ((m * n) // s)
    return FamilyInstance(s, A, n1, m, n, p, h, Q)


def audit_instance(instance: FamilyInstance) -> None:
    s, A = instance.s, instance.A
    n1, m, n, p = instance.n1, instance.m, instance.n, instance.p
    h, Q = instance.h, instance.Q

    assert n1 > m >= n >= p >= 3
    assert m >= s and n >= s and p < s

    r, u = m % s, n % s
    assert (r, u) == (1, 4)
    assert r * u < s
    assert r * u * p == 2 * s
    assert 3 <= r * u < s
    assert 3 <= p <= s - 2

    assert h == 2 * A * s + s // 2 + 3
    assert h - (n1 - 1) + 1 == s
    assert h >= n1 - 1

    formula_Q = (s // 2) * (A * (A + 1) * s + 5 * A + 4)
    assert Q == formula_Q
    assert m * n * p == s * (Q + 2)
    assert (m * n) % s == r * u

    # If a Q+1-part minor partition existed, its unique nonlinear core would
    # have one of these sizes.  The remaining line-part excess is at most 2,
    # strictly below the per-layer residue ru=4.
    for nonlinear_size in (2 * s - 2, 2 * s - 1, 2 * s):
        line_excess = 2 * s - nonlinear_size
        assert 0 <= line_excess <= 2 < r * u

    # The full product has exactly Q+2 minimum class-size units.  The theorem
    # excludes Q+2 colours and the balanced lift supplies Q colours.
    total_vertices = n1 * m * n * p
    minimum_class_size = n1 * s
    assert total_vertices == minimum_class_size * (Q + 2)


def main() -> None:
    instances = []
    for s in range(8, 401, 2):
        for A in range(2, 101):
            instance = make_instance(s, A)
            audit_instance(instance)
            instances.append(instance)

    first, last = instances[0], instances[-1]
    print("thin Hamming second-carry arithmetic audit")
    print(f"family instances checked: {len(instances)}")
    print("parameter range: even 8 <= s <= 400, 2 <= A <= 100")
    print(
        "first instance: "
        f"(n1,m,n,p)=({first.n1},{first.m},{first.n},{first.p}), Q={first.Q}"
    )
    print(
        "last instance: "
        f"(n1,m,n,p)=({last.n1},{last.m},{last.n},{last.p}), Q={last.Q}"
    )
    print("nonlinear boundary budgets checked per instance: 3")
    print("all exact checks passed")


if __name__ == "__main__":
    main()
