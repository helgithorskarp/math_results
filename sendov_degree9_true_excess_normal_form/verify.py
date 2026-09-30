#!/usr/bin/env python3
"""Exact all-coordinate block algebra for the fine degree-nine excess normal form.

Actual author six-sendov-3, researcher. Python 3.11 standard library.
The sparse polynomial kernel is openly adapted from this author's fixed-rectangle checker. All six independent split coordinates are symbolic. This checks polynomial identities,
not analytic uniformity, the IFT, global entry, or disk-root enumeration.
No campaign module, external package, floating point, or solver is used.
"""
from fractions import Fraction as Q
from hashlib import sha256
from pathlib import Path
import json
import sys


class Poly:
    """Sparse rational Laurent polynomials; only v has negative powers."""
    def __init__(self, terms=None):
        self.terms = {m: Q(c) for m, c in (terms or {}).items() if c}

    def __add__(self, other):
        other = polynomial(other)
        out = dict(self.terms)
        for m, c in other.terms.items():
            out[m] = out.get(m, Q()) + c
        return Poly(out)

    __radd__ = __add__

    def __neg__(self):
        return Poly({m: -c for m, c in self.terms.items()})

    def __sub__(self, other):
        return self + -polynomial(other)

    def __rsub__(self, other):
        return polynomial(other) + -self

    def __mul__(self, other):
        other = polynomial(other)
        out = {}
        for m, c in self.terms.items():
            for n, d in other.terms.items():
                powers = dict(m)
                for name, exponent in n:
                    powers[name] = powers.get(name, 0) + exponent
                key = tuple(sorted((s, e) for s, e in powers.items() if e))
                out[key] = out.get(key, Q()) + c * d
        return Poly(out)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if not isinstance(other, (int, Q)) or not other:
            raise ValueError('only nonzero rational scalar division')
        return Poly({m: c / other for m, c in self.terms.items()})

    def __pow__(self, power):
        if not isinstance(power, int) or power < 0:
            raise ValueError('nonnegative integer power required')
        out = polynomial(1)
        for _ in range(power):
            out = out * self
        return out

    def __eq__(self, other):
        return self.terms == polynomial(other).terms

    def derivative(self, name):
        out = {}
        for m, c in self.terms.items():
            powers = dict(m)
            exponent = powers.get(name, 0)
            if exponent:
                powers[name] = exponent - 1
                key = tuple(sorted((s, e) for s, e in powers.items() if e))
                out[key] = out.get(key, Q()) + exponent * c
        return Poly(out)

    def truncate(self, name, maximum):
        return Poly({m: c for m, c in self.terms.items()
                     if dict(m).get(name, 0) <= maximum})

    def substitute(self, values):
        out = polynomial(0)
        for m, c in self.terms.items():
            term = polynomial(c)
            for name, exponent in m:
                if name in values:
                    value = values[name]
                    if exponent < 0:
                        if not isinstance(value, (int, Q)) or not value:
                            raise ValueError('negative power needs rational value')
                        term *= Q(value) ** exponent
                    else:
                        term *= polynomial(value) ** exponent
                else:
                    term *= monomial(name, exponent)
            out += term
        return out


def polynomial(value):
    return value if isinstance(value, Poly) else Poly({(): Q(value)})


def monomial(name, exponent=1):
    if exponent < 0 and name != 'v':
        raise ValueError('only v is a Laurent variable')
    return Poly({((name, exponent),): Q(1)}) if exponent else polynomial(1)


def matmul(a, b):
    if not a or not b or len(a[0]) != len(b):
        raise ValueError('matrix dimensions')
    return [[sum((a[i][k] * b[k][j] for k in range(len(b))), Q())
             for j in range(len(b[0]))] for i in range(len(a))]


def trace(a):
    return sum((a[i][i] for i in range(len(a))), Q())


def encode(value):
    if isinstance(value, Poly):
        return {'terms': [[[[name, exponent] for name, exponent in m],
                           [c.numerator, c.denominator]]
                          for m, c in sorted(value.terms.items())]}
    if isinstance(value, Q):
        return [value.numerator, value.denominator]
    if isinstance(value, (tuple, list)):
        return [encode(x) for x in value]
    if isinstance(value, dict):
        return {k: encode(v) for k, v in value.items()}
    return value


RECORDS = []
CONTROLS = []


def require(name, actual, expected):
    if actual != expected:
        raise RuntimeError('exact identity failed: ' + name)
    RECORDS.append({'name': name, 'value': encode(actual)})


def reject(name, actual, false_expected):
    if actual == false_expected:
        raise RuntimeError('corruption control failed: ' + name)
    CONTROLS.append(name)


def mplus(a, b):
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def mscale(a, value):
    return [[x * value for x in row] for row in a]


def mminus(a, b):
    return mplus(a, mscale(b, -1))


def mtrunc(a, order):
    return [[polynomial(x).truncate('t', order) for x in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def zeros(rows, cols):
    return [[polynomial(0) for _ in range(cols)] for _ in range(rows)]


def diagonal(values):
    return [[values[i] if i == j else polynomial(0) for j in range(len(values))]
            for i in range(len(values))]


def residual(name, actual, expected):
    value = mminus(actual, expected)
    require(name, value, zeros(len(value), len(value[0])))


def fixture():
    t, v, c0, c1, y, ua, ub = [monomial(n) for n in ('t', 'v', 'c0', 'c1', 'y', 'uA', 'uB')]
    x = [monomial('x' + str(j)) for j in range(6)]
    x.append(-sum(x, polynomial(0)))
    S = sum((z ** 2 for z in x), polynomial(0))
    m = y + S / 112
    singleton_shift = y - S / 16
    q = [[Q(int(i == j)) - Q(1, 7) for j in range(7)] for i in range(7)]
    pb = [[Q() for _ in range(8)] for _ in range(8)]
    for i in range(7):
        for j in range(7):
            pb[i + 1][j + 1] = q[i][j]
    j8 = [[Q(int(i == j)) + 1 for j in range(8)] for i in range(8)]
    n = [[Q(7)]] + [[Q(-1)]] * 7
    f = [[Q(1)]] * 8
    nleft = mscale(transpose(n), Q(1, 56))
    fleft = mscale(transpose(f), Q(1, 8))
    embed = [[Q()] * 7] + q
    complement = [[n[i][0], f[i][0]] for i in range(8)]
    dual = nleft + fleft
    full_baseline = matmul(diagonal([ua] + [ub] * 7), j8)

    residual('fixed repeated-root projector is idempotent', matmul(pb, pb), pb)
    residual('left exact repeated-root scalar eigenspace', matmul(pb, full_baseline), mscale(pb, ub))
    residual('right exact repeated-root scalar eigenspace', matmul(full_baseline, pb), mscale(pb, ub))
    require('rational complementary basis metric', matmul(transpose(complement), complement),
            [[Q(56), Q()], [Q(), Q(8)]])
    require('rational complementary dual basis', matmul(dual, complement),
            [[Q(1), Q()], [Q(), Q(1)]])
    residual('full repeated/complementary decomposition',
             mplus(pb, matmul(complement, dual)), [[Q(int(i == j)) for j in range(8)] for i in range(8)])
    cbase = matmul(matmul(dual, full_baseline), complement)
    residual('entire exact two-dimensional baseline block', cbase,
             [[(7 * ua + ub) / 8, 9 * (ua - ub) / 8],
              [7 * (ua - ub) / 8, 9 * (ua + 7 * ub) / 8]])

    # The baseline first jet is uA=v+7c0t and uB=v-c0t. Higher terms
    # cannot affect the divided Riccati equations at their t=0 limit.
    base_jet = matmul(diagonal([v + 7 * c0 * t] + [v - c0 * t] * 7), j8)
    uj = v - c0 * t
    cj = matmul(matmul(dual, base_jet), complement)
    residual('baseline complementary minus cluster first jet',
             mminus(cj, diagonal([uj, uj])),
             [[7 * c0 * t, 9 * c0 * t], [7 * c0 * t, 8 * v + c0 * t]])
    require('nonzero divided Riccati Jacobian determinant polynomial',
            7 * c0 * 8 * v, 56 * c0 * v)

    # Every independent split variable is retained. c1 is arbitrary:
    # cancellation below therefore covers the actual complex tangent c(t).
    tangent = c0 + c1 * t
    du = [c0 * t ** 3 * singleton_shift]
    du.extend(c0 * t ** 2 * z + t ** 3 * (c1 * z + c0 * m) for z in x)
    dn = matmul(diagonal(du), j8)
    da = [row[1:] for row in matmul(matmul(pb, dn), pb)[1:]]
    db = [row for row in matmul(matmul(pb, dn), complement)[1:]]
    dd = matmul(matmul(dual, dn), embed)
    dc = matmul(matmul(dual, dn), complement)
    X = matmul(matmul(q, diagonal(x)), q)
    xx = [[a * b for b in x] for a in x]
    residual('full fine repeated-block original-root jet', da,
             mplus(mscale(X, tangent * t ** 2), mscale(q, c0 * m * t ** 3)))
    residual('leading near and far forward coupling, all splits', mtrunc(db, 2),
             [[-c0 * t ** 2 * z, 9 * c0 * t ** 2 * z] for z in x])
    residual('leading near and far backward coupling, all splits', mtrunc(dd, 2),
             [[-c0 * t ** 2 * z / 56 for z in x], [c0 * t ** 2 * z / 8 for z in x]])
    require('full fixed-energy amplitude and mean shifts',
            7 * (-(S / 112)) + y, singleton_shift)

    # K_n=t*x^T/392 and K_f=-t^2*c0*x^T/(56v). The second row differs
    # from a diagonalized complementary basis because the fixed rational
    # basis retains the baseline n-to-f coupling 7c0t. It affects no t^3
    # normalized six-block coefficient, but is required by the Riccati IFT.
    K = [[t * z / 392 for z in x],
         [-t ** 2 * c0 * monomial('v', -1) * z / 56 for z in x]]
    A = mplus(mscale(q, uj), da)
    C = mplus(cj, dc)
    riccati = mminus(mplus(dd, matmul(C, K)), mplus(matmul(K, A), matmul(matmul(K, db), K)))
    residual('both full divided Riccati leading equations', mtrunc(riccati, 2), zeros(2, 7))
    require('fixed-basis near graph first coefficient',
            [polynomial(z).derivative('t').substitute({'t': 0}) for z in K[0]],
            [z / 392 for z in x])
    # A graph matrix acts on the natural Euclidean balanced seven-root
    # space. The normalization is checked by cross multiplication; no
    # numeric complex division or sampled eigenvector is used.
    R3 = mminus(mscale(q, m), mscale(xx, Q(1, 392)))
    Wjet = mplus(mscale(X, t ** 2), mscale(R3, t ** 3))
    effective_shift = mplus(da, matmul(db, K))
    residual('complete normalized six-block matrix through degree three',
             mtrunc(effective_shift, 3), mtrunc(mscale(Wjet, tangent), 3))
    residual('entire second-degree coefficient is symmetric', X, transpose(X))
    residual('entire third-degree coefficient is symmetric', R3, transpose(R3))
    residual('both coefficients preserve the balanced split space',
             matmul(mplus(X, R3), [[Q(1)]] * 7), zeros(7, 1))
    require('independent degree-three normalized cluster trace', trace(R3), 6 * y + Q(5, 98) * S)
    require('cluster plus separated-near degree-three trace consistency',
            trace(R3) + y - Q(5, 98) * S, 7 * y)
    require('angular second coefficient has no complementary tangent symbols',
            sorted({name for term in X for item in term for m0 in item.terms for name, _ in m0}),
            ['x' + str(j) for j in range(6)])
    require('angular third coefficient is real in all independent coordinates',
            sorted({name for row in R3 for item in row for m0 in item.terms for name, _ in m0}),
            ['x' + str(j) for j in range(6)] + ['y'])

    false_R3 = mscale(q, m)
    reject('omit shrinking-gap rank-one feedback', mtrunc(effective_shift, 3),
           mtrunc(mscale(mplus(mscale(X, t ** 2), mscale(false_R3, t ** 3)), tangent), 3))
    false_K = [K[0], [-t ** 2 * c0 * monomial('v', -1) * z / 64 for z in x]]
    wrong = mminus(mplus(dd, matmul(C, false_K)),
                   mplus(matmul(false_K, A), matmul(matmul(false_K, db), false_K)))
    reject('ignore fixed complementary n-to-f coupling', mtrunc(wrong, 2), zeros(2, 7))
    reject('replace full fixed-energy elimination by fixed amplitude', m,
           y)
    reject('incorrect reciprocal tangent normalization', mtrunc(effective_shift, 3), mtrunc(mscale(Wjet, c0), 3))
    asym = zeros(7, 7)
    asym[0][1] = polynomial(1)
    asym[1][0] = polynomial(-1)
    asym = matmul(matmul(q, asym), q)
    reject('real antisymmetric coefficient is Hermitian', mplus(R3, asym), transpose(mplus(R3, asym)))
    digest = sha256(json.dumps(RECORDS, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    reject('altered complete exact record digest', digest, '0' * 64)
    return {'schema': 1, 'agent': 'six-sendov-3', 'role': 'researcher',
            'arithmetic': 'exact rational multivariate Laurent polynomial matrix identities',
            'claim_status': 'universal block coefficients; uniform analytic and completeness arguments separate',
            'independent_split_coordinates': 6, 'matrix_ambient_dimension': 8,
            'identity_count': len(RECORDS), 'corruption_control_count': len(CONTROLS),
            'corruption_controls': CONTROLS, 'records_sha256': digest, 'complete_records': RECORDS}


def main():
    if sys.argv[1:] not in ([], ['--emit-fixture']):
        raise SystemExit('usage: python3 -I -B verify.py [--emit-fixture]')
    path = Path(__file__).with_name('expected.json')
    if sys.argv[1:] != ['--emit-fixture']:
        try:
            expected = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            raise RuntimeError('required expected.json absent or malformed') from exc
    result = fixture()
    if sys.argv[1:] == ['--emit-fixture']:
        path.write_text(json.dumps(result, indent=2) + '\n')
    elif expected != result:
        raise RuntimeError('complete exact fixture differs')
    print(json.dumps({k: v for k, v in result.items() if k != 'complete_records'}, sort_keys=True))


if __name__ == '__main__':
    main()
