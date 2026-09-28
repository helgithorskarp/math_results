#!/usr/bin/env python3
"""Independent exact replay of the radial-cube shortcut certificate."""

from collections import Counter
from itertools import combinations
from heapq import heappop, heappush
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "planar_two_geodesic_zero_mass_cube_shortcut" / "certificate.json"
MARKS = tuple(range(15, 26))
PRICE_VECTORS = {
    "A": (14, 38, 7, 23, 20, 17, 8, 30, 11, 21, 14, 29,
          10, 28, 36, 4, 3, 7, 30, 6, 2, 4, 9, 5),
    "B": (7, 10, 4, 8, 7, 11, 9, 6, 16, 14, 3, 23,
          3, 16, 15, 16, 3, 10, 22, 9, 12, 3, 12, 7),
}


def geometry():
    # Construct by binary coordinates, without using an oriented face list.
    adj = [set() for _ in range(26)]
    triangles = []
    def add(a, b):
        adj[a].add(b)
        adj[b].add(a)
    core = []
    for v in range(8):
        for axis in range(3):
            f = 8 + 2 * axis + ((v >> axis) & 1)
            add(v, f)
            core.append((v, f))
    cube_edges = [(a, b) for a, b in combinations(range(8), 2)
                  if (a ^ b) in (1, 2, 4)]
    for z, (a, b) in enumerate(cube_edges, 14):
        axis = (a ^ b).bit_length() - 1
        add(a, z)
        add(b, z)
        for j in range(3):
            if j == axis:
                continue
            f = 8 + 2 * j + ((a >> j) & 1)
            add(z, f)
            triangles.extend(((a, z, f), (b, z, f)))
    edge_faces = Counter(tuple(sorted((a, b)))
                         for t in triangles for a, b in
                         ((t[0], t[1]), (t[1], t[2]), (t[2], t[0])))
    assert len(cube_edges) == 12 and len(core) == 24
    assert len(edge_faces) == 72 and len(triangles) == 48
    assert all(count == 2 for count in edge_faces.values())
    assert {tuple(sorted((a, b))) for a, ns in enumerate(adj) for b in ns} == set(edge_faces)
    # Every vertex link is one cycle, so the connected Euler-2 complex is a sphere.
    for v in range(26):
        link = {u: set() for u in adj[v]}
        for t in triangles:
            if v in t:
                a, b = (u for u in t if u != v)
                link[a].add(b)
                link[b].add(a)
        assert all(len(ns) == 2 for ns in link.values())
        seen = {next(iter(link))}
        todo = list(seen)
        while todo:
            u = todo.pop()
            for w in link[u] - seen:
                seen.add(w)
                todo.append(w)
        assert seen == set(link)
    assert 26 - len(edge_faces) + len(triangles) == 2
    return adj, sorted(core)


ADJ, CORE = geometry()


def distances(prices, extra=None):
    weighted = [[] for _ in range(14)]
    for (a, b), weight in prices.items():
        weighted[a].append((b, weight))
        weighted[b].append((a, weight))
    if extra is not None:
        a, b, t = extra
        weighted[a].append((b, t))
        weighted[b].append((a, t))
    out = []
    for source in range(14):
        d = [None] * 14
        d[source] = 0
        queue = [(0, source)]
        while queue:
            cost, u = heappop(queue)
            if cost != d[u]:
                continue
            for v, weight in weighted[u]:
                trial = cost + weight
                if d[v] is None or trial < d[v]:
                    d[v] = trial
                    heappush(queue, (trial, v))
        assert all(x is not None for x in d)
        out.append(d)
    return out


def components_without(removed):
    unseen = set(range(26)) - removed
    blocks = []
    while unseen:
        seed = unseen.pop()
        block = {seed}
        todo = [seed]
        while todo:
            u = todo.pop()
            new = ADJ[u] & unseen
            unseen.difference_update(new)
            block.update(new)
            todo.extend(new)
        blocks.append(block & set(MARKS))
    return blocks


def path_data(path, parents, ends, prices):
    assert path and len(path) == len(set(path))
    assert path[0] != 14 and path[-1] != 14
    assert all(0 <= v < 26 for v in path)
    assert all(b in ADJ[a] for a, b in zip(path, path[1:]))
    assert all(v not in MARKS for v in path[1:-1])
    if len(path) == 1:
        return None
    middle = list(path)
    if middle[0] in MARKS:
        assert parents.get(middle[0]) == middle[1]
        middle.pop(0)
    if middle[-1] in MARKS:
        assert parents.get(middle[-1]) == middle[-2]
        middle.pop()
    assert middle and middle[0] < 14 and middle[-1] < 14
    shortcut_count = 0
    fixed = 0
    for a, b in zip(middle, middle[1:]):
        if 14 in (a, b):
            shortcut_count += 1
        else:
            fixed += prices[tuple(sorted((a, b)))]
    assert shortcut_count in (0, 2)
    if shortcut_count:
        i = middle.index(14)
        assert {middle[i - 1], middle[i + 1]} == set(ends)
    return middle[0], middle[-1], fixed, shortcut_count // 2


def check_template(template, cell, ends, prices, endpoint_dist):
    conditions = template["conditions"]
    parents = dict(conditions)
    assert len(parents) == len(conditions)
    assert all(z in MARKS and p in ADJ[z] for z, p in conditions)
    big = []
    for pair in template["pairs"]:
        assert len(pair) == 2
        deleted = set()
        for path in pair:
            data = path_data(path, parents, ends, prices)
            if data is not None:
                a, b, fixed, slope = data
                for t, d in endpoint_dist.items():
                    assert fixed + slope * t == d[a][b], (cell, path, t)
            deleted.update(path)
        blocks = [s for s in components_without(deleted) if len(s) > 4]
        big.append(blocks)
    if template["kind"] == "four-residue":
        assert big == [[]]
    else:
        assert template["kind"] == "disjoint-exceptional-blocks"
        assert len(big) == 2 and all(len(x) == 1 for x in big)
        assert big[0][0].isdisjoint(big[1][0])
        assert [sum(1 << z for z in x[0]) for x in big] == template["exceptional_blocks"]


def rup_replay(clauses, lines):
    added = 0
    for line in lines:
        if line.startswith("d "):
            continue  # Retaining deleted premises is sound for RUP replay.
        ints = [int(x) for x in line.split()]
        assert ints and ints[-1] == 0
        proposed = tuple(ints[:-1])
        assignment = {}
        contradiction = False
        for lit in proposed:
            variable, value = abs(lit), lit < 0
            if variable in assignment and assignment[variable] != value:
                contradiction = True
                break
            assignment[variable] = value
        while not contradiction:
            changed = False
            for clause in clauses:
                undecided = []
                satisfied = False
                for lit in clause:
                    value = assignment.get(abs(lit))
                    if value is None:
                        undecided.append(lit)
                    elif value == (lit > 0):
                        satisfied = True
                        break
                if satisfied:
                    continue
                if not undecided:
                    contradiction = True
                    break
                if len(undecided) == 1:
                    lit = undecided[0]
                    assignment[abs(lit)] = lit > 0
                    changed = True
            if not changed:
                break
        assert contradiction, ("invalid RUP step", line)
        clauses.append(proposed)
        added += 1
    assert clauses[-1] == ()
    return added


def main():
    data = json.loads(SOURCE.read_text())
    assert data["schema"] == "radial-cube-zero-mass-shortcut-v1"
    assert data["vertices"] == 26 and data["shortcut_vertex"] == 14
    assert data["mass_support"] == list(MARKS)
    assert len(data["rows"]) == 4
    assert {(r["metric"], tuple(r["opposite_pair"])) for r in data["rows"]} == {
        (name, pair) for name in PRICE_VECTORS for pair in ((0, 1), (10, 12))}
    counts = Counter()
    for row in data["rows"]:
        prices = {(a, b): w for a, b, w in row["original_prices"]}
        assert sorted(prices) == CORE and all(w > 0 for w in prices.values())
        assert tuple(prices[e] for e in CORE) == PRICE_VECTORS[row["metric"]]
        u, v = row["opposite_pair"]
        assert (u, v) in ((0, 1), (10, 12))
        original = distances(prices)
        changes = {0}
        for a in range(14):
            for b in range(14):
                q = original[a][b] - min(original[a][u] + original[v][b],
                                        original[a][v] + original[u][b])
                if q > 0:
                    changes.add(q)
        points = sorted(changes)
        assert [(c["lower"], c["upper"]) for c in row["cells"]] == [
            (lo, hi) for lo, hi in zip(points, points[1:] + [None])]
        assert len(points) == {("A", (0, 1)): 10, ("A", (10, 12)): 15,
                               ("B", (0, 1)): 8, ("B", (10, 12)): 7}[
                                   row["metric"], (u, v)]
        counts["cells"] += len(row["cells"])
        for cell in row["cells"]:
            lo, hi = cell["lower"], cell["upper"]
            test_values = (lo, hi) if hi is not None else (lo, lo + 1)
            endpoint_dist = {t: distances(prices, (u, v, t)) for t in test_values}
            choices = {}
            clauses = []
            for z in MARKS:
                choices[z] = {p: 1 + 4 * (z - 15) + j for j, p in enumerate(sorted(ADJ[z]))}
                literals = list(choices[z].values())
                assert len(literals) == 4
                clauses.append(tuple(literals))
                clauses.extend((-a, -b) for a, b in combinations(literals, 2))
            for template in cell["templates"]:
                check_template(template, cell, (u, v), prices, endpoint_dist)
                clauses.append(tuple(-choices[z][p] for z, p in template["conditions"]))
                counts["templates"] += 1
                counts[template["kind"]] += 1
            counts["rup"] += rup_replay(clauses, cell["rup_proof"])
    assert counts == {"cells": 40, "templates": 1055,
                      "four-residue": 876, "disjoint-exceptional-blocks": 179,
                      "rup": 333}
    print("cells=40 templates=1055 four_residue=876 adaptive=179 "
          "RUP_additions=333 PASS")


if __name__ == "__main__":
    main()
