#!/usr/bin/env python3
"""Exact author algebra for PROOF.md; Python 3.11 standard library.

Rational functions have domain Q(m,x,s,u), with denominators products
of m,m-1,m-2,m-3. Only cleared polynomial identities and rational
inequalities are checked. Rolle, spectral weights, projection inequalities
and geometric interpretation remain written mathematics. No floating
point, solver, fitting, eigenvalue search or external corpus is used.
Agent six-sendov-2, role researcher. Arithmetic is adapted from the
author's angular quartic checker, source57dd686, not independent review.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json


def require(ok, label):
    if not ok:
        raise AssertionError(label)


class Poly:
    def __init__(self, terms=0):
        if isinstance(terms, Poly):
            terms = terms.t
        if isinstance(terms, (int, F)):
            terms = {(0, 0, 0, 0): F(terms)}
        self.t = {k: F(v) for k, v in terms.items() if v}

    def __add__(self, other):
        if not isinstance(other, (Poly, int, F)):
            return NotImplemented
        other = poly(other)
        out = dict(self.t)
        for k, v in other.t.items():
            out[k] = out.get(k, F(0)) + v
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.t.items()})

    def __sub__(self, other):
        if not isinstance(other, (Poly, int, F)):
            return NotImplemented
        return self + -poly(other)

    def __rsub__(self, other):
        if not isinstance(other, (Poly, int, F)):
            return NotImplemented
        return poly(other) + -self

    def __mul__(self, other):
        if not isinstance(other, (Poly, int, F)):
            return NotImplemented
        other = poly(other)
        out = {}
        for a, v in self.t.items():
            for b, w in other.t.items():
                k = tuple(a[i] + b[i] for i in range(4))
                out[k] = out.get(k, F(0)) + v*w
        return Poly(out)

    __rmul__ = __mul__

    def __pow__(self, k):
        require(isinstance(k, int) and k >= 0, 'nonnegative polynomial power')
        out = Poly(1)
        for _ in range(k):
            out *= self
        return out

    def __eq__(self, other):
        if not isinstance(other, (Poly, int, F)):
            return NotImplemented
        return self.t == poly(other).t

    def at(self, index, value):
        out = Poly(0)
        for k, v in self.t.items():
            powers = list(k)
            powers[index] = 0
            out += Poly({tuple(powers): v})*poly(value)**k[index]
        return out

    def divide_m_minus(self, root):
        """Exact division by m-root, grouped by all other variable powers."""
        out, rem = {}, {}
        groups = sorted({k[1:] for k in self.t})
        for group in groups:
            coeff = {k[0]: v for k, v in self.t.items() if k[1:] == group}
            top = max(coeff)
            carry = coeff[top]
            if top:
                out[(top-1,) + group] = carry
            for degree in range(top-1, 0, -1):
                carry = coeff.get(degree, F(0)) + root*carry
                out[(degree-1,) + group] = carry
            remainder = coeff.get(0, F(0)) + (root*carry if top else F(0))
            if remainder:
                rem[(0,) + group] = remainder
        return Poly(out), Poly(rem)


def poly(value):
    return value if isinstance(value, Poly) else Poly(value)


m = Poly({(1, 0, 0, 0): 1})
x = Poly({(0, 1, 0, 0): 1})
s = Poly({(0, 0, 1, 0): 1})
u = Poly({(0, 0, 0, 1): 1})
FACTORS = (m, m-1, m-2, m-3)


class RF:
    def __init__(self, numerator=0, denominator=(0, 0, 0, 0)):
        self.p, d = poly(numerator), list(denominator)
        if self.p == 0:
            d = [0, 0, 0, 0]
        for root in range(4):
            while d[root] and self.p != 0:
                quotient, remainder = self.p.divide_m_minus(root)
                if remainder != 0:
                    break
                self.p = quotient
                d[root] -= 1
        self.d = tuple(d)

    def __add__(self, other):
        other = rf(other)
        d = tuple(max(a, b) for a, b in zip(self.d, other.d))
        p, q = self.p, other.p
        for i, factor in enumerate(FACTORS):
            p *= factor**(d[i]-self.d[i])
            q *= factor**(d[i]-other.d[i])
        return RF(p+q, d)

    __radd__ = __add__

    def __neg__(self):
        return RF(-self.p, self.d)

    def __sub__(self, other):
        return self + -rf(other)

    def __rsub__(self, other):
        return rf(other) + -self

    def __mul__(self, other):
        other = rf(other)
        return RF(self.p*other.p, tuple(a+b for a, b in zip(self.d, other.d)))

    __rmul__ = __mul__

    def __pow__(self, k):
        return RF(self.p**k, tuple(k*a for a in self.d))

    def __eq__(self, other):
        return (self-rf(other)).p == 0

    def at(self, index, value):
        if index:
            return RF(self.p.at(index, value), self.d)
        require(isinstance(value, (int, F)), 'dimension specialization rational')
        denominator = F(1)
        for root, exponent in enumerate(self.d):
            denominator *= (value-root)**exponent
        require(denominator != 0, 'dimension specialization outside poles')
        return RF(self.p.at(0, value)*F(1, denominator))


def rf(value):
    return value if isinstance(value, RF) else RF(value)


im = RF(1, (1, 0, 0, 0))
i1 = RF(1, (0, 1, 0, 0))
i2 = RF(1, (0, 0, 1, 0))
i3 = RF(1, (0, 0, 0, 1))


def power_sum(k):
    return {0: RF(m), 1: RF(0), 2: RF(1), 3: RF(s), 4: RF(x)}[k]


def trace_power(k):
    """Enumerate tr(Theta P)^k, expanding every P=I-ee*.

    Selected Q positions split the cyclic trace into power-sum factors.
    This contraction enumeration does not use the claimed trace formula.
    """
    out = RF(0)
    for flags in product((0, 1), repeat=k):
        positions = [j for j, flag in enumerate(flags) if flag]
        if not positions:
            out += power_sum(k)
            continue
        term = RF((-1)**len(positions))*im**len(positions)
        for j, position in enumerate(positions):
            gap = (positions[(j+1) % len(positions)]-position) % k
            term *= power_sum(gap or k)
        out += term
    return out


def coupling_power(k):
    """Expand e*Theta(PThetaP)^kTheta e as a linear projection word."""
    length = k+2
    out = RF(0)
    for flags in product((0, 1), repeat=length-1):
        cuts = [j+1 for j, flag in enumerate(flags) if flag]
        boundaries = [0] + cuts + [length]
        term = RF((-1)**len(cuts))*im**(len(cuts)+1)
        for left, right in zip(boundaries, boundaries[1:]):
            term *= power_sum(right-left)
        out += term
    return out


def run(mutation=None):
    checks = []

    def equal(label, lhs, rhs):
        require(lhs == rhs, label)
        checks.append(label)

    def positive(label, value):
        require(value > 0, label)
        checks.append(label)

    equal('polynomial linear factor division',
          Poly((m-2)*(x+s)).divide_m_minus(2)[0], x+s)
    equal('rational cancellation', RF((m-2)*(x+s), (0, 0, 1, 0)), x+s)
    equal('trace A', trace_power(1), 0)
    equal('trace A squared', trace_power(2), RF(m-2)*im)
    equal('trace A cubed', trace_power(3), RF((m-3)*s)*im)
    t4 = RF(m-4)*im*x+2*im**2
    if mutation == 'wrong_trace_fourth':
        t4 += im**2
    equal('trace A fourth', trace_power(4), t4)
    equal('coupling zeroth moment', m*coupling_power(0), 1)
    equal('coupling first moment', m*coupling_power(1), s)
    equal('coupling second moment', m*coupling_power(2), x-im)

    c2, c3, c4 = F(-1, 2), -RF(s)*F(1, 3), RF(F(1, 8))-RF(x)*F(1, 4)
    quartic = [RF(24)*c4, 24*(m-3)*c3,
               RF(12*(m-2)*(m-3))*c2, RF(0), RF(m*(m-1)*(m-2)*(m-3))]
    reverse = list(reversed(quartic))
    derivative = [(j+1)*reverse[j+1] for j in range(4)]
    equal('reversed quartic derivative has factor y', derivative[0], 0)
    quadratic = [term*F(1, 24) for term in derivative[1:]]
    equal('reversed derivative quadratic constant', quadratic[0], (m-2)*(m-3)*c2)
    equal('reversed derivative quadratic linear', quadratic[1], 3*(m-3)*c3)
    equal('reversed derivative quadratic leading', quadratic[2], 4*c4)
    discr = quadratic[1]**2-4*quadratic[0]*quadratic[2]
    z0 = 2*(m-2)*i3*(x-F(1, 2))
    h = RF(s**2)-z0
    if mutation == 'weak_newton_constant':
        h = RF(s**2)-F(3, 2)*(m-2)*i3*(x-F(1, 2))
    equal('classical discriminant is moment slack', discr, RF((m-3)**2)*h)
    equal('Pearson square contraction',
          power_sum(4)-2*RF(s)*power_sum(3)+(RF(s**2)-2*im)*power_sum(2)
          +2*RF(s)*im*power_sum(1)+im**2*power_sum(0), RF(x-s**2)-im)

    xs = RF(m*m-3*m+3)*im*i1
    delta = xs-x
    t2, t3 = RF(m-2)*im, RF((m-3)*s)*im
    gram_d = t4-t2**2*i1-t3**2*RF(m)*i2
    gram_n = RF(x)-im-t2*i1-t3*RF(m)*i2*s
    base = i1+RF(m)*i2*s**2
    c = RF(m-2)*im
    beta = RF(m-3)*i2
    equal('Gram D cleared representation', gram_d, c*delta-c*beta**2*h)
    equal('Gram N cleared representation', gram_n, delta-beta*h)
    ell = RF(m*(m-1)*x-(2*m-3))*i2*i3
    if mutation == 'wrong_pinching_line':
        ell += im
    equal('positive cleared pinching identity',
          (base-ell)*gram_d+gram_n**2, delta*h*i2**2)
    equal('singular D implies nonzero N off endpoint',
          delta-delta*RF(m-2)*i3, -delta*i3)
    equal('line at fourth moment endpoint',
          RF(m*(m-1))*i2*i3*xs-RF(2*m-3)*i2*i3, 1)
    equal('line at moving pair', ell.at(1, F(1, 2)), F(1, 2))
    equal('Pearson moment upper coefficient',
          (RF(m-1)*i3)*delta, RF(x)-im-z0)

    pp = m**4-9*m**3+13*m**2-13*m-6
    shifted = pp.at(0, 8+u)
    positive_poly = u**4+23*u**3+181*u**2+515*u+210
    equal('all-degree positive shift polynomial', shifted, positive_poly)
    require(all(v > 0 for v in shifted.t.values()), 'positive shift coefficients')
    checks.append('positive shift coefficients')
    bm = RF(m*pp)*i2*i3
    affine_slope = RF(m*(m*m-4*m-4))-9*(m+2)*RF(m*(m-1))*i2*i3
    equal('affine angular slope', affine_slope, bm)
    tm = RF(m*m*(m*m-4*m-4))*i1-RF((m-6)*(3*m+2))
    equal('maximum matches two-block source',
          RF(m*(m*m-4*m-4))*xs+(13*m+18)-9*(m+2), tm)
    angular_bound = RF(m*(m*m-4*m-4))*x+(13*m+18)-9*(m+2)*ell
    equal('global moment deficit identity', angular_bound, tm-bm*delta)
    equal('degree-nine moment endpoint', xs.at(0, 8), F(43, 56))
    equal('degree-nine maximum bracket', tm.at(0, 8), 204)
    equal('degree-nine deficit slope', bm.at(0, 8), 56)
    pref = F((8+2)*(3*8+2)**3, 256*8**7)
    equal('degree-nine prefactor', pref, F(10985, 33554432))
    equal('degree-nine maximum coefficient', 204*pref, F(560235, 8388608))
    equal('degree-nine minimum coefficient', 60*pref, F(164775, 8388608))
    equal('degree-nine lower bracket', 224*F(1, 8)+122-90, 60)
    equal('near maximum coefficient threshold', F(14, 25)/56, F(1, 100))
    equal('degree-nine Pearson residual coefficient',
          (RF(m-1)*i3).at(0, 8), F(7, 5))
    equal('degree-nine quadratic residual from coefficient', F(7, 5)/56, F(1, 40))

    # Rational squares certify every radical comparison used in clustering.
    zlower = F(9, 14)-F(12, 5)*F(1, 100)
    equal('near maximum third moment lower square', zlower, F(1083, 1750))
    positive('third moment square above three fifths', zlower-F(3, 5))
    positive('third moment above 31/40', zlower-F(31, 40)**2)
    positive('gap below 15/14', F(15, 14)**2-F(8, 7))
    equal('root-distance squared coefficient', 4*F(7, 5)/F(11, 10), F(56, 11))
    positive('count error below two thirds', F(4, 9)-F(448, 11)*F(1, 100))
    positive('zero positive levels excluded', F(14, 15)-F(2, 3))
    positive('two positive levels excluded', F(31, 10)-F(15, 7)-F(2, 3))
    positive('normalized contrast at least seven eighths', F(7, 8)*F(11, 10)-F(7, 8)**2)
    geometry_constant = F(56, 11)/F(7, 8)
    if mutation == 'wrong_geometry_radius':
        geometry_constant = F(6)
    positive('distance coefficient below six', F(6)-geometry_constant)
    equal('geometry from angular deficit', F(6, 56), F(3, 28))

    # Exact controls use invariants, never evaluate irrational eigenvalues.
    if mutation == 'moment_only_eta':
        pair_eta = F(1)
    else:
        pair_eta = F(1, 2)
    equal('moving-pair active weights', 2*F(1, 2)**2, pair_eta)
    equal('singleton active weight', F(1)**2, F(1))
    equal('singleton degree-nine moments', F(7**4+7, (7**2+7)**2), F(43, 56))
    equal('four/four degree-nine moments', F(8, 8**2), F(1, 8))
    pair_coefficient = pref*(224*F(1, 2)+122-90*pair_eta)
    equal('moving-pair published coefficient', pair_coefficient, F(2076165, 33554432))
    if mutation == 'wrong_maximum':
        equal('maximum profile consistency', pref*(224*F(43, 56)+122-90), pref*203)
    else:
        equal('maximum profile consistency', pref*(224*F(43, 56)+122-90), pref*204)

    return {'agent': 'six-sendov-2', 'role': 'researcher',
            'status': 'exact author algebra; ordinary proof bridges unformalized and independently unreviewed',
            'domain': 'balanced real slopes, m>=4; angular maximum m>=8',
            'checks': len(checks), 'check_labels': checks,
            'degree_nine': {'minimum': str(60*pref), 'maximum': str(204*pref),
                            'moment_deficit_factor': str(56*pref),
                            'near_maximum_threshold_divided_by_prefactor': '14/25',
                            'shape_distance_factor_multiplied_by_prefactor': '3/28'},
            'positive_shift_coefficients': [210, 515, 181, 23, 1]}


def main():
    result = run()
    rejected = []
    for mutation in ('wrong_trace_fourth', 'weak_newton_constant',
                     'wrong_pinching_line', 'wrong_geometry_radius',
                     'moment_only_eta', 'wrong_maximum'):
        try:
            run(mutation)
        except AssertionError as error:
            rejected.append({'mutation': mutation, 'detected': str(error)})
        else:
            raise AssertionError('undetected mutation: '+mutation)
    result['rejected_mutations'] = rejected
    expected = Path(__file__).with_name('expected.json')
    if expected.exists():
        require(json.loads(expected.read_text()) == result, 'fixed compact manifest differs')
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
