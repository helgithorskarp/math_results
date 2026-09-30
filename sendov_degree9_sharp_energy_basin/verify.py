#!/usr/bin/env python3
"""Exact varying-a algebra in Q[v,v^-1][i][t]/(t^5), v=(1+a)^-1.

Author implementation; no other research source is imported. Symbolic
identities control the two-block examples and the second-order constants.
The all-disk spectral and completeness bridges remain written arguments.
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
A = V**(-1)-1
KAPPA = V**(-2)-Q(13, 8)*V**(-1)
V0 = Q(8, 13)
RADIAL0, MEAN0 = Q(128, 169), Q(40, 2197)
P8, CMAX = Q(10985, 33554432), Q(560235, 8388608)
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


def evaluate(value, v):
    return [G(x.re.evaluate(v), x.im.evaluate(v)) for x in value]


def two_block(r, phi_a, phi_b, tau_a, tau_b, shift, label):
    s = 8-r
    marked = add(series(A), shift)
    center = inverse(add(series(1), marked))
    radial_a = mul(sub(series(1), tau_a), exponential_i(phi_a))
    radial_b = mul(sub(series(1), tau_b), exponential_i(phi_b))
    za, zb = scale(radial_a, -1), scale(radial_b, -1)
    ua, ub = inverse(add(marked, radial_a)), inverse(add(marked, radial_b))
    trace = add(scale(ua, r+1), scale(ub, s+1))
    determinant = scale(mul(ua, ub), 9)
    disc = square_root(sub(mul(trace, trace), scale(determinant, 4)))
    near = scale(sub(trace, disc), Q(1, 2))
    far = scale(add(trace, disc), Q(1, 2))
    for which, q in [('near', near), ('far', far)]:
        check(label+':reciprocal-quadratic:'+which,
              add(sub(mul(q, q), mul(trace, q)), determinant), series())
    # Direct differentiation in the original z coordinate, followed by z=a-1/q.
    linear = scale(add(add(scale(za, s+1), scale(zb, r+1)), scale(marked, 8)), -1)
    constant = add(mul(za, zb), mul(marked, add(scale(zb, r), scale(za, s))))
    q2 = add(add(scale(mul(marked, marked), 9), mul(linear, marked)), constant)
    q1 = sub(scale(linear, -1), scale(marked, 18))
    check(label+':direct-derivative-trace', scale(mul(q1, inverse(q2)), -1), trace)
    check(label+':direct-derivative-determinant', scale(inverse(q2), 9), determinant)
    total = add(add(scale(modulus(ua), r-1), scale(modulus(ub), s-1)),
                add(modulus(near), modulus(far)))
    gap = sub(total, scale(center, 16))
    ea, eb = sub(ua, center), sub(ub, center)
    energy = add(scale(mul(ea, [x.conjugate() for x in ea]), r),
                 scale(mul(eb, [x.conjugate() for x in eb]), s))
    records.append([label, encode(gap), encode(energy)])
    return gap, energy


def run():
    c2 = V**2/2-V**3
    check('generic-angular-second-order', 2*c2+Q(3, 8)*V**3, KAPPA*V**4)
    check('cutoff-kappa', KAPPA.evaluate(V0), Q(0))
    check('cutoff-radial', (2*V**2).evaluate(V0), RADIAL0)
    check('cutoff-mean', (Q(5, 64)*V**3).evaluate(V0), MEAN0)
    check('angular-maximum', 204*P8, CMAX)
    pure_profiles, second_profiles, mixed_profiles = 0, 0, 0
    pure = {}
    for r in range(1, 8):
        s, mu2 = 8-r, Q(8*r*(8-r))
        label = f'pure:r{r}'
        gap, energy = two_block(r, series(0, s), series(0, -r),
                                series(), series(), series(), label)
        check(label+':energy-order2', energy[2], G(V**4*mu2))
        mu4 = Q(r*s**4+s*r**4)
        check(label+':energy-order4-from-original-distance', energy[4],
              G(V**4*(A*V**2-Q(1, 12))*mu4))
        check(label+':gap-order2', gap[2], G(KAPPA*V**4*mu2))
        for order in (0, 1, 3):
            check(label+f':gap-order{order}', gap[order], G())
        coefficient = P8*(224*Q(64-3*r*s, 8*r*s)+32)
        check(label+':cutoff-quartic', gap[4].re.evaluate(V0),
              -coefficient*V0**8*mu2**2)
        pure[r] = (gap, energy)
        pure_profiles += 1
        for k in range(4):
            sa, sb = Q(k-2, 2), Q(3-k, 3)
            ra, rb = Q(k, 9), Q(3-k, 10)
            label = f'second:r{r}:k{k}'
            gap, energy = two_block(r, series(0, sa), series(0, sb),
                                    series(0, 0, ra), series(0, 0, rb), series(), label)
            expected = 2*V**2*(r*ra+s*rb)+KAPPA*V**4*(r*sa**2+s*sb**2)
            expected = expected+Q(5, 64)*V**3*(r*sa+s*sb)**2
            check(label+':generic-second-order', gap[2], G(expected))
            check(label+':gap-order1', gap[1], G())
            second_profiles += 1
        for k in range(3):
            ba, bb = Q(k-1, 3), Q(2-k, 5)
            ca, cb = Q(2-k, 7), Q(k+1, 11)
            ra, rb = Q(k, 4), Q(2-k, 6)
            rate = (Q(0), Q(1, 37), Q(3, 5))[k]
            label = f'joint:r{r}:k{k}'
            gap, energy = two_block(r, series(0, s, ba, ca), series(0, -r, bb, cb),
                                    series(0, 0, 0, 0, ra), series(0, 0, 0, 0, rb),
                                    series(0, 0, rate, 0, Q(k-1, 17)), label)
            inward, mean = r*ra+s*rb, r*ba+s*bb
            expected = Q(13, 8)*rate*V0**4*mu2+RADIAL0*inward+MEAN0*mean**2
            expected = expected-coefficient*V0**8*mu2**2
            cutoff_gap = evaluate(gap, V0)
            for order in range(4):
                check(label+f':cutoff-gap-order{order}', cutoff_gap[order], G())
            check(label+':cutoff-gap-order4', cutoff_gap[4], G(expected))
            check(label+':cutoff-energy-order2', evaluate(energy, V0)[2], G(V0**4*mu2))
            mixed_profiles += 1
    # A symbolic variable-base marked-motion control, not a finite a sample.
    eta = Q(2, 7)
    moved_gap, moved_energy = two_block(1, series(0, 7), series(0, -1),
                                       series(), series(), series(0, 0, eta), 'variable-base-motion')
    base_gap, base_energy = pure[1]
    check('generic-marked-motion-gap', moved_gap[4]-base_gap[4],
          G(-eta*V**2*base_gap[2].re.derivative()))
    check('generic-marked-motion-energy', moved_energy[4]-base_energy[4],
          G(-eta*V**2*base_energy[2].re.derivative()))
    # Full varying-a normalized quartic of the singleton/seven example.
    singleton_k = -(base_gap[4].re-KAPPA*base_energy[4].re)/(V**8*56**2)
    check('singleton-generic-quartic-formula', singleton_k,
          V**(-3)*(516*V**(-2)-528*V**(-1)-393)/7168)
    check('singleton-cutoff-quartic', singleton_k.evaluate(V0), CMAX)
    check('sharp-energy-radius-constant', 1/CMAX, Q(8388608, 560235))
    critical_rate = CMAX*V0**4*56/Q(13, 8)
    crossing_signs = []
    for numerator in (1, 3):
        eta = Q(numerator, 2)*critical_rate
        label = f'crossing-control:{numerator}'
        gap, energy = two_block(1, series(0, 7), series(0, -1),
                                series(), series(), series(0, 0, eta), label)
        observed = gap[4].re.evaluate(V0)
        expected = (Q(numerator, 2)-1)*CMAX*V0**8*56**2
        check(label+':quartic-sign', observed, expected)
        if (observed < 0) != (numerator == 1):
            raise RuntimeError('Sharp crossing sign reversed')
        crossing_signs.append([numerator, encode(observed)])
    reject('omit-marked-radius-term', moved_gap[4], base_gap[4])
    reject('halve-angular-second-order', 2*c2+Q(3, 8)*V**3, KAPPA*V**4/2)
    reject('replace-mean-constant', Q(5, 64)*V**3, V**3/128)
    reject('omit-energy-fourth-order', singleton_k, -base_gap[4].re/(V**8*56**2))
    reject('wrong-basin-reciprocal', Q(8388608, 560235), CMAX)
    reject('wrong-singleton-quartic', singleton_k.evaluate(V0), CMAX+Q(1, 8388608))
    payload = json.dumps(records, sort_keys=True, separators=(',', ':')).encode()
    manifest = {
        'agent': 'six-sendov-3', 'role': 'researcher',
        'arithmetic': 'Q[v,v^-1][i][t]/(t^5); v positive and real',
        'symbolic_pure_profiles': pure_profiles,
        'symbolic_second_order_profiles': second_profiles,
        'symbolic_joint_profiles': mixed_profiles,
        'checks': len(checks), 'mutation_controls': 6,
        'sharp_energy_radius_constant': encode(1/CMAX),
        'singleton_varying_a_quartic_laurent': encode(singleton_k),
        'singleton_critical_a_rate_for_slopes_7_minus1': encode(critical_rate),
        'crossing_sign_controls': crossing_signs,
        'records_sha256': sha256(payload).hexdigest(),
        'unformalized': ['all-disk spectral comparison', 'uniform parameter bridge',
                         'basin completeness', 'analytic implicit-function argument'],
    }
    fixture = Path(__file__).with_name('expected.json')
    if fixture.exists():
        check('complete-fixture', manifest, json.loads(fixture.read_text()))
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == '__main__':
    if len(sys.argv) != 1:
        raise SystemExit('Usage: python3 -I -B verify.py')
    run()
