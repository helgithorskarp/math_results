#!/usr/bin/env python3
"""Exact unit-distance-graph tooling over K = Q(sqrt3, sqrt5, sqrt11).

Functions operate on lists of exact points (pairs of 8-tuples of Fractions).
Unit-distance tests use integer arithmetic after scaling all coordinates to a
common denominator.  Completion points are enumerated exactly with the
recursive square-root test of kfield.  Colouring searches use PySAT only to
find witnesses, which are validated directly before being returned.
"""
from __future__ import annotations
import json, sys, time
from fractions import Fraction
from math import lcm
from pathlib import Path
from multiprocessing import Pool

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import kfield as kf

K = 3
FOUR = kf.const(K, 4)
HALF = Fraction(1, 2)
_G = {}


# ---------------------------------------------------------------- points I/O

def points_to_json(points):
    return [[kf.to_strings(x), kf.to_strings(y)] for x, y in points]


def points_from_json(data):
    return [(kf.from_strings(x), kf.from_strings(y)) for x, y in data]


def point_key(p):
    return (tuple(p[0]), tuple(p[1]))


# ------------------------------------------------------------- exact edges

def imul(x, y):
    out = [0] * 8
    for sx, a in enumerate(x):
        if not a:
            continue
        for sy, b in enumerate(y):
            if not b:
                continue
            c = a * b
            common = sx & sy
            if common & 1:
                c *= 3
            if common & 2:
                c *= 5
            if common & 4:
                c *= 11
            out[sx ^ sy] += c
    return out


def scale_points(points):
    den = 1
    for x, y in points:
        for c in x + y:
            den = lcm(den, c.denominator)
    scaled = [([int(c * den) for c in x], [int(c * den) for c in y]) for x, y in points]
    return scaled, den


def _edges_init(scaled, den):
    _G['pts'] = scaled
    _G['one'] = [den * den, 0, 0, 0, 0, 0, 0, 0]


def _edges_row(i):
    pts, one = _G['pts'], _G['one']
    xi, yi = pts[i]
    out = []
    for j in range(i + 1, len(pts)):
        xj, yj = pts[j]
        dx = [a - b for a, b in zip(xi, xj)]
        dy = [a - b for a, b in zip(yi, yj)]
        s = imul(dx, dx)
        t = imul(dy, dy)
        if [a + b for a, b in zip(s, t)] == one:
            out.append(j)
    return i, out


def unit_edges(points, workers=8):
    """All pairs at exact unit distance (strict unit-distance graph)."""
    if len(set(point_key(p) for p in points)) != len(points):
        raise ValueError('duplicate points')
    scaled, den = scale_points(points)
    edges = []
    with Pool(workers, initializer=_edges_init, initargs=(scaled, den)) as pool:
        for i, js in pool.imap_unordered(_edges_row, range(len(points)), chunksize=16):
            edges.extend((i, j) for j in js)
    return sorted(edges)


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


# ------------------------------------------------------ completion points

def _cp_init(points):
    _G['points'] = points


def _cp_row(i):
    pts = _G['points']
    xi, yi = pts[i]
    out = {}
    rational = 0
    for j in range(i + 1, len(pts)):
        xj, yj = pts[j]
        dx = kf.sub(xi, xj)
        dy = kf.sub(yi, yj)
        d2 = kf.add(kf.mul(dx, dx, K), kf.mul(dy, dy, K))
        rho2 = kf.mul(kf.sub(FOUR, d2), kf.inv(kf.scale(d2, 4), K), K)
        r = kf.field_sqrt(rho2, K)
        if r is None:
            continue
        rational += 1
        mx = kf.scale(kf.add(xi, xj), HALF)
        my = kf.scale(kf.add(yi, yj), HALF)
        rwx = kf.mul(r, kf.neg(dy), K)
        rwy = kf.mul(r, dx, K)
        for s in (1, -1):
            q = (kf.add(mx, kf.scale(rwx, s)), kf.add(my, kf.scale(rwy, s)))
            out.setdefault(q, set()).update((i, j))
    return rational, out


def _scan_point(q):
    pts = _G['points']
    one = kf.one(K)
    res = []
    for idx, p in enumerate(pts):
        dx = kf.sub(q[0], p[0])
        dy = kf.sub(q[1], p[1])
        if kf.add(kf.mul(dx, dx, K), kf.mul(dy, dy, K)) == one:
            res.append(idx)
    return res


def completion_points(points, edges, workers=8, min_neighbors=3):
    """Exact enumeration of all points of the plane (outside the vertex set)
    at unit distance from >= min_neighbors (>= 3 required for completeness
    of the K-rational restriction) of the given points."""
    n = len(points)
    adj = adjacency(n, edges)
    merged = {}
    rational_pairs = 0
    with Pool(workers, initializer=_cp_init, initargs=(points,)) as pool:
        for rational, out in pool.imap_unordered(_cp_row, range(n), chunksize=4):
            rational_pairs += rational
            for q, gens in out.items():
                merged.setdefault(q, set()).update(gens)
    index = {point_key(p): i for i, p in enumerate(points)}
    recovered = 0
    for q, gens in merged.items():
        if q in index:
            recovered += 1
            if gens != adj[index[q]]:
                raise ValueError('vertex neighbourhood not reproduced by circle intersections')
    if recovered != sum(1 for v in range(n) if len(adj[v]) >= 2):
        raise ValueError('not every vertex of degree >= 2 was recovered')
    completion = {q: gens for q, gens in merged.items() if q not in index}
    hist = {}
    for gens in completion.values():
        hist[len(gens)] = hist.get(len(gens), 0) + 1
    selected = [(q, sorted(gens)) for q, gens in completion.items() if len(gens) >= min_neighbors]
    with Pool(workers, initializer=_cp_init, initargs=(points,)) as pool:
        scans = pool.map(_scan_point, [q for q, _ in selected], chunksize=8)
    for (q, gens), sc in zip(selected, scans):
        if sc != gens:
            raise ValueError('full exact rescan disagrees with generating pairs')
    records = []
    for q, gens in selected:
        records.append({'x': kf.to_strings(q[0]), 'y': kf.to_strings(q[1]),
                        'x_float': kf.to_float(q[0]), 'y_float': kf.to_float(q[1]), 'neighbors': gens})
    records.sort(key=lambda r: (-len(r['neighbors']), r['x_float'], r['y_float']))
    return {
        'vertices': n, 'edges': len(edges), 'pairs_total': n * (n - 1) // 2,
        'pairs_with_K_rational_intersection': rational_pairs,
        'distinct_K_points_on_two_or_more_unit_circles_excluding_vertices': len(completion),
        'histogram_by_neighbors': {str(k): v for k, v in sorted(hist.items())},
        'q3_count': sum(1 for _, g in selected if len(g) >= 3),
        'q4_count': sum(1 for _, g in selected if len(g) >= 4),
        'points': records,
    }


# --------------------------------------------------------------- colouring

def color_var(v, c, k=4):
    return v * k + c + 1


def validate_coloring(n, edges, coloring, k, deleted=()):
    deleted = set(deleted)
    for v, c in enumerate(coloring):
        if v in deleted:
            if c != -1:
                raise ValueError('deleted vertex coloured')
        elif not 0 <= c < k:
            raise ValueError('invalid colour')
    for a, b in edges:
        if a not in deleted and b not in deleted and coloring[a] == coloring[b]:
            raise ValueError(f'monochromatic edge {(a, b)}')


def triangle_avoiding(n, edges, deleted=()):
    adj = adjacency(n, edges)
    deleted = set(deleted)
    for a, b in edges:
        if a in deleted or b in deleted:
            continue
        for w in sorted(adj[a] & adj[b]):
            if w not in deleted:
                return a, b, w
    raise ValueError('no triangle')


def solve_coloring(n, edges, k, deleted=(), solver_name='cadical195', pin=True, extra_clauses=()):
    """Return a validated proper k-colouring of the graph minus `deleted`, or None."""
    from pysat.solvers import Solver
    deleted = set(deleted)
    clauses = [[color_var(v, c, k) for c in range(k)] for v in range(n) if v not in deleted]
    for a, b in edges:
        if a not in deleted and b not in deleted:
            for c in range(k):
                clauses.append([-color_var(a, c, k), -color_var(b, c, k)])
    if pin:
        for c, v in enumerate(triangle_avoiding(n, edges, deleted)):
            clauses.append([color_var(v, c, k)])
    clauses.extend(list(cl) for cl in extra_clauses)
    with Solver(name=solver_name, bootstrap_with=clauses) as s:
        if not s.solve():
            return None
        pos = {l for l in s.get_model() if l > 0}
    coloring = []
    for v in range(n):
        if v in deleted:
            coloring.append(-1)
            continue
        sel = [c for c in range(k) if color_var(v, c, k) in pos]
        if not sel:
            raise ValueError('uncoloured vertex in model')
        coloring.append(sel[0])
    validate_coloring(n, edges, coloring, k, deleted)
    return coloring


def rainbow(coloring, nbrs, excluded=()):
    seen = 0
    for w in nbrs:
        if w not in excluded:
            seen |= 1 << coloring[w]
    return seen == 15


# ---------------------------------------------------------------- swap search

def _swap_init(n, edges, rows, q4, solver_name):
    _G.update(n=n, edges=edges, rows=rows, q4=q4, solver=solver_name)


def _swap_run(u):
    from pysat.solvers import Solver
    n, edges, rows, q4 = _G['n'], _G['edges'], _G['rows'], _G['q4']
    X = n
    t0 = time.time()
    uncovered = [qi for qi, nb in enumerate(q4) if rainbow(rows[u], nb, (u,))]
    initial = len(uncovered)
    sel_base = (n + 1) * 4
    clauses = [[color_var(v, c) for c in range(4)] for v in range(n) if v != u]
    clauses.append([color_var(X, c) for c in range(4)])
    for a, b in edges:
        if a != u and b != u:
            for c in range(4):
                clauses.append([-color_var(a, c), -color_var(b, c)])
    for c, v in enumerate(triangle_avoiding(n, edges, (u,))):
        clauses.append([color_var(v, c)])
    for qi in uncovered:
        s = sel_base + qi + 1
        for w in q4[qi]:
            if w != u:
                for c in range(4):
                    clauses.append([-s, -color_var(X, c), -color_var(w, c)])
    colorings, swaps, calls = [], [], 0
    with Solver(name=_G['solver'], bootstrap_with=clauses) as solver:
        while uncovered:
            qi = uncovered[0]
            calls += 1
            if not solver.solve(assumptions=[sel_base + qi + 1]):
                swaps.append(qi)
                uncovered.pop(0)
                continue
            pos = {l for l in solver.get_model() if l > 0}
            coloring = []
            for v in range(n):
                if v == u:
                    coloring.append(-1)
                    continue
                sel = [c for c in range(4) if color_var(v, c) in pos]
                assert sel
                coloring.append(sel[0])
            validate_coloring(n, edges, coloring, 4, (u,))
            assert not rainbow(coloring, q4[qi], (u,))
            uncovered = [qj for qj in uncovered if rainbow(coloring, q4[qj], (u,))]
            colorings.append(coloring)
    return {'u': u, 'initial_uncovered': initial, 'sat_calls': calls, 'colorings': colorings, 'swaps': swaps, 'seconds': round(time.time() - t0, 2)}


def swap_search(n, edges, rows, q4, workers=8, solver_name='cadical195', log=None):
    """For every vertex u: witness colourings of G-u covering all q in q4, and the swap list."""
    results = [None] * n
    with Pool(workers, initializer=_swap_init, initargs=(n, edges, rows, q4, solver_name)) as pool:
        for r in pool.imap_unordered(_swap_run, range(n), chunksize=1):
            results[r['u']] = r
            if log:
                log(f"u={r['u']:3d} uncovered0={r['initial_uncovered']:4d} calls={r['sat_calls']:3d} colorings={len(r['colorings'])} swaps={r['swaps']} {r['seconds']:.1f}s")
    return results
