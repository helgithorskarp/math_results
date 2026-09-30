#!/usr/bin/env python3
"""Independent exact sextic Sendov audit.

Scalar characteristic residues reconstruct the global quartic mean term;
implicit roots of directly differentiated translated polynomials supply
sixth-order controls. No author module or reciprocal discriminant is used.
The multivariate sparse arithmetic kernel adapts this reviewer's own
previous published checker. Ordinary analytic coverage remains external.
"""
from collections import defaultdict
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json
import sys
from math import factorial

NAMES = ('v', 'z', 'A', 'I', 'X2', 'Y2', 'XY', 'XY2', 'Y3', 'Y4', 'rho', 'beta', 'lam', 'r', 's')
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


V, Z, A, I, X2, Y2, XY, XY2, Y3, Y4, RHO, BETA, LAM, R, SS = [variable(name) for name in NAMES]
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


def series(*values, order=6):
    demand(len(values) <= order+1, 'too many truncated coefficients')
    return [G.cast(x) for x in values]+[G() for _ in range(order+1-len(values))]


def add(a, b):
    demand(len(a) == len(b), 'series order mismatch')
    return [x+y for x, y in zip(a, b)]


def scale(a, c):
    return [x*c for x in a]


def mul(a, b):
    demand(len(a) == len(b), 'product order mismatch')
    return [sum((a[k]*b[n-k] for k in range(n+1)), G()) for n in range(len(a))]


def power(a, n):
    b = series(1, order=len(a)-1)
    for _ in range(n):
        b = mul(b, a)
    return b


def inverse(a):
    b = [G(1)/a[0]]
    for n in range(1, len(a)):
        b.append(-sum((a[k]*b[n-k] for k in range(1, n+1)), G())/a[0])
    return b


def real(a):
    return [G(x.re) for x in a]


def imag(a):
    return [G(x.im) for x in a]


def substitute(a, values):
    return [x.substitute(values) for x in a]


def check_series(label, a, b=None):
    b = b if b is not None else series(order=len(a)-1)
    demand(len(a) == len(b), 'comparison order mismatch')
    for k, (x, y) in enumerate(zip(a, b)):
        identity(label+':'+str(k), x, y)


def modulus(a, base):
    # Solve the defining square equation with the positive constant branch.
    b = [G(base)]
    square = mul(a, [x.conjugate() for x in a])
    identity('positive modulus base', b[0]*b[0], square[0])
    for n in range(1, len(a)):
        b.append((square[n]-sum((b[k]*b[n-k] for k in range(1, n)), G()))/(2*b[0]))
    return b


def exp_i(phi):
    b, c = series(1), series()
    for k in range(7):
        c = add(c, scale(b, F(1, factorial(k))))
        b = mul(b, scale(phi, G(0, 1)))
    return c


def functional(moments, trace, far, v):
    vi = inverse(v)
    value = trace
    for k, c in [(2, F(-1, 2)), (3, F(1, 6)), (4, F(-1, 8)),
                 (5, F(3, 40)), (6, F(-1, 16))]:
        value = add(value, scale(mul(real(moments[k]), power(vi, k-1)), c))
    m = real(moments[1])
    value = add(value, scale(mul(power(m, 2), vi), F(1, 14)))
    value = add(value, scale(mul(power(m, 3), power(vi, 2)), F(-1, 294)))
    value = add(value, scale(mul(mul(power(m, 2), real(moments[2])), power(vi, 3)), F(1, 196)))
    return add(value, add(modulus(far, 9*v[0].re), scale(real(far), -1)))


def global_mean_residue():
    # Complete joint moments through weight four, independent of profile fits.
    def s(*a):
        return series(*a, order=4)
    sums = [None, s(0, G(0, I), A), s(0, 0, -Y2, G(0, 2*XY), X2),
            s(0, 0, 0, G(0, -Y3), -3*XY2), s(0, 0, 0, 0, Y4)]
    elementary = [s(1)]
    for ell in range(1, 5):
        value = s()
        for j in range(1, ell+1):
            value = add(value, scale(mul(elementary[ell-j], sums[j]), F((-1)**(j-1), ell)))
        elementary.append(value)
    inverse_far = sum((-Z**j/(8*V)**(j+1) for j in range(5)), P())
    w = s()
    for ell in range(1, 5):
        factor = (-1)**ell*Z**(-ell)*((ell+1)*Z-(8-ell)*V)*inverse_far
        w = add(w, scale(elementary[ell], factor))
    logarithm = s()
    for ell in range(1, 5):
        logarithm = add(logarithm, scale(power(w, ell), F((-1)**(ell+1), ell)))
    moments = {k: [G(-k*x.re.coefficient('z', -k), -k*x.im.coefficient('z', -k))
                   for x in logarithm] for k in range(1, 5)}
    ell4 = s(0, 0, 2*A)
    for k, c in [(2, -D/2), (3, D**2/6), (4, -D**3/8)]:
        ell4 = add(ell4, scale(real(moments[k]), c))
    ell4 = add(ell4, scale(power(real(moments[1]), 2), D/14))
    p4 = ell4[4].re-3*D*X2/8
    far = add(s(9*V), add(scale(sums[1], 2), scale(moments[1], -1)))
    loss = add(modulus(far, 9*V), scale(real(far), -1))
    boundary = {'A': -B*Y2/2, 'X2': B**2*Y4/4, 'XY': -B*Y3/2, 'XY2': -B*Y4/2}
    total_q4 = (p4+loss[4].re).substitute(boundary)
    translated = total_q4.substitute({'Y2': Y2+I**2/8,
                    'Y3': Y3+3*I*Y2/8+I**3/64,
                    'Y4': Y4+I*Y3/2+3*I**2*Y2/32+I**4/512})
    c = translated.coefficient('I', 1).coefficient('Y3', 1)
    identity('complete global quartic linear mean', translated.coefficient('I', 1), c*Y3)
    identity('global quartic mean closed form', c, D**3*(-48*D**2+121*D-88)/512)
    identity('cutoff global mean coefficient', c.substitute({'v': F(8, 13)}), F(-318565, 2097152))
    identity('near quadratic mean', ell4[2].re, 2*A+3*D*Y2/8+D*I**2/128)
    identity('far quadratic mean', loss[2].re, 9*D*I**2/128)
    RECORDS.append(['generic-quartic-residue', {str(k): [x.record() for x in moments[k]] for k in moments}, total_q4.record(), c.record()])
    return c


def original_root(linear, constant, base, label):
    # Roots of p'(a+y) after its repeated linear factors are removed.
    value = series(base)
    derivative = G(18*base)+linear[0]
    for n in range(1, 7):
        residual = add(add(scale(mul(value, value), 9), mul(linear, value)), constant)
        value[n] = -residual[n]/derivative
    residual = add(add(scale(mul(value, value), 9), mul(linear, value)), constant)
    check_series(label+' original differentiated root', residual)
    return value


def boundary_reciprocal(y, a, v):
    b = add(series(1), scale(power(a, 2), -1))
    x = series()
    for n, c in [(2, F(-1, 2)), (4, F(-1, 8)), (6, F(-1, 16))]:
        x = add(x, scale(mul(power(b, n-1), power(y, n)), c))
    return add(v, add(x, scale(y, G(0, 1))))


def original_profile(r, a, v, ua, ub, label):
    s = 8-r
    alpha, beta = inverse(ua), inverse(ub)
    linear = add(scale(alpha, s+1), scale(beta, r+1))
    constant = mul(alpha, beta)
    yn = original_root(linear, constant, -P(1)/v[0].re, label+' near')
    yf = original_root(linear, constant, -P(1)/(9*v[0].re), label+' far')
    qn, qf = scale(inverse(yn), -1), scale(inverse(yf), -1)
    da, db, dn = add(ua, scale(v, -1)), add(ub, scale(v, -1)), add(qn, scale(v, -1))
    za, zb = add(a, scale(alpha, -1)), add(a, scale(beta, -1))
    for name, z in [('A', za), ('B', zb)]:
        check_series(label+' original unit-circle '+name, mul(z, [x.conjugate() for x in z]), series(1))
    def near_sum(fn):
        return add(add(scale(fn(da), r-1), scale(fn(db), s-1)), fn(dn))
    moments = {k: near_sum(lambda x: power(x, k)) for k in range(1, 7)}
    check_series(label+' differentiated trace', add(add(scale(ua, r-1), scale(ub, s-1)), add(qn, qf)),
                 scale(add(scale(ua, r), scale(ub, s)), 2))
    energy = add(scale(mul(da, [x.conjugate() for x in da]), r), scale(mul(db, [x.conjugate() for x in db]), s))
    gap = add(add(scale(modulus(ua, v[0].re), r-1), scale(modulus(ub, v[0].re), s-1)),
              add(modulus(qn, v[0].re), modulus(qf, 9*v[0].re)))
    gap = add(gap, scale(v, -16))
    trace = scale(real(add(scale(da, r), scale(db, s))), 2)
    analytic = functional(moments, trace, qf, v)
    rm = real(moments[1])
    variance = add(near_sum(lambda x: power(real(x), 2)), scale(power(rm, 2), F(-1, 7)))
    cubic_defect = add(near_sum(lambda x: power(real(x), 3)), scale(power(rm, 3), F(-1, 49)))
    mixed_defect = add(near_sum(lambda x: mul(power(real(x), 2), power(imag(x), 2))),
                       scale(mul(power(rm, 2), real(moments[2])), F(1, 49)))
    vi = inverse(v)
    correction = scale(mul(variance, vi), F(1, 2))
    correction = add(correction, scale(mul(cubic_defect, power(vi, 2)), F(-1, 6)))
    correction = add(correction, scale(mul(mixed_defect, power(vi, 3)), F(-1, 4)))
    check_series(label+' complete variance defect', add(gap, scale(analytic, -1)), correction)
    RECORDS.append([label, [x.record() for x in gap], [x.record() for x in energy],
                    [x.record() for x in analytic], [x.record() for x in variance],
                    [x.record() for x in qn], [x.record() for x in qf]])
    return gap, energy, analytic, variance, qn, ub


def scalar_control():
    q = series(V, G(0, SS), R)
    xi = add(q, series(-V))
    value = series()
    for k, c in [(2, -D/2), (3, D**2/6), (4, -D**3/8), (5, 3*D**4/40), (6, -D**5/16)]:
        value = add(value, scale(real(power(xi, k)), c))
    value = add(value, scale(power(real(xi), 2), D/2))
    value = add(value, scale(power(real(xi), 3), -D**2/6))
    value = add(value, scale(mul(power(real(xi), 2), power(imag(xi), 2)), -D**3/4))
    check_series('fully symbolic weighted scalar modulus', add(modulus(q, V), scale(real(q), -1)), value)
    RECORDS.append(['scalar-modulus-v-r-s', [x.record() for x in value]])


def kt(d):
    return d**3*(3792*d**2-7728*d+2991)/28672


def kt_series(d):
    inner = add(add(scale(power(d, 2), 3792), scale(d, -7728)), series(2991))
    return scale(mul(power(d, 3), inner), F(1, 28672))


def corrected(gap, energy, a):
    d = add(series(1), a)
    kappa = mul(d, add(a, series(-F(5, 8))))
    return add(add(gap, scale(mul(kappa, energy), -1)), mul(kt_series(d), power(energy, 2)))


def parameter_coefficients(value, name):
    index = NAMES.index(name)
    demand(all(not any(e[:index]+e[index+1:]) for e in value.terms), 'univariate parameter polynomial required')
    return [[e[index], c.numerator, c.denominator] for e, c in sorted(value.terms.items())]


def constant_fraction(value):
    p = P.cast(value)
    demand(all(e == ZERO for e in p.terms), 'constant rational output expected')
    c = p.terms.get(ZERO, F(0))
    return [c.numerator, c.denominator]


def derive():
    cmean = global_mean_residue()
    scalar_control()
    a0, v0, d0 = F(5, 8), F(8, 13), F(13, 8)
    cstar = F(560235, 8388608)
    dstar = F(520320727875, 6734508720128)
    # Generic marked radius also checks the necessary real variance scale.
    a, v = series(D-1), series(V)
    ua = boundary_reciprocal(series(0, 7, 0, RHO), a, v)
    ub = boundary_reciprocal(series(0, -1, 0, RHO), a, v)
    gg, ee, aa, vv, qn, ub = original_profile(1, a, v, ua, ub, 'generic-radius-circle-cubic-mean')
    identity('singleton isolated real second contrast', qn[2].re-ub[2].re, 21*D*(D-d0))
    identity('singleton variance radius penalty', vv[4].re, 378*D**2*(D-d0)**2)
    g, e, analytic, variance = [substitute(x, {'v': v0}) for x in [gg, ee, aa, vv]]
    check_series('cutoff circle variance through six', variance)
    check_series('cutoff circle analytic saturation', add(g, scale(analytic, -1)))
    remainder = add(g, scale(power(e, 2), cstar))
    for k in range(6):
        identity('circle cutoff lower cancellation '+str(k), remainder[k])
    circle_d = remainder[6].re/e[2].re**3
    s0 = circle_d.coefficient('rho', 0)
    alpha0 = F(5, 64)/v0
    identity('circle constant sextic', s0, F(717042898065, 6734508720128))
    identity('circle global mean coefficient', circle_d.coefficient('rho', 1), cmean.substitute({'v': v0})*F(3, 196))
    identity('circle quadratic mean', circle_d.coefficient('rho', 2), 64*alpha0/56**3)
    rhoopt = -circle_d.coefficient('rho', 1)/(2*circle_d.coefficient('rho', 2))
    identity('circle cubic mean optimum', rhoopt, F(102921, 4096))
    identity('circle sharp energy sextic', circle_d.substitute({'rho': rhoopt}), dstar)
    ua = inverse(add(series(a0), exp_i(series(0, 7, 0, BETA))))
    ub = inverse(add(series(a0), exp_i(series(0, -1, 0, BETA))))
    g, e, analytic, variance, _, _ = original_profile(1, series(a0), series(v0), ua, ub, 'original-angular-cubic-mean')
    check_series('angular analytic saturation', add(g, scale(analytic, -1)))
    remainder = add(g, scale(power(e, 2), cstar))
    for k in range(6):
        identity('angular cutoff lower cancellation '+str(k), remainder[k])
    angular_d = remainder[6].re/e[2].re**3
    betaopt = -angular_d.coefficient('beta', 1)/(2*angular_d.coefficient('beta', 2))
    identity('original common phase optimum', betaopt, F(112, 169))
    identity('original sharp sextic', angular_d.substitute({'beta': betaopt}), dstar)
    c3 = v0**2/6-v0**3+v0**4
    identity('full coordinate mean conversion', angular_d,
             circle_d.substitute({'rho': (v0**2*BETA-42*c3)/v0**6}))
    # Comparable radius/energy scale, with the full changing energy retained.
    a = series(a0, 0, LAM)
    v = inverse(add(series(1), a))
    ua = inverse(add(a, exp_i(series(0, 7, 0, betaopt))))
    ub = inverse(add(a, exp_i(series(0, -1, 0, betaopt))))
    g, e, _, _, _, _ = original_profile(1, a, v, ua, ub, 'moving-radius-quadratic-angular')
    check_series('complete mixed marked-radius sixth coefficient',
                 add(corrected(g, e, a), scale(power(e, 3), -dstar)))
    # Radius comparable to sqrt(energy): independent positive-penalty control.
    a = series(a0, LAM)
    v = inverse(add(series(1), a))
    ua = boundary_reciprocal(series(0, 7, 0, RHO), a, v)
    ub = boundary_reciprocal(series(0, -1, 0, RHO), a, v)
    g, e, _, variance, _, _ = original_profile(1, a, v, ua, ub, 'moving-radius-linear-circle')
    rem = corrected(g, e, a)
    for k in range(6):
        identity('linear-radius lower cancellation '+str(k), rem[k])
    identity('linear-radius sharpness penalty', rem[6].re, 56**3*circle_d+189*d0**3*LAM**2)
    identity('linear-radius variance penalty', variance[6].re, 378*d0**2*LAM**2)
    # Nonsaturating repeated profile and unbalanced symbolic common phase.
    for r, ya, yb, label in [(4, series(0, 4), series(0, -4), 'balanced-four-four'),
                            (1, series(0, 7+RHO), series(0, -1+RHO), 'unbalanced-linear-mean')]:
        a, v = series(a0), series(v0)
        original_profile(r, a, v, boundary_reciprocal(ya, a, v), boundary_reciprocal(yb, a, v), label)
    # Independently convert the energy coefficient into the basin and means.
    shifted_kt = kt(d0+Z)
    kprime = shifted_kt.coefficient('z', 1)
    identity('marked-radius derivative', kprime, F(5953701, 7340032))
    gamma = dstar/cstar**3-kprime/(d0*cstar**2)
    identity('second universal basin coefficient', gamma, F(2965647537471488, 20111391661725))
    identity('fixed-level first correction radius term', kprime/d0, F(5953701, 11927552))
    improvement = (angular_d.coefficient('beta', 0)-dstar)/cstar**3
    identity('nonlinear phase crossing improvement', improvement, F(2199023255552, 663012911925))
    reciprocal_mean = -3*cmean.substitute({'v': v0})/(2*alpha0)
    identity('necessary reciprocal mean', reciprocal_mean, F(14703, 8192))
    original_mean = -d0**2*reciprocal_mean-3*c3*d0**8
    identity('necessary original phase mean', original_mean, F(-28561, 32768))
    digest = sha256(json.dumps(RECORDS, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    radius_penalty = F(189)*d0**3/F(56)**3
    return {'agent': 'six-reviewer-3', 'role': 'independent mathematical reviewer',
            'method': 'global scalar characteristic quartic residues; implicit original translated critical roots through degree six',
            'arithmetic': 'exact multivariate rational Laurent/Gaussian series, t truncated through six',
            'variables': list(NAMES), 'checks': len(LABELS), 'original_profiles': 6,
            'global_quartic_mean_c_in_v': cmean.univariate_v(),
            'circle_D_polynomial_in_rho': parameter_coefficients(circle_d, 'rho'),
            'angular_D_polynomial_in_beta': parameter_coefficients(angular_d, 'beta'),
            'Dstar': constant_fraction(dstar), 'Gamma': constant_fraction(gamma), 'alpha0': constant_fraction(alpha0),
            'S0': constant_fraction(s0), 'rho_opt': constant_fraction(rhoopt), 'beta_opt': constant_fraction(betaopt),
            'cutoff_quartic_mean_coefficient': constant_fraction(cmean.substitute({'v': v0})),
            'Ktrace_prime_at_cutoff': constant_fraction(kprime),
            'phase_crossing_improvement': constant_fraction(improvement),
            'fixed_level_radius_term': constant_fraction(kprime/d0),
            'necessary_reciprocal_mean_factor_before_sqrt14': constant_fraction(reciprocal_mean),
            'necessary_original_mean_factor_before_sqrt14': constant_fraction(original_mean),
            'radius_sqrt_energy_penalty': [radius_penalty.numerator, radius_penalty.denominator],
            'records_sha256': digest,
            'ordinary_written_obligations': ['uniform contour/Taylor estimates and variance absorption',
                'all-disk monotonicity and invariant-space completeness', 'classical moment inequality and equality set',
                'joint minimizing sequences, basin sandwich and strengthened sharpness geometry']}


def main():
    demand(len(sys.argv) == 1, 'Usage: python3 -I -B independent_check.py')
    output = derive()
    fixture = Path(__file__).with_name('expected.json')
    demand(fixture.is_file(), 'required expected.json fixture is missing')
    demand(output == json.loads(fixture.read_text()), 'complete expected fixture mismatch')
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
