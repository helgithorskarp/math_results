"""new fixed-bcW-column-mass radius refinement.

Uses this contribution's fresh original DATA decoder only, not a parent
program, witness PSD factor or private aggregate record. The new count,
two-group energy, full box primal and algebraic signs are checked exactly.
All-real completeness bridges are explicitly ordinary in COUPLED-PROOF.md.
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd, isqrt, lcm
import json
from radius import decode, require


def check(decoded=None):
    masks, values, D, degrees, cap = decode() if decoded is None else decoded
    v = [F(x, D) for x in values];k = [220*n for n in degrees]
    P = [i for i in range(58) if v[i] > 0]
    N = [i for i in range(58) if v[i] < 0]
    require((len(P), len(N)) == (20, 38), 'same entire signed original partition')
    triples = [6|(1 << (12+i)) for i in range(9)]
    pure_pairs = [sum(1 << (offset+i) for i in pair)
                  for offset in (3, 12) for pair in combinations(range(9), 2)]
    forbidden = sum(bool(masks[i] & t) for i in N for t in triples)
    allowed = sum(not (masks[i] & b) for i in P for b in pure_pairs)
    require(forbidden == 38*9 and allowed == 1296,
            'EVERY negative/bcW support position and positive/pure-pair position')
    require([sum(not (masks[i] & t) for i in P) for t in triples] == [18]*9,
            'ALL nine actual bcW original column capacities')
    V = sum(v[i] for i in P);K = 220*allowed
    require(K == 285120 and V == F(2912214312567, 1073741824),
            'fixed bcW contribution removes162 apparent movable positive-row slots')
    # The original Ch=0 and 38 fixed -1 positions force positive sum38 in EACH bcW column.
    fixed_positive_bcW_mass_C_units = 38*9
    require(sum(degrees[i] for i in P)-allowed == 162,
            'whole actual support partition of the positive rows')
    gap = [(V*V/760-cap)/2, -V*K/760, F(K*K, 1520)]
    def polynomial(c, e):
        return c[0]+c[1]*e+c[2]*e*e
    lower, upper = F(1, 500), F(1, 320)
    require(V-K*upper > 0 and gap[1]+2*gap[2]*upper < 0,
            'ENTIRE necessary real radius interval has positive group sum and decreasing energy')
    primal_positions = 0
    for e in (lower, upper):
        T = V-K*e
        q = [T/20 if i in P else -T/38 for i in range(58)]
        require(sum(q) == 0 and sum(q[i] for i in P) == T and
                sum(x*x for x in q) == 58*T*T/760,
                'new exact whole original primal/kernel/coupling/energy equality')
        for i in range(58):
            require(v[i]-k[i]*e <= q[i] <= v[i]+k[i]*e,
                    'EVERY original coordinate of the coupled full-box minimizing vector')
            primal_positions += 1
    cage = [F(1, 363), F(1, 362)]
    require(lower < cage[0] < cage[1] < upper and
            polynomial(gap, cage[0]) > 0 and polynomial(gap, cage[1]) < 0,
            'NEW exact strict coupled-threshold isolation in original M units')
    radicand = 760*cap
    require(radicand > 0 and (V-K*cage[0])**2 > radicand > (V-K*cage[1])**2,
            'the explicit smaller square-root threshold matches the isolated root')
    common = lcm(*(x.denominator for x in gap));primitive = [int(x*common) for x in gap]
    divisor = gcd(gcd(abs(primitive[0]), abs(primitive[1])), abs(primitive[2]))
    primitive = [x//divisor for x in primitive]
    c0, c1, c2 = primitive;discriminant = c1*c1-4*c0*c2
    require(c0 > 0 and c1 < 0 and c2 > 0 and discriminant > 0 and
            isqrt(discriminant)**2 != discriminant, 'positive irrational coupled threshold')
    deductions = []
    for radius, clean in [(F(1, 1280), 1600), (F(1, 640), 900),
                           (F(1, 500), 450), (F(1, 400), 180), (cage[0], 0)]:
        g = polynomial(gap, radius)
        require(g > clean, 'NEW exact coupled near-optimal exclusion')
        deductions.append({'original_NS_entry_radius': str(radius), 'Psi': str(g),
                           'strict_clean_gap_lower': clean})
    return {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'status': 'complete ordinary author proof; unformalized and independently unreviewed',
        'published_witness_source_commit': '782bc9042896c0f3887b1807dbd991f75fa13c9b',
        'whole_original_carrier_N_s_B': [278, 58, 81],
        'positive_original_star_positions': P, 'negative_original_star_positions': N,
        'complete_original_fixed_N_bcW_support_positions': forbidden,
        'all_nine_bcW_original_column_allowed_P_counts': [18]*9,
        'fixed_P_bcW_C_sum_in_each_column': 38,
        'fixed_P_bcW_C_sum_all_nine_columns': fixed_positive_bcW_mass_C_units,
        'movable_P_ZZ_WW_original_support_positions': allowed,
        'positive_original_aggregate_sum': str(V), 'positive_sum_displacement_slope': K,
        'old_BB_cap': str(cap),
        'Psi_coefficients_low_to_high': [str(x) for x in gap],
        'full_real_Psi_radius_interval': ['0', '1/320'],
        'coupled_minimum_energy_real_window': ['1/500', '1/320'],
        'new_full_original_primal_endpoint_coordinate_checks': primal_positions,
        'threshold_expression': '(V-sqrt(760*cap))/285120',
        'threshold_radicand': str(radicand),
        'primitive_threshold_polynomial_low_to_high': primitive,
        'threshold_strict_rational_isolation': ['1/363', '1/362'],
        'complete_relaxation_classification': 'original58-coordinate box + zero sum + sum_P q>=V-285120e + optimizer scalar-Schur ball feasible iff e>=threshold, for ALL real e>=0',
        'original_optimizer_NS_entry_movement_clean_strict_lower': '1/363',
        'near_optimal_deductions': deductions,
        'full_real_tau_interval': ['0', '1/256'],
        'original_NS_matrix_realization_or_best_original_distance_claimed': False,
        'parent_or_peer_executable_PSD_factor_or_numerical_package_replayed': False,
        'independent_review_claimed': False,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
