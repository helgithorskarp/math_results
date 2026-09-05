#!/usr/bin/env python3
"""Inspect the literal twelve-vertex core without importing the SAT encoding."""
from itertools import combinations, product
from pathlib import Path
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def inspect(path):
    lines = path.read_text().splitlines()
    require(lines[0] == '12 42' and len(lines) == 43, 'core dimensions')
    edges = [tuple(map(int, s.split())) for s in lines[1:]]
    require(all(len(e) == 2 and 0 <= e[0] < e[1] < 12 for e in edges), 'edge syntax')
    require(edges == sorted(set(edges)), 'edge ordering or multiplicity')
    graph = {e: e in edges for e in combinations(range(12), 2)}
    for a, b in graph:
        i, u = divmod(a, 3)
        j, v = divmod(b, 3)
        expected = True if i == j else ((v-u) % 3 == 0 if (i, j) in ((0, 1), (2, 3)) else (v-u) % 3 in (0, 1))
        require(graph[a, b] == expected, 'literal core differs from the stated definition')
    sigma = [3*(v//3)+(v+1) % 3 for v in range(12)]
    require(all(graph[e] == graph[tuple(sorted(sigma[v] for v in e))] for e in graph), 'core action')
    counts = {str(color): {str(k): sum(all(graph[e] == color for e in combinations(vs, 2))
                                      for vs in combinations(range(12), k)) for k in range(2, 6)}
              for color in (0, 1)}
    require(counts == {'0': {'2': 24, '3': 0, '4': 0, '5': 0},
                       '1': {'2': 42, '3': 52, '4': 18, '5': 0}}, 'core clique census')
    degrees = [sum(graph[tuple(sorted((v, w)))] for w in range(12) if w != v) for v in range(12)]
    require(degrees == [7]*12, 'core degree')
    red_fours = [vs for vs in combinations(range(12), 4) if all(graph[e] for e in combinations(vs, 2))]
    signatures = []
    for sig in product((0, 1), repeat=4):
        # A fixed vertex is uniformly adjacent to each of the four moving triangles.
        bad_red = any(all(sig[v//3] for v in vs) for vs in red_fours)
        if not bad_red:
            signatures.append(list(sig))
    require(signatures == [list(s) for s in product((0, 1), repeat=4) if sum(s) <= 2], 'fixed extension signatures')
    # An independent test through all 1287 five-sets of each 13-vertex extension.
    for sig in product((0, 1), repeat=4):
        enlarged = dict(graph) | {(v, 12): bool(sig[v//3]) for v in range(12)}
        valid = not any(len({enlarged[e] for e in combinations(vs, 2)}) == 1
                        for vs in combinations(range(13), 5))
        require(valid == (list(sig) in signatures), 'literal fixed extension mismatch')
    return {'vertices': 12, 'red_edges': 42, 'red_degrees': degrees, 'cliques_by_color_and_order': counts,
            'permitted_fixed_signatures': signatures, 'full_fixed_extensions_checked': 16,
            'is_a_43_vertex_target': False}


if __name__ == '__main__':
    print(json.dumps(inspect(Path(__file__).with_name('minority_core.edges')), indent=2, sort_keys=True))
