#!/usr/bin/env python3
"""Exact unit-edge controls for the all-order common-window path theorem."""

from collections import deque
from fractions import Fraction as F
from itertools import combinations


def host(n, ears):
    """Return path edges, internally disjoint ear edge lists, and adjacency."""
    assert n >= 2
    path = [(i, i + 1) for i in range(n - 1)]
    pieces = []
    next_vertex = n
    for a, b, length in ears:
        assert 0 <= a < b < n and length >= 2
        chain = [a] + list(range(next_vertex, next_vertex + length - 1)) + [b]
        next_vertex += length - 1
        pieces.append(list(zip(chain, chain[1:])))
    adj = adjacency(next_vertex, path + sum(pieces, []))
    return path, pieces, adj


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert u != v
        adj[u].add(v)
        adj[v].add(u)
    return adj


def distances(adj, source):
    dist = [-1] * len(adj)
    dist[source] = 0
    queue = deque([source])
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                queue.append(v)
    return dist


def focus(n, ports, adj):
    active = {}
    for a, b in combinations(sorted(ports), 2):
        dist = distances(adj, a)[b]
        assert 0 <= dist <= b - a
        if dist < b - a:
            active[(a, b)] = (F(a + b - dist, 2),
                              F(a + b + dist, 2), dist)
    if not active:
        return active, F(0), F(n - 1)
    lower = max(w[0] for w in active.values())
    upper = min(w[1] for w in active.values())
    return active, lower, upper


def path_components(n, mask):
    start = 0
    for edge in range(n - 1):
        if not mask & (1 << edge):
            yield list(range(start, edge + 1))
            start = edge + 1
    yield list(range(start, n))


def check_state(n, path, ears, active, focus_point, path_mask, ear_mask):
    edges = [path[i] for i in range(n - 1) if path_mask & (1 << i)]
    for j, piece in enumerate(ears):
        if ear_mask & (1 << j):
            edges.extend(piece)
    adj = adjacency(max(max(u, v) for u, v in path + sum(ears, [])) + 1,
                    edges)
    for comp in path_components(n, path_mask):
        left, right = comp[0], comp[-1]
        relevant = [(a, b) for a, b in active if left <= a < b <= right]
        if not relevant:
            assert distances(adj, left)[right] == right - left
            continue
        assert left < right
        cuts = [k for k in range(left, right)
                if F(k) <= focus_point <= F(k + 1)]
        assert cuts, (n, comp, focus_point)
        k = cuts[0]
        assert distances(adj, left)[k] == k - left
        assert distances(adj, right)[k + 1] == right - k - 1


def exhaustive_example(n, ear_specs, expected_active):
    path, ears, adj = host(n, ear_specs)
    ports = {v for a, b, _ in ear_specs for v in (a, b)}
    active, low, high = focus(n, ports, adj)
    assert active == expected_active
    assert low <= high
    point = (low + high) / 2
    states = 0
    for pm in range(1 << (n - 1)):
        for em in range(1 << len(ears)):
            check_state(n, path, ears, active, point, pm, em)
            states += 1
    print(f'n={n} ports={len(ports)} active_pairs={len(active)} '
          f'window=[{low},{high}] states={states} PASS')


def main():
    nested = {(0, 4): (F(1, 2), F(7, 2), 3),
              (0, 8): (F(3, 2), F(13, 2), 5)}
    exhaustive_example(10, [(0, 4, 3), (0, 8, 5)], nested)

    for n in (8, 16, 32):
        ears = [(0, j, j - 1) for j in range(3, n)]
        _, _, adj = host(n, ears)
        ports = {0} | set(range(3, n))
        active, low, high = focus(n, ports, adj)
        assert set(active) == {(0, j) for j in range(3, n)}
        assert all(active[(0, j)] == (F(1, 2), F(2*j-1, 2), j-1)
                   for j in range(3, n))
        assert (low, high) == (F(1, 2), F(5, 2))
        print(f'fan_n={n} ports={len(ports)} active_pairs={len(active)} '
              f'window=[{low},{high}] PASS')
    n = 8
    ear_specs = [(0, j, j - 1) for j in range(3, n)]
    expected = {(0, j): (F(1, 2), F(2*j-1, 2), j-1)
                for j in range(3, n)}
    exhaustive_example(n, ear_specs, expected)
    print('PASS')


if __name__ == '__main__':
    main()
