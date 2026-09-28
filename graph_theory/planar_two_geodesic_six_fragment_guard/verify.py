#!/usr/bin/env python3
"""Classify robust six-vertex P3 tilings and audit a planar family.

Python 3.11+, standard library only. Vertices in the finite classification
are 0,...,5, and graph mask bit i denotes EDGE_LIST[i].
"""

from collections import Counter
from itertools import combinations, permutations


EDGE_LIST = tuple(combinations(range(6), 2))
EDGE_ID = {edge: i for i, edge in enumerate(EDGE_LIST)}
FULL6 = (1 << 6) - 1


def rows_from_mask(mask):
    rows = [0] * 6
    for i, (u, v) in enumerate(EDGE_LIST):
        if mask & (1 << i):
            rows[u] |= 1 << v
            rows[v] |= 1 << u
    return tuple(rows)


def components(rows, allowed):
    unseen = allowed
    answer = []
    while unseen:
        bit = unseen & -unseen
        unseen ^= bit
        reached = frontier = bit
        while frontier:
            step = frontier & -frontier
            frontier ^= step
            u = step.bit_length() - 1
            fresh = rows[u] & unseen
            unseen ^= fresh
            frontier |= fresh
            reached |= fresh
        answer.append(reached)
    return answer


def has_p3_partition(rows):
    """Can the six vertices split into two induced three-vertex paths?"""
    triples = set()
    for a, b, c in combinations(range(6), 3):
        edge_count = ((rows[a] >> b) & 1) + ((rows[a] >> c) & 1)
        edge_count += (rows[b] >> c) & 1
        if edge_count == 2:
            triples.add((1 << a) | (1 << b) | (1 << c))
    return any((FULL6 ^ triple) in triples for triple in triples)


def classify_six():
    """Two exact formulations of robustness, checked against each other."""
    total = 1 << len(EDGE_LIST)
    connected = [False] * total
    tiled = [False] * total
    robust = [False] * total

    # Induction on edge count: every connected one-edge deletion must
    # preserve robustness, and the current graph itself must be tiled.
    for mask in sorted(range(total), key=int.bit_count):
        rows = rows_from_mask(mask)
        connected[mask] = components(rows, FULL6) == [FULL6]
        if not connected[mask]:
            continue
        tiled[mask] = has_p3_partition(rows)
        robust[mask] = tiled[mask] and all(
            not connected[mask ^ (1 << e)] or robust[mask ^ (1 << e)]
            for e in range(len(EDGE_LIST)) if mask & (1 << e))

    # Independent Boolean subset transform: mark all masks that contain
    # any connected non-tileable spanning edge subgraph.
    contains_bad = [connected[m] and not tiled[m] for m in range(total)]
    for e in range(len(EDGE_LIST)):
        bit = 1 << e
        for mask in range(total):
            if mask & bit:
                contains_bad[mask] |= contains_bad[mask ^ bit]
    assert all(robust[m] == (connected[m] and not contains_bad[m])
               for m in range(total))

    # Canonicalize only robust graphs; all 6! relabelings are examined.
    permutation_maps = [tuple(EDGE_ID[tuple(sorted((p[u], p[v])))]
                              for u, v in EDGE_LIST)
                        for p in permutations(range(6))]

    def canonical(mask):
        used = [i for i in range(len(EDGE_LIST)) if mask & (1 << i)]
        return min(sum(1 << mapping[i] for i in used)
                   for mapping in permutation_maps)

    classes = Counter(canonical(m) for m, ok in enumerate(robust) if ok)
    expected = {121: 90, 122: 360, 692: 360, 246: 180, 1880: 60}
    assert dict(classes) == expected
    assert sum(connected) == 26704
    assert sum(tiled) == 22360
    assert sum(robust) == 1050
    assert Counter(m.bit_count() for m, ok in enumerate(robust) if ok) == {
        5: 810, 6: 240}
    return robust, classes


def octahedron_with_six_cycles(count):
    """Rotation system: add each 6-cycle inside the face incident to 01."""
    assert count >= 1
    rotation = [[1, 4, 3, 5], [2, 4, 0, 5], [3, 4, 1, 5],
                [0, 4, 2, 5], [0, 1, 2, 3], [0, 3, 2, 1]]
    for _ in range(count):
        a, b, c, d, e, f = range(len(rotation), len(rotation) + 6)
        rotation[0].insert(rotation[0].index(1) + 1, a)
        rotation[1].insert(rotation[1].index(0), f)
        rotation += [[0, f, b], [a, c], [b, d], [c, e], [d, f], [e, a, 1]]
    rows = []
    for u, order in enumerate(rotation):
        assert len(order) == len(set(order))
        assert all(0 <= v < len(rotation) and v != u for v in order)
        rows.append(sum(1 << v for v in order))
    return tuple(rows), tuple(tuple(order) for order in rotation)


def check_rotation(rows, rotation, count):
    n = len(rows)
    assert n == 6 + 6 * count
    darts = {(u, v) for u in range(n)
             for v in range(n) if rows[u] & (1 << v)}
    for u in range(n):
        assert set(rotation[u]) == {v for v in range(n)
                                    if rows[u] & (1 << v)}
    assert all((v, u) in darts for u, v in darts)
    unseen = darts.copy()
    faces = []
    while unseen:
        start = min(unseen)
        dart = start
        length = 0
        while True:
            assert dart in unseen
            unseen.remove(dart)
            length += 1
            u, v = dart
            order = rotation[v]
            dart = (v, order[(order.index(u) - 1) % len(order)])
            if dart == start:
                break
        faces.append(length)
    edges = len(darts) // 2
    assert edges == 12 + 8 * count
    assert len(faces) == 8 + 2 * count
    assert n - edges + len(faces) == 2
    return edges, len(faces)


def check_family(robust):
    for count in range(1, 9):
        rows, rotation = octahedron_with_six_cycles(count)
        edges, faces = check_rotation(rows, rotation, count)
        full = (1 << len(rows)) - 1
        assert components(rows, full) == [full]
        assert all(len(components(rows, full ^ (1 << v))) == 1
                   for v in range(len(rows)))
        guard = sum(1 << v for v in range(4))
        residual = components(rows, full ^ guard)
        assert sorted(c.bit_count() for c in residual) == \
            [1, 1] + [6] * count
        for comp in residual:
            if comp.bit_count() != 6:
                continue
            vertices = [v for v in range(len(rows)) if comp & (1 << v)]
            local_mask = sum(
                1 << i for i, (a, b) in enumerate(EDGE_LIST)
                if rows[vertices[a]] & (1 << vertices[b]))
            assert robust[local_mask]
            assert local_mask.bit_count() == 6
        print(f'cycles={count} vertices={len(rows)} edges={edges} '
              f'faces={faces} biconnected=yes')

    # An exact control for the pigeonhole argument in the written proof.
    rows, _ = octahedron_with_six_cycles(5)
    full = (1 << len(rows)) - 1
    assert all(any(c.bit_count() >= 6 for c in components(
                   rows, full ^ sum(1 << v for v in guard)))
               for guard in combinations(range(len(rows)), 4))


def main():
    robust, classes = classify_six()
    print('six-vertex connected=26704 individually tiled=22360 '
          'robust=1050 unlabeled_classes=5')
    print('canonical class counts:', sorted(classes.items()))
    check_family(robust)
    print('PASS')


if __name__ == '__main__':
    main()
