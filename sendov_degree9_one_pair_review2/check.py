#!/usr/bin/env python3
"""Independent moment-quadrature and tensor-interpolation audit, six-reviewer-2.

No author code or coefficient input is imported. All arithmetic is rational.
Nine moment-certified quadrature nodes integrate the degree-eight t polynomial;
Bernstein collocation matrices reconstruct each full tensor certificate.
"""
import argparse
import hashlib
import json
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def inverse(matrix):
    n = len(matrix)
    require(all(len(row) == n for row in matrix), "Nonsquare matrix")
    rows = [[F(x) for x in row] + [F(i == j) for j in range(n)]
            for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if rows[i][col]), None)
        require(pivot is not None, "Singular interpolation matrix")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        scale = rows[col][col]
        rows[col] = [x / scale for x in rows[col]]
        for i in range(n):
            if i != col and rows[i][col]:
                scale = rows[i][col]
                rows[i] = [x - scale * y for x, y in zip(rows[i], rows[col])]
    result = [row[n:] for row in rows]
    require(all(sum(matrix[i][j] * result[j][k] for j in range(n)) == F(i == k)
                for i in range(n) for k in range(n)), "Inverse identity")
    return result


def bernstein(n, x):
    return [comb(n, i) * x**i * (1 - x)**(n - i) for i in range(n + 1)]


@lru_cache(None)
def collocation(n):
    nodes = tuple(F(i, n) for i in range(n + 1))
    matrix = [bernstein(n, x) for x in nodes]
    return nodes, matrix, inverse(matrix)


def quadrature():
    nodes = tuple(F(i, 8) for i in range(9))
    moments = [[t**degree for t in nodes] for degree in range(9)]
    inv = inverse(moments)
    weights = tuple(sum(inv[i][j] / (j + 1) for j in range(9)) for i in range(9))
    check_moments(nodes, weights)
    return nodes, weights


def check_moments(nodes, weights):
    require(len(nodes) == len(weights) == 9, "Quadrature dimensions")
    require(all(sum(w * t**d for t, w in zip(nodes, weights)) == F(1, d + 1)
                for d in range(9)), "Quadrature moment identity")


NODES, WEIGHTS = quadrature()


def profile_value(k, a, u, v):
    m = 6 - k
    d, radius = 1 + a, 1 + 4 * a * v
    free = 1 + F(8, m) * a * (1 - v) * u
    integral = F(0)
    for t, weight in zip(NODES, WEIGHTS):
        real_factors = (d - a * t)**k * (d - a * t * free)**m
        pair = d*d*(1 - t) + ((1 - a*a)*t + a*a*t*t)*radius*radius
        integral += weight * real_factors * pair
    return 9 * integral - radius*radius*free**m


def transform(values, degree, axis, matrix):
    out = {}
    for index in product(*(range(n + 1) for n in degree)):
        total = F(0)
        for j, coefficient in enumerate(matrix[index[axis]]):
            if coefficient:
                old = list(index)
                old[axis] = j
                total += coefficient * values[tuple(old)]
        out[index] = total
    return out


def interpolate(function, degree):
    nodes = [collocation(n)[0] for n in degree]
    samples = {idx: function(*(nodes[axis][idx[axis]] for axis in range(len(degree))))
               for idx in product(*(range(n + 1) for n in degree))}
    coefficients = samples
    for axis, n in enumerate(degree):
        coefficients = transform(coefficients, degree, axis, collocation(n)[2])
    # Full reverse grid checks, independent of positivity and of the target hash.
    recovered = coefficients
    for axis, n in enumerate(degree):
        recovered = transform(recovered, degree, axis, collocation(n)[1])
    require(recovered == samples, "Full tensor interpolation identity")
    return coefficients


def tensor_value(coefficients, degree, point):
    bases = [bernstein(n, x) for n, x in zip(degree, point)]
    return sum(c * bases[0][i] * bases[1][j] * bases[2][h]
               for (i, j, h), c in coefficients.items())


def digest(coefficients):
    raw = ''.join(','.join(map(str, idx)) + ':' +
                  str(c.numerator) + '/' + str(c.denominator) + '\n'
                  for idx, c in sorted(coefficients.items())).encode('ascii')
    return hashlib.sha256(raw).hexdigest()


def bound_check(k, coefficients, lower=F(44, 7)):
    require(all(c >= 0 for c in coefficients.values()), "Negative certificate coefficient")
    zeros = [idx for idx, c in coefficients.items() if not c]
    require(zeros == ([(11, 1, 0)] if k == 5 else []), "Incorrect zero locus")
    require(all(c >= lower for c in coefficients.values() if c), "False uniform bound")
    require(all(c == 8 for idx, c in coefficients.items() if idx[0] == 0),
            "Incorrect a=0 face")


def polar_dependency():
    # I(a)=integral[a+(1-a*a-a/4)t]^8. Its degree in a is at most16.
    def deficit(a):
        return 1 - sum(w * (a + (1 - a*a - a/F(4))*t)**8
                       for t, w in zip(NODES, WEIGHTS))
    result = []
    for left, right in [(F(0), F(1, 2)), (F(1, 2), F(5, 8)), (F(5, 8), F(3, 4))]:
        coefficients = interpolate(lambda x: deficit(left + (right - left)*x), (16,))
        require(min(coefficients.values()) > 0, "Negative-real polar exclusion not certified")
        result.append({'interval': [str(left), str(right)], 'degree': 16,
                       'minimum_deficit_coefficient': str(min(coefficients.values()))})
    return result


def rejected(action):
    try:
        action()
    except ValueError:
        return True
    raise ValueError("Corrupted certificate accepted")


def derive():
    profiles = []
    holdouts = [(F(2, 7), F(3, 8), F(5, 9)), (F(1, 19), F(11, 13), F(7, 17)),
                (F(18, 19), F(2, 13), F(15, 17))]
    last_coefficients = None
    refinements = []
    for k in range(6):
        degree = (16, 6, 12) if not k else (16 - k, 6 - k, 8 - k)
        coefficients = interpolate(lambda a, u, v: profile_value(k, a, u, v), degree)
        bound_check(k, coefficients)
        for point in holdouts:
            require(tensor_value(coefficients, degree, point) == profile_value(k, *point),
                    "Off-grid exact profile check")
        positive = [c for c in coefficients.values() if c]
        profiles.append({'k': k, 'degree': list(degree), 'coefficients': len(coefficients),
                         'minimum_positive': str(min(positive)),
                         'zero_indices': [list(idx) for idx, c in coefficients.items() if not c],
                         'sha256': digest(coefficients)})
        # Independently interpolate the subtracted polynomial, then check the
        # classical binomial-moment identity for every scalar coefficient.
        subtracted = interpolate(lambda a: 8*(1 - a**9), (degree[0],))
        require(all(subtracted[i,] == 8*(1 - (F(comb(i, 9), comb(degree[0], 9))
                                                if i >= 9 else 0))
                    for i in range(degree[0] + 1)), "Subtracted gap identity")
        strengthened = {idx: c - subtracted[idx[0],] for idx, c in coefficients.items()}
        require(all(c >= 0 for c in strengthened.values()), "Stronger gap not certified")
        refinements.append({'k': k, 'coefficients': len(strengthened),
                            'all_coefficients_nonnegative': True,
                            'zero_coefficients': sum(c == 0 for c in strengthened.values()),
                            'minimum_positive': str(min(c for c in strengthened.values() if c)),
                            'sha256': digest(strengthened)})
        if k == 5:
            last_coefficients = coefficients
    bad_weights = list(WEIGHTS)
    bad_weights[0] += 1
    controls = [rejected(lambda: check_moments(NODES, bad_weights)),
                rejected(lambda: bound_check(5, last_coefficients, F(8)))]
    bad = dict(last_coefficients)
    bad[11, 1, 0] = 1
    controls.append(rejected(lambda: bound_check(5, bad)))
    # At a=0 every original coefficient is8: subtracting9 is a false gap.
    controls.append(rejected(lambda: require(min(c - 9 for idx, c in last_coefficients.items()
                                                if idx[0] == 0) >= 0, "False gap9")))
    require(all(controls), "Negative control")
    small_a = F(1, 10000)
    optimality_ratio = profile_value(0, small_a, F(0), F(0)) / (1 - small_a**9)
    require(optimality_ratio == ((1 + small_a)**9 - (1 + small_a)) /
            (small_a*(1 - small_a**9)) < F(801, 100), "Optimality model")
    return {'method': 'exact degree-eight moment quadrature and rational tensor collocation',
            'quadrature_nodes': [str(t) for t in NODES],
            'quadrature_weights': [str(w) for w in WEIGHTS],
            'moment_identities': 9, 'profiles': profiles, 'total_coefficients': 3467,
            'reverse_tensor_grid_checks': 3467, 'off_grid_identity_checks': 18,
            'negative_real_polar_dependency': polar_dependency(),
            'rejected_controls': len(controls), 'strengthened_gap8_certificate': refinements,
            'stronger_gap_reverse_grid_checks': sum(17 - k for k in range(6)),
            'optimality_control': {'a': str(small_a), 'all_reciprocals': str(1/(1 + small_a)),
                                   'normalized_gap': str(optimality_ratio),
                                   'proposed_coefficient_801_over_100_rejected': True}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target-expected', type=Path)
    parser.add_argument('--expected', type=Path, default=Path(__file__).with_name('expected.json'))
    args = parser.parse_args()
    result = derive()
    if args.target_expected:
        target = json.loads(args.target_expected.read_text())
        require(result['profiles'] == target['profiles'], "Target profile hashes/summaries differ")
    expected = json.loads(args.expected.read_text())['certificate']
    require(result == expected, 'Independent expected result differs')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
