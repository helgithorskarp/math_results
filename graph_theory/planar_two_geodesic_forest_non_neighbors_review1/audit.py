#!/usr/bin/env python3
"""Independent plane-tree port fixtures and decomposition audit."""

from collections import deque
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from random import Random
import json


SOURCE = Path(__file__).resolve().parent.parent / 'planar_two_geodesic_forest_non_neighbors/verify.py'
spec = spec_from_file_location('forest_claim_verifier', SOURCE)
claim = module_from_spec(spec)
spec.loader.exec_module(claim)


def edge(a, b):
    return tuple(sorted((a, b)))


def graph(n, edges):
    result = [set() for _ in range(n)]
    for a, b in edges:
        result[a].add(b)
        result[b].add(a)
    return result


def boundary_word(tree, rng):
    if len(tree) == 1:
        return [1]
    rotation = {v: rng.sample(sorted(neighbors), len(neighbors))
                for v, neighbors in tree.items()}
    start = (1, rotation[1][0])
    dart = start
    word = []
    while True:
        u, v = dart
        word.append(u)
        around = rotation[v]
        dart = (v, around[(around.index(u) + 1) % len(around)])
        if dart == start:
            break
        assert len(word) < 2 * len(tree)
    assert len(word) == 2 * (len(tree) - 1)
    return word


def fixture(rng, index):
    k = 1 if index % 19 == 0 else rng.randrange(2, 20)
    tree = {v: set() for v in range(1, k + 1)}
    tree_edges = set()
    for v in range(2, k + 1):
        parent = rng.randrange(1, v)
        tree[parent].add(v)
        tree[v].add(parent)
        tree_edges.add(edge(parent, v))
    corners = boundary_word(tree, rng)
    sources = [v for v in corners for _ in range(rng.randrange(4))]
    if not sources:
        sources = [rng.choice(corners)]
    rotate = rng.randrange(len(sources))
    sources = sources[rotate:] + sources[:rotate]
    ports = len(sources)
    m = rng.randrange(1, min(ports, 12) + 1)
    breaks = sorted(rng.sample(range(1, ports), m - 1))
    labels = []
    for j in range(ports):
        labels.append(sum(cut <= j for cut in breaks))
    n = 1 + k + m
    boundary = list(range(k + 1, n))
    pairs = [(x, k + 1 + label) for x, label in zip(sources, labels)]
    cycle = {edge(a, b) for a, b in zip(boundary, boundary[1:] + boundary[:1]) if a != b}
    kept = {e for e in cycle if rng.randrange(2)}
    actual = tree_edges | {edge(0, y) for y in boundary} | {edge(x, y) for x, y in pairs} | kept
    fill = actual | cycle | {edge(0, x) for x in tree}
    return {'n': n, 'k': k, 'actual': actual, 'fill': fill,
            'ports': pairs, 'boundary': boundary,
            'tree_edges': tree_edges}


def shortest_distance(adj, a, b):
    distance = {a: 0}
    queue = deque([a])
    while queue:
        v = queue.popleft()
        if v == b:
            return distance[v]
        for w in adj[v]:
            if w not in distance:
                distance[w] = distance[v] + 1
                queue.append(w)
    raise AssertionError('disconnected')


def components(adj, removed):
    unseen = set(range(len(adj))) - removed
    result = []
    while unseen:
        root = unseen.pop()
        part = {root}
        stack = [root]
        while stack:
            v = stack.pop()
            for w in adj[v] & unseen:
                unseen.remove(w)
                part.add(w)
                stack.append(w)
        result.append(part)
    return result


def check_patch(patch, rows, counters):
    n = patch['n']
    assert len(rows) == n and {row['v'] for row in rows} == set(range(n))
    actual = graph(n, patch['actual'])
    bag = [set(row['bag']) for row in rows]
    order = {row['v']: i for i, row in enumerate(rows)}
    td = [set() for _ in range(n)]
    for i, row in enumerate(rows):
        assert len(bag[i]) <= 5
        assert 1 <= len(row['paths']) <= 2
        union = set()
        for path in row['paths']:
            assert path and len(path) == len(set(path))
            assert all(b in actual[a] for a, b in zip(path, path[1:]))
            assert shortest_distance(actual, path[0], path[-1]) == len(path) - 1
            union.update(path)
            counters['geodesics'] += 1
        assert bag[i] <= union
        counters['bags'] += 1
        counters['five_bags'] += (len(bag[i]) == 5)
        later = bag[i] - {row['v']}
        if later:
            parent = min(later, key=order.get)
            j = order[parent]
            assert i < j and later <= bag[j]
            td[i].add(j)
            td[j].add(i)
    assert sum(map(len, td)) == 2 * (n - 1)
    for v in range(n):
        indices = {i for i, current in enumerate(bag) if v in current}
        found = {min(indices)}
        stack = list(found)
        while stack:
            i = stack.pop()
            for j in td[i] & indices - found:
                found.add(j)
                stack.append(j)
        assert found == indices
    for a, b in patch['actual']:
        assert any({a, b} <= current for current in bag)
    boundary = patch['boundary']
    for a, b in zip(boundary, boundary[1:] + boundary[:1]):
        assert any({0, a, b} <= current for current in bag)
    weights = [
        [1] * n,
        [(17 * v * v + 11 * v + 5) % 23 for v in range(n)],
        [int(v == n - 1) * 1000 for v in range(n)],
    ]
    assigned = [next(i for i, current in enumerate(bag) if v in current) for v in range(n)]
    for mass in weights:
        total = sum(mass)
        tree_mass = [0] * n
        for v, w in enumerate(mass):
            tree_mass[assigned[v]] += w
        centroid = None
        for i in range(n):
            sides = []
            for neighbor in td[i]:
                reached = {i, neighbor}
                stack = [neighbor]
                side_mass = 0
                while stack:
                    j = stack.pop()
                    side_mass += tree_mass[j]
                    for other in td[j] - reached:
                        reached.add(other)
                        stack.append(other)
                sides.append(side_mass)
            if all(2 * x <= total for x in sides):
                centroid = i
                break
        assert centroid is not None
        removed = set().union(*(set(p) for p in rows[centroid]['paths']))
        assert all(2 * sum(mass[v] for v in part) <= total
                   for part in components(actual, removed))
        counters['mass_checks'] += 1


def strict_example(counters):
    k, m = 3, 12
    n = 1 + k + m
    boundary = list(range(k + 1, n))
    tree_edges = {edge(1, 2), edge(2, 3)}
    sources = [x for x in (1, 2, 3, 2) for _ in range(3)]
    ports = [(x, y) for x, y in zip(sources, boundary)]
    cycle = {edge(a, b) for a, b in zip(boundary, boundary[1:] + boundary[:1])}
    actual = tree_edges | cycle | {edge(0, y) for y in boundary} | {edge(x, y) for x, y in ports}
    fill = actual | {edge(0, x) for x in range(1, k + 1)}
    patch = {'n': n, 'k': k, 'actual': actual, 'fill': fill,
             'ports': ports, 'boundary': boundary, 'tree_edges': tree_edges}
    adj = graph(n, actual)
    assert min(map(len, adj)) == 4
    assert components(adj, {0} | adj[0]) == [{1, 2, 3}]
    for root in range(n):
        outside = components(adj, {root} | adj[root])
        assert any(any(len(adj[v] & part) < len(part) - 1 for v in part)
                   for part in outside)
    assert all({a, b} | adj[a] | adj[b] != set(range(n)) for a, b in actual)
    local_counts = {'fan_nonedge': 0, 'fan_triangle': 0,
                    'leaf_nonedge': 0, 'leaf_adjacent': 0}
    rows = claim.construct(patch, local_counts)
    check_patch(patch, rows, counters)
    return {'order': n, 'minimum_degree': 4, 'maximum_bag_size': max(len(x['bag']) for x in rows),
            'clique_nonneighbor_roots': 0, 'dominating_edges': 0}


def main():
    assert __debug__, 'run without -O'
    rng = Random(2026092817)
    count = {'cases': 0, 'bags': 0, 'five_bags': 0,
             'geodesics': 0, 'mass_checks': 0,
             'fan_nonedge': 0, 'fan_triangle': 0,
             'leaf_nonedge': 0, 'leaf_adjacent': 0}
    failures = []
    for index in range(1200):
        patch = fixture(rng, index)
        author_counts = {'fan_nonedge': 0, 'fan_triangle': 0,
                         'leaf_nonedge': 0, 'leaf_adjacent': 0}
        try:
            rows = claim.construct(patch, author_counts)
            check_patch(patch, rows, count)
        except Exception as exc:
            failures.append({'index': index, 'error': str(exc)})
            break
        for key, value in author_counts.items():
            count[key] += value
        count['cases'] += 1
    strict = strict_example(count)
    print(json.dumps({'counts': count, 'strict_example': strict,
                      'failures': failures}, indent=2, sort_keys=True))
    assert not failures


if __name__ == '__main__':
    main()
