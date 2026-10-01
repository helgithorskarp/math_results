#!/usr/bin/env python3
"""Exact moving-pair angular Hessian certificate; analytic proof is separate.

Actual author six-sendov-3, role researcher. CPython standard library only.
Sparse Fraction arithmetic is self-contained. The angular functional,
critical matrix and actual-family cubic retain the named parent credit.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from pathlib import Path

NAMES = ('a', 'v', 'z', 'b', 'q', 'y', 'h', 'j', 'w', 'x')
ZERO = (0,) * len(NAMES)
checks, signs, damages = [], [], []
records = {}

class P:
    def __init__(self, terms=0):
        if isinstance(terms, P):
            terms = terms.d
        elif isinstance(terms, (int, F)):
            terms = {ZERO: F(terms)}
        self.d = {k: F(c) for k, c in terms.items() if c}
    def __add__(self, other):
        other = P(other)
        result = dict(self.d)
        for key, value in other.d.items():
            result[key] = result.get(key, F(0)) + value
        return P(result)
    __radd__ = __add__
    def __neg__(self):
        return P({key: -value for key, value in self.d.items()})
    def __sub__(self, other):
        return self + -P(other)
    def __rsub__(self, other):
        return P(other) + -self
    def __mul__(self, other):
        other = P(other)
        result = {}
        for key, value in self.d.items():
            for other_key, other_value in other.d.items():
                target = tuple(a + b for a, b in zip(key, other_key))
                result[target] = result.get(target, F(0)) + value * other_value
        return P(result)
    __rmul__ = __mul__
    def __pow__(self, exponent):
        if not isinstance(exponent, int) or exponent < 0:
            raise ValueError('nonnegative integer polynomial power required')
        result = P(1)
        for _ in range(exponent):
            result = result * self
        return result
    def __truediv__(self, other):
        if not isinstance(other, (int, F)) or not other:
            raise ValueError('only nonzero rational scalar division')
        return P({key: value / other for key, value in self.d.items()})
    def coefficient(self, name, exponent):
        index = NAMES.index(name)
        result = {}
        for key, value in self.d.items():
            if key[index] == exponent:
                target = key[:index] + (0,) + key[index + 1:]
                result[target] = value
        return P(result)
    def derivative(self, name):
        index = NAMES.index(name)
        return P({key[:index] + (key[index] - 1,) + key[index + 1:]:
                  value * key[index] for key, value in self.d.items() if key[index]})
    def degree(self, name):
        index = NAMES.index(name)
        return max((key[index] for key in self.d), default=-1)
    def substitute(self, name, replacement):
        index = NAMES.index(name)
        replacement = P(replacement)
        out = P()
        for key, value in self.d.items():
            reduced = key[:index] + (0,) + key[index + 1:]
            out += P({reduced: value}) * replacement ** key[index]
        return out
    def value(self, **values):
        out = self
        for name, value in values.items():
            out = out.substitute(name, F(value))
        if out.d and set(out.d) != {ZERO}:
            raise RuntimeError('unevaluated variable in scalar value')
        return out.d.get(ZERO, F(0))
    def wire(self):
        return {'terms': [
            [[[name, degree] for name, degree in zip(NAMES, key) if degree],
             [value.numerator, value.denominator]]
            for key, value in sorted(self.d.items())]}

def var(name):
    key = list(ZERO)
    key[NAMES.index(name)] = 1
    return P({tuple(key): F(1)})

def equal(name, actual, expected):
    difference = P(actual) - expected
    if difference.d:
        raise RuntimeError(name + ': ' + json.dumps(difference.wire()))
    checks.append(name)

def damaged(name, actual, wrong):
    difference = P(actual) - wrong
    if not difference.d:
        raise RuntimeError('Damaged mathematical expression accepted: ' + name)
    damages.append(name)
    record('rejected ' + name, difference)

def wire(item):
    if isinstance(item, P):
        return item.wire()
    if isinstance(item, F):
        return [item.numerator, item.denominator]
    if isinstance(item, (str, int)):
        return item
    if isinstance(item, (tuple, list)):
        return [wire(x) for x in item]
    if isinstance(item, dict):
        return {str(key): wire(value) for key, value in sorted(item.items())}
    raise TypeError(type(item).__name__)

def record(name, value):
    if name in records:
        raise RuntimeError('duplicate full record: ' + name)
    records[name] = wire(value)

def positive(name, value):
    value = F(value)
    if value <= 0:
        raise RuntimeError('nonpositive exact sign: ' + name)
    signs.append(name)
    record('positive ' + name, value)

def remainder(poly, name, monic_quadratic):
    poly = P(poly)
    quadratic = P(monic_quadratic)
    equal('monic remainder divisor ' + name, quadratic.coefficient(name, 2), 1)
    if quadratic.degree(name) != 2:
        raise RuntimeError('quadratic remainder divisor changed')
    symbol = var(name)
    while poly.degree(name) >= 2:
        degree = poly.degree(name)
        poly = poly - poly.coefficient(name, degree) * symbol ** (degree - 2) * quadratic
    return poly

def truncate(poly, name, order):
    index = NAMES.index(name)
    return P({key: value for key, value in P(poly).d.items() if key[index] <= order})

def inverse_series(poly, name, order):
    poly = P(poly)
    constant = poly.coefficient(name, 0).value()
    if not constant:
        raise RuntimeError('zero series constant')
    nilpotent = truncate((poly - constant) / constant, name, order)
    return truncate(sum((truncate((-nilpotent) ** k, name, order)
                         for k in range(order + 1)), P()) / constant, name, order)

def rational_series(numerator, denominator, name, order):
    return truncate(P(numerator) * inverse_series(denominator, name, order), name, order)

a, v, z, b, q, y, h, j, w, x = (var(name) for name in NAMES)
d = 1 + a

# Complete original and reciprocal polynomial identities, not sampled roots.
original = (w - a) * (w + 1) ** 6 * (w ** 2 + 2 * (1 - x) * w + 1)
physical_cubic = ((w + 1) * (w ** 2 + 2 * (1 - x) * w + 1)
                  + (w - a) * (6 * (w ** 2 + 2 * (1 - x) * w + 1)
                               + (w + 1) * (2 * w + 2 * (1 - x))))
equal('complete physical fivefold critical factor', original.derivative('w'),
      (w + 1) ** 5 * physical_cubic)
reciprocal = P()
from math import comb
for degree in range(physical_cubic.degree('w') + 1):
    coefficient = physical_cubic.coefficient('w', degree)
    for ell in range(degree + 1):
        reciprocal += coefficient * comb(degree, ell) * a ** (degree - ell) * (-1) ** ell * q ** (3 - ell)
denominator = d ** 2 - 2 * a * x
quoted_reciprocal = (d * denominator * q ** 3
                     - (7 * denominator + 4 * d * (d - x)) * q ** 2
                     + (3 * d + 16 * (d - x)) * q - 9)
equal('complete literal reciprocal cubic', reciprocal, quoted_reciprocal)
root_polynomial = (q - v) ** 6 * (q ** 2 - j * q + h)
critical_cubic = q ** 3 - (7 * v + 2 * j) * q ** 2 + (3 * h + 8 * v * j) * q - 9 * v * h
equal('full reciprocal degree8 characteristic polynomial',
      9 * root_polynomial - q * root_polynomial.derivative('q'),
      (q - v) ** 5 * critical_cubic)
record('physical cubic', physical_cubic)
record('cleared reciprocal cubic', reciprocal)
record('full characteristic polynomial', (q - v) ** 5 * critical_cubic)

def mm(left, right):
    if not left or not right or len(left[0]) != len(right):
        raise RuntimeError('matrix product dimensions differ')
    return [[sum((left[i][k] * right[k][j] for k in range(len(right))), F(0))
             for j in range(len(right[0]))] for i in range(len(left))]

def transpose(matrix):
    return [list(row) for row in zip(*matrix)]

def matrix_equal(name, actual, expected):
    if len(actual) != len(expected) or any(len(a) != len(b) for a, b in zip(actual, expected)):
        raise RuntimeError('matrix dimensions differ: ' + name)
    for i, (row, expected_row) in enumerate(zip(actual, expected)):
        for j, (entry, expected_entry) in enumerate(zip(row, expected_row)):
            if (P(entry) - expected_entry).d:
                raise RuntimeError('full matrix entry differs: ' + name + ' at ' + str((i, j)))
    checks.append(name)

def sparse_matrix(matrix):
    return {'rows': len(matrix), 'columns': len(matrix[0]),
            'nonzero_entries': [[i, j, wire(entry)] for i, row in enumerate(matrix)
                                for j, entry in enumerate(row) if entry != 0]}

# Complete linear original-reciprocal coordinates in the fixed six-block space.
Q6 = [[F(i == j) - F(1, 6) for j in range(6)] for i in range(6)]
embedding = [[F(0)] * 6 for _ in range(2)] + Q6
complement = [[F(1), F(0), F(0)], [F(0), F(1), F(0)]] + [[F(0), F(0), F(1)] for _ in range(6)]
dual = [[F(j == 0) for j in range(8)], [F(j == 1) for j in range(8)],
        [F(0), F(0)] + [F(1, 6)] * 6]
matrix_equal('six projector complete idempotence', mm(Q6, Q6), Q6)
equal('six projector rank trace', sum(Q6[i][i] for i in range(6)), 5)
for coordinate in range(8):
    u = [F(j == coordinate) for j in range(8)]
    N = [[u[i] * (F(i == j) + 1) for j in range(8)] for i in range(8)]
    projected = [sum(Q6[i][k] * u[k + 2] for k in range(6)) for i in range(6)]
    wanted_A = mm(mm(Q6, [[u[i + 2] * F(i == j) for j in range(6)] for i in range(6)]), Q6)
    wanted_B = [[entry, entry, 7 * entry] for entry in projected]
    wanted_D = [[F(0)] * 6, [F(0)] * 6, [entry / 6 for entry in projected]]
    average = sum(u[2:]) / 6
    wanted_C = [[2 * u[0], u[0], 6 * u[0]],
                [u[1], 2 * u[1], 6 * u[1]], [average, average, 7 * average]]
    blocks = {
        'A': mm(mm(transpose(embedding), N), embedding),
        'B': mm(mm(transpose(embedding), N), complement),
        'D': mm(mm(dual, N), embedding),
        'C': mm(mm(dual, N), complement),
    }
    for label, wanted in [('A', wanted_A), ('B', wanted_B), ('D', wanted_D), ('C', wanted_C)]:
        matrix_equal('full compression basis ' + str(coordinate) + ' block ' + label, blocks[label], wanted)
    record('complete compression basis ' + str(coordinate),
           {label: sparse_matrix(block) for label, block in blocks.items()})

# Literal 8x8 projected angular matrices independently recover moment weights.
P8 = [[F(i == j) - F(1, 8) for j in range(8)] for i in range(8)]
for label, theta in [('split', [P(1), P(-1), x, -x] + [P(0)] * 4),
                     ('relative', [1 + 3 * b, -1 + 3 * b] + [-b] * 6)]:
    angular = mm(mm(P8, [[theta[i] * F(i == j) for j in range(8)] for i in range(8)]), P8)
    vector = [[entry] for entry in theta]
    first_vector = mm(angular, vector)
    second_vector = mm(angular, first_vector)
    mu2_literal, mu3_literal, mu4_literal = (sum((entry ** k for entry in theta), P()) for k in (2, 3, 4))
    zero_moment = mm(transpose(vector), vector)[0][0] / 8
    first_moment = mm(transpose(vector), first_vector)[0][0] / 8
    second_moment = mm(transpose(vector), second_vector)[0][0] / 8
    equal(label + ' literal spectral mass', zero_moment, mu2_literal / 8)
    equal(label + ' literal first spectral moment', first_moment, mu3_literal / 8)
    equal(label + ' literal second spectral moment', second_moment,
          mu4_literal / 8 - mu2_literal ** 2 / 64)
    record(label + ' complete literal moments',
           [mu2_literal, mu3_literal, mu4_literal, zero_moment, first_moment, second_moment])

# Angular split: slopes(1,-1,s,-s,0^4), z=s^2. Eigenvalue squares y.
split_f = y ** 4 * (y ** 2 - 1) * (y ** 2 - z)
split_characteristic = y ** 3 * (y ** 4 - 3 * (1 + z) * y ** 2 / 4 + z / 2)
equal('split complete angular characteristic', split_f.derivative('y') / 8, split_characteristic)
split_quadratic = y ** 2 - 3 * (1 + z) * y / 4 + z / 2
split_y_sum, split_y_product = 3 * (1 + z) / 4, z / 2
split_total_weight = (1 + z) / 8
split_weighted_y = (3 - 2 * z + 3 * z ** 2) / 32
split_denominator = (y - 1) ** 2 * (y - z) ** 2 * y
split_secular_numerator = (2 * (y + 1) * (y - z) ** 2 * y
                           + 2 * (y + z) * (y - 1) ** 2 * y
                           + 4 * (y - 1) ** 2 * (y - z) ** 2)
split_weight_identity = ((split_weighted_y - split_y_sum * split_total_weight + y * split_total_weight)
                         * split_secular_numerator
                         - 8 * (2 * y - split_y_sum) * split_denominator)
equal('split secular norm versus two-moment weights', remainder(split_weight_identity, 'y', split_quadratic), 0)
split_discriminant = 9 - 14 * z + 9 * z ** 2
equal('split angular square-root discriminant', 16 * (split_y_sum ** 2 - 4 * split_y_product), split_discriminant)
split_psi_numerator = (1 + z) ** 2 * split_discriminant + (3 - 10 * z + 3 * z ** 2) ** 2
split_psi_denominator = 64 * split_discriminant
split_psi = rational_series(split_psi_numerator, split_psi_denominator, 'z', 2)
split_mu2, split_mu4 = 2 + 2 * z, 2 + 2 * z ** 2
split_X = rational_series(split_mu4, split_mu2 ** 2, 'z', 2)
split_eta = rational_series(64 * split_psi_numerator,
                            split_psi_denominator * split_mu2 ** 2, 'z', 2)
split_gamma = split_eta - (56 * split_X - 13) / 30
equal('split Psi constant', split_psi.coefficient('z', 0), F(1, 32))
equal('split Psi quadratic coefficient', split_psi.coefficient('z', 1), -F(7, 144))
equal('split X quadratic coefficient', split_X.coefficient('z', 1), -1)
equal('split eta quadratic coefficient', split_eta.coefficient('z', 1), -F(16, 9))
equal('split Gamma quadratic coefficient', split_gamma.coefficient('z', 1), F(4, 45))
record('split complete Psi rational numerator', split_psi_numerator)
record('split complete Psi rational denominator', split_psi_denominator)
record('split Psi through z2', split_psi)
record('split X through z2', split_X)
record('split eta through z2', split_eta)
record('split Gamma through z2', split_gamma)

# Relative block means: slopes(1+3b,-1+3b,(-b)^6).
relative_f = (q + b) ** 6 * ((q - 3 * b) ** 2 - 1)
relative_quadratic = q ** 2 - 5 * b * q + 6 * b ** 2 - F(3, 4)
equal('relative complete angular characteristic', relative_f.derivative('q') / 8,
      (q + b) ** 5 * relative_quadratic)
relative_mu2 = 2 + 24 * b ** 2
relative_mu3 = 18 * b + 48 * b ** 3
relative_mu4 = 2 + 108 * b ** 2 + 168 * b ** 4
relative_weight, relative_first_moment = relative_mu2 / 8, relative_mu3 / 8
relative_D = (q - 3 * b) ** 2 - 1
relative_norm_denominator = relative_D ** 2 * (q + b) ** 2
relative_secular_numerator = 2 * ((q - 3 * b) ** 2 + 1) * (q + b) ** 2 + 6 * relative_D ** 2
relative_weight_identity = ((relative_first_moment - 5 * b * relative_weight + q * relative_weight)
                            * relative_secular_numerator
                            - 8 * (2 * q - 5 * b) * relative_norm_denominator)
equal('relative secular norm versus moment weights', remainder(relative_weight_identity, 'q', relative_quadratic), 0)
relative_gap_squared = b ** 2 + 3
relative_difference_numerator = 13 * b / 4 - 3 * b ** 3
equal('relative first-moment numerator', 2 * relative_first_moment - 5 * b * relative_weight,
      relative_difference_numerator)
relative_psi_numerator = relative_weight ** 2 * relative_gap_squared + relative_difference_numerator ** 2
relative_psi_denominator = 2 * relative_gap_squared
relative_psi = rational_series(relative_psi_numerator, relative_psi_denominator, 'b', 4)
relative_X = rational_series(relative_mu4, relative_mu2 ** 2, 'b', 4)
relative_eta = rational_series(64 * relative_psi_numerator,
                               relative_psi_denominator * relative_mu2 ** 2, 'b', 4)
relative_gamma = relative_eta - (56 * relative_X - 13) / 30
equal('relative Psi constant', relative_psi.coefficient('b', 0), F(1, 32))
equal('relative Psi quadratic coefficient', relative_psi.coefficient('b', 2), F(241, 96))
equal('relative X quadratic coefficient', relative_X.coefficient('b', 2), 15)
equal('relative eta quadratic coefficient', relative_eta.coefficient('b', 2), F(169, 6))
equal('relative Gamma quadratic coefficient', relative_gamma.coefficient('b', 2), F(1, 6))
for expression, label in ((relative_psi, 'Psi'), (relative_X, 'X'), (relative_eta, 'eta')):
    for degree in (1, 3):
        equal('relative complete parity ' + label + str(degree), expression.coefficient('b', degree), 0)
record('relative complete Psi rational numerator', relative_psi_numerator)
record('relative complete Psi rational denominator', relative_psi_denominator)
record('relative Psi through b4', relative_psi)
record('relative X through b4', relative_X)
record('relative eta through b4', relative_eta)
record('relative Gamma through b4', relative_gamma)

# Clear the common positive d^5 before comparing stiffness identities.
PG = 2768 * a ** 2 + 3080 * a - 2875
S0, C0 = PG / 30720, (4 * a + 5) ** 2 / 8192
L_numerator = (208 * a ** 2 + 232 * a - 215) / 1152
B_numerator = (69025 - 73880 * a - 66416 * a ** 2) / 12288
equal('full split stiffness polynomial', 2 * S0 + F(8, 45) * C0, L_numerator)
equal('full relative stiffness polynomial', -60 * S0 + F(2, 3) * C0, B_numerator)
equal('full relative numerator from sharp angular gap',
      B_numerator * 12288, (4 * a + 5) ** 2 - 24 * PG)
equal('split derivative numerator',
      (208 * a ** 2 + 232 * a - 215).derivative('a') * d
      - 5 * (208 * a ** 2 + 232 * a - 215),
      1307 - 512 * a - 624 * a ** 2)
equal('relative derivative numerator',
      (69025 - 73880 * a - 66416 * a ** 2).derivative('a') * d
      - 5 * (69025 - 73880 * a - 66416 * a ** 2),
      199248 * a ** 2 + 162688 * a - 419005)
positive('split derivative lower on unit interval', 1307 - 512 - 624)
positive('negative relative derivative lower on unit interval', 419005 - 162688 - 199248)
positive('split stiffness numerator at lower compact endpoint',
         (L_numerator * 1152).value(a=F(151, 250)))
positive('relative stiffness numerator at upper compact endpoint',
         (B_numerator * 12288).value(a=F(121, 200)))
positive('sharp angular numerator negative at lower compact endpoint', -PG.value(a=F(151, 250)))
positive('sharp angular numerator positive at upper compact endpoint', PG.value(a=F(121, 200)))
positive('P local numerator at lower compact endpoint',
         (1616 * a ** 2 + 1800 * a - 1675).value(a=F(151, 250)))
lower_root_rational, lower_root_radical = F(-29, 52), F(6, 52)
equal('split threshold radical rational coefficient',
      208 * (lower_root_rational ** 2 + 101 * lower_root_radical ** 2)
      + 232 * lower_root_rational - 215, 0)
equal('split threshold radical irrational coefficient',
      416 * lower_root_rational * lower_root_radical + 232 * lower_root_radical, 0)
positive('split threshold positive radical branch', 36 * 101 - 29 ** 2)
positive('split threshold below lower compact endpoint',
         (52 * F(151, 250) + 29) ** 2 - 36 * 101)
positive('relative threshold below303over500',
         -(B_numerator * 12288).value(a=F(303, 500)))
record('split d5-scaled stiffness', L_numerator)
record('relative d5-scaled stiffness', B_numerator)
record('physical relative d5-scaled stiffness', B_numerator / 16)
record('local interval compact endpoints', [F(151, 250), F(121, 200)])
record('split threshold in Qsqrt101', [lower_root_rational, lower_root_radical])

# Stronger Gram consequence independently published in review 8230.
# It is reproduced here as a credited input to the new full-disk transfer.
# Here x denotes X and z denotes mu3^2/mu2^3, independently of the curves.
Delta = F(43, 56) - x
moment_slack = z - F(12, 5) * (x - F(1, 2))
gram_D = F(3, 4) * Delta - F(25, 48) * moment_slack
gram_N = Delta - F(5, 6) * moment_slack
gram_B = F(1, 7) + F(4, 3) * z
old_gram_lower = (56 * x - 13) / 30
equal('credited Gram residual reproduced',
      (gram_B - old_gram_lower) * gram_D + gram_N ** 2,
      Delta * moment_slack / 36)
equal('credited complete Gram tangent residual',
      (gram_B - old_gram_lower - moment_slack / 27) * gram_D + gram_N ** 2,
      25 * moment_slack ** 2 / 1296)
equal('credited linear Gram consequence in full moments',
      moment_slack / 27, F(4, 45) * (F(1, 2) - x) + z / 27)
equal('credited full angular moving-pair lower decomposition',
      S0 * (F(1, 2) - x) + C0 * moment_slack / 27,
      (S0 + F(4, 45) * C0) * (F(1, 2) - x) + C0 * z / 27)
equal('singular Gram residual forces moment slack zero',
      gram_N - F(4, 3) * gram_D, -F(5, 36) * moment_slack)
record('complete credited Gram tangent residual', 25 * moment_slack ** 2 / 1296)
record('full Gram quantities', {'Delta': Delta, 'h': moment_slack,
                               'D': gram_D, 'N': gram_N, 'B': gram_B})
record('complete moving-pair angular lower decomposition',
       (S0 + F(4, 45) * C0) * (F(1, 2) - x) + C0 * z / 27)

damaged('split Gamma altered coefficient', split_gamma.coefficient('z', 1), F(1, 10))
damaged('relative Gamma altered coefficient', relative_gamma.coefficient('b', 2), F(1, 5))
damaged('relative mean physical normalization', B_numerator / 16, B_numerator / 4)
damaged('split stiffness omitted spectral-weight term', L_numerator, 2 * S0)
damaged('relative stiffness sign changed', B_numerator, 60 * S0 + F(2, 3) * C0)
damaged('fivefold critical multiplicity damaged', original.derivative('w'), (w + 1) ** 4 * physical_cubic)
damaged('Gram tangent coefficient damaged',
        (gram_B - old_gram_lower - moment_slack / 27) * gram_D + gram_N ** 2,
        moment_slack ** 2 / 54)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--emit-fixture', action='store_true',
                        help='explicit regeneration mode; default requires the entire fixture')
    parser.add_argument('--check', type=Path,
                        help='validate an explicitly supplied complete fixture')
    args = parser.parse_args()
    if args.emit_fixture and args.check is not None:
        parser.error('--emit-fixture and --check are mutually exclusive')
    payload = {key: records[key] for key in sorted(records)}
    digest = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    result = {
        'schema': 'sendov-moving-pair-two-chart-v1',
        'agent': 'six-sendov-3', 'role': 'researcher',
        'identity_count': len(checks), 'strict_sign_count': len(signs),
        'linear_compression_basis_count': 8, 'literal_matrix_moment_count': 6,
        'damaged_math_count': len(damages), 'record_count': len(payload),
        'record_sha256': digest,
        'status': 'exact polynomial/weight/Hessian certificate; uniform analytic bridges are in PROOF.md',
    }
    full = {**result, 'records': payload}
    if args.emit_fixture:
        print(json.dumps(full, indent=2, sort_keys=True))
        return
    fixture = args.check if args.check is not None else Path(__file__).with_name('expected.json')
    if not fixture.is_file():
        raise RuntimeError('Required complete fixture is missing')
    expected = json.loads(fixture.read_text())
    if expected != full:
        raise RuntimeError('Required complete fixture differs in an entry or metadata')
    print(json.dumps(result, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
