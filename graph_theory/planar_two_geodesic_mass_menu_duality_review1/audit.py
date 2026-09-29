#!/usr/bin/env python3
"""Independent bounded-integer audit of finite-menu mass duality.

The target uses rational basis enumeration. This checker instead enumerates
integer witnesses within the stated bounds and uses explicit incidence data.
"""

from itertools import combinations, product


def three_by_three():
    masses = list(product(range(1, 7), repeat=3))
    coeffs = [(a, b, c) for total in range(1, 25)
              for a in range(total + 1)
              for b in range(total - a + 1)
              for c in (total - a - b,)]
    assert len(coeffs) == 2924
    duals = primals = 0
    for sets in product(range(8), repeat=3):
        primal = any(all(2 * sum(w[v] for v in range(3) if S >> v & 1) > sum(w)
                         for S in sets) for w in masses)
        dual = any(all(2 * sum(a[i] for i, S in enumerate(sets) if S >> v & 1)
                           <= sum(a) for v in range(3)) for a in coeffs)
        assert primal != dual, sets
        primals += primal
        duals += dual
    assert (duals, primals) == (337, 175)
    return duals, primals


def fano():
    lines = ({1, 2, 3}, {1, 4, 5}, {1, 6, 7}, {2, 4, 6},
             {2, 5, 7}, {3, 4, 7}, {3, 5, 6})
    assert len(lines) == 7 and all(len(L) == 3 for L in lines)
    assert all(sum(v in L for L in lines) == 3 for v in range(1, 8))
    assert all(len(A & B) == 1 for A, B in combinations(lines, 2))
    four = next((ids for ids in combinations(range(7), 4)
                 if max(sum(v in lines[i] for i in ids)
                        for v in range(1, 8)) <= 2), None)
    assert four is not None
    # One or two lines always meet. For three, either a common vertex sees
    # all the mass, or three distinct pair intersections give 2A <= 3A/2.
    for ids in combinations(range(7), 3):
        pair_points = [next(iter(lines[i] & lines[j]))
                       for i, j in combinations(ids, 2)]
        assert len(set(pair_points)) in (1, 3)
    checked = 0
    for w in product(range(3), repeat=7):
        W = sum(w)
        assert min(sum(w[v - 1] for v in L) for L in lines) * 2 <= W
        checked += 1
    assert checked == 2187
    return four, checked


def planar_star():
    # Centre 0 and five leaves. Each menu pair is two leaf-to-leaf
    # geodesics covering four leaves and the centre, leaving one singleton.
    leaves = set(range(1, 6))
    menu = []
    for left_out in leaves:
        covered = sorted(leaves - {left_out})
        paths = ((covered[0], 0, covered[1]),
                 (covered[2], 0, covered[3]))
        assert set(paths[0]) | set(paths[1]) == set(range(6)) - {left_out}
        menu.append((paths, {left_out}))
    # Choose any two distinct residual singleton components with unit
    # coefficients: total A=2 and each vertex incidence at most one.
    assert all(2 * sum(v in C for _, C in menu[:2]) <= 2
               for v in range(6))
    checked = 0
    for w in product(range(3), repeat=6):
        assert min(sum(w[v] for v in C) for _, C in menu) * 2 <= sum(w)
        checked += 1
    assert checked == 729
    return len(menu), checked


if __name__ == '__main__':
    print('three_by_three_dual_primal=', three_by_three())
    print('fano_four_support_and_masses=', fano())
    print('planar_star_menu_and_masses=', planar_star())
    print('PASS')
