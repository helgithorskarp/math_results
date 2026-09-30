#!/usr/bin/env python3
"""Exact sextic algebra for the degree-nine second-order energy basin.

Author six-sendov-3, researcher. The rational polynomial/Gaussian kernel
is openly adapted from this author's preceding cubic trace checker. This
standalone file imports no campaign module. Analytic uniformity, variance
absorption and universal basin completeness remain written proof obligations.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, isqrt
from pathlib import Path
import json
import sys

ORDER = 6


@dataclass(frozen=True)
class L:
    terms: tuple = ()

    def __add__(self, other):
        other = laurent(other)
        terms = dict(self.terms)
        for exponent, coefficient in other.terms:
            terms[exponent] = terms.get(exponent, Q(0)) + coefficient
        return polynomial(terms)

    __radd__ = __add__

    def __neg__(self):
        return L(tuple((e, -c) for e, c in self.terms))

    def __sub__(self, other):
        return self + -laurent(other)

    def __rsub__(self, other):
        return laurent(other) + -self

    def __mul__(self, other):
        other = laurent(other)
        terms = {}
        for e, c in self.terms:
            for f, d in other.terms:
                terms[e+f] = terms.get(e+f, Q(0)) + c*d
        return polynomial(terms)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = laurent(other)
        if len(other.terms) != 1:
            raise ValueError('Division requires a nonzero Laurent monomial')
        f, d = other.terms[0]
        return L(tuple((e-f, c/d) for e, c in self.terms))

    def __pow__(self, power):
        if not isinstance(power, int):
            raise TypeError('Integer exponent required')
        if power < 0:
            return laurent(1) / self**(-power)
        total = laurent(1)
        for _ in range(power):
            total = total*self
        return total

    def evaluate(self, value):
        return sum((c*value**e for e, c in self.terms), Q(0))

    def derivative(self):
        return polynomial({e-1: e*c for e, c in self.terms if e})


def polynomial(terms):
    return L(tuple(sorted((e, Q(c)) for e, c in terms.items() if c)))


def laurent(value):
    return value if isinstance(value, L) else polynomial({0: Q(value)})


@dataclass(frozen=True)
class G:
    re: L = L()
    im: L = L()

    def __post_init__(self):
        object.__setattr__(self, 're', laurent(self.re))
        object.__setattr__(self, 'im', laurent(self.im))

    def __add__(self, other):
        other = gaussian(other)
        return G(self.re+other.re, self.im+other.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + -gaussian(other)

    def __rsub__(self, other):
        return gaussian(other) + -self

    def __mul__(self, other):
        other = gaussian(other)
        return G(self.re*other.re-self.im*other.im,
                 self.re*other.im+self.im*other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = gaussian(other)
        norm = other.re**2+other.im**2
        numerator = self*G(other.re, -other.im)
        return G(numerator.re/norm, numerator.im/norm)

    def conjugate(self):
        return G(self.re, -self.im)


def gaussian(value):
    return value if isinstance(value, G) else G(value)


def series(*coefficients):
    if len(coefficients) > ORDER+1:
        raise ValueError('Too many coefficients')
    return [gaussian(x) for x in coefficients]+[G()]*(ORDER+1-len(coefficients))


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def scale(a, value):
    return [x*value for x in a]


def sub(a, b):
    return add(a, scale(b, -1))


def mul(a, b):
    return [sum((a[k]*b[n-k] for k in range(n+1)), G())
            for n in range(ORDER+1)]


def inverse(a):
    b = [G(1)/a[0]]
    for n in range(1, ORDER+1):
        b.append(-sum((a[k]*b[n-k] for k in range(1, n+1)), G())/a[0])
    return b


def square_root(a):
    if a[0].im != L() or len(a[0].re.terms) != 1:
        raise ValueError('Positive rational monomial constant required')
    exponent, coefficient = a[0].re.terms[0]
    if exponent % 2 or coefficient <= 0:
        raise ValueError('Even power and positive coefficient required')
    p, q = coefficient.numerator, coefficient.denominator
    ip, iq = isqrt(p), isqrt(q)
    if ip*ip != p or iq*iq != q:
        raise ValueError('Constant square root is not rational')
    b = [G(polynomial({exponent//2: Q(ip, iq)}))]
    for n in range(1, ORDER+1):
        b.append((a[n]-sum((b[k]*b[n-k] for k in range(1, n)), G()))/(2*b[0]))
    return b


def modulus(a):
    return square_root(mul(a, [x.conjugate() for x in a]))


def exponential_i(phi):
    iphi, power, total = scale(phi, G(0, 1)), series(1), series()
    for k in range(ORDER+1):
        total = add(total, scale(power, Q(1, factorial(k))))
        power = mul(power, iphi)
    return total


X = polynomial({1: 1})
A0, D0, V0, B0 = Q(5, 8), Q(13, 8), Q(8, 13), Q(39, 64)
CSTAR = Q(560235, 8388608)
ALPHA = Q(65, 512)
CMEAN = Q(-318565, 2097152)
S0 = Q(717042898065, 6734508720128)
DSTAR = Q(520320727875, 6734508720128)
KPRIME = Q(5953701, 7340032)
GAMMA = Q(2965647537471488, 20111391661725)
BETA_OPT = Q(112, 169)
RHO_OPT = Q(102921, 4096)
checks, records = [], []


def check(label, actual, expected):
    if actual != expected:
        raise RuntimeError(f'{label}: {actual!r} != {expected!r}')
    checks.append(label)


def reject(label, actual, wrong):
    if actual == wrong:
        raise RuntimeError('Corruption survived: '+label)


def encode(value):
    if isinstance(value, L):
        return [[e, c.numerator, c.denominator] for e, c in value.terms]
    if isinstance(value, G):
        return [encode(value.re), encode(value.im)]
    if isinstance(value, Q):
        return [value.numerator, value.denominator]
    if isinstance(value, (list, tuple)):
        return [encode(x) for x in value]
    return value


def power(a, exponent):
    total = series(1)
    for _ in range(exponent):
        total = mul(total, a)
    return total


def real(a):
    return [G(z.re) for z in a]


def imaginary(a):
    return [G(z.im) for z in a]


def circle(slope, cubic_mean=0, linear_mean=0):
    y = series(0, slope+linear_mean, 0, cubic_mean)
    boundary = add(add(scale(power(y, 2), -B0/2),
                       scale(power(y, 4), -B0**3/8)),
                   scale(power(y, 6), -B0**5/16))
    return add(series(V0), add(boundary, scale(y, G(0, 1))))


def kt(d):
    return d**3*(3792*d**2-7728*d+2991)/28672


def kt_series(d):
    inner = add(sub(scale(power(d, 2), 3792), scale(d, 7728)), series(2991))
    return scale(mul(power(d, 3), inner), Q(1, 28672))


def actual_profile(r, marked, ua, ub, v, label):
    """Differentiate the actual original polynomial, then check both q roots."""
    s = 8-r
    trace = add(scale(ua, r+1), scale(ub, s+1))
    determinant = scale(mul(ua, ub), 9)
    disc = square_root(sub(power(trace, 2), scale(determinant, 4)))
    near = scale(sub(trace, disc), Q(1, 2))
    far = scale(add(trace, disc), Q(1, 2))
    for name, q in [('near', near), ('far', far)]:
        check(label+':residual-root:'+name,
              add(sub(power(q, 2), mul(trace, q)), determinant), series())

    za, zb = sub(marked, inverse(ua)), sub(marked, inverse(ub))
    # Residual factor of derivative of (z-marked)(z-za)^r(z-zb)^s:
    # 9z^2+linear*z+constant. Substitute z=marked-1/q.
    linear = scale(add(add(scale(za, s+1), scale(zb, r+1)), scale(marked, 8)), -1)
    constant = add(mul(za, zb), mul(marked, add(scale(zb, r), scale(za, s))))
    q2 = add(add(scale(power(marked, 2), 9), mul(linear, marked)), constant)
    q1 = sub(scale(linear, -1), scale(marked, 18))
    check(label+':original-derivative-trace', scale(mul(q1, inverse(q2)), -1), trace)
    check(label+':original-derivative-determinant', scale(inverse(q2), 9), determinant)
    b = sub(series(1), power(marked, 2))
    for name, u, z in [('a', ua, za), ('b', ub, zb)]:
        delta = sub(u, v)
        check(label+':disk-boundary:'+name,
              add(scale(real(delta), 2), mul(b, mul(delta, [w.conjugate() for w in delta]))), series())
        check(label+':original-unit-circle:'+name, mul(z, [w.conjugate() for w in z]), series(1))

    aa, bb, nn = sub(ua, v), sub(ub, v), sub(near, v)
    moments = {k: add(add(scale(power(aa, k), r-1), scale(power(bb, k), s-1)), power(nn, k))
               for k in range(1, 7)}
    energy = add(scale(mul(aa, [w.conjugate() for w in aa]), r),
                 scale(mul(bb, [w.conjugate() for w in bb]), s))
    total = add(add(scale(modulus(ua), r-1), scale(modulus(ub), s-1)),
                add(modulus(near), modulus(far)))
    gap = sub(total, scale(v, 16))
    trace_gap = scale(add(scale(real(aa), r), scale(real(bb), s)), 2)
    inverse_v = inverse(v)
    analytic = trace_gap
    for k, coefficient in [(2, Q(-1, 2)), (3, Q(1, 6)), (4, Q(-1, 8)),
                           (5, Q(3, 40)), (6, Q(-1, 16))]:
        analytic = add(analytic, scale(mul(real(moments[k]), power(inverse_v, k-1)), coefficient))
    mean = real(moments[1])
    analytic = add(analytic, scale(mul(power(mean, 2), inverse_v), Q(1, 14)))
    analytic = add(analytic, scale(mul(power(mean, 3), power(inverse_v, 2)), Q(-1, 294)))
    analytic = add(analytic, scale(mul(mul(power(mean, 2), real(moments[2])), power(inverse_v, 3)), Q(1, 196)))
    analytic = add(analytic, sub(modulus(far), real(far)))

    def near_sum(fn):
        return add(add(scale(fn(aa), r-1), scale(fn(bb), s-1)), fn(nn))

    squares = near_sum(lambda z: power(real(z), 2))
    cubes = near_sum(lambda z: power(real(z), 3))
    rs = near_sum(lambda z: mul(power(real(z), 2), power(imaginary(z), 2)))
    variance = sub(squares, scale(power(mean, 2), Q(1, 7)))
    correction = scale(mul(variance, inverse_v), Q(1, 2))
    cubic_defect = sub(cubes, scale(power(mean, 3), Q(1, 49)))
    correction = add(correction, scale(mul(cubic_defect, power(inverse_v, 2)), Q(-1, 6)))
    mixed_defect = add(rs, scale(mul(power(mean, 2), real(moments[2])), Q(1, 49)))
    correction = add(correction, scale(mul(mixed_defect, power(inverse_v, 3)), Q(-1, 4)))
    check(label+':weighted-variance-identity-order6', sub(gap, analytic), correction)
    records.append([label, encode(gap), encode(energy), encode(analytic), encode(variance)])
    return gap, energy, analytic, variance


def run():
    check('credited-cutoff-quartic', kt(laurent(D0)), laurent(CSTAR))
    d = laurent(D0)+X
    check('varying-radius-derivative', dict(kt(d).terms)[1], KPRIME)
    check('sextic-completed-mean-square', S0-CMEAN**2*Q(9, 14)/(4*ALPHA), DSTAR)
    check('basin-coefficient-conversion', DSTAR/CSTAR**3-KPRIME/(D0*CSTAR**2), GAMMA)
    check('mean-coefficient-near-plus-far', ALPHA, Q(1, 128)/V0+Q(9, 128)/V0)
    check('necessary-normalized-reciprocal-mean', -3*CMEAN/(2*ALPHA), Q(14703, 8192))
    c3 = V0**2/6-V0**3+V0**4
    check('necessary-normalized-original-mean', -D0**2*Q(14703, 8192)-3*c3*D0**8, Q(-28561, 32768))

    # A complete symbolic scalar weighted modulus identity (real part X*t^2,
    # imaginary part t); homogeneity supplies arbitrary imaginary scale.
    scalar = series(V0, G(0, 1), X)
    xi = sub(scalar, series(V0))
    rr, ss = real(xi), imaginary(xi)
    scalar_taylor = series()
    for k, coefficient in [(2, -Q(1, 2)/V0), (3, Q(1, 6)/V0**2),
                           (4, -Q(1, 8)/V0**3), (5, Q(3, 40)/V0**4),
                           (6, -Q(1, 16)/V0**5)]:
        scalar_taylor = add(scalar_taylor, scale(real(power(xi, k)), coefficient))
    scalar_taylor = add(scalar_taylor, scale(power(rr, 2), Q(1, 2)/V0))
    scalar_taylor = add(scalar_taylor, scale(power(rr, 3), -Q(1, 6)/V0**2))
    scalar_taylor = add(scalar_taylor, scale(mul(power(rr, 2), power(ss, 2)), -Q(1, 4)/V0**3))
    check('complete-scalar-modulus-order6', sub(modulus(scalar), real(scalar)), scalar_taylor)
    records.append(['scalar-weighted-modulus', encode(scalar_taylor)])

    # Symbolic cubic imaginary mean, using a different input coordinate.
    gap, energy, analytic, variance = actual_profile(1, series(A0), circle(7, X), circle(-1, X), series(V0), 'circle-cubic-mean')
    check('circle-cauchy-saturation-through6', gap, analytic)
    check('circle-variance-through6', variance, series())
    remainder = add(gap, scale(power(energy, 2), CSTAR))
    for k in range(6):
        check(f'circle-credited-quartic-cancellation:{k}', remainder[k], G())
    circle_d = remainder[6].re/(energy[2].re**3)
    expected_circle = laurent(S0)+CMEAN*Q(3, 196)*X+Q(5, 1)/(V0*56**3)*X**2
    check('circle-symbolic-sextic', circle_d, expected_circle)
    check('circle-optimal-cubic-mean', -dict(circle_d.terms)[1]/(2*dict(circle_d.terms)[2]), RHO_OPT)
    check('circle-sharp-sextic', circle_d.evaluate(RHO_OPT), DSTAR)

    # First-order formal common mean checks the independent invariant coefficient.
    _, energy_m, analytic_m, _ = actual_profile(1, series(A0), circle(7, 0, X), circle(-1, 0, X), series(V0), 'circle-linear-mean')
    normalized_m = add(analytic_m, scale(power(energy_m, 2), CSTAR))
    check('formal-mean-quadratic-polynomial', normalized_m[2], G(64*ALPHA*X**2))
    check('formal-mean-quartic-linear-invariant', dict(normalized_m[4].re.terms)[1], 8*336*CMEAN)
    # Non-saturating repeated balanced profile checks the full variance identity.
    actual_profile(4, series(A0), circle(4), circle(-4), series(V0), 'balanced-four-four-control')

    # Actual original-root polynomial, with symbolic common phase beta*t^3.
    ua = inverse(add(series(A0), exponential_i(series(0, 7, 0, X))))
    ub = inverse(add(series(A0), exponential_i(series(0, -1, 0, X))))
    gap_a, energy_a, analytic_a, _ = actual_profile(1, series(A0), ua, ub, series(V0), 'original-angular-cubic-mean')
    check('angular-cauchy-saturation-through6', gap_a, analytic_a)
    check('angular-baseline-energy2', energy_a[2], G(56*V0**4))
    angular_remainder = add(gap_a, scale(power(energy_a, 2), CSTAR))
    for k in range(6):
        check(f'angular-credited-quartic-cancellation:{k}', angular_remainder[k], G())
    angular_d = angular_remainder[6].re/(energy_a[2].re**3)
    rho_of_beta = (V0**2*X-42*c3)/V0**6
    check('inverse-coordinate-symbolic-identity', angular_d, circle_d.evaluate(rho_of_beta))
    check('angular-optimal-phase', -dict(angular_d.terms)[1]/(2*dict(angular_d.terms)[2]), BETA_OPT)
    check('angular-sharp-sextic', angular_d.evaluate(BETA_OPT), DSTAR)
    check('coordinate-optima-agree', rho_of_beta.evaluate(BETA_OPT), RHO_OPT)

    # Mixed a=a0+lambda*t^2 verifies the varying-radius coefficient directly,
    # without substituting a fixed-radius derivative into the q calculation.
    marked = series(A0, 0, X)
    dser = add(series(1), marked)
    vser = inverse(dser)
    kappa = mul(dser, sub(marked, series(A0)))
    ua = inverse(add(marked, exponential_i(series(0, 7, 0, BETA_OPT))))
    ub = inverse(add(marked, exponential_i(series(0, -1, 0, BETA_OPT))))
    gap_j, energy_j, analytic_j, _ = actual_profile(1, marked, ua, ub, vser, 'joint-marked-radius')
    check('joint-cauchy-saturation-through6', gap_j, analytic_j)
    corrected = add(sub(gap_j, mul(kappa, energy_j)), mul(kt_series(dser), power(energy_j, 2)))
    corrected = sub(corrected, scale(power(energy_j, 3), DSTAR))
    check('complete-mixed-sextic-identity', corrected, series())

    gamma_balanced = angular_d.evaluate(0)/CSTAR**3-KPRIME/(D0*CSTAR**2)
    check('phase-improves-second-crossing', gamma_balanced-GAMMA, Q(2199023255552, 663012911925))
    reject('discard-far-quadratic-mean', ALPHA, Q(1, 128)/V0)
    reject('wrong-sextic-fifth-moment-sign', scalar_taylor,
           sub(scalar_taylor, scale(real(power(xi, 5)), Q(3, 20)/V0**4)))
    reject('opposite-quartic-mean-sign', CMEAN, -CMEAN)
    reject('omit-cubic-phase-optimization', DSTAR, angular_d.evaluate(0))
    reject('wrong-marked-radius-conversion', GAMMA, DSTAR/CSTAR**3-KPRIME/CSTAR**2)
    reject('zero-reciprocal-mean-optimum', RHO_OPT, Q(0))

    payload = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    manifest = {
        'agent': 'six-sendov-3', 'role': 'researcher',
        'arithmetic': 'Q[X][i][t]/(t^7); X a formal real parameter',
        'actual_two_block_profiles': 5,
        'complete_symbolic_scalar_modulus_control': True,
        'checks': len(checks), 'mutation_controls': 6,
        'Csharp': encode(CSTAR), 'alpha0': encode(ALPHA), 'quartic_mean_coefficient': encode(CMEAN),
        'balanced_sextic_S0': encode(S0), 'sharp_sextic_Dstar': encode(DSTAR),
        'Ktrace_prime_at_cutoff': encode(KPRIME), 'basin_Gamma': encode(GAMMA),
        'optimal_original_common_phase_beta': encode(BETA_OPT),
        'optimal_reciprocal_cubic_mean_rho': encode(RHO_OPT),
        'circle_D_polynomial': encode(circle_d), 'angular_D_polynomial': encode(angular_d),
        'phase_crossing_improvement': encode(gamma_balanced-GAMMA),
        'records_sha256': sha256(payload).hexdigest(),
        'unformalized': ['uniform analytic remainder bounds', 'variance absorption',
                         'all-disk slack comparison', 'invariant-space and moment equality arguments',
                         'universal basin completeness and analytic crossing'],
    }
    fixture = Path(__file__).with_name('expected.json')
    if fixture.exists():
        check('complete-fixture', manifest, json.loads(fixture.read_text()))
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == '__main__':
    if len(sys.argv) != 1:
        raise SystemExit('Usage: python3 -I -B verify.py')
    run()
