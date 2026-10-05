"""Exact original q18 weighted-radius finite certificate.

Actual six-downset-3 / researcher. The new local census original DATA
decoder is openly shared, as is the 143-key comparison DATA convention.
No ancestor program, EXPECTED record, PSD factor or peer input is read.
The all-real Schur/dual/Cauchy bridges are in WEIGHTED-PROOF.md.
This is an author checker, not independent review or a formal proof.
"""
from collections import Counter
from fractions import Fraction as F
from math import gcd, isqrt, lcm
from pathlib import Path
import hashlib
import importlib.util
import json
import sys


def require(ok, message):
    if not ok:
        raise ValueError(message)


def square(t):
    return [t[0]**2, 2*t[0]*t[1], t[1]**2]


def multiply(t, u):
    return [t[0]*u[0], t[0]*u[1]+t[1]*u[0], t[1]*u[1]]


def at(c, x):
    return sum(value*x**i for i, value in enumerate(c))


def record():
    root = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location('weighted_original_census', root/'census.py')
    decoder = importlib.util.module_from_spec(spec); spec.loader.exec_module(decoder)
    S, B, label, A, nums, P, N, D = decoder.original()
    abc = S.index(7); J = [i for i in P if i != abc]
    pure = [j for j, bad in enumerate(B) if label[bad] in {(0, 2, 0), (0, 0, 2)}]
    triples = [j for j, bad in enumerate(B) if label[bad] == (6, 0, 1)]
    t = [int(j in triples) for j in range(81)]
    require((len(J), len(N), len(pure), len(triples), sum(t)) == (19, 38, 72, 9, 9),
            'weighted original partition')
    require(all(S[i] & B[j] and A[i][j] == -D for i in N+[abc] for j in triples),
            'all351 weighted fixed-complement entries')
    require(all(sum(A[i][j] for i in J) == 39*D for j in triples),
            'all9 individual weighted J column kernels')
    require(sum(not S[abc] & B[j] for j in pure) == 72 and
            sum(not S[i] & B[j] for i in J for j in pure) == 1224,
            'all72 and1224 original movable weighted positions')
    w = [F(sum(A[i][j] for j in triples), D) for i in range(58)]
    require(w[abc] == -9 and all(w[i] == -9 for i in N) and
            sum(w[i] for i in J) == 351 and sum(w) == 0,
            'whole58 original weighted perturbation vector')

    raw = (root.parent/'q18-schur-weight-radius/COMPARISON.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() ==
            '6770d9db69983e4cbd75480a9f784dd4c9c9d254cf7f455bbd0d4a62633b2ca2',
            'whole defining comparison DATA')
    comparison = json.loads(raw); X = sorted(label)
    keys = sorted({tuple(sorted((label[u], label[v])))
                   for i, u in enumerate(X) for v in X[i+1:]
                   if u != 1 and v != 1 and not u & v})
    require(len(keys) == 143 and comparison['comparison_free_denominator'] == 16384 and
            len(comparison['comparison_free_numerators']) == 143,
            'entire original rational comparison domain')
    table = {key: F(value, 16384) for key, value in
             zip(keys, comparison['comparison_free_numerators'])}
    old = [[F(57) if u == v else F(-1) if u & v else
            table[tuple(sorted((label[u], label[v])))] for v in B] for u in B]
    edges = [(i, j) for i, u in enumerate(B) for j, v in enumerate(B) if i < j and not u & v]
    edge_counts = Counter(t[i]+t[j] for i, j in edges)
    require(len(edges) == 2628 and edge_counts == {0: 2052, 1: 576},
            'all2628 original edge products; no disjoint triple/triple edge')
    require(all(t[i]*t[j] == 0 for i, j in edges) and any(t[i]+t[j] == 1 for i, j in edges),
            'alpha_u exactly1+lambda for every real lambda>=0')
    cap_coeff = [sum(map(sum, old)),
                 sum((t[i]+t[j])*old[i][j] for i in range(81) for j in range(81)),
                 sum(t[i]*t[j]*old[i][j] for i in range(81) for j in range(81))]
    R = F(186731, 4096)
    require(all(sum(old[j]) == R for j in triples), 'each9 original old triple row sums')
    require(cap_coeff == [F(4998177, 1024), 18*R, F(441)],
            'whole6561 original weighted cap polynomial')

    V = F(sum(nums[i] for i in P), D); alpha0 = F(nums[abc], D)
    a = [alpha0, F(-220*72)]; b = [V-alpha0, F(-220*1224)]
    T = [a[i]+b[i] for i in range(2)]
    energy = [square(a)[i]+square(b)[i]/19+square(T)[i]/38 for i in range(3)]
    base = [energy[i]/58-(cap_coeff[0] if i == 0 else 0) for i in range(3)]
    linear = [(-18*a[i]+702*b[i]/19+18*T[i])/58-
              (cap_coeff[1] if i == 0 else 0) for i in range(2)]
    quadratic = (F(81)+F(351**2, 19)+F(342**2, 38))/58-cap_coeff[2]
    require(linear == [18*(b[0]/19-R), 18*b[1]/19] and quadratic == F(-5220, 19),
            'entire bivariate weighted energy-minus-cap identity')
    selected = [-value/(2*quadratic) for value in linear]
    Baffine = [b[0]-19*R, b[1]]
    require(selected == [value/580 for value in Baffine],
            'exact vertex of concave unnormalized lambda quadratic')
    Fpoly = [base[i]+multiply(linear, selected)[i]+quadratic*square(selected)[i]
             for i in range(3)]
    require(Fpoly == [base[i]+F(9, 11020)*square(Baffine)[i] for i in range(3)],
            'entire optimized unnormalized weighted-radius polynomial')
    require(Fpoly == [F(91211746346430036217583571, 12705194980767453675520),
                      F(-25756116822218871, 9244246016), F(91593089280, 551)],
            'named exact weighted polynomial coefficients')
    a_selected = [a[i]-9*selected[i] for i in range(2)]
    b_selected = [b[i]+351*selected[i] for i in range(2)]
    signs = []
    for e in (F(0), F(1, 300)):
        require(at(selected, e) > 0 and at(a_selected, e) > 0 and at(b_selected, e) > 0,
                'all-real endpoint licence for positive weighted groups')
        signs.append({'e': str(e), 'lambda': str(at(selected, e)),
                      'abc_lower': str(at(a_selected, e)), 'J_mass_lower': str(at(b_selected, e))})
    require(Fpoly[2] > 0 and Fpoly[1]+2*Fpoly[2]*F(1, 300) < 0,
            'strictly decreasing whole real window by affine derivative')
    samples = []
    for e in (F(0), F(1, 320), F(1, 315), F(1, 314), F(1, 300)):
        value = at(Fpoly, e); lam = at(selected, e)
        samples.append({'e': str(e), 'F': str(value), 'lambda': str(lam),
                        'necessary_cost_gap': str(max(F(0), value)/(2*(1+lam)))})
    require(at(Fpoly, F(1, 315)) > 0 > at(Fpoly, F(1, 314)),
            'sharp original radius root strict coarse cage')
    common = lcm(*(v.denominator for v in Fpoly)); primitive = [int(v*common) for v in Fpoly]
    divisor = gcd(gcd(abs(primitive[0]), abs(primitive[1])), abs(primitive[2]))
    primitive = [v//divisor for v in primitive]
    c0, c1, c2 = primitive; disc = c1*c1-4*c0*c2
    require(c0 > 0 and c1 < 0 and c2 > 0 and disc > 0 and isqrt(disc)**2 != disc,
            'exact irrational smaller weighted root')
    Q = 10**9; lo, hi = Q//315, (Q+313)//314
    require(at(Fpoly, F(lo, Q)) > 0 > at(Fpoly, F(hi, Q)), 'weighted integer-grid cage initialized')
    while hi-lo > 1:
        mid = (lo+hi)//2; value = at(Fpoly, F(mid, Q))
        require(value != 0, 'irrational weighted root excludes rational grid equality')
        if value > 0:
            lo = mid
        else:
            hi = mid
    old_upper = F(2757399, 10**9)  # Explicitly credited proved subset-root cage, not loaded EXPECTED.
    eta0 = F(1, 315)-old_upper
    require(eta0 > 0 and F(lo, Q) > F(1, 315) > old_upper,
            'explicit uniform separation from credited subset threshold')
    return {'actual_agent': 'six-downset-3', 'role': 'researcher',
            'status': 'PRIVATE exact finite author certificate; ordinary all-real proof separate',
            'original_B_masks': B, 'original_triple_indicator_all81': t,
            'original_star_masks': S, 'original_triple_weight_vector_all58': [str(x) for x in w],
            'original_BB_positions_checked': 6561, 'original_unordered_bad_edges': 2628,
            'all_original_edge_product_census': {'1': edge_counts[0], '1+lambda': edge_counts[1], '(1+lambda)^2': 0},
            'alpha_u_for_all_real_lambda_nonnegative': '1+lambda',
            'all9_comparison_triple_row_sums': [{'bad_mask': B[j], 'R': str(sum(old[j]))} for j in triples],
            'weighted_old_cap_lambda_coefficients': [str(x) for x in cap_coeff],
            'a_affine': [str(x) for x in a], 'b_affine': [str(x) for x in b],
            'F_lambda_constant_in_lambda_low_to_high_e': [str(x) for x in base],
            'F_lambda_linear_in_lambda_affine_e': [str(x) for x in linear],
            'F_lambda_quadratic_in_lambda': str(quadratic),
            'selected_lambda_affine': [str(x) for x in selected],
            'optimized_unnormalized_F_polynomial_low_to_high': [str(x) for x in Fpoly],
            'all_real_necessary_cost_curve': 'Delta>=max(0,F(e))/(2*(1+lambda(e))) for d<=e',
            'all_real_e_interval_for_cost_curve': ['0', '1/300'],
            'all_real_tau_interval': ['0', '1/256'],
            'full_endpoint_positivity_licence': signs, 'rational_samples': samples,
            'primitive_weighted_root_polynomial_low_to_high': primitive,
            'root_discriminant': str(disc), 'discriminant_is_nonsquare': True,
            'smaller_root_expression': '(-c1-sqrt(c1^2-4*c0*c2))/(2*c2)',
            'weighted_root_strict_coarse_cage': ['1/315', '1/314'],
            'weighted_root_strict_grid_cage': [str(F(lo, Q)), str(F(hi, Q))],
            'explicit_uniform_gap_above_subset_root': str(eta0),
            'credited_subset_root_strict_upper': str(old_upper),
            'normalized_cost_bound_or_ALL81_weight_radius_optimality_claimed': False,
            'full_original_optimizer_distance_optimality_or_root_attainment_claimed': False,
            'general_H_or_I_claimed': False, 'formal_proof': False, 'independent_review': False,
            'source_commit': None, 'graph_ref': None, 'new_graph_packet': None}


def main():
    result = record()
    if len(sys.argv) == 3 and sys.argv[1] == '--check':
        incoming = json.loads(Path(sys.argv[2]).read_text())
        # Specific mathematical gates precede whole-record equality so a
        # designated damaged certificate fails for its actual stated reason.
        for field, message in (
            ('original_triple_indicator_all81', 'certificate original weights'),
            ('all_original_edge_product_census', 'certificate original edge products'),
            ('weighted_old_cap_lambda_coefficients', 'certificate original weighted comparison cap'),
            ('selected_lambda_affine', 'certificate concave lambda optimizer'),
            ('optimized_unnormalized_F_polynomial_low_to_high', 'certificate exact weighted polynomial'),
            ('weighted_root_strict_coarse_cage', 'certificate exact root cage')):
            require(incoming.get(field) == result[field], message)
        require(incoming == result, 'whole weighted certificate')
        print(json.dumps({'status': 'WHOLE exact weighted certificate accepted', 'independent_review': False}))
    elif len(sys.argv) == 1:
        print(json.dumps(result, indent=2))
    else:
        raise ValueError('usage: weighted_radius.py [--check CERTIFICATE.json]')


if __name__ == '__main__':
    main()
