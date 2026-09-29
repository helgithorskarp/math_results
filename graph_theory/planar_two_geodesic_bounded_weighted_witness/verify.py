"""Exact small controls for factorial-bounded weighted witness compression."""

from fractions import Fraction
from itertools import combinations
from math import factorial


def simple_paths(n, edges, s, t):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    stack = [(s, (s,), ())]
    while stack:
        u, visited, used = stack.pop()
        if u == t:
            yield visited, used
            continue
        for v, i in adj[u]:
            if v not in visited:
                stack.append((v, visited + (v,), used + (i,)))


def solve(a, b):
    """Exact square-system solver; return None for a singular matrix."""
    n = len(b)
    z = [[Fraction(x) for x in row] + [Fraction(y)] for row, y in zip(a, b)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if z[i][j]), None)
        if pivot is None:
            return None
        z[j], z[pivot] = z[pivot], z[j]
        scale = z[j][j]
        z[j] = [x / scale for x in z[j]]
        for i in range(n):
            if i != j:
                scale = z[i][j]
                z[i] = [x - scale * y for x, y in zip(z[i], z[j])]
    return [row[-1] for row in z]


def determinant(a):
    z = [[Fraction(x) for x in row] for row in a]
    n = len(z)
    det = Fraction(1)
    for j in range(n):
        pivot = next((i for i in range(j, n) if z[i][j]), None)
        if pivot is None:
            return 0
        if pivot != j:
            z[j], z[pivot] = z[pivot], z[j]
            det = -det
        p = z[j][j]
        det *= p
        for i in range(j + 1, n):
            c = z[i][j] / p
            for k in range(j, n):
                z[i][k] -= c * z[j][k]
    assert det.denominator == 1
    return int(det)


def components(n, edges, removed):
    alive = set(range(n)) - removed
    out = []
    while alive:
        comp = {next(iter(alive))}
        todo = list(comp)
        alive -= comp
        while todo:
            u = todo.pop()
            for a, b in edges:
                v = b if a == u else a if b == u else None
                if v in alive:
                    alive.remove(v)
                    comp.add(v)
                    todo.append(v)
        out.append(comp)
    return out


def diamond_control():
    edges = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 3)]
    base = (2, 3, 8, 4, 7)
    m = len(edges)
    rows = [tuple(int(i == j) for i in range(m)) for j in range(m)]
    catalog = []
    for s in range(4):
        for t in range(s + 1, 4):
            routes = list(simple_paths(4, edges, s, t))
            routes.sort(key=lambda route: sum(base[i] for i in route[1]))
            assert sum(base[i] for i in routes[0][1]) < sum(base[i] for i in routes[1][1])
            catalog.append((s, t, routes[0][0]))
            ref = set(routes[0][1])
            for route in routes[1:]:
                other = set(route[1])
                rows.append(tuple(int(i in other) - int(i in ref) for i in range(m)))
    rows = sorted(set(rows))
    best = None
    checked = 0
    for indices in combinations(range(len(rows)), m):
        basis = [rows[i] for i in indices]
        x = solve(basis, [1] * m)
        if x is None or any(sum(a * b for a, b in zip(row, x)) < 1 for row in rows):
            continue
        checked += 1
        if best is None or sum(x) < sum(best[0]):
            best = (x, basis)
    assert best is not None
    x, basis = best
    d = abs(determinant(basis))
    integer = tuple(int(d * z) for z in x)
    assert all(1 <= z <= factorial(m) for z in integer)
    assert all(sum(a * b for a, b in zip(row, integer)) >= 1 for row in rows)
    for s, t, route in catalog:
        routes = list(simple_paths(4, edges, s, t))
        routes.sort(key=lambda p: sum(integer[i] for i in p[1]))
        assert routes[0][0] == route
        assert sum(integer[i] for i in routes[0][1]) < sum(integer[i] for i in routes[1][1])
    return len(rows), checked, integer


def k9_control():
    n = 9
    edges = list(combinations(range(n), 2))
    paths = [{v} for v in range(n)] + [set(e) for e in edges]
    assert len(paths) == 45
    pairs = 0
    minimum_heavy = n
    for i, p in enumerate(paths):
        for q in paths[i:]:
            comps = components(n, edges, p | q)
            heavy = max((len(c) for c in comps), default=0)
            assert 2 * heavy > n
            minimum_heavy = min(minimum_heavy, heavy)
            pairs += 1
    assert pairs == 1035 and minimum_heavy == 5
    assert all(1 <= 1 <= factorial(n) for _ in range(n))
    return len(paths), pairs, minimum_heavy


if __name__ == "__main__":
    a = diamond_control()
    b = k9_control()
    print("diamond rows, feasible bases, bounded lengths:", a)
    print("K9 geodesics, pairs, minimum heavy size:", b)
    print("PASS")
