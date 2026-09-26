#!/usr/bin/env python3
"""Exact symbolic checks and compressed signed-diagonal certificates.

The universal analytic argument is in PROOF.md. Standard library only.
No Gaussian quadrature, solver, floating-point arithmetic or private input.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
import json
from math import comb, factorial
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def trim(poly):
    while len(poly) > 1 and poly[-1] == 0:
        poly.pop()
    return poly


def add(a, b):
    return trim([(a[i] if i < len(a) else F(0))
                 + (b[i] if i < len(b) else F(0))
                 for i in range(max(len(a), len(b)))])


def scale(a, c):
    return trim([x * c for x in a])


def multiply(a, b):
    out = [F(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return trim(out)


def binomial_polynomial(offset, degree):
    # binom(j+offset,degree), as a polynomial in the unbounded integer j.
    result = [F(1)]
    for t in range(degree):
        result = multiply(result, [F(offset - t), F(1)])
    return scale(result, F(1, factorial(degree)))


def coefficient_identity(q, ell):
    # Equation (14) after clearing its positive denominators.
    left = multiply([F(q + 1), F(1)], [F(q + 2), F(1)])
    left = multiply(left, binomial_polynomial(q, q))
    left = scale(left, F(comb(q, ell)))
    right = multiply([F(ell + 2), F(1)], [F(ell + 1), F(1)])
    right = multiply(right, binomial_polynomial(q + 2, q - ell))
    right = multiply(right, binomial_polynomial(ell, ell))
    require(left == right, 'symbolic coefficient normalization')
    return list(map(str, left))


def bivariate_add(a, b):
    out = dict(a)
    for key, value in b.items():
        out[key] = out.get(key, F(0)) + value
    return {key: value for key, value in out.items() if value}


def bivariate_multiply(a, b):
    out = {}
    for (i, j), x in a.items():
        for (k, ell), y in b.items():
            key = (i + k, j + ell)
            out[key] = out.get(key, F(0)) + x * y
    return {key: value for key, value in out.items() if value}


def outer(v):
    return [[x * y for y in v] for x in v]


def gram_update(p, q):
    """Two coefficient matrices of the same universal quadratic form."""
    size = p + q
    lhs = [[F(i == j) - F(1, size) for j in range(size)]
           for i in range(size)]
    rhs = [[F(i == j) - F(1, p) if i < p and j < p else F(0)
            for j in range(size)] for i in range(size)]
    vectors = [[F(i == a) - (F(1, p) if i < p else F(0))
                for i in range(size)] for a in range(p, size)]
    for vector in vectors:
        matrix = outer(vector)
        for i in range(size):
            for j in range(size):
                rhs[i][j] += matrix[i][j]
    total = [sum((v[i] for v in vectors), F(0)) for i in range(size)]
    matrix = outer(total)
    for i in range(size):
        for j in range(size):
            rhs[i][j] -= matrix[i][j] / size
    require(lhs == rhs, 'Gram variance-update identity')
    return size * size


def partitions(total, maximum=None):
    if total == 0:
        yield ()
        return
    if maximum is None:
        maximum = total
    for first in range(min(total, maximum), 0, -1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def residual_patterns():
    unresolved = set()
    count = pair_count = 0
    for counts in partitions(9):
        count += 1
        for a, b in combinations(range(len(counts)), 2):
            pair_count += 1
            remainder = list(counts)
            remainder[a] -= 1
            remainder[b] -= 1
            if sum(v > 0 for v in remainder) > 6:
                unresolved.add((counts, tuple(sorted((counts[a], counts[b]), reverse=True))))
    require(count == 30, 'partition completeness')
    return count, pair_count, sorted(unresolved, key=lambda row: (len(row[0]), row))


def determinant(matrix):
    a = [list(map(F, row)) for row in matrix]
    n = len(a)
    require(all(len(row) == n for row in a), 'square determinant input')
    value = F(1)
    for col in range(n):
        pivot = next((j for j in range(col, n) if a[j][col]), None)
        if pivot is None:
            return F(0)
        if pivot != col:
            a[pivot], a[col] = a[col], a[pivot]
            value = -value
        diagonal = a[col][col]
        value *= diagonal
        for j in range(col + 1, n):
            factor = a[j][col] / diagonal
            for k in range(col + 1, n):
                a[j][k] -= factor * a[col][k]
            a[j][col] = F(0)
    return value


def boundary(data):
    vertices = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    x, y = list(vertices), list(vertices)
    for i in range(4):
        for j in range(4):
            if i != j:
                x.append(tuple(b - a for a, b in zip(vertices[i], vertices[j])))
                y.append(tuple(b + a for a, b in zip(vertices[i], vertices[j])))
    ids = data['boundary_original_labels']
    require(len(ids) == len(set(ids)) == 7 and all(0 <= i < 16 for i in ids),
            'boundary label coverage')
    counts = data['boundary_multiplicities']
    require(len(counts) == 7 and all(type(n) is int and n > 0 for n in counts)
            and sum(counts) == 9, 'boundary multiplicities')
    pair = data['boundary_distinguished_labels']
    require(len(pair) == 2 and pair[0] != pair[1] and all(a in ids for a in pair),
            'boundary pair labels')
    remains = list(counts)
    for label in pair:
        remains[ids.index(label)] -= 1
    require(remains == [1] * 7, 'remaining seven distinct labels')
    def loss(a, b):
        return sum((x[a][i] - x[b][i]) ** 2 - (y[a][i] - y[b][i]) ** 2
                   for i in range(3))
    losses = [loss(a, b) for a, b in combinations(ids, 2)]
    require(min(losses) >= 0, 'boundary endpoint contraction')
    require(loss(*pair) == F(data['boundary_pair_loss']) > 0,
            'boundary distinguished pair loss')
    z = [x[i] + y[i] for i in ids]
    matrix = [[F(v - u) for u, v in zip(z[0], point)] for point in z[1:]]
    det = determinant(matrix)
    require(det == F(data['boundary_paired_determinant']) != 0,
            'rank-six boundary determinant')
    return {'sites': 7, 'replica_positions': 9, 'contraction_pairs': len(losses),
            'strict_pairs': sum(v > 0 for v in losses), 'paired_determinant': str(det),
            'midpoint_interpolation_determinant': str(det / 8),
            'distinguished_pair_loss': str(loss(*pair)),
            'scope': 'rank-test coverage boundary; no negative Gaussian or beta value claimed'}


def compact_bound(frontier, degree, index):
    require(type(frontier) is int and frontier >= 1, 'positive frontier index')
    require(type(degree) is int and type(index) is int and 0 <= index <= degree,
            'beta index range')
    q = degree - index
    require(q <= 6, 'outside proved complement range')
    mantissa = F((degree + 1) * comb(degree, q), 1024 * 3 ** q)
    exponent = 2 * (index + 2) * (18 * frontier ** 2 + 8 * frontier + 4)
    require(mantissa > 0 and exponent > 0, 'strict certificate coefficient')
    return {'N': degree, 'j': index, 'q': q, 'mantissa': str(mantissa),
            'negative_binary_exponent': exponent,
            'meaning': 'b_(N,j)(Q) >= mantissa * 2^(-exponent) * E(pair loss), for every Q in K_l'}


def audit(data):
    require(data.get('schema') == 'gaussian-beta-pair-conditioning-v1', 'schema')
    require(data['dimension'] == 3 and data['maximum_complement'] == 6,
            'proved dimension and complement range')
    polynomials = [[q, ell, coefficient_identity(q, ell)]
                   for q in range(7) for ell in range(q + 1)]
    gram_entries = sum(gram_update(p, q) for p in range(2, 9) for q in range(7))
    # Exact identities underlying the affine-offset and exponential budget.
    # Variables of these small two-variable expressions are formal.
    # r(p+r)-r^2=pr, and beta*(1-p/(p+r))=beta*r/(p+r).
    p_var, r_var = {(1, 0): F(1)}, {(0, 1): F(1)}
    first = bivariate_multiply(r_var, bivariate_add(p_var, r_var))
    second = {key: -v for key, v in bivariate_multiply(r_var, r_var).items()}
    require(bivariate_add(first, second) == bivariate_multiply(p_var, r_var),
            'offset polynomial')
    radius = [F(0), F(1)]
    square = multiply(radius, radius)
    budget = add(scale(square, F(5)),
                 add(multiply([F(2), F(2)], [F(2), F(2)]), [F(4)]))
    require(budget == list(map(F, [8, 8, 9])), 'continuous radius exponent')
    frontier_budget = [F(4), F(8), F(18)]
    require([budget[0] / 2, budget[1], 2 * budget[2]] == frontier_budget,
            'compact frontier exponent')
    require(8 ** 5 < 256 ** 2, 'Gaussian normalization constant')
    require(F(1) + F(1, 2) + F(1, 8) > F(3, 2), 'complement lower bound')
    # exp(1): tail after degree two starts at 1/6; subsequent ratios <=1/4.
    e_upper = F(5, 2) + F(1, 6) / (1 - F(1, 4))
    require(e_upper == F(49, 18) < 4, 'exponential base bound')
    count, pairs, remaining = residual_patterns()
    supplied = sorted((tuple(r['multiplicities']), tuple(r['pair_multiplicities']))
                      for r in data['remaining_patterns'])
    require(sorted(remaining) == supplied, 'complete first residual cases')
    l = data['frontier_index']
    require(type(l) is int and l >= 1, 'positive frontier index')
    degree = 2 ** 16 * l ** 8 - 2
    record = {
        'status': 'UNIVERSAL_BETA_DIAGONALS_EXACT_AUDIT_PASS',
        'scope': 'All bounded R3 laws and contractions; all N,j with 0<=N-j<=6',
        'strictness': 'Positive unless the support map preserves every pair distance',
        'symbolic_identities_in_unbounded_base_index': len(polynomials),
        'symbolic_identity_sha256': sha256(json.dumps(polynomials, separators=(',', ':')).encode()).hexdigest(),
        'symbolic_affine_offset_identity': True,
        'finite_gram_identity_sizes': 49, 'exact_gram_entries_compared': gram_entries,
        'first_residual_partition_count': count, 'distinct_pair_cases_checked': pairs,
        'remaining_patterns': data['remaining_patterns'], 'boundary': boundary(data),
        'compact_frontier': {'l': l, 'degree': degree,
                             'certified_entries': [compact_bound(l, degree, degree - q)
                                                   for q in range(7)]},
        'trust': 'Written conditional-Gaussian and Poisson proof plus exact symbolic audit; independent review pending'
    }
    raw = json.dumps(record, sort_keys=True, separators=(',', ':')).encode()
    return {'record': record, 'record_sha256': sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).with_name('CERTIFICATE.json'))
    args = parser.parse_args()
    print(json.dumps(audit(json.loads(args.certificate.read_text())), indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
