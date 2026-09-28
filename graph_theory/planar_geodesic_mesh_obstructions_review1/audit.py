#!/usr/bin/env python3
"""Independent, finite definition-level audit of the capped-mesh proof."""

from collections import deque
from hashlib import sha256
from itertools import product
import json


def make_graph(m, h, cylinder, diagonals):
    s, t = ("s",), ("t",)
    vertices = [s, t] + [(i, j) for i in range(m) for j in range(1, h + 1)]
    graph = {v: set() for v in vertices}

    def join(a, b):
        assert a != b
        graph[a].add(b)
        graph[b].add(a)

    for i in range(m):
        column = [s] + [(i, j) for j in range(1, h + 1)] + [t]
        for a, b in zip(column, column[1:]):
            join(a, b)
    seams = range(m if cylinder else m - 1)
    cells = [(i, j) for i in seams for j in range(1, h)]
    assert len(cells) == len(diagonals)
    for i in seams:
        q = (i + 1) % m
        for j in range(1, h + 1):
            join((i, j), (q, j))
    for (i, j), choice in zip(cells, diagonals):
        q = (i + 1) % m
        if choice == 1:
            join((i, j), (q, j + 1))
        elif choice == -1:
            join((q, j), (i, j + 1))
        else:
            assert choice == 0
    if not cylinder:
        join(s, t)
    return graph


def median_paths(m, h, cylinder, mass, first=0):
    s, t = ("s",), ("t",)
    columns = [sum(mass[i, j] for j in range(1, h + 1)) for i in range(m)]
    total = sum(columns)

    def meridian(i):
        return [s] + [(i, j) for j in range(1, h + 1)] + [t]

    if cylinder:
        if columns[first] * 2 >= total:
            return [meridian(first)]
        prefix = columns[first]
        for offset in range(1, m):
            i = (first + offset) % m
            prefix += columns[i]
            if prefix * 2 >= total:
                return [meridian(first), meridian(i)]
        raise AssertionError("median absent")
    prefix = 0
    for i in range(m):
        prefix += columns[i]
        if prefix * 2 >= total:
            break
    k = h // 2
    return [[s] + [(i, j) for j in range(1, k + 1)],
            [t] + [(i, j) for j in range(h, k, -1)]]


def distance(graph, source, target):
    queue = deque([(source, 0)])
    visited = {source}
    while queue:
        v, d = queue.popleft()
        if v == target:
            return d
        for w in graph[v]:
            if w not in visited:
                visited.add(w)
                queue.append((w, d + 1))
    raise AssertionError("disconnected path endpoints")


def verify(graph, mass, paths):
    assert 1 <= len(paths) <= 2
    for path in paths:
        assert path and len(set(path)) == len(path)
        assert all(b in graph[a] for a, b in zip(path, path[1:]))
        assert distance(graph, path[0], path[-1]) == len(path) - 1
    removed = set().union(*(set(p) for p in paths))
    unseen = set(graph) - removed
    component_masses = []
    while unseen:
        start = unseen.pop()
        todo = [start]
        weight = 0
        while todo:
            v = todo.pop()
            weight += mass[v]
            for w in graph[v] & unseen:
                unseen.remove(w)
                todo.append(w)
        component_masses.append(weight)
    assert 2 * max(component_masses, default=0) <= sum(mass.values())
    return sorted(component_masses)


def weighted_leaves(graph, mass, m, h, cylinder):
    enlarged = {v: set(neighbors) for v, neighbors in graph.items()}
    weight = dict(mass)
    roots = list(graph)
    for index, root in enumerate(roots):
        for leaf_number in range((index * index + 2 * index + 1) % 3):
            leaf = ("leaf", index, leaf_number)
            enlarged[leaf] = {root}
            enlarged[root].add(leaf)
            weight[leaf] = (13 * index + 7 * leaf_number + 3) % 29
    leaves = [v for v in enlarged if v not in graph]
    if leaves:
        weight[leaves[-1]] = 1 + 2 * sum(weight.values())
        verify(enlarged, weight, [[leaves[-1]]])
        weight[leaves[-1]] = 0
    aggregate = {v: weight[v] for v in graph}
    for leaf in leaves:
        aggregate[next(iter(enlarged[leaf]))] += weight[leaf]
    assert all(2 * weight[leaf] <= sum(weight.values()) for leaf in leaves)
    paths = median_paths(m, h, cylinder, aggregate)
    verify(enlarged, weight, paths)
    return len(leaves)


def main():
    counts = {"mesh_graphs": 0, "weighted_core_checks": 0,
              "weighted_leaf_checks": 0, "heavy_leaf_checks": 0,
              "max_order": 0}
    digest = sha256()
    for cylinder, dimensions in (
            (True, [(3, 1), (3, 2), (3, 3), (4, 1), (4, 2)]),
            (False, [(m, h) for m in range(1, 5) for h in range(1, 4)])):
        for m, h in dimensions:
            cells = (m if cylinder else m - 1) * (h - 1)
            for choices in product((-1, 0, 1), repeat=cells):
                graph = make_graph(m, h, cylinder, choices)
                counts["mesh_graphs"] += 1
                counts["max_order"] = max(counts["max_order"], len(graph))
                order = list(graph)
                weightings = [
                    {v: 0 for v in order},
                    {v: 1 for v in order},
                    {v: (17 * i * i + 5 * i + 9) % 31 for i, v in enumerate(order)},
                    {v: (10**5 if v == ("s",) else 0) for v in order},
                    {v: (10**5 if v == order[-1] else 0) for v in order},
                ]
                for mass in weightings:
                    for first in (range(m) if cylinder else (0,)):
                        paths = median_paths(m, h, cylinder, mass, first)
                        result = verify(graph, mass, paths)
                        counts["weighted_core_checks"] += 1
                        digest.update(json.dumps([cylinder, m, h, choices, first,
                                                  [str(v) for p in paths for v in p], result],
                                                 separators=(",", ":")).encode() + b"\n")
                if choices == tuple(0 for _ in range(cells)):
                    weight = weightings[2]
                    leaves = weighted_leaves(graph, weight, m, h, cylinder)
                    counts["weighted_leaf_checks"] += 1
                    if leaves:
                        counts["heavy_leaf_checks"] += 1
    counts["audit_sha256"] = digest.hexdigest()
    print(json.dumps(counts, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
