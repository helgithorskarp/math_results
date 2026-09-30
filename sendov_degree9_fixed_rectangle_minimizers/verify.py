#!/usr/bin/env python3
"""Universal exact algebra for the coarse degree-nine minimizer chart.

Actual author six-sendov-3, researcher. Python 3.11 standard library.
All phase coordinates are symbolic. This checks polynomial identities,
not analytic uniformity, the IFT, global entry, or disk-root enumeration.
No campaign module, external package, floating point, or solver is used.
"""
from fractions import Fraction as Q
from hashlib import sha256
from math import comb
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


def fixture():
    v = monomial('v')
    phi = [monomial('phi' + str(j)) for j in range(8)]
    p = [[Q(int(i == j)) - Q(1, 8) for j in range(8)] for i in range(8)]
    require('collapse projection idempotence', matmul(p, p), p)
    require('collapse projection balanced kernel', matmul(p, [[1]] * 8), [[Q()]] * 8)
    diag = [[phi[i] if i == j else polynomial(0) for j in range(8)]
            for i in range(8)]
    b = matmul(matmul(p, diag), p)
    mean = sum(phi, polynomial(0)) / 8
    square_sum = sum((x ** 2 for x in phi), polynomial(0))
    require('all-coordinate near first trace', trace(b), 7 * mean)
    require('all-coordinate compressed second trace', trace(matmul(b, b)),
            Q(3, 4) * square_sum + mean ** 2)
    total_imag = -2 * v ** 2 * sum(phi, polynomial(0))
    near_imag = -v ** 2 * trace(b)
    require('all-coordinate far first imaginary shift', total_imag - near_imag,
            -9 * v ** 2 * mean)

    real_trace = (v ** 2 - 2 * v ** 3) * square_sum
    near_norm = v ** 3 * trace(matmul(b, b)) / 2
    far_norm = Q(9, 2) * v ** 3 * mean ** 2
    kappa = monomial('v', -2) - Q(13, 8) * monomial('v', -1)
    expected_quadratic = kappa * v ** 4 * square_sum + 5 * v ** 3 * mean ** 2
    require('universal original-circle quadratic objective',
            real_trace + near_norm + far_norm, expected_quadratic)
    require('quadratic energy coefficient normalization',
            kappa * v ** 4, v ** 2 - Q(13, 8) * v ** 3)

    # All six independent balanced split coordinates, not a profile fit.
    h = [monomial('h' + str(j)) for j in range(6)]
    h.append(-sum(h, polynomial(0)))
    T, M, s = [monomial(name) for name in ('T', 'M', 's')]
    phases = [7 * T + M] + [-T + M + x for x in h]
    split_square = sum((x ** 2 for x in h), polynomial(0))
    require('full seven-root balanced split', sum(h, polynomial(0)), polynomial(0))
    require('full chart phase mean', sum(phases, polynomial(0)), 8 * M)
    require('full chart phase squared norm',
            sum((x ** 2 for x in phases), polynomial(0)),
            56 * T ** 2 + 8 * M ** 2 + split_square)
    theta = [7 * s] + [-s + x for x in h]
    require('all-coordinate leading coarse energy norm',
            sum((x ** 2 for x in theta), polynomial(0)),
            56 * s ** 2 + split_square)
    require('leading coarse energy IFT derivative',
            (v ** 4 * (56 * s ** 2 + split_square)).derivative('s'),
            112 * v ** 4 * s)

    # Exact base eigenvectors: simple six, sixfold minus one, plus zero.
    th = [Q(7)] + [Q(-1)] * 7
    d0 = [[th[i] if i == j else Q() for j in range(8)] for i in range(8)]
    b0 = matmul(matmul(p, d0), p)
    require('divided single near base eigenvector', matmul(b0, [[x] for x in th]),
            [[6 * x] for x in th])
    balanced = [[Q(int(i == j + 1)) - Q(int(i == 7)) for j in range(6)]
                for i in range(8)]
    require('entire six-group base eigenspace', matmul(b0, balanced),
            [[-x for x in row] for row in balanced])
    require('fixed divided single-six gap', Q(6) - Q(-1), Q(7))

    # f0 = v sqrt(1+v^2 w^2) - i v asinh(v w), through degree seven.
    w = monomial('w')
    real_f, imag_f, root = polynomial(0), polynomial(0), polynomial(0)
    binomial = Q(1)
    for k in range(4):
        real_f += binomial * v ** (2 * k + 1) * w ** (2 * k)
        root += binomial * v ** (2 * k) * w ** (2 * k)
        imag_f -= Q((-1) ** k * comb(2 * k, k), 4 ** k * (2 * k + 1)) * v ** (2 * k + 2) * w ** (2 * k + 1)
        binomial *= (Q(1, 2) - k) / (k + 1)
    require('collapsed primitive derivative real polynomial',
            (real_f.derivative('w') * root).truncate('w', 6), v ** 3 * w)
    require('collapsed primitive derivative imaginary polynomial',
            (imag_f.derivative('w') * root).truncate('w', 6), -v ** 2)
    require('collapsed primitive even real parity',
            real_f.substitute({'w': -w}), real_f)
    require('collapsed primitive odd imaginary parity',
            imag_f.substitute({'w': -w}), -imag_f)
    require('collapsed primitive constant and quadratic real jet',
            real_f.truncate('w', 2), v + v ** 3 * w ** 2 / 2)

    # Circle energy |u-v|^2: direct jet multiplication of u-v.
    phase = monomial('q')
    re_u_minus_v = (v ** 2 / 2 - v ** 3) * phase ** 2
    im_u_minus_v = -v ** 2 * phase + (v ** 2 / 6 - v ** 3 + v ** 4) * phase ** 3
    require('exact circle energy quadratic jet',
            (re_u_minus_v ** 2 + im_u_minus_v ** 2).truncate('q', 2),
            v ** 4 * phase ** 2)
    require('exact circle energy fourth jet',
            (re_u_minus_v ** 2 + im_u_minus_v ** 2).truncate('q', 4),
            v ** 4 * phase ** 2 + v ** 4 * (v - v ** 2 - Q(1, 12)) * phase ** 4)

    d = monomial('v', -1)
    delta = d - Q(13, 8)
    ktr = d ** 3 * (3792 * d ** 2 - 7728 * d + 2991) / 28672
    k1 = d ** 3 * (516 * d ** 2 - 528 * d - 393) / 7168
    require('retained minus stationary branch coefficient, all marked radii',
            ktr - k1, Q(27, 448) * d ** 3 * delta ** 2)
    values = {'v': Q(8, 13)}
    require('positive stationary quartic coefficient at cutoff',
            k1.substitute(values), polynomial(Q(560235, 8388608)))
    require('positive retained quartic coefficient at cutoff',
            ktr.substitute(values), polynomial(Q(560235, 8388608)))
    aa = d - 1
    L = (1616 * aa ** 2 + 1800 * aa - 1675) * v ** 5 / 224
    require('positive coarse split coefficient at cutoff',
            L.substitute(values), polynomial(Q(6400, 199927)))
    require('positive coarse mean coefficient at cutoff',
            (5 * v ** 3).substitute(values), polynomial(Q(2560, 2197)))
    require('positive coarse inward coefficient at cutoff',
            (2 * v ** 2).substitute(values), polynomial(Q(128, 169)))

    reject('omit universal mean cost', real_trace + near_norm + far_norm,
           kappa * v ** 4 * square_sum)
    reject('incorrect uncompressed second trace', trace(matmul(b, b)), square_sum)
    reject('omit balanced split from exact energy', sum((x ** 2 for x in phases), polynomial(0)),
           56 * T ** 2 + 8 * M ** 2)
    reject('replace divided simple near eigenvalue by cluster eigenvalue',
           matmul(b0, [[x] for x in th]), [[-x] for x in th])
    reject('omit radius-dependent retained correction', ktr - k1, polynomial(0))
    reject('incorrect primitive imaginary parity', imag_f.substitute({'w': -w}), imag_f)
    digest = sha256(json.dumps(RECORDS, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    reject('altered complete record digest', digest, '0' * 64)
    return {'schema': 1, 'agent': 'six-sendov-3', 'role': 'researcher',
            'arithmetic': 'exact rational multivariate Laurent polynomials and matrices',
            'claim_status': 'universal coefficient identities; written analytic and completeness proof separate',
            'phase_coordinates': 8, 'independent_split_coordinates': 6,
            'identity_count': len(RECORDS), 'corruption_control_count': len(CONTROLS),
            'corruption_controls': CONTROLS, 'records_sha256': digest,
            'complete_records': RECORDS}


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
