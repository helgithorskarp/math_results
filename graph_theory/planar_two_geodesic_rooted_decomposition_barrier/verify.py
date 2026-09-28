#!/usr/bin/env python3
"""Exact, standard-library checks for a rooted decomposition obstruction."""
import argparse
from collections import deque
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import random


HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        require(0 <= u < n and 0 <= v < n and u != v, "invalid edge")
        adj[u].add(v)
        adj[v].add(u)
    return adj


def annulus(k):
    b = lambda i: 1 + i % k
    c = lambda i: 1 + k + i % k
    edges, faces = [], []
    for i in range(k):
        edges.extend(((0, b(i)), (b(i), b(i+1)), (c(i), c(i+1)),
                      (b(i), c(i)), (b(i), c(i+1))))
        faces.extend(((0, b(i), b(i+1)), (b(i), c(i+1), b(i+1)),
                      (b(i), c(i), c(i+1))))
    faces.append(tuple(c(i) for i in reversed(range(k))))
    return graph(2*k+1, edges), faces


def distances(adj):
    result = []
    for start in range(len(adj)):
        row = [-1] * len(adj)
        row[start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if row[v] == -1:
                    row[v] = row[u] + 1
                    queue.append(v)
        require(min(row) >= 0, "disconnected graph")
        result.append(row)
    return result


def check_sphere(adj, faces):
    """Check a connected orientable cellular embedding with Euler value 2."""
    darts = set()
    turns = [dict() for _ in adj]
    for face in faces:
        require(len(set(face)) == len(face) >= 3, "invalid face")
        for i, u in enumerate(face):
            v, prev = face[(i+1) % len(face)], face[i-1]
            require(v in adj[u] and (u, v) not in darts, "invalid face dart")
            darts.add((u, v))
            require(prev not in turns[u], "repeated vertex turn")
            turns[u][prev] = v
    require(darts == {(u, v) for u in range(len(adj)) for v in adj[u]},
            "face darts do not cover the edges")
    for u, turn in enumerate(turns):
        require(set(turn) == adj[u] == set(turn.values()), "incomplete rotation")
        start = min(turn)
        seen, v = set(), start
        while v not in seen:
            seen.add(v)
            v = turn[v]
        require(v == start and seen == adj[u], "split vertex link")
    require(len(adj) - len(darts)//2 + len(faces) == 2, "not a sphere")
    distances(adj)  # also require connectedness


def all_geodesics(adj, dist):
    """Enumerate shortest paths directly by strictly increasing BFS levels."""
    paths = []
    for start in range(len(adj)):
        def extend(path):
            u = path[-1]
            if start <= u:
                paths.append(tuple(path))
            for v in sorted(adj[u]):
                if dist[start][v] == dist[start][u] + 1:
                    extend(path + [v])
        extend([start])
    return paths


def two_cover(vertices, paths):
    """Return actual witnesses, allowing all vertices outside the target set."""
    vertices = set(vertices)
    traces = {}
    for path in paths:
        trace = frozenset(vertices.intersection(path))
        traces.setdefault(trace, path)
    for first, p in traces.items():
        for second, q in traces.items():
            if vertices <= first | second:
                return p, q
    return None


def check_path(adj, dist, path):
    require(path and len(set(path)) == len(path), "path not simple")
    require(all(v in adj[u] for u, v in zip(path, path[1:])), "nonedge in path")
    require(len(path)-1 == dist[path[0]][path[-1]], "path not shortest")


def check_type(adj, dist, ordered, expected):
    require(len(set(ordered)) == 6, "neighborhood size")
    for i, j in combinations(range(6), 2):
        edge = j in expected[i]
        require((ordered[j] in adj[ordered[i]]) == edge, "wrong induced type")
        require(dist[ordered[i]][ordered[j]] == (1 if edge else 2),
                "wrong ambient distance")


def check_td(adj, bags, links):
    require(len(links) == len(bags)-1, "wrong decomposition edge count")
    tree = graph(len(bags), links)
    distances(tree)
    for v in range(len(adj)):
        owners = {i for i, bag in enumerate(bags) if v in bag}
        require(owners, "uncovered vertex")
        reached, stack = set(), [min(owners)]
        while stack:
            u = stack.pop()
            if u not in reached:
                reached.add(u)
                stack.extend((tree[u] & owners) - reached)
        require(reached == owners, "disconnected vertex occurrences")
    for u in range(len(adj)):
        for v in adj[u]:
            require(any({u, v} <= bag for bag in bags), "uncovered edge")


def elimination_td(adj, order):
    require(sorted(order) == list(range(len(adj))), "invalid order")
    filled = [set(row) for row in adj]
    alive = set(order)
    index = {v: i for i, v in enumerate(order)}
    bags, links = [], []
    for i, v in enumerate(order):
        later = filled[v] & (alive - {v})
        bags.append(later | {v})
        if later:
            links.append((i, min(index[u] for u in later)))
        for u, w in combinations(later, 2):
            filled[u].add(w)
            filled[w].add(u)
        alive.remove(v)
    return bags, links


def median_paths(k, mass):
    columns = [mass[1+i] + mass[1+k+i] for i in range(k)]
    total = sum(columns)
    chosen = [0]
    if 2*columns[0] < total:
        prefix = columns[0]
        for j in range(1, k):
            prefix += columns[j]
            if 2*prefix >= total:
                chosen.append(j)
                break
    return [(0, 1+i, 1+k+i) for i in chosen]


def check_separator(adj, dist, paths, mass):
    require(len(paths) <= 2, "too many paths")
    for path in paths:
        check_path(adj, dist, path)
        require(path[0] == 0, "path not rooted")
    remaining = set(range(len(adj))) - set().union(*map(set, paths))
    total = sum(mass)
    while remaining:
        component, stack = set(), [min(remaining)]
        while stack:
            u = stack.pop()
            if u in remaining:
                remaining.remove(u)
                component.add(u)
                stack.extend(adj[u] & remaining)
        require(2*sum(mass[v] for v in component) <= total, "unbalanced")


def run():
    wheel = graph(6, [(0, i) for i in range(1, 6)] +
                  [(i, 1+i % 5) for i in range(1, 6)])
    sun = graph(6, [(0, 1), (1, 2), (2, 0), (3, 0), (3, 1),
                    (4, 0), (4, 2), (5, 1), (5, 2)])
    result = dict(local_obstructions=0, sphere_embeddings=0,
                  blocked_neighborhoods=0, ambient_pair_obstructions=0,
                  unrestricted_decompositions=0, verified_bags=0,
                  verified_bag_paths=0, mass_checks=0, rejected_controls=0)
    for obstruction in (wheel, sun):
        paths = all_geodesics(obstruction, distances(obstruction))
        require(two_cover(range(6), paths) is None, "local obstruction failed")
        for omitted in range(6):
            require(two_cover(set(range(6)) - {omitted}, paths) is not None,
                    "unexpected five-vertex obstruction")
        result['local_obstructions'] += 1
    orders = json.loads((HERE / 'orders.json').read_text())
    rng = random.Random(20260928)
    for k in range(4, 41):
        adj, faces = annulus(k)
        n = len(adj)
        dist = distances(adj)
        check_sphere(adj, faces)
        result['sphere_embeddings'] += 1
        b = lambda i: 1 + i % k
        c = lambda i: 1 + k + i % k
        paths = all_geodesics(adj, dist) if str(k) in orders else None
        for i in range(k):
            outer = [b(i), 0, b(i-1), c(i), c(i+1), b(i+1)]
            inner = [c(i), b(i-1), b(i), c(i-1), c(i+1), 0]
            require(set(outer) == adj[b(i)] | {b(i), 0}, "outer neighborhood")
            require(set(inner) == adj[c(i)] | {c(i), 0}, "inner neighborhood")
            for vertices, target in ((outer, wheel), (inner, sun)):
                check_type(adj, dist, vertices, target)
                result['blocked_neighborhoods'] += 1
                if paths is not None:
                    require(two_cover(vertices, paths) is None, "ambient cover")
                    result['ambient_pair_obstructions'] += 1
        if paths is not None:
            bags, links = elimination_td(adj, orders[str(k)])
            check_td(adj, bags, links)
            require(any(0 not in bag for bag in bags), "root retained everywhere")
            for bag in bags:
                cover = two_cover(bag, paths)
                require(cover is not None, "uncovered unrestricted bag")
                for path in cover:
                    check_path(adj, dist, path)
                require(bag <= set().union(*map(set, cover)), "invalid cover")
                result['verified_bags'] += 1
                result['verified_bag_paths'] += len(cover)
            result['unrestricted_decompositions'] += 1
        masses = [[0]*n, [1]*n]
        masses.extend([[int(i == j) for i in range(n)] for j in range(n)])
        for _ in range(20):
            masses.append([Fraction(rng.randrange(100), rng.randrange(1, 10))
                           for _ in range(n)])
        if k in (4, 5):
            masses.extend(product((0, 1), repeat=n))
        for mass in masses:
            check_separator(adj, dist, median_paths(k, mass), mass)
            result['mass_checks'] += 1
    adj, _ = annulus(4)
    dist = distances(adj)
    for invalid in ((0, 5), (0, 1, 5, 6)):
        try:
            check_path(adj, dist, invalid)
        except AssertionError:
            result['rejected_controls'] += 1
        else:
            raise AssertionError("invalid path accepted")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='compare expected.json')
    args = parser.parse_args()
    result = run()
    if args.check:
        require(result == json.loads((HERE / 'expected.json').read_text()),
                'expected output mismatch')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
