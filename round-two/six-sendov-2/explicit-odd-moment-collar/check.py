#!/usr/bin/env python3
"""Exact small-Gram identities and rational budgets; no root search or solver.

The analytic heat separation, real-root sign argument, least squares and
collision completion are ordinary written proof, not checked by this script.
The closed parent executables and their generated corpora are not imported.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
from math import factorial
import argparse
import hashlib
import json

NAMES = ('T', 'D', 'p', 'a', 'E', 'G', 'J', 'c', 'u', 'v', 'z', 's')
ZERO = (0,) * len(NAMES)
CHECKS = []
HEAT_BUDGET = F(112)
DET_FLOOR = F(1, 20000000)
EPSILON = F(1, 10**180)
HEAT_TIME = F(1, 10**20)


def require(ok, name):
    if not ok:
        raise ArithmeticError(name)
    CHECKS.append(name)


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            self.d = dict(value.d)
        elif isinstance(value, dict):
            self.d = {k: F(v) for k, v in value.items() if v}
        else:
            self.d = {ZERO: F(value)} if value else {}

    def __add__(self, other):
        d = dict(self.d)
        for k, v in P(other).d.items():
            d[k] = d.get(k, F(0)) + v
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.d.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        d = {}
        for k, v in self.d.items():
            for q, w in P(other).d.items():
                t = tuple(i+j for i, j in zip(k, q))
                d[t] = d.get(t, F(0)) + v*w
        return P(d)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1/F(scalar))

    def __pow__(self, n):
        if type(n) is not int or n < 0:
            raise ValueError('only nonnegative integer powers')
        out = P(1)
        for _ in range(n):
            out = out*self
        return out

    def __eq__(self, other):
        return self.d == P(other).d

    def derivative(self, name):
        i = NAMES.index(name)
        out = {}
        for key, value in self.d.items():
            if key[i]:
                q = list(key)
                q[i] -= 1
                out[tuple(q)] = value*key[i]
        return P(out)

    def substitute(self, replacements):
        out = P(0)
        for key, value in self.d.items():
            term = P(value)
            for name, n in zip(NAMES, key):
                if n:
                    term *= P(replacements.get(name, variable(name)))**n
            out += term
        return out

    def coefficient(self, name, n):
        i = NAMES.index(name)
        out = {}
        for key, value in self.d.items():
            if key[i] == n:
                q = list(key)
                q[i] = 0
                out[tuple(q)] = value
        return P(out)

    def encode(self):
        return [[list(k), v.numerator, v.denominator]
                for k, v in sorted(self.d.items())]


def variable(name):
    k = list(ZERO)
    k[NAMES.index(name)] = 1
    return P({tuple(k): 1})


T, D, p, a, E, G, J, c, u, v, z, s = map(variable, NAMES)


def det(matrix):
    n = len(matrix)
    out = P(0)
    for order in permutations(range(n)):
        inversions = sum(order[i] > order[j]
                         for i in range(n) for j in range(i+1, n))
        term = P((-1)**inversions)
        for i, j in enumerate(order):
            term *= matrix[i][j]
        out += term
    return out


def adjugate(matrix):
    n = len(matrix)
    return [[(-1)**(i+j)*det([[matrix[r][k] for k in range(n) if k != i]
                            for r in range(n) if r != j])
             for j in range(n)] for i in range(n)]


def newton(poly, degree, top):
    coefficients = [poly.coefficient('z', degree-i)
                    for i in range(degree+1)]
    require(coefficients[0] == 1, 'monic input for Newton degree '+str(degree))
    moments = [P(degree)]
    for k in range(1, top+1):
        if k <= degree:
            value = -k*coefficients[k]
            value -= sum((coefficients[j]*moments[k-j]
                          for j in range(1, k)), P(0))
        else:
            value = -sum((coefficients[j]*moments[k-j]
                          for j in range(1, degree+1)), P(0))
        moments.append(value)
    return moments


def heat(poly):
    out, derivative = P(0), P(poly)
    for j in range(5):
        out += (-s)**j/factorial(j)*derivative
        derivative = derivative.derivative('z').derivative('z')
    return out


def record():
    f = z**8-z**6/2-u*z**5/3+2*E*z**4+(u/6-v/5)*z**3+4*G*z**2+8*J*z+c
    h = f.derivative('z')/8
    r = 8*z*h-8*f
    expected_r = z**6+u*z**5-8*E*z**4+(v-5*u/6)*z**3-24*G*z**2-56*J*z-8*c
    require(r == expected_r, 'whole general compression resolvent numerator')
    tau = newton(h, 7, 8)
    target_tau = {
        0: P(7), 2: P(F(3, 4)), 4: P(F(9, 32))-4*E,
        6: P(F(27, 256))-9*E/4-6*G+25*u**2/192,
        8: P(F(81, 2048))-9*E/8+4*E**2-3*G+5*u**2/192+u*v/8}
    for k, target in target_tau.items():
        require(tau[k] == target, 'whole general even critical trace '+str(k))
    hc = [h.coefficient('z', 7-j) for j in range(8)]
    nu = []
    for k in range(5):
        value = r.coefficient('z', 6-k)
        value -= sum((hc[j]*nu[k-j] for j in range(1, k+1)), P(0))
        nu.append(value)
    target_nu = [P(1), u, P(F(3, 8))-8*E, v-u/4,
                 P(F(9, 64))-4*E-24*G+5*u**2/24]
    for k in range(5):
        require(nu[k] == target_nu[k], 'whole general coupling moment '+str(k))
    mu = newton(f, 8, 6)
    require(mu[3] == u and mu[5] == v, 'whole original third and fifth moments')
    require(mu[4]-F(1, 8) == nu[2], 'second coupling versus direct projected square')
    require(mu[6]-mu[4]/4+F(1, 64)-mu[3]**2/8 == nu[4],
            'fourth coupling versus direct projected cube norm')
    require(mu[6] == P(F(1, 4))-6*E+u**2/3-24*G,
            'whole original sixth moment and G budget identity')

    A = [[tau[2*(i+j)] for j in range(3)] for i in range(3)]
    w = [nu[2*i] for i in range(3)]
    exact = {'u': 0, 'v': 0, 'E': F(3, 64)-D/8,
             'G': -F(1, 512)+D/64-p}
    A0 = [[entry.substitute(exact) for entry in row] for row in A]
    w0 = [entry.substitute(exact) for entry in w]
    require(w0 == [P(1), D, D/8+24*p], 'whole exact-locus even coupling chart')
    delta = det(A0)
    adj = adjugate(A0)
    for i in range(3):
        for j in range(3):
            product = sum((A0[i][k]*adj[k][j] for k in range(3)), P(0))
            require(product == (delta if i == j else P(0)),
                    'whole small Gram adjugate product '+str(i)+','+str(j))
    phi = (T*D-1)*delta+sum((w0[i]*adj[i][j]*w0[j]
                           for i in range(3) for j in range(3)), P(0))
    target_phi = (3*(T+2)*D**4/32+3*(4-T)*D**3/512
                  +3*(T-16)*D**2/4096
                  +p*D*(9*T/64-3*(T+26)*D/4)
                  +p**2*(486-252*T*D))
    require(phi == target_phi, 'whole credited cleared even-envelope polynomial')
    require(delta.coefficient('p', 2) == -252, 'whole Gram determinant concavity')
    for sign in (-1, 1):
        specialized = delta.substitute({'D': 24*a**2, 'p': sign*2*a**3})
        expected = 72*a**2*(F(1, 8)-sign*a)**2*(F(1, 8)+sign*2*a)**2
        require(specialized == expected,
                'whole determinant boundary factor sign '+str(sign))
    sharp = phi.substitute({'T': F(208, 9), 'D': 24*a**2})
    B = P(F(13, 4))-81*a-884*a**2+23296*a**3
    require(sharp.derivative('p').substitute({'p': -2*a**3}) == 24*a**2*B,
            'whole lower-endpoint sharp p derivative')
    require(B.derivative('a') == -55+(a-F(1, 28))*(69888*a+728),
            'whole decreasing B derivative')
    require(B.substitute({'a': F(1, 28)}) == F(57, 196), 'positive B endpoint')
    require(sharp.substitute({'p': -2*a**3}) == 192*a**4*(a+F(1, 8))**2*(34*a-1)**2,
            'whole sharp boundary square')

    ft = heat(f)
    expected_ft = (z**8-(F(1, 2)+56*s)*z**6-u*z**5/3
        +(2*E+15*s+840*s**2)*z**4+(u/6-v/5+20*u*s/3)*z**3
        +(4*G-24*E*s-90*s**2-3360*s**3)*z**2
        +(8*J-u*s+6*v*s/5-20*u*s**2)*z
        +c-8*G*s+24*E*s**2+60*s**3+1680*s**4)
    require(ft == expected_ft, 'whole general backward heat polynomial')
    f0 = f.substitute({'u': 0, 'v': 0})
    discrepancy = heat(f-f0)
    require(discrepancy == -u*(z**5-20*s*z**3+60*s**2*z)/3
            +(u/6-v/5)*(z**3-6*s*z), 'whole odd-erasure heat discrepancy')
    heat0_mu = newton(heat(f0), 8, 5)
    require(heat0_mu[1] == 0 and heat0_mu[2] == 1+112*s,
            'whole erased heat balance and square norm')
    require(heat0_mu[3] == 0 and heat0_mu[5] == 0,
            'whole erased heat third and fifth moments')
    require((F(3, 8)*(1+112*s)**2-8*(E+15*s/2+420*s**2)).substitute(
            {'E': F(3, 64)-D/8}) == D+24*s+1344*s**2,
            'whole normalized heat fourth variance numerator')

    time, eps = HEAT_TIME, EPSILON
    sqrt_eps = F(1, 10**90)
    require(sqrt_eps**2 == eps, 'exact residual square root')
    require(time > 0 and eps > 0 and time <= F(1, 10**6), 'positive small heat time and collar')
    require((32+160+120)/F(3)+(8+12)/F(6)+(8+12)/F(5) <= HEAT_BUDGET,
            'whole odd heat discrepancy at absolute z at most two')
    require(HEAT_BUDGET*sqrt_eps < time**4/4096, 'strict eight-root sign licence')
    require(1+112*time < F(9, 4) and time/8 < F(1, 4),
            'heated root and interval endpoints stay within absolute two')
    for i in range(1, 8):
        require(2*(F(1, i)+F(1, 8-i)) >= 1,
                'minimal-gap root velocity bound index '+str(i))
    require(F(43, 2)+1204*time < 24, 'whole normalized E perturbation budget')
    require(F(339, 8)+F(9453, 2)*time+176456*time**2 < 44,
            'whole normalized G perturbation budget')
    require((F(1, 4)+6*F(1, 16)+F(1, 3)+1)/24 < F(1, 8),
            'whole original G absolute budget')
    require(192*time < F(1, 1352) and 192*time < F(9, 2800),
            'heated comparison stays inside enlarged localized band')
    require(F(3, 100)/24 == F(1, 800) and F(1, 800) < F(1, 784),
            'enlarged band lies below convenient a endpoint')
    require(F(1, 8)-F(1, 28) == F(5, 56)
            and F(1, 8)-F(1, 14) == F(3, 56), 'whole positive square-node margins')
    require(486-252*F(208, 9)*F(3, 100) == F(7782, 25)
            and F(7782, 25) > 300, 'positive sharp p quadratic on enlarged band')
    coarse_det = 72*F(1, 32448)*F(5, 56)**2*F(3, 56)**2
    require(coarse_det > DET_FLOOR, 'strict quantitative even Gram determinant floor')
    require(4*24 <= 320 and F(9, 4)*24+6*44 <= 320,
            'whole fourth and sixth trace time budgets')
    require(F(9, 8)*24+4*F(1, 8)*24+3*44 <= 320,
            'whole eighth trace time budget')
    require(F(25, 192) <= 1 and F(5, 192)+F(1, 16) <= 1,
            'whole sixth and eighth trace residual budgets')
    require(4*24+24*44 == 1152 and F(5, 24) <= 1,
            'whole fourth coupling perturbation budget')
    beta, gamma, d = 320*time+eps, 1152*time+eps, 192*time
    require(6*3*7**2 == 882 and 2*2*7 == 28 and 2*7**2 == 98,
            'literal determinant and cofactor telescoping constants')
    require(882*beta < DET_FLOOR, 'perturbed Gram determinant stays positive')
    require(F(70, 3)*F(3, 100) < 1, 'comparison numerator coefficient absolute at most one')
    loss = 24*d*2058+1134*beta+1764*gamma
    budget = 12000000*time+3000*eps
    require(loss < budget, 'whole cleared numerator perturbation budget')
    margin = F(2, 9)*F(1, 1352)*DET_FLOOR
    require(F(70, 3)-F(208, 9) == F(2, 9), 'whole threshold gap')
    require(budget < margin, 'strict numerical collar sign margin')
    require(F(5560, 243) < F(70, 3) and 23 < F(70, 3) and 16 < F(70, 3),
            'credited small-variance tail and uniform values below threshold')
    return {
        'actual_agent': 'six-sendov-2', 'role': 'researcher',
        'ring': 'Q['+','.join(NAMES)+']', 'variables': list(NAMES),
        'epsilon': [eps.numerator, eps.denominator],
        'heat_time': [time.numerator, time.denominator], 'threshold': [70, 3],
        'whole_general_even_Gram': [[entry.encode() for entry in row] for row in A],
        'whole_general_even_coupling': [nu[i].encode() for i in (0, 2, 4)],
        'whole_exact_determinant': delta.encode(),
        'whole_exact_Phi_T': phi.encode(),
        'whole_erased_heat_discrepancy': discrepancy.encode(),
        'determinant_floor': [DET_FLOOR.numerator, DET_FLOOR.denominator],
        'strict_sign_margin': [margin.numerator, margin.denominator],
        'perturbation_budget': [budget.numerator, budget.denominator],
        'complete_finite_checks': len(CHECKS), 'checks': CHECKS,
        'no_solver_float_enumeration_or_parent_reexecution': True,
        'trust_boundary': 'ordinary written heat-gap, real-root sign, least-squares and collision bridges; unformalized and independently unreviewed'
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit', type=Path)
    args = parser.parse_args()
    value = record()
    payload = (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()
    if args.emit:
        args.emit.write_bytes(payload)
    else:
        frozen = Path(__file__).with_name('expected.json').read_bytes()
        if payload != frozen:
            raise ArithmeticError('entire external expected record mismatch')
    print(json.dumps({'checks': len(CHECKS), 'bytes': len(payload),
                      'sha256': hashlib.sha256(payload).hexdigest(),
                      'complete_record_equal': not bool(args.emit)}, sort_keys=True))


if __name__ == '__main__':
    main()
