#!/usr/bin/env python3
"""Independent scalar-residue audit of the complete weighted quartic.

Exact multivariate Laurent/Gaussian arithmetic, standard library only.
No author module or quoted moment formula is imported. The sparse kernel
adapts this reviewer's earlier public checker. Joint moments stay symbolic.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import sys

NAMES = ('v', 'z', 'A', 'I', 'X2', 'Y2', 'XY', 'XY2', 'Y3', 'Y4')
NV = len(NAMES)
ZERO = (0,)*NV
LABELS = []
RECORDS = []


def demand(ok, label):
    if not ok:
        raise ValueError(label)


class P:
    def __init__(self, value=0):
        self.terms = ({e: F(c) for e, c in value.items() if c}
                      if isinstance(value, dict) else ({ZERO: F(value)} if value else {}))

    @staticmethod
    def cast(x):
        return x if isinstance(x, P) else P(x)

    def __add__(self, x):
        result = dict(self.terms)
        for e, c in P.cast(x).terms.items():
            result[e] = result.get(e, F(0))+c
        return P(result)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.terms.items()})

    def __sub__(self, x):
        return self+-P.cast(x)

    def __rsub__(self, x):
        return P.cast(x)+-self

    def __mul__(self, x):
        result = defaultdict(F)
        for e, c in self.terms.items():
            for f, b in P.cast(x).terms.items():
                result[tuple(a+d for a, d in zip(e, f))] += c*b
        return P(result)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = P.cast(x)
        demand(len(x.terms) == 1, 'nonzero Laurent monomial divisor required')
        f, b = next(iter(x.terms.items()))
        return P({tuple(a-d for a, d in zip(e, f)): c/b for e, c in self.terms.items()})

    def __pow__(self, n):
        demand(type(n) is int, 'integer exponent required')
        if n < 0:
            return P(1)/(self**(-n))
        result, base = P(1), self
        while n:
            if n & 1:
                result = result*base
            base, n = base*base, n//2
        return result

    def coefficient(self, name, power):
        index = NAMES.index(name)
        result = {}
        for e, c in self.terms.items():
            if e[index] == power:
                f = list(e)
                f[index] = 0
                result[tuple(f)] = c
        return P(result)

    def substitute(self, values):
        result = P()
        for e, c in self.terms.items():
            remaining, factor = list(e), P(c)
            for name, value in values.items():
                index = NAMES.index(name)
                remaining[index] = 0
                factor = factor*P.cast(value)**e[index]
            result = result+P({tuple(remaining): 1})*factor
        return result

    def record(self):
        return [[*e, c.numerator, c.denominator] for e, c in sorted(self.terms.items())]

    def univariate_v(self):
        demand(all(not any(e[1:]) for e in self.terms), 'univariate coefficient expected')
        return [[e[0], c.numerator, c.denominator] for e, c in sorted(self.terms.items())]


def variable(name):
    e = list(ZERO)
    e[NAMES.index(name)] = 1
    return P({tuple(e): 1})


V, Z, A, I, X2, Y2, XY, XY2, Y3, Y4 = [variable(name) for name in NAMES]
D = V**(-1)
B = 2*D-D**2
KAPPA = D*(D-F(13, 8))


class G:
    def __init__(self, re=0, im=0):
        self.re, self.im = P.cast(re), P.cast(im)

    @staticmethod
    def cast(x):
        return x if isinstance(x, G) else G(x)

    def __add__(self, x):
        x = G.cast(x)
        return G(self.re+x.re, self.im+x.im)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.re, -self.im)

    def __sub__(self, x):
        return self+-G.cast(x)

    def __rsub__(self, x):
        return G.cast(x)+-self

    def __mul__(self, x):
        x = G.cast(x)
        return G(self.re*x.re-self.im*x.im, self.re*x.im+self.im*x.re)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = G.cast(x)
        numerator = self*x.conjugate()
        norm = x.re*x.re+x.im*x.im
        return G(numerator.re/norm, numerator.im/norm)

    def conjugate(self):
        return G(self.re, -self.im)

    def substitute(self, values):
        return G(self.re.substitute(values), self.im.substitute(values))

    def record(self):
        return [self.re.record(), self.im.record()]


def identity(label, actual, expected=0):
    difference = G.cast(actual)-expected
    demand(not difference.re.terms and not difference.im.terms, label)
    LABELS.append(label)


def series(*values):
    demand(len(values) <= 5, 'too many truncated coefficients')
    return [G.cast(x) for x in values]+[G() for _ in range(5-len(values))]


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def scale(a, x):
    return [v*x for v in a]


def mul(a, b):
    return [sum((a[k]*b[n-k] for k in range(n+1)), G()) for n in range(5)]


def power(a, n):
    result = series(1)
    for _ in range(n):
        result = mul(result, a)
    return result


def inverse(a):
    result = [G(1)/a[0]]
    for n in range(1, 5):
        result.append(-sum((a[k]*result[n-k] for k in range(1, n+1)), G())/a[0])
    return result


def real(a):
    return [G(x.re) for x in a]


def modulus(a, base):
    base = P.cast(base)
    demand(len(base.terms) == 1, 'positive monomial modulus base required')
    exponent, coefficient = next(iter(base.terms.items()))
    demand(coefficient > 0 and not any(exponent[1:]), 'base positive for all v>0')
    square = mul(a, [x.conjugate() for x in a])
    result = [G(base)]
    identity('modulus positive base', result[0]*result[0], square[0])
    for n in range(1, 5):
        result.append((square[n]-sum((result[k]*result[n-k] for k in range(1, n)), G()))/(2*result[0]))
    return result


def analytic_functional(moments, trace):
    value = add(trace, scale(real(moments[2]), -D/2))
    value = add(value, scale(real(moments[3]), D**2/6))
    value = add(value, scale(real(moments[4]), -D**3/8))
    return add(value, scale(power(real(moments[1]), 2), D/14))


def scalar_residues():
    # u_j=v+i y_j t+x_j t^2, with all joint moments kept independent.
    sums = [None, series(0, G(0, I), A), series(0, 0, -Y2, G(0, 2*XY), X2),
            series(0, 0, 0, G(0, -Y3), -3*XY2), series(0, 0, 0, 0, Y4)]
    elementary = [series(1)]
    for ell in range(1, 5):
        value = series()
        for j in range(1, ell+1):
            value = add(value, scale(mul(elementary[ell-j], sums[j]), F((-1)**(j-1), ell)))
        elementary.append(value)
    # C(v+z)=9 product(z-delta)-(v+z) d/dz product(z-delta).
    # C0=z^7(z-8v); the inverse far factor is expanded about z=0.
    inverse_far = sum((-Z**j/(8*V)**(j+1) for j in range(5)), P())
    ratio_minus_one = series()
    for ell in range(1, 5):
        factor = (-1)**ell*Z**(-ell)*((ell+1)*Z-(8-ell)*V)*inverse_far
        ratio_minus_one = add(ratio_minus_one, scale(elementary[ell], factor))
    logarithm = series()
    for ell in range(1, 5):
        logarithm = add(logarithm, scale(power(ratio_minus_one, ell), F((-1)**(ell+1), ell)))
    moments = {}
    for k in range(1, 5):
        moments[k] = [G(-k*x.re.coefficient('z', -k), -k*x.im.coefficient('z', -k))
                      for x in logarithm]
        for order in range(k):
            identity('moment lower order '+str((k, order)), moments[k][order])
    envelope = analytic_functional(moments, series(0, 0, 2*A))
    for order in (0, 1, 3):
        identity('functional even/lower '+str(order), envelope[order])
    identity('complete second coefficient', envelope[2], 2*A+3*D*Y2/8+D*I**2/128)
    p4 = envelope[4].re-3*D*X2/8
    identity('functional fourth coefficient real', envelope[4].im)
    closed = (-59*D**3*Y4/512-47*D**2*XY2/64-83*D**3*Y2**2/14336
              -3*D*X2/4-59*D**3*I*Y3/4096+7*D**2*I*XY/128
              +1277*D**3*I**2*Y2/229376-677*D**3*I**4/1835008
              +23*D**2*A*Y2/512-D**2*A*I**2/128+3*D*A**2/64)
    identity('complete eleven-term normal form', p4, closed)
    c2 = -B/2
    balanced = p4.substitute({'A': c2*Y2, 'I': 0, 'X2': c2**2*Y4,
                             'XY': c2*Y3, 'XY2': c2*Y4})
    alpha = -(D**3)*(96*D**2-196*D+67)/512
    beta = D**3*(168*D**2-350*D-55)/14336
    identity('complete balanced boundary quartic', balanced, alpha*Y4+beta*Y2**2)
    ktrace = -(alpha*F(43, 56)+beta)
    identity('trace coefficient', ktrace, D**3*(3792*D**2-7728*D+2991)/28672)
    singleton = D**3*(516*D**2-528*D-393)/7168
    identity('variance coefficient difference', ktrace-singleton, F(27, 448)*D**3*(D-F(13, 8))**2)
    cutoff = {'v': F(8, 13)}
    identity('sharp cutoff', ktrace.substitute(cutoff), F(560235, 8388608))
    near_trace = moments[1][2].re.substitute({'I': 0, 'A': c2*Y2})
    identity('balanced near trace', near_trace, (7*c2/8+9*D/64)*Y2)
    cauchy_gain = D*(7*c2/8+9*D/64)**2/14
    identity('cutoff Cauchy gain', cauchy_gain.substitute(cutoff), F(19773, 117440512))
    identity('disk cancellation', 3*D/8-B, KAPPA)
    identity('disk branch budget', B+KAPPA, 3*D/8)
    # Explicit positivity on d=d0+s, s>=0, without numerical sampling.
    # Polynomial substitutions are made in d directly, avoiding inverse of a binomial.
    identity('alpha sign shifted', 96*(F(13, 8)+Z)**2-196*(F(13, 8)+Z)+67,
             2+116*Z+96*Z**2)
    identity('trace sign shifted', 3792*(F(13, 8)+Z)**2-7728*(F(13, 8)+Z)+2991,
             F(1785, 4)+4596*Z+3792*Z**2)
    identity('improved real-part budget',
             1+(F(13, 8)+Z)**2/2-F(19, 16)*(F(13, 8)+Z),
             F(25, 64)+7*Z/16+Z**2/2)
    coeffs = {'alpha_laurent': alpha.univariate_v(), 'beta_laurent': beta.univariate_v(),
              'ktrace_laurent': ktrace.univariate_v(),
              'cutoff_sharp_coefficient': [560235, 8388608],
              'cutoff_cauchy_gain': [19773, 117440512]}
    return moments, envelope, p4, coeffs


def original_critical_root(linear, constant, base):
    # Directly differentiated original p(a+y), not reciprocal discriminants.
    value = series(base)
    derivative = G(18*base)+linear[0]
    for n in range(1, 5):
        residual = add(add(scale(mul(value, value), 9), mul(linear, value)), constant)
        value[n] = -residual[n]/derivative
    residual = add(add(scale(mul(value, value), 9), mul(linear, value)), constant)
    for n in range(5):
        identity('original critical residual '+str(n), residual[n])
    return value


def moment_values(r, xa, xb, ya, yb):
    s = 8-r
    return {'A': r*xa+s*xb, 'I': r*ya+s*yb, 'X2': r*xa**2+s*xb**2,
            'Y2': r*ya**2+s*yb**2, 'XY': r*xa*ya+s*xb*yb,
            'XY2': r*xa*ya**2+s*xb*yb**2, 'Y3': r*ya**3+s*yb**3,
            'Y4': r*ya**4+s*yb**4}


def original_controls(moments, generic_envelope):
    controls = []
    for r in range(1, 8):
        s = 8-r
        for balanced in (False, True):
            ya, yb = (F(s), F(-r)) if balanced else (F(r-4, 3), F(s+2, 5))
            xa = -B*ya**2/2+(0 if balanced else F(r, 17))
            xb = -B*yb**2/2+(0 if balanced else F(s, 19))
            controls.append((r, xa, xb, ya, yb))
    controls.append((3, P(F(2, 7)), P(F(3, 11)), F(0), F(0)))
    for index, (r, xa, xb, ya, yb) in enumerate(controls):
        s = 8-r
        ua, ub = series(V, G(0, ya), xa), series(V, G(0, yb), xb)
        alpha, beta = inverse(ua), inverse(ub)
        linear = add(scale(alpha, s+1), scale(beta, r+1))
        constant = mul(alpha, beta)
        ynear = original_critical_root(linear, constant, -D)
        yfar = original_critical_root(linear, constant, -D/9)
        qnear, qfar = scale(inverse(ynear), -1), scale(inverse(yfar), -1)
        da, db, dn = add(ua, series(-V)), add(ub, series(-V)), add(qnear, series(-V))
        actual_moments = {}
        substitution = moment_values(r, xa, xb, ya, yb)
        for k in range(1, 5):
            actual_moments[k] = add(add(scale(power(da, k), r-1), scale(power(db, k), s-1)), power(dn, k))
            for order in range(5):
                identity('complete original moment '+str((index, k, order)),
                         actual_moments[k][order], moments[k][order].substitute(substitution))
        trace = scale(add(scale(real(da), r), scale(real(db), s)), 2)
        envelope = analytic_functional(actual_moments, trace)
        for order in range(5):
            identity('complete original functional '+str((index, order)),
                     envelope[order], generic_envelope[order].substitute(substitution))
        actual_moduli = add(add(scale(modulus(ua, V), r-1), scale(modulus(ub, V), s-1)),
                            add(modulus(qnear, V), modulus(qfar, 9*V)))
        gap = add(actual_moduli, series(-16*V))
        real_squares = add(add(scale(power(real(da), 2), r-1), scale(power(real(db), 2), s-1)),
                           power(real(dn), 2))
        variance = add(real_squares, scale(power(real(actual_moments[1]), 2), -F(1, 7)))
        far_loss = add(modulus(qfar, 9*V), scale(real(qfar), -1))
        difference = add(add(gap, scale(envelope, -1)),
                         add(scale(variance, -D/2), scale(far_loss, -1)))
        for order in range(5):
            identity('actual modulus/variance/far identity '+str((index, order)), difference[order])
        RECORDS.append([index, [x.record() for x in envelope], [x.record() for x in variance]])
    return len(controls)


def quartic_basis(p4):
    groups = defaultdict(dict)
    for e, c in p4.terms.items():
        demand(e[1] == 0, 'residue variable must be eliminated')
        key = tuple(e[2:])
        groups[key][e[0]] = c
    result = []
    for key, coeffs in sorted(groups.items()):
        label = '*'.join(name+(('^'+str(exponent)) if exponent > 1 else '')
                         for name, exponent in zip(NAMES[2:], key) if exponent)
        result.append({'moment_monomial': label,
                       'coefficient_in_v': [[e, c.numerator, c.denominator] for e, c in sorted(coeffs.items())]})
    return result


def moment_rigidity_controls():
    lower_z = F(9, 14)-F(12, 5)*F(1, 100)
    controls = {
        'skew lower square': lower_z > F(31, 40)**2,
        'root gap lower square': lower_z+F(1, 2) > F(11, 10),
        'root gap upper square': F(8, 7) < F(15, 14)**2,
        'rounding sum excludes multiplicities': F(448, 11)*F(1, 100) < F(4, 9),
        'zero positive roots excluded': F(14, 15) > F(2, 3),
        'two positive roots excluded': F(67, 70) > F(2, 3),
        'projection scale lower': F(7, 8)*F(11, 10) > F(7, 8)**2,
        'coarse moment rigidity constant': F(64, 11) < 6,
    }
    for label, condition in controls.items():
        demand(condition, label)
        LABELS.append(label)
    return len(controls)


def main():
    demand(len(sys.argv) == 1, 'Usage: python3 -I -B independent_check.py')
    moments, envelope, p4, coeffs = scalar_residues()
    count = original_controls(moments, envelope)
    basis = quartic_basis(p4)
    rigidity_count = moment_rigidity_controls()
    records = {'moments': {str(k): [x.record() for x in moments[k]] for k in moments},
               'quartic': p4.record(), 'original_controls': RECORDS}
    digest = sha256(json.dumps(records, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    output = {'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
              'arithmetic': 'Q[v,v^-1,z,z^-1,A,I,X2,Y2,XY,XY2,Y3,Y4][i][t]/(t^5)',
              'joint_moment_names': list(NAMES[2:]), 'method': 'scalar characteristic logarithmic residues and implicit original critical roots',
              'checks': len(LABELS), 'complete_quartic_basis': basis,
              'quartic_basis_size': len(basis), 'original_critical_controls': count,
              'rational_moment_rigidity_controls': rigidity_count,
              'unbalanced_moment_series': {str(k): [x.record() for x in moments[k]] for k in moments},
              **coeffs, 'records_sha256': digest,
              'not_machine_checked': ['uniform contour and weighted Taylor remainders', 'disk substitution/centering absorption',
                                      'basin completeness', 'quantitative fixed-energy minimizers']}
    fixture = Path(__file__).with_name('expected.json')
    demand(fixture.is_file(), 'required expected.json fixture is missing')
    demand(output == json.loads(fixture.read_text()), 'complete expected fixture mismatch')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
