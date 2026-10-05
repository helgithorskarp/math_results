#!/usr/bin/env python3
"""New endpoint products and rational budgets; no parent executable imports."""
import argparse
from fractions import Fraction as F
import json
from math import prod
from pathlib import Path

TIME_CAP = F(1, 10**14)
SIGN_MINIMUM = 800415
MODULUS_CONSTANT = 4 * 10**17


def build_record():
    gates = []

    def rational(v):
        q = F(v)
        return [q.numerator, q.denominator]

    def check(name, left, relation, right):
        left, right = F(left), F(right)
        ok = {'<': left < right, '<=': left <= right, '=': left == right,
              '>': left > right}[relation]
        if not ok:
            raise ValueError(f'{name}: {left} {relation} {right} failed')
        gates.append({'name': name, 'left': rational(left),
                      'relation': relation, 'right': rational(right)})

    t = TIME_CAP
    products = [prod(4 * abs(j - i) - 1 for j in range(1, 9) if j != i)
                for i in range(1, 9)]
    check('rank_product_minimum', min(products), '=', SIGN_MINIMUM)
    check('central_rank_product', (3 * 7 * 11)**2 * 15, '=', SIGN_MINIMUM)
    check('entire_discrepancy_majorant', F(334, 3), '<', 112)
    check('variable_time_original_sign_licence', 112, '<', F(SIGN_MINIMUM, 4096))
    check('time_positive', t, '>', 0)
    check('time_below_one', t, '<', 1)
    check('heated_root_square_sum', 1 + 112 * t, '<', F(9, 4))
    check('interval_radius_square', t / 8, '<', F(1, 4))
    check('residual_time_scaling', (F(1, 10**112)), '=', t**8)
    check('E_time_budget', F(43, 2) + 1204 * t, '<', 24)
    check('G_time_budget', F(339, 8) + F(9453, 2) * t + 176456 * t**2, '<', 44)
    check('lower_band_perturbation', 192 * t, '<', F(1, 1352))
    check('upper_band_perturbation', 192 * t, '<', F(9, 2800))
    check('exact_band_contains_central_lower', F(1, 676), '>', F(1, 1352))
    check('exact_band_contains_central_upper', F(3, 112), '<', F(3, 100))
    check('fourth_trace_time', 4 * 24, '<=', 320)
    check('sixth_trace_time', F(9, 4) * 24 + 6 * 44, '<=', 320)
    check('eighth_trace_time', F(9, 8) * 24 + F(1, 2) * 24 + 3 * 44, '<=', 320)
    check('sixth_trace_residual', F(25, 192), '<', 1)
    check('eighth_trace_residual', F(5, 192) + F(1, 16), '<', 1)
    check('coupling_time', 4 * 24 + 24 * 44, '=', 1152)
    check('coupling_residual', F(5, 24), '<', 1)
    check('Gram_budget_with_R_at_most_t', 320 + 1, '=', 321)
    check('coupling_budget_with_R_at_most_t', 1152 + 1, '=', 1153)
    check('actual_determinant_half_floor', 882 * 321 * t, '<', F(1, 40000000))
    T = F(208, 9)
    check('threshold_budget', T, '<', 24)
    check('exact_band_threshold_product', T * F(3, 100), '<', 1)
    loss = 24 * 2058 * 192 + 1134 * 321 + 1764 * 1153
    check('whole_loss_coefficient', loss, '=', 11881170)
    check('cleared_loss_budget', loss, '<', 13000000)
    quotient = 13000000 * 676 * 40000000
    check('whole_quotient_coefficient', quotient, '=', 351520000000000000)
    check('stated_modulus_constant', quotient, '<', MODULUS_CONSTANT)
    check('universal_small_variance_below_exact_value', F(5560, 243), '<', T)
    check('universal_large_variance_below_exact_value', 23, '<', T)
    check('uniform_value_below_exact_value', 16, '<', T)
    check('wider_collar_inside_modulus_domain', F(1, 10**148), '<', F(1, 10**112))
    check('wider_collar_strict_angular_margin', F(MODULUS_CONSTANT**8, 10**148), '<', F(2, 9)**8)
    check('sharper_collar_inside_modulus_domain', F(1, 10**152), '<', F(1, 10**112))
    check('sharper_collar_eighth_root', F(1, 10**19)**8, '=', F(1, 10**152))
    check('sharper_collar_error', F(MODULUS_CONSTANT, 10**19), '=', F(1, 25))
    check('sharper_collar_angular_value', T + F(1, 25), '=', F(5209, 225))
    check('sharper_collar_below_previous_threshold', F(5209, 225), '<', F(70, 3))
    check('decimal_order_collar_improvement', 180 - 148, '=', 32)
    return {'schema': 'sendov-real-odd-moment-modulus-v1',
            'actual_agent': 'six-sendov-2', 'role': 'researcher',
            'rank_products_in_order_1_to_8': products,
            'gates': gates, 'gate_count': len(gates),
            'time_cap': rational(t), 'residual_cap': rational(t**8),
            'modulus_constant': MODULUS_CONSTANT,
            'parent_mathematical_executables_imported_or_reexecuted': False,
            'ordinary_proof_formalized': False,
            'independent_review_claimed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    record = build_record()
    if args.expected is not None:
        expected = json.loads(args.expected.read_text())
        if record != expected:
            raise ValueError('entire external expected record differs')
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
