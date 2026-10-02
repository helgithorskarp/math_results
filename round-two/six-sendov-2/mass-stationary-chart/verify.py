#!/usr/bin/env python3
"""Exact polynomial stationary chart, author six-sendov-2, researcher.

Standard-library Fraction only. Small arithmetic kernels adapt this
author's9271/9353/9398/9440; not an independent peer review.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json

def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    """Sparse rational polynomial in sixteen independent variables."""
    zero = (0,)*16

    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(v) for k, v in value.items() if v}
            require(all(len(k) == 16 for k in self.c), 'polynomial variable count')
        else:
            self.c = {self.zero: F(value)} if value else {}

    def __add__(self, other):
        out = dict(self.c)
        for k, v in P(other).c.items():
            out[k] = out.get(k, F(0))+v
            if not out[k]:
                del out[k]
        return P(out)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.c.items()})

    def __sub__(self, other):
        return self+-P(other)

    def __rsub__(self, other):
        return P(other)+-self

    def __mul__(self, other):
        out = {}
        for k, a in self.c.items():
            for l, b in P(other).c.items():
                key = tuple(i+j for i, j in zip(k, l))
                out[key] = out.get(key, F(0))+a*b
        return P(out)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(isinstance(exponent, int) and exponent >= 0, 'bad power')
        out = P(1)
        for _ in range(exponent):
            out = out*self
        return out

    def __eq__(self, other):
        return self.c == P(other).c

    def encoded(self):
        return [[list(k), str(v)] for k, v in sorted(self.c.items())]


def variable(index):
    key = [0]*16
    key[index] = 1
    return P({tuple(key): 1})


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')).encode()


class Dual:
    def __init__(self, value=0, derivative=0):
        if isinstance(value, Dual):
            self.value, self.derivative = value.value, value.derivative
        else:
            self.value, self.derivative = F(value), F(derivative)

    def __add__(self, other):
        other = Dual(other)
        return Dual(self.value+other.value, self.derivative+other.derivative)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.value, -self.derivative)

    def __sub__(self, other):
        return self+-Dual(other)

    def __rsub__(self, other):
        return Dual(other)+-self

    def __mul__(self, other):
        other = Dual(other)
        return Dual(self.value*other.value,
                    self.derivative*other.value+self.value*other.derivative)

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = Dual(other)
        require(other.value != 0, 'dual nonunit division')
        return Dual(self.value/other.value,
                    (self.derivative*other.value-self.value*other.derivative)/other.value**2)

    def __rtruediv__(self, other):
        return Dual(other)/self


def matmul(left, right):
    return [[sum((left[i][k]*right[k][j] for k in range(len(right))), Dual())
             for j in range(len(right[0]))] for i in range(len(left))]


def mateval(coefficients, x):
    n = len(x)
    out = [[Dual() for _ in range(n)] for _ in range(n)]
    for coefficient in reversed(coefficients):
        out = matmul(out, x)
        for i in range(n):
            out[i][i] += coefficient
    return out


def matinv(matrix):
    n = len(matrix)
    a = [[Dual(x) for x in row]+[Dual(int(i == j)) for j in range(n)]
         for i, row in enumerate(matrix)]
    for j in range(n):
        pivot = next((i for i in range(j, n) if a[i][j].value != 0), None)
        require(pivot is not None, 'squarefree critical sample')
        a[j], a[pivot] = a[pivot], a[j]
        divisor = a[j][j]
        a[j] = [x/divisor for x in a[j]]
        for i in range(n):
            if i == j:
                continue
            factor = a[i][j]
            a[i] = [x-factor*y for x, y in zip(a[i], a[j])]
    return [row[n:] for row in a]


def trim(poly):
    out = [F(x) for x in poly]
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def add(left, right):
    return trim([(left[i] if i < len(left) else 0)+(right[i] if i < len(right) else 0)
                 for i in range(max(len(left), len(right)))])


def scale(value, poly):
    return trim([value*x for x in poly])


def mul(left, right):
    out = [F(0)]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i+j] += a*b
    return trim(out)


def divide(left, right):
    left, right = trim(left), trim(right)
    require(right != [F(0)], 'zero polynomial divisor')
    out = [F(0)]*max(1, len(left)-len(right)+1)
    while left != [F(0)] and len(left) >= len(right):
        k, a = len(left)-len(right), left[-1]/right[-1]
        out[k] += a
        left = add(left, [F(0)]*k+scale(-a, right))
    return trim(out), left


def inverse(poly, modulus):
    r0, r1, s0, s1 = trim(modulus), trim(poly), [F(0)], [F(1)]
    while r1 != [F(0)]:
        q, rem = divide(r0, r1)
        r0, r1, s0, s1 = r1, rem, s1, add(s0, scale(-1, mul(q, s1)))
    require(len(r0) == 1 and r0[0] != 0, 'squarefree quotient control')
    result = divide(scale(1/r0[0], s0), modulus)[1]
    require(divide(mul(poly, result), modulus)[1] == [F(1)], 'Euclid inverse control')
    return result


def derivative(poly):
    return trim([i*poly[i] for i in range(1, len(poly))] or [F(0)])


def ut(poly):
    out = list(poly)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out or [0]


def ua(left, right):
    return ut([(left[i] if i < len(left) else 0)+(right[i] if i < len(right) else 0)
               for i in range(max(len(left), len(right)))])


def us(value, poly):
    return ut([value*x for x in poly])


def um(left, right):
    out = [0]*(len(left)+len(right)-1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            out[i+j] = out[i+j]+a*b
    return ut(out)


def ud(poly):
    return ut([i*poly[i] for i in range(1, len(poly))] or [0])


def uq(poly, h):
    require(len(h) == 8 and h[-1] == 1, 'monic degree-seven quotient')
    poly = ut(poly)
    q = [0]*max(1, len(poly)-7)
    while len(poly) >= 8:
        k, a = len(poly)-8, poly[-1]
        q[k] = q[k]+a
        poly = ua(poly, [0]*k+us(-a, h))
    return ut(q), ut(poly)


def ur(poly, h):
    return uq(poly, h)[1]


def nth(poly, k):
    return poly[k] if k < len(poly) else 0


def moment_list(h, last=12):
    out = [F(7)]
    for k in range(1, last+1):
        if k <= 7:
            value = -sum((nth(h, 7-i)*out[k-i] for i in range(1, k)), 0)
            value -= k*nth(h, 7-k)
        else:
            value = -sum((nth(h, 7-i)*out[k-i] for i in range(1, 8)), 0)
        out.append(value)
    return out


def adj(poly, h, moments=None, damage=None):
    """Adjoint to derivative of the UNIQUE normal representative, not a derivation."""
    poly = ur(poly, h)
    moments = moments or moment_list(h, 6)
    out = [0]*6
    for k in range(1, len(poly)):
        for j in range(k):
            out[k-1-j] = out[k-1-j]+poly[k]*moments[j]
        if damage != 'adjoint_boundary':
            out[k-1] = out[k-1]-k*poly[k]
    return ut(out)


def pairing(poly, h):
    return nth(ur(poly, h), 6)


def primitive(h, constant=0):
    return [constant]+[F(8, i+1)*h[i] for i in range(8)]


def algebra(p, h, f=None, damage=None):
    f = primitive(h) if f is None else f
    Q, residual = uq(ua(us(8, f), um(p, ud(h))), h)
    if damage == 'quotient_constant':
        Q = ua(Q, [0, -8])
    ode = ua(um(p, ud(ud(h))), um(ua(ud(p), us(-1, Q)), ud(h)))
    ode = ua(ode, um(ua([64], us(-1, ud(Q))), h))
    moments = moment_list(h, 6)
    p2 = ur(um(p, p), h)
    W = ur(um(p, ua(Q, us(-1, ud(p)))), h)
    K = ua(us(-16, p), us(F(-1, 4), adj(adj(p2, h, moments, damage), h, moments, damage)))
    K = ua(K, us(F(1, 4), adj(W, h, moments, damage)))
    return {'Q': Q, 'residual': residual, 'ODE': ode, 'K': K, 'p2': p2, 'W': W}


def polydigest(poly):
    coeff = [P(x).encoded() for x in ut(poly)]
    return {'degree': len(ut(poly))-1,
            'coefficient_terms': [len(P(x).c) for x in ut(poly)],
            'sha256': hashlib.sha256(canonical(coeff)).hexdigest()}


def universal_certificates(damage=None):
    A, B, E, F0, G, J = [variable(i) for i in range(6)]
    h = [J, G, F0, E, B, A, 0, 1]
    moments = moment_list(h, 6)
    count = 0
    for i in range(7):
        p = [0]*i+[P(1)]
        for j in range(7):
            q = [0]*j+[P(1)]
            left = pairing(um(p, ud(q)), h)
            right = pairing(um(adj(p, h, moments, damage), q), h)
            require(left == right, 'universal residue-adjoint basis identity')
            count += 1
    pc = [variable(i+6) for i in range(7)]
    a6 = algebra(pc, h, damage=damage)
    expected6 = -16*pc[6] if damage != 'drop_center' else P(0)
    require(nth(a6['K'], 6) == expected6, 'universal constant-centering coefficient')
    a5 = algebra(pc[:6], h, damage=damage)
    # P deliberately has no division; all coefficient division is rational scaling.
    expected5 = F(1, 4)*(7*pc[2]*pc[5]+7*pc[3]*pc[4]-9*A*pc[4]*pc[5]
                         -5*B*pc[5]**2-56*pc[5])
    require(nth(a5['K'], 5) == expected5, 'universal leading odd stationary identity')
    a4 = algebra(pc[:5], h)
    require(nth(a4['K'], 5) == F(7, 4)*pc[3]*pc[4], 'quartic top coefficient')
    a3 = algebra(pc[:4], h)
    require(nth(a3['K'], 4) == F(3, 2)*pc[3]**2, 'cubic degree-drop obstruction')
    quartic = [pc[0], pc[1], pc[2], P(0), pc[4]]
    a40 = algebra(quartic, h)
    require(nth(a40['K'], 4) == pc[4]*(3*pc[2]-2*A*pc[4]-12), 'quartic next leading condition')
    require(nth(a40['K'], 3) == F(3, 4)*pc[4]*(5*pc[1]-4*B*pc[4]), 'quartic odd condition')
    t, p0 = pc[4], pc[0]
    branch = [p0, F(4, 5)*B*t, 4+F(2, 3)*A*t, P(0), t]
    ab = algebra(branch, h)
    require(nth(ab['K'], 5) == nth(ab['K'], 4) == nth(ab['K'], 3) == 0,
            'all quartic branch leading conditions')
    k2 = F(-1, 9)*t*(-2*A*A*t+24*A+27*p0)
    k1 = F(1, 20)*t*(5*A*B*t-36*B+25*F0*t)
    o5 = 2*(2*A*A*t-16*A-12*E*t+21*p0)
    o4 = 7*A*B*t-36*B-25*F0*t
    o2 = F(1, 5)*(-20*A*F0*t-3*B*E*t+60*B*p0-100*F0-105*J*t)
    require(nth(ab['K'], 2) == k2 and nth(ab['K'], 1) == k1, 'quartic lower kernel coefficients')
    require(nth(ab['ODE'], 5) == o5 and nth(ab['ODE'], 4) == o4 and nth(ab['ODE'], 2) == o2,
            'quartic complete selected ODE coefficients')
    require(k1+F(1, 20)*t*o4 == F(3, 5)*t*B*(A*t-6), 'quartic exceptional split')
    aq = algebra(pc[:3], h)
    require(nth(aq['K'], 2) == 2*pc[2]*(pc[2]-4), 'quadratic angular value')
    require(nth(aq['K'], 1) == F(3, 4)*pc[1]*(5*pc[2]-8), 'quadratic odd equation')
    pe = [pc[0], P(0), pc[2]]
    ae = algebra(pe, h)
    require(nth(ae['ODE'], 4) == -3*(5*pc[2]-8)*B, 'quadratic first parity resonance')
    h_no_B = [J, G, F0, E, 0, A, 0, 1]
    ae2 = algebra(pe, h_no_B)
    require(nth(ae2['ODE'], 2) == -5*(3*pc[2]-8)*F0, 'quadratic second parity resonance')
    h_odd_constant = [J, G, 0, E, 0, A, 0, 1]
    ae0 = algebra(pe, h_odd_constant)
    require(nth(ae0['ODE'], 0) == -7*(pc[2]-8)*J, 'quadratic constant parity resonance')
    c = pc[0]
    g = us(7, um(um([c*F(1, 8), 0, 1], [c*F(1, 8), 0, 1]), [c*F(1, 8), 0, 1]))
    if damage == 'resonance_power':
        g = us(7, um([c*F(1, 8), 0, 1], [c*F(1, 8), 0, 1]))
    require(ua(um([c, 0, 8], ud(g)), us(-48, [0]+g)) == [0] and nth(g, 6) == 7,
            'exceptional quadratic derivative cube')
    selected = {'top_odd_relation': [expected5], 'quartic_K2': [k2], 'quartic_K1': [k1],
                'quartic_ODE5': [o5], 'quartic_ODE4': [o4], 'quartic_ODE2': [o2],
                'resonance_derivative': g}
    return {'residue_adjoint_universal_basis_pairs': count,
            'general_mass_kernel': polydigest(a6['K']),
            'degree_five_mass_kernel': polydigest(a5['K']),
            'selected_entire_polynomials': {k: polydigest(v) for k, v in selected.items()},
            'identity_count_beyond_basis': 22}


def dual_trace_eta(f, q, damage=None):
    fd = [Dual(x, nth(q, i)) for i, x in enumerate(f)]
    h = [F(i, 8)*fd[i] for i in range(1, 9)]
    hp = [i*h[i] for i in range(1, 8)]
    x = [[Dual() for _ in range(7)] for _ in range(7)]
    for i in range(7):
        x[i][-1] = -h[i]
        if i:
            x[i][i-1] += 1
    if damage == 'freeze_nodes':
        x = [[Dual(a.value) for a in row] for row in x]
    m = matmul(mateval(fd, x), matinv(mateval(hp, x)))
    m = [[-8*a for a in row] for row in m]
    square = matmul(m, m)
    return sum((square[i][i] for i in range(7)), Dual())


def trace(poly, h):
    poly = ur(poly, h)
    moments = moment_list(h, len(poly)-1)
    return sum((a*moments[i] for i, a in enumerate(poly)), F(0))


def data(f):
    f = [F(x) for x in f]
    require(len(f) == 9 and f[-1] == 1 and f[-2] == 0, 'balanced monic octic')
    h = scale(F(1, 8), derivative(f))
    inv = inverse(derivative(h), h)
    p = ur(us(-8, um(f, inv)), h)
    a = algebra(p, h, f)
    require(a['residual'] == [0] and a['ODE'] == [0], 'exact mass relation and ODE')
    N = -2*f[6]
    D = F(3, 8)*N*N-4*f[4]
    eta = trace(um(p, p), h)
    require(trace(p, h) == N, 'exact total mass identity')
    return {'f': f, 'h': h, 'p': p, 'N': N, 'D': D, 'eta': eta, **a}


def root_poly(originals):
    out = [F(1)]
    for u in originals:
        out = mul(out, [-F(u), F(1)])
    return out


def sturm_count(poly):
    seq = [trim(poly), derivative(poly)]
    while seq[-1] != [F(0)]:
        rem = divide(seq[-2], seq[-1])[1]
        if rem == [F(0)]:
            break
        seq.append(scale(-1, rem))
    def variation(positive):
        signs = []
        for p in seq:
            sign = 1 if p[-1] > 0 else -1
            if not positive and (len(p)-1)%2:
                sign = -sign
            signs.append(sign)
        return sum(a != b for a, b in zip(signs, signs[1:]))
    return variation(False)-variation(True)


def differential_controls(damage=None):
    f1 = root_poly([-4, -3, -2, -1, 1, 2, 3, 4])
    f2 = root_poly([-7, -5, -3, -1, 2, 3, 4, 7])
    f3 = root_poly([-5, -3, -2, -1, 0, 1, 4, 6])
    hermite = [F(x) for x in [105, 0, -420, 0, 210, 0, -28, 0, 1]]
    a = data(f2);kappa = us(-8, inverse(derivative(a['h']), a['h']))
    shift = -trace(um(a['p'], kappa), a['h'])/trace(um(kappa, kappa), a['h'])
    centered = list(f2);centered[0] += shift
    cases = [('symmetric_integer', f1), ('asymmetric_integer', f2),
             ('asymmetric_zero_original', f3), ('Hermite_low_degree', hermite),
             ('asymmetric_centered', centered)]
    records = []
    for name, f in cases:
        a = data(f);K,h=a['K'],a['h'];values=[]
        for k in range(7):
            q = [F(0)]*k+[F(1)]
            actual = dual_trace_eta(f, q, damage)
            expected = pairing(um(K, q), h)
            require(actual.value == a['eta'], 'independent dual-matrix eta value')
            require(actual.derivative == expected, 'independent full moving-node adjoint gradient')
            values.append(str(expected))
        radial = [F(k-8)*f[k] for k in range(7)]
        require(pairing(um(K, radial), h) == -4*a['eta'], 'full radial Euler identity')
        require(sturm_count(h) == 7, 'seven real simple critical control')
        C = (a['N']**2-a['eta'])/a['D']
        target = [-4*a['N'], 0, 4*C]
        require(ua(K, us(-1, target)) != [0], 'controls are not fully stationary')
        if name == 'Hermite_low_degree':
            require(a['p'] == [F(8)] and K == [F(-32)] and C == 8,
                    'literal Hermite degree-zero nonstationary control')
        if name == 'asymmetric_centered':
            require(nth(a['p'], 6) == 0 and nth(a['p'], 5) != 0,
                    'actual asymmetric degree-five constant center')
        records.append({'name': name, 'f': [str(x) for x in f],
                        'mass_interpolant': [str(x) for x in a['p']],
                        'quotient_Q': [str(x) for x in a['Q']],
                        'kernel_K': [str(x) for x in K],
                        'N': str(a['N']), 'D': str(a['D']), 'eta': str(a['eta']), 'C': str(C),
                        'all_seven_derivatives': values, 'real_distinct_original_count': sturm_count(f)})
    return records


def scalar_and_domain_controls(damage=None):
    # Exceptional quartic branch, normalized N1.
    d = F(1, 8);p0 = F(8, 7)*d-F(1, 2)
    gamma = 12*p0-2 if damage != 'quartic_exception' else 12*p0+2
    require(gamma == F(96, 7)*d-8, 'exceptional quartic value relation')
    require(F(96, 7)*F(7, 8)-8 == 4, 'exceptional strict variance endpoint')
    negative = {str(r): str(r*(r-4)/2) for r in [F(8, 5), F(8, 3)]}
    require(all(F(v) < 0 for v in negative.values()), 'excluded negative quadratic resonance values')
    require(all(8*(k-6) != 0 for k in range(6)), 'unique degree-six derivative-cube recurrence')
    f = root_poly([-4, -3, -2, -1, 1, 2, 3, 4]);bad = list(f);bad[0] -= 1000
    a = data(bad)
    central = nth(a['p'], 0)
    if damage == 'negative_mass':
        central = -central
    require(sturm_count(a['h']) == 7 and sturm_count(bad) < 8 and central < 0,
            'real criticals alone do not imply original feasibility')
    collision = root_poly([-3, -3, -1, 1, 3, 3, -2, 2]);ac = data(collision)
    count = sturm_count(collision)
    if damage == 'collision_scope':
        count = 8
    require(sturm_count(ac['h']) == 7 and count < 8,
            'simple criticals do not authorize all-distinct stationary chart')
    # A positive polynomial on a real critical spectrum need not satisfy the required ODE.
    formal = algebra([F(1)], scale(F(1, 8), derivative(f)))
    require(formal['ODE'] != [0], 'mass positivity without the ODE is insufficient')
    return {'quartic_exception_test_d': str(d), 'quartic_exception_gamma': str(gamma),
            'strict_variance_endpoint': '7/8', 'negative_quadratic_resonances': negative,
            'six_recurrence_pivots': [8*(k-6) for k in range(6)],
            'negative_mass_primitive': {'critical_count': 7, 'original_count': sturm_count(bad),
                                       'central_mass': str(central)},
            'collision_chart_rejection': {'critical_count': 7, 'distinct_original_count': count},
            'positive_fake_mass_has_nonzero_ODE': True}


def build_record():
    return {'actual_agent': 'six-sendov-2', 'role': 'researcher',
            'scope': 'all eight-distinct real balanced angular stationary profiles; no high-value assumption',
            'universal': universal_certificates(),
            'differential_controls': differential_controls(),
            'scalar_and_domain_controls': scalar_and_domain_controls(),
            'degree_drop_proof_status': 'ordinary universal argument using credited9323 C>4 and9398 no-even stationarity',
            'degree_exactly_five': True,
            'feasibility_conditions': ['seven simple real h roots', 'strict positive p at every h root',
                                       'full polynomial ODE', 'full kernel quadratic identity'],
            'global_Cstar_c3_proved': False, 'complex_first_power_proved': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    record = build_record();damages=[]
    for name, function in [('adjoint_boundary', universal_certificates),
                           ('drop_center', universal_certificates),
                           ('quotient_constant', universal_certificates),
                           ('resonance_power', universal_certificates),
                           ('freeze_nodes', differential_controls),
                           ('quartic_exception', scalar_and_domain_controls),
                           ('negative_mass', scalar_and_domain_controls),
                           ('collision_scope', scalar_and_domain_controls)]:
        try:
            function(name)
        except ValueError as error:
            damages.append({'damage': name, 'rejection': str(error)})
        else:
            raise ValueError('unchecked mathematical damage: '+name)
    record['rejected_mathematical_damages'] = damages
    if args.emit:
        args.expected.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    require(json.loads(args.expected.read_text()) == record, 'whole expected record mismatch')
    print(json.dumps({'status': 'PASS', 'record_sha256': hashlib.sha256(canonical(record)).hexdigest(),
                      'universal_residue_adjoint_pairs': 49,
                      'universal_degree_and_ODE_identities': 22,
                      'independent_dual_differentials': 35, 'mathematical_damages': len(damages)}))


if __name__ == '__main__':
    main()
