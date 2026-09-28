"""Independent radius-five audit using the published radius-four review checker.

Run from repository root with Python 3.11+ and PYTHONDONTWRITEBYTECODE=1.
No target verifier is imported. The 2665 exceptional children are checked
with a separate BFS-level path enumerator and full residual searches.
"""

import importlib.util
import json
from itertools import combinations
from pathlib import Path


ROOT = Path('graph_theory/planar_two_geodesic_template_radius20')
BASE_AUDIT = Path('graph_theory/planar_two_geodesic_template_radius20_review1/audit.py')
spec = importlib.util.spec_from_file_location('independent_radius4_audit', BASE_AUDIT)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)


def mask(items):
    return sum(1 << v for v in items)


def delete(adj, deleted):
    return tuple(frozenset(v for v in row if base.edge(u, v) not in deleted)
                 for u, row in enumerate(adj))


def geodesics(adj, dist):
    # All shortest paths from a start follow strictly increasing BFS levels.
    # Keep a representative for each vertex mask, including singletons.
    paths = {}
    for start in range(len(adj)):
        stack = [(start, (start,), 1 << start)]
        while stack:
            u, path, used = stack.pop()
            if u >= start:
                paths.setdefault(used, path)
            for v in adj[u]:
                if dist[start].get(v) == dist[start][u] + 1:
                    stack.append((v, path + (v,), used | (1 << v)))
    return paths


def small_residual_witness(adj):
    dist = base.distances(adj)
    paths = geodesics(adj, dist)
    ordered = sorted(paths, key=lambda value: (-value.bit_count(), value))
    seen = set()
    for i, first in enumerate(ordered):
        for second in ordered[i:]:
            union = first | second
            if union in seen:
                continue
            seen.add(union)
            parts = base.components(adj, (v for v in range(len(adj))
                                          if union >> v & 1))
            if any(len(part) > 5 for part in parts):
                continue
            if any(len(part) == 5 and
                   all(v in adj[u] for u, v in combinations(part, 2))
                   for part in parts):
                continue
            entry = {'primary': [paths[first], paths[second]], 'secondary': []}
            base.validate_template(entry, adj, dist)
            return True, len(paths), len(seen)
    return False, len(paths), len(seen)


def main():
    source = json.loads((ROOT / 'certificates.json').read_text())
    adj = base.decode_graph6(source['graph6'])
    base.check_rotation(adj)
    edges = sorted(base.edge(u, v) for u, row in enumerate(adj)
                   for v in row if u < v)
    assert len(edges) == 54
    edge_number = {e: i for i, e in enumerate(edges)}
    dist = base.distances(adj)
    root_sets = [base.validate_template(t, adj, dist)[0]
                 for t in source['templates']]
    root_masks = [mask(edge_number[e] for e in set_) for set_ in root_sets]
    star = frozenset(base.edge(12, v) for v in adj[12])
    star_mask = mask(edge_number[e] for e in star)
    fallback = json.loads((ROOT / 'radius5_star.json').read_text())
    assert star == frozenset(map(tuple, fallback['deleted_edges']))
    star_child = delete(adj, star)
    fallback_edges, fallback_residuals = base.validate_template(
        fallback, star_child, base.distances(star_child))
    assert fallback_residuals == [1, 5, 6]
    assert len(fallback_edges) == 12 and not fallback_edges & star
    fallback_mask = mask(edge_number[e] for e in fallback_edges)

    root_covered = 0
    frontier = []
    for ids in combinations(range(len(edges)), 5):
        removed_mask = mask(ids)
        if any((removed_mask & p) == 0 for p in root_masks):
            root_covered += 1
        else:
            frontier.append(removed_mask)
    assert root_covered == 3159845 and len(frontier) == 2665
    star_descendants = [d for d in frontier if d & star_mask == star_mask]
    assert len(star_descendants) == 50
    new_minimal = len(frontier) - len(star_descendants)
    assert new_minimal == 2615

    five_residual = 0
    fallback_cases = []
    maximum_paths = maximum_pair_unions = 0
    for deleted_mask in frontier:
        deleted = frozenset(e for e in edges if deleted_mask >> edge_number[e] & 1)
        child = delete(adj, deleted)
        found, path_count, pair_count = small_residual_witness(child)
        maximum_paths = max(maximum_paths, path_count)
        maximum_pair_unions = max(maximum_pair_unions, pair_count)
        if found:
            five_residual += 1
        else:
            assert deleted_mask & star_mask == star_mask
            assert deleted_mask & fallback_mask == 0
            fallback_cases.append(deleted_mask)
    expected_edges = {(0, 4), (2, 9), (5, 6), (9, 17), (14, 19), (16, 19)}
    expected = {star_mask | (1 << edge_number[e]) for e in expected_edges}
    assert set(fallback_cases) == expected
    assert (five_residual, len(fallback_cases)) == (2659, 6)
    assert root_covered + five_residual + len(fallback_cases) == 3162510
    assert 342541 + 3162510 == 3505051
    print(f'root_covered={root_covered} frontier={len(frontier)} '
          f'star_descendants={len(star_descendants)} new_minimal={new_minimal}')
    print(f'five_residual_children={five_residual} star_fallback={len(fallback_cases)} '
          f'fallback_protected={len(fallback_edges)}')
    print(f'certified_through_radius_five=3505051 '
          f'max_child_geodesic_masks={maximum_paths} '
          f'max_child_pair_unions_checked={maximum_pair_unions}')


if __name__ == '__main__':
    main()
