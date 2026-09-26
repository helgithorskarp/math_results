#!/usr/bin/env python3
"""Exact author controls for recentering the q-fold Gaussian kernel.

No positivity certificate is claimed. All arithmetic uses Fraction.
"""
from fractions import Fraction as Q
from itertools import combinations
from math import factorial
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def matchings(vertices):
    if not vertices:
        yield (), ()
        return
    i, *rest = vertices
    for pairs, singles in matchings(tuple(rest)):
        yield pairs, (i,) + singles
    for j in rest:
        for pairs, singles in matchings(tuple(k for k in rest if k != j)):
            yield ((i, j),) + pairs, singles


def rising(a, r):
    ans = Q(1)
    for k in range(r):
        ans *= a + k
    return ans


def polynomial(q, alpha=Q(5, 2)):
    terms = []
    for pairs, unmatched in matchings(tuple(range(q))):
        m = len(pairs)
        for r in range(len(unmatched) + 1):
            for scalars in combinations(unmatched, r):
                diagonal = tuple(i for i in unmatched if i not in scalars)
                coef = rising(alpha + m, r) / 2 ** len(diagonal)
                terms.append((coef, pairs, diagonal))
    return terms


def evaluate(terms, gram, z=Q(1), homogenize=None):
    ans = Q(0)
    for coef, pairs, diagonal in terms:
        term = coef
        for i, j in pairs:
            term *= gram[i][j]
        for i in diagonal:
            term *= gram[i][i]
        if homogenize is not None:
            term *= z ** (homogenize - len(pairs) - len(diagonal))
        ans += term
    return ans


# Independent square-free ring Q[h_1,...,h_q]/(h_1^2,...,h_q^2).
# Unlike the matching evaluator, this takes the original exponential
# quotient as input and performs truncated multiplication and composition.
def add(a, b):
    return [x + y for x, y in zip(a, b)]


def scale(a, c):
    return [x * c for x in a]


def mul(a, b):
    out = [Q(0)] * len(a)
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if y and not i & j:
                out[i | j] += x * y
    return out


def power_series(x, coefficients):
    require(x[0] == 0, 'series requires zero constant')
    ans = [Q(0)] * len(x)
    power = [Q(0)] * len(x)
    power[0] = Q(1)
    for c in coefficients:
        ans = add(ans, scale(power, c))
        power = mul(power, x)
    return ans


def direct_derivative(gram, p, tilt, alpha=Q(5, 2)):
    q = len(gram)
    A = p + sum(tilt)
    require(A > 0, 'positive base required')
    hsum = [Q(0)] * (1 << q)
    linear = hsum[:]
    Y = hsum[:]
    Gt = [sum(gram[i][j] * tilt[j] for j in range(q)) for i in range(q)]
    Y0 = sum(tilt[i] * Gt[i] for i in range(q))
    Y[0] = Y0
    for i in range(q):
        hsum[1 << i] = Q(1)
        linear[1 << i] = -gram[i][i] / 2
        Y[1 << i] = 2 * Gt[i]
        for j in range(i):
            Y[(1 << i) | (1 << j)] = 2 * gram[i][j]
    reciprocal = power_series(hsum, [(-1) ** r / A ** (r + 1) for r in range(q + 1)])
    exponent = add(linear, scale(mul(Y, reciprocal), Q(1, 2)))
    exponent[0] -= Y0 / (2 * A)
    expseries = power_series(exponent, [Q(1, factorial(r)) for r in range(q + 1)])
    prefactor = power_series(hsum, [(-1) ** r * rising(alpha, r) /
                                           (factorial(r) * A ** r) for r in range(q + 1)])
    return (-1) ** q * mul(prefactor, expseries)[-1]


def recentered_gram(gram, p, tilt):
    q = len(gram)
    A = p + sum(tilt)
    Gt = [sum(gram[i][j] * tilt[j] for j in range(q)) for i in range(q)]
    Y0 = sum(tilt[i] * Gt[i] for i in range(q))
    return [[A * gram[i][j] - Gt[i] - Gt[j] + Y0 / A
             for j in range(q)] for i in range(q)]


def dot_gram(vectors):
    return [[sum(x * y for x, y in zip(a, b)) for b in vectors] for a in vectors]


def main():
    checked = []
    for q in range(1, 8):
        terms = polynomial(q)
        fixtures = [
            ('zero', [[Q(0)] * 6 for _ in range(q)]),
            ('coincident', [[Q(k - 2, k + 1) for k in range(6)] for _ in range(q)]),
            ('rational', [[Q(((i + 2) * (k + 3) + i * i + k * k) % 17 - 8,
                              2 + (i + k) % 3) for k in range(6)] for i in range(q)]),
        ]
        for name, points in fixtures:
            gram = dot_gram(points)
            for p, tilt in [(Q(2), [Q(0)] * q),
                            (Q(7, 3), [Q((i % 4) + 1, i + 3) for i in range(q)])]:
                actual = direct_derivative(gram, p, tilt)
                A = p + sum(tilt)
                expected = evaluate(terms, recentered_gram(gram, p, tilt)) / A ** q
                require(actual == expected, f'recentering failed: {q} {name} {p}')
                checked.append([q, name, str(p), str(actual)])
                tr = sum(gram[i][i] for i in range(q))
                normalization = 1 + tr
                scaled = [[g / normalization for g in row] for row in gram]
                value = evaluate(terms, scaled, 1 / normalization, q)
                require(value * normalization ** q == evaluate(terms, gram),
                        'homogenization failed')
    terms = polynomial(7)
    require(len(terms) == 1850, 'term count')
    integers = []
    degrees = [0] * 8
    for coef, pairs, diag in terms:
        integer = coef * 128
        require(integer.denominator == 1, 'nonintegral coefficient')
        m, r = len(pairs), 7 - 2 * len(pairs) - len(diag)
        expected = 4 ** m
        for j in range(r):
            expected *= 5 + 2 * m + 2 * j
        require(integer == expected, 'integer formula')
        degrees[len(pairs) + len(diag)] += 1
        integers.append([int(integer), pairs, diag])
    zero = [[Q(0)] * 7 for _ in range(7)]
    require(128 * evaluate(terms, zero) == 11486475, 'constant coefficient')
    identity = [[Q(i == j) for j in range(7)] for i in range(7)]
    require(128 * evaluate(terms, identity, Q(0), 7) == 1, 'top degree')
    simplex = [[Q(1) if i == j else Q(-1, 6) for j in range(7)] for i in range(7)]
    homogeneous = [sum(coef * product([simplex[i][j] for i, j in pairs] +
                                                  [simplex[i][i] for i in diag])
                       for coef, pairs, diag in terms if len(pairs) + len(diag) == d)
                   for d in range(8)]
    require(homogeneous == list(map(Q, ['11486475/128','2837835/128','375375/128',
                            '339955/1152','30905/1152','875/384','21/128','1/128'])),
            'R2 regular simplex control')
    serialized = json.dumps(integers, separators=(',', ':')).encode()
    checks = json.dumps(checked, separators=(',', ':')).encode()
    result = {'status': 'exact recentring identities verified; PSD checked by the other two programs',
              'recentered_derivative_controls': len(checked),
              'homogenization_controls': len(checked),
              'integer_matching_terms': len(terms), 'terms_by_gram_degree': degrees,
              'regular_simplex_coefficients': list(map(str, homogeneous)),
              'polynomial_stream_sha256': hashlib.sha256(serialized).hexdigest(),
              'derivative_controls_sha256': hashlib.sha256(checks).hexdigest()}
    expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())['recentring']
    require(result == expected, 'EXPECTED.json recentring mismatch')
    print(json.dumps(result, indent=2))


def product(xs):
    result = Q(1)
    for x in xs:
        result *= x
    return result


if __name__ == '__main__':
    main()
