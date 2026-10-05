"""exact sign certificate for the full nonnegative three-type cone.

Freshly aggregates public DATA through this contribution's aggregate.py.
All-real monotonicity, Schur/dual and triangle bridges are in PROOF.md.
No author or peer ancestor program, PSD factor or numerical solver runs.
"""
from fractions import Fraction as F
from math import lcm
import json
from aggregate import aggregate, require


def check(data=None):
    if data is None:
        data = aggregate()
    K = [[F(x) for x in row] for row in data['Schur_minus_comparison_K']]
    Qmatrix = [[F(x) for x in row] for row in data['Q_Gram']]
    capmatrix = [[F(x) for x in row] for row in data['old_BB_cap']]
    A, B, C = map(F, data['balanced_gap_coefficients_t2_t_1'])
    signs = {
        'minus_K_ZZ_ZZ': -K[0][0], 'minus_K_WW_WW': -K[1][1],
        'minus_K_bcW_bcW': -C,
        'K_ZZ_WW_plus_K_ZZ_ZZ': K[0][1] + K[0][0],
        'K_ZZ_WW_plus_K_WW_WW': K[0][1] + K[1][1],
        'K_ZZ_bcW': K[0][2], 'K_WW_bcW': K[1][2],
        'K_ZZ_bcW_plus_K_bcW_bcW': K[0][2] + C,
        'K_WW_bcW_plus_K_bcW_bcW': K[1][2] + C,
        'balanced_A': A, 'balanced_B_plus_twice_C': B + 2*C,
        'balanced_low_chart_derivative_twice_at_quarter': A - 16*C,
    }
    require(all(x > 0 for x in signs.values()), 'ALL exact strict derivative-sign certificates')
    Q = sum(x for row in Qmatrix for x in row)
    cap = sum(x for row in capmatrix for x in row)
    optimum = (Q - cap) / 2
    require(Q - cap == A + B + C and optimum > 2493, 'full three-cone maximum value')
    quarter = F(data['balanced_normalized_bound_at_quarter'])
    require(optimum > quarter, 'published quarter weights strictly suboptimal for this certificate')
    # Fresh original entry-displacement corollary, with integer norm separators.
    require(756**2 < 58*Q < 757**2 and 58*cap < 533**2,
            'ALL new exact lower and upper norm separators')
    require(58*F(220*81, 610)**2 < 223**2,
            'original entry radius 1/610 cannot account for required weighted movement')
    # Fresh all-one robust cost curve; it is not claimed weight-optimal at e>0.
    kappa = F(61, 8) * 220 * 81
    radius = F(1, 610)
    require(58 < F(61, 8)**2 and kappa*radius < 756,
            'ENTIRE real radius interval has positive squared triangle bound')
    coefficients = [optimum, -F(757, 58)*kappa, kappa*kappa/116]
    def gamma(e):
        return coefficients[0] + coefficients[1]*e + coefficients[2]*e*e
    endpoints = []
    for e, lower in [(F(1, 1280), 1200), (F(1, 640), 100), (radius, 0)]:
        value = gamma(e)
        require(value > lower, 'NEW exact all-one robust cost endpoint')
        endpoints.append({'original_NS_entry_radius': str(e), 'Gamma': str(value),
                          'strict_clean_gap_lower': lower})
    common = lcm(*(x.denominator for row in K for x in row))
    return {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'status': 'complete ordinary author proof; unformalized and independently unreviewed',
        'witness_source_commit': data['published_witness_source_commit'],
        'whole_aggregation': data,
        'K_common_denominator': common,
        'K_numerators': [[int(x*common) for x in row] for row in K],
        'strict_sign_certificate': {key: str(value) for key, value in signs.items()},
        'certificate_domain': 'all real z,w,b>=0 with max(z,w)>0',
        'alpha': 'max(z,w)*max(z,w,b)',
        'unique_maximizing_rays': 'z=w=b>0',
        'fixed_witness_Q_all_one': str(Q), 'comparison_cap_all_one': str(cap),
        'full_three_type_maximum': str(optimum), 'clean_strict_lower': 2493,
        'quarter_weight_value': str(quarter),
        'all_one_weight_l1': 81, 'all_one_alpha': 1,
        'norm_lower': 756, 'norm_upper': 757, 'optimizer_norm_upper': 533,
        'weighted_norm_movement_strict_lower': 223,
        'original_NS_entry_movement_strict_lower': '1/610',
        'robust_Gamma_coefficients_low_to_high': [str(x) for x in coefficients],
        'robust_rho_coefficient': str(kappa), 'full_real_radius_interval': ['0', '1/610'],
        'robust_endpoint_deductions': endpoints,
        'full_real_tau_interval': ['0', '1/256'],
        'fixed_witness_fibers_vary_with_weights': True,
        'fiber_optimum_or_best_entry_movement_or_generic_H_claimed': False,
        'ancestor_program_or_PSD_factor_replayed': False,
        'independent_review_claimed': False,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
