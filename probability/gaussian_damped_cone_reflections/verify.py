#!/usr/bin/env python3
"""Exact supplementary audits. Universal analytic claims are in PROOF.md.

CPython >=3.11, standard library only. No numerical quadrature or sign tests.
Default prints deterministic JSON; --check compares with EXPECTED.json.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def norm2(a):
    return dot(a, a)


def cross(a, b):
    return a[0]*b[1]-a[1]*b[0]


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1)**j*a[0][j]*det([r[:j]+r[j+1:] for r in a[1:]])
               for j in range(len(a)))


def rank(a):
    a = [list(map(F, row)) for row in a]
    k = 0
    for j in range(len(a[0])):
        pivot = next((i for i in range(k, len(a)) if a[i][j]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        v = a[k][j]
        a[k] = [x/v for x in a[k]]
        for i in range(k+1, len(a)):
            v = a[i][j]
            a[i] = [x-v*y for x, y in zip(a[i], a[k])]
        k += 1
        if k == len(a):
            break
    return k


def hull(points):
    points = sorted(set(points))

    def half(seq):
        ans = []
        for p in seq:
            while len(ans) >= 2 and cross(sub(ans[-1], ans[-2]), sub(p, ans[-1])) <= 0:
                ans.pop()
            ans.append(p)
        return ans

    return half(points)[:-1]+half(reversed(points))[:-1]


def polar_vertices(points):
    ans = set()
    for u, v in combinations(points, 2):
        d = cross(u, v)
        if not d:
            continue
        z = ((v[1]-u[1])/d, (u[0]-v[0])/d)
        if all(dot(z, p) <= 1 for p in points):
            ans.add(z)
    return hull(ans)


NAMES = ('C', 'S', 'c', 'd', 'eta', 't', 'r',
         'ax', 'ay', 'az', 'bx', 'by', 'bz', 'U', 'V')
N = len(NAMES)


class Poly:
    def __init__(self, terms=None):
        self.terms = {m: F(v) for m, v in (terms or {}).items() if v}

    @staticmethod
    def const(v):
        return Poly({(0,)*N: v})

    @staticmethod
    def var(i):
        m = [0]*N
        m[i] = 1
        return Poly({tuple(m): 1})

    def __add__(self, other):
        if not isinstance(other, Poly):
            other = Poly.const(other)
        terms = dict(self.terms)
        for m, v in other.terms.items():
            terms[m] = terms.get(m, F(0))+v
        return Poly(terms)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -v for m, v in self.terms.items()})

    def __sub__(self, other):
        return self + (-other if isinstance(other, Poly) else -F(other))

    def __rsub__(self, other):
        return -self+other

    def __mul__(self, other):
        if not isinstance(other, Poly):
            other = Poly.const(other)
        terms = {}
        for m, v in self.terms.items():
            for k, w in other.terms.items():
                e = tuple(x+y for x, y in zip(m, k))
                terms[e] = terms.get(e, F(0))+v*w
        return Poly(terms)

    __rmul__ = __mul__

    def sq(self):
        return self*self

    def reduced(self):
        terms = {}

        def expand(m, v):
            for i, j in ((1, 0), (3, 2), (5, 4)):
                if m[i] >= 2:
                    e = list(m)
                    e[i] -= 2
                    expand(tuple(e), v)
                    e[j] += 2
                    expand(tuple(e), -v)
                    return
            terms[m] = terms.get(m, F(0))+v

        for m, v in self.terms.items():
            expand(m, v)
        return Poly(terms)

    def record(self):
        return [[list(m), str(v)] for m, v in sorted(self.terms.items())]


def polynomial_audit():
    C, S, c, d, eta, t, r, ax, ay, az, bx, by, bz, U, V = [Poly.var(i) for i in range(N)]
    zero = Poly.const(0)
    a, b = (ax, ay, az), (bx, by, bz)
    G = (r*ax, r*ay, az, zero)
    H = (r*(C*bx-S*by), r*(S*bx+C*by), c*bz, d*bz)
    transverse = ax*(C*bx-S*by)+ay*(S*bx+C*by)
    complex_real, complex_imag = ax*bx+ay*by, ax*by-ay*bx
    z = (-eta.sq(), eta*t)
    identities = {
        'fixed_metric': norm2(G)-(r.sq()*(ax.sq()+ay.sq())+az.sq()),
        'moving_metric': norm2(H)-(r.sq()*(bx.sq()+by.sq())+bz.sq()),
        'cross_distance': norm2(sub(G, H))-(r.sq()*(ax.sq()+ay.sq()+bx.sq()+by.sq())
                            +az.sq()+bz.sq()-2*(r.sq()*transverse+c*az*bz)),
        'complex_product_norm': complex_real.sq()+complex_imag.sq()
                             -(ax.sq()+ay.sq())*(bx.sq()+by.sq()),
        'AM_GM_remainder': (az*U-bz*V).sq()
                          -(az.sq()*U.sq()+bz.sq()*V.sq()-2*az*bz*U*V),
        'tangent_radius': norm2(z)-eta.sq(),
        'tangent_orthogonality': dot(z, sub((-1, zero), z)),
        'tangent_length': norm2(sub((-1, zero), z))-(1-eta.sq()),
        'calibration_unit_gradient_numerator': (r.sq()-eta.sq())+eta.sq()-r.sq(),
        'scalar_defect_sum': norm2(sub(a, tuple(r*x for x in b)))
                          +norm2(tuple(x+r*y for x, y in zip(a, b)))
                          -2*norm2(a)-2*r.sq()*norm2(b),
    }
    for name, poly in identities.items():
        require(not poly.reduced().terms, 'identity: '+name)
    bad = norm2((r*(C*bx-S*by), r*(S*bx+C*by), c*bz, 2*d*bz))
    bad -= r.sq()*(bx.sq()+by.sq())+bz.sq()
    require(bool(bad.reduced().terms), 'bad auxiliary scale not rejected')
    records = {k: p.record() for k, p in sorted(identities.items())}
    digest = sha256(json.dumps(records, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return {'count': len(identities), 'names': sorted(identities), 'expanded_sha256': digest}


def constants_audit():
    eta = F(16, 25)
    t = F(7, 8)
    cosine_lower = 1-t*t/2+t**4/24-t**6/720
    require(cosine_lower > eta, 'cosine lower polynomial')
    require(F(77, 100)**2 > 1-eta*eta, 'square root bound')
    require(F(19, 18)**2 > F(10, 9), 'kappa upper bound')
    upper = F(77, 100)+eta*(F(22, 7)-t)+eta-1
    require(upper == F(1303, 700), 'cost bound')
    margin = 2-F(19, 18)*upper
    require(margin == F(443, 12600) and margin > 0, 'motion margin')
    require(F(25, 24)**2 < F(10, 9), 'kappa lower bound')
    require(3*F(25, 24)*eta == 2, 'prior squeeze obstruction')
    selfdual_upper = F(3, 4)+F(11, 7)-F(1, 3)
    require(selfdual_upper == 2-F(1, 84), 'selfdual cost bound')
    require(F(9, 4)**2 > 5 and F(2, 3)**2 < F(1, 2), 'selfdual roots')
    # x^4(1-x)^4 = (1+x^2)(x^6-4x^5+5x^4-4x^2+4) - 4.
    numerator = [F(0)]*9
    for i, v in enumerate((1, -4, 6, -4, 1)):
        numerator[4+i] = F(v)
    quotient = [F(4), F(0), F(-4), F(0), F(5), F(-4), F(1)]
    product = [F(0)]*9
    for i, v in enumerate(quotient):
        product[i] += v
        product[i+2] += v
    product[0] -= 4
    require(product == numerator, 'pi polynomial division')
    require(sum(v/F(i+1) for i, v in enumerate(quotient)) == F(22, 7), 'pi integration')
    # Deliberately inadequate Taylor truncation must not certify this bound.
    require(1-t*t/2 <= eta, 'invalid Taylor control unexpectedly passes')
    return {'eta': str(eta), 'cosine_margin': str(cosine_lower-eta),
            'F_upper': str(upper), 'motion_margin': str(margin),
            'selfdual_cost_margin': '1/84', 'pi_integral_identity': True}


def fixture_audit():
    directions = [(1, 0), (F(4, 5), F(3, 5)), (F(3, 5), F(4, 5)), (0, 1),
                  (-F(3, 5), F(4, 5)), (-F(4, 5), F(3, 5)), (-1, 0),
                  (-F(4, 5), -F(3, 5)), (-F(3, 5), -F(4, 5)), (0, -1),
                  (F(3, 5), -F(4, 5)), (F(4, 5), -F(3, 5))]
    P = [tuple(map(F, p)) for p in directions]
    require(all(norm2(p) == 1 for p in P), 'unit directions')
    require(len(hull(P)) == 12, 'nonextreme P generator')
    Q = polar_vertices(P)
    expected_q = set()
    for p in [(F(1), F(1, 3)), (F(5, 7), F(5, 7)), (F(1, 3), F(1))]:
        for _ in range(4):
            expected_q.add(p)
            p = (-p[1], p[0])
    require(set(Q) == expected_q, 'dual polygon mismatch')
    require(set(polar_vertices(Q)) == set(P), 'reverse polar mismatch')
    require(max(map(norm2, Q)) == F(10, 9), 'circular slope')
    require(all(dot(p, q) >= -1 for p in P for q in Q), 'positive cone duality')
    facets = []
    for p in P:
        tight = [q for q in Q if dot(p, q) == 1]
        require(len(tight) == 2, 'missing or redundant facet')
        facets.append([list(map(str, p)), [list(map(str, q)) for q in tight]])
    A = [p+(F(1),) for p in P]
    B = [q+(F(1),) for q in Q]
    for cluster, height in ((A, F(1)), (B, F(2))):
        for i in range(3):
            for sign in (-1, 1):
                z = [F(0), F(0), height]
                z[i] += F(sign, 4)
                cluster.append(tuple(z))
    require(all(a[2] > 0 and norm2(a[:2]) <= a[2]**2 for a in A), 'A cone membership')
    require(all(b[2] > 0 and 9*norm2(b[:2]) <= 10*b[2]**2 for b in B), 'B cone membership')
    require(all(dot(a, b) >= 0 for a in A for b in B), 'dual positive products')
    lam = F(4, 5)
    zero = (F(0),)*3
    X = [zero]+A+[tuple(-v for v in b) for b in B]
    Y = [zero]+[tuple(lam*v for v in a) for a in A+B]
    require(len(X) == 37 and len(set(X)) == len(set(Y)) == 37, 'distinct endpoint sites')
    deficits = [norm2(sub(X[i], X[j]))-norm2(sub(Y[i], Y[j]))
                for i, j in combinations(range(37), 2)]
    require(len(deficits) == 666 and min(deficits) > 0, 'pairwise strict contraction')
    paired = [x+y for x, y in zip(X, Y)]
    require(rank(paired) == 6, 'paired rank')
    a3 = [(F(1), F(0), F(1)), (F(0), F(1), F(1)), (-F(1), F(0), F(1))]
    b3 = [(F(1), F(1, 3), F(1)), (F(1, 3), F(1), F(1)), (-F(1), -F(1, 3), F(1))]
    rows = [a+tuple(lam*v for v in a) for a in a3]
    rows += [tuple(-v for v in b)+tuple(lam*v for v in b) for b in b3]
    minor = abs(det(rows))
    require(minor == F(16384, 1125), 'six-row minor')
    require(minor == (2*lam)**3*abs(det(a3))*abs(det(b3)), 'block determinant factorization')
    scalar_gap = 2*(1+lam*lam)-6*(1-lam*lam)
    require(scalar_gap == F(28, 25) and scalar_gap > 0, 'scalar-defect exclusion')
    # Every four extreme ray triples must be independent: a check of the
    # geometric input to the scalar-operator argument, not a sampled motion.
    b0 = [q+(F(1),) for q in Q]
    minors3 = [det(list(triple)) for triple in combinations(b0, 3)]
    require(len(minors3) == 220 and all(minors3), 'dependent extreme-ray triple')
    fixture = {'lambda': str(lam), 'source': [list(map(str, x)) for x in X],
               'target': [list(map(str, y)) for y in Y], 'facets': facets}
    digest = sha256(json.dumps(fixture, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    # Mutation and boundary controls: violating polar inequalities and an
    # expansion of a within-cluster pair are detected by direct definitions.
    require(any(dot(P[0], (2*q[0], 2*q[1])) > 1 for q in Q), 'bad polar mutation')
    require(norm2(sub(A[0], A[1]))-F(11, 10)**2*norm2(sub(A[0], A[1])) < 0,
            'expanding scale mutation')
    return {'sites': 37, 'pairs': len(deficits), 'strict_pairs': len(deficits),
            'min_squared_deficit': str(min(deficits)), 'max_squared_deficit': str(max(deficits)),
            'paired_rank': 6, 'paired_minor_abs': str(minor),
            'dual_vertices': len(Q), 'dual_facets': len(facets),
            'independent_extreme_triples': len(minors3),
            'scalar_defect_gap': str(scalar_gap), 'fixture_sha256': digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    record = {'schema': 1, 'polynomials': polynomial_audit(),
              'constants': constants_audit(), 'fixture': fixture_audit(),
              'invalid_controls_rejected': 4,
              'scope': 'Supplementary exact audits; see PROOF.md for universal claims.'}
    rendered = json.dumps(record, sort_keys=True, indent=2)+'\n'
    if args.check:
        expected = Path(__file__).with_name('EXPECTED.json').read_text()
        require(rendered == expected, 'EXPECTED.json mismatch')
        print('DAMPED_CONE_EXACT_AUDITS_PASS '+sha256(rendered.encode()).hexdigest())
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
