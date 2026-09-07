#!/usr/bin/env python3
"""Small constructive, conservative-filter and malformed-input controls."""
import json
import folds


def point(x=0, y=0, sqrt3_y=0):
    row = [0]*16
    row[0], row[8], row[9] = x, y, sqrt3_y
    return tuple(row)


def main():
    diamond = [point(-48), point(48), point(sqrt3_y=48), point(sqrt3_y=-48)]
    edges = folds.unit_edges(diamond, 96)
    folds.require(len(edges) == 5, 'diamond geometry')
    result = folds.analyse(diamond, edges)
    witness = result['candidate']
    folds.require(not result['every_one_axis_fold_injective'] and witness['vertices'] == 3
                  and witness['all_input_edges_preserved'], 'constructive diamond control')
    folds.require(len(folds.unit_edges(witness['coordinates'], witness['scale'])) == 3,
                  'folded diamond is not a triangle')
    triangle = diamond[:3]
    folds.require(folds.analyse(triangle, folds.unit_edges(triangle, 96))[
                  'every_one_axis_fold_injective'], 'triangle negative control')
    spindle = [point(), point(96), point(48, sqrt3_y=48), point(144, sqrt3_y=48)]
    b = [0]*16; b[0], b[12] = 80, 16
    c = [0]*16; c[0], c[5], c[9], c[12] = 40, -8, 40, 8
    d = [0]*16; d[0], d[5], d[9], d[12] = 120, -8, 40, 24
    spindle += [tuple(b), tuple(c), tuple(d)]
    se = folds.unit_edges(spindle, 96)
    folds.require(len(se) == 11, 'seven-point control geometry')
    old_modulus, old_roots = folds.MODULUS, folds.ROOTS
    try:
        # Every coordinate numerator vanishes modulo 2. This intentionally
        # creates many false separator proposals and exercises exact refinement.
        folds.MODULUS, folds.ROOTS = 2, (1, 1, 1)
        refined = folds.analyse(spindle, se)
        folds.require(refined['every_one_axis_fold_injective'] and
                      refined['exact_fallback_paths'] == 10, 'exact fallback control')
        positive = folds.analyse(diamond, edges)
        folds.require(positive['candidate']['vertices'] == 3, 'exact positive fallback')
    finally:
        folds.MODULUS, folds.ROOTS = old_modulus, old_roots
    rejected = []
    for name, rows, es in [
        ('repeated_points', diamond+[diamond[0]], edges),
        ('non_unit_edge', diamond, sorted(edges+[(2, 3)])),
        ('reversed_edge', diamond, [(1, 0)])]:
        try:
            folds.analyse(rows, es)
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('malformed input accepted: '+name)
    print(json.dumps({'all_checks': True, 'diamond_fold_vertices': witness['vertices'],
          'diamond_unit_edges_preserved': 5, 'triangle_fold_injective': True,
          'spindle_exact_fallback_paths': refined['exact_fallback_paths'],
          'spindle_fold_injective': True, 'malformed_inputs_rejected': rejected}, sort_keys=True))


if __name__ == '__main__':
    main()
