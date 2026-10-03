#!/usr/bin/env python3
"""Exact coefficient/scalar certificate for quantitative stationary asymmetry.

Actual six-sendov-2, researcher. CPython 3.10+ standard library only.
Sparse Fraction arithmetic and the cubic trace construction adapt the credited
same-author even-angular-exclusion checker. This is not independent review or
formal verification. Universal root, derivative and norm arguments are in
PROOF.md. There are no assert gates, root approximations or solver assumptions.
"""
from fractions import Fraction as F
from itertools import permutations
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json


def require(condition, message):
    if not condition:
        raise ValueError(message)


class P:
    """Whole sparse rational polynomial; optional explicitly declared Laurent ring."""
    def __init__(self, value=0, n=5, laurent=False):
        self.n, self.laurent = n, laurent
        require(isinstance(n, int) and n > 0, 'invalid ring arity')
        if isinstance(value, P):
            require(value.n == n and value.laurent == laurent, 'ring mismatch')
            self.c = dict(value.c)
        elif isinstance(value, dict):
            self.c = {}
            for key, coefficient in value.items():
                require(len(key) == n and all(type(x) is int for x in key),
                        'invalid entire monomial')
                require(laurent or all(x >= 0 for x in key), 'undeclared localization')
                require(isinstance(coefficient, (int, F)), 'nonexact coefficient')
                if coefficient:
                    self.c[tuple(key)] = F(coefficient)
        else:
            require(isinstance(value, (int, F)), 'nonexact scalar')
            self.c = {(0,) * n: F(value)} if value else {}

    def cast(self, value):
        return P(value, self.n, self.laurent)

    def __add__(self, other):
        other = self.cast(other)
        out = dict(self.c)
        for key, coefficient in other.c.items():
            out[key] = out.get(key, F(0)) + coefficient
            if not out[key]:
                del out[key]
        return P(out, self.n, self.laurent)

    __radd__ = __add__

    def __neg__(self):
        return P({key: -coefficient for key, coefficient in self.c.items()},
                 self.n, self.laurent)

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        other = self.cast(other)
        out = {}
        for key, coefficient in self.c.items():
            for key2, coefficient2 in other.c.items():
                new = tuple(x+y for x, y in zip(key, key2))
                out[new] = out.get(new, F(0)) + coefficient * coefficient2
        return P(out, self.n, self.laurent)

    __rmul__ = __mul__

    def __pow__(self, exponent):
        require(type(exponent) is int and exponent >= 0, 'invalid power')
        out, base = self.cast(1), self
        while exponent:
            if exponent & 1:
                out = out * base
            base = base * base
            exponent //= 2
        return out

    def __eq__(self, other):
        return self.c == self.cast(other).c

    def diff(self, variable):
        out = {}
        for key, coefficient in self.c.items():
            if key[variable]:
                new = list(key)
                new[variable] -= 1
                out[tuple(new)] = coefficient * key[variable]
        return P(out, self.n, self.laurent)

    def at(self, values):
        require(len(values) == self.n and all(isinstance(x, (int, F)) for x in values),
                'nonexact evaluation')
        return sum((coefficient * product(F(x)**k for x, k in zip(values, key))
                    for key, coefficient in self.c.items()), F(0))

    def norm(self):
        return sum(map(abs, self.c.values()), F(0))

    def encoded(self):
        return [[list(key), str(coefficient)] for key, coefficient in sorted(self.c.items())]


def product(items):
    result = 1
    for item in items:
        result *= item
    return result


def variable(index, n=5, exponent=1, laurent=False):
    key = [0] * n
    key[index] = exponent
    return P({tuple(key): 1}, n, laurent)


def identity(left, right, name, record):
    require(left == right, 'whole identity: ' + name)
    record.append(name)


def determinant(matrix):
    size = len(matrix)
    require(all(len(row) == size for row in matrix), 'nonsquare determinant')
    out = P(0)
    for perm in permutations(range(size)):
        inversions = sum(perm[i] > perm[j] for i in range(size) for j in range(i+1, size))
        term = P((-1)**inversions)
        for i, j in enumerate(perm):
            term = term * matrix[i][j]
        out = out + term
    return out


def eye(size):
    return [[P(int(i == j)) for j in range(size)] for i in range(size)]


def scale(scalar, matrix):
    return [[scalar * x for x in row] for row in matrix]


def madd(left, right):
    require(len(left) == len(right), 'matrix addition shape')
    return [[x+y for x, y in zip(lrow, rrow)] for lrow, rrow in zip(left, right)]


def mmul(left, right):
    require(all(len(row) == len(right) for row in left), 'matrix product shape')
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), P(0))
             for j in range(len(right[0]))] for i in range(len(left))]


def mpow(matrix, exponent):
    out = eye(len(matrix))
    for _ in range(exponent):
        out = mmul(out, matrix)
    return out


def trace(matrix):
    return sum((matrix[i][i] for i in range(len(matrix))), P(0))


def cleared_b(poly, numerator, denominator, degree):
    """Full homogenized substitution; no polynomial or slope division."""
    a, b = variable(0), variable(1)
    require(all(key[1] <= degree and not any(key[2:]) for key in poly.c),
            'cleared substitution degree')
    return sum((coefficient * a**key[0] * numerator**key[1] * denominator**(degree-key[1])
                for key, coefficient in poly.c.items()), P(0))


def algebra(damage=None):
    a, b, c = (variable(i) for i in range(3))
    A, d, g = 32*a-3, 15-112*a, 208*a-15
    L = 256*a**3-18*a*a+432*a*b+864*b*b-27*b
    H = 512*a**3-36*a*a+736*a*b+1344*b*b-45*b
    U = 16*a*a-a+6*b
    W = 4096*a**4-512*a**3+7680*a*a*b+18*a*a-816*a*b+1440*b*b+27*b
    J = 8192*a**4-1024*a**3+13312*a*a*b+36*a*a-1376*a*b+2496*b*b+45*b
    V = 8192*a**4+13312*a*a*b-36*a*a+96*a*b+5184*b*b-45*b
    FF = 4*a*a+d*b
    GG = 4*a*a*(64*a-5)+g*b
    T = 27648*a*a-4960*a+225
    names = []
    cubic_A, cubic_B, cubic_C = P(F(-3, 8)), a*F(1, 2), b*F(1, 4)
    disc = (cubic_A**2*cubic_B**2-4*cubic_B**3-4*cubic_A**3*cubic_C
            -27*cubic_C**2+18*cubic_A*cubic_B*cubic_C)
    identity(disc, -L*F(1, 512), 'full cubic discriminant', names)
    identity(T, 27648*(a-F(155, 1728))**2+F(275, 108), 'positive T completion', names)
    Na = V.diff(0)*A*H-V*(32*H+A*H.diff(0))
    Nb = V.diff(1)*H-V*H.diff(1)
    identity(Nb, 768*FF*GG, 'entire b gradient numerator', names)
    n = -4*a*a
    DF = P(0)
    require(all(key[1] <= 4 and not any(key[2:]) for key in Na.c), 'Na b degree')
    for key, coefficient in Na.c.items():
        i, j = key[:2]
        DF += coefficient*a**i*sum((b**(j-1-ell)*n**ell*d**(3-ell)
                                    for ell in range(j)), P(0))
    if damage == 'last_DF_coefficient':
        last = sorted(DF.c)[-1]
        changed = dict(DF.c)
        changed[last] += 1
        DF = P(changed)
    factor = (56*a-5)**2 if damage != 'omitted_degree_loss_factor' else P(1)
    identity(d**4*Na+1075200*a**4*A**4*factor, FF*DF,
             'undivided complete F lift', names)
    HF = cleared_b(H, n, d, 2)
    identity(HF, 8*a*a*A*(56*a-5)*(448*a-45), 'whole H on F branch', names)
    VF = cleared_b(V, n, d, 2)
    identity(VF*(448*a-45), (224*a+15)*A*HF, 'credited centered F branch', names)
    g0 = 4*a*a*(64*a-5)
    WG = -GG*F(27, 16)+g0*F(27, 8)-g*(432*a-27)*F(1, 512)
    if damage == 'G_lift_constant':
        WG += 1
    identity(g*g*disc+a*a*A*A*T*F(1, 256), GG*WG,
             'undivided G discriminant lift including g zero', names)

    # Cubic companion trace, including both members of every nonzero critical pair.
    X = [[P(0), P(0), -b*F(1, 4)],
         [P(1), P(0), -a*F(1, 2)],
         [P(0), P(1), P(F(3, 8))]]
    Z = madd(madd(scale(3, mpow(X, 3)), scale(F(-3, 4), mpow(X, 2))),
             scale(a*F(1, 2), X))
    DZ = determinant(Z)
    adj = [[(-1)**(i+j)*determinant([
        [Z[row][col] for col in range(3) if col != i]
        for row in range(3) if row != j]) for j in range(3)] for i in range(3)]
    identity(DZ, -b*L*F(1, 2048), 'whole cubic inverse determinant', names)
    require(mmul(Z, adj) == scale(DZ, eye(3)), 'whole cubic adjugate')
    names.append('whole cubic adjugate')
    poly_at_X = madd(madd(madd(madd(mpow(X, 4), scale(F(-1, 2), mpow(X, 3))),
                             scale(a, mpow(X, 2))), scale(b, X)), scale(c, eye(3)))
    Y = scale(-4, mmul(poly_at_X, adj))
    eta_den = b*b*DZ*DZ
    eta_num = 1024*c*c*DZ*DZ+2*b*b*trace(mmul(Y, Y))
    eta_cleared = 1536*H*c*c-6144*b*b*U*c-b*b*W
    identity(2*b*b*L*eta_num, eta_den*eta_cleared,
             'entire actual eta trace quadratic', names)
    identity(W*H+6144*b*b*U*U, L*J, 'credited eta completion', names)
    identity(2*H+J, V, 'credited centered C', names)
    centered_remainder = c*H-2*b*b*U
    identity(-4*H*(2*b*b*L-eta_cleared),
             -4*V*b*b*L+6144*centered_remainder**2,
             'whole full C equals Cbar minus w k squared', names)
    polynomials = {'A': A, 'd': d, 'g': g, 'L': L, 'H': H, 'U': U,
                   'W': W, 'J': J, 'V': V, 'F': FF, 'G': GG, 'T': T,
                   'Na': Na, 'Nb': Nb, 'DF': DF, 'WG': WG,
                   'H_F_cleared': HF, 'V_F_cleared': VF,
                   'eta_num': eta_num, 'eta_den': eta_den,
                   'eta_cleared': eta_cleared, 'centered_remainder': centered_remainder}
    norms = {'DF': DF.norm(), 'WG': WG.norm(), 'H': H.norm(),
             'H_a': H.diff(0).norm(), 'H_b': H.diff(1).norm(),
             'L_a': L.diff(0).norm(), 'L_b': L.diff(1).norm(),
             'center_num': (2*b*b*U).norm(),
             'center_num_a': (2*b*b*U).diff(0).norm(),
             'center_num_b': (2*b*b*U).diff(1).norm()}
    require(norms == {'DF': F(5615304682700256), 'WG': F(533493, 512), 'H': F(2673),
                      'H_a': F(2344), 'H_b': F(3469), 'L_a': F(1236), 'L_b': F(2187),
                      'center_num': F(46), 'center_num_a': F(66), 'center_num_b': F(104)},
            'whole polynomial coefficient norms')
    return {'variables': ['a', 'b', 'c', 'unused', 'unused'],
            'domain': 'QQ[a,b,c]; no localization in the checked identities',
            'identities': names,
            'complete_polynomials': {name: poly.encoded() for name, poly in polynomials.items()},
            'complete_coefficient_norms': {name: str(value) for name, value in norms.items()}}, polynomials


def moving_node_jet(damage=None):
    labels = ['m', 'H', 'J', 'q0', 'q1', 'q2', 'q3', 'lambda_v', 'm_v', 'H_v', 'J_v']
    m, H, J, q0, q1, q2, q3, lv, mv, Hv, Jv = [variable(i, 11, laurent=True) for i in range(11)]
    invH = variable(1, 11, -1, True)
    first = -8*q0*invH-m*q2*invH*F(1, 8)+m*J*q1*invH**2*F(1, 8)
    zero = P(0, 11, True)
    derivatives = [mv, Hv, Jv, q1*lv, q2*lv, q3*lv, zero, zero, zero, zero, zero]
    second = sum((first.diff(i)*v for i, v in enumerate(derivatives)), zero)
    terms = [-8*q1*lv*invH, 8*q0*Hv*invH**2,
             -mv*q2*invH*F(1, 8), -m*q3*lv*invH*F(1, 8),
             m*q2*Hv*invH**2*F(1, 8), mv*J*q1*invH**2*F(1, 8),
             m*Jv*q1*invH**2*F(1, 8), m*J*q2*lv*invH**2*F(1, 8),
             -m*J*q1*Hv*invH**3*F(1, 4)]
    if damage == 'frozen_J_node':
        terms[6] = zero
    require(second == sum(terms, zero), 'whole nine-term moving-node mass derivative')
    require(len(second.c) == 9, 'complete nine distinct second-mass monomials')
    return {'variables': labels, 'localization': 'H only; actual h prime never zero by interlacing',
            'first_mass_derivative': first.encoded(),
            'whole_second_mass_derivative': second.encoded(),
            'whole_nine_displayed_terms': [term.encoded() for term in terms]}


def newton(damage=None):
    mu3, mu4, mu5, mu6, mu7 = [variable(i) for i in range(5)]
    moments = [P(8), P(0), P(1), mu3, mu4, mu5, mu6, mu7]
    coefficients = [P(1)]
    for k in range(1, 8):
        coefficients.append(-sum((coefficients[j]*moments[k-j]
                                 for j in range(k)), P(0))*F(1, k))
    displayed = [-mu3*F(1, 3), mu3*F(1, 6)-mu5*F(1, 5),
                 (mu4*F(1, 12)-F(1, 24))*mu3+mu5*F(1, 10)-mu7*F(1, 7)]
    if damage == 'odd_seventh_moment_sign':
        displayed[2] += 2*mu7*F(1, 7)
    require(coefficients[1] == 0 and coefficients[2] == F(-1, 2),
            'balance and norm Newton coefficients')
    require([coefficients[j] for j in [3, 5, 7]] == displayed, 'entire odd Newton moment identities')
    require(moments[4]-F(1, 8) == F(3, 8)-4*coefficients[4], 'entire D Newton identity')
    return {'variables': ['mu3', 'mu4', 'mu5', 'mu6', 'mu7'],
            'complete_first_seven_octic_coefficients': [p.encoded() for p in coefficients],
            'complete_odd_coefficient_maps': [p.encoded() for p in displayed]}


def scalars(damage=None):
    hmin, hmax, amin, dmin = F(2048, 3), F(2673), F(4), F(9, 2)
    kappa = F(1, 10**8)
    mf, wg = F(5615304682700256), F(1042)
    projection = F(3469)*kappa/(dmin*hmin)
    ca_first = F(67200, 4*45**2)
    ca_error = 4*kappa*mf/(dmin**4*amin**2*hmin**2)
    g_floor = (F(3, 8)**2*amin**2*F(275, 108))/(256*wg)
    cb_floor = 3072*kappa*g_floor/(3*hmax**2)
    if damage == 'weakened_large_F_budget':
        cb_floor *= F(1, 100)
    wmax = 6144*hmax/(4*4**2*512)
    loga = F(2344)/hmin+F(32, 4)+F(1236, 512)
    logb = F(3469)/hmin+F(2, 4)+F(2187, 512)
    centerderiv = F(104)/hmin+F(46*3469)/hmin**2
    transfer = 2+F(10240, 2048**2)
    lprime = F(5, 8*36)
    mprime = F(8, 36)+F(20, 8*36)+F(1344*5, 8*36**2)
    msecond_terms = [F(8*5, 36), F(8*1347, 36**2), F(20, 8*36), F(60, 8*36),
                     F(20*1347, 8*36**2), F(1344*5, 8*36**2),
                     F(3368*5, 8*36**2), F(1344*20, 8*36**2),
                     F(2*1344*5*1347, 8*36**3)]
    msecond = sum(msecond_terms, F(0))
    eta_second = 2*(7+100)
    csecond_terms = [2*eta_second, 64, 256]
    csecond = sum(csecond_terms)
    endpoints = F(1, 4)*F(3, 4)**7*min(factorial(i)*factorial(7-i) for i in range(8))
    perturb = F(5, 4)**5
    asymmetry_exact = F(1, 10**21*2**116)
    weights = [F(13, 24), F(3, 10), F(1, 7)]
    weights2 = sum((x*x for x in weights), F(0))
    checks = {
        'entire DF norm at most 6e15': mf <= 6*10**15,
        'entire WG norm at most 1042': F(533493, 512) <= wg,
        'closed small F projection relative error below half': projection < F(1, 2),
        'signed small F a gradient exceeds one': ca_first-ca_error > 1,
        'large F b gradient at least 1e-17': cb_floor >= F(1, 10**17),
        'all full even log derivatives at most twenty': max(loga, logb) <= 20,
        'full even w at most 512 delta^-28': wmax <= 512,
        'both center derivatives at most delta^-24': centerderiv <= 1,
        'full even gradient transfer below three': transfer < 3,
        'full even gradient constant': F(1, 10**18) <= F(1, 3*10**17),
        'whole critical node first derivative at most one': lprime <= 1,
        'whole first mass derivative at most one': mprime <= 1,
        'whole nine-term second mass derivative at most one hundred': msecond <= 100,
        'universal moving-node Hessian at most one thousand': csecond <= 1000,
        'closed root boxes have a strict endpoint sign margin': endpoints > perturb,
        'complete asymmetry constant including dyadic loss': asymmetry_exact >= F(1, 10**56),
        'large odd part branch also implies target': F(1, 10**56) <= 1,
        'entire triple-moment weight norm': weights2 == F(284929, 705600),
        'paired root coefficient norm constant': 64**2*8 < 192**2,
        'arbitrary reflected target coefficient norm constant': 128**2*8 < 384**2}
    require(all(checks.values()), 'complete sufficient rational scalar comparisons')
    return {'universal_arguments': 'delta in (0,1]; powers compared by monotonicity, not sampling',
            'checks': checks, 'complete_scalars': {
                name: str(value) for name, value in {
                    'H_min': hmin, 'H_max': hmax, 'small_F': kappa,
                    'projection_ratio': projection, 'Ca_first': ca_first, 'Ca_error': ca_error,
                    'G_floor': g_floor, 'Cb_floor': cb_floor, 'wmax': wmax,
                    'loga': loga, 'logb': logb, 'center_derivative': centerderiv,
                    'full_gradient_transfer': transfer, 'lambda_first': lprime,
                    'mass_first': mprime, 'mass_second': msecond,
                    'eta_second': F(eta_second), 'C_second': F(csecond),
                    'root_endpoint': endpoints, 'root_perturbation': perturb,
                    'asymmetry_before_rounding': asymmetry_exact, 'weights_square': weights2}.items()},
            'complete_second_mass_bound_terms': list(map(str, msecond_terms)),
            'complete_C_Hessian_bound_terms': list(map(str, csecond_terms)),
            'critical_cardinal_factorials': [factorial(i)*factorial(6-i) for i in range(7)],
            'original_cardinal_factorials': [factorial(i)*factorial(7-i) for i in range(8)],
            'claimed_exponents': {'reduced_gradient': 48, 'full_even_gradient': 88,
                                  'Hessian': 28, 'odd_coefficients': 116, 'triple_moments': 232},
            'claimed_constants': {'full_even_gradient': '1/1000000000000000000',
                                  'odd_coefficient_norm': '1/'+str(10**56),
                                  'triple_odd_moment_squared': str(F(705600, 284929*10**112)),
                                  'distance_to_reflection_symmetric_originals': str(F(1, 384*10**56))}}


def controls(polynomials):
    p = polynomials
    special = F(5, 56)
    bf = -4*special**2/(15-112*special)
    values = [special, bf, F(0), F(0), F(0)]
    require(p['F'].at(values) == 0 and p['H'].at(values) == 0,
            'actual retained F degree-loss branch')
    exceptional = F(15, 208)
    exceptional_values = [exceptional, F(0), F(0), F(0), F(0)]
    require(p['g'].at(exceptional_values) == 0 and p['G'].at(exceptional_values) != 0,
            'undivided g zero control')
    # Feasible exact even coefficients: originals +-1,+-3,+-5,+-7 divided by sqrt(168).
    squares = [F(k*k, 168) for k in [1, 3, 5, 7]]
    require(sum(squares) == F(1, 2) and len(set(squares)) == 4 and min(squares) > 0,
            'separate feasible root square construction')
    coefficients = [F(1)]
    for square in squares:
        new = [F(0)]*(len(coefficients)+1)
        for i, coefficient in enumerate(coefficients):
            new[i] -= square*coefficient
            new[i+1] += coefficient
        coefficients = new
    c, b, a = coefficients[:3]
    require(coefficients[3:] == [F(-1, 2), F(1)], 'feasible even fixed norm coefficients')
    values = [a, b, c, F(0), F(0)]
    num, den = p['eta_num'], p['eta_den']
    nv, dv = num.at(values), den.at(values)
    eta = nv/dv
    D = F(3, 8)-4*a
    C = (1-eta)/D
    gradients = []
    for i in range(3):
        eta_i = (num.diff(i).at(values)*dv-nv*den.diff(i).at(values))/dv**2
        D_i = F(-4) if i == 0 else F(0)
        gradients.append(-eta_i/D-(1-eta)*D_i/D**2)
    require(0 < eta < 1 and D > 0 and C > 0, 'feasible even actual trace mass control')
    require(max(map(abs, gradients)) >= F(1, 10**18*42**44),
            'feasible exact even gradient bound with delta squared 1/42')
    require(p['H'].at(values) < 0 and p['L'].at(values) < 0 and b < 0,
            'feasible trace denominator signs')
    return {'retained_degree_loss_F_branch': {'a': str(special), 'b': str(bf),
                    'H': '0', 'scope': 'polynomial boundary, not a feasible simple critical profile'},
            'retained_g_zero_branch': {'a': str(exceptional), 'g': '0',
                    'scope': 'no g inverse in the G identity'},
            'feasible_even_separate_root_square_control': {
                'original_positive_squares': list(map(str, squares)), 'a': str(a), 'b': str(b),
                'c': str(c), 'eta': str(eta), 'D': str(D), 'C': str(C),
                'all_three_full_gradients': list(map(str, gradients)),
                'delta_squared': '1/42', 'scope': 'one consistency control; universal proof is written'}}


def damage_checks():
    cases = [('last_DF_coefficient', algebra), ('omitted_degree_loss_factor', algebra),
             ('G_lift_constant', algebra), ('frozen_J_node', moving_node_jet),
             ('odd_seventh_moment_sign', newton), ('weakened_large_F_budget', scalars)]
    rejected = []
    for name, function in cases:
        try:
            function(name)
        except ValueError as error:
            rejected.append({'damage': name, 'whole_mathematical_rejection': str(error)})
        else:
            raise ValueError('mathematical damage accepted: '+name)
    return rejected


def build_record():
    a, polynomials = algebra()
    return {'actual_agent': 'six-sendov-2', 'role': 'researcher',
            'claim_status': 'complete ordinary author proof; unformalized; independently unreviewed',
            'scope': 'eight distinct real normalized originals; explicit stationary asymmetry and three odd moments',
            'not_concluded': ['p5 floor', 'separation-only two-moment bound', 'stationary existence',
                              'collision continuation', 'physical H', 'full degree-nine first-power inequality'],
            'whole_algebra': a, 'whole_moving_node_jet': moving_node_jet(),
            'whole_Newton': newton(), 'whole_scalar_certificate': scalars(),
            'controls': controls(polynomials), 'rejected_mathematical_damages': damage_checks()}


def canonical(record):
    return json.dumps(record, sort_keys=True, separators=(',', ':')).encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    parser.add_argument('--bootstrap', action='store_true', help='author-only initial fixture generation')
    args = parser.parse_args()
    record = build_record()
    if args.bootstrap:
        args.expected.write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
    expected = json.loads(args.expected.read_text())
    require(canonical(expected) == canonical(record), 'ENTIRE typed mathematical record mismatch')
    print(json.dumps({'status': 'PASS', 'actual_agent': 'six-sendov-2', 'role': 'researcher',
                      'whole_algebraic_identities': len(record['whole_algebra']['identities']),
                      'whole_moving_second_mass_terms': 9,
                      'complete_rational_comparisons': len(record['whole_scalar_certificate']['checks']),
                      'rejected_mathematical_damages': len(record['rejected_mathematical_damages']),
                      'record_sha256': hashlib.sha256(canonical(record)).hexdigest()}, sort_keys=True))


if __name__ == '__main__':
    main()
