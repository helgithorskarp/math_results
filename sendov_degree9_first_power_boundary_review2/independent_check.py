"""Independent exact algebra for six-reviewer-2's ordinary analytic audit.

Standard-library Python 3.11. No imports from the target contribution.
Formal jets check identities, not analytic remainder bounds or compactness.
"""
from fractions import Fraction as F
from math import factorial
import hashlib
import json
from pathlib import Path
import sys


class Ring:
    def __init__(self, names, weights, cap):
        self.names, self.weights, self.cap = names, weights, cap
        self.zero_key = (0,) * len(names)

    def constant(self, value):
        return Poly(self, {self.zero_key: F(value)})

    def variable(self, index):
        key = list(self.zero_key)
        key[index] = 1
        return Poly(self, {tuple(key): F(1)})


class Poly:
    def __init__(self, ring, terms):
        self.ring = ring
        self.terms = {k: F(v) for k, v in terms.items() if v and
                      sum(a*b for a, b in zip(k, ring.weights)) <= ring.cap}

    def coerce(self, other):
        if isinstance(other, Poly):
            if other.ring is not self.ring:
                raise ValueError('mixed rings')
            return other
        return self.ring.constant(other)

    def __add__(self, other):
        other = self.coerce(other)
        terms = self.terms.copy()
        for k, v in other.terms.items():
            terms[k] = terms.get(k, 0) + v
        return Poly(self.ring, terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly(self.ring, {k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + -self.coerce(other)

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        other = self.coerce(other)
        terms = {}
        for k, v in self.terms.items():
            for l, w in other.terms.items():
                key = tuple(a+b for a, b in zip(k, l))
                if sum(a*b for a, b in zip(key, self.ring.weights)) <= self.ring.cap:
                    terms[key] = terms.get(key, 0) + v*w
        return Poly(self.ring, terms)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1 / F(scalar))

    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError('use unit_power for fractional or negative powers')
        result = self.ring.constant(1)
        for _ in range(exponent):
            result = result*self
        return result

    def derivative(self, index):
        terms = {}
        for k, v in self.terms.items():
            if k[index]:
                key = list(k)
                key[index] -= 1
                terms[tuple(key)] = v*k[index]
        return Poly(self.ring, terms)

    def at_power(self, index, power):
        terms = {}
        for k, v in self.terms.items():
            if k[index] == power:
                key = list(k)
                key[index] = 0
                terms[tuple(key)] = v
        return Poly(self.ring, terms)

    def integral_01(self, index):
        terms = {}
        for k, v in self.terms.items():
            key = list(k)
            key[index] = 0
            key = tuple(key)
            terms[key] = terms.get(key, 0) + v/F(k[index]+1)
        return Poly(self.ring, terms)

    def encode(self):
        return [{'powers': list(k), 'coefficient': str(v)}
                for k, v in sorted(self.terms.items())]


def equal(actual, expected, label):
    expected = actual.coerce(expected)
    if actual.terms != expected.terms:
        raise ValueError(label)


def positive_order(poly):
    if any(sum(a*b for a, b in zip(k, poly.ring.weights)) == 0
           for k in poly.terms):
        raise ValueError('series argument must have positive order')


def unit_power(base, exponent):
    u = base - 1
    positive_order(u)
    result, term, coefficient = base.ring.constant(1), base.ring.constant(1), F(1)
    for k in range(1, base.ring.cap+1):
        term = term*u
        coefficient *= (F(exponent)-k+1)/k
        result += coefficient*term
    return result


def exponential(poly):
    positive_order(poly)
    return sum((poly**k)/factorial(k) for k in range(poly.ring.cap+1))


def rejected(check):
    try:
        check()
    except ValueError:
        return
    raise AssertionError('mutation unexpectedly accepted')


def certificate():
    # A full second-order Taylor jet in 17 independent real coordinates.
    ring = Ring(['delta'] + [f'{c}{j}' for j in range(8) for c in 'xy'],
                [1]*17, 2)
    d = ring.variable(0)
    xs = [ring.variable(1+2*j) for j in range(8)]
    ys = [ring.variable(2+2*j) for j in range(8)]
    inverse = [unit_power((1-d-x)**2+y**2, F(-1, 2)) for x, y in zip(xs, ys)]
    for x, y, inv in zip(xs, ys, inverse):
        equal(inv**2*((1-d-x)**2+y**2), 1, 'inverse-distance jet')
    mean = sum(inverse)/8
    sx, sy = sum(xs), sum(ys)
    # Derive c8,c7 by multiplying the linear derivative factors through e2.
    e2re = sum(xs[i]*xs[j]-ys[i]*ys[j] for i in range(8) for j in range(i+1, 8))
    e2im = sum(xs[i]*ys[j]+ys[i]*xs[j] for i in range(8) for j in range(i+1, 8))
    c8re, c8im = -F(9, 8)*sx, -F(9, 8)*sy
    c7re, c7im = F(9, 7)*e2re, F(9, 7)*e2im
    q = sum(x*x+y*y for x, y in zip(xs, ys))
    p2re, p2im = sum(x*x-y*y for x, y in zip(xs, ys)), 2*sum(x*y for x, y in zip(xs, ys))
    equal(p2re, F(64, 81)*(c8re**2-c8im**2)-F(14, 9)*c7re, 'Newton real')
    equal(p2im, F(128, 81)*c8re*c8im-F(14, 9)*c7im, 'Newton imaginary')
    claimed = 1+d-c8re/9+q/32-F(7, 48)*c7re+F(2, 27)*(c8re**2-c8im**2)
    equal(mean-claimed, d*d+d*sx/4, 'local coefficient expansion')
    rejected(lambda: equal(mean-claimed+d*sy, d*d+d*sx/4, 'local mutation'))

    # Expand the exact polar defect integrand, not a supplied coefficient list.
    polar = Ring(['delta', 'sigma', 'd_scaled', 'v', 't'], [1, 0, 0, 0, 0], 2)
    delta, sigma, ds, v, t = [polar.variable(i) for i in range(5)]
    a, b, mu = 1-delta, 2*delta-delta**2, 1-sigma*delta
    radius = 8*mu-F(7, 2)*unit_power(1-delta/2, -1)
    denom_inverse = unit_power(a+b*t*radius, -2)
    exponent = -8*(a*b*t*ds*delta+b*b*t*t*v/2)*denom_inverse
    integrand = (a+b*mu*t)**8 * exponential(exponent)
    integral = integrand.integral_01(4)
    budget = 1+8*(F(2, 3)-sigma-ds-F(2, 3)*v)*delta**2
    equal(integral, budget, 'integrated polar budget')
    rejected(lambda: equal(integral, budget+v*delta**2, 'variance mutation'))

    # Independently generate the reciprocal parity transform used by equality classification.
    degrees = list(range(4, 17))
    for n in degrees:
        m = n-1
        parity = Ring(['X', 'A', 'B'], [1, 0, 0], m)
        X, A, B = [parity.variable(i) for i in range(3)]
        T = X**m+A*X**(m-2)
        if m >= 4:
            T += B*X**(m-4)
        transformed = (m+1)*T-(X+F(1, 2))*T.derivative(0)
        equal(transformed.at_power(0, m), 1, 'classification leading')
        equal(transformed.at_power(0, m-1), -F(m, 2), 'classification e1')
        equal(transformed.at_power(0, m-2), 3*A, 'classification e2')
        equal(transformed.at_power(0, m-3), -F(m-2, 2)*A, 'classification e3')

    # The strengthening uses an exact factorization on 1/2<x<1; no floating trigonometry.
    trig = Ring(['x'], [1], 2)
    x = trig.variable(0)
    A, B = 1+x, 2-2*x*x
    equal(A-B, (2*x-1)*(1+x), 'constraint denominator factorization')
    equal(6*A-9, 3*(2*x-1), 'constraint numerator factorization')
    equal(2*(6*A-9)-3*(A-B), 3*(2*x-1)*(1-x), 'trigonometric margin factorization')
    controls = []
    for alpha in [F(8, 9), F(15, 16), F(1)]:
        gamma, kappa = F(1, 2)-alpha/6, (8*alpha-7)/112
        assert kappa > 0
        assert F(1, 32)+(alpha/9-F(7, 48))*F(9, 14) == kappa
        controls.append({'alpha': str(alpha), 'gamma_ceiling': str(gamma),
                         'kappa_ceiling': str(kappa)})
    assert F(7, 20) < F(17, 48) < F(1, 2)
    assert 8*F(7, 20) == F(14, 5)
    rejected(lambda: equal(2*(6*A-9)-3*(A-B), 3*(2*x-1)*(1+x), 'factor mutation'))
    return {
        'reviewer': 'six-reviewer-2',
        'method': 'independent exact multivariate jets and reciprocal-parity transforms',
        'inverse_distance_coordinates': 17,
        'newton_components': 2,
        'integrated_polar_budget': integral.encode(),
        'classification_degree_controls': degrees,
        'strengthening_factorization': '2*(6*A-9)-3*(A-B)=3*(2*x-1)*(1-x)',
        'local_tradeoff_controls': controls,
        'annulus_gamma_ceiling': '17/48',
        'stronger_exact_gamma_ceiling': '1/3+1/(24*(1+cos(pi/9)))',
        'concrete_sum_slope': '14/5',
        'rejected_mutations': 3,
    }


def main():
    result = certificate()
    encoded = json.dumps(result, sort_keys=True, indent=2)+'\n'
    if sys.argv[1:] == ['--json']:
        print(encoded, end='')
        return
    if sys.argv[1:]:
        raise SystemExit('usage: independent_check.py [--json]')
    expected = Path(__file__).with_name('expected.json').read_text()
    if encoded != expected:
        raise SystemExit('expected certificate mismatch')
    print('PASS: 17-variable local jet; polar variance budget; 13 parity transforms; slope refinement; 3 mutations rejected.')
    print('certificate SHA256: '+hashlib.sha256(encoded.encode()).hexdigest())


if __name__ == '__main__':
    main()
