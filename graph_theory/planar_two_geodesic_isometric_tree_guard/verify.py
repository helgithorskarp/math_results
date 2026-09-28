#!/usr/bin/env python3
"""Exact finite audits for deletion-stable isometric tree fragments."""

from collections import deque
from heapq import heapify, heappop, heappush
from itertools import product


def components(rows, allowed=None):
    remaining = set(range(len(rows))) if allowed is None else set(allowed)
    answer = []
    while remaining:
        start = min(remaining)
        todo = [start]
        remaining.remove(start)
        comp = {start}
        while todo:
            u = todo.pop()
            for v in rows[u] & remaining:
                remaining.remove(v)
                comp.add(v)
                todo.append(v)
        answer.append(comp)
    return answer


def prufer_tree(n, sequence):
    degree = [1] * n
    for v in sequence:
        degree[v] += 1
    leaves = [v for v in range(n) if degree[v] == 1]
    heapify(leaves)
    rows = [set() for _ in range(n)]
    for v in sequence:
        u = heappop(leaves)
        rows[u].add(v)
        rows[v].add(u)
        degree[u] -= 1
        degree[v] -= 1
        if degree[v] == 1:
            heappush(leaves, v)
    u, v = leaves
    rows[u].add(v)
    rows[v].add(u)
    return rows


def tree_path(rows, a, b):
    parent = {a: None}
    todo = [a]
    for u in todo:
        if u == b:
            break
        for v in sorted(rows[u]):
            if v not in parent:
                parent[v] = u
                todo.append(v)
    assert b in parent
    path = [b]
    while path[-1] != a:
        path.append(parent[path[-1]])
    return path


def leaf_order(rows):
    if len(rows) == 1:
        return [0]
    if len(rows) == 2:
        return [0, 1]
    root = next(v for v in range(len(rows)) if len(rows[v]) > 1)
    leaves = []

    def visit(u, parent):
        if len(rows[u]) == 1:
            leaves.append(u)
        for v in sorted(rows[u]):
            if v != parent:
                visit(v, u)

    visit(root, -1)
    return leaves


def audit_pairing(rows):
    n = len(rows)
    if n == 1:
        return 1
    leaves = leaf_order(rows)
    assert len(leaves) == sum(len(row) == 1 for row in rows)
    cyclic = leaves[:]
    if len(cyclic) % 2:
        cyclic.insert(0, cyclic[0])
    pairs = [(cyclic[i], cyclic[i + len(cyclic) // 2])
             for i in range(len(cyclic) // 2)]
    covered = set()
    for a, b in pairs:
        path = tree_path(rows, a, b)
        covered.update(tuple(sorted((u, v))) for u, v in zip(path, path[1:]))
    edges = {tuple(sorted((u, v))) for u in range(n) for v in rows[u] if u < v}
    assert covered == edges
    assert len(pairs) == (len(leaves) + 1) // 2
    return len(pairs)


def audit_labeled_trees():
    counts = []
    subtrees = 0
    for n in range(2, 8):
        count = 0
        for seq in product(range(n), repeat=n - 2):
            rows = prufer_tree(n, seq)
            assert len(components(rows)) == 1
            assert sum(map(len, rows)) == 2 * (n - 1)
            audit_pairing(rows)
            count += 1
            parent_leaves = sum(len(row) == 1 for row in rows)
            if parent_leaves <= 4:
                for mask in range(1, 1 << n):
                    vertices = {v for v in range(n) if mask >> v & 1}
                    if len(components(rows, vertices)) != 1:
                        continue
                    subrows = [set() for _ in vertices]
                    renumber = {v: i for i, v in enumerate(sorted(vertices))}
                    for v in vertices:
                        subrows[renumber[v]] = {renumber[w] for w in rows[v] & vertices}
                    child_leaves = sum(len(row) == 1 for row in subrows)
                    assert child_leaves <= parent_leaves
                    assert audit_pairing(subrows) <= 2
                    subtrees += 1
        assert count == n ** (n - 2)
        counts.append((n, count))
    return counts, subtrees


def family(r, ell):
    assert r >= 1 and ell >= 1
    rotation = [[1, 4, 3, 5], [2, 4, 0, 5], [3, 4, 1, 5],
                [0, 4, 2, 5], [0, 1, 2, 3], [0, 3, 2, 1]]
    trees = []
    for _ in range(r):
        a, b = len(rotation), len(rotation) + 1
        rotation[0].insert(rotation[0].index(1) + 1, a)
        rotation[1].insert(rotation[1].index(0), b)
        rotation.extend([[0, b], [a, 1]])
        vertices = [a, b]
        for center in (a, a, b, b):
            previous = center
            for _ in range(ell):
                v = len(rotation)
                position = len(rotation[previous]) - 1 if previous == center else len(rotation[previous])
                rotation[previous].insert(position, v)
                rotation.append([previous])
                vertices.append(v)
                previous = v
        trees.append(vertices)
    return rotation, trees


def distance(rows, source):
    dist = [-1] * len(rows)
    dist[source] = 0
    todo = deque([source])
    while todo:
        u = todo.popleft()
        for v in rows[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                todo.append(v)
    return dist


def audit_family(r, ell):
    rotation, trees = family(r, ell)
    rows = [set(order) for order in rotation]
    n = len(rows)
    assert all(len(order) == len(set(order)) for order in rotation)
    darts = {(u, v) for u in range(n) for v in rows[u]}
    assert all(u != v and (v, u) in darts for u, v in darts)
    unseen = darts.copy()
    faces = 0
    while unseen:
        first = min(unseen)
        dart = first
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            order = rotation[v]
            dart = (v, order[(order.index(u) - 1) % len(order)])
            if dart == first:
                break
        faces += 1
    edges = len(darts) // 2
    assert (n, edges, faces) == (6 + r * (2 + 4 * ell),
                                12 + r * (3 + 4 * ell), 8 + r)
    assert n - edges + faces == 2
    assert len(components(rows)) == 1
    residual = components(rows, set(range(4, n)))
    assert {frozenset(c) for c in residual} == (
        {frozenset([4]), frozenset([5])} | {frozenset(t) for t in trees}
    )
    for vertices in trees:
        assert len(vertices) == 2 + 4 * ell
        subrows = [rows[v] & set(vertices) for v in vertices]
        assert sum(len(row) == 1 for row in subrows) == 4
        assert sum(len(row) >= 3 for row in subrows) == 2
        for u in vertices:
            ambient = distance(rows, u)
            internal = distance([rows[v] & set(vertices) for v in range(n)], u)
            assert all(ambient[v] == internal[v] for v in vertices)
    return n, edges, faces


def main():
    counts, subtrees = audit_labeled_trees()
    print("labeled trees:", counts, "connected subtrees of <=4-leaf parents:", subtrees)
    for r, ell in ((1, 1), (1, 2), (5, 2), (8, 5)):
        n, edges, faces = audit_family(r, ell)
        print(f"ears={r} arm_length={ell} vertices={n} edges={edges} "
              f"faces={faces} planar=yes isometric=yes")
    print("PASS")


if __name__ == "__main__":
    main()
