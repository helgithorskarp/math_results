"""New exact 1+19+38 original-row/column radius refinement.

Same-author canonical original-entry decoder is openly credited in census.py.
The old comparison cap and Schur/dual theorem are explicit published
premises. No old factor, EXPECTED record, program or peer input is loaded.
The all-real/group-Cauchy/nesting bridges belong in PROOF.md.
"""
from fractions import Fraction as F
from math import gcd, isqrt, lcm
from pathlib import Path
import importlib.util
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def decoder():
    p = Path(__file__).with_name('census.py')
    spec = importlib.util.spec_from_file_location('new_floor_census', p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.original()


def check():
    S, B, label, A, values, P, N, D = decoder()
    abc = S.index(7); J = [i for i in P if i != abc]
    require(len(J) == 19 and len(N) == 38, 'NEW entire1+19+38 original partition')
    pure = [j for j, b in enumerate(B) if label[b] in {(0, 2, 0), (0, 0, 2)}]
    bcW = [j for j, b in enumerate(B) if label[b] == (6, 0, 1)]
    require(len(pure) == 72 and len(bcW) == 9, 'named original bad types')
    require(all(S[abc] & B[j] and A[abc][j] == -D for j in bcW),
            'NEW all9 fixed abc triple positions')
    require(all(A[i][j] == -D for i in N+[abc] for j in bcW),
            'NEW all351 fixed complement/triple positions')
    require(all(sum(A[i][j] for i in J) == 39*D for j in bcW),
            'NEW ALL9 individual J column sum39 identities')
    allowed = [(i, j) for i in J for j in pure if not (S[i] & B[j])]
    require(len(allowed) == 1224 and all(not (S[abc] & B[j]) for j in pure),
            'NEW all1224 J pure positions and72 abc pure positions')
    v = [F(x, D) for x in values]
    vabc = v[abc]; V = sum(v[i] for i in P)
    require(vabc == F(148830682779, 1073741824) and
            V == F(2912214312567, 1073741824), 'whole original group constants')
    cap = F(4998177, 1024)
    z = [vabc, F(-15840)]; y = [V-vabc, F(-269280)]; T = [V, F(-285120)]

    def square(t):
        return [t[0]**2, 2*t[0]*t[1], t[1]**2]

    zs, ys, ts = square(z), square(y), square(T)
    E = [zs[i]+ys[i]/19+ts[i]/38 for i in range(3)]
    G = [(E[0]-58*cap)/116, E[1]/116, E[2]/116]
    old = [(ts[0]/760-cap)/2, ts[1]/1520, ts[2]/1520]
    diff = [20*z[i]-T[i] for i in range(2)]
    require([G[i]-old[i] for i in range(3)] == [x/44080 for x in square(diff)],
            'NEW whole quadratic improvement identity')

    def polynomial(c, e):
        return sum(x*e**i for i, x in enumerate(c))

    r0, r1 = F(1, 500), F(1, 320)
    require(polynomial(z, r1) > 0 and polynomial(y, r1) > 0 and
            G[0] > 0 and G[1]+2*G[2]*r1 < 0,
            'NEW entire real necessary window positive groups and strictly decreasing gap')
    endpoint_checks = []
    for e in (r0, r1):
        a, b, t = polynomial(z, e), polynomial(y, e), polynomial(T, e)
        q = [a if i == abc else b/19 if i in J else -t/38 for i in range(58)]
        require(sum(q) == 0 and q[abc] == a and sum(q[i] for i in J) == b and
                sum(x*x for x in q) == polynomial(E, e),
                'NEW full original1+19+38 primal energy and masses')
        for i, s in enumerate(S):
            k = 220*sum(not (s & bad) for bad in B)
            require(v[i]-k*e <= q[i] <= v[i]+k*e,
                    'NEW EVERY original coordinate box of subset primal')
            endpoint_checks.append({'e': str(e), 'position': i,
                                    'lower_slack': str(q[i]-(v[i]-k*e)),
                                    'upper_slack': str(v[i]+k*e-q[i])})
    require(len(endpoint_checks) == 116, 'NEW whole116 subset-primal endpoint constraints')
    require(polynomial(diff, r0) < 0 and diff[1] < 0,
            'NEW strict improvement throughout whole primal window')
    require(polynomial(G, F(1, 363)) > 0 and polynomial(G, F(1, 362)) < 0,
            'NEW exact coarse threshold cage')
    common = lcm(*(c.denominator for c in G))
    primitive = [int(c*common) for c in G]
    divisor = gcd(gcd(abs(primitive[0]), abs(primitive[1])), abs(primitive[2]))
    primitive = [n//divisor for n in primitive]
    c0, c1, c2 = primitive; discriminant = c1*c1-4*c0*c2
    require(c0 > 0 and c1 < 0 and c2 > 0 and discriminant > 0 and
            isqrt(discriminant)**2 != discriminant, 'NEW irrational subset threshold')
    Q = 10**9

    def cage(c):
        lo, hi = Q//363, (Q+361)//362
        require(polynomial(c, F(lo, Q)) > 0 and polynomial(c, F(hi, Q)) < 0,
                'exact integer grid cage initialized')
        while hi-lo > 1:
            mid = (lo+hi)//2
            value = polynomial(c, F(mid, Q))
            require(value != 0, 'irrational threshold grid equality impossible')
            if value > 0:
                lo = mid
            else:
                hi = mid
        return F(lo, Q), F(hi, Q)

    old_cage, new_cage = cage(old), cage(G)
    require(old_cage[1] < new_cage[0], 'NEW strict separation from previous coupled threshold')
    sep = (old_cage[1]+new_cage[0])/2
    require(polynomial(old, sep) < 0 < polynomial(G, sep),
            'NEW exact rational original-movement separation certificate')
    # The original floor-clipping proposal is exactly inactive on the WHOLE
    # necessary window, including the largest allowed real tau.
    positive_pure = [(i, j) for i in P for j in pure if not (S[i] & B[j])]
    margins = [F(A[i][j]+D, D) for i, j in positive_pure]
    first_floor = (min(margins)-F(1, 256))/220
    require(len(margins) == 1296 and first_floor > F(1, 100) > r1,
            'NEW entire tau/radius window has no active P-pure floor clipping')
    return {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'status': 'PRIVATE exact author subset certificate; ordinary bridges separately required',
        'original_carrier_N_s_B': [278, 58, 81],
        'whole_original_star_masks': S, 'whole_original58_vector_numerators': values,
        'vector_denominator': D, 'abc_position': abc,
        'remaining_positive_original_positions': J, 'negative_original_positions': N,
        'fixed_complement_bcW_positions': 351, 'each_J_bcW_column_sum': 39,
        'all9_actual_bcW_masks': [B[j] for j in bcW],
        'original_J_pure_disjoint_positions': 1224, 'abc_pure_disjoint_positions': 72,
        'abc_lower_affine': [str(x) for x in z],
        'J_mass_lower_affine': [str(x) for x in y],
        'total_positive_lower_affine': [str(x) for x in T],
        'energy_polynomial_low_to_high': [str(x) for x in E],
        'Gamma_polynomial_low_to_high': [str(x) for x in G],
        'old_Psi_polynomial_low_to_high': [str(x) for x in old],
        'Gamma_minus_Psi_square_affine': [str(x) for x in diff],
        'Gamma_minus_Psi_square_denominator': 44080,
        'full_real_necessary_radius_interval': ['0', '1/320'],
        'full_real_primal_minimum_window': ['1/500', '1/320'],
        'all116_actual_endpoint_box_checks': endpoint_checks,
        'primitive_threshold_polynomial_low_to_high': primitive,
        'threshold_expression': '(-c1-sqrt(c1^2-4*c0*c2))/(2*c2)',
        'threshold_strict_coarse_cage': ['1/363', '1/362'],
        'new_threshold_strict_grid_cage': [str(x) for x in new_cage],
        'old_threshold_strict_grid_cage': [str(x) for x in old_cage],
        'old_threshold_strictly_less_than_rational_original_optimizer_lower': str(sep),
        'old_Psi_at_separator': str(polynomial(old, sep)),
        'new_Gamma_at_separator': str(polynomial(G, sep)),
        'first_possible_P_pure_floor_hit_at_largest_tau': str(first_floor),
        'floor_clipping_exactly_inactive_for_ALL_tau_and_e_in_necessary_window': True,
        'full_real_tau_interval': ['0', '1/256'],
        'aggregate_relaxation_full_iff_or_original_realization_claimed_by_code_alone': False,
        'original_matrix_or_best_original_distance_or_general_H_I_claimed': False,
        'ancestor_program_PSD_factor_or_peer_input_imported': False,
        'independent_review_claimed': False,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
