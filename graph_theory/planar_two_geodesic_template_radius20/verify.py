#!/usr/bin/env python3
"""Check 21 path templates and all <=4-edge deletions of a triangulation."""

import json
from collections import deque
from itertools import combinations
from pathlib import Path

N = 20
FULL = (1 << N) - 1
GRAPH6 = 'S|fIID`KGo`@B@@`_OgE@?OC@oG?oW?Xs'
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


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def vertex_mask(items):
    return sum(1 << v for v in items)


def decode_graph6(data):
    assert len(data) == 1 + (N * (N - 1) // 2 + 5) // 6
    assert ord(data[0]) == N + 63
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
    assert all(not digits[i // 6] & (1 << (5 - i % 6))
               for i in range(position, 6 * len(digits)))
    return tuple(rows)


def components(rows, allowed=FULL):
    remaining = allowed
    result = []
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        frontier = bit
        comp = bit
        while frontier:
            item = frontier & -frontier
            frontier ^= item
            u = item.bit_length() - 1
            fresh = rows[u] & remaining
            frontier |= fresh
            comp |= fresh
            remaining ^= fresh
        result.append(comp)
    return result


def check_embedding(rows):
    assert components(rows) == [FULL]
    darts = set()
    for u in range(N):
        assert not rows[u] & (1 << u)
        assert set(ROTATION[u]) == set(vertices(rows[u]))
        for v in vertices(rows[u]):
            assert rows[v] & (1 << u)
            darts.add((u, v))
    remaining = darts.copy()
    faces = []
    while remaining:
        start = min(remaining)
        dart = start
        length = 0
        while True:
            assert dart in remaining
            remaining.remove(dart)
            length += 1
            u, v = dart
            order = ROTATION[v]
            dart = (v, order[(order.index(u) - 1) % len(order)])
            if dart == start:
                break
        faces.append(length)
    assert len(darts) == 108
    assert len(faces) == 36 and all(n == 3 for n in faces)
    assert N - len(darts) // 2 + len(faces) == 2


def distances(rows):
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
        result.append(dist)
    return result


def edge_list(rows):
    return [(u, v) for u in range(N) for v in range(u + 1, N)
            if rows[u] & (1 << v)]


def check_paths(pair, rows, dist, edge_ids):
    assert len(pair) == 2
    vertex_union = edge_union = 0
    for path in pair:
        assert path and all(isinstance(v, int) and 0 <= v < N for v in path)
        assert len(set(path)) == len(path)
        assert len(path) - 1 == dist[path[0]][path[-1]]
        for u, v in zip(path, path[1:]):
            assert rows[u] & (1 << v)
            edge_union |= 1 << edge_ids[tuple(sorted((u, v)))]
        vertex_union |= vertex_mask(path)
    return vertex_union, edge_union


def check_hybrid(entry, rows, dist, edge_ids):
    primary_vertices, protected = check_paths(
        entry['primary'], rows, dist, edge_ids)
    residual = components(rows, FULL & ~primary_vertices)
    exceptional = {c for c in residual if c.bit_count() > 5}
    for c in residual:
        if c.bit_count() == 5:
            vs = list(vertices(c))
            assert any(not rows[u] & (1 << v)
                       for u in vs for v in vs if u < v)
    seen = set()
    for item in entry['secondary']:
        labels = item['component']
        assert len(labels) == len(set(labels))
        assert all(isinstance(v, int) and 0 <= v < N for v in labels)
        c = vertex_mask(labels)
        assert c in exceptional and c not in seen
        seen.add(c)
        covered, edges = check_paths(item['paths'], rows, dist, edge_ids)
        assert c & ~covered == 0
        protected |= edges
    assert seen == exceptional
    return protected, sorted(c.bit_count() for c in residual)


def main():
    data = json.loads(Path(__file__).with_name('certificates.json').read_text())
    assert data['graph6'] == GRAPH6
    rows = decode_graph6(data['graph6'])
    check_embedding(rows)
    edges = edge_list(rows)
    assert len(edges) == 54
    edge_ids = {edge: i for i, edge in enumerate(edges)}
    dist = distances(rows)

    templates = data['templates']
    assert len(templates) == 21
    protected = [check_hybrid(t, rows, dist, edge_ids)[0] for t in templates]
    assert len(set(protected)) == 21
    assert min(x.bit_count() for x in protected) == 11
    assert max(x.bit_count() for x in protected) == 15

    exception = data['exception']
    missing = exception['deleted_edges']
    assert missing == [[4, 12], [5, 12], [11, 12], [12, 13]]
    exception_mask = sum(1 << edge_ids[tuple(edge)] for edge in missing)
    assert exception_mask.bit_count() == 4
    child = list(rows)
    for u, v in missing:
        child[u] &= ~(1 << v)
        child[v] &= ~(1 << u)
    assert {c.bit_count() for c in components(child)} == {1, 19}
    _, child_residual = check_hybrid(
        exception, tuple(child), distances(child), edge_ids)
    assert child_residual == [1, 6, 6]

    covered_counts = []
    exceptional_masks = []
    for k in range(5):
        covered_count = 0
        for choices in combinations(range(len(edges)), k):
            deleted = sum(1 << i for i in choices)
            if any((deleted & e) == 0 for e in protected):
                covered_count += 1
            else:
                exceptional_masks.append(deleted)
        covered_counts.append(covered_count)
    assert covered_counts == [1, 54, 1431, 24804, 316250]
    assert exceptional_masks == [exception_mask]
    print('triangulation: 20 vertices, 54 edges, 36 triangular faces')
    print('templates:', len(templates), 'protected edges: 11..15')
    print('covered deletion counts k=0..4:', covered_counts)
    print('unique uncovered deletion: star of vertex 12; child residuals:',
          child_residual)
    print('PASS')


if __name__ == '__main__':
    main()
