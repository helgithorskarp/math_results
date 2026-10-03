#!/usr/bin/env python3
"""Exact unscaled mass-degree-drop certificate. Actual six-sendov-2, researcher.

CPython 3.10+ standard library. Sparse Fraction arithmetic and rho/T/ODE/kernel
construction adapt this author's credited mass-stationary-chart source. This
is an author check, not independent review or formalization. No root finding,
solver, old fixture, peer executable, localization, or external input is needed.
Universal root-box and analytic implication proofs are in PROOF.md.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import hashlib
def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    """Entire sparse polynomial in QQ[B,E,F,G,J,p0,p1,p2,p3,p4,p5,C]."""
    zero = (0,)*12

    def __init__(self, value=0):
        if isinstance(value, P):
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {tuple(k): F(v) for k, v in value.items() if v}
            require(all(len(k) == 12 and all(type(x) is int and x >= 0 for x in k)
                        for k in self.c), 'polynomial ring QQ, nonnegative exponents')
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
    key = [0]*12
    key[index] = 1
    return P({tuple(key): 1})


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
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


def substitute(q, values):
    out = P(0)
    for powers, coefficient in P(q).c.items():
        term = P(coefficient)
        for i, k in enumerate(powers):
            term = term * P(values.get(i, variable(i)))**k
        out += term
    return out


def degree(q):
    return max([sum(k) for k in P(q).c] or [0])


def norm(q):
    return sum((abs(c) for c in P(q).c.values()), F(0))


def gradient_norm(q):
    return sum((sum(k)*abs(c) for k, c in P(q).c.items()), F(0))


def encoded(poly):
    return [P(q).encoded() for q in poly]


def compute(damage=None):
    B, E, F0, G, J = [variable(i) for i in range(5)]
    p = [variable(i+5) for i in range(6)]
    C = variable(11)
    A = F(-3, 8)
    h = [J, G, F0, E, B, A, 0, 1]
    identities = []

    def identity(left, right, name):
        require(left == right, 'whole identity: '+name)
        identities.append(name)

    def phi(mass, heptic=h):
        data = algebra(mass, heptic, damage=damage)
        require(len(data['ODE']) <= 6, 'all higher full ODE rows vanish')
        return data['ODE']+[nth(data['K'], k)
                           -(4*C if k == 2 else -4 if k == 0 else 0)
                           for k in range(7)]

    full = algebra(p, h, damage=damage)
    q_expected = [7*p[1]-2*A*p[3]-3*B*p[4]+(2*A*A-4*E)*p[5],
                  8+7*p[2]-2*A*p[4]-3*B*p[5],
                  7*p[3]-2*A*p[5], 7*p[4], 7*p[5]]
    require(full['Q'] == q_expected, 'whole quotient Q, including constant')
    identities.append('entire quotient Q')
    rows = phi(p)
    require(len(rows) == 13, 'complete canonical residual row count')
    require(max(map(degree, rows)) == 4, 'entire residual degree')
    require(max(map(gradient_norm, rows)) <= 10000, 'full gradient norm budget')

    quartic = algebra(p[:5], h, damage=damage)
    identity(nth(quartic['K'], 5), F(7, 4)*p[3]*p[4], 'quartic leading odd row')
    cubic = algebra(p[:4], h, damage=damage)
    identity(nth(cubic['K'], 4), F(3, 2)*p[3]**2, 'cubic positive square row')
    even_quartic = [p[0], p[1], p[2], P(0), p[4]]
    eq = algebra(even_quartic, h, damage=damage)
    identity(nth(eq['K'], 4), p[4]*(3*p[2]-2*A*p[4]-12), 'quartic quadratic pivot')
    identity(nth(eq['K'], 3), F(3, 4)*p[4]*(5*p[1]-4*B*p[4]), 'quartic linear pivot')
    t = p[4]
    branch = [p[0], F(4, 5)*B*t, 4+F(2, 3)*A*t, P(0), t]
    branch_data = algebra(branch, h, damage=damage)
    branch_rows = phi(branch)
    require(max(map(degree, branch_rows)) <= 4, 'full quartic branch degree')
    require(max(map(gradient_norm, branch_rows)) <= 10000, 'whole branch gradient budget')
    k2 = F(-1, 9)*t*(-2*A*A*t+24*A+27*p[0])
    k1 = F(1, 20)*t*(5*A*B*t-36*B+25*F0*t)
    o5 = 2*(2*A*A*t-16*A-12*E*t+21*p[0])
    o4 = 7*A*B*t-36*B-25*F0*t
    o2 = F(1, 5)*(-20*A*F0*t-3*B*E*t+60*B*p[0]-100*F0-105*J*t)
    for k, target in [(5, o5), (4, o4), (2, o2)]:
        identity(nth(branch_data['ODE'], k), target, 'quartic full ODE row '+str(k))
    for k, target in [(2, k2), (1, k1)]:
        identity(nth(branch_data['K'], k), target, 'quartic full kernel row '+str(k))
    identity(k1+F(1, 20)*t*o4, F(3, 5)*t*B*(A*t-6), 'undivided exceptional split')
    D = F(3, 8)-8*E
    p0_star = F(8, 7)*D-F(1, 2)
    identity(substitute(o5, {9: -16}), 42*(p[0]-p0_star), 'exceptional actual D pivot')
    identity(substitute(k2, {9: -16}), 48*p[0]-8, 'exceptional actual C pivot')
    wrong = 2 if damage == 'exceptional_constant' else -2
    identity(12*p0_star+wrong, F(96, 7)*D-8, 'exceptional scalar angular value')

    quad = algebra(p[:3], h, damage=damage)
    identity(nth(quad['K'], 2), 2*p[2]*(p[2]-4), 'quadratic angular value')
    identity(nth(quad['K'], 1), F(3, 4)*p[1]*(5*p[2]-8), 'quadratic odd pivot')
    even_quad = [p[0], P(0), p[2]]
    aq = algebra(even_quad, h, damage=damage)
    identity(nth(aq['ODE'], 4), -3*(5*p[2]-8)*B, 'quadratic first parity pivot')
    hB = [J, G, F0, E, P(0), A, 0, 1]
    aB = algebra(even_quad, hB, damage=damage)
    identity(nth(aB['ODE'], 2), -5*(3*p[2]-8)*F0, 'quadratic second parity pivot')
    hBF = [J, G, P(0), E, P(0), A, 0, 1]
    aBF = algebra(even_quad, hBF, damage=damage)
    identity(nth(aBF['ODE'], 0), -7*(p[2]-8)*J, 'quadratic final parity pivot')

    # Whole resonance cube and the triangular inverse, including p0=0.
    cube_base = [p[0]*F(1, 8), P(0), P(1)]
    cube_power = 2 if damage == 'resonance_degree' else 3
    cube = [P(1)]
    for _ in range(cube_power):
        cube = um(cube, cube_base)
    require(len(cube) == 7 and cube[-1] == 1, 'resonance cube is monic sextic')
    require(ua(um([p[0], 0, 8], ud(cube)), us(-48, [0]+cube)) == [0],
            'whole resonance ODE')
    identities.append('whole monic sextic resonance ODE')
    jet = [variable(i) for i in range(5)]+[variable(6), P(1)]
    residual = ua(um([p[0], 0, 8], ud(jet)), us(-48, [0]+jet))
    recovered = [P(0)]*7
    for k in range(5, -1, -1):
        recovered[k] = F(1, 8*(k-6))*(nth(residual, k+1)
                          -p[0]*(k+2)*nth(recovered, k+2))
    require(all(recovered[k] == jet[k]-cube[k] for k in range(6)),
            'entire triangular inverse of resonance, all six coefficients')
    identities.append('all six resonance inverse coefficients')

    # Universal monomial bounds: 0<e<=M^-50, M>=100. Each compared
    # expression is a sum of positive monomials coefficient*e^a*M^b.
    budgets = []

    def budget(name, terms, target):
        c0, a0, b0 = target
        upper = F(0)
        ratio_terms = []
        for c, a, b in terms:
            da, db = a-a0, b-b0
            require(da >= 0 and db-50*da <= 0, 'unsupported monomial bound '+name)
            coefficient, power = F(c)/F(c0), db-50*da
            upper += coefficient*F(100)**power
            ratio_terms.append([str(coefficient), power])
        require(upper <= 1, 'exact budget inequality '+name)
        budgets.append({'name': name,
                        'left': [[str(c), a, b] for c, a, b in terms],
                        'right': [str(c0), a0, b0],
                        'ratios_at_closed_boundary': ratio_terms,
                        'proved_leq': True})

    R = (1, 0, 0) if damage == 'budget_residual' else (1, 22, -200)
    budget('small quartic to cubic square', [(F(2, 3), R[1], R[2]), (F(2, 3), 4, -24)], (1, 4, -22))
    budget('quadratic projection residual', [R, (1, 4, -24), (1, 2, -3)], (1, 2, -2))
    budget('quadratic p1 projection', [(1, 2, -2), (F(4, 3), 2, 6)], (1, 2, 7))
    budget('quadratic B projection', [(1, 2, 7), (F(1, 3), 2, 15)], (1, 2, 16))
    budget('quadratic F projection', [(1, 2, 16), (F(1, 5), 2, 24)], (1, 2, 25))
    budget('quadratic B odd floor contradiction', [(F(1, 3), 2, 7)], (1, 1, 0))
    budget('quadratic F odd floor contradiction', [(F(1, 5), 2, 16)], (1, 1, 0))
    budget('quadratic J odd floor contradiction', [(F(1, 7), 1, -3)], (1, 1, 0))
    budget('quadratic final resonance residual', [(1, 2, 7), (1, 1, 36)], (1, 1, 37))
    budget('resonance inverse norm', [(F(21, 8), 0, 5)], (1, 0, 7))
    budget('quartic p3 projection', [R, (1, 18, -160)], (1, 18, -159))
    budget('quartic p1+p2 projection distance', [(F(1, 3)+F(4, 15), 14, -127)], (1, 14, -126))
    budget('complete quartic projected residual', [(1, 18, -159), (1, 14, -118)], (1, 14, -117))
    budget('quartic split without factor division', [(F(5, 3), 0, 0), (F(1, 12), 0, 1)], (1, 0, 1))
    budget('quartic F estimate', [(F(1, 25), 5, -50), (F(1, 25), 10, -85)], (1, 5, -49))
    budget('quartic J estimate', [(F(1, 21), 1, -15), (F(1, 21), 5, -50), (F(1, 21), 10, -85)], (1, 1, -14))
    budget('quartic B odd floor contradiction', [(1, 9, -84)], (1, 1, 0))
    budget('quartic F odd floor contradiction', [(1, 5, -49)], (1, 1, 0))
    budget('quartic J odd floor contradiction', [(1, 1, -14)], (1, 1, 0))
    budget('quartic exceptional projection residual', [(1, 14, -117), (3, 1, 8)], (1, 1, 9))
    budget('quartic exceptional C error <1', [(F(15, 28), 1, 9)], (F(1, 2), 0, 0))
    budget('quadratic split alpha <=1', [(1, 1, 28)], (1, 0, 0))
    budget('quadratic value residual <=1', [(1, 2, -2)], (1, 0, 0))
    # The whole convex quadratic has its minimum at 2; on each stated
    # resonance interval its maximum is the indicated outer endpoint.
    scalar = {
        'heat_B_floor': F(3)*6/F(3, 2),
        'eta_floor': F(1, 7),
        'C_floor': F(29, 7),
        'D_ceiling': F(6, 29),
        'exceptional_C_ceiling': F(96, 7)*F(6, 29)-8,
        'first_resonance_quadratic_max': F(7, 5)*(F(7, 5)-4)/2,
        'second_resonance_quadratic_max': F(3)*(F(3)-4)/2,
        'sextic_box_floor': F(1, 4)*F(3, 4)**5*12,
        'sextic_perturbation_ceiling': F(5, 4)**5,
        'sextic_resonance_distance': F(729, 3125),
        'odd_heptic_floor_multiplier': F(15, 184),
        'triple_weight': F(8, 5)+F(8, 3)+8,
        'two_moment_multiplier': F(57600, 4549),
        'whole_input_max_gradient_norm': max(map(gradient_norm, rows)),
        'whole_branch_max_gradient_norm': max(map(gradient_norm, branch_rows)),
    }
    require(scalar['heat_B_floor'] == 12 and scalar['C_floor'] == 4+scalar['eta_floor'],
            'actual heat coercivity')
    require(scalar['exceptional_C_ceiling'] == F(-1048, 203), 'quartic exceptional gap')
    require(scalar['first_resonance_quadratic_max'] < 0 and scalar['second_resonance_quadratic_max'] < 0,
            'both quadratic resonance intervals have negative angular values')
    require(scalar['sextic_box_floor']/scalar['sextic_perturbation_ceiling']
            == scalar['sextic_resonance_distance'], 'all sextic endpoint constants')
    require(1/scalar['triple_weight'] == scalar['odd_heptic_floor_multiplier'], 'whole odd heptic weight')
    require(F(1, 10**60) < F(15, 184*10**56), 'new threshold strictly below actual odd floor')
    require(F(1, 10**60) < scalar['sextic_resonance_distance'], 'new resonance tolerance is strictly below sextic floor')
    # e=10^-60 delta^116 M^-50, M=100 delta^-6,
    # |p5| threshold=e^22 M^-208.
    constant_power = 60*22+2*(50*22+208)
    delta_power = 116*22+6*(50*22+208)
    require((constant_power, delta_power) == (3936, 10400), 'leading mass threshold simplification')
    moment_constant = 136+190*constant_power
    moment_delta = 190*(delta_power+6)
    require((moment_constant, moment_delta) == (747976, 1977140), 'separation-only two-moment substitution')

    # Preserve each whole difference quotient: no coefficient is sampled.
    drop_quotients = []
    for row in rows:
        dropped = substitute(row, {10: 0})
        difference = P(row)-dropped
        q = P({tuple(x-1 if i == 10 else x for i, x in enumerate(key)): c
               for key, c in difference.c.items()})
        identity(difference, p[5]*q, 'complete p5 difference quotient '+str(len(drop_quotients)))
        drop_quotients.append(q)
    return {
        'actual_agent': 'six-sendov-2', 'role': 'researcher',
        'domain': 'QQ[B,E,F,G,J,p0,p1,p2,p3,p4,p5,C], A=-3/8; no localization',
        'variable_order': ['B', 'E', 'F', 'G', 'J', 'p0', 'p1', 'p2', 'p3', 'p4', 'p5', 'C'],
        'whole_maps': {'Q': encoded(full['Q']), 'ODE': encoded(full['ODE']),
                       'Phi': encoded(rows), 'rho_p_squared': encoded(full['p2']),
                       'rho_p_Q_minus_pprime': encoded(full['W']),
                       'Newton_tau_0_through_6': encoded(moment_list(h, 6)),
                       'p5_difference_quotients': encoded(drop_quotients),
                       'projected_quartic_Phi': encoded(branch_rows),
                       'monic_resonance_cube': encoded(cube),
                       'resonance_inverse': encoded(recovered[:6])},
        'whole_row_degrees': [degree(q) for q in rows],
        'whole_row_gradient_norms': [str(gradient_norm(q)) for q in rows],
        'complete_residual_terms': sum(len(P(q).c) for q in rows),
        'whole_identities': identities,
        'closed_monomial_budget_domain': '0<e<=M^-50, M>=100',
        'all_exact_budget_comparisons': budgets,
        'exact_scalar_constants': {k: str(v) for k, v in scalar.items()},
        'leading_mass_floor': {'ten_negative_exponent': constant_power, 'delta_exponent': delta_power},
        'two_moment_gap': {'multiplier': str(scalar['two_moment_multiplier']),
                           'ten_negative_exponent': moment_constant, 'delta_exponent': moment_delta},
        'proof_status_at_publication': 'complete ordinary author proof; unformalized and independently unreviewed',
        'scope': 'actual separated eight-distinct real originals at angular stationarity; no stationary existence, collisions, physical H or complex first-power endpoint',
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--write-expected', type=Path)
    args = parser.parse_args()
    record = compute()
    damages = ['quotient_constant', 'adjoint_boundary', 'exceptional_constant',
               'resonance_degree', 'budget_residual']
    rejected = []
    for damage in damages:
        try:
            compute(damage)
        except ValueError:
            rejected.append(damage)
        else:
            raise ValueError('mathematical damage accepted: '+damage)
    record['mathematical_damages_rejected_without_fixture'] = rejected
    if args.write_expected:
        args.write_expected.write_bytes(canonical(record)+b'\n')
    else:
        expected = json.loads(args.expected.read_text())
        require(canonical(record) == canonical(expected), 'ENTIRE typed mathematical record differs')
    print(json.dumps({'complete': True, 'record_sha256': hashlib.sha256(canonical(record)).hexdigest(),
                      'whole_residual_rows': len(record['whole_maps']['Phi']),
                      'whole_residual_terms': record['complete_residual_terms'],
                      'whole_identities': len(record['whole_identities']),
                      'exact_closed_budget_comparisons': len(record['all_exact_budget_comparisons']),
                      'mathematical_damages_rejected': rejected,
                      'leading_mass_floor': record['leading_mass_floor'],
                      'two_moment_gap': record['two_moment_gap']}))


if __name__ == '__main__':
    main()
