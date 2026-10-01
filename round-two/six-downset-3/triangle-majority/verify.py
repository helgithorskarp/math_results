#!/usr/bin/env python3
"""Replay exact infinite signs, full matrices, literal action and damage controls."""
import argparse
import copy
from fractions import Fraction as F
import json
from pathlib import Path
import resource
from time import monotonic
from poly import R, polynomial, exact_divide
from model import formula, model
from signs import regenerate, compare, lower_sign
from matrices import weights, decode, build, affine, audit
from literal_action import literal, check_columns
from exact import require, schur_psd, polynomial_psd, digest

ROOT = Path(__file__).resolve().parent


def controls(signs, columns):
    tested = []
    def reject(name, callback):
        try:
            callback()
        except (ValueError, TypeError, ZeroDivisionError):
            tested.append(name)
        else:
            raise ValueError('damage control was accepted: '+name)
    boundary = json.loads((ROOT/'BOUNDARIES.json').read_text())[0]
    bad = copy.deepcopy(boundary); bad['values'].pop()
    reject('missing_boundary_value', lambda: decode(bad))
    bad2 = copy.deepcopy(boundary); bad2['keys'][1] = bad2['keys'][0]
    reject('duplicated_boundary_orbit', lambda: decode(bad2))
    bad3 = copy.deepcopy(boundary); bad3['values'][0] = 0.5
    reject('floating_boundary_value', lambda: decode(bad3))
    bad4 = copy.deepcopy(boundary); bad4['q'] = 4
    reject('wrong_boundary_scope', lambda: decode(bad4))
    reject('q_below_domain', lambda: weights(1))
    reject('floating_q', lambda: weights(4.0))
    reject('boolean_q', lambda: weights(True))
    reject('floating_formula_parameter', lambda: formula(4.0))
    reject('negative_lower_constant', lambda: lower_sign(polynomial((-1, 1))))
    reject('negative_lower_coefficient', lambda: lower_sign(polynomial((1, -1))))
    reject('zero_rational_denominator', lambda: R(1, 0))
    reject('inexact_polynomial_division', lambda: exact_divide(polynomial(1), polynomial((1, 1))))
    reject('floating_polynomial_coefficient', lambda: polynomial((1, 0.5)))
    bad_weights = weights(4); key = ((0, 1), (1, 0)); bad_weights[key] += 1
    bad_domain = build(4, bad_weights)
    reject('changed_disjoint_weight_kernel', lambda: affine(*bad_domain))
    reject('asymmetric_matrix', lambda: schur_psd([[F(1), F(1)], [F(0), F(1)]]))
    reject('zero_pivot_nonzero_row', lambda: schur_psd([[F(0), F(1)], [F(1), F(0)]]))
    reject('negative_Schur_pivot', lambda: schur_psd([[F(-1)]]))
    reject('negative_characteristic_root', lambda: polynomial_psd([[F(-1)]]))
    reject('floating_matrix_entry', lambda: schur_psd([[0.5]]))
    float_weights = weights(4); float_weights[((0, 1), (1, 0))] = 0.5
    reject('floating_disjoint_weight', lambda: build(4, float_weights))
    reject('missing_literal_basis_vector', lambda: check_columns(columns[:-1], 41))
    duplicate = copy.deepcopy(columns); duplicate[-1] = duplicate[0]
    reject('duplicated_literal_basis_vector', lambda: check_columns(duplicate, 41))
    c = build(4)[3]; changed = copy.deepcopy(c)
    changed[0][1] += 1; changed[1][0] += 1
    reject('changed_literal_matrix_action', lambda: literal(4, changed))
    reject('wrong_literal_operator_sign', lambda: literal(4, [[-v for v in row] for row in c]))
    changed_sign = copy.deepcopy(signs); changed_sign['signs'][0]['coefficients'][0] = '0'
    reject('changed_infinite_coefficient', lambda: compare(signs, changed_sign))
    missing_sign = copy.deepcopy(signs); missing_sign['signs'].pop()
    reject('missing_infinite_sign_record', lambda: compare(signs, missing_sign))
    positive = [([[F(0)]], 0), ([[F(2, 3)]], 1),
                ([[F(1), F(1)], [F(1), F(1)]], 1),
                ([[F(2), F(-1)], [F(-1), F(2)]], 2)]
    for matrix, rank in positive:
        require(schur_psd(matrix) == rank and polynomial_psd(matrix)[0] == rank,
                'positive matrix control differs')
    return {'rejected': tested, 'rejection_count': len(tested), 'positive_matrix_controls': len(positive)}


def replay():
    signs = regenerate()
    compare(json.loads((ROOT/'SIGNS.json').read_text()), signs)
    matrices = [audit(q) for q in [2, 3, 4]]
    action, columns, _ = literal(4)
    result = {'agent': 'six-downset-3', 'role': 'researcher',
              'mathematical_scope': 'every integer q>=2, and every finite nonempty mixed product',
              'infinite_signs_sha256': signs['signs_sha256'], 'infinite_sign_count': signs['sign_count'],
              'infinite_coefficient_count': signs['coefficient_count'],
              'literal_matrices': matrices, 'literal_sector_action': action,
              'controls': controls(signs, columns)}
    result['records_sha256'] = digest(result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-results', type=Path, help='write deterministic replay records to this path')
    args = parser.parse_args()
    start = monotonic()
    result = replay()
    if args.write_results:
        args.write_results.write_text(json.dumps(result, indent=2)+'\n')
    else:
        require(result == json.loads((ROOT/'RESULTS.json').read_text()), 'stored results differ from replay')
    print(json.dumps({'passed': True, 'infinite_scope': 'all integers q>=2',
                      'sign_count': result['infinite_sign_count'],
                      'literal_matrix_q': [r['q'] for r in result['literal_matrices']],
                      'literal_basis_rank_q4': result['literal_sector_action']['literal_basis_rank'],
                      'damage_rejections': result['controls']['rejection_count'],
                      'records_sha256': result['records_sha256'],
                      'seconds': round(monotonic()-start, 3),
                      'peak_RSS_KiB': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}))
