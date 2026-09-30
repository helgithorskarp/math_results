#!/usr/bin/env python3
"""Exact all-radius degree-nine quartic and global-minimizer controls.

Actual author six-sendov-3, researcher. Standard-library Python3.11.
The sparse exact kernel is openly adapted from the author's true-excess
checker. Newton/contour algebra retains credit to the independent angular
review. New calculations keep the marked radius, nonlinear mean and each
radial contribution symbolic; no source imports or sampled roots are used.
Polynomial arithmetic is exact in the quotient t^5=0. Uniform collision
limits, spectral geometry and global completeness are written mathematics.
"""
from fractions import Fraction as Q
from hashlib import sha256
from dataclasses import dataclass
from math import factorial, isqrt
from pathlib import Path
import json
import sys


class Poly:
    """Sparse exact rational Laurent polynomials in v and contour z."""
    def __init__(self, terms=None):
        self.terms = {m: Q(c) for m, c in (terms or {}).items() if c}

    def __add__(self, other):
        other = polynomial(other)
        out = dict(self.terms)
        for m, c in other.terms.items():
            out[m] = out.get(m, Q()) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -polynomial(other)

    def __rsub__(self, other):
        return polynomial(other) + -self

    def __mul__(self, other):
        other = polynomial(other)
        out = {}
        for m, c in self.terms.items():
            for n, d in other.terms.items():
                powers = dict(m)
                for name, exponent in n:
                    powers[name] = powers.get(name, 0) + exponent
                if powers.get('t', 0) > 4:
                    continue
                key = tuple(sorted((s, e) for s, e in powers.items() if e))
                out[key] = out.get(key, Q()) + c * d
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, (int, Q)) or not other:
            raise ValueError('only nonzero rational scalar division')
        return Poly({m: c / other for m, c in self.terms.items()})

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError('nonnegative integer power required')
        out = polynomial(1)
        for _ in range(power):
            out = out * self
        return out

    def __eq__(self, other):
        return self.terms == polynomial(other).terms

    def derivative(self, name):
        out = {}
        for m, c in self.terms.items():
            powers = dict(m)
            exponent = powers.get(name, 0)
            if exponent:
                powers[name] = exponent - 1
                key = tuple(sorted((s, e) for s, e in powers.items() if e))
                out[key] = out.get(key, Q()) + exponent * c
        return Poly(out)

    def truncate(self, name, maximum):
        return Poly({m: c for m, c in self.terms.items()
                     if dict(m).get(name, 0) <= maximum})

    def coefficient(self, name, exponent):
        out = {}
        for m, c in self.terms.items():
            powers = dict(m)
            if powers.get(name, 0) == exponent:
                powers.pop(name, None)
                key = tuple(sorted(powers.items()))
                out[key] = out.get(key, Q()) + c
        return Poly(out)

    def substitute(self, values):
        out = polynomial(0)
        for m, c in self.terms.items():
            term = polynomial(c)
            for name, exponent in m:
                if name in values:
                    value = values[name]
                    if exponent < 0:
                        if not isinstance(value, (int, Q)) or not value:
                            raise ValueError('negative power needs rational value')
                        term *= Q(value) ** exponent
                    else:
                        term *= polynomial(value) ** exponent
                else:
                    term *= monomial(name, exponent)
            out += term
        return out


def polynomial(value):
    return value if isinstance(value, Poly) else Poly({(): Q(value)})


def monomial(name, exponent=1):
    if exponent < 0 and name not in ('v','z'):
        raise ValueError('only v and contour z are Laurent variables')
    return Poly({((name, exponent),): Q(1)}) if exponent else polynomial(1)


@dataclass(frozen=True)
class G:
    re: object = 0
    im: object = 0

    def __post_init__(self):
        object.__setattr__(self, 're', polynomial(self.re))
        object.__setattr__(self, 'im', polynomial(self.im))

    def __add__(self, other):
        other = gaussian(other)
        return G(self.re + other.re, self.im + other.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, other):
        return self + -gaussian(other)

    def __rsub__(self, other):
        return gaussian(other) + -self

    def __mul__(self, other):
        other = gaussian(other)
        return G(self.re * other.re - self.im * other.im,
                 self.re * other.im + self.im * other.re)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return G(self.re / other, self.im / other)

    def __pow__(self, exponent):
        if type(exponent) is not int or exponent < 0:
            raise ValueError('nonnegative Gaussian power required')
        out = G(1)
        for _ in range(exponent):
            out = out * self
        return out

    def coefficient(self, name, exponent):
        return G(self.re.coefficient(name, exponent), self.im.coefficient(name, exponent))


def gaussian(value):
    return value if isinstance(value, G) else G(value)


def encode(value):
    if isinstance(value, Poly):
        return {'terms': [[[[name, exponent] for name, exponent in m],
                           [c.numerator, c.denominator]]
                          for m, c in sorted(value.terms.items())]}
    if isinstance(value, G):
        return {'re': encode(value.re), 'im': encode(value.im)}
    if isinstance(value, Q):
        return [value.numerator, value.denominator]
    if isinstance(value, (list, tuple)):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    return value


RECORDS = []
CONTROLS = []
IDENTITIES = []


def require(name, actual, expected):
    if actual != expected:
        raise RuntimeError('exact identity failed: ' + name)
    IDENTITIES.append(name)
    record(name, actual)


def record(name, actual):
    RECORDS.append({'name': name, 'value': encode(actual)})


def reject(name, actual, false_expected):
    if actual == false_expected:
        raise RuntimeError('corruption control failed: ' + name)
    CONTROLS.append(name)


def inverse_monomial(p):
    if len(p.terms) != 1:
        raise ValueError('nonzero monomial required')
    m, c = next(iter(p.terms.items()))
    return Poly({tuple((name, -power) for name, power in m): 1 / c})


def inverse_gaussian(g):
    return G(g.re, -g.im) * inverse_monomial(g.re ** 2 + g.im ** 2)


def series_inverse(a):
    inverse0 = inverse_gaussian(a.coefficient('t', 0))
    b = [inverse0]
    for k in range(1, 5):
        b.append(-sum((a.coefficient('t', j) * b[k - j] for j in range(1, k + 1)), G()) * inverse0)
    return sum((g * monomial('t', k) for k, g in enumerate(b)), G())


def series_sqrt(a):
    constant = a.coefficient('t', 0)
    if constant.im != polynomial(0) or len(constant.re.terms) != 1:
        raise ValueError('positive real monomial constant required')
    m, c = next(iter(constant.re.terms.items()))
    p, q = c.numerator, c.denominator
    ip, iq = isqrt(p), isqrt(q)
    if c <= 0 or ip * ip != p or iq * iq != q or any(e % 2 for _, e in m):
        raise ValueError('positive rational monomial square root required')
    b = [G(Poly({tuple((name, e // 2) for name, e in m): Q(ip, iq)}))]
    inverse_twice = inverse_gaussian(2 * b[0])
    for k in range(1, 5):
        b.append((a.coefficient('t', k) - sum((b[j] * b[k - j] for j in range(1, k)), G())) * inverse_twice)
    return sum((g * monomial('t', k) for k, g in enumerate(b)), G())


def conjugate(a):
    return G(a.re, -a.im)


def norm(a):
    return series_sqrt(a * conjugate(a))


def exp_i_slope(k):
    return sum((G(0, k) ** j * monomial('t', j) / factorial(j) for j in range(5)), G())


def direct_two_level(m, v, kap):
    """Separate two-simple-root calculation, not a universal shape argument."""
    n = 8 - m
    a = monomial('v', -1) - 1
    uA = series_inverse(G(a) + exp_i_slope(n))
    uB = series_inverse(G(a) + exp_i_slope(-m))
    tr = (m + 1) * uA + (n + 1) * uB
    det = 9 * uA * uB
    sq = series_sqrt(tr * tr - 4 * det)
    qn, qf = (tr - sq) / 2, (tr + sq) / 2
    require('direct near quadratic root profile ' + str(m), qn * qn - tr * qn + det, G())
    require('direct far quadratic root profile ' + str(m), qf * qf - tr * qf + det, G())
    F = (m - 1) * norm(uA) + (n - 1) * norm(uB) + norm(qn) + norm(qf)
    dA, dB = uA - v, uB - v
    E = m * dA * conjugate(dA) + n * dB * conjugate(dB)
    E2 = E.coefficient('t', 2)
    require('direct two-level leading energy profile ' + str(m), E2, G(8 * m * n * v ** 4))
    require('direct two-level quadratic objective profile ' + str(m), F.coefficient('t', 2), E2 * kap)
    R4 = (F - E * kap).coefficient('t', 4)
    if R4.im != polynomial(0):
        raise RuntimeError('direct profile quartic must be real')
    return -R4.re * inverse_monomial(E2.re ** 2)


def moments(power_sums, v):
    """Full symbolic Newton identities and fixed-contour logarithm through t^4."""
    elementary = [G(1)]
    for ell in range(1, 5):
        elementary.append(sum(((-1) ** (j - 1) * elementary[ell - j] * power_sums[j]
                               for j in range(1, ell + 1)), G()) / ell)
    # On the fixed near contour, the far pole is expanded about z=0.
    pole = sum((-(monomial('z', j) * monomial('v', -j - 1)) / (8 ** (j + 1))
                for j in range(5)), polynomial(0))
    W = sum(((-1) ** ell * elementary[ell] * monomial('z', -ell)
             * ((ell + 1) * monomial('z') - (8 - ell) * v) * pole
             for ell in range(1, 5)), G())
    logarithm = W - W * W / 2
    near = {ell: -ell * logarithm.coefficient('z', -ell) for ell in range(1, 5)}
    return near, elementary, W


def fixture():
    v, t, mu2, mu3, mu4, psi, y, radial = [monomial(n) for n in
                                        ('v', 't', 'mu2', 'mu3', 'mu4', 'psi', 'y', 'radial')]
    vi = monomial('v', -1)
    c2 = v ** 2 / 2 - v ** 3
    c3 = v ** 2 / 6 - v ** 3 + v ** 4
    c4 = -v ** 2 / 24 + 7 * v ** 3 / 12 - 3 * v ** 4 / 2 + v ** 5
    cR = c2 + 9 * v ** 3 / 8
    gap_inverse = vi / 8
    kap = vi ** 2 - Q(13, 8) * vi

    # u_j-v through order four for phi_j=t theta_j+t^2 y,
    # tau_j=t^4 r_j, sum theta=0. Only sum r enters at this order.
    power_sums = {
        1: G(c2 * mu2, -8 * v ** 2 * y) * t ** 2
           + G(0, c3 * mu3) * t ** 3
           + G(8 * c2 * y ** 2 + c4 * mu4 + v ** 2 * radial,
               3 * c3 * y * mu2) * t ** 4,
        2: G(-v ** 4 * mu2) * t ** 2
           + G(0, -2 * v ** 2 * c2 * mu3) * t ** 3
           + G((c2 ** 2 + 2 * v ** 2 * c3) * mu4 - 8 * v ** 4 * y ** 2,
               -6 * c2 * v ** 2 * y * mu2) * t ** 4,
        3: G(0, v ** 6 * mu3) * t ** 3
           + G(-3 * v ** 4 * c2 * mu4, 3 * v ** 6 * y * mu2) * t ** 4,
        4: G(v ** 8 * mu4) * t ** 4,
    }
    near, elementary, W = moments(power_sums, v)
    require('near second moment quadratic coefficient', near[2].coefficient('t', 2), G(-Q(3, 4) * v ** 4 * mu2))
    T4 = mu4 / 2 + mu2 ** 2 / 32
    U = mu4 / 8 - mu2 ** 2 / 64
    R0sq = mu2 ** 2 / 64
    expected2 = (c2 ** 2 * (T4 + 2 * U + R0sq)
                 + 2 * v ** 2 * c3 * (T4 + 2 * U)
                 + 18 * c2 * v ** 4 * gap_inverse * (3 * U + R0sq)
                 - 18 * v ** 8 * gap_inverse ** 2 * U
                 + 81 * v ** 8 * gap_inverse ** 2 * R0sq)
    expected3 = -3 * c2 * v ** 4 * (T4 + U) - 27 * v ** 8 * gap_inverse * U
    require('complete near second moment quartic, including nonlinear mean',
            near[2].coefficient('t', 4).re, expected2 - 7 * v ** 4 * y ** 2)
    require('complete near third moment quartic', near[3].coefficient('t', 4).re, expected3)
    require('complete near fourth moment quartic', near[4].coefficient('t', 4).re, v ** 8 * T4)
    for ell in range(1, 5):
        record('complete characteristic near trace jet ' + str(ell), near[ell])

    # At z=8v, implicit simple-far root differentiation uses C0'=(8v)^7.
    far2 = (9 * elementary[1].coefficient('t', 2) / 8
            - elementary[2].coefficient('t', 2) * vi * Q(9, 32))
    require('far second coefficient imaginary nonlinear mean', far2.im, -9 * v ** 2 * y)
    require('far second coefficient real balanced shape', far2.re,
            (9 * c2 / 8 - 9 * v ** 3 / 64) * mu2)

    energy4 = (c2 ** 2 - 2 * v ** 2 * c3) * mu4 + 8 * v ** 4 * y ** 2
    real_squares = c2 ** 2 * T4 + 2 * c2 * cR * U + cR ** 2 * psi
    F4 = (2 * power_sums[1].coefficient('t', 4).re
          - near[2].coefficient('t', 4).re * vi / 2
          + real_squares * vi / 2
          + near[3].coefficient('t', 4).re * vi ** 2 / 6
          - near[4].coefficient('t', 4).re * vi ** 3 / 8
          + Q(9, 2) * v ** 3 * y ** 2)
    alpha = -3 * v ** 3 / 32 + 5 * v ** 4 / 64 + 53 * v ** 5 / 512
    beta = -v ** 3 / 512 + 13 * v ** 4 / 1024 - 203 * v ** 5 / 8192
    gamma = v ** 3 / 8 + v ** 4 / 16 + v ** 5 / 128
    residual = F4 - kap * energy4
    require('full universal angular-mean-inward fixed-energy quartic', residual,
            alpha * mu4 + beta * mu2 ** 2 + gamma * psi + 5 * v ** 3 * y ** 2 + 2 * v ** 2 * radial)
    require('exact complete mean-square cost', residual.coefficient('y', 2), 5 * v ** 3)
    require('exact complete sum of independent inward costs', residual.coefficient('radial', 1), 2 * v ** 2)
    require('spectral concentration coefficient', gamma, cR ** 2 * vi / 2)

    A = -alpha * vi ** 8
    B = -beta * vi ** 8
    C = gamma * vi ** 8 / 64
    require('radius-parametric angular coefficient A', A, vi ** 3 * (48 * vi ** 2 - 40 * vi - 53) / 512)
    require('radius-parametric angular coefficient B', B, vi ** 3 * (16 * vi ** 2 - 104 * vi + 203) / 8192)
    require('radius-parametric spectral coefficient C', C, vi ** 3 * (4 * vi + 1) ** 2 / 8192)
    X, eta = monomial('X'), monomial('eta')
    K = A * X + B - C * eta
    Kstar = A * Q(43, 56) + B - C
    knownK1 = (516 * vi ** 5 - 528 * vi ** 4 - 393 * vi ** 3) / 7168
    require('credited one-plus-seven quartic baseline', Kstar, knownK1)
    slope = A - Q(28, 15) * C
    require('complete angular deficit identity', Kstar - K,
            slope * (Q(43, 56) - X) + C * (eta - (56 * X - 13) / 30))
    require('positive-slope polynomial factor', slope,
            vi ** 3 * (2768 * vi ** 2 - 2456 * vi - 3187) / 30720)
    minimum = A / 8 + B - C
    require('full marked-interval angular minimum', minimum,
            3 * vi ** 3 * (vi - 1) ** 2 / 256)
    require('credited cutoff angular minimum', minimum.substitute({'v': Q(8, 13)}),
            polynomial(Q(164775, 8388608)))

    d, s = monomial('d'), monomial('s')
    slope_poly = 2768 * d ** 2 - 2456 * d - 3187
    require('entire marked interval slope positivity certificate',
            slope_poly.substitute({'d': Q(13, 8) + s}), Q(525, 4) + 6540 * s + 2768 * s ** 2)
    branch_poly = 516 * d ** 2 - 528 * d - 393
    require('entire marked interval branch positivity certificate',
            branch_poly.substitute({'d': Q(13, 8) + s}), Q(1785, 16) + 1149 * s + 516 * s ** 2)
    profile_poly = 48 * d ** 2 - 40 * d - 53
    require('entire marked interval two-level gap positivity certificate',
            profile_poly.substitute({'d': Q(13, 8) + s}), Q(35, 4) + 116 * s + 48 * s ** 2)
    for name, p in [('slope', slope_poly), ('branch', branch_poly), ('two-level gap', profile_poly)]:
        shifted = p.substitute({'d': Q(13, 8) + s})
        if not shifted.terms or any(c <= 0 for c in shifted.terms.values()):
            raise RuntimeError('positive exact coefficient certificate failed')
        record(name + ' positive shifted coefficient list', sorted(shifted.terms.values()))

    # The cutoff identity is an exact replay of the independent angular formula.
    cutoffp = Q(10985, 33554432)
    require('credited cutoff functional in every moment coordinate',
            K.substitute({'v': Q(8, 13)}), cutoffp * (224 * X + 122 - 90 * eta))
    require('credited cutoff optimizer slope', slope.substitute({'v': Q(8, 13)}), polynomial(56 * cutoffp))
    for m in range(1, 5):
        n = 8 - m
        Xm = Q(8, m * n) - Q(3, 8)
        Km = K.substitute({'X': Xm, 'eta': 1})
        require('two-original-value profile gap m=' + str(m), Kstar - Km,
                Q((m - 1) * (7 - m), 448 * m * n) * vi ** 3 * (48 * vi ** 2 - 40 * vi - 53))
        require('independent direct-quadratic quartic profile m=' + str(m),
                direct_two_level(m, v, kap), Km)
    for name, value in [('A', A), ('B', B), ('C', C), ('optimizer slope', slope)]:
        record('complete coefficient record ' + name, value)

    reject('drop the spectral rank-one real-square term', residual,
           residual - cR ** 2 * psi * vi / 2)
    reject('omit exact energy elimination', residual, F4)
    reject('drop far nonlinear-mean modulus contribution', residual,
           residual - Q(9, 2) * v ** 3 * y ** 2)
    reject('incorrect spectral Gram slope', Kstar - K,
           A * (Q(43, 56) - X) + C * (eta - (56 * X - 13) / 30))
    reject('corrupt all-radius positivity certificate', slope_poly.substitute({'d': Q(13, 8) + s}),
           Q(525, 4) - 6540 * s + 2768 * s ** 2)
    log_wrong = W
    reject('omit nonlinear contour-log contribution', near[2], -2 * log_wrong.coefficient('z', -2))
    digest = sha256(json.dumps(RECORDS, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    reject('alter complete exact record digest', digest, '0' * 64)
    return {'schema': 1, 'agent': 'six-sendov-3', 'role': 'researcher',
            'arithmetic': 'exact rational Gaussian multivariate Laurent algebra modulo t^5',
            'claim_status': 'complete radius-parametric quartic algebra; uniform collision and global analytic proof separate',
            'identity_count': len(IDENTITIES), 'complete_record_count': len(RECORDS),
            'corruption_control_count': len(CONTROLS),
            'corruption_controls': CONTROLS, 'records_sha256': digest, 'complete_records': RECORDS}


def main():
    if sys.argv[1:] not in ([], ['--emit-fixture']):
        raise SystemExit('usage: python3 -I -B verify.py [--emit-fixture]')
    path = Path(__file__).with_name('expected.json')
    if sys.argv[1:] != ['--emit-fixture']:
        try:
            expected = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise RuntimeError('required expected.json absent or malformed') from exc
    result = fixture()
    if sys.argv[1:] == ['--emit-fixture']:
        path.write_text(json.dumps(result, indent=2) + '\n')
    elif result != expected:
        raise RuntimeError('complete exact fixture differs')
    print(json.dumps({k:v for k,v in result.items() if k!='complete_records'}, sort_keys=True))


if __name__ == '__main__':
    main()
