#!/usr/bin/env python3
"""Exact path-template transversal certificate for the 20-vertex example.

Run from anywhere with Python 3.11 or later. The graph and its checked
rotation system are in the adjacent planar_two_geodesic_template_radius20
source directory. This program uses only the standard library.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] /
                       'planar_two_geodesic_template_radius20'))
import verify as base


def all_geodesics(rows, dist, edge_id):
    """Enumerate actual paths, retaining both their vertex and edge masks."""
    paths = {}

    def extend(start, target, path):
        u = path[-1]
        if u == target:
            vertices = base.vertex_mask(path)
            edges = sum(1 << edge_id[tuple(sorted((a, b)))]
                        for a, b in zip(path, path[1:]))
            paths[(vertices, edges)] = path
            return
        for v in base.vertices(rows[u]):
            if (dist[start][v] == dist[start][u] + 1 and
                    dist[v][target] >= 0 and
                    dist[start][v] + dist[v][target] ==
                    dist[start][target]):
                extend(start, target, path + (v,))

    for start in range(base.N):
        for target in range(start, base.N):
            if dist[start][target] >= 0:
                extend(start, target, (start,))
    return paths


def protected_sets(rows, paths):
    """Every primary pair whose residual components have at most 8 vertices."""
    entries = list(paths.items())
    templates = set()
    qualifying_pairs = 0
    minimum_maximum = base.N
    for i, ((a, x), _) in enumerate(entries):
        for (b, y), _ in entries[i:]:
            residual = base.components(rows, base.FULL & ~(a | b))
            maximum = max((c.bit_count() for c in residual), default=0)
            minimum_maximum = min(minimum_maximum, maximum)
            if maximum <= 8:
                qualifying_pairs += 1
                templates.add(x | y)
    return templates, qualifying_pairs, minimum_maximum


def find_transversal(templates, limit):
    """Exact bounded hitting-set search; return (witness or None, states).

    At any state, a set T disjoint from the chosen deletions must be hit.
    Branching on each edge of T is exhaustive. Memoization merges orders
    of choosing the same deletion set. The first unhit template has the
    fewest edges, then smallest numerical mask, for deterministic counts.
    """
    ordered = sorted(templates, key=lambda x: (x.bit_count(), x))
    seen = set()

    def search(deleted):
        if deleted in seen:
            return None
        seen.add(deleted)
        unhit = next((t for t in ordered if not t & deleted), None)
        if unhit is None:
            return deleted
        if deleted.bit_count() == limit:
            return None
        for edge in base.vertices(unhit):
            answer = search(deleted | (1 << edge))
            if answer is not None:
                return answer
        return None

    return search(0), len(seen)


def main():
    rows = base.decode_graph6(base.GRAPH6)
    base.check_embedding(rows)
    edges = base.edge_list(rows)
    assert len(edges) == 54
    edge_id = {edge: i for i, edge in enumerate(edges)}
    dist = base.distances(rows)
    paths = all_geodesics(rows, dist, edge_id)
    assert len(paths) == 425
    assert len({v for v, _ in paths}) == 425
    templates, pair_count, minimum_maximum = protected_sets(rows, paths)
    assert pair_count == 1759 and len(templates) == 1759
    assert minimum_maximum == 6
    assert min(t.bit_count() for t in templates) == 5
    assert sum(t.bit_count() == 5 for t in templates) == 253

    example = ((0, 1, 6), (3, 10, 19, 15))
    union, protected = base.check_paths(
        example, rows, dist, edge_id)
    assert protected in templates and protected.bit_count() == 5
    assert sorted(c.bit_count() for c in base.components(
        rows, base.FULL & ~union)) == [6, 7]

    witness, states = find_transversal(templates, 11)
    assert witness is None and states == 3632861
    print('vertices=20 edges=54 geodesics=425')
    print('eight-residual pairs=1759 protected sets=1759'
          ' minimum protected edges=5')
    print('hitting-set limit=11 states=3632861 witness=none')
    print('PASS: all edge deletions of size at most 11 retain a template')


if __name__ == '__main__':
    main()
