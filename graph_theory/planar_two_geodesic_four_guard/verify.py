#!/usr/bin/env python3
"""Audit the explicit planar family in the dynamic four-vertex guard lemma."""

from itertools import combinations


def octahedron_with_ears(count):
    assert count >= 1
    rotation = [[(i + 1) % 4, 4, (i - 1) % 4, 5]
                for i in range(4)]
    rotation += [[0, 1, 2, 3], [0, 3, 2, 1]]
    for _ in range(count):
        start = len(rotation)
        path = list(range(start, start + 5))
        # Both insertions occur in the face next to the equatorial edge 01.
        rotation[0].insert(rotation[0].index(1) + 1, path[0])
        rotation[1].insert(rotation[1].index(0), path[-1])
        for i in range(5):
            rotation.append([0 if i == 0 else path[i - 1],
                             1 if i == 4 else path[i + 1]])
    rows = [0] * len(rotation)
    for u, order in enumerate(rotation):
        assert len(order) == len(set(order))
        for v in order:
            assert 0 <= v < len(rotation) and v != u
            rows[u] |= 1 << v
    return tuple(rows), tuple(tuple(order) for order in rotation)


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


def check_guard(rows, guard, paths=2):
    assert len(guard) == len(set(guard)) <= 2 * paths
    n = len(rows)
    assert all(0 <= v < n for v in guard)
    keep = ((1 << n) - 1) ^ sum(1 << v for v in guard)
    residual = components(rows, keep)
    for comp in residual:
        size = comp.bit_count()
        assert size <= 2 * paths + 1
        if size == 2 * paths + 1:
            vertices = [v for v in range(n) if comp & (1 << v)]
            assert any(not rows[u] & (1 << v)
                       for u, v in combinations(vertices, 2))
    return sorted(comp.bit_count() for comp in residual)


def check_rotation(rows, rotation, ears):
    n = len(rows)
    assert n == 6 + 5 * ears
    darts = {(u, v) for u in range(n)
             for v in range(n) if rows[u] & (1 << v)}
    for u in range(n):
        assert set(rotation[u]) == {v for v in range(n)
                                    if rows[u] & (1 << v)}
        for v in rotation[u]:
            assert (v, u) in darts
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
    assert edges == 12 + 6 * ears
    assert len(faces) == 8 + ears
    assert n - edges + len(faces) == 2
    return edges, len(faces)


def check_biconnected(rows):
    n = len(rows)
    full = (1 << n) - 1
    assert components(rows, full) == [full]
    for v in range(n):
        assert len(components(rows, full ^ (1 << v))) == 1


def main():
    for count in range(1, 5):
        rows, rotation = octahedron_with_ears(count)
        edges, faces = check_rotation(rows, rotation, count)
        check_biconnected(rows)
        residual = check_guard(rows, (0, 1, 2, 3))
        assert residual == [1, 1] + [5] * count
        assert all((rows[v] & 63).bit_count() == 4
                   for v in range(6))
        print(f'ears={count} vertices={len(rows)} edges={edges} '
              f'faces={faces} residuals={residual}')
    print('PASS')


if __name__ == '__main__':
    main()
