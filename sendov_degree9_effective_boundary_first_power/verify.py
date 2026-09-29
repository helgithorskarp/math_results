#!/usr/bin/env python3
"""Exact symbolic identities and constants for the effective annulus.

No numerical roots, external packages, sampling proof, or imported checker.
The ordinary analytic proof and its explicit local dependency are in PROOF.md.
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb


N = 8
ZERO = (0,) * N


class Checks:
    def __init__(self):
        self.count = 0

    def require(self, condition, name):
        if not condition:
            raise AssertionError(name)
        self.count += 1


def add(p, q):
    out = p.copy()
    for monomial, coefficient in q.items():
        out[monomial] = out.get(monomial, F(0)) + coefficient
        if not out[monomial]:
            del out[monomial]
    return out


def scale(p, c):
    return {m: c*v for m, v in p.items() if c*v}


def mul(p, q):
    out = {}
    for m, c in p.items():
        for n, d in q.items():
            exponent = tuple(a+b for a, b in zip(m, n))
            out[exponent] = out.get(exponent, F(0)) + c*d
    return {m: c for m, c in out.items() if c}


def total(polynomials):
    out = {}
    for p in polynomials:
        out = add(out, p)
    return out


def product(polynomials):
    out = {ZERO: F(1)}
    for p in polynomials:
        out = mul(out, p)
    return out


def symmetric(variables, k):
    return total(product(variables[i] for i in indices)
                 for indices in combinations(range(len(variables)), k))


def complex_mul(p, q):
    real = add(mul(p[0], q[0]), scale(mul(p[1], q[1]), -1))
    imaginary = add(mul(p[0], q[1]), mul(p[1], q[0]))
    return real, imaginary


def complex_symmetric(variables, k):
    real, imaginary = {}, {}
    for indices in combinations(range(N), k):
        term = ({ZERO: F(1)}, {})
        for i in indices:
            term = complex_mul(term, variables[i])
        real, imaginary = add(real, term[0]), add(imaginary, term[1])
    return real, imaginary


def check_newton(lhs, rhs):
    if lhs != rhs:
        raise AssertionError('Newton certificate identity failed')


def symbolic_checks(checks):
    variables = []
    for i in range(N):
        monomial = tuple(int(j == i) for j in range(N))
        variables.append({monomial: F(1)})
    e1, e2, e3 = (symmetric(variables, k) for k in [1, 2, 3])
    lhs = add(scale(mul(e2, e2), 12), scale(mul(e1, e3), -21))
    rhs = {}
    for i, j in combinations(range(N), 2):
        difference = add(variables[i], scale(variables[j], -1))
        remaining = [variables[k] for k in range(N) if k not in [i, j]]
        bracket = add(total(mul(p, p) for p in remaining),
                      symmetric(remaining, 2))
        rhs = add(rhs, mul(mul(difference, difference), bracket))
    check_newton(lhs, rhs)
    checks.require(len(lhs) == 266, 'Newton expanded support size')
    for monomial, coefficient in lhs.items():
        pattern = sorted((i for i in monomial if i), reverse=True)
        expected = {(2, 2): 12, (2, 1, 1): 3, (1, 1, 1, 1): -12}
        checks.require(tuple(pattern) in expected
                       and coefficient == expected[tuple(pattern)],
                       'Newton grouped monomial coefficient')

    mutated = add(scale(mul(e2, e2), 12), scale(mul(e1, e3), -20))
    rejected = False
    try:
        check_newton(mutated, rhs)
    except AssertionError:
        rejected = True
    checks.require(rejected, 'changed Newton coefficient must be rejected')

    half = {ZERO: F(1, 2)}
    shifted = [add(p, scale(half, -1)) for p in variables]
    x1, x2, x3 = (symmetric(shifted, k) for k in [1, 2, 3])
    x2_formula = add(add(e2, scale(e1, F(-7, 2))), {ZERO: F(7)})
    x3_formula = add(add(add(e3, scale(e2, -3)),
                         scale(e1, F(21, 4))), {ZERO: F(-7)})
    checks.require(x2 == x2_formula, 'shifted second symmetric identity')
    checks.require(x3 == x3_formula, 'shifted third symmetric identity')
    difference_formula = add(add(add(e3, scale(e2, -4)),
                                scale(e1, F(35, 4))), {ZERO: F(-14)})
    checks.require(add(x3, scale(x2, -1)) == difference_formula,
                   'shifted saturation difference')
    variance64 = add(scale(total(mul(p, p) for p in shifted), 8),
                     scale(mul(x1, x1), -1))
    checks.require(variance64 == add(scale(mul(x1, x1), 7), scale(x2, -16)),
                   'exact variance identity')

    vertical = [(half, p) for p in variables]
    u2, u3 = (complex_symmetric(vertical, k)[0] for k in [2, 3])
    checks.require(u2 == add({ZERO: F(7)}, scale(e2, -1)),
                   'vertical reciprocal e2 real part')
    checks.require(u3 == add({ZERO: F(7)}, scale(e2, -3)),
                   'vertical reciprocal e3 real part')
    checks.require(u3 == add(scale(u2, 3), {ZERO: F(-14)}),
                   'vertical reciprocal saturation identity')


def bound_checks(checks):
    eta0 = F(1, 10**6)
    h = F(1, 100)
    gamma = F(1, 160)
    cauchy_sum = sum((F(comb(8, k), k+1) * F(1, 7)**k
                      for k in range(1, 9)), F(0))
    checks.require(cauchy_sum == F(41980912, 51883209) < 1,
                   'reciprocal other-root Cauchy radius')
    checks.require(7*(1+gamma*eta0) < 8, 'other-root reciprocal radius eight')
    checks.require(8+eta0/20-F(7, 2) < 5, 'critical reciprocal radius five')
    checks.require(1-eta0 > F(99, 100), 'real root lower endpoint')
    checks.require(64/F(99, 100) < 65, 'negative root real defect')
    checks.require(7*65+F(1, 40) < 456, 'positive root real defect')
    checks.require(2*8*65+F(1, 40) < 1100, 'root real L1 defect')
    checks.require(8+456*eta0 < 9, 'projected reciprocal radius nine')
    checks.require(2*8*64-8 == 1016, 'critical real-sum bound numerator')
    checks.require(1016/F(99, 100) < 1030, 'critical real-sum deficit')
    checks.require(1030+F(1, 20) < 1100, 'angular total defect')
    checks.require(F(1100, 8) < 140, 'mean angular defect')
    checks.require(F(1030, 8) < 130 and gamma < 130, 'mean modulus drift')

    checks.require((1+h)**8 < 2, 'polar prefactor upper bound')
    checks.require(16/(1-h)**2 < 17, 'polar exponent upper coefficient')
    checks.require(17*25 == 425, 'polar exponent total bound')
    checks.require(F(425**2) < 200000, 'exponential quartic remainder')
    # Clear denominators in the exact lower loss ratio. Coefficients
    # beyond degree one must be 1045/4 and 1539, respectively.
    # Scalar polynomials are embedded in the first variable.
    one, z, z2, z3 = ({ZERO: F(1)}, {(1,)+(0,)*7: F(1)},
                     {(2,)+(0,)*7: F(1)}, {(3,)+(0,)*7: F(1)})
    left = add(add(one, scale(z, -1)), scale(z2, F(1, 4)))
    right = mul(add(one, scale(z, -19)),
                add(add(one, scale(z, 18)), scale(z2, 81)))
    checks.require(add(left, scale(right, -1))
                   == add(scale(z2, F(1045, 4)), scale(z3, 1539)),
                   'cleared polar lower-loss identity')
    checks.require(F(1045, 4) > 0 and 1539 > 0,
                   'nonnegative lower-loss coefficients')
    checks.require(8+19 <= 30, 'combined polar loss coefficient')
    radius = 1+h+h*h
    cubic_tail = (8*gamma+28*(1+h)*(2+h+h*h)
                  + sum((F(comb(8, k))*h**(k-3)*radius**k
                         for k in range(3, 9)), F(0)))
    checks.require(cubic_tail < 128, 'uniform finite-binomial cubic tail')
    checks.require(F(3, 16)*128 == 24, 'variance cubic-tail factor')
    checks.require(F(3, 16)*200000 == 37500, 'variance quartic-tail factor')
    variance_upper = ((1+F(3, 2)*gamma+24*eta0+37500*eta0**2)
                      /(1-30*eta0))
    checks.require(variance_upper == F(80751923, 79997600) < F(5, 4),
                   'finite collapsed-family variance exclusion')

    checks.require(comb(7, 1)*9*1100 == 69300,
                   'e2 reciprocal projection error')
    checks.require(comb(7, 2)*9**2*1100 == 1871100,
                   'e3 reciprocal projection error')
    checks.require(4*(1871100+3*69300) == 8316000,
                   'complex saturation error')
    checks.require(2*comb(7, 1)*5*1100 == 77000, 'e2 angular error')
    checks.require(3*comb(7, 2)*25*1100 == 1732500, 'e3 angular error')
    defect = 8316000+1732500+4*77000+F(35, 4)*1100
    checks.require(defect == 10366125 < 11000000,
                   'real shifted saturation error')
    checks.require(F(7, 16)*(4-1100*eta0)**2-5 > 1,
                   'noncollapsed Newton branch e2 lower bound')
    checks.require(F(7, 16)*(4+eta0/20)**2 < 8,
                   'Newton e2 upper bound')
    checks.require(F(7, 4)*(4+eta0/20) < 8,
                   'Newton coefficient upper bound')
    checks.require(F(7, 4)*1100*8+8*11000000 < 90000000,
                   'Newton saturation quantitative defect')
    checks.require(F(7, 64)*(F(2, 5)+eta0/400) < 1,
                   'variance mean-drift coefficient')
    checks.require(F(90000000, 4)+1 < 23000000,
                   'quantitative modulus variance bound')
    checks.require(8*(23000000+130**2*eta0+280) < 190000000,
                   'reciprocal energy bound')
    checks.require(16*eta0+8*190000000 < 1600000000,
                   'critical energy bound')

    threshold = F(1, 10000)
    checks.require(8-F(1, 20) > 6, 'relaxed local failure coefficient')
    checks.require(F(8, 3)+F(16, 3)*h < 3, 'eta at most three critical radii')
    checks.require(F(1, 16)-72*threshold == F(553, 10000) > F(1, 20),
                   'local first-moment gain')
    checks.require(F(1, 14)-182*threshold == F(1863, 35000) > F(1, 20),
                   'local critical-energy gain')
    checks.require(F(3, 40) > F(1, 20), 'strict local margin contradiction')
    checks.require(8/(F(3, 4)+threshold) > 8+F(1, 20),
                   'central local-root branch')
    annulus_width = F(1, 10**18)
    checks.require(annulus_width <= eta0, 'annulus within stability domain')
    checks.require(1600000000*annulus_width == F(1, 625000000)
                   < threshold**2, 'explicit annulus feeds cluster theorem')


def controls(checks):
    for eta in [F(1, 10**6), F(1, 10**18)]:
        a = 1-eta
        # z^9-a^9, critical points all zero.
        checks.require(F(8)/a > 8+eta/20, 'interior binomial margin')
        # (z-a)(z+1)^8: two exact critical locations and variance.
        collapsed_sum = F(16)/(a+1)
        checks.require(collapsed_sum-8 == 8*eta/(a+1),
                       'collapsed-family exact first-power slope')
        checks.require(collapsed_sum > 8+eta/20,
                       'collapsed-family excludes relaxed failure')
        r = [F(1)/(a+1)]*7+[F(9)/(a+1)]
        mean = sum(r, F(0))/8
        variance = sum(((x-mean)**2 for x in r), F(0))/8
        checks.require(variance == F(7)/(a+1)**2 > F(5, 4),
                       'collapsed-family exact variance control')
    checks.require(F(7, 4) > F(5, 4), 'boundary collapsed variance gap')
    checks.require(0 < F(5, 4), 'boundary binomial variance zero')


def main():
    checks = Checks()
    symbolic_checks(checks)
    bound_checks(checks)
    controls(checks)
    print(f'PASS: {checks.count} exact checks; Newton mutation rejected.')


if __name__ == '__main__':
    main()
