"""Independent set-based checker for the radius-four guarded templates.

Run from repository root with Python 3.11+. Uses only the published JSON
certificate and the standard library; imports no target routines.
"""

import json
from collections import deque
from itertools import combinations
from pathlib import Path


CERTIFICATE = Path('graph_theory/planar_two_geodesic_template_radius20/certificates.json')
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


def decode_graph6(record):
    assert record == GRAPH6
    n = ord(record[0]) - 63
    assert n == 20
    stream = ''.join(f'{ord(c)-63:06b}' for c in record[1:])
    assert len(stream) >= n * (n - 1) // 2
    assert set(stream[n * (n - 1) // 2:]) <= {'0'}
    adj = [set() for _ in range(n)]
    pos = 0
    for high in range(1, n):
        for low in range(high):
            if stream[pos] == '1':
                adj[low].add(high)
                adj[high].add(low)
            pos += 1
    assert all(v not in adj[v] for v in range(n))
    return tuple(frozenset(row) for row in adj)


def edge(u, v):
    return tuple(sorted((u, v)))


def components(adj, removed=()):
    unseen = set(range(len(adj))) - set(removed)
    result = []
    while unseen:
        start = unseen.pop()
        part = {start}
        pending = deque([start])
        while pending:
            u = pending.popleft()
            for v in adj[u] & unseen:
                unseen.remove(v)
                part.add(v)
                pending.append(v)
        result.append(frozenset(part))
    return result


def distances(adj):
    output = []
    for start in range(len(adj)):
        d = {start: 0}
        pending = deque([start])
        while pending:
            u = pending.popleft()
            for v in adj[u]:
                if v not in d:
                    d[v] = d[u] + 1
                    pending.append(v)
        output.append(d)
    return output


def check_rotation(adj):
    assert len(components(adj)) == 1
    assert all(set(ROTATION[v]) == adj[v] for v in range(len(adj)))
    darts = {(u, v) for u, row in enumerate(adj) for v in row}
    remaining = darts.copy()
    faces = []
    while remaining:
        initial = next(iter(remaining))
        current = initial
        face = []
        while True:
            assert current in remaining
            remaining.remove(current)
            face.append(current)
            u, v = current
            order = ROTATION[v]
            current = (v, order[(order.index(u) + 1) % len(order)])
            if current == initial:
                break
        faces.append(face)
    assert len(darts) == 108 and len(faces) == 36
    assert all(len(face) == 3 for face in faces)
    assert len(adj) - len(darts) // 2 + len(faces) == 2


def paths_cover(pair, adj, dist):
    assert isinstance(pair, list) and len(pair) == 2
    vertices = set()
    edges = set()
    for path in pair:
        assert path and len(path) == len(set(path))
        assert all(isinstance(v, int) and 0 <= v < len(adj) for v in path)
        assert len(path) - 1 == dist[path[0]][path[-1]]
        for u, v in zip(path, path[1:]):
            assert v in adj[u]
            edges.add(edge(u, v))
        vertices.update(path)
    return vertices, edges


def validate_template(template, adj, dist):
    removed, protected = paths_cover(template['primary'], adj, dist)
    parts = components(adj, removed)
    exceptional = {part for part in parts if len(part) > 5}
    for part in parts:
        if len(part) == 5:
            assert any(v not in adj[u] for u, v in combinations(part, 2))
    listed = set()
    for item in template['secondary']:
        part = frozenset(item['component'])
        assert part in exceptional and part not in listed
        listed.add(part)
        covered, used_edges = paths_cover(item['paths'], adj, dist)
        assert part <= covered
        protected |= used_edges
    assert listed == exceptional
    return frozenset(protected), sorted(len(part) for part in parts)


def main():
    data = json.loads(CERTIFICATE.read_text())
    adj = decode_graph6(data['graph6'])
    check_rotation(adj)
    edges = sorted(edge(u, v) for u, row in enumerate(adj) for v in row if u < v)
    assert len(edges) == 54
    dist = distances(adj)
    templates = data['templates']
    assert len(templates) == 21
    protected = [validate_template(item, adj, dist)[0] for item in templates]
    assert len(set(protected)) == len(protected)
    assert (min(map(len, protected)), max(map(len, protected))) == (11, 15)
    star = frozenset(edge(12, v) for v in adj[12])
    assert star == frozenset(map(tuple, data['exception']['deleted_edges']))
    assert len(star) == 4
    child = tuple(frozenset(v for v in row if edge(u, v) not in star)
                  for u, row in enumerate(adj))
    assert sorted(map(len, components(child))) == [1, 19]
    child_protected, child_residual = validate_template(
        data['exception'], child, distances(child))
    assert child_residual == [1, 6, 6]
    assert len(child_protected) == 16 and not child_protected & star
    covered = []
    exceptions = []
    for count in range(5):
        accepted = 0
        for deleted in combinations(edges, count):
            choice = frozenset(deleted)
            if any(choice.isdisjoint(cert) for cert in protected):
                accepted += 1
            else:
                exceptions.append(choice)
        covered.append(accepted)
    assert covered == [1, 54, 1431, 24804, 316250]
    assert exceptions == [star]
    print('embedding: vertices=20 edges=54 triangular_faces=36')
    print('templates=21 protected_range=11..15')
    print(f'covered={covered} unique_exception={sorted(star)}')
    print(f'exception_child_residuals={child_residual}')
    print(f'fallback_protected={len(child_protected)} '
          f'certified_five_edge_extensions={54-len(star)-len(child_protected)}')


if __name__ == '__main__':
    main()
