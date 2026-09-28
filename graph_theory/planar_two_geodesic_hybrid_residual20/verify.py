#!/usr/bin/env python3
"""Exact audit of a connected guarded-residual planar triangulation."""

from collections import deque

GRAPH6 = 'S|fIID`KGo`@B@@`_OgE@?OC@oG?oW?Xs'
N = 20
FULL = (1 << N) - 1
ROWS_EXPECTED = (62, 485, 779, 1557, 7209, 12371, 57506, 229698,
                 131718, 394508, 789016, 554000, 10288, 22624,
                 567360, 606400, 950400, 328576, 722432, 379904)
ROTATION = (
    (1, 5, 4, 3, 2), (0, 2, 8, 7, 6, 5), (1, 0, 3, 9, 8),
    (2, 0, 4, 10, 9), (3, 0, 5, 12, 11, 10), (4, 0, 1, 6, 13, 12),
    (5, 1, 7, 15, 14, 13), (6, 1, 8, 17, 16, 15),
    (7, 1, 2, 9, 17), (8, 2, 3, 10, 18, 17),
    (9, 3, 4, 11, 19, 18), (10, 4, 12, 13, 14, 19),
    (11, 4, 5, 13), (12, 5, 6, 14, 11),
    (13, 6, 15, 19, 11), (14, 6, 7, 16, 19),
    (15, 7, 17, 18, 19), (16, 7, 8, 9, 18),
    (17, 9, 10, 19, 16), (18, 10, 11, 14, 15, 16))
PRIMARY = ((0, 4, 10, 18), (12, 5, 6, 7, 17))
SECONDARY = ((11, 19, 16), (13, 14, 15))
SMALL_RESIDUAL = frozenset((1, 2, 3, 8, 9))
LARGE_RESIDUAL = frozenset((11, 13, 14, 15, 16, 19))


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def vertex_mask(xs):
    return sum(1 << x for x in xs)


def decode_graph6(data):
    assert ord(data[0]) == N + 63
    count = N * (N - 1) // 2
    assert len(data) == 1 + (count + 5) // 6
    digits = [ord(c) - 63 for c in data[1:]]
    assert all(0 <= d < 64 for d in digits)
    rows = [0] * N
    position = 0
    for v in range(1, N):
        for u in range(v):
            if digits[position // 6] & (1 << (5 - position % 6)):
                rows[u] |= 1 << v
                rows[v] |= 1 << u
            position += 1
    assert all(not digits[k // 6] & (1 << (5 - k % 6))
               for k in range(count, 6 * len(digits)))
    return tuple(rows)


def components(rows, allowed=FULL):
    remaining = allowed
    answer = []
    while remaining:
        start = remaining & -remaining
        remaining ^= start
        comp = start
        frontier = start
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            u = bit.bit_length() - 1
            fresh = rows[u] & remaining
            frontier |= fresh
            comp |= fresh
            remaining ^= fresh
        answer.append(comp)
    return answer


def check_embedding(rows):
    assert len(ROTATION) == N
    for u in range(N):
        assert not rows[u] & (1 << u)
        assert set(ROTATION[u]) == set(vertices(rows[u]))
        for v in vertices(rows[u]):
            assert rows[v] & (1 << u)
    assert components(rows) == [FULL]
    darts = {(u, v) for u in range(N) for v in vertices(rows[u])}
    unseen = darts.copy()
    lengths = []
    while unseen:
        first = min(unseen)
        dart = first
        length = 0
        while True:
            assert dart in unseen
            unseen.remove(dart)
            length += 1
            u, v = dart
            r = ROTATION[v]
            dart = (v, r[(r.index(u) - 1) % len(r)])
            if dart == first:
                break
        lengths.append(length)
    edges = len(darts) // 2
    faces = len(lengths)
    assert edges == 54 and faces == 36 and N - edges + faces == 2
    assert set(lengths) == {3}
    return edges, faces


def all_distances(rows):
    result = []
    for source in range(N):
        dist = [-1] * N
        dist[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in vertices(rows[u]):
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        assert all(d >= 0 for d in dist)
        result.append(dist)
    return result


def all_geodesics(rows, dist):
    paths = []

    def extend(source, target, path):
        u = path[-1]
        if u == target:
            paths.append(tuple(path))
            return
        for v in vertices(rows[u]):
            if (dist[source][v] == len(path)
                    and dist[source][v] + dist[v][target]
                    == dist[source][target]):
                extend(source, target, path + [v])

    for source in range(N):
        for target in range(source, N):
            extend(source, target, [source])
    return paths


def check_path(path, rows, dist):
    assert len(path) == len(set(path))
    assert all(rows[u] & (1 << v) for u, v in zip(path, path[1:]))
    assert len(path) - 1 == dist[path[0]][path[-1]]
    return vertex_mask(path)


def main():
    rows = decode_graph6(GRAPH6)
    assert rows == ROWS_EXPECTED
    edges, faces = check_embedding(rows)
    dist = all_distances(rows)
    paths = all_geodesics(rows, dist)
    masks = {vertex_mask(p) for p in paths}
    unions = {a | b for a in masks for b in masks}
    largest = [max((c.bit_count() for c in components(rows, FULL & ~u)),
                   default=0) for u in unions]
    assert len(paths) == len(masks) == 425
    assert len(unions) == 36159
    assert min(largest) == 6 and largest.count(6) == 151
    print('triangulation:', N, 'vertices,', edges, 'edges,', faces, 'triangular faces')
    print('geodesics:', len(paths), 'pair unions:', len(unions),
          'minimum largest residual:', min(largest),
          'minimum-attaining unions:', largest.count(6))

    primary = 0
    for path in PRIMARY:
        primary |= check_path(path, rows, dist)
    residual = components(rows, FULL & ~primary)
    assert set(residual) == {vertex_mask(SMALL_RESIDUAL),
                             vertex_mask(LARGE_RESIDUAL)}
    assert any(not rows[u] & (1 << v)
               for u in SMALL_RESIDUAL for v in SMALL_RESIDUAL if u < v)
    covered = 0
    for path in SECONDARY:
        covered |= check_path(path, rows, dist)
    assert vertex_mask(LARGE_RESIDUAL) & ~covered == 0
    protected = {tuple(sorted((u, v)))
                 for path in PRIMARY + SECONDARY
                 for u, v in zip(path, path[1:])}
    assert len(protected) == 11
    print('hybrid residual sizes:', sorted(c.bit_count() for c in residual),
          'protected edges:', len(protected))
    print('PASS')


if __name__ == '__main__':
    main()
