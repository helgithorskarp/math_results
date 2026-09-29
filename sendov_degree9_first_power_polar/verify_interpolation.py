#!/usr/bin/env python3
"""Alternative exact checker: endpoint formula and rational interpolation."""
from fractions import Fraction as F
import json
from math import comb
from pathlib import Path


def need(condition, message):
    if not condition:
        raise ValueError(message)


def point_value(a, c):
    # The degree-15 quotient P(a), using the endpoint integral formula.
    if a == 1:
        return 8 * (1 - c)
    b = c * (1 - a * a)
    integral = ((a + b)**9 - a**9) / (9 * b)
    return (1 - integral) / (1 - a)


def solve(matrix):
    n = len(matrix)
    for column in range(n):
        pivot = next((i for i in range(column, n)
                      if matrix[i][column] != 0), None)
        need(pivot is not None, 'Singular interpolation matrix')
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [x / scale for x in matrix[column]]
        for row in range(n):
            if row != column:
                factor = matrix[row][column]
                matrix[row] = [x - factor * y
                               for x, y in zip(matrix[row], matrix[column])]
    return [matrix[i][-1] for i in range(n)]


def coefficients(left, right, c):
    matrix = []
    for k in range(16):
        x = F(k, 15)
        row = [comb(15, i) * x**i * (1-x)**(15-i) for i in range(16)]
        row.append(point_value(left + (right-left)*x, c))
        matrix.append(row)
    return solve(matrix)


def main():
    cert = json.loads(Path(__file__).with_name('certificate.json').read_text())
    need(cert['degree'] == 9 and cert['bernstein_degree'] == 15,
         'Unexpected degree')
    c = F(cert['uniform_mean_bound'])
    need(c == F(46643, 50000), 'Unexpected constant')
    cover = [(F(l), F(r)) for l, r in cert['intervals']]
    need(cover and cover[0][0] == 0 and cover[-1][1] == 1,
         'Malformed cover endpoints')
    results = []
    previous = F(0)
    for left, right in cover:
        need(left == previous and left < right <= 1, 'Malformed interval cover')
        values = coefficients(left, right, c)
        need(all(x > 0 for x in values), 'Independent positivity failure')
        results.append(values)
        previous = right

    # This comparison is additional; independent positivity passed above.
    import verify
    P = verify.divide_one_minus_a(verify.add([F(1)], verify.scale(verify.polar(c), -1)))
    for (left, right), values in zip(cover, results):
        need(values == verify.bernstein(P, left, right, 15),
             'Algorithms disagree coefficientwise')
    need(28 * F(101, 100)**2 * F(10101, 10000)**6 < 64,
         'Uniform Taylor remainder comparison failed')
    need(F(99, 100)**8 > F(1, 2), 'Boundary compactness comparison failed')
    print('PASS: endpoint formula and exact Bernstein interpolation')
    print('PASS: 96 positive coefficients; all match the direct algorithm')
    print('PASS: rational comparisons in the boundary variance proof')


if __name__ == '__main__':
    main()
