"""Exact schedules and finite guards for the written small-loss theorem.

Standard library only. Gaussian integrals and the analytic proof are not
formalized here. Integer exponents are stored without expanding powers of two.
Finite geometry helpers follow gaussian_effective_mean_loss/certificate.py.
"""
from fractions import Fraction as F
from itertools import combinations
from math import isqrt


def need(ok, message):
    if not ok:
        raise ValueError(message)


def rational(x):
    need(isinstance(x, (int, F)) and not isinstance(x, bool),
         "exact integer or Fraction required")
    return F(x)


def integer(x, minimum=0):
    need(isinstance(x, int) and not isinstance(x, bool) and x >= minimum,
         "integer outside domain")
    return x


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def floor_log2(x):
    x = rational(x)
    need(x > 0, "positive logarithm argument")
    p, q = x.numerator, x.denominator
    n = p.bit_length()-q.bit_length()
    at_least = p >= q << n if n >= 0 else p << (-n) >= q
    return n if at_least else n-1


def ceil_log2(x):
    return -floor_log2(1/rational(x))


def at_most_pow2(x, exponent):
    x = rational(x)
    need(x >= 0 and isinstance(exponent, int), "nonnegative comparison")
    return x == 0 or ceil_log2(x) <= exponent


def annular_schedule(radius, kappa, m):
    """Signs exp(-m^2/2)<=u<=exp(-S0^2/2); no upper-window join.

    e<4 supplies all transcendental comparisons. kappa>0 may describe an
    empty geometry; feasibility is a separate input obligation.
    """
    R, k, m = map(rational, (radius, kappa, m))
    need(R > 0 and k > 0, "positive radius and covariance floor")
    S0 = max(5*R, 3*R+1)
    need(m >= S0, "m below annular window")
    omega = ceil_fraction(4*R*m+5*R*R)
    aexp = 6+ceil_fraction(6*R*m)
    k0 = ceil_log2(2*R*R/k)
    ell = ceil_log2(96*R**3/k+6*R)
    k1 = aexp+ceil_log2(16*R/k)
    k2 = ceil_log2(2*R)+2*omega
    cexp = 2*omega+4
    dexp = cexp+2+k1
    budgets = [
        ceil_log2(4*R*R/(k*k))+k0,
        2*dexp+1+k0,
        ceil_log2(8*R*R/k)+2*dexp+k0,
        4*omega+2*dexp+k0+ceil_log2(144*R**4/(k*k)),
        dexp+ceil_log2(R/(2*k)),
        cexp+4*dexp+3+aexp+2*ell+2*k0,
        2*cexp+4*dexp+6+2*k2+3*k0,
    ]
    return {"R": R, "kappa": k, "m": m, "S0": S0,
            "omega": omega, "A_exponent": aexp,
            "K0_exponent": k0, "L_exponent": ell,
            "K1_exponent": k1, "K2_exponent": k2,
            "c_negative_exponent": cexp, "delta_negative_exponent": dexp,
            "budget_exponents": budgets, "loss_bits": max(0, *budgets),
            "scope": "ANNULAR_WINDOW_ONLY"}


def normalized_schedule(m):
    """Explicit all-upper-threshold join, PROOF.md (13)--(14)."""
    m = integer(m, 4)
    budgets = [44, 14*m+83, 14*m+98, 22*m+124,
               7*m+47, 35*m+219, 44*m+208]
    return {"m": m, "loss_bits": 44*m+208,
            "budget_exponents": budgets,
            "minus_log_signed_threshold": F(m*m, 2),
            "scope": "MOVING_UPPER_SIGN_WINDOW"}


def relative_schedule(bits):
    b = integer(bits)
    q = 3*(b+20)
    m = isqrt(q)
    m += m*m < q
    m = max(4, m)
    out = normalized_schedule(m)
    out["relative_defect_bits"] = b
    return out


def dot(x, y):
    return sum((a*b for a, b in zip(x, y)), F(0))


def sub(x, y):
    return tuple(a-b for a, b in zip(x, y))


def norm2(x):
    return dot(x, x)


def center(xs, p):
    av = tuple(sum((pi*x[j] for pi, x in zip(p, xs)), F(0))
               for j in range(3))
    return [sub(x, av) for x in xs]


def covariance(xs, p):
    return [[sum((pi*x[i]*x[j] for pi, x in zip(p, xs)), F(0))
             for j in range(3)] for i in range(3)]


def det(a):
    if not a:
        return F(1)
    return sum(((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]])
                for j in range(len(a))), F(0))


def psd(a):
    return (all(a[i][j] == a[j][i] for i in range(3) for j in range(3))
            and all(det([[a[i][j] for j in ix] for i in ix]) >= 0
                    for n in (1, 2, 3) for ix in combinations(range(3), n)))


def finite_guard(xs, ys, weights, bits, variance=F(1)):
    """Certify Def<=2^-bits*d plus a signed moving window.

    Invalid data raise ValueError; an unmet sufficient guard is UNRESOLVED.
    Positive-weight source/target pairs must be a contraction. A contraction
    of a finite subset has a Euclidean 1-Lipschitz extension; only its
    prescribed values enter the two convolutions. Zero-weight labels vanish.
    """
    schedule = relative_schedule(bits)
    need(len(xs) == len(ys) == len(weights) > 0, "matching nonempty data")
    need(all(len(x) == 3 for x in list(xs)+list(ys)), "three coordinates")
    xs = [tuple(map(rational, x)) for x in xs]
    ys = [tuple(map(rational, y)) for y in ys]
    p = list(map(rational, weights))
    s = rational(variance)
    need(s > 0 and min(p) >= 0 and sum(p) == 1,
         "positive variance and probability law")
    triples = [(x, y, w) for x, y, w in zip(xs, ys, p) if w]
    xs, ys, p = map(list, zip(*triples))
    d_pair = F(0)
    for i, j in combinations(range(len(p)), 2):
        loss = norm2(sub(xs[i], xs[j]))-norm2(sub(ys[i], ys[j]))
        need(loss >= 0, "not a contraction")
        d_pair += 2*p[i]*p[j]*loss
    xc, yc = center(xs, p), center(ys, p)
    d_marginal = 2*sum((w*(norm2(x)-norm2(y))
                       for w, x, y in zip(p, xc, yc)), F(0))
    need(d_pair == d_marginal, "pair/marginal loss mismatch")
    d = d_pair/s
    if d == 0:
        return {"status": "ZERO_LOSS", "d": d}
    if any(norm2(x) > s/4 for x in xc):
        return {"status": "UNRESOLVED", "reason": "radius", "d": d}
    cov = covariance(xc, p)
    if not psd([[cov[i][j]-(s/2**15 if i == j else 0)
                 for j in range(3)] for i in range(3)]):
        return {"status": "UNRESOLVED", "reason": "covariance", "d": d}
    if not at_most_pow2(d, -schedule["loss_bits"]):
        return {"status": "UNRESOLVED", "reason": "loss", "d": d,
                "required_loss_bits": schedule["loss_bits"]}
    return {"status": "CONTROLLED_DEFECT", "d": d, **schedule}
