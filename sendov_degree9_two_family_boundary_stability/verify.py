#!/usr/bin/env python3
"""Exact certificate checks for degree-nine two-family boundary stability.

Standard library only. No floating-point roots, imported research checker,
sampling argument, solver, or external data. See PROOF.md for the universal
analytic proof and its two published quadratic-stability dependencies.
"""

from fractions import Fraction as F
from itertools import combinations
from math import comb


DIM = 16
ZERO = (0,) * DIM
ONE = {ZERO: F(1)}


class Checks:
    def __init__(self):
        self.count = 0
        self.mutations = 0

    def require(self, condition, name):
        if not condition:
            raise AssertionError(name)
        self.count += 1

    def identity(self, left, right, name):
        self.require(left == right, name)

    def reject_mutation(self, left, right, name):
        rejected = False
        try:
            if left != right:
                raise AssertionError(name)
        except AssertionError:
            rejected = True
        self.require(rejected, name + ' must be rejected')
        self.mutations += 1


def constant(value):
    return {ZERO: F(value)} if value else {}


def variable(index, exponent=1):
    return {tuple(exponent if j == index else 0 for j in range(DIM)): F(1)}


def add(p, q):
    result = p.copy()
    for m, c in q.items():
        result[m] = result.get(m, F(0)) + c
        if not result[m]:
            del result[m]
    return result


def scale(p, coefficient):
    return {m: coefficient*c for m, c in p.items() if coefficient*c}


def mul(p, q):
    result = {}
    for m, c in p.items():
        for n, d in q.items():
            exponent = tuple(a+b for a, b in zip(m, n))
            result[exponent] = result.get(exponent, F(0)) + c*d
    return {m: c for m, c in result.items() if c}


def total(polynomials):
    result = {}
    for p in polynomials:
        result = add(result, p)
    return result


def product(polynomials):
    result = ONE
    for p in polynomials:
        result = mul(result, p)
    return result


def power(p, exponent):
    return product(p for _ in range(exponent))


def symmetric(variables, k):
    return total(product(variables[i] for i in indices)
                 for indices in combinations(range(len(variables)), k))


def derivative(p, index):
    result = {}
    for m, c in p.items():
        if m[index]:
            n = tuple(v-int(j == index) for j, v in enumerate(m))
            result[n] = c*m[index]
    return result


def specialize(p, index, value):
    result = {}
    for m, c in p.items():
        n = tuple(0 if j == index else v for j, v in enumerate(m))
        result[n] = result.get(n, F(0)) + c*value**m[index]
    return {m: c for m, c in result.items() if c}


def complex_mul(p, q):
    return (add(mul(p[0], q[0]), scale(mul(p[1], q[1]), -1)),
            add(mul(p[0], q[1]), mul(p[1], q[0])))


def complex_symmetric(variables, k):
    real, imaginary = {}, {}
    for indices in combinations(range(len(variables)), k):
        term = (ONE, {})
        for i in indices:
            term = complex_mul(term, variables[i])
        real, imaginary = add(real, term[0]), add(imaginary, term[1])
    return real, imaginary


def algebra_checks(checks):
    xs = [variable(i) for i in range(8)]
    e, L, M = (symmetric(xs, k) for k in [1, 2, 3])
    lhs = add(scale(mul(L, L), 12), scale(mul(e, M), -21))
    rhs = {}
    for i, j in combinations(range(8), 2):
        difference = add(xs[i], scale(xs[j], -1))
        other = [xs[k] for k in range(8) if k not in [i, j]]
        bracket = add(total(mul(x, x) for x in other), symmetric(other, 2))
        rhs = add(rhs, mul(mul(difference, difference), bracket))
    checks.identity(lhs, rhs, 'Newton sum-of-squares identity')
    checks.require(len(lhs) == 266, 'Newton expanded support')
    expected = {(2, 2): 12, (2, 1, 1): 3, (1, 1, 1, 1): -12}
    for monomial, coefficient in lhs.items():
        pattern = tuple(sorted((v for v in monomial if v), reverse=True))
        checks.require(pattern in expected and coefficient == expected[pattern],
                       'Newton monomial coefficient')
    checks.reject_mutation(add(scale(mul(L, L), 12), scale(mul(e, M), -20)),
                          rhs, 'altered Newton coefficient')

    rs = [add(x, constant(F(1, 2))) for x in xs]
    r1, r2, r3 = (symmetric(rs, k) for k in [1, 2, 3])
    shift = add(add(add(r3, scale(r2, -4)), scale(r1, F(35, 4))),
                constant(-14))
    checks.identity(add(M, scale(L, -1)), shift, 'shifted saturation identity')
    checks.reject_mutation(add(shift, scale(r2, -1)), add(M, scale(L, -1)),
                          'altered shift coefficient')
    checks.identity(r2, add(add(L, scale(e, F(7, 2))), constant(7)),
                    'shifted second symmetric identity')
    variance64 = add(scale(total(mul(x, x) for x in xs), 8),
                     scale(mul(e, e), -1))
    checks.identity(variance64, add(scale(mul(e, e), 7), scale(L, -16)),
                    'variance identity')

    vertical = [(constant(F(1, 2)), x) for x in xs]
    u2, u3 = (complex_symmetric(vertical, k)[0] for k in [2, 3])
    checks.identity(u2, add(constant(7), scale(L, -1)), 'vertical e2 real part')
    checks.identity(u3, add(constant(7), scale(L, -3)), 'vertical e3 real part')
    checks.identity(u3, add(scale(u2, 3), constant(-14)),
                    'vertical saturation identity')

    alphas = xs
    ts = [variable(i+8) for i in range(8)]
    us = [(add(constant(F(1, 2)), a), t) for a, t in zip(alphas, ts)]
    A, B = total(alphas), total(ts)
    a2, t2 = (total(mul(x, x) for x in variables) for variables in [alphas, ts])
    re2 = complex_symmetric(us, 2)[0]
    energy_rhs = total([scale(re2, 2), constant(-14), scale(A, -7),
                        scale(mul(A, A), -1), scale(a2, 2), mul(B, B)])
    checks.identity(add(a2, t2), energy_rhs, 'other-root reciprocal energy')

    # Differentiate w prod(1+w u) in an independent sparse expansion.
    w = variable(15)
    g = product(add(ONE, mul(w, x)) for x in xs)
    derivative_product = derivative(mul(w, g), 15)
    coefficients = total(scale(mul(power(w, k), symmetric(xs, k)), k+1)
                         for k in range(9))
    checks.identity(derivative_product, coefficients,
                    'reciprocal derivative generating identity')

    tau = variable(14)
    ev = add(constant(4), scale(tau, 8))
    lv = variable(13)
    mean = add(ONE, tau)
    vformula = total([constant(F(7, 4)), scale(lv, F(-1, 4)),
                      scale(tau, 7), scale(power(tau, 2), 7)])
    meansquare = total([scale(power(ev, 2), F(1, 8)), scale(lv, F(-1, 4)),
                        scale(ev, F(1, 8)), constant(F(1, 4))])
    checks.identity(add(meansquare, scale(power(mean, 2), -1)), vformula,
                    'first-power variance formula')

    radius = variable(12)
    paired = total(scale(power(radius, 7-k),
                         2*F(9, k)*F(comb(8, 9-k), 8))
                   for k in range(1, 5))
    paired_formula = scale(total([scale(power(radius, 3), 126),
                                  scale(power(radius, 4), 84),
                                  scale(power(radius, 5), 36),
                                  scale(power(radius, 6), 9)]), F(1, 4))
    checks.identity(paired, paired_formula, 'paired high-index coefficient sum')

    x, y = variable(0), variable(1)
    quadratic = total([ONE, x, power(x, 2), scale(power(y, 2), F(-1, 2))])
    distance2 = total([ONE, scale(x, -2), power(x, 2), power(y, 2)])
    residual = add(mul(power(quadratic, 2), distance2), scale(ONE, -1))
    checks.require(all(sum(m) >= 3 for m in residual),
                   'inverse-distance Taylor coefficients through degree two')


def bound_checks(checks):
    tau0, coarse = F(1, 10**10), F(1, 100)
    cauchy_sum = sum((F(comb(8, k), (k+1)*7**k) for k in range(1, 9)), F(0))
    checks.require(cauchy_sum == F(41980912, 51883209) < 1,
                   'reciprocal Cauchy radius')
    checks.require(7*(1+coarse) < 8, 'reciprocal other-root radius eight')
    checks.require(F(9, 2)+8*coarse < 5, 'critical reciprocal radius five')
    checks.require(comb(7, 1)*8*4 == 224, 'second projection error')
    checks.require(comb(7, 2)*8**2*4 == 5376, 'third projection error')
    checks.require(4*(5376+3*224) == 24192, 'complex saturation error')
    checks.require(2*comb(7, 1)*5*8 == 560, 'second phase error')
    checks.require(3*comb(7, 2)*25*8 == 12600, 'third phase error')
    checks.require(24192+12600+4*560+70 == 39102 < 40000,
                   'shifted saturation error')
    checks.require((7+14*coarse)*40000 < 300000,
                   'Newton quantitative saturation')
    checks.require(F(300000, 6) == 50000, 'collapsed L bound')
    checks.require(F(300000, 4)+7+7*coarse < 76000,
                   'regular modulus variance')
    checks.require(76000+2+coarse < 77000, 'regular quadratic deficit')
    checks.require(77000*tau0 == F(77, 10**7) < F(2, 10**5),
                   'input to quadratic stability theorem')
    checks.require(9*77000 == 693000, 'regular critical energy constant')

    delta0 = F(2, 10**5)
    checks.require(2**8*4 == 1024, 'radial-projection coefficient error')
    checks.require(9*delta0 < F(1, 32)**2, 'critical radius one over thirty-two')
    checks.require(126+84*F(1, 32)+36*F(1, 32)**2+9*F(1, 32)**3 < 129,
                   'paired coefficient polynomial envelope')
    checks.require(F(9, 4)*129*27 == F(31347, 4),
                   'paired coefficient deficit constant')
    checks.require(delta0 < F(1, 200)**2, 'coarse quadratic square-root bound')
    checks.require(300*8*tau0+2500*delta0**2*F(1, 200) < F(1, 100),
                   'radial-interpolation matching radius')
    checks.require(sum((F(comb(9, k))*F(1, 100)**(k-1) for k in range(2, 10)), F(0)) < 1,
                   'Rouche binomial tail')
    checks.require(F(101, 100)**8+1 < F(21, 10), 'Rouche coefficient norm factor')
    checks.require(F(21, 10)*1024 < 8*300, 'Rouche radial-error comparison')
    checks.require(F(21, 10)*F(31347, 4) < 8*2500, 'Rouche high-index comparison')
    checks.require(F(1, 50) < F(4, 9), 'disjoint anchored matching disks')
    checks.require(77000 < 278**2, 'deficit-constant square-root enclosure')
    checks.require(2500*77000**2*278*F(1, 10**15) < 5,
                   'first-power high-index matching constant')
    checks.require(300*8+5 < 2500, 'regular first-power root matching constant')

    checks.require(4*5*8 == 160, 'other-root imaginary-sum bound')
    checks.require(32*tau0+160+F(2, 3)*50000+F(56, 3) < 34000,
                   'collapsed reciprocal-root energy')
    checks.require(16*34000 < 800**2, 'collapsed root matching constant')
    scalar = 100008**2+100000**2
    checks.require(scalar*tau0 < 3, 'collapsed scalar reciprocal energy')
    checks.require(2*5*8 == 80, 'critical phase energy')
    checks.require(2*80+2*3 == 166, 'critical reciprocal matching energy')
    checks.require(16*166 == 2656 < 52**2, 'critical matching constant')
    checks.require(F(5, 8) > 0 and F(3, 32) > 0,
                   'positive first-power sharpness coefficients')


def family_checks(checks):
    z, v = variable(0), variable(1)
    base = total([power(z, 2), scale(z, 2), scale(mul(v, z), -2), ONE])
    quadratic = total([scale(power(z, 2), 9), scale(z, 2),
                       scale(mul(v, z), -10), constant(-7), scale(v, 8)])
    hv = mul(add(z, constant(-1)), power(base, 4))
    checks.identity(derivative(hv, 0), mul(power(base, 3), quadratic),
                    'collapsed family derivative factorization')
    checks.reject_mutation(mul(power(base, 3), add(quadratic, scale(v, -16))),
                          derivative(hv, 0), 'altered collapsed derivative sign')
    checks.identity(specialize(quadratic, 0, F(-1)), scale(v, 18),
                    'negative quadratic endpoint')
    checks.identity(specialize(quadratic, 0, F(0)), add(constant(-7), scale(v, 8)),
                    'zero quadratic endpoint')
    checks.identity(specialize(quadratic, 0, F(1)), add(constant(4), scale(v, -2)),
                    'positive quadratic endpoint')
    checks.identity(specialize(derivative(quadratic, 0), 0, F(1)),
                    scale(specialize(quadratic, 0, F(1)), 5),
                    'real critical reciprocal sum five')
    discriminant = add(power(add(constant(2), scale(v, -10)), 2),
                       scale(add(constant(-7), scale(v, 8)), -36))
    checks.identity(discriminant,
                    total([constant(256), scale(v, -328), scale(power(v, 2), 100)]),
                    'collapsed quadratic discriminant')
    checks.require(256-328*F(1, 100) > 0, 'discriminant positivity on family interval')
    checks.require(-7+8*F(1, 100) < 0 and 4-2*F(1, 100) > 0,
                   'critical root interval signs')
    checks.identity(add(ONE, scale(power(add(ONE, scale(v, -1)), 2), -1)),
                    add(scale(v, 2), scale(power(v, 2), -1)),
                    'original-root imaginary square')
    checks.identity(add(power(v, 2), add(scale(v, 2), scale(power(v, 2), -1))),
                    scale(v, 2), 'collapsed displacement squared')
    checks.require(F(3, 8)*F(1, 2)*F(1, 2) == F(3, 32),
                   'collapsed first-power linear coefficient')

    pu = total([power(z, 9), scale(mul(v, power(z, 8)), F(-27, 4)),
                scale(mul(add(v, scale(power(v, 2), 9)), power(z, 7)), F(9, 7)),
                constant(-1), scale(v, F(27, 4)),
                scale(add(v, scale(power(v, 2), 9)), F(-9, 7))])
    checks.identity(specialize(pu, 0, F(1)), {}, 'regular full-disk marked root')
    critical_factor = add(power(add(z, scale(v, -3)), 2), v)
    checks.identity(derivative(pu, 0), scale(mul(power(z, 6), critical_factor), 9),
                    'regular full-disk derivative')
    checks.require(F(1, 4)*F(1, 2)*5 == F(5, 8),
                   'regular full-disk first-power coefficient')

    gt = total([power(z, 9), constant(-1), mul(v, add(power(z, 5), scale(power(z, 4), -1)))])
    derivative_factor = total([scale(power(z, 5), 9), scale(mul(v, z), 5), scale(v, -4)])
    checks.identity(derivative(gt, 0), mul(power(z, 3), derivative_factor),
                    'unit-circle regular derivative')
    checks.require(not any(m[0] in [7, 6] for m in derivative(gt, 0)),
                   'zero first and second critical power sums by Vieta')
    x = add(z, variable(0, -1))
    quartic = total([power(x, 4), power(x, 3), scale(power(x, 2), -3), scale(x, -2), ONE, v])
    quotient = add(total(power(z, k) for k in range(9)), mul(v, power(z, 4)))
    checks.identity(mul(power(z, 4), quartic), quotient, 'unit-circle quartic reduction')
    checks.identity(mul(add(z, constant(-1)), quotient), gt, 'unit-circle quotient')
    intervals = [(F(-19, 10), F(-18, 10)), (F(-11, 10), F(-9, 10)),
                 (F(3, 10), F(4, 10)), (F(15, 10), F(16, 10))]
    for left, right in intervals:
        checks.require(-2 < left < right < 2, 'quartic root interval containment')
        values = []
        for endpoint in [left, right]:
            values.append([endpoint**4+endpoint**3-3*endpoint**2-2*endpoint+1+t
                           for t in [F(0), F(1, 1000)]])
        checks.require(values[0][0]*values[0][1] > 0 and
                       values[1][0]*values[1][1] > 0 and
                       values[0][0]*values[1][0] < 0,
                       'uniform quartic sign change')
    checks.require(F(1, 8)*F(1, 4) == F(1, 32),
                   'unit-circle first-power energy coefficient')


def equality_controls(checks):
    for name, rs, expected_L, expected_v in [
            ('regular', [F(1)]*8, F(7), F(0)),
            ('collapsed', [F(1, 2)]*7+[F(9, 2)], F(0), F(7, 4))]:
        xs = [r-F(1, 2) for r in rs]
        e = sum(xs, F(0))
        L = sum((xs[i]*xs[j] for i, j in combinations(range(8), 2)), F(0))
        M = sum((xs[i]*xs[j]*xs[k] for i, j, k in combinations(range(8), 3)), F(0))
        checks.require(sum(rs, F(0)) == 8 and e == 4, name+' first-power equality')
        checks.require(L == M == expected_L, name+' Newton saturation')
        checks.require(sum(((r-1)**2 for r in rs), F(0))/8 == expected_v,
                       name+' variance')
        checks.require(12*L**2-21*e*M == 0, name+' SOS equality')
    checks.require(F(7, 4) > F(2, 10**5),
                   'first-power equality does not imply small quadratic deficit')


def main():
    checks = Checks()
    algebra_checks(checks)
    bound_checks(checks)
    family_checks(checks)
    equality_controls(checks)
    print(f'PASS: {checks.count} exact checks; {checks.mutations} certificate mutations rejected.')


if __name__ == '__main__':
    main()
