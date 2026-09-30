#!/usr/bin/env python3
"""Exact algebra for the degree-nine Cauchy trace bound.

The Laurent/Gaussian kernel is openly adapted from this author's previous
energy-basin checker. No author module is imported; this file is standalone.
Generic identities support the written weighted analytic proof. Neither
finite profiles nor the symbolic arithmetic formalize its uniform estimates.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from hashlib import sha256
from math import factorial, isqrt
from pathlib import Path
import json
import sys

ORDER = 4


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


V = polynomial({1: 1})
D = V**(-1)
B = 2*D-D**2
KAPPA = D*(D-Q(13, 8))
C2, C4 = -B/2, -(B**3)/8
V0, D0 = Q(8, 13), Q(13, 8)
CMAX, P8 = Q(560235, 8388608), Q(10985, 33554432)
checks, records = [], []


def check(label, actual, expected):
    if actual != expected:
        raise RuntimeError(f'{label}: {actual!r} != {expected!r}')
    checks.append(label)


def reject(label, actual, wrong):
    if actual == wrong:
        raise RuntimeError(f'Corruption survived: {label}')


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
    result = series(1)
    for _ in range(exponent):
        result = mul(result, a)
    return result


def real(a):
    return [G(x.re) for x in a]


def boundary_reciprocal(slope):
    return series(V, G(0, slope), C2*slope**2, 0, C4*slope**4)


def trace_envelope(r, ua, ub, label):
    s, marked = 8-r, series(D-1)
    trace = add(scale(ua, r+1), scale(ub, s+1))
    determinant = scale(mul(ua, ub), 9)
    disc = square_root(sub(mul(trace, trace), scale(determinant, 4)))
    near, far = scale(sub(trace, disc), Q(1, 2)), scale(add(trace, disc), Q(1, 2))
    for name, q in [('near', near), ('far', far)]:
        check(label+':root:'+name, add(sub(mul(q, q), mul(trace, q)), determinant), series())
    za, zb = sub(marked, inverse(ua)), sub(marked, inverse(ub))
    linear = scale(add(add(scale(za, s+1), scale(zb, r+1)), scale(marked, 8)), -1)
    constant = add(mul(za, zb), mul(marked, add(scale(zb, r), scale(za, s))))
    q2 = add(add(scale(mul(marked, marked), 9), mul(linear, marked)), constant)
    q1 = sub(scale(linear, -1), scale(marked, 18))
    check(label+':original-derivative-trace', scale(mul(q1, inverse(q2)), -1), trace)
    check(label+':original-derivative-determinant', scale(inverse(q2), 9), determinant)
    for name, u, z in [('a', ua, za), ('b', ub, zb)]:
        delta = sub(u, series(V))
        check(label+':reciprocal-circle:'+name,
              add(scale(real(delta), 2), scale(mul(delta, [x.conjugate() for x in delta]), B)), series())
        check(label+':original-unit-circle:'+name,
              mul(z, [x.conjugate() for x in z]), series(1))
    aa, bb, nn = sub(ua, series(V)), sub(ub, series(V)), sub(near, series(V))
    moments = {}
    for k in range(1, 5):
        moments[k] = add(add(scale(power(aa, k), r-1), scale(power(bb, k), s-1)), power(nn, k))
    energy = add(scale(mul(aa, [x.conjugate() for x in aa]), r),
                 scale(mul(bb, [x.conjugate() for x in bb]), s))
    trace_gap = scale(add(scale(real(aa), r), scale(real(bb), s)), 2)
    envelope = add(trace_gap, scale(real(moments[2]), -D/2))
    envelope = add(envelope, scale(real(moments[3]), D**2/6))
    envelope = add(envelope, scale(real(moments[4]), -(D**3)/8))
    envelope = add(envelope, scale(power(real(moments[1]), 2), D/14))
    total = add(add(scale(modulus(ua), r-1), scale(modulus(ub), s-1)),
                add(modulus(near), modulus(far)))
    actual = sub(total, series(16*V))
    real_square = add(add(scale(power(real(aa), 2), r-1), scale(power(real(bb), 2), s-1)), power(real(nn), 2))
    variance = sub(real_square, scale(power(real(moments[1]), 2), Q(1, 7)))
    check(label+':actual-minus-envelope', sub(actual, envelope), scale(variance, D/2))
    records.append([label, encode(actual), encode(energy), encode(envelope), encode(variance)])
    return actual, energy, envelope, moments, variance


def analytic_coefficients():
    # Credited scalar contour formulas, applied to u=v+i theta t+c2 theta^2 t^2+c4 theta^4 t^4.
    result = {}
    for name, mu4, mu22 in [('mu4', Q(1), Q(0)), ('mu22', Q(0), Q(1))]:
        t4 = mu4/2+mu22/32
        coupling = mu4/8-mu22/64
        norm_square = mu22/64
        m24 = C2**2*(t4+2*coupling+norm_square)
        m24 = m24+Q(9, 4)*C2*D*(3*coupling+norm_square)-Q(9, 32)*D**2*coupling+Q(81, 64)*D**2*norm_square
        m34 = -3*C2*(t4+coupling)-Q(27, 8)*D*coupling
        m44 = t4
        h4 = 2*C4*mu4-D*m24/2+D**2*m34/6-D**3*m44/8
        result[name] = h4-KAPPA*C2**2*mu4
    r = Q(7, 8)*C2+Q(9, 64)*D
    result['mu22'] = result['mu22']+D*r**2/14
    return result, r


def run():
    coeffs, near_trace = analytic_coefficients()
    alpha = -(D**3)*(96*D**2-196*D+67)/512
    beta = D**3*(168*D**2-350*D-55)/14336
    ktrace = D**3*(3792*D**2-7728*D+2991)/28672
    ksingleton = D**3*(516*D**2-528*D-393)/7168
    check('generic-analytic-mu4', coeffs['mu4'], alpha)
    check('generic-analytic-mu22-with-cauchy', coeffs['mu22'], beta)
    check('generic-moment-envelope', -alpha*Q(43, 56)-beta, ktrace)
    check('generic-singleton-variance-defect', ktrace-ksingleton, Q(27, 448)*D**3*(D-Q(13, 8))**2)
    check('generic-quadratic-disk-cancellation', Q(3, 8)*D-B, KAPPA)
    check('cutoff-trace-coefficient', near_trace.evaluate(V0), Q(-39, 1024))
    check('cutoff-alpha', alpha.evaluate(V0), Q(-2197, 131072))
    check('cutoff-beta', beta.evaluate(V0), Q(-3165877, 58720256))
    check('cutoff-sharp-envelope', ktrace.evaluate(V0), CMAX)
    check('cutoff-cauchy-gain', (D*near_trace**2/14).evaluate(V0), Q(19773, 117440512))
    check('alpha-sign-polynomial-at-cutoff', (96*D**2-196*D+67).evaluate(V0), Q(2))
    check('alpha-sign-derivative-at-cutoff', (192*D-196).evaluate(V0), Q(116))
    check('ktrace-sign-polynomial-at-cutoff', (3792*D**2-7728*D+2991).evaluate(V0), Q(1785, 4))
    controls = {}
    for r in range(1, 8):
        s = 8-r
        ua, ub = boundary_reciprocal(s), boundary_reciprocal(-r)
        actual, energy, envelope, moments, variance = trace_envelope(r, ua, ub, f'circle:r{r}')
        mu2, mu4 = Q(8*r*s), Q(r*s**4+s*r**4)
        if r in (1, 4):
            check(f'circle:r{r}:determining-moment-ratio', mu4/mu2**2,
                  Q(43, 56) if r == 1 else Q(1, 8))
        check(f'circle:r{r}:energy-order2', energy[2], G(mu2))
        check(f'circle:r{r}:energy-order4', energy[4], G(C2**2*mu4))
        check(f'circle:r{r}:envelope-order2', envelope[2], G(KAPPA*mu2))
        normalized = sub(envelope, scale(energy, KAPPA))
        check(f'circle:r{r}:analytic-order4', normalized[4], G(alpha*mu4+beta*mu2**2))
        check(f'circle:r{r}:near-real-trace-order2', real(moments[1])[2], G(near_trace*mu2))
        for order in (0, 1, 3):
            check(f'circle:r{r}:gap-order{order}', actual[order], G())
        controls[r] = (actual, energy, envelope, moments, variance)
    actual, energy, envelope, moments, variance = controls[1]
    check('singleton-circle-generic-quartic', sub(actual, scale(energy, KAPPA))[4], G(-ksingleton*56**2))
    check('singleton-circle-variance-quartic', variance[4], G(378*D**2*(D-Q(13, 8))**2))
    check('singleton-cutoff-cauchy-saturation', variance[4].re.evaluate(V0), Q(0))
    # Reproduce the useful actual angular singleton/seven baseline by a different input coordinate.
    marked = series(D-1)
    ua = inverse(add(marked, exponential_i(series(0, 7))))
    ub = inverse(add(marked, exponential_i(series(0, -1))))
    actual, energy, envelope, _, variance = trace_envelope(1, ua, ub, 'angular-singleton-baseline')
    check('angular-singleton-generic-quartic', sub(actual, scale(energy, KAPPA))[4], G(-ksingleton*V**8*56**2))
    check('angular-singleton-envelope-quartic', sub(envelope, scale(energy, KAPPA))[4], G(-ktrace*V**8*56**2))
    reject('drop-cauchy-gain', CMAX, CMAX+Q(19773, 117440512))
    reject('six-near-roots', D*near_trace**2/14, D*near_trace**2/12)
    reject('wrong-fourth-moment-bound', ktrace, -alpha-beta)
    reject('omit-energy-quartic', coeffs['mu4'], coeffs['mu4']+KAPPA*C2**2)
    reject('corrupt-alpha-linear-term', alpha, -(D**3)*(96*D**2-197*D+67)/512)
    reject('wrong-singleton-variance', ktrace-ksingleton, Q(27, 448)*D**3*(D-Q(13, 8)))
    payload = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    manifest = {
        'agent': 'six-sendov-3', 'role': 'researcher',
        'arithmetic': 'Q[v,v^-1][i][t]/(t^5), real v>0',
        'symbolic_reciprocal_circle_profiles': 7,
        'actual_angular_baseline_profiles': 1,
        'balanced_symmetric_quartic_basis': ['mu4', 'mu2^2'],
        'determining_profile_moment_ratios': [[43, 56], [1, 8]],
        'checks': len(checks), 'mutation_controls': 6,
        'alpha_laurent': encode(alpha), 'beta_laurent': encode(beta),
        'ktrace_laurent': encode(ktrace),
        'cutoff_sharp_coefficient': encode(CMAX),
        'cutoff_cauchy_gain': encode(Q(19773, 117440512)),
        'records_sha256': sha256(payload).hexdigest(),
        'unformalized': ['uniform weighted analytic remainders',
                         'all-disk comparison and absorption', 'basin supremum argument'],
    }
    fixture = Path(__file__).with_name('expected.json')
    if fixture.exists():
        check('complete-fixture', manifest, json.loads(fixture.read_text()))
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == '__main__':
    if len(sys.argv) != 1:
        raise SystemExit('Usage: python3 -I -B verify.py')
    run()
