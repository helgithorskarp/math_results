#!/usr/bin/env python3
"""Exhaust the three-list criterion and check exact norm fixtures."""
from itertools import product
import json
import common as C


def main():
    large = [m for m in range(1, 16) if m.bit_count() >= 2]
    cases = bad = 0
    for a, b, c in product(large, large, range(1, 16)):
        for edge_mask in range(8):
            edges = [p for k, p in enumerate(((0, 1), (0, 2), (1, 2))) if edge_mask >> k & 1]
            satisfiable = any(all((m >> co) & 1 for m, co in zip((a, b, c), cols))
                              and all(cols[i] != cols[j] for i, j in edges)
                              for cols in product(range(4), repeat=3))
            predicted = C.triangle_obstruction(a, b, c, edge_mask)
            C.S.require(satisfiable != predicted, 'list criterion disagrees with brute force')
            cases += 1
            bad += predicted
    zero = (1, 0, 0, 0, 0, 0, 0, 0, 0)
    one = (1, 1, 0, 0, 0, 0, 0, 0, 0)
    alpha = (1, 0, 0, 0, 0, 1, 0, 0, 0)
    radical = (1, 0, 0, 1, 0, 0, 0, 0, 0)
    imaginary_radical = (1, 0, 0, 0, 0, 0, 0, 1, 0)
    half = (2, 1, 0, 0, 0, 0, 0, 0, 0)
    minus_half = (2, -1, 0, 0, 0, 0, 0, 0, 0)
    fixtures = [(zero, zero, (1, 0, 0, 0, 0)),
                (zero, one, (1, 1, 0, 0, 0)),
                (zero, alpha, (1, 3, 0, 0, 0)),
                (zero, radical, (1, -408, 72, 0, 0)),
                (zero, imaginary_radical, (1, -1224, 216, 0, 0)),
                (half, minus_half, (1, 1, 0, 0, 0))]
    for a, b, expected in fixtures:
        C.S.require(C.squared_distance(a, b) == expected, 'norm fixture mismatch')
    print(json.dumps({'list_cases': cases, 'noncolourable_cases': bad,
                      'all_predictions_match_brute_force': True,
                      'exact_norm_fixtures': len(fixtures)}, indent=2))


if __name__ == '__main__':
    main()
