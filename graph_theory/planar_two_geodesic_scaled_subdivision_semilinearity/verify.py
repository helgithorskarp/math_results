"""Finite checks for the refined-edge encoding used in README.md.

This checks small scaled skeletons against explicit unit subdivisions.  The
ultimately-periodic theorem itself follows from the written construction and
the Presburger semilinearity theorem, not from these bounded checks.
"""

from collections import deque
from itertools import product
from random import Random


def vertex(edges, edge_id, coordinate, scale):
    u, v, length = edges[edge_id]
    if coordinate == 0:
        return u
    if coordinate == scale * length:
        return v
    return (edge_id, coordinate)


def unit_graph(n, edges, scale):
    adj = {u: set() for u in range(n)}
    for j, (_, _, length) in enumerate(edges):
        for x in range(scale * length):
            a = vertex(edges, j, x, scale)
            b = vertex(edges, j, x + 1, scale)
            adj.setdefault(a, set()).add(b)
            adj.setdefault(b, set()).add(a)
    return adj


def refined_graph(n, edges, scale, terminals):
    """Insert up to four terminal vertices and retain their edge segments."""
    adj = {u: {} for u in range(n)}
    segments = {}
    for j, (_, _, length) in enumerate(edges):
        coordinates = {0, scale * length}
        coordinates.update(x for t in terminals
                           if isinstance(t, tuple) and t[0] == j
                           for x in [t[1]])
        coordinates = sorted(coordinates)
        for x, y in zip(coordinates, coordinates[1:]):
            a = vertex(edges, j, x, scale)
            b = vertex(edges, j, y, scale)
            assert y > x
            adj.setdefault(a, {})[b] = y - x
            adj.setdefault(b, {})[a] = y - x
            segments[frozenset((a, b))] = (j, x, y)
    return adj, segments


def simple_paths(adj, source, target):
    stack = [(source, (source,))]
    while stack:
        u, path = stack.pop()
        if u == target:
            yield path
            continue
        for v in adj[u]:
            if v not in path:
                stack.append((v, path + (v,)))


def distances(adj, source):
    queue = deque([source])
    d = {source: 0}
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if v not in d:
                d[v] = d[u] + 1
                queue.append(v)
    return d


def shortest_path_sets(adj, source, target):
    ds = distances(adj, source)
    dt = distances(adj, target)
    stack = [(source, (source,))]
    result = set()
    while stack:
        u, path = stack.pop()
        if u == target:
            result.add(frozenset(path))
            continue
        for v in adj[u]:
            if ds.get(v) == ds[u] + 1 and ds[v] + dt[v] == ds[target]:
                stack.append((v, path + (v,)))
    return result


def path_length(path, refined):
    return sum(refined[a][b] for a, b in zip(path, path[1:]))


def expanded_path(path, segments, edges, scale):
    result = set(path)
    for a, b in zip(path, path[1:]):
        j, x, y = segments[frozenset((a, b))]
        result.update(vertex(edges, j, z, scale) for z in range(x, y + 1))
    return result


def component_sizes(adj, deleted):
    unseen = set(adj) - deleted
    sizes = []
    while unseen:
        start = unseen.pop()
        queue = [start]
        for u in queue:
            for v in adj[u] & unseen:
                unseen.remove(v)
                queue.append(v)
        sizes.append(len(queue))
    return sorted(sizes)


def auxiliary_sizes(refined, segments, paths):
    """One affine-weight block for every untraversed refined-edge interior."""
    removed = set().union(*(set(p) for p in paths))
    traversed = {frozenset((a, b)) for p in paths
                 for a, b in zip(p, p[1:])}
    adj = {u: set() for u in refined if u not in removed}
    mass = {u: 1 for u in adj}
    for edge, (j, x, y) in segments.items():
        if edge in traversed:
            continue
        block = ("block", j, x, y)
        adj[block] = set()
        mass[block] = y - x - 1
        for u in edge:
            if u in adj:
                adj[u].add(block)
                adj[block].add(u)
    unseen = set(adj)
    sizes = []
    while unseen:
        start = unseen.pop()
        queue = [start]
        for u in queue:
            for v in adj[u] & unseen:
                unseen.remove(v)
                queue.append(v)
        weight = sum(mass[u] for u in queue)
        if weight:
            sizes.append(weight)
    return sorted(sizes)


def audit(n, edges, scale, samples, rng):
    full = unit_graph(n, edges, scale)
    vertices = list(full)
    if len(vertices) ** 4 <= samples:
        choices = product(vertices, repeat=4)
    else:
        choices = (tuple(rng.choice(vertices) for _ in range(4))
                   for _ in range(samples))
    configurations = pairs = 0
    for terminals in choices:
        refined, segments = refined_graph(n, edges, scale, terminals)
        options = []
        for a, b in ((terminals[0], terminals[1]),
                     (terminals[2], terminals[3])):
            d = distances(full, a)[b]
            candidates = list(simple_paths(refined, a, b))
            assert min(path_length(p, refined) for p in candidates) == d
            geodesics = [p for p in candidates if path_length(p, refined) == d]
            # Every refined candidate is a simple path in the unit graph.
            assert all(len(expanded_path(p, segments, edges, scale)) ==
                       path_length(p, refined) + 1 for p in candidates)
            assert {frozenset(expanded_path(p, segments, edges, scale))
                    for p in geodesics} == shortest_path_sets(full, a, b)
            options.append(geodesics)
        for p, q in product(*options):
            deleted = expanded_path(p, segments, edges, scale)
            deleted |= expanded_path(q, segments, edges, scale)
            assert component_sizes(full, deleted) == \
                   auxiliary_sizes(refined, segments, (p, q))
            pairs += 1
        configurations += 1
    return configurations, pairs


def main():
    examples = [
        (4, [(0, 1, 1), (1, 2, 2), (2, 3, 1),
             (3, 0, 2), (0, 2, 2)]),
        (4, [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1)]),
    ]
    rng = Random(3192026)
    configurations = pairs = 0
    for n, edges in examples:
        for scale in (1, 2, 3):
            c, p = audit(n, edges, scale, 96, rng)
            configurations += c
            pairs += p
    print(f"skeletons=2 scales=1,2,3 configurations={configurations} "
          f"geodesic_pairs={pairs} PASS")


if __name__ == "__main__":
    main()
