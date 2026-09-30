#!/usr/bin/env python3
"""Exact finite algebra for PROOF.md; no spectral sampling or formalization.

Coefficient domain: Q in characteristic zero. A monomial is a sorted tuple
of variable indices (repetition records powers); the monomial order is only
for deterministic serialization and has no mathematical role. All matrix
operations and bounds use fractions.Fraction. Standard library only.
"""

from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json


class Poly:
    def __init__(self, terms=None):
        if isinstance(terms, (int, F)):
            terms = {(): F(terms)}
        self.t = {m: F(c) for m, c in (terms or {}).items() if c}

    @staticmethod
    def var(i):
        return Poly({(i,): F(1)})

    def __add__(self, other):
        other = aspoly(other)
        result = dict(self.t)
        for m, c in other.t.items():
            result[m] = result.get(m, F(0)) + c
        return Poly(result)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.t.items()})

    def __sub__(self, other):
        return self + (-aspoly(other))

    def __rsub__(self, other):
        return aspoly(other) - self

    def __mul__(self, other):
        other = aspoly(other)
        result = {}
        for m, c in self.t.items():
            for n, d in other.t.items():
                k = tuple(sorted(m + n))
                result[k] = result.get(k, F(0)) + c * d
        return Poly(result)

    __rmul__ = __mul__

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError('Only nonnegative integer polynomial powers')
        result = Poly(1)
        for _ in range(power):
            result = result * self
        return result

    def diff(self, variable):
        result = {}
        for m, c in self.t.items():
            multiplicity = m.count(variable)
            if multiplicity:
                n = list(m)
                n.remove(variable)
                n = tuple(n)
                result[n] = result.get(n, F(0)) + multiplicity * c
        return Poly(result)

    def __eq__(self, other):
        return self.t == aspoly(other).t


def aspoly(value):
    return value if isinstance(value, Poly) else Poly(value)


def mm(a, b):
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), 0)
             for j in range(len(b[0]))] for i in range(len(a))]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), 0)


def diag(values):
    return [[values[i] if i == j else 0 for j in range(len(values))]
            for i in range(len(values))]


def determinant(matrix):
    """Exact Gaussian elimination, independent of the rank-one formula."""
    a = [[F(c) for c in row] for row in matrix]
    result = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result
        scale = a[j][j]
        result *= scale
        for i in range(j + 1, len(a)):
            ratio = a[i][j] / scale
            for k in range(j + 1, len(a)):
                a[i][k] -= ratio * a[j][k]
            a[i][j] = F(0)
    return result


groups = {}


def check(group, condition, label):
    if not condition:
        raise AssertionError(f'{group}: {label}')
    groups[group] = groups.get(group, 0) + 1


def elementary(values, k):
    return sum((multiply(values[i] for i in subset)
                for subset in combinations(range(len(values)), k)), Poly(0))


def multiply(values):
    result = Poly(1)
    for value in values:
        result *= value
    return result


def run():
    n = 8
    identity = [[F(i == j) for j in range(n)] for i in range(n)]
    zero = [[F(0) for _ in range(n)] for _ in range(n)]
    h = [[identity[i][j] + 1 for j in range(n)] for i in range(n)]
    s = [[identity[i][j] + F(1, 4) for j in range(n)] for i in range(n)]
    p = [[identity[i][j] - F(1, 8) for j in range(n)] for i in range(n)]
    q = [[F(1, 8) for _ in range(n)] for _ in range(n)]
    check('matrices', mm(s, s) == h, 'S^2=H')
    check('matrices', mm(p, p) == p, 'P^2=P')
    check('matrices', mm(q, q) == q, 'Q^2=Q')
    check('matrices', mm(p, q) == zero, 'PQ=0')
    check('matrices', mm(q, p) == zero, 'QP=0')
    check('matrices', mm(s, p) == p, 'SP=P')
    check('matrices', mm(p, s) == p, 'PS=P')
    check('matrices', trace(p) == 7 and trace(q) == 1, 'ranks')
    check('matrices', determinant(s) == 3, 'invertible S')

    u = [Poly.var(i) for i in range(n)]
    t = Poly.var(8)
    characteristic = Poly(0)
    for k in range(n + 1):
        # Principal minors of diag(u) H factor as prod(u_i) det(H_I).
        for subset in combinations(range(n), k):
            minor = [[h[i][j] for j in subset] for i in subset]
            value = determinant(minor)
            check('principal_minors', value == k + 1, str(subset))
            characteristic += ((-1) ** k * value
                               * multiply(u[i] for i in subset) * t ** (n-k))
    rank_one = multiply(t - x for x in u)
    for i in range(n):
        rank_one -= u[i] * multiply(t - u[j] for j in range(n) if j != i)
    reciprocal = sum(((-1) ** k * (k+1) * elementary(u, k) * t ** (n-k)
                      for k in range(n + 1)), Poly(0))
    check('characteristic', characteristic == rank_one, 'determinant identity')
    check('characteristic', characteristic == reciprocal, 'derivative reciprocals')
    direct = (t * multiply(1 + x*t for x in u)).diff(8)
    reversed_derivative = Poly(0)
    for monomial, coefficient in direct.t.items():
        k = monomial.count(8)
        base = tuple(i for i in monomial if i != 8)
        reversed_derivative += Poly({base: coefficient * (-1) ** k}) * t ** (8-k)
    check('characteristic', characteristic == reversed_derivative,
          'directly differentiated product')

    v = mm(mm(s, diag(u)), s)
    compressed = mm(mm(p, diag(u)), p)
    moment = trace(mm(compressed, compressed))
    expected = F(3, 4) * sum((x*x for x in u), Poly(0)) + sum(u, Poly(0))**2 * F(1, 64)
    check('compressed_trace', moment == expected, 'formal eight-variable identity')
    check('compressed_trace', mm(mm(p, v), p) == compressed, 'PVP=PDP')

    # Residue of w^2 / [w^number_P (w-gap)^number_Q] at w=0.
    # Coefficients are obtained directly from the binomial power series.
    def residue(number_p, number_q, gap=F(4)):
        if number_p < 3:
            return F(0)
        degree = number_p - 3
        if not number_q:
            return F(degree == 0)
        return ((-gap) ** (-number_q)
                * comb(number_q + degree - 1, degree) / gap ** degree)

    for order in range(3):
        coefficient = Poly(0)
        for word in product((0, 1), repeat=order+1):
            projection = [p if bit == 0 else q for bit in word]
            term = projection[0]
            for projection_next in projection[1:]:
                term = mm(mm(term, v), projection_next)
            res = residue(word.count(0), word.count(1))
            check('contour_words', res == F(order == 2 and word == (0, 0, 0)),
                  str(word))
            coefficient += res * trace(term)
            if word[0] != word[-1]:
                check('contour_cyclicity', trace(term) == 0, str(word))
        check('contour_coefficients', coefficient == (moment if order == 2 else 0),
              str(order))

    # Real and imaginary parts are independent variables, not sample values.
    x = [Poly.var(i) for i in range(8)]
    y = [Poly.var(i+8) for i in range(8)]
    mx = mm(mm(p, diag(x)), p)
    my = mm(mm(p, diag(y)), p)
    negative_real = trace(mm(my, my)) - trace(mm(mx, mx))
    energy = sum((x[i]**2+y[i]**2 for i in range(8)), Poly(0))
    formula = (F(3, 4)*energy - F(3, 2)*sum((r*r for r in x), Poly(0))
               - F(1, 64)*sum(x, Poly(0))**2 + F(1, 64)*sum(y, Poly(0))**2)
    check('complex_trace', negative_real == formula, 'negative real trace')

    a, c, z, r = [Poly.var(i) for i in range(4)]
    b = 1-a*a
    d = 1+a
    kappa = d*(a-F(5, 8))
    check('disk_geometry', b+2*a*d-d*d == 0, 'constant disk term')
    check('disk_geometry', 2*b+2*a*d == 2*d, 'linear centered term')
    check('disk_geometry', F(3, 8)*d-b == kappa, 'radius threshold')
    # Clear denominators in b|v+delta|^2+2a Re(v+delta)-1.
    xr, yi = Poly.var(4), Poly.var(5)
    disk_cleared = b*((1+d*xr)**2+(d*yi)**2)+2*a*d*(1+d*xr)-d*d
    check('disk_geometry', disk_cleared == d*d*(2*xr+b*(xr*xr+yi*yi)),
          'full centered disk identity')

    g = z*z+2*c*z+1
    obstruction = (z-a)*g**4
    critical_quad = 9*z*z+(10*c-8*a)*z+1-8*a*c
    check('obstruction', obstruction.diff(2) == g**3*critical_quad,
          'degree-nine derivative factorization')
    dist2 = a*a+2*a*c+1
    substituted = (9*(a*r-1)**2+(10*c-8*a)*(a*r-1)*r+(1-8*a*c)*r*r)
    check('obstruction', substituted == dist2*r*r-10*(a+c)*r+9,
          'reciprocal quadratic')
    check('obstruction', dist2-2*a*(a+c) == b, 'derivative of quotient')
    check('obstruction', 10*b-6*a*d == d*(10-16*a), 'derivative sign')
    check('obstruction', ((a+c)*d-dist2)**2+d*d*(1-c*c) == 2*(1-c)*dist2,
          'exact family reciprocal energy')
    check('obstruction', F(-1, 16)*(10-16*a)*d == kappa,
          'limiting gap-to-energy coefficient')
    check('obstruction', 18*a*a*d-40*a*b == a*(58*a-40)*d,
          'second c derivative at one')
    check('obstruction', F(-1, 2)*(10-16*a) == 8*(a-F(5, 8)),
          'quadratic t coefficient')
    a0 = F(5, 8)
    quartic = a0*(58*a0-40)/(8*(1+a0)**5)
    check('obstruction', quartic == -F(9600, 13**5), 'threshold quartic')
    check('obstruction', 16/(1+a0) == F(128, 13), 'threshold baseline')
    check('obstruction', 25*F(99, 100)**2 > 9, 'positive discriminant')

    bounds = [
        (F(3, 4)/13000 < F(1, 10000), 'epsilon ceiling'),
        (8*9**3/(1-9*F(1, 10000)) < 6000, 'Neumann tail'),
        (F(39, 64)+F(3, 16) < 1, 'real-defect split'),
        (F(97, 64) < 2, 'real trace correction'),
        (F(27, 8)/(F(1, 2)**2) == F(27, 2), 'denominator loss'),
        (F(27, 2)+6000+16 < 6030, 'combined loss'),
        (F(6030, 13000) < F(1, 2), 'half kappa retained'),
        (F(13, 8)*(F(13, 8)-F(3, 20000)) > F(13, 5), 'root radius conversion'),
        (F(3, 4)/5000 == F(3, 20000), 'root radius ceiling'),
        (F(3, 4)-6000*F(3, 52000)-16*F(3, 52000)**2 > 0, 'moment positivity'),
        ((1+F(999, 1000))*(F(999, 1000)-F(5, 8)) > F(1, 2), 'routing kappa'),
        (23*10**6*F(1, 10**18) < F(1, 26000**2), 'routing radius'),
        (22*10**6+4*F(1, 10**18) < 23*10**6, 'routing energy'),
        (F(7, 4)+F(81, 4) == 22, 'boundary model second moment'),
    ]
    for valid, label in bounds:
        check('rational_bounds', valid, label)

    # Mutation controls demonstrate rejection by the actual checked identities.
    bad_s = [[identity[i][j]+F(1, 3) for j in range(n)] for i in range(n)]
    bad_trace = F(1, 2)*sum((u_i*u_i for u_i in u), Poly(0)) + F(1, 64)*sum(u, Poly(0))**2
    mutations = {
        'square_root_1_over_3': mm(bad_s, bad_s) != h,
        'compressed_trace_1_over_2': moment != bad_trace,
        'threshold_2_over_3': F(3, 8)*d-b != d*(a-F(2, 3)),
        'radius_denominator_10000': not (F(6030, 10000) <= F(1, 2)),
    }
    for label, rejected in mutations.items():
        if not rejected:
            raise AssertionError(f'Mutation escaped: {label}')
    print(json.dumps({'status': 'PASS', 'exact_checks': sum(groups.values()),
                      'groups': groups, 'mutations_rejected': list(mutations),
                      'external_inputs': 0, 'floating_point_operations': 0},
                     indent=2, sort_keys=True))


if __name__ == '__main__':
    run()
