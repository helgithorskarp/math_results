#!/usr/bin/env python3
"""Independent exact audit of the integer-witness LP step.

Uses a four-cycle, not the target's diamond, and a separate synthetic mass
polyhedron. No target code or floating-point solver is imported.
"""

from fractions import Fraction
from itertools import combinations, permutations
from math import factorial, isqrt


def det(matrix):
    n = len(matrix)
    ans = 0
    for p in permutations(range(n)):
        inversions = sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        term = (-1) ** inversions
        for i in range(n):
            term *= matrix[i][p[i]]
        ans += term
    return ans


def vertices(rows):
    d = len(rows[0])
    best = None
    count = 0
    for basis in combinations(rows, d):
        denom = det(basis)
        if not denom:
            continue
        numer = []
        for j in range(d):
            numer.append(det([[1 if k == j else row[k] for k in range(d)]
                              for row in basis]))
        x = tuple(Fraction(z, denom) for z in numer)
        if any(sum(a * b for a, b in zip(row, x)) < 1 for row in rows):
            continue
        count += 1
        score = (sum(x), x)
        if best is None or score < best[0]:
            best = score, basis, denom, x
    assert best is not None
    _, basis, denom, x = best
    integer = tuple(int(abs(denom) * z) for z in x)
    assert all(z > 0 for z in integer)
    assert all(sum(a * b for a, b in zip(row, integer)) >= 1 for row in rows)
    assert max(integer) <= isqrt(d ** d) <= factorial(d)
    return x, integer, count


def four_cycle():
    edges = ((0, 1), (1, 2), (2, 3), (3, 0))
    base = (2, 4, 3, 6)
    adj = {v: [] for v in range(4)}
    for j, (u, v) in enumerate(edges):
        adj[u].append((v, j))
        adj[v].append((u, j))

    def paths(s, t):
        stack = [(s, (s,), ())]
        while stack:
            v, seen, used = stack.pop()
            if v == t:
                yield used
                continue
            for w, e in adj[v]:
                if w not in seen:
                    stack.append((w, seen + (w,), used + (e,)))

    rows = [tuple(int(i == j) for i in range(4)) for j in range(4)]
    chosen = {}
    for s, t in combinations(range(4), 2):
        routes = sorted(paths(s, t), key=lambda p: sum(base[e] for e in p))
        assert len(routes) == 2
        assert sum(base[e] for e in routes[0]) < sum(base[e] for e in routes[1])
        chosen[s, t] = routes[0]
        rows.append(tuple(int(e in routes[1]) - int(e in routes[0])
                          for e in range(4)))
    x, integer, count = vertices(rows)
    for st, route in chosen.items():
        assert sum(integer[e] for e in route) < sum(integer[e] for e in next(
            p for p in paths(*st) if p != route))
    return len(rows), count, integer, x


def mass_system():
    r = 4
    rows = [tuple(int(i == j) for i in range(r)) for j in range(r)]
    for C in ({0, 1}, {0, 2}, {0, 3}):
        rows.append(tuple(1 if v in C else -1 for v in range(r)))
    x, integer, count = vertices(rows)
    assert all(2 * sum(integer[v] for v in C) > sum(integer)
               for C in ({0, 1}, {0, 2}, {0, 3}))
    return count, integer, x


if __name__ == '__main__':
    c = four_cycle()
    m = mass_system()
    print('cycle_rows_feasible_bases_integer_rational=', c)
    print('mass_feasible_bases_integer_rational=', m)
    print('hadamard_bounds_dim4=', isqrt(4 ** 4), 'factorial_dim4=', factorial(4))
    print('PASS')
