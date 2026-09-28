#!/usr/bin/env python3
"""Independent exact audits for planar isometric-lollipop cover obstructions."""

from collections import deque


def graphs(m):
    assert m >= 5
    t, x, y = m, m + 1, m + 2
    n = m + 3
    full = [set() for _ in range(n)]

    def add(u, v):
        full[u].add(v)
        full[v].add(u)

    for i in range(m):
        add(i, (i + 1) % m)
    add(0, t)
    add(0, x)
    add(2, x)
    add(1, y)
    add(3, y)
    deleted = [set(row) for row in full]
    deleted[1].remove(2)
    deleted[2].remove(1)
    fragment = [row & set(range(m + 1)) for row in full]
    return full, deleted, fragment


def rotation(m):
    # A spherical rotation for F_m, including the degree-one tail.
    order = [[1, m - 1, m, m + 1], [0, 2, m + 2],
             [1, m + 1, 3], [2, 4, m + 2]]
    order.extend([[i - 1, i + 1] for i in range(4, m - 1)])
    order.extend([[0, m - 2], [0], [0, 2], [1, 3]])
    return order


def audit_rotation(graph, order, expected_faces):
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
    assert faces == expected_faces
    assert n - edges + faces == 2
    return edges, faces


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


def dag_geodesic_masks(graph):
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
    d = [[0 if i == j else (1 if j in graph[i] else infinity)
          for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d


def simple_path_geodesic_masks(graph):
    # Independent of the BFS shortest-path DAG: enumerate every simple
    # path, then use all-pairs Floyd-Warshall distances to filter it.
    n = len(graph)
    distance = floyd(graph)
    masks = set()
    all_simple_paths = 0
    for source in range(n):

        def visit(u, used, length):
            nonlocal all_simple_paths
            all_simple_paths += 1
            if length == distance[source][u]:
                masks.add(used)
            for v in graph[u]:
                if not (used >> v & 1):
                    visit(v, used | (1 << v), length + 1)

        visit(source, 1 << source, 0)
    assert all(distance[u] == bfs(graph, u) for u in range(n))
    return masks, all_simple_paths


def max_covered(masks, target):
    masks = sorted(masks)
    return max(((a | b) & target).bit_count()
               for i, a in enumerate(masks) for b in masks[i:])


def components_after(graph, deleted):
    unseen = {v for v in range(len(graph)) if not (deleted >> v & 1)}
    sizes = []
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        todo = [start]
        size = 1
        while todo:
            u = todo.pop()
            for v in graph[u] & unseen:
                unseen.remove(v)
                todo.append(v)
                size += 1
        sizes.append(size)
    return sizes


def audit_instance(m, independent=False):
    full, deleted, fragment = graphs(m)
    n = m + 3
    assert all(len(row) == len(set(row)) for row in full)
    assert sum(map(len, full)) // 2 == m + 5
    order = rotation(m)
    edges_full, faces_full = audit_rotation(full, order, 4)
    order[1].remove(2)
    order[2].remove(1)
    edges_deleted, faces_deleted = audit_rotation(deleted, order, 3)
    assert (edges_full, faces_full, edges_deleted, faces_deleted) == (m + 5, 4, m + 4, 3)
    assert all(bfs(full, u)[v] == bfs(fragment, u)[v]
               for u in range(m + 1) for v in range(m + 1))
    assert all(bfs(deleted, u)[v] >= 0 for u in range(n) for v in range(n))
    assert all(bfs([row & set(range(m + 1)) for row in deleted], 0)[v] >= 0
               for v in range(m + 1))
    target = (1 << (m + 1)) - 1
    masks = dag_geodesic_masks(deleted)
    if independent:
        other, all_simple = simple_path_geodesic_masks(deleted)
        assert masks == other
        print(f"independent simple paths={all_simple} geodesic vertex masks={len(masks)}")
    covered = max_covered(masks, target)
    if m == 9:
        assert len(masks) == 85 and covered == 9
        assert any(max(components_after(deleted, a | b), default=0) <= n // 2
                   for a in masks for b in masks)
        full_masks = dag_geodesic_masks(full)
        assert any(max(components_after(full, a | b), default=0) <= n // 2
                   for a in full_masks for b in full_masks)
    return n, covered


def main():
    for m in (7, 8, 9, 10, 11, 12, 13, 15, 19):
        n, covered = audit_instance(m, independent=(m == 9))
        expected = m if m >= 9 and m % 2 else m + 1
        assert covered == expected
        print(f"cycle={m} graph_vertices={n} target={m + 1} max_two_geodesics={covered}")
    print("PASS")


if __name__ == "__main__":
    main()
