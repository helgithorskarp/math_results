#!/usr/bin/env python3
"""Exact boundary controls for the geometric exclusions."""
from itertools import combinations
import json
import verify as V

U = V.V.UNITS
ZERO, ONE = (0, 0), (1, 0)


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def negative(a):
    return -a[0], -a[1]


def norm(a):
    return a[0] ** 2 + a[0] * a[1] + a[1] ** 2


def main():
    pairs = 0
    for a, b in combinations((ZERO,) + U, 2):
        if a == ZERO or b == ZERO:
            unit = b if a == ZERO else a
            roots = [V.V.times(unit, U[2]), V.V.times(unit, U[4])]
        else:
            roots = [ZERO, negative(add(a, b))]
        V.need(all(norm(add(p, a)) == norm(add(p, b)) == 1 for p in roots), 'exact offset-circle intersections')
        pairs += 1

    # Adjacent phases must NOT be excluded by the endpoint/nonadjacent rule.
    p, q, omega = ONE, (-2, 1), (0, 1)
    V.need(norm(p) == norm(add(p, q)) == norm(add(p, V.V.times(omega, q))) == 1, 'allowed adjacent-phase example')
    V.need(norm(q) == 3 and q != ZERO and norm(add(ONE, negative(omega))) == 1, 'adjacent boundary is not a unit triangle')

    triangles = 0
    for u in U:
        for phase in (U[2], U[4]):
            p = V.V.times(u, phase)
            V.need(norm(p) == norm(u) == norm(add(p, u)) == 1, 'both unit-triangle orientations')
            triangles += 1
    print(json.dumps({'verified': True, 'constant_offset_pairs_checked': pairs,
                      'unit_triangle_orientations_checked': triangles,
                      'allowed_adjacent_phase_control': True}, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
