#!/usr/bin/env python3
"""Self-contained exact verifier for the O'Donnell-core difference body."""

import collections
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
CERT = json.loads((HERE / "certificate.json").read_text())
EXPECTED = json.loads((HERE / "EXPECTED.json").read_text())
N = 8
ZERO = (F(0),) * N
ONE = (F(1),) + (F(0),) * 7


def need(ok, message):
    if not ok:
        raise ValueError(message)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    c = [F(0)] * 15
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            c[i + j] += x * y
    for k in range(14, 7, -1):
        q = c[k]
        c[k] = F(0)
        c[k - 2] += 3 * q
        c[k - 4] += F(28, 5) * q
        c[k - 6] += F(11, 5) * q
        c[k - 8] -= F(1, 25) * q
    return tuple(c[:8])


def parse_element(values):
    need(len(values) == 8, "field-vector length")
    return tuple(F(x) for x in values)


def parse_point(value):
    need(len(value) == 2, "point arity")
    return parse_element(value[0]), parse_element(value[1])


def psub(a, b):
    return sub(a[0], b[0]), sub(a[1], b[1])


def norm2(a):
    return add(mul(a[0], a[0]), mul(a[1], a[1]))


def sqdist(a, b):
    return norm2(psub(a, b))


def frac(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def point_line(p):
    return " | ".join(" ".join(frac(q) for q in a) for a in p)


def digest(lines):
    h = hashlib.sha256()
    for line in lines:
        h.update((line + "\n").encode())
    return h.hexdigest()


def interval_mul(a, b):
    values = [a[i] * b[j] for i in (0, 1) for j in (0, 1)]
    return min(values), max(values)


def interval_eval(coefficients, root_interval):
    out = (F(0), F(0))
    for q in reversed(coefficients):
        out = interval_mul(out, root_interval)
        out = out[0] + q, out[1] + q
    return out


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        need(0 <= a < b < n, "edge range/order")
        adj[a].add(b)
        adj[b].add(a)
    return adj


def components(adj):
    unseen = set(range(len(adj)))
    sizes = []
    while unseen:
        root = min(unseen)
        unseen.remove(root)
        stack = [root]
        size = 0
        while stack:
            u = stack.pop()
            size += 1
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def cuts(adj):
    n = len(adj)
    tin = [-1] * n
    low = [-1] * n
    timer = 0
    arts = set()
    bridges = []

    def dfs(u, parent):
        nonlocal timer
        tin[u] = low[u] = timer
        timer += 1
        children = 0
        for v in sorted(adj[u]):
            if v == parent:
                continue
            if tin[v] >= 0:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u)
                children += 1
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    bridges.append((min(u, v), max(u, v)))
                if parent >= 0 and low[v] >= tin[u]:
                    arts.add(u)
        if parent < 0 and children > 1:
            arts.add(u)

    for u in range(n):
        if tin[u] < 0:
            dfs(u, -1)
    return sorted(arts), sorted(bridges)


def core_order(adj, k):
    alive = set(range(len(adj)))
    degree = [len(a) for a in adj]
    stack = [u for u in alive if degree[u] < k]
    while stack:
        u = stack.pop()
        if u not in alive:
            continue
        alive.remove(u)
        for v in adj[u]:
            if v in alive:
                degree[v] -= 1
                if degree[v] == k - 1:
                    stack.append(v)
    return len(alive)


def verify():
    need(CERT["schema"] == 2, "schema")
    source = [parse_point(p) for p in CERT["source_coordinates"]]
    points = [parse_point(p) for p in CERT["physical_coordinates"]]
    need(len(source) == len(set(source)) == EXPECTED["source_points"], "source order")
    need(digest(point_line(p) for p in source) == EXPECTED["source_coordinate_sha256"],
         "source coordinate hash")

    root = tuple(F(x) for x in CERT["primitive_root_interval"])
    need(root[0] < root[1], "root interval")
    poly = (F(1), F(0), F(-55), F(0), F(-140), F(0), F(-75), F(0), F(25))
    deriv = tuple((i + 1) * poly[i + 1] for i in range(8))
    left = sum(q * root[0] ** i for i, q in enumerate(poly))
    right = sum(q * root[1] ** i for i, q in enumerate(poly))
    derivative_interval = interval_eval(deriv, root)
    need(left < 0 < right and derivative_interval[0] > 0,
         "root is not uniquely isolated")

    source_edges = []
    for i, j in combinations(range(len(source)), 2):
        d2 = sqdist(source[i], source[j])
        if d2 == ONE:
            source_edges.append((i, j))
        else:
            gap = interval_eval(sub(d2, ONE), root)
            need(not (gap[0] <= 0 <= gap[1]), "unresolved source unit pair")
    need(len(source_edges) == EXPECTED["source_complete_unit_edges"], "source edge count")
    need(source_edges == [tuple(e) for e in CERT["source_edges"]], "source edges")

    classes = {}
    for i, a in enumerate(source):
        for j, b in enumerate(source):
            classes.setdefault(psub(a, b), []).append([i, j])
    rebuilt = sorted(classes)
    need(rebuilt == points, "difference-body collision quotient")
    need([classes[p] for p in points] == CERT["difference_label_classes"],
         "difference-label classes")
    need(len(points) == EXPECTED["physical_points"], "physical order")
    need(digest(point_line(p) for p in points) == EXPECTED["coordinate_sha256"],
         "physical coordinate hash")

    edges = []
    collision_checks = 0
    nonedge_checks = 0
    for i, j in combinations(range(len(points)), 2):
        d2 = sqdist(points[i], points[j])
        positive = interval_eval(d2, root)
        need(positive[0] > 0, "unmerged physical collision")
        collision_checks += 1
        gap = sub(d2, ONE)
        if gap == ZERO:
            edges.append((i, j))
        else:
            enclosure = interval_eval(gap, root)
            need(not (enclosure[0] <= 0 <= enclosure[1]), "unresolved possible unit pair")
            nonedge_checks += 1
    need(edges == [tuple(e) for e in CERT["edges"]], "complete edge serialization")
    need(len(edges) == EXPECTED["complete_unit_edges"], "edge count")
    need(digest(f"{a} {b}" for a, b in edges) == EXPECTED["edge_sha256"], "edge hash")

    adj = adjacency(len(points), edges)
    need(components(adj) == [len(points)], "graph disconnected")
    arts, bridges = cuts(adj)
    need(not arts and not bridges, "separable graph")
    need(core_order(adj, 4) == len(points), "four-core does not use whole support")

    word = CERT["three_colouring"]
    need(len(word) == len(points) and set(word) <= {0, 1, 2}, "three-colour word")
    need(all(word[a] != word[b] for a, b in edges), "monochromatic unit edge")
    four = CERT["four_colouring"]
    need(len(four) == len(points) and set(four) <= {0, 1, 2, 3}, "four-colour word")
    need(all(four[a] != four[b] for a, b in edges), "bad four-colour word")
    need(CERT["three_colourable"] is True and CERT["four_colourable"] is True,
         "colourability flags")
    need(CERT["chromatic_number"] == 3 and CERT["record_candidate"] is False,
         "chromatic conclusion flags")
    cycle = CERT["odd_cycle_lower_bound"]
    need(cycle[0] == cycle[-1] and (len(cycle) - 1) % 2 == 1, "odd cycle form")
    need(len(set(cycle[:-1])) == len(cycle) - 1, "odd cycle repeats")
    need(all(cycle[i + 1] in adj[cycle[i]] for i in range(len(cycle) - 1)),
         "odd cycle edge")

    summary = {
        "status": "VERIFIED_ODONNELL15_DIFFERENCE_THREECOLOUR_STOP",
        "source_points": len(source),
        "source_complete_unit_edges": len(source_edges),
        "physical_points": len(points),
        "complete_unit_edges": len(edges),
        "all_unordered_pairs_checked": collision_checks,
        "nonedge_interval_exclusions": nonedge_checks,
        "component_sizes": [len(points)],
        "articulations": arts,
        "bridges": bridges,
        "four_core_order": core_order(adj, 4),
        "chromatic_number": 3,
        "odd_cycle_length": len(cycle) - 1,
        "proper_three_word_checked": True,
        "proper_four_word_checked": True,
        "record_candidate": False,
        "coordinate_sha256": EXPECTED["coordinate_sha256"],
        "edge_sha256": EXPECTED["edge_sha256"],
    }
    need(summary == EXPECTED["verification_summary"], "summary mismatch")
    return summary


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
