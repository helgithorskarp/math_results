#!/usr/bin/env python3
"""Exact finite audits for the exterior-ear coverage threshold."""

from collections import deque


def construct(m, s):
    assert m >= 5 and s >= 2
    n = m + s
    graph = [set() for _ in range(n)]

    def add(u, v):
        graph[u].add(v)
        graph[v].add(u)

    for u in range(m):
        add(u, (u + 1) % m)
    add(0, m)  # leaf t
    ear = [1] + list(range(m + 1, m + s)) + [3]
    assert len(ear) == s + 1
    for u, v in zip(ear, ear[1:]):
        add(u, v)
    deleted = [row.copy() for row in graph]
    deleted[1].remove(2)
    deleted[2].remove(1)
    fragment = [row & set(range(m + 1)) for row in graph]
    return graph, deleted, fragment, ear


def rotation(m, s):
    first, last = m + 1, m + s - 1
    order = [[1, m - 1, m], [0, 2, first], [1, 3], [2, 4, last]]
    order.extend([[v - 1, v + 1] for v in range(4, m - 1)])
    order.extend([[0, m - 2], [0]])
    for v in range(first, last + 1):
        order.append([1 if v == first else v - 1,
                      3 if v == last else v + 1])
    return order


def check_rotation(graph, order, faces):
    assert len(order) == len(graph)
    assert all(len(order[u]) == len(graph[u]) and set(order[u]) == graph[u]
               for u in range(len(graph)))
    unseen = {(u, v) for u, row in enumerate(graph) for v in row}
    edge_count = len(unseen) // 2
    found_faces = 0
    while unseen:
        start = min(unseen)
        dart = start
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            around = order[v]
            dart = (v, around[(around.index(u) - 1) % len(around)])
            if dart == start:
                break
        found_faces += 1
    assert found_faces == faces
    assert len(graph) - edge_count + faces == 2
    return edge_count


def bfs(graph, start):
    distances = [-1] * len(graph)
    distances[start] = 0
    todo = deque([start])
    while todo:
        u = todo.popleft()
        for v in graph[u]:
            if distances[v] < 0:
                distances[v] = distances[u] + 1
                todo.append(v)
    return distances


def geodesic_masks(graph):
    masks = set()
    for start in range(len(graph)):
        distances = bfs(graph, start)

        def walk(u, mask):
            masks.add(mask)
            for v in graph[u]:
                if distances[v] == distances[u] + 1:
                    walk(v, mask | (1 << v))

        walk(start, 1 << start)
    return masks


def independent_masks(graph):
    n = len(graph)
    distances = [[0 if u == v else (1 if v in graph[u] else n + 1)
                  for v in range(n)] for u in range(n)]
    for k in range(n):
        for u in range(n):
            for v in range(n):
                distances[u][v] = min(distances[u][v],
                                      distances[u][k] + distances[k][v])
    masks = set()
    path_count = 0
    for start in range(n):

        def walk(u, mask, length):
            nonlocal path_count
            path_count += 1
            if length == distances[start][u]:
                masks.add(mask)
            for v in graph[u]:
                if not (mask >> v & 1):
                    walk(v, mask | (1 << v), length + 1)

        walk(start, 1 << start, 0)
    return masks, path_count


def check_path(graph, path):
    assert len(path) == len(set(path))
    assert all(v in graph[u] for u, v in zip(path, path[1:]))
    assert len(path) - 1 == bfs(graph, path[0])[path[-1]]


def audit(m, s, independent=False):
    full, deleted, fragment, ear = construct(m, s)
    order = rotation(m, s)
    assert check_rotation(full, order, 3) == m + s + 1
    order[1].remove(2)
    order[2].remove(1)
    assert check_rotation(deleted, order, 2) == m + s
    for u in range(m + 1):
        full_distance = bfs(full, u)
        fragment_distance = bfs(fragment, u)
        assert all(full_distance[v] == fragment_distance[v]
                   for v in range(m + 1))
    target = (1 << (m + 1)) - 1
    masks = geodesic_masks(deleted)
    if independent:
        other, count = independent_masks(deleted)
        assert masks == other
        print(f"independent m={m} s={s} simple_paths={count} geodesic_masks={len(masks)}")
    best = max(((left | right) & target).bit_count()
               for left in masks for right in masks)
    L, a = m - 3, s + 1
    long_arc = [0] + list(range(m - 1, 2, -1))
    assert len(long_arc) == L + 1 and long_arc[-1] == 3
    if a < L - 4:
        q = (a + L) // 2
        first = [m] + long_arc[:q + 1]
        second = [2] + list(reversed(long_arc[q + 1:]))
        assert ({*first, *second} & set(range(m + 1))) == set(range(m + 1)) - {1}
        expected = m
    elif a <= L:
        first = [m, 0] + ear + [2]
        second = long_arc[1:-1]
        expected = m + 1
    else:
        first = [m] + long_arc + [2]
        second = [1]
        expected = m + 1
    check_path(deleted, first)
    check_path(deleted, second)
    assert ((sum(1 << v for v in set(first + second))) & target).bit_count() == expected
    assert best == expected
    return len(full), len(masks), best


def main():
    total = 0
    for m in range(5, 19):
        for s in range(2, m + 1):
            n, masks, best = audit(m, s, independent=(m, s) in {(11, 2), (11, 3), (12, 3), (12, 4), (15, 6), (15, 7)})
            total += 1
            if s in {2, m - 9, m - 8, m - 7} and s >= 2:
                print(f"m={m} s={s} vertices={n} geodesic_masks={masks} covered={best}/{m+1}")
    for m, s in ((20, 2), (20, 11), (20, 12), (30, 2), (30, 21), (30, 22)):
        n, masks, best = audit(m, s)
        total += 1
        print(f"m={m} s={s} vertices={n} geodesic_masks={masks} covered={best}/{m+1}")
    print(f"PASS {total} exact instances")


if __name__ == "__main__":
    main()
