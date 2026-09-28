#!/usr/bin/env python3
"""Exact finite checks of the proof mechanisms; standard library only.

Vertex labels are consecutive integers; original vertices come first. Paths
are unoriented (one orientation per endpoint pair), including singleton paths.
All shortest paths are generated, then equal vertex masks are deduplicated
because the separator test depends only on the vertex set. No completeness
claim extends beyond the explicit fixtures below.
"""

import itertools
import json
from collections import deque
from heapq import heappop, heappush


def adjacency(n, edges):
    adj = [0] * n
    for u, v in edges:
        assert 0 <= u < n and 0 <= v < n and u != v
        assert not adj[u] & (1 << v), "duplicate edge"
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def vertices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def components(adj, removed):
    remaining = ((1 << len(adj)) - 1) & ~removed
    answer = []
    while remaining:
        frontier = remaining & -remaining
        found = 0
        while frontier:
            found |= frontier
            remaining &= ~frontier
            neighbors = 0
            for v in vertices(frontier):
                neighbors |= adj[v]
            frontier = neighbors & remaining
        answer.append(found)
    return answer


def all_geodesics(adj):
    """BFS distances plus every predecessor choice, with no path-count cap."""
    answer = []
    for source in range(len(adj)):
        dist = [-1] * len(adj)
        dist[source] = 0
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in vertices(adj[u]):
                if dist[v] < 0:
                    dist[v] = dist[u] + 1
                    queue.append(v)

        def backwards(v):
            if v == source:
                yield (source,)
            else:
                for u in vertices(adj[v]):
                    if dist[u] == dist[v] - 1:
                        for prefix in backwards(u):
                            yield prefix + (v,)

        for target in range(source, len(adj)):
            if dist[target] >= 0:
                answer.extend(backwards(target))
    return answer


def path_mask(path):
    return sum(1 << v for v in path)


def path_masks(adj):
    return sorted({path_mask(path) for path in all_geodesics(adj)})


def weighted_distances(n, edges):
    adj = [[] for _ in range(n)]
    for u, v, length in edges:
        assert length > 0
        adj[u].append((v, length))
        adj[v].append((u, length))
    answer = []
    for source in range(n):
        dist = [None] * n
        dist[source] = 0
        queue = [(0, source)]
        while queue:
            value, u = heappop(queue)
            if dist[u] != value:
                continue
            for v, length in adj[u]:
                candidate = value + length
                if dist[v] is None or candidate < dist[v]:
                    dist[v] = candidate
                    heappush(queue, (candidate, v))
        answer.append(dist)
    return answer


def corridors(n, edges, copies):
    new_edges = []
    next_vertex = n
    for u, v, length in edges:
        assert isinstance(length, int) and length >= 2
        for _ in range(copies):
            interior = list(range(next_vertex, next_vertex + length - 1))
            next_vertex += length - 1
            path = [u] + interior + [v]
            new_edges.extend(zip(path, path[1:]))
    return adjacency(next_vertex, new_edges)


def leaf_expansion(adj, masses):
    assert len(adj) == len(masses)
    assert all(isinstance(b, int) and b >= 1 for b in masses)
    expanded = list(adj)
    for parent, mass in enumerate(masses):
        for _ in range(mass - 1):
            leaf = len(expanded)
            expanded.append(1 << parent)
            expanded[parent] |= 1 << leaf
    return expanded


def balanced(adj, masses, removed):
    total = sum(masses)
    return all(2 * sum(masses[v] for v in vertices(c)) <= total
               for c in components(adj, removed))


def has_separator(adj, masses, k):
    masks = path_masks(adj)
    # Repetition allows fewer than k nonempty paths: extra deletions never hurt.
    for family in itertools.combinations_with_replacement(masks, k):
        removed = 0
        for mask in family:
            removed |= mask
        if balanced(adj, masses, removed):
            return True
    return False


def preserves_core_components(core_adj, expanded_adj, removed):
    core_mask = (1 << len(core_adj)) - 1
    projected = removed & core_mask
    surviving = components(expanded_adj, removed)
    return all(any(c & ~d == 0 for d in surviving)
               for c in components(core_adj, projected))


def check_metric_fixture(name, n, edges, k=2):
    core_adj = adjacency(n, [(u, v) for u, v, _ in edges])
    expanded = corridors(n, edges, k + 1)
    distances = weighted_distances(n, edges)
    lengths = {frozenset((u, v)): length for u, v, length in edges}
    paths = all_geodesics(expanded)
    for path in paths:
        projected = [v for v in path if v < n]
        if projected:
            length = sum(lengths[frozenset((u, v))]
                         for u, v in zip(projected, projected[1:]))
            assert length == distances[projected[0]][projected[-1]]
    masks = sorted({path_mask(path) for path in paths})
    families = 0
    for family in itertools.combinations_with_replacement(masks, k):
        removed = 0
        for mask in family:
            removed |= mask
        assert preserves_core_components(core_adj, expanded, removed), (name, family)
        families += 1
    return dict(name=name, vertices=len(expanded), geodesics=len(paths),
                path_masks=len(masks), families=families)


def check_leaf_fixtures():
    fixtures = [
        ("single_total_one", 1, [], [1]),
        ("single_heavy", 1, [], [4]),
        ("disconnected", 3, [(0, 1)], [2, 1, 4]),
        ("weighted_path", 3, [(0, 1), (1, 2)], [3, 1, 2]),
        ("weighted_cycle", 5, [(i, (i + 1) % 5) for i in range(5)],
         [2, 3, 1, 1, 2]),
        ("K5_negative_control", 5, list(itertools.combinations(range(5), 2)), [1]*5),
    ]
    answer = []
    for name, n, edges, masses in fixtures:
        adj = adjacency(n, edges)
        expanded = leaf_expansion(adj, masses)
        values = []
        for k in (1, 2):
            original = has_separator(adj, masses, k)
            lifted = has_separator(expanded, [1] * len(expanded), k)
            assert original == lifted, (name, k)
            values.append(original)
        answer.append(dict(name=name, masses=masses, separator_k1_k2=values))
    return answer


def check_obstruction_lift():
    # K5 is deliberately NONPLANAR. It tests the graph-theoretic transfer and
    # is not a counterexample to any planar claim. One geodesic in unit K5
    # removes at most two vertices, leaving a connected set of at least three.
    n, k = 5, 1
    edges = [(u, v, 2) for u, v in itertools.combinations(range(n), 2)]
    core = adjacency(n, [(u, v) for u, v, _ in edges])
    assert not has_separator(core, [1] * n, k)
    intermediate = corridors(n, edges, k + 1)
    B = len(intermediate)
    M = B + 1
    masses = [M + 1] * n + [1] * (B - n)
    expanded = leaf_expansion(intermediate, masses)
    assert len(expanded) == B + M * n
    masks = path_masks(expanded)
    best = len(expanded)
    for removed in masks:
        largest = max((c.bit_count() for c in components(expanded, removed)), default=0)
        assert 2 * largest > len(expanded)
        best = min(best, largest)
    return dict(core="K5 (nonplanar)", k=k, B=B, M=M, N=len(expanded),
                path_masks=len(masks), minimum_largest_remaining_component=best)


def main():
    # A single subdivided edge fails the component-preservation assertion.
    bare = corridors(2, [(0, 1, 2)], 1)
    core = adjacency(2, [(0, 1)])
    assert not preserves_core_components(core, bare, 1 << 2)
    result = {
        "metric_projection_and_component_checks": [
            check_metric_fixture("unequal_path", 3, [(0, 1, 2), (1, 2, 3)]),
            check_metric_fixture("triangle", 3, [(0, 1, 2), (1, 2, 2), (0, 2, 2)]),
            check_metric_fixture("nongeodesic_edge", 3,
                                 [(0, 1, 2), (1, 2, 2), (0, 2, 5)]),
            check_metric_fixture("K4", 4,
                                 [(u, v, 2) for u, v in itertools.combinations(range(4), 2)]),
        ],
        "leaf_equivalence_checks": check_leaf_fixtures(),
        "integer_obstruction_lift": check_obstruction_lift(),
        "bare_subdivision_negative_control_rejected": True,
        "status": "PASS",
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
