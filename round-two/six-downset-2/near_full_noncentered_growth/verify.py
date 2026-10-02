"""Exact validation of the written unbounded theorem, using stdlib only.

Finite controls are not an all-n completeness bridge or PSD constructions.
"""
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path
import argparse, hashlib, json
import affine, certificate as c
from model import parameters, physical, quadratic, require


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def evaluate(n, k, B):
    aa, lower, upper, mu = c.tests(n, k)
    a, F = physical(n, B)
    b, U = physical(n, B, True)
    require(a == b == aa, 'Physical test layer order')
    return quadratic(U, upper) + mu * quadratic(F, lower)


def affine_controls(n, k):
    pairs = [p for p in affine.supported_pairs(n) if p[0] >= 2]
    free, recover = affine.rref(n)
    require(pairs == free, 'Independent RREF coordinates')
    N, s, h = parameters(n)
    base = [Q(s-1) if a+b == n else Q(0) for a, b in pairs]
    B = affine.direct(n, base)
    require(B == recover(base), 'Independent base completion')
    anchor = evaluate(n, k, B)
    require(anchor == c.identity_rhs(n, k, B), 'Full-face anchor identity')
    v, mu, f, deficit = c.profile(n, k)
    rho = c.weights(n, k)
    coefficients = []
    for i, (a, b) in enumerate(pairs):
        values = base.copy()
        values[i] += 1
        T = affine.direct(n, values)
        require(T == recover(values), 'Independent direction completion')
        change = evaluate(n, k, T) - anchor
        require(evaluate(n, k, T) == c.identity_rhs(n, k, T), 'Full-face directional identity')
        if a <= k:
            expected = Q(0)
        elif a+b == n:
            expected = 2*c.pair_count(n, a, b)*deficit[a]
        else:
            expected = 2*c.pair_count(n, a, b)*mu*rho[a, b]
        require(change == expected, 'Every original class coefficient, including low cancellations')
        coefficients.append([[a, b], str(change)])
    values = [v+Q((-1)**i*(i+1), 13) for i, v in enumerate(base)]
    T = affine.direct(n, values)
    require(T == recover(values), 'Independent signed completion')
    require(evaluate(n, k, T) == c.identity_rhs(n, k, T), 'Signed full-face identity')
    return {'n': n, 'k': k, 'directions': len(pairs),
            'coefficients_sha256': digest(coefficients),
            'low_cancellations': sum(a <= k for a, b in pairs),
            'positive_proper_classes': len(rho)}


def independently_count_constant(n, k, roots):
    """Literal layer norms, with no closed constant formula supplied."""
    N, s, h = parameters(n)
    aa, lower, upper, mu = c.tests(n, k)
    upper = dict(zip(aa, upper))
    for a, r in roots.items():
        upper[n-a] = r
    shifted = {a: upper[a]-a for a in aa}
    total = sum(comb(n, a)*upper[a] for a in aa)
    cardinality_total = sum(comb(n, a)*a for a in aa)
    require(cardinality_total == n*s, 'Actual counted cardinality total')
    upper_norm = sum(comb(n, a)*upper[a]**2 for a in aa)
    shifted_norm = sum(comb(n, a)*shifted[a]**2 for a in aa)
    complement = sum(comb(n, a)*shifted[a]*shifted[n-a] for a in range(k+1, n-k))
    return N*upper_norm-total**2-s*(shifted_norm+complement)+(total-cardinality_total)**2


def scalar_controls(n, k):
    rec = c.constant(n, k)
    tail = c.tail_condition(n, k)
    v, mu, f, deficit = c.profile(n, k)
    s, h = rec['s'], rec['h']
    roots = {a: Q(s*a, h) for a in range(2, k+1)}
    require(independently_count_constant(n, k, roots) == rec['upper_constant'], 'Counted general-k constant')
    changed = {a: r+Q((-1)**a*(a+1), 17) for a, r in roots.items()}
    excess = h*sum(comb(n, a)*(changed[a]-roots[a])**2 for a in roots)
    require(independently_count_constant(n, k, changed) == rec['upper_constant']+excess,
            'Exact independent high-root square completion')
    base = c.constant(n, 2)
    alpha = Q(h)-Q(s*s, h)
    require(rec['eta']-base['eta'] == alpha*tail['B']+(n-1)*(rec['bulk_norm2']-base['bulk_norm2']),
            'Exact k2 to general-k difference')
    require(0 < alpha < 2*(n-1) and rec['bulk_norm2'] <= base['bulk_norm2'], 'Tail multiplier and clipping')
    if n >= 12:
        require(tail['D'] > 0, 'Finite control of written positive-tail induction')
        require(c.k2_tail_bound(n) < -Q(n, 3)*tail['D'], 'Finite tail dominance control')
        require(rec['eta'] <= c.k2_tail_bound(n)+2*(n-1)*tail['B'], 'General tail upper bound')
    if tail['holds']:
        require(rec['eta'] < -Q(tail['D'], 3), 'Strict sufficient-criterion margin')
        require(rec['positive_mass_floor'] > Q(tail['D'], 6*h*mu), 'Explicit positive mass margin')
        if n >= 16:
            require(rec['positive_mass_floor'] > Q(1, 2*n*n), 'Simplified positive original mass floor')
    weights = c.weights(n, k)
    count = sum(c.pair_count(n, a, b) for a, b in weights)
    low = sum(comb(n, a)*2**(n-a) for a in range(k+1))
    both = sum(comb(n, a)*comb(n-a, b) for a in range(k+1) for b in range(k+1))
    complement_count = 2**n-2*sum(comb(n, a) for a in range(k+1))
    require(2*count == 3**n-2*low+both-complement_count,
            'Independent ternary-assignment proper original pair count')
    return {**{key: str(value) if type(value) is Q else value for key, value in rec.items()},
            'tail_condition': tail, 'proper_unordered_pairs': count,
            'weights': len(weights),
            'minimum_weight': str(min(weights.values())) if weights else None,
            'maximum_weight': str(max(weights.values())) if weights else None,
            'profile_sha256': digest({str(a): str(v[a]) for a in v})}


def literal_control(n, cutoffs):
    N, s, h = parameters(n)
    pairs = [p for p in affine.supported_pairs(n) if p[0] >= 2]
    values = [Q(s-1) if a+b == n else Q((-1)**(a+b), 17) for a, b in pairs]
    B = affine.direct(n, values)
    masks = [a for a in range(1, 2**n) if a.bit_count() <= n-2]
    sizes = [a.bit_count() for a in masks]
    m = len(masks)
    C = [[Q(s*int(i == j)-1)+(B[sizes[i]][sizes[j]] if not a&b else 0)
          for j, b in enumerate(masks)] for i, a in enumerate(masks)]
    require(m+1 == N, 'Actual domain including empty')
    sums = [sum(row) for row in C]
    empty = [1-v for v in sums]
    loop = 1+sum(sums)
    L = [[loop]+empty]+[[empty[i]]+[v+1 for v in row] for i, row in enumerate(C)]
    require(all(sum(row) == N for row in L), 'Actual full rows including empty loop')
    require(all(L[i+1][i+1] == s for i in range(m)), 'Actual nonempty diagonals')
    require(all(L[i+1][j+1] == 0 for i, a in enumerate(masks) for j, b in enumerate(masks)
                if i != j and a&b), 'Actual intersecting support')
    for p in range(n):
        star = [int(bool(a&(1 << p))) for a in masks]
        require(sum(star) == s, 'Actual star count')
        require(all(sum(v*z for v, z in zip(row, star)) == 0 for row in C), 'Every actual star kernel')
    U = [[Q(N*int(i == j))-L[i+1][j+1] for j in range(m)] for i in range(m)]
    identities = []
    for k in cutoffs:
        aa, lower, upper, mu = c.tests(n, k)
        lv, uv = [lower[a-1] for a in sizes], [upper[a-1] for a in sizes]
        result = quadratic(U, uv)+mu*quadratic(C, lv)
        require(result == evaluate(n, k, B) == c.identity_rhs(n, k, B), 'Literal original general-k identity')
        identities.append({'k': k, 'identity': str(result)})
    require(sum(empty) != N, 'Replacing the actual empty loop by zero fails the original row equation')
    return {'n': n, 'original_order': N, 'checked_original_entries': N*N, 'identities': identities,
            'scope': 'Affine identity/rows/support/stars only; no PSD or cap feasibility assertion'}


def noninvariant_control():
    n, k = 16, 3
    aa, lower, upper, mu = c.tests(n, k)
    rho = c.weights(n, k)
    mask = lambda pts: sum(1 << p for p in pts)
    left = {mask(range(0, 4)): 1, mask(range(4, 8)): 1,
            mask(range(0, 3)): -1, mask(range(3, 8)): -1}
    right = {mask(range(8, 12)): 1, mask(range(12, 16)): 1,
             mask(range(8, 11)): -1, mask(range(11, 16)): -1}
    for trade in (left, right):
        require(sum(trade.values()) == 0, 'Trade has zero row sum')
        require(all(sum(z for a, z in trade.items() if a&(1 << p)) == 0 for p in range(n)),
                'Trade annihilates each individual actual point star')
    score = lambda trade, vec: sum(z*vec[a.bit_count()-1] for a, z in trade.items())
    result = 2*mu*score(left, lower)*score(right, lower)-2*score(left, upper)*score(right, upper)
    rhs, positions, omitted = Q(0), 0, 0
    for a, x in left.items():
        for b, y in right.items():
            require(not a&b and a.bit_count()+b.bit_count() < n, 'Allowed proper original pair')
            positions += 2
            sa, sb = sorted((a.bit_count(), b.bit_count()))
            if sa > k:
                rhs += 2*mu*rho[sa, sb]*x*y
                omitted += 1
    require(rhs == result == Q(9063, 128), 'Nonzero noninvariant original identity')
    return {'n': n, 'k': k, 'changed_ordered_positions': positions,
            'omitted_unordered_pairs': omitted, 'exact_scalar_change': str(result),
            'scope': 'Signed affine trade; no PSD or cap feasibility assertion'}


def analytic_controls():
    # The written counted-moment, induction and Chernoff proofs supply all-n coverage.
    moments = []
    for n in (12, 16, 24, 32, 64, 128, 256, 512):
        m2 = sum(Q(comb(n, a)*(2*a-n)**2, 4) for a in range(n+1))
        m4 = sum(Q(comb(n, a)*(2*a-n)**4, 16) for a in range(n+1))
        require(m2 == Q(2**n*n, 4) and m4 == Q(2**n*(3*n*n-2*n), 16), 'Counted binomial moments')
        full = sum(comb(n, a)*(Q(5, 4)-Q((2*a-n)**2, 4*n))**2 for a in range(n+1))
        N, s, h = parameters(n)
        require(full == (s+n)*(Q(9, 4)-Q(1, 4*n)), 'Whole clipped-square majorant')
        base = c.constant(n, 2)
        bound = n*h+comb(n, 2)*(8*h-10*s)+(n-1)*full+base['mu']*(4*s-4)
        require(bound == c.k2_tail_bound(n) and base['eta'] <= bound, 'Whole scalar tail expansion')
        if n >= 16:
            require(2**(n-3)-n-12*n*n > 0, 'Finite three-quarter-exponential tail control')
        moments.append({'n': n, 'moment2': str(m2), 'moment4': str(m4)})
    for t in (0, 1, 2, 7):
        n = 12+t
        require(12*n*n-23*n-13 == 12*t*t+265*t+1439, 'D-positive induction polynomial')
        require(5*n*n-45*n-3 == 5*t*t+75*t+177, 'Linear dominance polynomial')
        require(23*n*n-22*n+24 == 23*t*t+530*t+3072, 'Cubic remainder polynomial')
        n = 16+t
        require(12*n*n-23*n-13 == 12*t*t+361*t+2691, 'Three-quarter tail induction polynomial')
    require(2**(16-3)-16-12*16*16 == 5104, 'Three-quarter induction base')
    require(sum(Q(1, factorial(j)) for j in range(4)) == Q(8, 3), 'Strict exponential lower-series base')
    require(Q(8, 3)**8 > 2304, 'Exact n24 logarithm endpoint witness')
    require(Q(1, 2)-Q(2, 24)-Q(8, 24**2) == Q(29, 72), 'Positive endpoint derivative margin')
    require(all(factorial(2*j) >= 2**j*factorial(j) for j in range(12)), 'Finite cosh coefficient controls')
    return {'moments': moments, 'tail_start': 12, 'D_base': 308,
            'induction_coefficients': [1439, 265, 12],
            'linear_dominance_coefficients': [177, 75, 5],
            'remainder_dominance_coefficients': [3072, 530, 23],
            'three_quarter_tail_start': 16, 'three_quarter_base': 5104,
            'three_quarter_induction_coefficients': [2691, 361, 12],
            'growth_start': 24, 'logarithm_constant': 4,
            'log_endpoint_rational_witness': str(Q(8, 3)**8),
            'derivative_margin': '29/72', 'all_finite_controls_exact': True}


def cutoff_controls(n):
    k = c.certified_cutoff(n)
    tail = c.tail_condition(n, k)
    require(tail['holds'], 'Chosen integer cutoff satisfies the sufficient criterion')
    require(k+1 <= (n-2)//2 and not c.tail_condition(n, k+1)['holds'], 'Next integer fails this criterion only')
    return {'n': n, 'cutoff': k, 'forced_minimum_integer_size': k+1,
            'next_fails_this_sufficient_criterion_only': True, 'scalar': scalar_controls(n, k)}


def run():
    cases = [(6, 2), (7, 2), (8, 2), (8, 3), (10, 2), (10, 3), (10, 4), (11, 2), (11, 4),
             (12, 2), (12, 3), (12, 4), (12, 5), (16, 3), (16, 4), (16, 7), (20, 4), (20, 7), (20, 9)]
    return {'agent': 'six-downset-2', 'role': 'researcher',
            'proof_status': 'Ordinary author proof, unformalized and independently unreviewed',
            'theorem_domain': 'Every real original capped near-cube H; no centering; all n>=24 growth corollary',
            'affine_controls': [affine_controls(n, k) for n, k in cases],
            'scalar_controls': [scalar_controls(n, k) for n, k in cases],
            'literal_controls': [literal_control(6, (2,)), literal_control(8, (2, 3))],
            'noninvariant_control': noninvariant_control(), 'analytic_controls': analytic_controls(),
            'cutoff_controls': [cutoff_controls(n) for n in (24, 32, 64, 128, 256, 512)],
            'no_finite_computation_substituted_for_unbounded_coverage': True,
            'no_solver_or_floating_point_input': True}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--check', type=Path)
    args = p.parse_args()
    result = run()
    raw = json.dumps(result, sort_keys=True, separators=(',', ':'))+'\n'
    if args.check:
        require(args.check.read_bytes() == raw.encode(), 'Complete frozen record mismatch')
        print(json.dumps({'ok': True, 'record_sha256': hashlib.sha256(raw.encode()).hexdigest(),
                          'affine_directions': sum(r['directions'] for r in result['affine_controls']),
                          'literal_original_entries': sum(r['checked_original_entries'] for r in result['literal_controls']),
                          'growth_start': 24, 'logarithm_constant': 4,
                          'no_centering': True, 'positive_original_entries_and_mass': True}))
    else:
        print(raw, end='')
