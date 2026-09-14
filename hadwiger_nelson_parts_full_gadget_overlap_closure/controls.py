#!/usr/bin/env python3
"""Focused checks of this coordinate adapter and its hypothesis boundary."""
import json
from fractions import Fraction as Q
import verify as v


def reject(fn):
    try:
        fn()
    except ValueError:
        return
    raise ValueError('damaged input was accepted')


def main():
    rows, seeds, field = v.inputs()
    for i in range(8):
        a = tuple(int(i == j) for j in range(8))
        v.need(v.sqrt15_times(v.sqrt15_times(a)) == tuple(15*x for x in a),
               'sqrt15 basis roundtrip')
    small = [rows[0]] + rows[374:]
    wrong = [v.rotate_numerators(r, 1) for r in small]
    v.need(sum(not v.in_E(r) for r in wrong) == 135, 'wrong-sign control')
    reject(lambda: v.project(wrong[1], 768))
    corrupt = list(rows[0]); corrupt[2] = 1
    reject(lambda: v.project(tuple(corrupt), 96))
    # The original, unmodified placement has only one overlap and remains 509 points.
    v.need(set(rows[:374]) & set(small) == {rows[0]}, 'one-overlap boundary')
    edges = [(i, j) for i, p in enumerate(rows) for j in range(i+1, 509)
             if v.squared_distance8(p, rows[j]) == (9216,) + (0,)*7]
    v.need(len(edges) == 2442, 'original complete edge graph')
    # Cross-check the new E norm formula against the inherited field arithmetic.
    sample = [field.element(Q(i, 3), Q(j, 2), Q(i-j, 6), Q(i+j, 4))
              for i in range(-2, 3) for j in range(-2, 3)]
    for z in sample:
        a, b, c, d = z
        norm = field.multiply(z, field.conjugate(z))
        v.need(norm == (a*a+33*b*b+3*c*c+11*d*d, 2*(a*b+c*d), 0, 0),
               'norm cross-check')
    graph = v.complete_graph_E([field.element(0), field.element(1)])
    v.need(graph == [(0, 1)], 'unit segment fixture')
    v.check_word('01', 2, graph)
    reject(lambda: v.check_word('00', 2, graph))
    reject(lambda: v.check_word('04', 2, graph))
    reject(lambda: v.complete_graph_E([field.element(0), field.element(0)]))
    result = {'status': 'PASS', 'sqrt15_basis_controls': 8, 'norm_cross_checks': 25,
              'wrong_sign_outside_E': 135, 'damaged_inputs_rejected': 5,
              'original_identity_overlaps': 1, 'original_identity_points': 509,
              'original_identity_all_pairs': 129286, 'original_identity_unit_edges': 2442,
              'original_non_four_proof_replayed': False}
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
