#!/usr/bin/env python3
"""Exact affine-distance certificate for an infinite planar two-ear family."""

from collections import deque
from itertools import permutations

# An affine length is (coefficient of r, constant term), where r=m-7>=2.
SKELETON_EDGES = (
    (0, 1, (0, 1)), (1, 2, (0, 1)), (0, 4, (0, 1)),
    (0, 6, (0, 1)), (4, 5, (1, 1)), (5, 3, (0, 2)),
    (1, 3, (1, 0)), (1, 5, (1, 0)),
)
# Skeleton vertex 4 is q=m-1; vertex 6 is the pendant leaf t.
LANDMARKS = (2, 3, 5, 4, 6)
DISTANCE_FORMS = (
    ((0, 0), (1, 1), (1, 1), (0, 3), (0, 3)),
    ((1, 1), (0, 0), (0, 2), (1, 2), (1, 2)),
    ((1, 1), (0, 2), (0, 0), (1, 1), (1, 2)),
    ((0, 3), (1, 2), (1, 1), (0, 0), (0, 2)),
    ((0, 3), (1, 2), (1, 2), (0, 2), (0, 0)),
)


def affine_distance_certificate():
    graph = [[] for _ in range(7)]
    for u, v, length in SKELETON_EDGES:
        graph[u].append((v, length))
        graph[v].append((u, length))
    checked_paths = 0
    for i, source in enumerate(LANDMARKS):
        for j, target in enumerate(LANDMARKS):
            if i >= j:
                continue
            expected = DISTANCE_FORMS[i][j]
            exact_witness = False

            def visit(u, seen, form):
                nonlocal checked_paths, exact_witness
                if u == target:
                    checked_paths += 1
                    da = form[0] - expected[0]
                    db = form[1] - expected[1]
                    # A nonnegative affine difference on every r>=2.
                    assert da >= 0 and 2 * da + db >= 0
                    exact_witness |= form == expected
                    return
                for v, weight in graph[u]:
                    if v not in seen:
                        visit(v, seen | {v},
                              (form[0] + weight[0], form[1] + weight[1]))

            visit(source, {source}, (0, 0))
            assert exact_witness, (source, target)

    minimum_slack = 10**9
    for i, j, k in permutations(range(5), 3):
        ij, jk, ik = (DISTANCE_FORMS[a][b]
                      for a, b in ((i, j), (j, k), (i, k)))
        slope = ij[0] + jk[0] - ik[0]
        intercept = ij[1] + jk[1] - ik[1]
        assert slope >= 0 and 2 * slope + intercept >= 1
        minimum_slack = min(minimum_slack, 2 * slope + intercept)
    return checked_paths, minimum_slack


def family(m):
    assert m >= 9
    r = m - 7
    edges = [(i, (i + 1) % m) for i in range(m)] + [(0, m)]
    next_vertex = m + 1
    ears = []
    for source, target in ((1, 3), (1, 5)):
        first = next_vertex
        last = source
        for _ in range(r - 1):
            edges.append((last, next_vertex))
            last = next_vertex
            next_vertex += 1
        ears.append((first, last))
        edges.append((last, target))
    graph = [set() for _ in range(next_vertex)]
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    assert len(edges) == m + 1 + 2 * r
    return graph, ears


def faces_from_rotation(graph, ears, m):
    rotation = [sorted(row) for row in graph]
    rotation[0] = [m - 1, 1, m]
    rotation[1] = [0, ears[1][0], 2, ears[0][0]]
    rotation[3] = [2, 4, ears[0][1]]
    rotation[5] = [ears[1][1], 6, 4]
    assert all(set(row) == graph[u] and len(row) == len(graph[u])
               for u, row in enumerate(rotation))
    unseen = {(u, v) for u, row in enumerate(rotation) for v in row}
    faces = 0
    while unseen:
        start = min(unseen)
        dart = start
        while True:
            assert dart in unseen
            unseen.remove(dart)
            u, v = dart
            row = rotation[v]
            dart = (v, row[(row.index(u) - 1) % len(row)])
            if dart == start:
                break
        faces += 1
    return faces


def bfs(graph, source):
    distance = [-1] * len(graph)
    distance[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in graph[u]:
            if distance[v] < 0:
                distance[v] = distance[u] + 1
                queue.append(v)
    return distance


def finite_controls():
    for m in range(9, 25):
        graph, ears = family(m)
        faces = faces_from_rotation(graph, ears, m)
        n = len(graph)
        edge_count = sum(map(len, graph)) // 2
        assert faces == 4 and n - edge_count + faces == 2
        graph[2].remove(3)
        graph[3].remove(2)
        actual_landmarks = (2, 3, 5, m - 1, m)
        for i, source in enumerate(actual_landmarks):
            distance = bfs(graph, source)
            for j, target in enumerate(actual_landmarks):
                slope, constant = DISTANCE_FORMS[i][j]
                assert distance[target] == slope * (m - 7) + constant
    return 16


if __name__ == "__main__":
    paths, slack = affine_distance_certificate()
    controls = finite_controls()
    print(f"affine_simple_paths={paths} minimum_triangle_slack_r2={slack} "
          f"planar_bfs_controls={controls} PASS")
