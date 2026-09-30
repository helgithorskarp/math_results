"""Independent universal polynomial and literal-set seven-weight audit.

six-reviewer-5; Python 3.11 standard library. No author code is imported.
The all-orders bridge is the counting proof in REVIEW.md, not finite tests.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


class P:
    """Exact sparse Q[X,Y], with exponent pairs as keys."""
    def __init__(self, terms):
        self.d = {e: F(c) for e, c in terms.items() if c}
    @staticmethod
    def coerce(x):
        return x if isinstance(x, P) else P({(0, 0): F(x)})
    def __add__(self, x):
        x = P.coerce(x)
        d = self.d.copy()
        for e, c in x.d.items():
            d[e] = d.get(e, F(0)) + c
        return P(d)
    __radd__ = __add__
    def __neg__(self):
        return P({e: -c for e, c in self.d.items()})
    def __sub__(self, x):
        return self + -P.coerce(x)
    def __rsub__(self, x):
        return P.coerce(x) - self
    def __mul__(self, x):
        x = P.coerce(x)
        d = {}
        for (i, j), a in self.d.items():
            for (k, l), b in x.d.items():
                e = (i + k, j + l)
                d[e] = d.get(e, F(0)) + a * b
        return P(d)
    __rmul__ = __mul__
    def __pow__(self, k):
        result = P.coerce(1)
        for _ in range(k):
            result = result * self
        return result


class R:
    """Exact rational functions, checked by numerator after cross multiplication."""
    def __init__(self, n, d=1):
        self.n, self.d = P.coerce(n), P.coerce(d)
        require(bool(self.d.d), 'zero polynomial denominator')
    @staticmethod
    def coerce(x):
        return x if isinstance(x, R) else R(x)
    def __add__(self, x):
        x = R.coerce(x)
        return R(self.n * x.d + x.n * self.d, self.d * x.d)
    __radd__ = __add__
    def __neg__(self):
        return R(-self.n, self.d)
    def __sub__(self, x):
        return self + -R.coerce(x)
    def __rsub__(self, x):
        return R.coerce(x) - self
    def __mul__(self, x):
        x = R.coerce(x)
        return R(self.n * x.n, self.d * x.d)
    __rmul__ = __mul__
    def __truediv__(self, x):
        x = R.coerce(x)
        return R(self.n * x.d, self.d * x.n)


def polynomial_checks():
    v, m = R(P({(1, 0): 1})), R(P({(0, 1): 1}))
    N = 1 + v + v * (v - 1) / 2 + m * v * (v - 1) / 6
    s = v + m * (v - 1) / 2
    h2 = (v * (v - 5) + 2 * m * (v - 1) * (v - 3) / 3) / ((v - 3) * (v - 4))
    h1 = 2 * v / (v - 3) - m * (v - 1) / 6
    c = 2 * ((v - 1) * s + 1 - N - m * (v - 3) * (v - 4) * h2 / 3) / ((v - 2) * (v - 3))
    b = s - (v - 3) * c - m * (v - 5) * h2 / 2
    a = m * (v - 3) * (6 - m * (v - 1)) / 36
    lam = v + m * v * (v - 1) / 6 - m * m * (v - 1) * (v - 1) * (v - 3) / 36
    lam2 = v + 2 * v * (v - 1) / 6 - 4 * (v - 1) * (v - 1) * (v - 3) / 36
    identities = {
        'triple_star': h1 + (v - 4) * h2 - s,
        'triple_row': 1 + s + (v - 3) * h1 + (v - 3) * (v - 4) * h2 / 2 - N,
        'pair_star': b + (v - 3) * c + m * (v - 5) * h2 / 2 - s,
        'pair_row': 1 + s + (v - 2) * b + (v - 2) * (v - 3) * c / 2 + m * (v - 1) * (v - 6) * h2 / 6 - N,
        'singleton_star': a + (v - 2) * b - m * h2 + m * (v - 3) * h1 / 2 - s,
        'singleton_row': 1 + s + (v - 1) * a + (v - 1) * (v - 2) * b / 2 - m * (v - 1) * h2 / 2 + m * (v - 1) * (v - 3) * h1 / 6 - N,
        'singleton_eigenvalue': s + (v - 1) * a - lam,
        'lambda2': lam2 + (v * v * (v - 8) + v - 3) / 9,
        'lambda_difference': lam - lam2 - (m - 2) * (v - 1) * (6 * v - (m + 2) * (v - 1) * (v - 3)) / 36,
        'm4_v9_quadratic': R(F(-1023)) - R(9) * R(F(-341, 3)),
    }
    for name, x in identities.items():
        require(not x.n.d, 'polynomial identity failed: ' + name)
    # A single positive-coefficient certificate proves lambda<0 on all
    # v=9+X, m=2+Y, X,Y>=0. No finite-range extrapolation is used.
    X, Y = P({(1, 0): 1}), P({(0, 1): 1})
    V, M = 9 + X, 2 + Y
    negative36 = M ** 2 * (V - 1) ** 2 * (V - 3) - 6 * M * V * (V - 1) - 36 * V
    require(negative36.d[(0, 0)] > 0 and all(c > 0 for c in negative36.d.values()),
            'negative-eigenvalue positivity certificate')
    return {'zero_identities': sorted(identities),
            'negative36lambda_at_v9plusX_m2plusY':
            [[i, j, str(c)] for (i, j), c in sorted(negative36.d.items())]}


def solve(rows):
    """Full rational RREF, retaining every literal equation for verification."""
    A = [list(map(F, row)) for row in rows]
    original = [row[:] for row in A]
    k = 0
    for c in range(7):
        p = next((i for i in range(k, len(A)) if A[i][c]), None)
        require(p is not None, 'unforced variable')
        A[k], A[p] = A[p], A[k]
        d = A[k][c]
        A[k] = [x / d for x in A[k]]
        for i in range(len(A)):
            if i != k and A[i][c]:
                d = A[i][c]
                A[i] = [x - d * y for x, y in zip(A[i], A[k])]
        k += 1
    weights = [A[i][-1] for i in range(7)]
    require(all(sum(x * y for x, y in zip(row[:7], weights)) == row[7]
                for row in original), 'inconsistent literal equations')
    return weights


def concrete(U, v, m):
    ground = set(range(v))
    require(all(len(a) == 3 and a <= ground for a in U), 'bad triple')
    require(all(sum(frozenset(p) <= a for a in U) == m for p in combinations(range(v), 2)),
            'not a simple pair design')
    D = ([frozenset()] + [frozenset([i]) for i in range(v)] +
         [frozenset(p) for p in combinations(range(v), 2)] +
         sorted(U, key=lambda a: tuple(sorted(a))))
    N, s = len(D), v + m * (v - 1) // 2
    require(N == 1 + v + v * (v - 1) // 2 + m * v * (v - 1) // 6, 'parameters')
    def coeff(A, B):
        row = [0] * 7
        if not A or not B:
            return 1, row
        if A == B:
            return s, row
        if A & B:
            return 0, row
        sizes = tuple(sorted((len(A), len(B))))
        if sizes == (1, 1):
            row[0] = 1
        elif sizes == (1, 2):
            row[1] = 1
            row[2] = -int(A | B in U)
        else:
            row[{(2, 2): 3, (1, 3): 4, (2, 3): 5, (3, 3): 6}[sizes]] = 1
        return 0, row
    table = [[coeff(A, B) for B in D] for A in D]
    rows = set()
    supports = [(list(range(N)), N)] + [([j for j, B in enumerate(D) if i in B], s)
                                        for i in range(v)]
    for row in table:
        for selected, rhs in supports:
            cs = [0] * 7
            for j in selected:
                constant, vector = row[j]
                rhs -= constant
                cs = [x + y for x, y in zip(cs, vector)]
            rows.add(tuple(cs + [rhs]))
    w = solve(sorted(rows))
    h2 = F(3 * v * (v - 5) + 2 * m * (v - 1) * (v - 3), 3 * (v - 3) * (v - 4))
    h1 = F(2 * v, v - 3) - F(m * (v - 1), 6)
    c = 2 * ((v - 1) * s + 1 - N - F(m * (v - 3) * (v - 4), 3) * h2) / ((v - 2) * (v - 3))
    b = s - (v - 3) * c - F(m * (v - 5), 2) * h2
    a = F(m * (v - 3) * (6 - m * (v - 1)), 36)
    require(w == [a, b, h2, c, h1, h2, F(0)], 'literal weights differ from universal formula')
    fvalues = []
    for A in U:
        fs = [sum(frozenset(p) | {i} in U for p in combinations(A, 2)) for i in ground - A]
        require(sum(fs) == 3 * (m - 1), 'completing point sum')
        fvalues.append(tuple(sorted(set(fs))))
    require(any(len(fs) > 1 for fs in fvalues), 'missing variation')
    witness = v * (s + (v - 1) * w[0])
    require(witness < 0, 'negative singleton witness')
    return {'v': v, 'm': m, 'N': N, 's': s, 'affine_rank': 7,
            'weights_a_b_u_c_h1_h2_t': list(map(str, w)),
            'distinct_literal_equations': len(rows),
            'singleton_ones_quadratic_form': str(witness)}


def run(args):
    data = json.loads(args.input.read_text())
    def sets(layer):
        return {frozenset(i for i in range(9) if a & (1 << i)) for a in layer}
    cases = []
    for case in data['cases']:
        cases.append(concrete(set().union(*(sets(t) for t in case['layers'])), 9, 4))
    layers = data['cases'][0]['layers']
    cases.append(concrete(sets(layers[0]) | sets(layers[1]), 9, 2))
    cases.append(concrete({frozenset(t) for t in combinations(range(9), 3)} - sets(layers[0]), 9, 6))
    U13 = {frozenset((i + j) % 13 for j in seed) for i in range(13)
           for seed in [(0, 1, 4), (0, 2, 7)]}
    p = [8, 4, 5, 9, 7, 12, 11, 2, 6, 1, 10, 0, 3]
    V13 = {frozenset(p[i] for i in t) for t in U13}
    require(U13.isdisjoint(V13), 'thirteen seed not disjoint')
    cases.append(concrete(U13 | V13, 13, 2))
    result = {'reviewer': 'six-reviewer-5', 'polynomial_certificates': polynomial_checks(),
              'literal_set_cases': cases, 'universal_scope':
              'Counting proof and exact polynomial identities; v>=9,m>=2 with design and variation hypotheses'}
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print('Verified', len(cases), 'literal designs and 10 universal polynomial identities')


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    run(p.parse_args())
