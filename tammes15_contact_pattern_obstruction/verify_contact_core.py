#!/usr/bin/env python3
"""Exact 13-vertex/24-edge contact-core certificate checker; stdlib only.

Rational functions use canonical pairs of integer polynomials. The Gram
determinants are computed directly from vector coefficients by Leibniz sums.
The geometric implication is proved in CONTACT_CORE.md.
"""
from fractions import Fraction
from functools import reduce
from itertools import permutations
from math import gcd
from pathlib import Path
import copy
import json
import sys
import verify as base
from verify import (Z, ONE, T, F, ROOT_LO, ROOT_HI, need, trim, add, sub,
                    mul, scale, power, exactdiv, primitive, pgcd,
                    bernstein, value)


def strip_factors(p, factors):
    need(bool(p), 'zero cannot certify invertibility')
    p = primitive(p)
    for f in factors:
        while len(p) >= len(f):
            q, r = base.divrem(p, f)
            if q is None or r:
                break
            p = primitive(q)
    return p


SAFE = base.SAFE


def nonzero(p, label='divisor'):
    need(bool(p), label+': zero')
    coefficients = bernstein(p)
    need(all(c > 0 for c in coefficients) or all(c < 0 for c in coefficients)
         or len(strip_factors(p, SAFE)) == 1, label+': uncertified roots')


class Rat:
    """A reduced rational function over Q(t); numerical divisions are audited."""
    __slots__ = ('n', 'd')

    def __init__(self, n=Z, d=ONE):
        n, d = trim(n), trim(d)
        need(bool(d), 'zero rational-function denominator')
        if not n:
            self.n, self.d = Z, ONE
            return
        content = reduce(gcd, n+d)
        if d[-1] < 0:
            content = -content
        n, d = tuple(c//content for c in n), tuple(c//content for c in d)
        common = pgcd(n, d)
        self.n, self.d = exactdiv(n, common), exactdiv(d, common)

    @staticmethod
    def convert(x):
        return x if isinstance(x, Rat) else Rat((x,))

    def __add__(self, other):
        other = self.convert(other)
        common = pgcd(self.d, other.d)
        p, q = exactdiv(self.d, common), exactdiv(other.d, common)
        return Rat(add(mul(self.n, q), mul(other.n, p)), mul(p, other.d))

    __radd__ = __add__

    def __neg__(self):
        return Rat(scale(self.n, -1), self.d)

    def __sub__(self, other):
        return self + (-self.convert(other))

    def __rsub__(self, other):
        return self.convert(other) - self

    def __mul__(self, other):
        other = self.convert(other)
        g1, g2 = pgcd(self.n, other.d), pgcd(other.n, self.d)
        return Rat(mul(exactdiv(self.n, g1), exactdiv(other.n, g2)),
                   mul(exactdiv(self.d, g2), exactdiv(other.d, g1)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.convert(other)
        nonzero(other.n)
        return self * Rat(other.d, other.n)

    def __rtruediv__(self, other):
        return self.convert(other) / self

    def __pow__(self, exponent):
        need(type(exponent) is int and exponent >= 0, 'nonnegative integer power required')
        return Rat(power(self.n, exponent), power(self.d, exponent))

    def __eq__(self, other):
        other = self.convert(other)
        return self.n == other.n and self.d == other.d


def determinant(matrix):
    total = Rat()
    for p in permutations(range(len(matrix))):
        inversions = sum(p[i] > p[j] for i in range(len(p)) for j in range(i+1, len(p)))
        product = Rat(((-1)**inversions,))
        for i, j in enumerate(p):
            product *= matrix[i][j]
        total += product
    return total


def positive(rational, label):
    nonzero(rational.n, label+' numerator')
    nonzero(rational.d, label+' denominator')
    need(value(rational.n, Fraction(11, 20))*value(rational.d, Fraction(11, 20)) > 0,
         label+': not positive on the interval')


def core_model():
    ap, bp, cross = base.model('asymmetric')
    return ([step for step in ap if step[0] != 14],
            [step for step in bp if step[0] != 3],
            [edge for edge in cross if edge not in ((7, 3), (14, 3))])


def verify(data):
    global SAFE
    need(set(data) == {'P5', 'P6', 'P14', 'P15'}, 'certificate factor names')
    factors = {}
    for name, degree in (('P5', 5), ('P6', 6), ('P14', 14), ('P15', 15)):
        need(type(data[name]) is list and len(data[name]) == degree+1 and
             all(type(x) is int for x in data[name]), 'integer factor coefficients')
        factors[name] = trim(data[name])
        need(len(factors[name]) == degree+1, 'factor degree')
        need(all(c > 0 for c in bernstein(factors[name])), 'factor positivity')
    SAFE = base.SAFE + tuple(factors.values())
    for p in base.SAFE:
        b = bernstein(p)
        need(all(c > 0 for c in b) or all(c < 0 for c in b), 'base factor sign')
    t, one, zero = Rat(T), Rat(ONE), Rat()
    h = [[one if i == j else t for j in range(3)] for i in range(3)]
    hi = [[(one/(one-t) if i == j else zero)-t/((one-t)*(one+2*t))
           for j in range(3)] for i in range(3)]
    dh = (one-t)**2*(one+2*t)
    a = {i: [one if j == k else zero for j in range(3)]
         for k, i in enumerate((0, 5, 11))}
    b = {i: [one if j == k else zero for j in range(3)]
         for k, i in enumerate((1, 2, 4))}
    ap, bp, cross = core_model()
    edges = set()
    for group, steps in ((a, ap), (b, bp)):
        roots = list(group)
        edges.update(tuple(sorted((i, j))) for i in roots for j in roots if i < j)
        for new, i, j, old in steps:
            need(all(tuple(sorted(e)) in edges for e in ((i, j), (i, old), (j, old))),
                 'reflection lacks its old triangle')
            group[new] = [2*t/(one+t)*(group[i][k]+group[j][k])-group[old][k]
                          for k in range(3)]
            edges.update((tuple(sorted((new, i))), tuple(sorted((new, j)))))
    edges.update(tuple(sorted(e)) for e in cross)
    vertices = set(range(15)) - {3, 14}
    need(set(a) | set(b) == vertices and len(edges) == 24, 'core graph size')
    def dot(x, y):
        return sum((x[i]*h[i][j]*y[j] for i in range(3) for j in range(3)), zero)
    def cross3(x, y):
        return [x[1]*y[2]-x[2]*y[1], x[2]*y[0]-x[0]*y[2], x[0]*y[1]-x[1]*y[0]]
    def metric_inverse(x):
        return [sum((hi[i][j]*x[j] for j in range(3)), zero) for i in range(3)]
    for group in (a, b):
        need(all(dot(v, v) == one for v in group.values()), 'block unit norms')
        need(all(dot(group[i], group[j]) == t for i, j in edges if i in group and j in group),
             'within-block contact identity')
    kappa = t*(9*t*t-2*t-3)/(one+t)**2
    need(all(dot(a[i], a[j]) == kappa for i, j in ((6, 7), (6, 9), (7, 9))),
         'reflected anchor-triangle identity')
    positive(one-kappa, 'reflected triangle eigenvalue')
    positive(one+2*kappa, 'reflected triangle other eigenvalue')
    reflection_matrix = [[a[j][i] for j in (6, 7, 9)] for i in range(3)]
    reflection_pivot = determinant(reflection_matrix)
    need(reflection_pivot == (3*t-one)*(3*t+one)**2/(one+t)**3,
         'original anchor recovery identity')
    positive(reflection_pivot, 'original anchor recovery pivot')
    w = dot(b[10], b[13])
    positive(one-w, 'common-neighbor pair separation')
    positive(one+w, 'common-neighbor pair nonantipodality')
    need(dot(b[2], b[10]) == t and dot(b[2], b[13]) == t, 'existing common neighbor')
    parent = [[dot(x, y) for y in (b[2], b[10], b[13])] for x in (b[2], b[10], b[13])]
    positive(determinant(parent), 'common-neighbor triple independence')
    v = [2*t/(one+w)*(x+y)-z for x, y, z in zip(b[10], b[13], b[2])]
    need(dot(v, v) == one and dot(v, b[10]) == t and dot(v, b[13]) == t,
         'forced distinct common-neighbor reflection identity')
    gamma = kappa/(one+kappa)
    mu0 = (t-one)*(t+one)*(2*t+one)*(3*t-one)/(9*t**3-t*t-t+one)
    need(mu0**2 == dh*(one+2*kappa)/(one+kappa)**2, 'orientation square identity')
    nonzero(mu0.n, 'orientation magnitude')
    common = scale(mul(mul(power(T, 2), power((-1, 1), 3)),
                       mul(power((1, 2), 2), (-1, 0, 5))), 4)
    denominator = mul(mul(power((1, 1), 10), (1, -1, -1, 9)),
                      power((1, 3, -1, -3, 8), 4))
    nonzero(denominator, 'displayed determinant denominator')
    pivot = None
    for sign in (-1, 1):
        normal = metric_inverse(cross3(b[12], v))
        c = [gamma*x+sign*mu0*y for x, y in zip(b[12], normal)]
        vectors = (v, b[8], c)
        gram = [[dot(x, y) for y in vectors] for x in vectors]
        rhs = (kappa, t, t-gamma*dot(v, b[12]))
        augmented = [row+[rhs[i]] for i, row in enumerate(gram)] + [list(rhs)+[one]]
        actual = determinant(augmented)
        extra = (mul(mul((-3, -11, -5, 11), factors['P6']), factors['P15'])
                 if sign == -1 else mul(mul(F, factors['P5']), factors['P14']))
        expected = Rat(mul(common, extra), denominator)
        need(actual == expected, 'orientation '+str(sign)+' Gram determinant factorization identity')
        if sign == -1:
            nonzero(actual.n, 'excluded orientation numerator')
        else:
            need(strip_factors(actual.n, SAFE) == F, 'remaining orientation obstruction differs from F')
            pivot = determinant(gram)
            need(pgcd(pivot.n, F) == ONE, 'Gram3 rank pivot vanishes at an F root')
            nonzero(pivot.d, 'Gram3 pivot denominator')
    need(all(c > 0 for c in bernstein(tuple(i*F[i] for i in range(1, len(F))))), 'F derivative sign')
    need(value(F, Fraction(1, 2)) < 0 < value(F, Fraction(3, 5)), 'F endpoint signs')
    need(value(F, ROOT_LO) < 0 < value(F, ROOT_HI), 'incumbent root bracket')
    # Existing exact existence certificate identifies the unique allowed core.
    old_data = json.loads(Path(__file__).with_name('certificate.json').read_text())
    base.check_variant('asymmetric', old_data['asymmetric'])
    return {'status': 'VERIFIED', 'vertices': sorted(vertices), 'vertex_count': 13,
            'prescribed_edges': 24, 'interval': '(1/2,3/5)',
            'excluded_orientation': -1, 'allowed_orientation': 1,
            'common_obstruction': list(F), 'unique_labeled_core_Gram_at_root': True,
            'all_geometric_divisors_certified_nonzero': True,
            'incumbent_existence_checked': True, 'global_Tammes15_bound_improved': False}


def selftest(data):
    for name in ('P14', 'P15'):
        bad = copy.deepcopy(data)
        bad[name][0] += 1
        try:
            verify(bad)
        except ValueError as error:
            need('factorization identity' in str(error), 'corruption rejected for wrong reason')
        else:
            raise ValueError('corrupted branch factor accepted')
    need(Rat((2, 2), (4, 4)) == Rat((1,), (2,)), 'rational cancellation control')
    need((Rat((1, 1))/Rat((1, 1))) == 1, 'audited division control')
    need(pgcd(mul(F, (2, 1)), mul(F, (3, 1))) == F, 'gcd control')


if __name__ == '__main__':
    certificate = json.loads(Path(__file__).with_name('certificate_contact_core.json').read_text())
    result = verify(certificate)
    if '--selftest' in sys.argv:
        selftest(certificate)
        result['controls'] = 'both corrupted branch factorizations rejected; exact arithmetic controls passed'
    print(json.dumps(result, sort_keys=True, indent=2))
