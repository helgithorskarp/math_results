#!/usr/bin/env python3
"""Construct and directly check proof witnesses; no planar enumeration."""

import argparse
import itertools
import json
from collections import deque
from pathlib import Path


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < n and 0 <= v < n and u != v
        adj[u].add(v)
        adj[v].add(u)
    return [sorted(row) for row in adj]


def components(adj, deleted=()):
    unseen = set(range(len(adj))) - set(deleted)
    result = []
    while unseen:
        source = min(unseen)
        unseen.remove(source)
        queue = [source]
        found = [source]
        while queue:
            u = queue.pop()
            for v in adj[u]:
                if v in unseen:
                    unseen.remove(v)
                    queue.append(v)
                    found.append(v)
        result.append(sorted(found))
    return result


def bfs(adj, source):
    dist = [None]*len(adj)
    parent = [None]*len(adj)
    dist[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] is None:
                dist[v] = dist[u]+1
                parent[v] = u
                queue.append(v)
    return dist, parent


def shortest_path(adj, source, target):
    dist, parent = bfs(adj, source)
    assert dist[target] is not None
    path = [target]
    while path[-1] != source:
        path.append(parent[path[-1]])
    return path[::-1]


def induced_p3(adj, allowed):
    allowed = set(allowed)
    for middle in sorted(allowed):
        neighbors = [u for u in adj[middle] if u in allowed]
        for u, v in itertools.combinations(neighbors, 2):
            if v not in adj[u]:
                return [u, middle, v]
    return None


def largest(adj, paths):
    deleted = {u for path in paths for u in path}
    return max((len(c) for c in components(adj, deleted)), default=0)


def two_path_witness(adj):
    """Returns a witness when this note's sufficient conditions apply.

    A return value of None is NOT a certificate of nonexistence outside them.
    The actual component condition is always checked before returning paths.
    """
    n = len(adj)
    heavy = next((c for c in components(adj) if 2*len(c) > n), None)
    if heavy is None:
        return [], 'already_balanced'
    if n <= 8:
        chosen = heavy[:4]
        paths = [shortest_path(adj, chosen[i], chosen[min(i+1, len(chosen)-1)])
                 for i in range(0, len(chosen), 2)]
        assert 2*largest(adj, paths) <= n
        return paths, 'endpoint_cover'
    # All searches stay in the heavy connected component, but distances are
    # computed in the original graph, where its paths remain geodesic.
    best = None
    for source in heavy:
        dist, _ = bfs(adj, source)
        for target in heavy:
            candidate = (dist[target], -source, -target)
            if best is None or candidate > best:
                best = candidate
    _, minus_s, minus_t = best
    P = shortest_path(adj, -minus_s, -minus_t)
    if 2*largest(adj, [P]) <= n:
        return [P], 'diametral_path_alone'
    Q = induced_p3(adj, set(range(n))-set(P))
    if Q is not None and 2*largest(adj, [P, Q]) <= n:
        return [P, Q], 'diametral_path_plus_P3'
    return None


def packing_witness(adj, k):
    remaining = set(range(len(adj)))
    paths = []
    for _ in range(k):
        P = induced_p3(adj, remaining)
        if P is None:
            break
        paths.append(P)
        remaining.difference_update(P)
    return paths if 2*largest(adj, paths) <= len(adj) else None


def verify_witness(adj, paths, k):
    assert paths is not None and len(paths) <= k
    n = len(adj)
    # Floyd--Warshall checks ambient distances independently of BFS path
    # construction. Its sentinel n+1 exceeds every finite simple distance.
    d = [[n+1]*n for _ in range(n)]
    for u in range(n):
        d[u][u] = 0
        for v in adj[u]:
            d[u][v] = 1
    for z in range(n):
        for u in range(n):
            for v in range(n):
                d[u][v] = min(d[u][v], d[u][z]+d[z][v])
    for P in paths:
        assert P and len(P) == len(set(P))
        assert all(v in adj[u] for u, v in zip(P, P[1:]))
        assert d[P[0]][P[-1]] == len(P)-1
    assert 2*largest(adj, paths) <= n


def complete_bipartite(a, b):
    return graph(a+b, [(u, v) for u in range(a) for v in range(a, a+b)])


def all_geodesic_masks(adj):
    masks = set()
    for source in range(len(adj)):
        dist, _ = bfs(adj, source)

        def enumerate_paths(v):
            if v == source:
                yield (source,)
            else:
                for u in adj[v]:
                    if dist[u] == dist[v]-1:
                        for prefix in enumerate_paths(u):
                            yield prefix+(v,)

        for target in range(source, len(adj)):
            if dist[target] is not None:
                for P in enumerate_paths(target):
                    masks.add(frozenset(P))
    return sorted(masks, key=lambda x: (len(x), sorted(x)))


def fixtures():
    yield 'empty', graph(0, [])
    for n in range(1, 9):
        name = f'K{n}' if n <= 4 else f'K{n}_nonplanar_endpoint_control'
        yield name, graph(n, itertools.combinations(range(n), 2))
    yield 'three_disjoint_K4s', graph(12, [(a+i, a+j) for a in [0, 4, 8]
                                           for i, j in itertools.combinations(range(4), 2)])
    yield 'star12', graph(12, [(0, v) for v in range(1, 12)])
    yield 'wheel12', graph(12, [(0, v) for v in range(1, 12)] +
                          [(v, v+1) for v in range(1, 11)] + [(11, 1)])
    yield 'bipyramid12', graph(12, [(v, (v+1)%10) for v in range(10)] +
                              [(u, v) for u in [10, 11] for v in range(10)])
    ico_edges = [(0, i+1) for i in range(5)] + [(11, i+6) for i in range(5)]
    for i in range(5):
        ico_edges.extend([(1+i, 1+(i+1)%5), (6+i, 6+(i+1)%5),
                          (1+i, 6+i), (1+i, 6+(i-1)%5)])
    yield 'icosahedron12', graph(12, ico_edges)
    yield 'K6_6_nonplanar_packing_control', complete_bipartite(6, 6)
    grid_edges = []
    for row in range(3):
        for col in range(5):
            u = 5*row+col
            if row+1 < 3:
                grid_edges.append((u, u+5))
            if col+1 < 5:
                grid_edges.append((u, u+1))
    yield 'grid3x5_diameter_case', graph(15, grid_edges)


def run():
    rows = []
    for name, adj in fixtures():
        result = two_path_witness(adj)
        assert result is not None, name
        paths, method = result
        verify_witness(adj, paths, 2)
        rows.append(dict(name=name, n=len(adj), method=method, paths=paths,
                         component_sizes=sorted([len(c) for c in components(
                             adj, {u for P in paths for u in P})], reverse=True)))
    packing_rows = []
    for k in range(1, 5):
        adj = complete_bipartite(3*k, 3*k)
        paths = packing_witness(adj, k)
        verify_witness(adj, paths, k)
        packing_rows.append(dict(k=k, n=len(adj), max_component=largest(adj, paths)))
    negative = complete_bipartite(6, 7)
    masks = all_geodesic_masks(negative)
    minimum = len(negative)
    pairs = 0
    for A, B in itertools.combinations_with_replacement(masks, 2):
        value = max((len(c) for c in components(negative, A | B)), default=0)
        assert 2*value > len(negative)
        minimum = min(minimum, value)
        pairs += 1
    cycle5 = graph(5, [(i, (i+1)%5) for i in range(5)])
    assert all(v in cycle5[u] for u, v in zip([0, 1, 2], [1, 2, 3]))
    assert 2 not in cycle5[0] and 3 not in cycle5[0] and 3 not in cycle5[1]
    assert bfs(cycle5, 0)[0][3] == 2 < 3
    return dict(status='PASS', constructive_fixtures=rows, packing_controls=packing_rows,
                negative_control_K6_7=dict(n=13, geodesic_masks=len(masks),
                                          pairs=pairs, minimum_largest_component=minimum),
                induced_P4_is_not_necessarily_ambient_geodesic=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    output = run()
    if args.check:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        assert output == expected
        print('PASS:', len(output['constructive_fixtures']), 'constructive fixtures;',
              len(output['packing_controls']), 'packing controls;',
              output['negative_control_K6_7']['pairs'], 'negative-control path pairs')
    else:
        print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
