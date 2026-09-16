#!/usr/bin/env python3
"""Exact one-shot probe for the O'Donnell 15-point core difference body.

The real coordinate field is Q(t), where

    25*t^8 - 75*t^6 - 140*t^4 - 55*t^2 + 1 = 0

and t is the real root 2.095109707686927... specified in the certificate.
Every field operation below uses rational coefficients modulo that polynomial.
There is no floating-point premise in collision or unit-edge reconstruction.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from fractions import Fraction as F
from itertools import combinations


N = 8
ZERO = (F(0),) * N
ONE = (F(1),) + (F(0),) * (N - 1)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def neg(a):
    return tuple(-x for x in a)


def sub(a, b):
    return add(a, neg(b))


def mul(a, b):
    """Multiply modulo 25x^8-75x^6-140x^4-55x^2+1."""
    c = [F(0)] * 15
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    c[i + j] += x * y
    for k in range(14, 7, -1):
        q = c[k]
        if not q:
            continue
        c[k] = F(0)
        # x^8 = 3x^6+(28/5)x^4+(11/5)x^2-1/25.
        c[k - 2] += 3 * q
        c[k - 4] += F(28, 5) * q
        c[k - 6] += F(11, 5) * q
        c[k - 8] -= F(1, 25) * q
    return tuple(c[:N])


def parse_row(values):
    assert len(values) == N
    return tuple(F(v) for v in values)


def frac(q):
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"


def row(a):
    return [frac(q) for q in a]


# Coordinates are ascending coefficient vectors in the displayed primitive
# element. They are an exact algebraic serialization of the three regular
# pentagonal rings in O'DonnellGraph40Core, not a numerical embedding.
SOURCE_ROWS = [
    (["1/2","0","0","0","0","0","0","0"], ["0","-1785/356","0","-2055/178","0","-485/89","0","675/356"]),
    (["543/712","0","235/89","0","125/89","0","-325/712","0"], ["0","1385/712","0","485/178","0","-45/178","0","-75/712"]),
    (["0","0","0","0","0","0","0","0"], ["0","2185/356","0","1570/89","0","1015/89","0","-1275/356"]),
    (["-543/712","0","-235/89","0","-125/89","0","325/712","0"], ["0","1385/712","0","485/178","0","-45/178","0","-75/712"]),
    (["-1/2","0","0","0","0","0","0","0"], ["0","-1785/356","0","-2055/178","0","-485/89","0","675/356"]),
    (["-169/712","0","235/89","0","125/89","0","-325/712","0"], ["0","1385/712","0","485/178","0","-45/178","0","-75/712"]),
    (["-187/712","0","-235/89","0","-125/89","0","325/712","0"], ["0","-585/712","0","300/89","0","1105/178","0","-1125/712"]),
    (["0","0","0","0","0","0","0","0"], ["0","-200/89","0","-1085/89","0","-1060/89","0","300/89"]),
    (["187/712","0","235/89","0","125/89","0","-325/712","0"], ["0","-585/712","0","300/89","0","1105/178","0","-1125/712"]),
    (["169/712","0","-235/89","0","-125/89","0","325/712","0"], ["0","1385/712","0","485/178","0","-45/178","0","-75/712"]),
    (["0","0","0","0","0","0","0","0"], ["0","-1829/356","0","-1570/89","0","-1015/89","0","1275/356"]),
    (["243/356","0","15/178","0","-295/178","0","125/356","0"], ["0","-599/356","0","-15/178","0","295/178","0","-125/356"]),
    (["257/712","0","615/178","0","405/89","0","-875/712","0"], ["0","3027/712","0","1585/178","0","360/89","0","-1025/712"]),
    (["-257/712","0","-615/178","0","-405/89","0","875/712","0"], ["0","3027/712","0","1585/178","0","360/89","0","-1025/712"]),
    (["-243/356","0","-15/178","0","295/178","0","-125/356","0"], ["0","-599/356","0","-15/178","0","295/178","0","-125/356"]),
]


def source_points():
    out = [(parse_row(x), parse_row(y)) for x, y in SOURCE_ROWS]
    assert len(out) == len(set(out)) == 15
    return out


def point_sub(a, b):
    return sub(a[0], b[0]), sub(a[1], b[1])


def squared_distance(a, b):
    dx, dy = point_sub(a, b)
    return add(mul(dx, dx), mul(dy, dy))


def graph_edges(points):
    return [(i, j) for i, j in combinations(range(len(points)), 2)
            if squared_distance(points[i], points[j]) == ONE]


def difference_body(points):
    labels = {}
    for i, a in enumerate(points):
        for j, b in enumerate(points):
            labels.setdefault(point_sub(a, b), []).append((i, j))
    pts = sorted(labels)
    return pts, [labels[p] for p in pts]


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return adj


def components(adj):
    unseen = set(range(len(adj)))
    out = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        unseen.remove(seed)
        comp = []
        while stack:
            u = stack.pop()
            comp.append(u)
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    stack.append(v)
        out.append(sorted(comp))
    return sorted(out, key=lambda c: (-len(c), c))


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
                continue
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


def kcore(adj, k):
    alive = set(range(len(adj)))
    deg = [len(x) for x in adj]
    todo = [u for u in alive if deg[u] < k]
    while todo:
        u = todo.pop()
        if u not in alive:
            continue
        alive.remove(u)
        for v in adj[u]:
            if v in alive:
                deg[v] -= 1
                if deg[v] == k - 1:
                    todo.append(v)
    return sorted(alive)


def dsatur(adj, k):
    """Return one proper k-colouring, or None after exhaustive search."""
    n = len(adj)
    colour = [-1] * n
    masks = [0] * n
    nodes = 0

    def rec(done):
        nonlocal nodes
        nodes += 1
        if done == n:
            return True
        u = max((v for v in range(n) if colour[v] < 0),
                key=lambda v: (masks[v].bit_count(), len(adj[v]), -v))
        forbidden = masks[u]
        used = 1 + max(colour, default=-1)
        for c in range(min(k, used + 1)):
            bit = 1 << c
            if forbidden & bit:
                continue
            colour[u] = c
            changed = []
            bad = False
            for v in adj[u]:
                if colour[v] == c:
                    bad = True
                    break
                if colour[v] < 0 and not (masks[v] & bit):
                    changed.append((v, masks[v]))
                    masks[v] |= bit
                    if masks[v] == (1 << k) - 1:
                        bad = True
                        break
            if not bad and rec(done + 1):
                return True
            for v, old in reversed(changed):
                masks[v] = old
            colour[u] = -1
        return False

    ok = rec(0)
    return (colour[:] if ok else None), nodes


def shortest_odd_cycle(adj):
    best = None
    for start in range(len(adj)):
        queue = collections.deque([(start, 0)])
        parent = {(start, 0): None}
        target = None
        while queue:
            u, parity = queue.popleft()
            if u == start and parity == 1:
                target = (u, parity)
                break
            for v in sorted(adj[u]):
                state = (v, 1 - parity)
                if state not in parent:
                    parent[state] = (u, parity)
                    queue.append(state)
        if target is not None:
            states = []
            state = target
            while state is not None:
                states.append(state)
                state = parent[state]
            cycle = [u for u, _ in reversed(states)]
            if best is None or len(cycle) < len(best):
                best = cycle
    return best


def digest_lines(lines):
    h = hashlib.sha256()
    for line in lines:
        h.update((line + "\n").encode())
    return h.hexdigest()


def point_row(p):
    return [row(p[0]), row(p[1])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--output")
    args = ap.parse_args()

    source = source_points()
    source_edges = graph_edges(source)
    assert len(source_edges) == 25, "wrong exact O'Donnell core realization"
    points, labels = difference_body(source)
    edges = graph_edges(points)
    adj = adjacency(len(points), edges)
    comps = components(adj)
    arts, bridges = cuts(adj)
    core4 = kcore(adj, 4)

    word3, nodes3 = dsatur(adj, 3)
    assert word3 is None or all(word3[a] != word3[b] for a, b in edges)
    word4 = word3[:] if word3 is not None else dsatur(adj, 4)[0]
    odd_cycle = shortest_odd_cycle(adj)
    assert odd_cycle is not None and (len(odd_cycle) - 1) % 2 == 1
    assert odd_cycle[0] == odd_cycle[-1]
    assert all(odd_cycle[i + 1] in adj[odd_cycle[i]]
               for i in range(len(odd_cycle) - 1))

    result = {
        "schema": 2,
        "field": "Q(t), 25t^8-75t^6-140t^4-55t^2+1=0",
        "primitive_root_interval": ["2.095109707686927", "2.095109707686928"],
        "source": "O'Donnell 15-point pentagonal core",
        "source_points": len(source),
        "source_complete_unit_edges": len(source_edges),
        "operation": "full oriented difference body S-S",
        "raw_cap_bound": 211,
        "formal_ordered_labels": 225,
        "physical_points": len(points),
        "complete_unit_edges": len(edges),
        "all_unordered_pairs_checked": len(points) * (len(points) - 1) // 2,
        "component_sizes": [len(c) for c in comps],
        "articulation_vertices": arts,
        "bridges": bridges,
        "four_core_order": len(core4),
        "four_core_uses_full_support": len(core4) == len(points),
        "four_colourable": word4 is not None,
        "three_colourable": word3 is not None,
        "three_colour_search_nodes": nodes3,
        "chromatic_number": 3 if word3 is not None else None,
        "odd_cycle_lower_bound": odd_cycle,
        "record_candidate": word4 is None,
        "source_coordinates": [point_row(p) for p in source],
        "source_edges": source_edges,
        "physical_coordinates": [point_row(p) for p in points],
        "difference_label_classes": labels,
        "edges": edges,
        "three_colouring": word3,
        "four_colouring": word4,
        "source_coordinate_sha256": digest_lines(
            " | ".join(" ".join(row(a)) for a in p) for p in source),
        "coordinate_sha256": digest_lines(" | ".join(" ".join(row(a)) for a in p)
                                            for p in points),
        "edge_sha256": digest_lines(f"{a} {b}" for a, b in edges),
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
    print(json.dumps({k: v for k, v in result.items()
                      if k not in {"source_coordinates", "source_edges",
                                   "physical_coordinates", "difference_label_classes",
                                   "edges", "three_colouring", "four_colouring"}},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
