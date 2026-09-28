#!/usr/bin/env python3
"""Exact audits for the one-shortcut planar lollipop obstruction."""

from collections import deque


def graphs(m):
    assert m >= 5
    n = m + 2
    full = [set() for _ in range(n)]

    def add(u, v):
        full[u].add(v)
        full[v].add(u)

    for i in range(m):
        add(i, (i + 1) % m)
    add(0, m)             # leaf t
    add(1, m + 1)         # exterior two-edge route 1-x-3
    add(3, m + 1)
    residual = [set(row) for row in full]
    residual[1].remove(2)
    residual[2].remove(1)
    fragment = [row & set(range(m + 1)) for row in full]
    return full, residual, fragment


def rotation(m):
    order = [[1, m - 1, m], [0, 2, m + 1], [1, 3], [2, 4, m + 1]]
    order.extend([[i - 1, i + 1] for i in range(4, m - 1)])
    order.extend([[0, m - 2], [0], [1, 3]])
    return order


def audit_rotation(graph, order, faces_expected):
    n = len(graph)
    assert len(order) == n
    assert all(set(order[u]) == graph[u] and len(order[u]) == len(graph[u])
               for u in range(n))
    unseen = {(u, v) for u in range(n) for v in graph[u]}
    assert all(u != v and (v, u) in unseen for u, v in unseen)
    edges = len(unseen) // 2
    faces = 0
    while unseen:
        first = min(unseen)
        dart = first
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            neighbors = order[v]
            dart = (v, neighbors[(neighbors.index(u) - 1) % len(neighbors)])
            if dart == first:
                break
        faces += 1
    assert faces == faces_expected and n - edges + faces == 2
    return edges


def bfs(graph, source):
    distance = [-1] * len(graph)
    distance[source] = 0
    todo = deque([source])
    while todo:
        u = todo.popleft()
        for v in graph[u]:
            if distance[v] == -1:
                distance[v] = distance[u] + 1
                todo.append(v)
    return distance


def dag_masks(graph):
    masks = set()
    for source in range(len(graph)):
        distance = bfs(graph, source)

        def visit(u, mask):
            masks.add(mask)
            for v in graph[u]:
                if distance[v] == distance[u] + 1:
                    visit(v, mask | (1 << v))

        visit(source, 1 << source)
    return masks


def floyd(graph):
    n = len(graph)
    infinity = n + 1
    distance = [[0 if i == j else (1 if j in graph[i] else infinity)
                 for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                distance[i][j] = min(distance[i][j],
                                     distance[i][k] + distance[k][j])
    return distance


def all_simple_path_masks(graph):
    # Independent enumeration: no BFS DAG is used to generate paths.
    n = len(graph)
    distance = floyd(graph)
    masks = set()
    count = 0
    for source in range(n):

        def visit(u, used, length):
            nonlocal count
            count += 1
            if length == distance[source][u]:
                masks.add(used)
            for v in graph[u]:
                if not (used >> v & 1):
                    visit(v, used | (1 << v), length + 1)

        visit(source, 1 << source, 0)
    assert all(distance[u] == bfs(graph, u) for u in range(n))
    return masks, count


def max_two_coverage(masks, target):
    masks = sorted(masks)
    return max(((a | b) & target).bit_count()
               for i, a in enumerate(masks) for b in masks[i:])


def component_sizes(graph, removed):
    unseen = {v for v in range(len(graph)) if not (removed >> v & 1)}
    sizes = []
    while unseen:
        first = min(unseen)
        unseen.remove(first)
        todo = [first]
        size = 1
        while todo:
            u = todo.pop()
            for v in graph[u] & unseen:
                unseen.remove(v)
                todo.append(v)
                size += 1
        sizes.append(size)
    return sizes


def audit(m, independent=False):
    full, residual, fragment = graphs(m)
    order = rotation(m)
    assert audit_rotation(full, order, 3) == m + 3
    order[1].remove(2)
    order[2].remove(1)
    assert audit_rotation(residual, order, 2) == m + 2
    internal = [row & set(range(m + 1)) for row in residual]
    for u in range(m + 1):
        in_fragment = bfs(fragment, u)
        in_full = bfs(full, u)
        assert all(in_fragment[v] == in_full[v] for v in range(m + 1))
    assert all(bfs(internal, 0)[v] >= 0 for v in range(m + 1))
    target = (1 << (m + 1)) - 1
    masks = dag_masks(residual)
    if independent:
        other, simple_count = all_simple_path_masks(residual)
        assert masks == other
        print(f"independent simple paths={simple_count} geodesic vertex masks={len(masks)}")
    best = max_two_coverage(masks, target)
    if m >= 11:
        q = m // 2
        long = [0] + list(range(m - 1, 2, -1))
        first = [m] + long[:q + 1]
        second = [2] + list(reversed(long[q + 1:]))
        assert all(v in residual[u] for path in (first, second)
                   for u, v in zip(path, path[1:]))
        assert all(len(path) - 1 == bfs(residual, path[0])[path[-1]]
                   for path in (first, second))
        assert ({*first, *second} & set(range(m + 1))) == set(range(m + 1)) - {1}
        assert best == m
    else:
        assert best == m + 1
    if m == 11:
        assert any(max(component_sizes(residual, a | b), default=0) <= (m + 2) // 2
                   for a in masks for b in masks)
        full_masks = dag_masks(full)
        assert any(max(component_sizes(full, a | b), default=0) <= (m + 2) // 2
                   for a in full_masks for b in full_masks)
    return len(full), best


def main():
    for m in (5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 20, 30):
        n, covered = audit(m, independent=(m == 11))
        print(f"cycle={m} graph_vertices={n} target={m + 1} max_two_geodesics={covered}")
    print("PASS")


if __name__ == "__main__":
    main()
