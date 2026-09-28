#!/usr/bin/env python3
"""Certify weighted two-geodesic half balance through five edge deletions."""

import json
from itertools import combinations
from pathlib import Path

import verify as base


def delete_edges(rows, edges, mask):
    child = list(rows)
    for i, (u, v) in enumerate(edges):
        if mask & (1 << i):
            child[u] &= ~(1 << v)
            child[v] &= ~(1 << u)
    return tuple(child)


def geodesic_vertex_masks(rows, dist):
    """Return one actual shortest path for each attainable vertex mask."""
    paths = {}

    def extend(start, target, path):
        u = path[-1]
        if u == target:
            paths.setdefault(base.vertex_mask(path), path)
            return
        for v in base.vertices(rows[u]):
            if (dist[start][v] == dist[start][u] + 1
                    and dist[v][target] >= 0
                    and dist[start][v] + dist[v][target]
                    == dist[start][target]):
                extend(start, target, path + (v,))

    for start in range(base.N):
        for target in range(start, base.N):
            if dist[start][target] >= 0:
                extend(start, target, (start,))
    return paths


def find_five_residual(rows, edge_ids):
    """Find and separately check a pair with all residual orders <= five."""
    dist = base.distances(rows)
    paths = geodesic_vertex_masks(rows, dist)
    masks = sorted(paths, key=lambda x: (-x.bit_count(), x))
    seen = set()
    for i, a in enumerate(masks):
        for b in masks[i:]:
            union = a | b
            if union in seen:
                continue
            seen.add(union)
            residual = base.components(rows, base.FULL & ~union)
            if all(c.bit_count() <= 5 for c in residual):
                entry = {'primary': [paths[a], paths[b]], 'secondary': []}
                base.check_hybrid(entry, rows, dist, edge_ids)
                return entry
    return None


def main():
    # Recheck the published graph, all 21 root templates, and radius four.
    base.main()
    root = base.decode_graph6(base.GRAPH6)
    edges = base.edge_list(root)
    edge_ids = {edge: i for i, edge in enumerate(edges)}
    root_dist = base.distances(root)
    data = json.loads(Path(__file__).with_name('certificates.json').read_text())
    protected = [base.check_hybrid(t, root, root_dist, edge_ids)[0]
                 for t in data['templates']]

    star = json.loads(Path(__file__).with_name('radius5_star.json').read_text())
    assert star['deleted_edges'] == [[4, 12], [5, 12], [11, 12], [12, 13]]
    star_mask = sum(1 << edge_ids[tuple(e)] for e in star['deleted_edges'])
    star_child = delete_edges(root, edges, star_mask)
    star_protected, star_residuals = base.check_hybrid(
        star, star_child, base.distances(star_child), edge_ids)
    assert star_residuals == [1, 5, 6]
    assert not star_protected & star_mask
    assert star_protected.bit_count() == 12

    root_covered = child_five_residual = star_fallback = 0
    fallback_masks = []
    for choice in combinations(range(len(edges)), 5):
        deleted = sum(1 << i for i in choice)
        if any((deleted & p) == 0 for p in protected):
            root_covered += 1
            continue
        child = delete_edges(root, edges, deleted)
        if find_five_residual(child, edge_ids) is not None:
            child_five_residual += 1
            continue
        assert (deleted & star_mask) == star_mask
        assert (deleted & star_protected) == 0
        fallback_masks.append(deleted)
        star_fallback += 1

    fifth_edges = {(0, 4), (2, 9), (5, 6), (9, 17), (14, 19), (16, 19)}
    assert set(fallback_masks) == {
        star_mask | (1 << edge_ids[e]) for e in fifth_edges}
    assert (root_covered, child_five_residual, star_fallback) == (
        3159845, 2659, 6)
    assert root_covered + child_five_residual + star_fallback == 3162510
    print('five-edge cases: root templates', root_covered,
          'five-residual children', child_five_residual,
          'star fallback', star_fallback)
    print('total certified deletion patterns through radius five: 3505051')
    print('PASS radius five')


if __name__ == '__main__':
    main()
