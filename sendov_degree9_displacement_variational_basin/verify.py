#!/usr/bin/env python3
"""Exact author checks for the displacement variational basin and cubic oracle.

Author six-sendov-2, researcher. Sparse kernel adapted from this author's
earlier symmetric-face code and public rational commutant controls;
no floating point, external CAS, solver, or numerical root labels.
"""
from fractions import Fraction as F
from itertools import permutations, combinations_with_replacement
from pathlib import Path
import argparse
import hashlib
import json
from math import isqrt


class P:
    def __init__(self, value=0):
        if isinstance(value, P):
            value = value.t
        if isinstance(value, (int, F)):
            value = {(0, 0, 0, 0): F(value)}
        self.t = {tuple(e): F(c) for e, c in value.items() if c}

    def __add__(self, other):
        d = dict(self.t)
        for e, c in P(other).t.items():
            d[e] = d.get(e, F(0)) + c
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({e: -c for e, c in self.t.items()})

    def __sub__(self, other):
        return self + -P(other)

    def __rsub__(self, other):
        return P(other) + -self

    def __mul__(self, other):
        d = {}
        for e, c in self.t.items():
            for h, b in P(other).t.items():
                k = tuple(x + y for x, y in zip(e, h))
                d[k] = d.get(k, F(0)) + c * b
        return P(d)

    __rmul__ = __mul__

    def __truediv__(self, scalar):
        return self * (1 / F(scalar))

    def __pow__(self, n):
        if n < 0:
            raise ValueError('polynomial exponent must be nonnegative')
        a, out = self, P(1)
        while n:
            if n & 1:
                out *= a
            a *= a
            n //= 2
        return out

    def __eq__(self, other):
        return self.t == P(other).t

    def at(self, values):
        out = P(0)
        for e, c in self.t.items():
            z = P(c)
            for v, k in zip(values, e):
                z *= P(v) ** k
            out += z
        return out

    def scalar(self):
        if any(any(e) for e in self.t):
            raise ValueError('not a scalar')
        return self.t.get((0, 0, 0, 0), F(0))

    def divide(self, divisor):
        """Exact lexicographic polynomial division by one polynomial."""
        divisor = P(divisor)
        de = max(divisor.t)
        dc = divisor.t[de]
        out, r = P(0), P(self)
        while r.t:
            re = max(r.t)
            if any(x < y for x, y in zip(re, de)):
                raise ValueError('nonzero division remainder')
            e = tuple(x-y for x, y in zip(re, de))
            q = P({e: r.t[re]/dc})
            out += q
            r -= q*divisor
        return out

    def dump(self):
        return [[*e, str(c)] for e, c in sorted(self.t.items())]


def mm(a, b):
    return [[sum((a[i][k]*b[k][j] for k in range(3)), P(0))
             for j in range(3)] for i in range(3)]


def lin(a, b, c, matrix):
    square = mm(matrix, matrix)
    return [[a*square[i][j]+b*matrix[i][j]+(c if i == j else P(0))
             for j in range(3)] for i in range(3)]


def det(m):
    out = P(0)
    for q in permutations(range(3)):
        sign = (-1)**sum(q[i] > q[j] for i in range(3) for j in range(i+1, 3))
        out += sign*m[0][q[0]]*m[1][q[1]]*m[2][q[2]]
    return out


def adj(m):
    result = [[P(0) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            rows, cols = [h for h in range(3) if h != j], [h for h in range(3) if h != i]
            result[i][j] = (-1)**(i+j)*(m[rows[0]][cols[0]]*m[rows[1]][cols[1]]-
                                      m[rows[0]][cols[1]]*m[rows[1]][cols[0]])
    return result


CHECKS = 0


def require(ok, message):
    global CHECKS
    CHECKS += 1
    if not ok:
        raise ValueError(message)


e1, e2, e3, e4 = [P({tuple(int(i == j) for j in range(4)): 1}) for i in range(4)]
disc = 36*e1**2*e2**2 - 128*e2**3 - 108*e1**3*e3 - 432*e3**2 + 432*e1*e2*e3
M = [[P(0), P(0), e3/4], [P(1), P(0), -e2/2], [P(0), P(1), 3*e1/4]]
T = lin(3*e1, -4*e2, 3*e3, M)
G = lin(e2/2 - 3*e1**2/16, e1*e2/8 - 3*e3/4, e4 - e1*e3/16, M)
adjT = adj(T)
C = mm(G, adjT)
Csq = mm(C, C)
trace = sum((Csq[i][i] for i in range(3)), P(0))
Psi_num_big = 16*e4**2*disc**2 + 2048*trace
Psi_den_big = e3**2*disc**2


def solve(a, b):
    """Exact Gaussian elimination; each selected constraint is independent."""
    n = len(b)
    a = [list(r)+[v] for r, v in zip(a, b)]
    for j in range(n):
        i = next(i for i in range(j, n) if a[i][j])
        a[j], a[i] = a[i], a[j]
        t = a[j][j]
        a[j] = [v/t for v in a[j]]
        for i in range(j+1, n):
            t = a[i][j]
            if t:
                a[i] = [u-t*v for u, v in zip(a[i], a[j])]
    out = [F(0)]*n
    for j in range(n-1, -1, -1):
        out[j] = a[j][-1]-sum(a[j][k]*out[k] for k in range(j+1, n))
    return out


def independent_rows(rows):
    pivots, selected = {}, []
    for original in rows:
        r = list(original)
        for j, b in sorted(pivots.items()):
            t = r[j]
            if t:
                r = [u-t*v for u, v in zip(r, b)]
        if any(r):
            j = next(j for j, v in enumerate(r) if v)
            t = r[j]
            pivots[j] = [v/t for v in r]
            selected.append(original)
    return selected


def pinching(theta):
    """Definition-level Psi via a rational symmetric-commutant projection.

    The full eight-space compression adds the zero eigenspace spanned by e.
    Since w is perpendicular to e, its spectral weights are unchanged.
    Every original commutation constraint is checked after solving the
    independent row system; rank selection is not assumed correct silently.
    """
    n = len(theta)
    require(n == 8 and sum(theta) == 0, 'balanced definition-level input')
    a = [[(theta[i] if i == j else 0)-(theta[i]+theta[j])/n
          for j in range(n)] for i in range(n)]
    pairs = list(combinations_with_replacement(range(n), 2))
    weights = [F(1 if i == j else 2) for i, j in pairs]
    w = [theta[i]*theta[j]/n for i, j in pairs]
    all_rows = []
    for i in range(n):
        for j in range(i+1, n):
            row = []
            for h, k in pairs:
                v = (a[i][h] if k == j else 0)-(a[k][j] if i == h else 0)
                if h != k:
                    v += (a[i][k] if h == j else 0)-(a[h][j] if i == k else 0)
                row.append(v)
            all_rows.append(row)
    rows = independent_rows(all_rows)
    rhs = [sum(c*v for c, v in zip(row, w)) for row in rows]
    gram = [[sum(c*d/g for c, d, g in zip(row, other, weights))
             for other in rows] for row in rows]
    lam = solve(gram, rhs)
    projected = [v-sum(row[k]*b for row, b in zip(rows, lam))/weights[k]
                 for k, v in enumerate(w)]
    for row in all_rows:
        require(sum(c*v for c, v in zip(row, projected)) == 0,
                'projected matrix commutes: original constraint')
    residual = [u-v for u, v in zip(w, projected)]
    require(sum(g*u*v for g, u, v in zip(weights, projected, residual)) == 0,
            'Frobenius orthogonality')
    return sum(g*v*v for g, v in zip(weights, projected)), len(rows)


def evaluate_bound():
    alpha = e1
    h = 112-11*alpha
    fnum = 764*alpha*h+1568*h-45*(56-13*alpha)**2
    require(847*fnum == 7*(2113776*h-16009*h*h-31752000),
            'AMGM reduction of the displacement relaxation')
    cleared = 813*7*h-fnum
    require(cleared == 16009*alpha*alpha-196441*alpha+602896,
            'rational 813 certificate')
    require(64036*cleared == (32018*alpha-196441)**2+17981775,
            'positive square certificate')
    require(17981775 > 0 and 112-11*8 > 0, 'positive certificate constants')
    require(16009*31752000 == 2520**2*80045, 'radical simplification')
    require(F(5388,7) < F(18658,23), 'low regime below the relaxation maximum')
    require(fnum.at([6,0,0,0]).scalar()/F(7*(112-11*6)) == F(18658,23),
            'relaxation at alpha=6')
    p0, d0 = F(10985,33554432), F(13,8)
    require(d0**4/p0 == F(106496,5), 'metric and coefficient scaling')
    scale = 10**12
    n = isqrt(80045*scale*scale)
    require(n*n <= 80045*scale*scale < (n+1)*(n+1), 'integer radical enclosure')
    lower = (2113776-5040*F(n+1,scale))/847
    upper = (2113776-5040*F(n,scale))/847
    require(F(812) < lower < upper < F(813), 'H0 exact interval')
    basin_lower, basin_upper = F(106496,5)/upper, F(106496,5)/lower
    require(F('26.2273440907') < basin_lower < basin_upper < F('26.2273440908'),
            'displacement lower-bound enclosure')
    return {'H0_lower': str(lower), 'H0_upper': str(upper),
            'B_relax_lower': str(basin_lower), 'B_relax_upper': str(basin_upper),
            'rational_simple_B_lower': '106496/4065'}


def verify():
    bound = evaluate_bound()
    require(det(T) == -e3*disc/16, 'T determinant')
    for i, row in enumerate(mm(T, adjT)):
        for j, v in enumerate(row):
            require(v == (-e3*disc/16 if i == j else 0), 'adjugate identity')
    powers = [None, M]
    powers.append(mm(M, M))
    powers.append(mm(powers[2], M))
    powers.append(mm(powers[3], M))
    for i in range(3):
        for j in range(3):
            identity = int(i == j)
            require(4*powers[3][i][j]-3*e1*powers[2][i][j]+2*e2*M[i][j]-e3*identity == 0,
                    'Q(M)=0')
            require(powers[4][i][j]-e1*powers[3][i][j]+e2*powers[2][i][j]-e3*M[i][j]+e4*identity == G[i][j],
                    'g(M)=G')
    numerator = Psi_num_big.divide(disc)
    require(numerator*disc == Psi_num_big, 'exact discriminant cancellation')
    denominator = e3**2*disc
    a = (128*e2**4-480*e1*e2**2*e3+180*e1**2*e3**2-64*e1**2*e2**3+
         204*e1**3*e2*e3+9*e1**4*e2**2-27*e1**5*e3)
    b = 3072*e2**2-768*e1**2*e2-2304*e1*e3
    c = (-64512*e3**2-24576*e2**3+70656*e1*e2*e3+
         6912*e1**2*e2**2-17280*e1**3*e3)
    require(8*numerator == e3**2*a+e3**2*e4*b+e4**2*c,
            'explicit 15-term rational Psi formula')
    S, P0 = e1, e2
    face_values = [2+S, 1+2*S+P0, S+2*P0, P0]
    A, B = 2+3*S, S+2*P0
    delta = A*A-16*B
    c0 = S*S+2*S+2*P0*S-12*P0
    c1 = 8*P0-3*S*S+4*S-4
    w = 2*c1*B+c0*A
    face_num = (1024*P0**2+c0**2)*delta+w*w
    face_den = 64*B*B*delta
    require(numerator.at(face_values)*face_den == denominator.at(face_values)*face_num,
            'symbolic Y=1 face recovery')
    controls = []
    examples = [(F(1),F(3,4),F(1,2),F(1,4)),
                (F(1),F(4,5),F(2,5),F(1,5)),
                (F(1),F(2,3),F(1,3),F(0)),
                (F(1),F(1),F(1,2),F(1,3)),
                (F(1),F(3,4),F(3,4),F(1,4)),
                (F(1),F(1),F(1),F(1,3)),
                (F(1),F(1),F(1),F(1)),
                (F(1),F(0),F(0),F(0)),
                (F(1),F(1),F(0),F(0))]
    for slopes in examples:
        coeff = [F(1), F(0), F(0), F(0), F(0)]
        for s in slopes:
            for k in range(4, 0, -1):
                coeff[k] += s*s*coeff[k-1]
        values = coeff[1:]
        theta = list(slopes)+[-s for s in slopes]
        psi, rank = pinching(theta)
        d = denominator.at(values).scalar()
        if d:
            require(values[2] > 0 and disc.at(values).scalar() > 0, 'physical generic domain')
            require(numerator.at(values).scalar()/d == psi, 'definition-level generic Psi control')
        else:
            # Compute the invariant directly, rather than divide by zero.
            expected = {(F(1),F(1),F(1),F(1,3)): F(17,81),
                        (F(1),F(1),F(1),F(1)): F(1),
                        (F(1),F(0),F(0),F(0)): F(1,32),
                        (F(1),F(1),F(0),F(0)): F(1,8)}
            require(slopes in expected, 'enumerated singular control')
            require(psi == expected[slopes], 'definition-level singular Psi control')
        mu2, mu4 = sum(t*t for t in theta), sum(t**4 for t in theta)
        J = (224*mu4+122*mu2*mu2-5760*psi)/mu2
        if slopes == (F(1),F(1),F(1),F(1,3)):
            require(J == F(5472,7), 'existing rational three-unit-pair profile')
        controls.append({'slopes': list(map(str,slopes)), 'Psi': str(psi),
                         'J': str(J), 'commutator_rank': rank, 'generic': bool(d)})
    singleton = [F(1)]+[F(-1,7)]*7
    psi, rank = pinching(singleton)
    mu2, mu4 = sum(t*t for t in singleton), sum(t**4 for t in singleton)
    J = (224*mu4+122*mu2*mu2-5760*psi)/mu2
    require(J == F(1632,7), 'credited energy optimizer in the different normalization')
    controls.append({'theta': list(map(str,singleton)), 'Psi': str(psi),
                     'J': str(J), 'commutator_rank': rank})
    coefficients = {'cubic_Psi_numerator': numerator.dump(), 'cubic_Psi_denominator': denominator.dump(),
                    'rational_813_certificate': (813*7*(112-11*e1)-
                        (764*e1*(112-11*e1)+1568*(112-11*e1)-45*(56-13*e1)**2)).dump()}
    digest = hashlib.sha256(json.dumps(coefficients, sort_keys=True, separators=(',',':')).encode()).hexdigest()
    return {'agent': 'six-sendov-2', 'role': 'researcher', 'status': 'exact author algebra checks; analytic bridges not formalized',
            'checks': CHECKS, 'coefficient_sha256': digest, 'cubic_numerator_terms': len(numerator.t),
            'cubic_denominator_terms': len(denominator.t), 'definition_controls': controls, 'bound': bound}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    parser.add_argument('--write-expected', type=Path)
    args = parser.parse_args()
    if args.expected and args.write_expected:
        parser.error('choose comparison or manifest generation')
    report = verify()
    if args.expected:
        expected = json.loads(args.expected.read_text())
        if report != expected:
            raise ValueError('computed evidence does not match the expected manifest')
    if args.write_expected:
        args.write_expected.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
