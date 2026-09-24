#!/usr/bin/env python3
"""Exact centered-triangle LP, rounding, and directly checkable packings.

Standard library only. The universal theorems are in PROOF.md. The dense
Fraction simplex is an audit implementation, not a large-instance LP engine.
"""
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations


def rank(matrix):
    a = [[Q(x) for x in row] for row in matrix]
    if not a:
        return 0
    r = 0
    for c in range(len(a[0])):
        p = next((i for i in range(r, len(a)) if a[i][c]), None)
        if p is None:
            continue
        a[r], a[p] = a[p], a[r]
        z = a[r][c]
        a[r] = [x / z for x in a[r]]
        for i in range(r + 1, len(a)):
            if a[i][c]:
                z = a[i][c]
                a[i] = [x - z * y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def lp_data(k, neighborhoods, multiplicities, base_edges=None):
    sets = [tuple(sorted(s)) for s in neighborhoods]
    assert len(sets) == len(multiplicities)
    assert all(len(set(s)) == len(s) and all(0 <= v < k for v in s) for s in sets)
    assert all(isinstance(m, int) and m >= 1 for m in multiplicities)
    es = sorted(combinations(range(k), 2) if base_edges is None else base_edges)
    assert len(set(es)) == len(es) and all(0 <= u < v < k for u, v in es)
    edge_ids = {e: j for j, e in enumerate(es)}
    degrees = [(i, v) for i, s in enumerate(sets) for v in s]
    degree_ids = {x: len(es) + j for j, x in enumerate(degrees)}
    variables = [(i, u, v) for i, s in enumerate(sets)
                 for u, v in combinations(s, 2) if (u, v) in edge_ids]
    columns = [(edge_ids[u, v], degree_ids[i, u], degree_ids[i, v])
               for i, u, v in variables]
    rhs = [1] * len(es) + [multiplicities[i] for i, _ in degrees]
    return es, degrees, variables, columns, rhs


def centered_lp(k, neighborhoods, multiplicities, base_edges=None):
    data = lp_data(k, neighborhoods, multiplicities, base_edges)
    es, degrees, variables, columns, rhs = data
    n, m = len(columns), len(rhs)
    rows = [[Q(i in column) for column in columns]
            + [Q(i == j) for j in range(m)] + [Q(rhs[i])] for i in range(m)]
    objective = [-Q(1)] * n + [Q(0)] * (m + 1)
    basis = list(range(n, n + m))
    pivots = 0
    while any(x < 0 for x in objective[:-1]):
        enter = next(j for j, x in enumerate(objective[:-1]) if x < 0)
        choices = [i for i in range(m) if rows[i][enter] > 0]
        assert choices, 'unexpected unbounded packing LP'
        leave = min(choices, key=lambda i: (rows[i][-1] / rows[i][enter], basis[i]))
        z = rows[leave][enter]
        rows[leave] = [x / z for x in rows[leave]]
        for i in range(m):
            if i != leave and rows[i][enter]:
                z = rows[i][enter]
                rows[i] = [x - z * y for x, y in zip(rows[i], rows[leave])]
        z = objective[enter]
        objective = [x - z * y for x, y in zip(objective, rows[leave])]
        basis[leave] = enter
        pivots += 1
        assert pivots < 100000
    primal = [Q(0)] * n
    for i, b in enumerate(basis):
        if b < n:
            primal[b] = rows[i][-1]
    result = dict(primal=primal, dual=objective[n:n + m], value=objective[-1],
                  variables=variables, pivots=pivots)
    verify_lp(k, neighborhoods, multiplicities, result, base_edges)
    return result


def verify_lp(k, neighborhoods, multiplicities, result, base_edges=None):
    """Recompute loads by (type, endpoints), and check primal/dual + rank."""
    es, degrees, variables, columns, rhs = lp_data(
        k, neighborhoods, multiplicities, base_edges)
    x, dual = result['primal'], result['dual']
    assert result['variables'] == variables and len(x) == len(variables)
    assert len(dual) == len(rhs) and all(v >= 0 for v in x + dual)
    base_loads = {(u, v): Q(0) for u, v in es}
    spoke_loads = {(i, v): Q(0) for i, v in degrees}
    for (i, u, v), w in zip(variables, x):
        base_loads[u, v] += w
        spoke_loads[i, u] += w
        spoke_loads[i, v] += w
    loads = list(base_loads.values()) + list(spoke_loads.values())
    assert all(w <= cap for w, cap in zip(loads, rhs))
    assert all(sum(dual[row] for row in column) >= 1 for column in columns)
    assert sum(x) == sum(d * b for d, b in zip(dual, rhs)) == result['value']
    support = [j for j, w in enumerate(x) if w]
    active = [i for i, w in enumerate(loads) if w == rhs[i]]
    assert rank([[int(i in columns[j]) for j in support] for i in active]) == len(support)
    return True


def edge_coloring(k, edges):
    """Delta+1 coloring by fans and alternating paths (Misra--Gries)."""
    edges = sorted(edges)
    adj = [set() for _ in range(k)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    palette = set(range(1 + max(map(len, adj), default=0)))
    colors = {}
    key = lambda u, v: (min(u, v), max(u, v))
    def used(v):
        return {colors[key(v, w)] for w in adj[v] if key(v, w) in colors}
    for root, first in edges:
        assert (root, first) not in colors
        fan = [first]
        while True:
            free = palette - used(fan[-1])
            nxt = next((v for v in sorted(adj[root]) if v not in fan
                        and colors.get(key(root, v), -1) in free), None)
            if nxt is None:
                break
            fan.append(nxt)
        c, d = min(palette - used(root)), min(palette - used(fan[-1]))
        path, vertex, expected = [], root, d
        if c != d:
            while True:
                nxt = next((v for v in sorted(adj[vertex])
                            if colors.get(key(vertex, v), -1) == expected), None)
                if nxt is None:
                    break
                path.append(key(vertex, nxt))
                vertex, expected = nxt, c if expected == d else d
                assert len(path) <= k
        for e in path:
            colors[e] = c if colors[e] == d else d
        assert d not in used(root)
        endpoint = None
        for j, v in enumerate(fan):
            if j and colors[key(root, v)] in used(fan[j - 1]):
                break
            if d not in used(v):
                endpoint = j
                break
        assert endpoint is not None
        replacements = [colors[key(root, fan[j + 1])] for j in range(endpoint)]
        for j, color in enumerate(replacements):
            colors[key(root, fan[j])] = color
        colors[key(root, fan[endpoint])] = d
    verify_coloring(k, edges, colors)
    return colors


def verify_coloring(k, edges, colors):
    assert set(colors) == set(edges)
    degree = Counter(v for e in edges for v in e)
    delta = max(degree.values(), default=0)
    assert all(isinstance(c, int) and 0 <= c <= delta for c in colors.values())
    for v in range(k):
        incident = [colors[e] for e in edges if v in e]
        assert len(set(incident)) == len(incident)


def round_centered(k, neighborhoods, multiplicities, result, base_edges=None):
    verify_lp(k, neighborhoods, multiplicities, result, base_edges)
    assigned = [set() for _ in neighborhoods]
    bad = set()
    for (i, u, v), w in zip(result['variables'], result['primal']):
        if w == 1:
            assigned[i].add((u, v))
        elif w:
            bad.add((u, v))
    incidence = sum(map(len, neighborhoods))
    assert len(bad) <= incidence
    floor_size = sum(map(len, assigned))
    assert result['value'] - floor_size <= len(bad)
    triangles = []
    next_center = k
    coloring_loss = 0
    for i, es in enumerate(assigned):
        m = multiplicities[i]
        assert all(sum(v in e for e in es) <= m for v in neighborhoods[i])
        colors = edge_coloring(k, es)
        counts = Counter(colors.values())
        keep = sorted(counts, key=lambda c: (-counts[c], c))[:m]
        centers = {c: next_center + j for j, c in enumerate(keep)}
        kept = [(centers[c], u, v) for (u, v), c in colors.items() if c in centers]
        coloring_loss += len(es) - len(kept)
        triangles.extend(kept)
        next_center += m
    assert coloring_loss <= Q(incidence, 2)
    assert len(triangles) >= result['value'] - Q(3 * incidence, 2)
    verify_packing(k, neighborhoods, multiplicities, triangles, base_edges)
    return triangles, dict(fractional_base_edges=len(bad), floor_size=floor_size,
                           coloring_loss=coloring_loss)


def verify_packing(k, neighborhoods, multiplicities, triangles, base_edges=None):
    es = set(combinations(range(k), 2) if base_edges is None else base_edges)
    next_center = k
    for s, m in zip(neighborhoods, multiplicities):
        for center in range(next_center, next_center + m):
            es.update((v, center) for v in s)
        next_center += m
    used = set()
    for triangle in triangles:
        assert len(set(triangle)) == 3
        te = set(combinations(sorted(triangle), 2))
        assert te <= es and not (used & te)
        used |= te
    return True


def add_clique_triangles(k, centered):
    used = {tuple(sorted(v for v in t if v < k)) for t in centered}
    es = set(combinations(range(k), 2)) - used
    counts = [0] * k
    for t in combinations(range(k), 3):
        if set(combinations(t, 2)) <= es:
            counts[sum(t) % k] += 1
    color = max(range(k), key=lambda c: counts[c])
    extra = []
    for u, v in sorted(es):
        w = (color - u - v) % k
        if w > v and (u, w) in es and (v, w) in es:
            extra.append((u, v, w))
    assert len(extra) == counts[color]
    return centered + extra


def residual_bound(k, h):
    q = k * (k - 1) // 2
    e = q - h
    return h + Q(e * (4 * e - k * k), 3 * k * k)


def saturated_gap_bound(k, r):
    return (Q(k * k, 66) - (Q(1, 2) + Q(12 * r, 11)) * k
            + Q(5, 12) - 4 * r - Q(48 * r * r, 11))


def local_saturation(k, neighborhoods, multiplicities):
    """Exact sufficient condition; false does not imply LP infeasibility."""
    if any(len(s) < 2 for s in neighborhoods):
        return False
    return all(sum((Q(m, len(s) - 1) for s, m in zip(neighborhoods, multiplicities)
                    if u in s and v in s), Q(0)) <= 1
               for u, v in combinations(range(k), 2))
