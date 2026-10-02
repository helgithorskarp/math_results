"""Exact audits of the uncentered row-defect/support bridge.

Actual agent six-downset-2, researcher. Arithmetic is standard-library
integer/Fraction arithmetic. Checks use exceptions and survive python -O.
The real PSD, cap, Cauchy and Chernoff bridges are written in PROOF.md;
finite fixtures do not prove their unbounded coverage.
"""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json
from math import comb, factorial
from pathlib import Path

from certificate import base, choose, forms, parameters, profiles, quadratic, require, scalar, certified_range
from defect import broad_tail, invariant_defect, norm_squared, positive_weight, predicted_pairing, residuals, row_profile, signed_pair_sum, small_tail, weight
from poly import FIRST, SECOND, P
from star_affine import check_stars, direct, rref, supported_pairs


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def symbolic(pair_damage=False, moment_damage=False):
    t, u = FIRST, SECOND
    F, G = 2*t*t+t+1, 2*u*u+u+1
    f, g = 2*t**3-t*t-1, 2*t**3+3*t*t+2*t+1
    require(f == (t-1)*F and g == (t+1)*F, 'Universal residual factorizations')
    fu, gu = f.substitute(u, 0), g.substitute(u, 0)
    require(f*fu-g*gu == -(2+int(pair_damage))*(t+u)*F*G, 'Universal positive proper-pair coefficient')
    require(F == 2*(t+Q(1, 4))**2+Q(7, 8), 'Strict coefficient positivity on every real t')
    rn, rm = 4*t**3-2*u*t*t, -4*t**3-2*u*t*t
    require(rn*rn+rm*rm == 2*(16*t**6+4*u*u*t**4), 'Paired odd/even norm cross cancellation')
    n = t
    sixth = n+15*n*(n-1)+15*n*(n-1)*(n-2)
    require(sixth == 15*n**3-30*n*n+(16+int(moment_damage))*n, 'Universal sixth Rademacher moment from even index partitions')
    require(n+3*n*(n-1) == 3*n*n-2*n, 'Universal fourth Rademacher moment')
    bound = 15*Q(21, 10)**6/256+3*Q(21, 10)**4/256+Q(27, 64)
    require(bound < Q(23, 4), 'Uniform normalized row-profile norm constant')
    require(2**63 > 1280*64**2, 'Stronger exponential margin base')
    require(2*n*n-(n+1)**2 == n*n-2*n-1, 'Stronger exponential margin induction polynomial')
    require(2-Q(1, 64)-Q(1, 256) > Q(63, 32), 'Small-tail stronger negative margin')
    require(Q(63, 32)**2/23 > Q(1, 6), 'Uniform actual-loop and RMS floor')
    exp7 = sum(Q(7, 10)**j/factorial(j) for j in range(5))
    exp6 = sum(Q(6, 5)**j/factorial(j) for j in range(4))
    require(exp7 > 2 and exp6 > 3, 'Rational logarithm bounds from positive Taylor terms')
    require(Q(6, 5)+21*Q(7, 10) < 16, 'Log(24*64^3)<64/4')
    return {'factorized_residual_numerators': [f.integers(), g.integers()],
            'positive_pair_identity': True, 'paired_norm_identity': True,
            'sixth_moment_coefficients': sixth.integers(),
            'bulk_and_tail_constant': str(bound), 'constant_strictly_less_than': '23/4',
            'stronger_margin': 'D>63*T/(32*n)', 'exponential_base_T64': 2**63,
            'exponential_base_1280_n_squared': 1280*64**2,
            'uniform_loop_and_rms_squared_floor': 'n/6',
            'exp_7_over_10_lower': str(exp7), 'exp_6_over_5_lower': str(exp6),
            'logarithm_base_upper': '159/10<16',
            'proof_mode': 'Universal coefficient identities, not interpolation'}


def finite(n, k, omit_row=False, wrong_orbit=False):
    pairs, recover = rref(n)
    values = [base(n)[a][b] for a, b in pairs]
    B = recover(values)
    require(B == direct(n, values) == base(n), 'Star-only RREF and separate singleton solver recover the credited base')
    p, q = profiles(n, k)
    f, g = residuals(n, k)
    r = row_profile(n, k)
    K, U = forms(n, B)
    cost = quadratic(K, p)+quadratic(U, q)
    require(cost == scalar(n, k), 'Independent physical base scalar')
    zero, positive = [], []
    for a, b in supported_pairs(n):
        w = weight(n, k, a, b)
        if a+b == n or min(a, b) <= k:
            require(w == 0, 'Every complement/active original pair cancels')
            zero.append((a, b))
        else:
            require(w == positive_weight(n, a, b) and w > 0, 'Every omitted proper original pair has strictly positive coefficient')
            positive.append((a, b, str(w)))
    noncentered, low_defect = 0, 0
    coefficients = []
    for i, (a, b) in enumerate(pairs):
        vv = list(values); vv[i] += 1
        BB = recover(vv)
        require(BB == direct(n, vv), 'Every star-only free direction, including all size-two directions')
        KK, UU = forms(n, BB)
        DK = [[x-K[ii][jj] for jj, x in enumerate(row)] for ii, row in enumerate(KK)]
        v, sigma = invariant_defect(n, BB)
        require(sum(comb(n, a)*a*v[a-1] for a in range(1, n-1)) == 0, 'Only the forced cardinality kernel is used')
        require(all(sum((j+1)*x for j, x in enumerate(row)) == 0 for row in DK), 'Physical star-only affine cardinality kernel')
        require(all(sum(row) == comb(n, a)*v[a-1] for a, row in enumerate(DK, 1)), 'Nonzero row sums retained')
        require(all(UU[ii][jj]-U[ii][jj] == -DK[ii][jj] for ii in range(n-2) for jj in range(n-2)), 'Lower/upper variation uses the same physical metric')
        actual = quadratic(KK, p)+quadratic(UU, q)
        pair = signed_pair_sum(n, k, BB)
        row = -Q(n*n-6, n*n)*sigma+sum(comb(n, a)*r[a-1]*v[a-1] for a in range(1, n-1))
        if all(v[a-1] == 0 for a in range(k+1, n-1)):
            require(row == Q(n*n-4, n*n)*sigma, 'Exact low-layer empty-defect specialization')
            low_defect += 1
        if omit_row:
            row = Q(0)
        require(actual == cost+pair+row == predicted_pairing(n, k, BB), 'Exact full-face noncentered support/row identity')
        residual = quadratic(DK, f)-quadratic(DK, g)
        require(residual == pair, 'Separate residual-shift pairing')
        if a+b < n and a > k:
            expected = (2-int(a == b))*comb(n, a)*choose(n-a, b)*weight(n, k, a, b)
            if wrong_orbit and a == b:
                expected *= 2
            require(pair == expected, 'Equal-size unordered original-orbit factor')
        else:
            require(pair == 0, 'Allowed star-only coordinate has zero pair term')
        noncentered += int(any(v))
        coefficients.append([a, b, str(pair), str(sigma), str(row)])
    require(noncentered > 0, 'This audit actually includes noncentered directions')
    return {'n': n, 'k': k, 'supported_coordinates': len(supported_pairs(n)),
            'star_only_rank': n-2, 'free_directions_checked': len(pairs),
            'noncentered_directions_checked': noncentered,
            'low_defect_directions_checked': low_defect,
            'zero_pair_orbits': len(zero), 'strictly_positive_pair_orbits': len(positive),
            'positive_coefficients': positive, 'direction_record_sha256': digest(coefficients),
            'center_equations_imposed': False, 'base_scalar': str(cost),
            'convention_audit_not_PSD_claim': True}


def make_original():
    n, k = 7, 2
    r, T, s, m = parameters(n)
    pairs, _ = rref(n)
    vv = [base(n)[a][b] for a, b in pairs]
    vv[pairs.index((2, 2))] += Q(1, 11)
    vv[pairs.index((3, 3))] += Q(2, 7)
    B = direct(n, vv)
    masks = [a for a in range(1, 1 << n) if a.bit_count() <= r]
    C = [[Q(s*int(i == j)-1)+B[a.bit_count()][b.bit_count()]*int(not(a&b))
          for j, b in enumerate(masks)] for i, a in enumerate(masks)]
    # A local four-point trade is not invariant under S_n. Its singleton,
    # singleton/two-set and two-set/two-set coefficients are 2,-1,1.
    # This credited sparse-trade mechanism preserves each original star.
    R = 15
    for i, a in enumerate(masks):
        for j, b in enumerate(masks):
            if not(a&b) and not(a&~R) and not(b&~R) and a.bit_count() <= 2 and b.bit_count() <= 2:
                z = 2 if a.bit_count()+b.bit_count() == 2 else -1 if a.bit_count()+b.bit_count() == 3 else 1
                C[i][j] += Q(z, 13)
    v = [sum(row) for row in C]
    sigma = sum(v)
    L = [[Q(1)+sigma]+[Q(1)-x for x in v]]+[[Q(1)-v[i]]+[x+1 for x in row] for i, row in enumerate(C)]
    require(len(masks) == m and L[0][0] != 1, 'Literal control has a genuine noncentered empty loop')
    return n, k, masks, C, L


def audit_original(n, k, masks, C, L, pair_scale=Q(1), metric_scale=Q(1)):
    _, T, s, m = parameters(n)
    N, h = m+1, T-1
    full = [0]+masks
    v, sigma = [sum(row) for row in C], sum(sum(row) for row in C)
    require(all(type(x) is Q for row in C+L for x in row), 'Literal exact rational input')
    require(all(L[i][j] == L[j][i] for i in range(N) for j in range(N)), 'Original symmetry')
    require(all(sum(row) == N for row in L), 'Full original regularity including the actual empty loop')
    require(L[0][0] == 1+sigma and all(L[0][i+1] == 1-v[i] for i in range(m)), 'Literal empty-row defect and actual loop')
    M = [[Q(L[i][j]-s*int(i == j), h) for j in range(N)] for i in range(N)]
    require(all(sum(row) == 1 for row in M), 'Normalized original M rows')
    require(all(M[i][j] == 0 for i, a in enumerate(full) for j, b in enumerate(full) if a&b), 'Every original intersection and nonempty loop')
    for point in range(n):
        star = [Q(int(bool(a&(1 << point)))) for a in masks]
        require(all(sum(x*y for x, y in zip(row, star)) == 0 for row in C), 'Every original star kernel without centering')
        full_star = [Q(0)]+star
        require(all(sum(x*y for x, y in zip(row, full_star)) == s for row in L), 'Every lifted star including the actual empty coordinate')
    require(sum(a.bit_count()*x for a, x in zip(masks, v)) == 0, 'Original defect perpendicular to cardinality')
    U = [[Q(N*int(i == j)-1)-C[i][j] for j in range(m)] for i in range(m)]
    p, q = profiles(n, k)
    pp, qq = [p[a.bit_count()-1] for a in masks], [q[a.bit_count()-1] for a in masks]
    pair = sum(2*weight(n, k, a.bit_count(), b.bit_count())*(C[i][j]+1)
               for i, a in enumerate(masks) for j, b in enumerate(masks) if i < j and not(a&b) and a.bit_count()+b.bit_count() < n and min(a.bit_count(), b.bit_count()) > k)
    row = -Q(n*n-6, n*n)*sigma+sum(row_profile(n, k)[a.bit_count()-1]*x for a, x in zip(masks, v))
    require(quadratic(C, pp)+quadratic(U, qq) == scalar(n, k)+pair_scale*pair+row, 'Original noninvariant support/empty-row identity')
    # E^T z=x and z perpendicular to the full constant vector; both
    # physical pairings are checked against the FULL original lift.
    for x, A, full_A in [(pp, C, L), (qq, U, [[Q(N*int(i == j))-L[i][j] for j in range(N)] for i in range(N)])]:
        mean = sum(x)/N
        z = [-mean]+[u-mean for u in x]
        require(metric_scale*quadratic(A, x) == quadratic(full_A, z), 'Full-lift physical restriction has no extra factor two')
    require(sum(row_profile(n, k)[a.bit_count()-1]**2 for a in masks) == norm_squared(n, k), 'Original Euclidean norm uses binomial physical weights')
    require((L[0][0]-1)**2+sum((L[0][i+1]-1)**2 for i in range(m)) == sigma*sigma+sum(x*x for x in v), 'Original empty-column square identity used by the cap bridge')
    require(C[masks.index(1)][masks.index(2)] != C[masks.index(16)][masks.index(32)], 'Literal fixture is genuinely noninvariant')
    return {'n': n, 'k': k, 'full_order': N, 'nonempty_order': m,
            'point_stars_checked': n, 'noninvariant': True, 'noncentered': True,
            'actual_empty_M_loop': str(M[0][0]), 'sigma': str(sigma),
            'squared_empty_row_defect': str(sum(x*x for x in v)),
            'signed_original_pair_sum': str(pair), 'row_correction': str(row),
            'lower_upper_pairing': str(quadratic(C, pp)+quadratic(U, qq)),
            'convention_audit_not_PSD_claim': True}


def literal(damage=None):
    n, k, masks, C, L = make_original()
    if damage == 'loop':
        L[0][0] += 1
    if damage == 'center':
        L[0] = [Q(1)]*len(L)
        for row in L:
            row[0] = Q(1)
    if damage == 'support':
        L[1][1] += 1
    return audit_original(n, k, masks, C, L,
                          pair_scale=Q(2) if damage == 'pair' else Q(1),
                          metric_scale=Q(2) if damage == 'metric' else Q(1))


def tails():
    rows = []
    for n in (64, 128, 256):
        k = max(k for k in range(2, (n-1)//2+1) if small_tail(n, k))
        mass, T = sum(comb(n, a) for a in range(k+1)), 2**(n-1)
        require(small_tail(n, k) and not small_tail(n, k+1), 'Largest exact small-tail cutoff')
        require(certified_range(n, k), 'Small-tail criterion implies inherited 9201 margin criterion')
        D, Qr = -scalar(n, k), norm_squared(n, k)
        require(D > Q(63*T, 32*n) and Qr < Q(23*T, 2*n**3), 'Exact representative stronger scalar and row-norm bounds')
        exact_loop_floor = D*D/((2*T-n-1)*Qr)
        exact_rms_floor = D*D/((2*T-n-2)*Qr)
        require(exact_loop_floor > Q(n, 6) and exact_rms_floor > Q(n, 6), 'Exact quantitative noncentering bounds in representative orders')
        moments = []
        for degree, formula in [(4, 3*n*n-2*n), (6, 15*n**3-30*n*n+16*n)]:
            actual = sum(comb(n, a)*(2*a-n)**degree for a in range(n+1))
            require(actual == 2*T*formula, 'Direct binomial moment convention check')
            moments.append([degree, actual])
        rows.append({'n': n, 'k': k, 'minimum_positive_coupling_size_if_small_defect': k+1,
                     'binomial_tail_0_to_k': mass, 'D': str(D), 'row_profile_norm_squared': str(Qr),
                     'exact_loop_floor': str(exact_loop_floor), 'exact_rms_squared_floor': str(exact_rms_floor),
                     'uniform_floor': str(Q(n, 6)), 'exact_moment_checks': moments})
    return rows


def broad_cutoffs():
    rows = []
    for n in (64, 128, 256):
        k = max(k for k in range(2, (n-1)//2+1) if broad_tail(n, k))
        require(broad_tail(n, k) and not broad_tail(n, k+1), 'Largest factor-two sufficient cutoff, credited reviewer3')
        D = -scalar(n, k)
        require(D > Q(2**(n-1), 4*n), 'Representative broader-cutoff margin, not the unbounded proof bridge')
        rows.append({'n':n,'k':k,'positive_centered_coupling_minimum_size':k+1,'D':str(D),
                     'scope':'Tradeoff applies to all real capped H; positive-coupling conclusion here requires zero defect',
                     'cutoff_credit':'six-reviewer-3 factor-two criterion, published source3014cab3c0ec44ad5ba90448604ada49ae6b51b6'})
    return rows


def rejected(function):
    try:
        function()
    except (ValueError, IndexError):
        return True
    return False


def controls():
    tests = [('wrong positive-pair coefficient', lambda: symbolic(pair_damage=True)),
             ('wrong sixth moment', lambda: symbolic(moment_damage=True)),
             ('omit the noncentered row term', lambda: finite(7, 2, omit_row=True)),
             ('double equal-size unordered orbit', lambda: finite(7, 2, wrong_orbit=True)),
             ('changed actual empty loop', lambda: literal('loop')),
             ('force the actual empty row to ones', lambda: literal('center')),
             ('forbidden nonempty diagonal', lambda: literal('support')),
             ('double unordered original pair term', lambda: literal('pair')),
             ('wrong full physical metric', lambda: literal('metric')),
             ('oversized star-only RREF', lambda: rref(64)),
             ('floating star-only input', lambda: direct(7, [0.0]*6))]
    for label, function in tests:
        require(rejected(function), 'Damage rejected: '+label)
    return [label for label, _ in tests]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = {'agent': 'six-downset-2', 'role': 'researcher',
              'claim': 'Quantitative original empty-row-defect/support tradeoff for real capped near-cube H, without centering',
              'scope': 'Every integer n>=64; exact signed cut for every 2<=k<n/2 with2*n^2*sum_{a=3}^k binom(n,a)<=2^(n-1), using the credited reviewer3 broader cutoff; uniform noncentering floor with12*n^3*sum_{a=0}^k binom(n,a)<=2^(n-1)',
              'proof_status': 'Exact rational/coefficient audits; ordinary real PSD/Cauchy/Chernoff bridges unformalized; independently unreviewed',
              'inherited_margin_source': 'Committed LEMMA9201, source fcb0fb77ae128c82bd3d684ba5ca7c5714f15c5c',
              'universal': symbolic(), 'star_only_affine': [finite(7, 2), finite(8, 3), finite(17, 3), finite(20, 4)],
              'literal': literal(), 'exact_tail_examples': tails(), 'credited_broader_cutoff_examples':broad_cutoffs(), 'rejected_controls': controls(),
              'arithmetic': 'CPython integers/fractions.Fraction; no solver or floating arithmetic',
              'no_large_original_matrix_allocated': True}
    body = json.dumps(result, indent=2, sort_keys=True)+'\n'
    if args.check:
        require(body == args.check.read_text(), 'Entire frozen record mismatch')
    if args.output:
        args.output.write_text(body)
    print(json.dumps({'ok': True, 'result_sha256': sha256(body.encode()).hexdigest(),
                      'star_only_free_directions_checked': sum(v['free_directions_checked'] for v in result['star_only_affine']),
                      'noncentered_directions_checked': sum(v['noncentered_directions_checked'] for v in result['star_only_affine']),
                      'literal_full_order': result['literal']['full_order'], 'uniform_minimum_n': 64,
                      'exact_tail_minimum_positive_sizes': [[v['n'], v['minimum_positive_coupling_size_if_small_defect']] for v in result['exact_tail_examples']],
                      'controls': len(result['rejected_controls'])}, sort_keys=True))


if __name__ == '__main__':
    main()
