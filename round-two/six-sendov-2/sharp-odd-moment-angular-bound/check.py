#!/usr/bin/env python3
"""Exact coefficient checks for the ordinary sharp two-odd-zero proof.

Python 3.10+ standard library only. No solver, root approximation, search,
parent mathematical executable, or generated input is used.
"""
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path
import argparse
import json


N = 7  # variable order T,D,p,a,u,v,z over Q
ZERO = (0,) * N


class Poly:
    def __init__(self, terms=None):
        if isinstance(terms, dict):
            self.terms = {k: F(v) for k, v in terms.items() if v}
        else:
            self.terms = {ZERO: F(terms)} if terms else {}

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Poly) else Poly(value)

    def __add__(self, other):
        out = dict(self.terms)
        for k, value in self.coerce(other).terms.items():
            out[k] = out.get(k, F(0)) + value
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({k: -v for k, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) - self

    def __mul__(self, other):
        out = {}
        for k, value in self.terms.items():
            for j, coefficient in self.coerce(other).terms.items():
                power = tuple(x + y for x, y in zip(k, j))
                out[power] = out.get(power, F(0)) + value * coefficient
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, constant):
        return self * (1 / F(constant))

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError('nonnegative integer polynomial power required')
        out = Poly(1)
        for _ in range(power):
            out = out * self
        return out

    def __eq__(self, other):
        return self.terms == self.coerce(other).terms

    def derivative(self, index):
        out = {}
        for k, value in self.terms.items():
            if k[index]:
                power = list(k)
                power[index] -= 1
                out[tuple(power)] = value * k[index]
        return Poly(out)

    def substitute(self, replacements):
        out = Poly()
        for k, value in self.terms.items():
            term = Poly(value)
            for index, power in enumerate(k):
                term = term * self.coerce(replacements.get(index, variables[index])) ** power
            out = out + term
        return out

    def scalar(self):
        if any(k != ZERO for k in self.terms):
            raise ValueError('constant polynomial required')
        return self.terms.get(ZERO, F(0))

    def encoded(self):
        return [[list(k), value.numerator, value.denominator]
                for k, value in sorted(self.terms.items())]


variables = []
for index in range(N):
    power = list(ZERO)
    power[index] = 1
    variables.append(Poly({tuple(power): 1}))
T, D, p, a, u, v, z = variables


def determinant(matrix):
    out = Poly()
    for order in permutations(range(len(matrix))):
        inversions = sum(order[i] > order[j] for i in range(len(order))
                         for j in range(i + 1, len(order)))
        term = Poly((-1) ** inversions)
        for i, j in enumerate(order):
            term = term * matrix[i][j]
        out = out + term
    return out


def adjugate(matrix):
    n = len(matrix)
    return [[(-1) ** (i + j) * determinant(
        [[matrix[r][c] for c in range(n) if c != i]
         for r in range(n) if r != j]) for j in range(n)] for i in range(n)]


def build(damage=None):
    checks = []

    def equal(label, lhs, rhs):
        if lhs != rhs:
            raise ValueError('REJECT: ' + label)
        checks.append(label)

    def positive(label, value):
        if value <= 0:
            raise ValueError('REJECT: ' + label)
        checks.append(label)

    A = [[Poly(7), Poly(F(3, 4)), F(3, 32) + D / 2],
         [Poly(F(3, 4)), F(3, 32) + D / 2, F(3, 256) + 3 * D / 16 + 6 * p],
         [F(3, 32) + D / 2, F(3, 256) + 3 * D / 16 + 6 * p,
          F(3, 2048) + 3 * D / 64 + D ** 2 / 16 + 3 * p]]
    nu = [Poly(1), D, D / 8 + 24 * p]
    y = [F(1, 8) + u, F(1, 8) + v, F(1, 8) - u - v]
    dc = 4 * (u ** 2 + v ** 2 + (u + v) ** 2)
    pc = -u * v * (u + v)
    for i in range(3):
        for j in range(3):
            direct = Poly(7) if i + j == 0 else 2 * sum(t ** (i + j) for t in y)
            equal('whole root-square Gram entry %d,%d' % (i, j),
                  A[i][j].substitute({1: dc, 2: pc}), direct)
    h = z * (z ** 2 - y[0]) * (z ** 2 - y[1]) * (z ** 2 - y[2])
    E = F(3, 64) - D / 8
    G = -F(1, 512) + D / 64 - p
    equal('whole critical polynomial from three square nodes', h,
          (z ** 7 - 3 * z ** 5 / 8 + E * z ** 3 + G * z).substitute({1: dc, 2: pc}))
    # Complete cubic discriminant, checked in the unconstrained u,v ring.
    equal('whole centered cubic discriminant',
          (y[0] - y[1]) ** 2 * (y[0] - y[2]) ** 2 * (y[1] - y[2]) ** 2,
          108 * (dc / 24) ** 3 - 27 * pc ** 2)
    equal('fourth coupling moment substitution', F(9, 64) - 4 * E - 24 * G, nu[2])
    det = determinant(A)
    adj = adjugate(A)
    for i in range(3):
        for j in range(3):
            equal('whole Gram-adjugate product %d,%d' % (i, j),
                  sum(A[i][k] * adj[k][j] for k in range(3)), det if i == j else 0)
    Q = sum(nu[i] * adj[i][j] * nu[j] for i in range(3) for j in range(3))
    phi = (T * D - 1) * det + Q
    closed = (3 * (T + 2) * D ** 4 / 32 + 3 * (4 - T) * D ** 3 / 512
              + 3 * (T - 16) * D ** 2 / 4096
              + p * D * (9 * T / 64 - 3 * (T + 26) * D / 4)
              + p ** 2 * (486 - 252 * T * D))
    equal('whole cleared sharp-envelope identity', phi, closed)
    sharp = F(208, 9)
    phis = phi.substitute({0: sharp})
    B = F(13, 4) - 81 * a - 884 * a ** 2 + 23296 * a ** 3
    equal('whole boundary derivative in p',
          phis.derivative(2).substitute({1: 24 * a ** 2, 2: -2 * a ** 3}), 24 * a ** 2 * B)
    factor_coefficient = 33 if damage == 'boundary-factor' else 34
    equal('whole sharp boundary square factor',
          phis.substitute({1: 24 * a ** 2, 2: -2 * a ** 3}),
          192 * a ** 4 * (a + F(1, 8)) ** 2 * (factor_coefficient * a - 1) ** 2)
    equal('whole decreasing B derivative', B.derivative(3),
          -55 + (a - F(1, 28)) * (69888 * a + 728))
    equal('B endpoint', B.substitute({3: F(1, 28)}).scalar(), F(57, 196))
    equal('p-quadratic minimum at band endpoint', 486 - 252 * sharp * F(3, 112), 330)
    equal('a squared cutoff', F(3, 112) / 24, F(1, 896))
    positive('a below convenient derivative endpoint', F(1, 784) - F(1, 896))
    positive('positive centered square nodes throughout band', F(1, 8) - F(2, 28))
    # Independent trace-tail rational algebra; no numerical evaluation.
    equal('whole centered trace-tail numerator',
          F(6, 7) * (F(3, 224) + D / 2) - (D - F(3, 28)) ** 2,
          D * (F(9, 14) - D))
    equal('tail threshold', (144 - 224 * F(3, 112)) / (3 + 112 * F(3, 112)), 23)
    equal('whole tail derivative numerator',
          -224 * (3 + 112 * D) - 112 * (144 - 224 * D), -16800)
    equal('sharp threshold gap', F(47, 2) - sharp, F(7, 18))
    skew_denominator = 55 if damage == 'skew-budget' else 56
    equal('whole seventh-moment penalty conversion',
          F(56 ** 2, skew_denominator), 56)
    equal('tail pays the seventh-moment penalty', sharp - F(1, 56) - 23, F(47, 504))
    positive('tail penalty margin', F(47, 504))
    # Credited 8672 optimizer; direct primitive/resolvent checks include
    # zero FULL masses at the two double critical eigenvalues.
    r, t, s = F(21, 136), F(5, 136), F(9, 136)
    fopt = (z ** 2 - r) ** 3 * (z ** 2 - t)
    hopt = z * (z ** 2 - r) ** 2 * (z ** 2 - s)
    equal('whole optimizer derivative', fopt.derivative(6) / 8, hopt)
    equal('optimizer norm', 6 * r + 2 * t, 1)
    dopt = 6 * r ** 2 + 2 * t ** 2 - F(1, 8)
    equal('optimizer fourth variance', dopt, F(6, 289))
    m0 = F(35, 51)
    ms = F(4, 51) if damage == 'grouped-mass' else F(8, 51)
    equal('full grouped mass normalization', m0 + 2 * ms, 1)
    equal('whole optimizer resolvent without denominator cancellation',
          hopt * (m0 * (z ** 2 - s) + 2 * ms * z ** 2),
          8 * (z * hopt - fopt) * z * (z ** 2 - s))
    eta = m0 ** 2 + 2 * ms ** 2
    equal('optimizer full grouped squared masses', eta, F(451, 867))
    equal('optimizer sharp angular quotient', (1 - eta) / dopt, sharp)
    aopt = F(1, 34)
    popt = -2 * aopt ** 3
    equal('optimizer discriminant-boundary coordinates', 24 * aopt ** 2, dopt)
    equal('optimizer double and simple critical squares',
          sorted([F(1, 8) + aopt, F(1, 8) + aopt, F(1, 8) - 2 * aopt]), sorted([r, r, s]))
    doptdet = det.substitute({1: dopt, 2: popt}).scalar()
    positive('optimizer Gram denominator remains positive', doptdet)
    equal('optimizer even envelope attains actual squared masses',
          Q.substitute({1: dopt, 2: popt}).scalar() / doptdet, eta)
    equal('optimizer nonuniform sharp numerator zero', phis.substitute({1: dopt, 2: popt}), 0)
    return {
        'actual_agent': 'six-sendov-2', 'role': 'researcher',
        'ring': 'Q[T,D,p,a,u,v,z]', 'complete_finite_checks': len(checks),
        'checks': checks, 'whole_det_A': det.encoded(), 'whole_nu_adjugate_nu': Q.encoded(),
        'whole_Phi_T': phi.encoded(), 'whole_sharp_boundary_factor':
        phis.substitute({1: 24 * a ** 2, 2: -2 * a ** 3}).encoded(),
        'sharp_bound': [208, 9], 'gap_below_47_over_2': [7, 18],
        'credited_optimizer': {'source_graph_height': 8672, 'r': [21, 136], 't': [5, 136],
                               'full_masses': [[35, 51], [8, 51], [8, 51]], 'D': [6, 289]},
        'trust_boundary': 'ordinary written positivity, feasibility, parity penalty and collision bridges; no formalization or independent review',
        'no_parent_executable_or_generated_data': True, 'no_solver_or_enumeration': True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--derive', action='store_true', help='derive the entire exact record without reading expected.json')
    parser.add_argument('--damage', choices=['boundary-factor', 'skew-budget', 'grouped-mass'])
    args = parser.parse_args()
    record = build(args.damage)
    if not args.derive:
        expected = json.loads(Path(__file__).with_name('expected.json').read_text())
        if record != expected:
            raise ValueError('REJECT: entire external exact record')
    print(json.dumps(record, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
