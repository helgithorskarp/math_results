"""Exact sufficient guards from PROOF.md. No floating point or quadrature."""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rational(x):
    need(isinstance(x, (int, F)) and not isinstance(x, bool), 'exact rational required')
    return F(x)


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def dyadic_exponent(x):
    """Smallest nonnegative e with 2^-e <= x, for x>0."""
    need(x > 0, 'positive bound required')
    e = max(0, x.denominator.bit_length()-x.numerator.bit_length())
    while F(1, 2**e) > x:
        e += 1
    while e and F(1, 2**(e-1)) <= x:
        e -= 1
    return e


def constants(radius, kappa, threshold, weight):
    R, k, t, w = map(rational, (radius, kappa, threshold, weight))
    need(R > 0 and k > 0 and 0 < t <= 1 and 0 < w <= 1, 'parameter domain')
    K0, L, K1, K2 = 2*R*R/k, 96*R**3/k+6*R, 16*R/k, 2*R/t**2
    c = w*w*min(t/4, F(1, 16))
    delta = c/(4*K1)
    bounds = {
        'global_alignment': k*k/(4*R*R*K0),
        'core_mass': delta**2/(2*K0),
        'core_covariance': k*delta**2/(8*R*R*K0),
        'rare_posterior': w**4*k*k*delta**2/(144*R**4*K0),
        'rare_loss': 2*k*delta/R,
        'core_quadratic': c*delta**4/(8*L*L*K0*K0),
        'cross_error': c*c*delta**4/(64*K2*K2*K0**3),
    }
    return {'R': R, 'kappa': k, 't': t, 'w': w, 'K0': K0, 'L': L,
            'K1': K1, 'K2': K2, 'c0': c, 'delta': delta,
            'bounds': bounds, 'cutoff': min(bounds.values())}


def rational_schedule(radius, kappa, threshold_exponent):
    """All-radius schedule for u>=2^-m, with elementary exponential bounds.

    log(2)<3/4, J^2>=3m/2, e<3 make B=R+J and
    w=3^-ceil((B+R)^2/2) valid. No transcendental library is trusted.
    """
    R, k = map(rational, (radius, kappa))
    m = threshold_exponent
    need(isinstance(m, int) and not isinstance(m, bool) and m >= 1, 'integer m>=1')
    J = isqrt((3*m+1)//2)
    if 2*J*J < 3*m:
        J += 1
    B = R+J
    n = ceil_fraction((B+R)**2/2)
    out = constants(R, k, F(1, 2**m), F(1, 3**n))
    out.update({'m': m, 'J': J, 'B': B, 'exponential_ceiling': n,
                'cutoff_exponent': dyadic_exponent(out['cutoff'])})
    return out


def audit_cutoff(c, d):
    """Check the actual inequalities used in assembly, including square roots
    by squaring nonnegative rational quantities. Reject outside the schedule.
    """
    d = rational(d)
    need(0 < d <= c['cutoff'], 'loss outside sufficient schedule')
    R, k, w, delta = (c[n] for n in ('R', 'kappa', 'w', 'delta'))
    K0, L, K1, K2, c0 = (c[n] for n in ('K0', 'L', 'K1', 'K2', 'c0'))
    M, alpha = K0*d, K0*d/delta**2
    need(R*R*M <= k*k/4, 'global alignment budget')
    need(alpha <= F(1, 2) and alpha <= k/(8*R*R), 'conditional covariance budget')
    need(M <= w**4*k*k*delta*delta/(144*R**4), 'rare posterior budget')
    need(d <= 2*k*delta/R, 'rare pair-loss budget')
    need(K1*delta <= c0/4, 'core linear budget')
    need(L*L*alpha*alpha <= c0*d/8, 'core quadratic budget')
    need((K2*alpha)**2*M <= (c0*d/8)**2, 'cross square-root budget')
    return True


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def center(xs, p):
    m = tuple(sum((pi*x[j] for pi, x in zip(p, xs)), F(0)) for j in range(3))
    return [sub(x, m) for x in xs]


def cross(xs, ys, p):
    return [[sum((pi*x[i]*y[j] for pi, x, y in zip(p, xs, ys)), F(0))
             for j in range(3)] for i in range(3)]


def det(a):
    if not a:
        return F(1)
    return sum(((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]])
                for j in range(len(a))), F(0))


def psd(a):
    if any(a[i][j] != a[j][i] for i in range(3) for j in range(3)):
        return False
    return all(det([[a[i][j] for j in ix] for i in ix]) >= 0
               for n in (1, 2, 3) for ix in combinations(range(3), n))


def pair_losses(xs, ys, p):
    losses = [[norm2(sub(x, xp))-norm2(sub(y, yp))
               for xp, yp in zip(xs, ys)] for x, y in zip(xs, ys)]
    need(all(v >= 0 for row in losses for v in row), 'not a contraction')
    d = sum((p[i]*p[j]*v for i, row in enumerate(losses)
             for j, v in enumerate(row)), F(0))
    q = sum((p[i]*p[j]*v*v for i, row in enumerate(losses)
             for j, v in enumerate(row)), F(0))
    return d, q, losses


def finite_guard(xs, ys, weights, variance=F(1)):
    """Dyadic corollary, on exact rational finite data.

    INVALID input raises ValueError. A legitimate law outside the sufficient
    radius, covariance or loss guard returns UNRESOLVED, not a negative sign.
    Zero-weight labels are not in the support and are discarded.
    """
    need(len(xs) == len(ys) == len(weights) > 0, 'matching nonempty data')
    need(all(len(x) == 3 for x in list(xs)+list(ys)), 'three coordinates')
    xs = [tuple(map(rational, x)) for x in xs]
    ys = [tuple(map(rational, y)) for y in ys]
    p = list(map(rational, weights))
    s = rational(variance)
    need(s > 0 and min(p) >= 0 and sum(p) == 1, 'positive variance and probability law')
    data = [(x, y, pi) for x, y, pi in zip(xs, ys, p) if pi]
    xs, ys, p = map(list, zip(*data))
    raw_d, _, _ = pair_losses(xs, ys, p)
    xc, yc = center(xs, p), center(ys, p)
    variance_loss = 2*sum((pi*(norm2(x)-norm2(y)) for pi, x, y in zip(p, xc, yc)), F(0))
    need(raw_d == variance_loss, 'pair/variance loss mismatch')
    d = raw_d/s
    if d == 0:
        # All positive-weight pair distances agree; the finite configurations
        # are congruent. This equality case does not require a covariance floor.
        return {'status': 'ZERO_LOSS', 'd': d}
    if any(norm2(x) > s/4 for x in xc):
        return {'status': 'UNRESOLVED', 'reason': 'radius', 'd': d}
    cov = cross(xc, xc, p)
    if not psd([[cov[i][j]-(s/F(2**15) if i == j else 0) for j in range(3)]
                for i in range(3)]):
        return {'status': 'UNRESOLVED', 'reason': 'covariance', 'd': d}
    if d > F(1, 2**360):
        return {'status': 'UNRESOLVED', 'reason': 'loss', 'd': d}
    return {'status': 'SIGNED_MIDDLE', 'd': d,
            'middle': [F(1, 64), F(1, 2)], 'margin': d/F(2**40),
            'signed_from': F(1, 64)}
