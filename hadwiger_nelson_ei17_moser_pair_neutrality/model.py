"""Exact interval model for the frozen EI17--Moser Minkowski support."""

from __future__ import annotations

from fractions import Fraction as F
from hashlib import sha256
from importlib import import_module
from itertools import combinations
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EI = ROOT / "hadwiger_nelson_ei17_common_pair"
DEPENDENCIES = {
    "intervals.py": "0fb646ef2fccf68334e6c0d80d1b2f7210a73a1f0135030a15ccf02c1d5b3ce7",
    "seed.py": "9ec359a35d352b1947d87516df918135eb83658a2125ccfc6515dcbff907e833",
    "seed_edges.json": "b77a3a242467f2c1ed3f047914492e70a0da9cbe6ca8234941c8dd008e25e450",
    "seed_midpoint.json": "fb712ad09168fa51814556641f31280acc8ad1e71a17a9878d1cfd55eeb96565",
}


def need(test, message):
    if not test:
        raise ValueError(message)


def check_dependencies():
    for name, expected in DEPENDENCIES.items():
        need(sha256((EI / name).read_bytes()).hexdigest() == expected,
             f"EI17 dependency hash: {name}")


check_dependencies()
sys.path.insert(0, str(EI))
try:
    intervals = import_module("intervals")
    seed = import_module("seed")
finally:
    sys.path.pop(0)

I = intervals.I


def real(a=0, b=0, c=0, d=0):
    return tuple(map(F, (a, b, c, d)))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    answer = [F(0)] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            answer[i ^ j] += x * y * (3 if i & j & 1 else 1) * (11 if i & j & 2 else 1)
    return tuple(answer)


def exact_moser():
    points = [
        (real(), real()),
        (real(1), real()),
        (real(F(1, 2)), real(0, F(1, 2))),
        (real(F(3, 2)), real(0, F(1, 2))),
        (real(F(5, 6)), real(0, 0, F(1, 6))),
        (real(F(5, 12), 0, 0, F(-1, 12)), real(0, F(5, 12), F(1, 12))),
        (real(F(5, 4), 0, 0, F(-1, 12)), real(0, F(5, 12), F(1, 4))),
    ]
    edges = []
    for a, b in combinations(range(7), 2):
        dx, dy = (sub(points[a][k], points[b][k]) for k in range(2))
        if add(mul(dx, dx), mul(dy, dy)) == real(1):
            edges.append((a, b))
    need(len(edges) == 11, "Moser edge count")
    return tuple(points), tuple(edges)


def interval_moser():
    z = I.rational(0)
    one = I.rational(1)
    half = I.rational(F(1, 2))
    s3 = I.rational(3).sqrt()
    s11 = I.rational(11).sqrt()
    s33 = I.rational(33).sqrt()
    return (
        (z, z),
        (one, z),
        (half, s3 * half),
        (I.rational(F(3, 2)), s3 * half),
        (I.rational(F(5, 6)), s11 * I.rational(F(1, 6))),
        (I.rational(F(5, 12)) - s33 * I.rational(F(1, 12)),
         s3 * I.rational(F(5, 12)) + s11 * I.rational(F(1, 12))),
        (I.rational(F(5, 4)) - s33 * I.rational(F(1, 12)),
         s3 * I.rational(F(5, 12)) + s11 * I.rational(F(1, 4))),
    )


HORIZONTAL_EI = ((1, 9), (2, 11), (5, 15), (10, 16))
MOSER_TRANSLATES = ((0, 1), (2, 3))
RHOMBI = ((5, 10, 16, 15), (1, 5, 15, 9), (1, 2, 11, 9))
EXTRA_CONTACT_IDENTITY = (
    (1, (0, 3, 12, 7)),
    (-1, (1, 2, 11, 9)),
    (-1, (2, 4, 8, 6)),
    (1, (3, 12, 16, 13)),
    (-1, (4, 7, 14, 13)),
    (1, (8, 9, 11, 10)),
)


def quotient_classes():
    parent = list(range(119))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[max(a, b)] = min(a, b)

    for low, high in HORIZONTAL_EI:
        for left, right in MOSER_TRANSLATES:
            union(7 * low + right, 7 * high + left)
    groups = {}
    for address in range(119):
        groups.setdefault(find(address), []).append(address)
    classes = tuple(tuple(group) for _, group in sorted(groups.items()))
    class_of = {address: k for k, group in enumerate(classes) for address in group}
    return classes, class_of


def build():
    ei_points, root = seed.certify()
    ei_edges = tuple(map(tuple, json.loads((EI / "seed_edges.json").read_text())))
    ei_edge_set = set(ei_edges)
    for cycle in RHOMBI:
        need(all(tuple(sorted((cycle[k], cycle[(k + 1) % 4]))) in ei_edge_set
                 for k in range(4)), f"missing rhombus edge: {cycle}")
        need(all(intervals.squared_distance(ei_points[a], ei_points[b]).lo > 0
                 for a, b in combinations(cycle, 2)), f"degenerate rhombus: {cycle}")
    need(ei_points[10][0].lo == ei_points[10][0].hi == -intervals.Q and
         ei_points[10][1].lo == ei_points[10][1].hi == 0 and
         ei_points[16][0].lo == ei_points[16][0].hi == 0 and
         ei_points[16][1].lo == ei_points[16][1].hi == 0,
         "pinned EI17 edge")
    identity = [0] * 17
    for coefficient, (a, b, c, d) in EXTRA_CONTACT_IDENTITY:
        need(all(tuple(sorted((u, v))) in ei_edge_set
                 for u, v in ((a, b), (b, c), (c, d), (d, a))),
             f"missing extra-contact rhombus edge: {(a,b,c,d)}")
        need(all(intervals.squared_distance(ei_points[u], ei_points[v]).lo > 0
                 for u, v in combinations((a, b, c, d), 2)),
             f"degenerate extra-contact rhombus: {(a,b,c,d)}")
        for vertex, sign in ((a, 1), (c, 1), (b, -1), (d, -1)):
            identity[vertex] += coefficient * sign
    target = [0] * 17
    for vertex, sign in ((0, 1), (16, 1), (10, -1), (1, -1),
                         (14, -1), (6, 1)):
        target[vertex] += sign
    need(identity == target, "extra-contact rhombus telescoping identity")

    exact_m, moser_edges = exact_moser()
    del exact_m
    m_points = interval_moser()
    classes, class_of = quotient_classes()
    points = []
    for group in classes:
        address = group[0]
        i, j = divmod(address, 7)
        points.append(tuple(ei_points[i][k] + m_points[j][k] for k in range(2)))

    edges = set()
    for a, b in ei_edges:
        for j in range(7):
            edges.add(tuple(sorted((class_of[7 * a + j], class_of[7 * b + j]))))
    for a, b in moser_edges:
        for i in range(17):
            edges.add(tuple(sorted((class_of[7 * i + a], class_of[7 * i + b]))))
    for left, right in MOSER_TRANSLATES:
        edges.add(tuple(sorted((class_of[right], class_of[7 + left]))))
    need(all(a < b for a, b in edges), "unit edge contracted")

    gap = separation = None
    for a, b in combinations(range(len(points)), 2):
        d2 = intervals.squared_distance(points[a], points[b])
        need(d2.lo > 0, f"unexcluded collision: {a},{b}")
        separation = d2.lo if separation is None else min(separation, d2.lo)
        if (a, b) in edges:
            need(d2.contains(1), f"inherited edge interval mismatch: {a},{b}")
        else:
            need(not d2.contains(1), f"unresolved extra unit edge: {a},{b}")
            local = min(abs(d2.lo - intervals.Q), abs(d2.hi - intervals.Q))
            gap = local if gap is None else min(gap, local)

    edges = tuple(sorted(edges))
    canonical = {"classes": classes, "edges": edges}
    graph_hash = sha256((json.dumps(canonical, separators=(",", ":")) + "\n").encode()).hexdigest()
    return {
        "classes": classes,
        "edges": edges,
        "points": tuple(points),
        "graph_sha256": graph_hash,
        "root": root,
        "interval_denominator": str(intervals.Q),
        "squared_separation_lower": str(F(separation, intervals.Q)),
        "nonedge_squared_unit_gap_lower": str(F(gap, intervals.Q)),
    }


if __name__ == "__main__":
    graph = build()
    print(json.dumps({k: v for k, v in graph.items() if k not in ("points", "edges", "classes")},
                     indent=2, sort_keys=True))
