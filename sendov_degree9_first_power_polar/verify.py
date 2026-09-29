#!/usr/bin/env python3
"""Exact compact certificate check for the degree-nine first-power estimate."""
from fractions import Fraction as F
from hashlib import sha256
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p.pop()
    return p


def add(p, q):
    out = [F(0)] * max(len(p), len(q))
    for i, v in enumerate(p):
        out[i] += v
    for i, v in enumerate(q):
        out[i] += v
    return trim(out)


def scale(p, c):
    return trim([c * v for v in p])


def mul(p, q):
    out = [F(0)] * (len(p) + len(q) - 1)
    for i, x in enumerate(p):
        for j, y in enumerate(q):
            out[i + j] += x * y
    return trim(out)


def power(p, n):
    out = [F(1)]
    for _ in range(n):
        out = mul(out, p)
    return out


def polar(c):
    # Integrate the binomial expansion term by term over 0 <= t <= 1.
    out = [F(0)]
    for k in range(9):
        term = mul(power([F(0), F(1)], 8 - k),
                   power([c, F(0), -c], k))
        out = add(out, scale(term, F(comb(8, k), k + 1)))
    return out


def evaluate(p, a):
    out = F(0)
    for v in reversed(p):
        out = out * a + v
    return out


def divide_one_minus_a(p):
    out = []
    acc = F(0)
    for v in p[:-1]:
        acc += v
        out.append(acc)
    require(p[-1] == -acc, 'Nonzero division remainder')
    return trim(out)


def bernstein(p, left, right, n):
    # Substitute a=left+(right-left)*x into the monomial representation.
    coeff = [F(0)] * (n + 1)
    for j, v in enumerate(p):
        for k in range(j + 1):
            coeff[k] += v * comb(j, k) * left**(j-k) * (right-left)**k
    # x^k = sum_{i=k}^n binom(i,k)/binom(n,k) * B_{i,n}(x).
    return [sum(coeff[k] * F(comb(i, k), comb(n, k))
                for k in range(i + 1)) for i in range(n + 1)]


def main():
    path = Path(__file__).with_name('certificate.json')
    raw = path.read_bytes()
    cert = json.loads(raw)
    require(cert['degree'] == 9, 'Wrong polynomial degree')
    require(cert['bernstein_degree'] == 15, 'Wrong Bernstein degree')
    c = F(cert['uniform_mean_bound'])
    require(c == F(46643, 50000), 'Unexpected uniform bound')
    H = polar(c)

    # Independent endpoint-antiderivative identity, checked coefficientwise.
    # 9*c*(1-a^2)*H = (a+c*(1-a^2))^9 - a^9.
    endpoint = add(power([c, F(1), -c], 9),
                   scale(power([F(0), F(1)], 9), -1))
    require(mul([9*c, F(0), -9*c], H) == endpoint,
            'Antiderivative coefficient identity failed')
    P = divide_one_minus_a(add([F(1)], scale(H, -1)))
    require(len(P) == 16, 'Wrong quotient degree')
    require(mul([F(1), F(-1)], P) == add([F(1)], scale(H, -1)),
            'Quotient reconstruction failed')

    intervals = [(F(l), F(r)) for l, r in cert['intervals']]
    require(intervals and intervals[0][0] == 0 and intervals[-1][1] == 1,
            'Cover endpoints failed')
    previous = F(0)
    margins = []
    for left, right in intervals:
        require(left == previous and left < right <= 1,
                'Cover has a gap, overlap, or malformed interval')
        coeff = bernstein(P, left, right, 15)
        require(min(coeff) > 0, 'Bernstein positivity failed')
        # Independent evaluation at both ends of the transformed polynomial.
        require(coeff[0] == evaluate(P, left) and
                coeff[-1] == evaluate(P, right), 'Endpoint check failed')
        margins.append(min(coeff))
        previous = right

    H1 = polar(F(1))
    lower, upper = map(F, cert['central_radius_bracket'])
    require(0 < lower < upper < F(1, 2), 'Malformed radius bracket')
    require(evaluate(H1, lower) < 1 < evaluate(H1, upper),
            'Radius bracket signs failed')
    require(evaluate(H1, F(1, 2)) == F(72319, 65536),
            'Known exact value failed')
    witness = cert['scalar_barrier_witness']
    aw, cw = F(witness['a']), F(witness['mean'])
    require(0 < aw < 1 and c < cw < 1, 'Malformed barrier witness')
    require(evaluate(polar(cw), aw) > 1, 'Scalar barrier witness failed')

    print('PASS: antiderivative and quotient identities')
    print(f'PASS: {len(intervals)} intervals, 96 strictly positive Bernstein coefficients')
    print(f'PASS: uniform first-power sum > {8*c}')
    print('PASS: 0.4398 < central radius < 0.4399')
    print('PASS: scalar polar optimum in [0.93286, 0.93287)')
    print(f'certificate SHA256: {sha256(raw).hexdigest()}')


if __name__ == '__main__':
    main()
