"""exact original-row radius deduction for the public q18 witness.

Only attributed defining CANDIDATE/COMPARISON DATA are read. The canonical
mask/coefficient decoding is openly adapted from our public q18 source.
No ancestor executable, original-candidate PSD factor or numerical solver
runs. The ordinary all-real/kernel/convex-relaxation bridges are in PROOF.md.
"""
from fractions import Fraction as F
from itertools import combinations
from math import gcd, isqrt, lcm
from pathlib import Path
import hashlib
import json


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read_data(root, name, digest):
    raw = (root/name).read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest, 'whole attributed public DATA: '+name)
    return json.loads(raw)


def decode():
    root = Path(__file__).resolve().parent
    candidate = read_data(root, 'CANDIDATE.json',
                          'fae303f40a542478e22083289ea982cd1814b58323f4e13d237d7269583ab16e')
    comparison = read_data(root, 'COMPARISON.json',
                           '6770d9db69983e4cbd75480a9f784dd4c9c9d254cf7f455bbd0d4a62633b2ca2')
    D = candidate['denominator'];Dold = comparison['comparison_free_denominator']
    require(D == 2**32 and Dold == 16384, 'named exact coefficient scales')
    X = []
    for rank in (1, 2, 3):
        for points in combinations(range(21), rank):
            m = sum(1 << p for p in points)
            if rank == 3 and ((m & 7).bit_count() < 2 or
                              ((m & 7) == 6 and (m & (511 << 3)))):
                continue
            X.append(m)
    X.sort()
    orbit = {m: (m & 7, ((m >> 3) & 511).bit_count(), (m >> 12).bit_count()) for m in X}
    S = [m for m in X if m & 1]
    bad_types = {(0, 2, 0), (0, 0, 2), (6, 0, 1)}
    B = [m for m in X if orbit[m] in bad_types]
    require((len(X), len(S), len(B)) == (277, 58, 81), 'whole original carrier/counts')
    keys = sorted({tuple(sorted((orbit[m], orbit[n])))
                   for i, m in enumerate(X) for n in X[i+1:]
                   if m != 1 and n != 1 and not (m & n)})
    require(len(keys) == 143 == len(candidate['free_numerators']) ==
            len(comparison['comparison_free_numerators']), 'whole original canonical free coefficient order')
    newtable = dict(zip(keys, candidate['free_numerators']))
    oldtable = dict(zip(keys, comparison['comparison_free_numerators']))
    def entry(m, n, table, d):
        if m == n:
            return 57*d
        if m & n:
            return -d
        if m == 1:
            return -sum(entry(s, n, table, d) for s in S if s != 1)
        if n == 1:
            return entry(n, m, table, d)
        return table[tuple(sorted((orbit[m], orbit[n])))]
    values = [sum(entry(s, b, newtable, D) for b in B) for s in S]
    degrees = [sum(not (s & b) for b in B) for s in S]
    require(sum(values) == 0, 'ALL58 original aggregate coordinates have zero sum')
    require({k: degrees.count(k) for k in set(degrees)} == {64: 36, 72: 12, 73: 9, 81: 1},
            'ALL58 literal original disjoint bad-neighbor counts')
    cap = F(sum(entry(a, b, oldtable, Dold) for a in B for b in B), Dold)
    require(cap == F(4998177, 1024), 'ALL81-by81 old comparison cap positions')
    return S, values, D, degrees, cap


def check(decoded=None):
    masks, values, D, degrees, cap = decode() if decoded is None else decoded
    v = [F(x, D) for x in values];k = [220*d for d in degrees]
    P = [i for i, x in enumerate(v) if x > 0]
    N = [i for i, x in enumerate(v) if x < 0]
    require(len(P) == 20 and len(N) == 38, 'ENTIRE nonzero signed partition of58 original coordinates')
    m = len(N);V = sum(v[i] for i in P);K = sum(k[i] for i in P)
    require(V == F(2912214312567, 1073741824) and K == 320760,
            'NEW complete original positive-part sums')
    energy = [sum(v[i]**2 for i in P)+V*V/m,
              -2*(sum(v[i]*k[i] for i in P)+V*K/m),
              sum(F(k[i])**2 for i in P)+F(K*K, m)]
    gap = [(energy[0]-58*cap)/116, energy[1]/116, energy[2]/116]
    def polynomial(c, e):
        return c[0]+c[1]*e+c[2]*e*e
    r0 = F(1, 600);r1 = F(1, 400)
    require(all(v[i]-k[i]*r1 > 0 for i in P), 'ENTIRE real radius interval keeps all20 positive lower bounds')
    require(gap[0] > 0 and gap[1]+2*gap[2]*r1 < 0,
            'ENTIRE real radius interval has strictly decreasing necessary quadratic')
    projection_checks = 0
    # Affine endpoint comparisons pay EVERY constraint for the full real window.
    for e in (r0, r1):
        q = [(v[i]-k[i]*e) if i in P else -(V-K*e)/m for i in range(58)]
        require(sum(q) == 0 and sum(x*x for x in q) == polynomial(energy, e),
                'NEW full original zero-sum primal energy equality')
        for i in range(58):
            require(v[i]-k[i]*e <= q[i] <= v[i]+k[i]*e,
                    'EVERY literal original coordinate of the minimizing full box vector')
            projection_checks += 1
    require(projection_checks == 116, 'ALL58 lower/upper original-coordinate endpoint checks paid')
    a = F(1, 408);b = F(1, 407)
    require(r0 < a < b < r1 and polynomial(gap, a) > 1 and polynomial(gap, b) < 0,
            'NEW exact strict real-root isolation in original M-entry units')
    common = lcm(*(x.denominator for x in gap))
    primitive = [int(x*common) for x in gap]
    divisor = gcd(gcd(abs(primitive[0]), abs(primitive[1])), abs(primitive[2]))
    primitive = [x//divisor for x in primitive]
    c0, c1, c2 = primitive
    discriminant = c1*c1-4*c0*c2
    require(c0 > 0 and c1 < 0 and c2 > 0 and discriminant > 0 and
            isqrt(discriminant)**2 != discriminant, 'NEW positive irrational quadratic threshold')
    samples = []
    for radius, lower in [(F(1, 1280), 1500), (F(1, 640), 750),
                          (F(1, 500), 380), (F(1, 420), 50), (a, 1)]:
        g = polynomial(gap, radius)
        require(g > lower, 'NEW exact necessary near-optimal radius exclusion')
        samples.append({'original_S_B_entry_radius': str(radius), 'Gamma': str(g),
                        'strict_clean_gap_lower': lower})
    return {
        'actual_agent': 'six-downset-3', 'role': 'researcher',
        'status': 'complete ordinary author proof; unformalized and independently unreviewed',
        'published_witness_source_commit': '782bc9042896c0f3887b1807dbd991f75fa13c9b',
        'original_carrier_N_s_B': [278, 58, 81],
        'original_star_masks': masks, 'all_one_vector_denominator': D,
        'complete_original58_vector_numerators': values,
        'complete_original58_allowed_bad_neighbor_counts': degrees,
        'allowed_original_S_B_positions': sum(degrees),
        'positive_star_positions': P, 'negative_star_positions': N,
        'positive_coordinate_sum': str(V), 'positive_original_entry_slope_sum': K,
        'old_all_one_BB_cap': str(cap),
        'necessary_energy_coefficients_low_to_high': [str(x) for x in energy],
        'Gamma_coefficients_low_to_high': [str(x) for x in gap],
        'full_real_Gamma_radius_interval': ['0', '1/400'],
        'exact_box_projection_real_window': ['1/600', '1/400'],
        'new_complete_box_endpoint_coordinate_checks': projection_checks,
        'primitive_threshold_polynomial_low_to_high': primitive,
        'threshold_expression': '(-c1-sqrt(c1^2-4*c0*c2))/(2*c2)',
        'threshold_strict_rational_isolation': ['1/408', '1/407'],
        'complete_relaxation_classification': 'original58-coordinate box + zero sum + scalar Schur optimizer-energy bound is feasible iff real radius e>=threshold, for all e>=0',
        'original_NS_optimizer_entry_movement_clean_strict_lower': '1/408',
        'near_optimal_deductions': samples,
        'full_real_tau_interval': ['0', '1/256'],
        'original_matrix_or_NS_fiber_realization_or_best_original_distance_claimed': False,
        'ancestor_executable_or_PSD_factor_or_numerical_package_replayed': False,
        'independent_review_claimed': False,
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
