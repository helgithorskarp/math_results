#!/usr/bin/env python3
"""Exact, standard-library audit for the guarded weighted descent example."""

from collections import deque
from functools import lru_cache

ROWS = (656, 2052, 2058, 2052, 33, 4176, 8352, 321,
        9856, 1281, 13056, 49166, 9248, 5440, 34816, 18432)
ROTATION = ((4, 9, 7), (2, 11), (1, 3, 11), (2, 11), (0, 5),
            (4, 6, 12), (5, 7, 13), (6, 0, 8), (7, 9, 10, 13),
            (8, 0, 10), (9, 12, 13, 8), (3, 1, 2, 14, 15),
            (10, 5, 13), (12, 6, 8, 10), (11, 15), (14, 11))
N = len(ROWS)
ALL = (1 << N) - 1
CORE = (0, 4, 5, 6, 7, 8, 9, 10, 12, 13)
OTHER = (1, 2, 3, 11, 14, 15)
PRIMARY = ((1,), (4, 0, 7, 8))
SECONDARY = (((2, 11, 14), (3, 11, 15)),
             ((5, 12), (6, 13, 10, 9)))
CORE_WITNESS = ((4, 0, 9, 10), (7, 6, 13, 12))


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def mask_of(vertices):
    return sum(1 << v for v in vertices)


def components(rows, allowed=ALL):
    unseen = allowed
    answer = []
    while unseen:
        start = unseen & -unseen
        unseen ^= start
        component = start
        frontier = start
        while frontier:
            bit = frontier & -frontier
            frontier ^= bit
            v = bit.bit_length() - 1
            fresh = rows[v] & unseen
            frontier |= fresh
            component |= fresh
            unseen ^= fresh
        answer.append(component)
    return answer


def distances(rows):
    output = []
    for source in range(N):
        dist = [-1] * N
        dist[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in bits(rows[u]):
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        output.append(dist)
    return output


def check_path(path, rows, dist):
    assert path and len(path) == len(set(path))
    assert all(rows[u] & (1 << v) for u, v in zip(path, path[1:]))
    assert len(path) - 1 == dist[path[0]][path[-1]]
    return mask_of(path)


def geodesic_masks(rows, dist):
    answer = {1 << v for v in range(N)}

    def extend(source, target, vertex, used):
        if vertex == target:
            answer.add(used)
            return
        for nxt in bits(rows[vertex]):
            if (dist[source][nxt] == dist[source][vertex] + 1
                    and dist[nxt][target] >= 0
                    and dist[source][nxt] + dist[nxt][target]
                    == dist[source][target]):
                extend(source, target, nxt, used | (1 << nxt))

    for source in range(N):
        for target in range(source + 1, N):
            if dist[source][target] >= 0:
                extend(source, target, source, 1 << source)
    return answer


def check_planarity_rotation(rows):
    for u in range(N):
        assert not rows[u] & (1 << u)
        assert set(ROTATION[u]) == set(bits(rows[u]))
        for v in bits(rows[u]):
            assert rows[v] & (1 << u)
    sizes = []
    for component in components(rows):
        darts = {(u, v) for u in bits(component) for v in bits(rows[u])}
        remaining = darts.copy()
        faces = 0
        while remaining:
            first = min(remaining)
            dart = first
            while True:
                assert dart in remaining
                remaining.remove(dart)
                u, v = dart
                rotation = ROTATION[v]
                dart = (v, rotation[(rotation.index(u) - 1) % len(rotation)])
                if dart == first:
                    break
            faces += 1
        order = component.bit_count()
        edges = len(darts) // 2
        assert order - edges + faces == 2
        sizes.append((order, edges, faces))
    return sorted(sizes)


def treewidth_at_most_three(rows, allowed):
    # Elimination characterization. Branch on every possible vertex of degree <=3;
    # eliminate it and fill all edges among its live neighbors.
    @lru_cache(None)
    def search(state, live):
        if not live:
            return True
        for v in bits(live):
            neighbors = state[v] & live
            if neighbors.bit_count() > 3:
                continue
            child = list(state)
            for u in bits(neighbors):
                child[u] |= neighbors & ~(1 << u)
            child[v] = 0
            for u in bits(live & ~(1 << v)):
                child[u] &= ~(1 << v)
            if search(tuple(child), live & ~(1 << v)):
                return True
        return False

    return search(rows, allowed), search.cache_info().currsize


def main():
    print('rotation component (vertices,edges,faces):',
          check_planarity_rotation(ROWS))
    assert set(components(ROWS)) == {mask_of(CORE), mask_of(OTHER)}
    dist = distances(ROWS)
    paths = geodesic_masks(ROWS, dist)
    unions = {a | b for a in paths for b in paths}
    min_residual = min(max((c.bit_count() for c in components(
        ROWS, ALL & ~union)), default=0) for union in unions)
    assert min_residual == 6
    print('path masks:', len(paths), 'pair unions:', len(unions),
          'minimum largest residual component:', min_residual)

    primary = 0
    for path in PRIMARY:
        primary |= check_path(path, ROWS, dist)
    residual = components(ROWS, ALL & ~primary)
    assert set(residual) == {mask_of((2, 3, 11, 14, 15)),
                             mask_of((5, 6, 9, 10, 12, 13))}
    for comp, pair in ((mask_of((2, 3, 11, 14, 15)), SECONDARY[0]),
                       (mask_of((5, 6, 9, 10, 12, 13)), SECONDARY[1])):
        covered = 0
        for path in pair:
            covered |= check_path(path, ROWS, dist)
        assert comp & ~covered == 0
    protected = {tuple(sorted((u, v)))
                 for path in PRIMARY + SECONDARY[0] + SECONDARY[1]
                 for u, v in zip(path, path[1:])}
    assert len(protected) == 11
    print('guarded residual sizes:', sorted(c.bit_count() for c in residual))

    core_covered = 0
    for path in CORE_WITNESS:
        core_covered |= check_path(path, ROWS, dist)
    assert {c.bit_count() for c in components(ROWS,
            mask_of(CORE) & ~core_covered)} == {1}
    core_tw3, root_states = treewidth_at_most_three(ROWS, mask_of(CORE))
    assert not core_tw3
    core_edges = [(u, v) for u in CORE for v in CORE
                  if u < v and ROWS[u] & (1 << v)]
    assert len(core_edges) == 16
    for u, v in core_edges:
        child = list(ROWS)
        child[u] &= ~(1 << v)
        child[v] &= ~(1 << u)
        assert treewidth_at_most_three(tuple(child), mask_of(CORE))[0]
    assert treewidth_at_most_three(ROWS, mask_of(OTHER))[0]
    print('ten-vertex core: treewidth >3; all', len(core_edges),
          'single-edge deletions have treewidth <=3; root search states:',
          root_states)
    print('PASS')


if __name__ == '__main__':
    main()
