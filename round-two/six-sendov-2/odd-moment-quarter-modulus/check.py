#!/usr/bin/env python3
"""New quarter-power licence budgets only; no parent mathematics imports."""
import argparse
from fractions import Fraction as F
import json
from pathlib import Path

TIME_MULTIPLIER = 10**10
TIME_CAP = F(1, 10**14)
COORDINATE_DENOMINATOR = 5376
MODULUS_CONSTANT = 4 * 10**27


def build_record():
    gates = []

    def pair(v):
        v = F(v)
        return [v.numerator, v.denominator]

    def check(name, left, relation, right):
        left, right = F(left), F(right)
        valid = {'=': left == right, '<': left < right,
                 '<=': left <= right, '>': left > right}[relation]
        if not valid:
            raise ValueError(f'{name}: {left} {relation} {right} failed')
        gates.append({'name': name, 'left': pair(left),
                      'relation': relation, 'right': pair(right)})

    t = TIME_CAP
    c = COORDINATE_DENOMINATOR
    check('projection_vector_norm_square', 1 - F(1, 8), '=', F(7, 8))
    check('projection_coefficient', F(8, 7) * F(7, 8), '=', 1)
    check('projection_displacement_square', F(8, 7)**2 * F(7, 8), '=', F(8, 7))
    check('quartic_band_below_quarter', F(103, 672), '<', F(1, 4))
    check('projection_loss_below_one', F(4, 7), '<', 1)
    check('normalized_projection_distance_square_budget', 2 * F(8, 7), '<', 4)
    check('gradient_times_distance_budget', 4 * 2, '=', 8)
    check('zero_face_band_difference', F(13, 84) - F(103, 672), '=', F(1, 672))
    check('coordinate_separation_budget', F(1, 672) / 8, '=', F(1, c))
    check('opposite_sign_distance', F(2, c), '=', F(1, 2688))
    check('new_time_positive', t, '>', 0)
    check('new_time_below_one', t, '<', 1)
    check('time_scaled_residual_cap', (t / TIME_MULTIPLIER)**4, '=', F(1, 10**96))
    check('heated_quartic_perturbation', 192 * t, '<', F(1, 672))
    check('heated_quartic_upper_band', F(1, 8) + F(3, 112) + F(1, 672), '=', F(103, 672))
    check('root_interval_radius_square', t / 8, '<', F(1, c*c))
    check('opposite_endpoint_distance_after_radius', F(1, 2688) - F(1, c), '=', F(1, c))
    check('full_endpoint_product_root_count', 1 + 3 + 4, '=', 8)
    check('three_near_factor_coefficient', 3**3, '=', 27)
    check('fourth_radius_power_heat_coefficient', F(1, 8)**2, '=', F(1, 64))
    check('entire_odd_discrepancy_majorant', F(334, 3), '<', 112)
    check('new_original_root_sign_licence', 112, '<', F(27 * TIME_MULTIPLIER**2, 64 * c**4))
    check('new_residual_at_most_time_coefficient', F(1, TIME_MULTIPLIER**4), '<=', 1)
    coefficient = 351520000000000000 * TIME_MULTIPLIER
    check('new_modulus_coefficient', coefficient, '<', MODULUS_CONSTANT)
    check('wider_collar_inside_domain', F(1, 10**114), '<', F(1, 10**96))
    check('quarter_collar_strict_angular_margin', F(MODULUS_CONSTANT**4, 10**114), '<', F(2, 9)**4)
    check('sharper_collar_inside_domain', F(1, 10**116), '<', F(1, 10**96))
    check('sharper_collar_fourth_root', F(1, 10**29)**4, '=', F(1, 10**116))
    check('sharper_collar_error', F(MODULUS_CONSTANT, 10**29), '=', F(1, 25))
    check('sharper_collar_value', F(208, 9) + F(1, 25), '=', F(5209, 225))
    check('first_collar_decimal_improvement', 180 - 114, '=', 66)
    check('previous_collar_decimal_improvement', 148 - 114, '=', 34)
    return {'schema': 'sendov-real-quarter-moment-modulus-v1',
            'actual_agent': 'six-sendov-2', 'role': 'researcher',
            'gates': gates, 'gate_count': len(gates),
            'time_multiplier': TIME_MULTIPLIER, 'time_cap': pair(t),
            'coordinate_denominator': c, 'modulus_constant': MODULUS_CONSTANT,
            'parent_mathematical_executables_imported_or_reexecuted': False,
            'ordinary_proof_formalized': False, 'independent_review_claimed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    record = build_record()
    if args.expected is not None and record != json.loads(args.expected.read_text()):
        raise ValueError('entire external expected record differs')
    print(json.dumps(record, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
