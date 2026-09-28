#!/usr/bin/env python3
"""Exact finite checks of a prescribed-path obstruction, not Problem 31."""
import argparse
from collections import deque
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def cone(m, triangulated=False):
    require(m >= 2, 'm must be at least two')
    ears = [list(range(4+j*m, 4+(j+1)*m)) for j in range(3)]
    edges = {(1, 2), (1, 3), (2, 3)}
    faces = [(1, 2, 3)]
    boundary = []
    for (a, b), ear in zip(((1, 2), (2, 3), (3, 1)), ears):
        chain = [a] + ear + [b]
        boundary.extend(chain[:-1])
        edges.update(tuple(sorted(pair)) for pair in zip(chain, chain[1:]))
        if triangulated:
            edges.update(tuple(sorted((a, x))) for x in ear)
            faces.extend((a, chain[i], chain[i+1]) for i in range(1, len(chain)-1))
        else:
            faces.append(tuple(chain))
    edges.update((0, v) for v in boundary)
    faces.extend((0, boundary[(i+1) % len(boundary)], boundary[i])
                 for i in range(len(boundary)))
    return 3*m+4, edges, faces, ears


def instance(k, m, triangulated=False):
    require(k >= 4, 'k must be at least four')
    n, edges, faces, ears = cone(m, triangulated)
    inner = list(range(n+k-2, n+2*k-2))
    outer = ears[0][:2] + list(range(n, n+k-2))
    n += 2*k-2
    faces.remove((0, ears[0][1], ears[0][0]))
    for i in range(k):
        a, b = outer[i], outer[(i+1) % k]
        c, d = inner[i], inner[(i+1) % k]
        edges.update(tuple(sorted(pair)) for pair in ((0, a), (a, b), (c, d), (a, c), (a, d)))
        if i != 0:
            faces.append((0, a, b))
        faces.extend(((a, d, b), (a, c, d)))
    faces.append(tuple(reversed(inner)))
    adj = [set() for _ in range(n)]
    for u, v in edges:
        require(0 <= u < v < n, 'simple labeled edge')
        adj[u].add(v)
        adj[v].add(u)
    return adj, faces, ears, outer, inner


def components(adj, deleted):
    unseen = set(range(len(adj))) - set(deleted)
    result = []
    while unseen:
        pending = [unseen.pop()]
        reached = set(pending)
        while pending:
            u = pending.pop()
            neighbors = adj[u] & unseen
            unseen.difference_update(neighbors)
            reached.update(neighbors)
            pending.extend(neighbors)
        result.append(reached)
    return result


def sphere(adj, faces):
    darts = set()
    rotation = [dict() for _ in adj]
    for face in faces:
        require(len(face) >= 3 and len(set(face)) == len(face), 'simple facial cycle')
        for i, u in enumerate(face):
            before, after = face[i-1], face[(i+1) % len(face)]
            require(after in adj[u] and (u, after) not in darts, 'face dart')
            require(before not in rotation[u], 'one successor per dart')
            darts.add((u, after))
            rotation[u][before] = after
    require(darts == {(u, v) for u, row in enumerate(adj) for v in row}, 'all darts')
    for u, row in enumerate(rotation):
        require(set(row) == set(row.values()) == adj[u], 'rotation domain')
        start = min(row)
        seen, v = set(), start
        while v not in seen:
            seen.add(v)
            v = row[v]
        require(v == start and seen == adj[u], 'one cyclic vertex link')
    require(len(adj)-len(darts)//2+len(faces) == 2, 'Euler characteristic two')
    require(len(components(adj, [])) == 1, 'connected embedding')


def distances(adj):
    rows = []
    for s in range(len(adj)):
        dist = [-1]*len(adj)
        dist[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if dist[v] < 0:
                    dist[v] = dist[u]+1
                    queue.append(v)
        require(min(dist) == 0, 'all vertices reached')
        rows.append(dist)
    return rows


def geodesics(adj, dist):
    # Every distance-increasing prefix is shortest; keep one orientation.
    for s in range(len(adj)):
        def extend(path):
            u = path[-1]
            if u >= s:
                yield path
            for v in sorted(adj[u]):
                if dist[s][v] == dist[s][u]+1:
                    yield from extend(path+(v,))
        yield from extend((s,))


def check_path(adj, dist, path):
    require(path and len(set(path)) == len(path), 'nonempty simple path')
    require(all(v in adj[u] for u, v in zip(path, path[1:])), 'path edges')
    require(len(path)-1 == dist[path[0]][path[-1]], 'ambient geodesic')


def local_check(m, result):
    n, edges, _, ears = cone(m)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u != 0:
            adj[u].add(v)
            adj[v].add(u)
    vertices = list(range(1, n))
    internal = set(sum(ears, []))
    triples = set()
    for center in vertices:
        for a, b in combinations(sorted(adj[center]), 2):
            if b not in adj[a]:
                triples.add(tuple(sorted((a, center, b))))
    sets = [()] + [(v,) for v in vertices] + list(combinations(vertices, 2)) + sorted(triples)
    for deleted in sets:
        central = {1, 2, 3} - set(deleted)
        require(central, 'some central vertex survives')
        region = next(c for c in components(adj, {0, *deleted}) if c & central)
        require(central <= region, 'surviving clique is connected')
        require(len(region & internal) >= 2*m-1, 'weighted local lower bound')
        require(len(region) >= 2*m, 'uniform local lower bound')
        result['local_deletion_sets'] += 1
    # A forbidden three-clique deletion has only m vertices per component.
    require(max(map(len, components(adj, {0, 1, 2, 3}))) == m, 'clique control')
    result['local_parameters'] += 1
    result['clique_controls'] += 1


def full_check(k, m, result, triangulated=False):
    adj, faces, ears, outer, inner = instance(k, m, triangulated)
    n = len(adj)
    sphere(adj, faces)
    dist = distances(adj)
    p = (0, outer[2], inner[2])
    check_path(adj, dist, p)
    require(n == 3*m+2*k+2, 'order')
    require(set(range(n))-adj[0]-{0} == set(inner), 'nonneighbors')
    require(all(adj[v] & set(inner) == {inner[(i-1) % k], inner[(i+1) % k]}
                for i, v in enumerate(inner)), 'chordless nonneighbor cycle')
    require(set(p) & set(range(1, 3*m+4)) == set(), 'prescribed path avoids pocket')
    support = set(sum(ears, []))
    best_mass = best_count = n
    for q in geodesics(adj, dist):
        check_path(adj, dist, q)
        cuts = components(adj, set(p) | set(q))
        largest_mass = max((len(c & support) for c in cuts), default=0)
        largest_count = max(map(len, cuts), default=0)
        best_mass = min(best_mass, largest_mass)
        best_count = min(best_count, largest_count)
        result['ambient_geodesics'] += 1
    if triangulated:
        require(best_count <= 13, 'fan control has a valid completion')
        result['triangulated_control_optimum'] = best_count
        result['triangulated_controls'] += 1
        return
    require(best_mass == 2*m-1, 'exact weighted optimum')
    require(best_count >= 2*m, 'uniform lower bound')
    if m >= 2*k-4:
        require(best_count == 2*m, 'exact uniform optimum')
    q_star = (1, 2, ears[1][0])
    check_path(adj, dist, q_star)
    q_cuts = components(adj, set(p) | set(q_star))
    require(max(len(c & support) for c in q_cuts) == 2*m-1, 'weighted upper witness')
    require(max(map(len, q_cuts)) <= max(2*m, m+2*k-4), 'uniform upper witness')
    free = ((0, 1), (2, 3))
    for path in free:
        check_path(adj, dist, path)
    cuts = components(adj, {0, 1, 2, 3})
    require(sorted(map(len, cuts)) == [m, m, m+2*k-2], 'unrestricted uniform witness')
    require(sorted(len(c & support) for c in cuts) == [m, m, m], 'unrestricted mass witness')
    if m > 2*k+2:
        require(2*best_count > n, 'prescribed uniform failure')
        require(2*max(map(len, cuts)) <= n, 'unrestricted uniform success')
        result['uniform_failures'] += 1
    if (k, m) == (4, 3):
        result['nineteen_vertex_weighted_optimum'] = best_mass
    if (k, m) == (4, 10):
        require(2*best_count == n, 'uniform equality control')
        result['uniform_equality_controls'] += 1
    if (k, m) == (4, 11):
        result['forty_three_vertex_optimum'] = best_count
        result['forty_three_vertex_free_largest'] = max(map(len, cuts))
    if m == 2:
        require(2*best_mass == 3*m, 'weighted equality control')
        result['weighted_equality_controls'] += 1
    result['full_fixtures'] += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = dict(local_parameters=0, local_deletion_sets=0, clique_controls=0,
                  full_fixtures=0, ambient_geodesics=0, uniform_failures=0,
                  weighted_equality_controls=0, uniform_equality_controls=0,
                  triangulated_controls=0)
    for m in range(2, 17):
        local_check(m, result)
    for k, m in ((4, 2), (4, 3), (4, 10), (4, 11), (4, 12), (5, 13), (6, 15)):
        full_check(k, m, result)
    full_check(4, 11, result, triangulated=True)
    if args.check:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        require(result == expected, ('expected output mismatch', result, expected))
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
