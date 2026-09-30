#!/usr/bin/env python3
"""Independent original-critical-point and rational-matrix Sendov checks.

Standard-library Q[d,d^-1][i][t]/(t^5), d=1+a>0. No author imports.
Taylor roots are solved implicitly in y=zeta-a, not by a reciprocal-root
discriminant. Finite matrix controls do not prove uniform spectral bounds.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from math import factorial
from pathlib import Path
import json
import sys

LABELS = []
RECORDS = []


def demand(condition, message):
    if not condition:
        raise ValueError(message)


class L:
    """Sparse rational Laurent polynomial in d; division by monomials only."""
    def __init__(self, value=0):
        self.terms = ({e: F(c) for e, c in value.items() if c}
                      if isinstance(value, dict) else ({0: F(value)} if value else {}))

    @staticmethod
    def cast(x):
        return x if isinstance(x, L) else L(x)

    def __add__(self, x):
        result = dict(self.terms)
        for e, c in L.cast(x).terms.items():
            result[e] = result.get(e, F(0)) + c
        return L(result)

    __radd__ = __add__

    def __neg__(self):
        return L({e: -c for e, c in self.terms.items()})

    def __sub__(self, x):
        return self + -L.cast(x)

    def __rsub__(self, x):
        return L.cast(x) + -self

    def __mul__(self, x):
        result = defaultdict(F)
        for e, c in self.terms.items():
            for f, b in L.cast(x).terms.items():
                result[e+f] += c*b
        return L(result)

    __rmul__ = __mul__

    def __truediv__(self, x):
        x = L.cast(x)
        demand(len(x.terms) == 1, 'nonzero monomial divisor required')
        f, b = next(iter(x.terms.items()))
        return L({e-f: c/b for e, c in self.terms.items()})

    def __pow__(self, n):
        demand(type(n) is int and n >= 0, 'nonnegative integer power required')
        result, base = L(1), self
        while n:
            if n & 1:
                result = result*base
            base, n = base*base, n//2
        return result

    def evaluate(self, d):
        return sum((c*d**e for e, c in self.terms.items()), F(0))

    def record(self):
        return [[e, c.numerator, c.denominator] for e, c in sorted(self.terms.items())]


D = L({1: 1})
V = L({-1: 1})


class G:
    def __init__(self, re=0, im=0):
        self.re, self.im = L.cast(re), L.cast(im)

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
        return self + -G.cast(x)

    def __rsub__(self, x):
        return G.cast(x) + -self

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

    def evaluate(self, d):
        return G(self.re.evaluate(d), self.im.evaluate(d))

    def record(self):
        return [self.re.record(), self.im.record()]


def identity(label, left, right=0):
    difference = G.cast(left)-right
    demand(not difference.re.terms and not difference.im.terms, label)
    LABELS.append(label)


def series(*values):
    demand(len(values) <= 5, 'too many series coefficients')
    return [G.cast(x) for x in values]+[G() for _ in range(5-len(values))]


def add(a, b):
    return [x+y for x, y in zip(a, b)]


def scale(a, x):
    return [v*x for v in a]


def mul(a, b):
    return [sum((a[k]*b[n-k] for k in range(n+1)), G()) for n in range(5)]


def inverse(a):
    result = [G(1)/a[0]]
    for n in range(1, 5):
        result.append(-sum((a[k]*result[n-k] for k in range(1, n+1)), G())/a[0])
    return result


def positive_modulus(a, positive_base):
    """Recursive sqrt(a conjugate(a)); caller supplies the positive base."""
    squared = mul(a, [x.conjugate() for x in a])
    result = [G(positive_base)]
    identity('positive modulus base', result[0]*result[0], squared[0])
    demand(positive_base.evaluate(F(13, 8)) > 0, 'base must be positive at cutoff')
    for n in range(1, 5):
        result.append((squared[n]-sum((result[k]*result[n-k] for k in range(1, n)), G()))/(2*result[0]))
    return result


def exponential(phase):
    result, power = series(), series(1)
    for k in range(5):
        result = add(result, scale(power, F(1, factorial(k))))
        power = mul(power, scale(phase, G(0, 1)))
    return result


def implicit_critical_root(linear, constant, base):
    # 9 y^2 + linear(t) y + constant(t)=0; derivative at base is +-8d.
    result = series(base)
    denominator = G(18*base)+linear[0]
    demand(bool(denominator.re.terms), 'simple critical-point branch required')
    for n in range(1, 5):
        residual = add(add(scale(mul(result, result), 9), mul(linear, result)), constant)
        result[n] = -residual[n]/denominator
    residual = add(add(scale(mul(result, result), 9), mul(linear, result)), constant)
    for n in range(5):
        identity('original critical quadratic order '+str(n), residual[n])
    return result


def two_block(r, phase_a, phase_b, radial_a=None, radial_b=None, marked_shift=None):
    s = 8-r
    radial_a, radial_b = radial_a or series(), radial_b or series()
    marked = add(series(D-1), marked_shift or series())
    # alpha=a-z_A, beta=a-z_B, directly in original critical-point coordinates.
    alpha = add(marked, mul(add(series(1), scale(radial_a, -1)), exponential(phase_a)))
    beta = add(marked, mul(add(series(1), scale(radial_b, -1)), exponential(phase_b)))
    linear = add(scale(alpha, s+1), scale(beta, r+1))
    constant = mul(alpha, beta)
    near = implicit_critical_root(linear, constant, -D)
    far = implicit_critical_root(linear, constant, -D/9)
    reciprocal_lengths = add(scale(inverse(positive_modulus(alpha, D)), r-1),
                             scale(inverse(positive_modulus(beta, D)), s-1))
    reciprocal_lengths = add(reciprocal_lengths, inverse(positive_modulus(near, D)))
    reciprocal_lengths = add(reciprocal_lengths, inverse(positive_modulus(far, D/9)))
    center = inverse(add(marked, series(1)))
    gap = add(reciprocal_lengths, scale(center, -16))
    energy = series()
    for multiplicity, distance in ((r, alpha), (s, beta)):
        displacement = add(inverse(distance), scale(center, -1))
        energy = add(energy, scale(mul(displacement, [x.conjugate() for x in displacement]), multiplicity))
    return gap, energy


def exact_taylor_checks():
    gap, energy = two_block(1, series(0, 7), series(0, -1))
    kappa = D*(D-F(13, 8))
    e2 = 56*V**4
    e4 = -F(602, 3)*V**4+2408*V**5-2408*V**6
    g2 = 56*(V**2-F(13, 8)*V**3)
    g4 = -F(602, 3)*V**2+F(7525, 3)*V**3-6090*V**4+F(65359, 16)*V**5
    for n in (0, 1, 3):
        identity('singleton gap vanishes order '+str(n), gap[n])
        identity('singleton energy vanishes order '+str(n), energy[n])
    identity('singleton generic energy second', energy[2], e2)
    identity('singleton generic energy fourth', energy[4], e4)
    identity('singleton generic gap second', gap[2], g2)
    identity('singleton generic gap fourth', gap[4], g4)
    # A separate direct original-distance energy expansion, without u-v.
    distance_energy = series()
    for count, slope in ((1, 7), (7, -1)):
        cosine = series(1, 0, -F(slope*slope, 2), 0, F(slope**4, 24))
        numerator = scale(add(series(1), scale(cosine, -1)), 2*V**2)
        denominator = add(series((D-1)**2+1), scale(cosine, 2*(D-1)))
        distance_energy = add(distance_energy, scale(mul(numerator, inverse(denominator)), count))
    for n in range(5):
        identity('direct original-distance energy order '+str(n), energy[n], distance_energy[n])
    k1 = D**3*(516*D**2-528*D-393)/7168
    identity('generic normalized quartic', -(gap[4]-energy[4]*kappa)/(e2*e2), k1)
    cutoff = F(13, 8)
    cstar = F(560235, 8388608)
    identity('cutoff sharp quartic', k1.evaluate(cutoff), cstar)
    identity('sharp radius reciprocal', 1/cstar, F(8388608, 560235))
    identity('generic angular quadratic', 2*(V**2/2-V**3)+F(3, 8)*V**3, kappa*V**4)
    RECORDS.append(['singleton', [x.record() for x in gap], [x.record() for x in energy]])
    # Different nonlinear profiles from the author: all seven two-block ranks.
    p8 = F(10985, 33554432)
    for r in range(1, 8):
        s = 8-r
        ba, bb = F(r-3, 13), F(s+2, 17)
        ca, cb = F(2*r+1, 19), F(3-s, 23)
        ra, rb, eta = F(r, 29), F(s, 31), F(r+s, 37)
        g, e = two_block(r, series(0, s, ba, ca), series(0, -r, bb, cb),
                         series(0, 0, 0, 0, ra), series(0, 0, 0, 0, rb),
                         series(0, 0, eta))
        mu2 = F(8*r*s)
        angular = p8*(224*F(64-3*r*s, 8*r*s)+32)
        expected = F(13, 8)*eta*F(8, 13)**4*mu2
        expected += F(128, 169)*(r*ra+s*rb)+F(40, 2197)*(r*ba+s*bb)**2
        expected -= angular*F(8, 13)**8*mu2**2
        for n in range(4):
            identity('joint profile lower gap '+str((r, n)), g[n].evaluate(cutoff))
        identity('joint profile cutoff gap '+str(r), g[4].evaluate(cutoff), expected)
        identity('joint profile energy '+str(r), e[2].evaluate(cutoff), F(8, 13)**4*mu2)
        RECORDS.append(['joint '+str(r), [x.record() for x in g], [x.record() for x in e]])
    return {'energy_second': e2.record(), 'energy_fourth': e4.record(),
            'gap_second': g2.record(), 'gap_fourth': g4.record(),
            'K1_in_d': k1.record(), 'sharp_radius': [8388608, 560235]}


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), G())
             for j in range(len(b[0]))] for i in range(len(a))]


def matrix_identity(label, a, b):
    for i in range(len(a)):
        for j in range(len(a[0])):
            identity(label+str((i, j)), a[i][j], b[i][j])


def rational_matrix_checks():
    q = [[G(F(1, 8)) for _ in range(8)] for _ in range(8)]
    p = [[G(int(i == j)-F(1, 8)) for j in range(8)] for i in range(8)]
    s = [[G(int(i == j)+F(1, 4)) for j in range(8)] for i in range(8)]
    profiles = [[8-r]*r+[-r]*(8-r) for r in range(1, 8)]
    profiles += [[1, -1, 0, 0, 0, 0, 0, 0], [-7, -5, -3, -1, 1, 3, 5, 7],
                 [3, 3, 3, 3, -1, -1, -5, -5]]
    repeated_pairs = 0
    for index, theta in enumerate(profiles):
        diagonal = [[G(theta[i] if i == j else 0) for j in range(8)] for i in range(8)]
        a = mm(mm(p, diagonal), p)
        aa = mm(a, a)
        t2 = mm(mm(p, mm(diagonal, diagonal)), p)
        ww = [[G(F(theta[i]*theta[j], 8)) for j in range(8)] for i in range(8)]
        matrix_identity('compression identity '+str(index), t2,
                        [[aa[i][j]+ww[i][j] for j in range(8)] for i in range(8)])
        v = F(8, 13)
        c2 = v*v/2-v**3
        rmat = mm(mm(s, diagonal), s)
        correction = mm(mm(p, mm(mm(rmat, q), rmat)), p)
        matrix_identity('separated graph correction '+str(index),
                        [[x*(v**3/8) for x in row] for row in correction],
                        [[x*(9*v**3/8) for x in row] for row in ww])
        cmat = [[aa[i][j]*c2+ww[i][j]*(c2+9*v**3/8) for j in range(8)] for i in range(8)]
        for i in range(8):
            for j in range(i):
                if theta[i] == theta[j]:
                    repeated_pairs += 1
                    y = [G(int(k == i)-int(k == j)) for k in range(8)]
                    for k in range(8):
                        identity('repeated-block scalar action',
                                 sum((cmat[k][ell]*y[ell] for ell in range(8)), G()),
                                 y[k]*(c2*theta[i]**2))
    # Unbalanced phase trace formula in a separate set of exact controls.
    for index in range(10):
        phi = [F((j+1)*(index+2) % 11-5, index+3) for j in range(8)]
        diagonal = [[G(phi[i] if i == j else 0) for j in range(8)] for i in range(8)]
        trace_matrix = mm(mm(mm(p, diagonal), p), diagonal)
        identity('unbalanced trace '+str(index), sum((trace_matrix[i][i] for i in range(8)), G()),
                 F(3, 4)*sum(x*x for x in phi)+sum(phi)**2/64)
    return {'angular_matrix_profiles': len(profiles), 'repeated_equal_coordinate_pairs': repeated_pairs,
            'unbalanced_trace_profiles': 10}


def polynomial_mul(a, b):
    out = [G() for _ in range(len(a)+len(b)-1)]
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] = out[i+j]+x*y
    return out


def companion_checks():
    profiles = [
        [G(-1)]*8,
        [G(-1)]*7+[G(F(-3, 5), F(4, 5))],
        [G(F(-3, 5), F(4, 5))]*4+[G(F(-3, 5), F(-4, 5))]*4,
        [G(F(j-8, 10), F((j % 3)-1, 10)) for j in range(8)],
        [G(0), G(-1), G(F(-1, 2), F(1, 2)), G(F(-1, 2), F(-1, 2)),
         G(F(1, 3)), G(F(2, 5), F(1, 5)), G(F(-2, 5), F(-1, 5)), G(F(-1, 4))],
    ]
    s = [[G(int(i == j)+F(1, 4)) for j in range(8)] for i in range(8)]
    for index, roots in enumerate(profiles):
        marked = F(5+index, 16)
        alpha = [marked-z for z in roots]
        u = [G(1)/x for x in alpha]
        diagonal = [[u[i] if i == j else G() for j in range(8)] for i in range(8)]
        b = mm(mm(s, diagonal), s)
        # Characteristic coefficients from exact traces and Newton identities.
        powers, traces = b, []
        for k in range(1, 9):
            traces.append(sum((powers[i][i] for i in range(8)), G()))
            if k < 8:
                powers = mm(powers, b)
        elementary = [G(1)]
        for k in range(1, 9):
            elementary.append(sum((elementary[k-j]*traces[j-1]*((-1)**(j-1))
                                   for j in range(1, k+1)), G())/k)
        # Independent polynomial in y=z-a; differentiate before reciprocation.
        poly = [G(0), G(1)]
        for x in alpha:
            poly = polynomial_mul(poly, [x, G(1)])
        derivative = [poly[k+1]*(k+1) for k in range(9)]
        transformed = [derivative[8-k]*((-1)**(8-k))/derivative[0] for k in range(9)]
        for k in range(9):
            identity('companion/original-derivative coefficient '+str((index, k)),
                     transformed[k], elementary[8-k]*((-1)**(8-k)))
        RECORDS.append(['companion '+str(index), [x.record() for x in transformed]])
    return len(profiles)


def main():
    demand(len(sys.argv) == 1, 'Usage: python3 -I -B independent_check.py')
    coefficients = exact_taylor_checks()
    matrix_counts = rational_matrix_checks()
    companion_count = companion_checks()
    digest = sha256(json.dumps(RECORDS, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    manifest = {'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
                'arithmetic': 'standard-library Q[d,d^-1][i][t]/(t^5), d=1+a>0',
                'method': 'implicit original critical roots; direct original-distance energy; exact rational matrices',
                'checks': len(LABELS), 'singleton_symbolic_profiles': 1, 'nonlinear_joint_profiles': 7,
                'original_derivative_companion_profiles': companion_count,
                **matrix_counts, 'coefficients': coefficients, 'records_sha256': digest,
                'not_machine_checked': ['arbitrary-root uniform estimates', 'all angular collisions',
                                        'basin completeness', 'inverse and implicit function theorems',
                                        'fixed-energy variational envelope']}
    fixture = Path(__file__).with_name('expected.json')
    demand(fixture.is_file(), 'required compact expected.json is missing')
    demand(manifest == json.loads(fixture.read_text()), 'complete manifest differs from expected.json')
    print(json.dumps(manifest, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
