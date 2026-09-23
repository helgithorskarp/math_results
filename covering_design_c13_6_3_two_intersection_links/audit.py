#!/usr/bin/env python3
"""Separate spectral/weight audit; does not import the enumeration/checker.

This is not a second independent classification. It checks two proof layers
using fraction-free matrix determinants and definition-level set operations.
"""
from itertools import combinations, combinations_with_replacement
import json
from math import isqrt
from pathlib import Path


def check(condition, message):
    if not condition:
        raise ValueError(message)


def determinant(matrix):
    a = [row[:] for row in matrix]
    previous, sign = 1, 1
    for k in range(len(a) - 1):
        pivot = next((i for i in range(k, len(a)) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign *= -1
        value = a[k][k]
        for i in range(k + 1, len(a)):
            for j in range(k + 1, len(a)):
                numerator = a[i][j] * value - a[i][k] * a[k][j]
                check(numerator % previous == 0, 'inexact Bareiss division')
                a[i][j] = numerator // previous
            a[i][k] = 0
        previous = value
    return sign * a[-1][-1]


def explicit_matrix(parts, x):
    a = [[x if i == j else 0 for j in range(12)] for i in range(12)]
    offset = 0
    for n in parts:
        vertices = list(range(offset, offset + n))
        for i, j in zip(vertices, vertices[1:] + vertices[:1]):
            a[i][j] = a[j][i] = -1
        offset += n
    return a


def decode(mask):
    check(type(mask) is int and 0 <= mask < 4096, 'invalid mask')
    return frozenset(j for j in range(12) if (mask // 2 ** j) % 2)


def main():
    root = Path(__file__).resolve().parent
    expected = json.loads((root / 'EXPECTED.json').read_text())
    certificate = json.loads((root / 'certificate.json').read_text())
    partitions = {p for count in range(1, 5)
                  for p in combinations_with_replacement(range(3, 13), count)
                  if sum(p) == 12}
    spectral = expected['spectral_and_enumeration']
    check(partitions == {tuple(r['parts']) for r in spectral}, 'partition coverage')
    evaluations = set()
    determinant_checks = 0
    for record in spectral:
        parts = record['parts']
        values = []
        polynomial = record['polynomial']
        check(len(polynomial) == 13 and polynomial[-1] == 1, 'degree or leading term')
        for x in range(13):
            actual = determinant(explicit_matrix(parts, x))
            check(actual == sum(c * x ** i for i, c in enumerate(polynomial)),
                  'characteristic polynomial mismatch')
            values.append(actual)
            determinant_checks += 1
        check(tuple(values) not in evaluations, 'cospectral cycle partitions')
        evaluations.add(tuple(values))
        check(values[3] == record['determinant'], 'determinant table mismatch')
        check((isqrt(values[3]) ** 2 == values[3]) == record['square'], 'square test')
    triples = list(map(frozenset, combinations(range(12), 3)))
    six_sets = list(map(frozenset, combinations(range(12), 6)))
    total_capacities = 0
    results = []
    for record in certificate['cases']:
        rows = list(map(decode, record['rows']))
        check(len(set(rows)) == 12 and all(len(r) == 5 for r in rows), 'rows')
        check(all(sum(j in r for r in rows) == 5 for j in range(12)), 'degrees')
        check(all(1 <= len(a & b) <= 2 for a, b in combinations(rows, 2)), 'intersections')
        check(all(any(p <= r for r in rows)
                  for p in map(frozenset, combinations(range(12), 2))), 'pair coverage')
        missing = {t for t in triples if not any(t <= r for r in rows)}
        check(len(missing) == 100, 'missing-triple count')
        weights = {decode(t): w for t, w in record['weights']}
        check(len(weights) == len(record['weights']), 'duplicate weight')
        check(weights.keys() <= missing and all(type(w) is int and w > 0
                                               for w in weights.values()), 'weights')
        loads = [sum(w for t, w in weights.items() if t <= b) for b in six_sets]
        check(max(loads) <= record['capacity'], 'capacity')
        check(sum(weights.values()) > 8 * record['capacity'], 'strict inequality')
        results.append([record['case'], sum(weights.values()), max(loads)])
        total_capacities += len(loads)
    check(len(results) == 6, 'six representatives required')
    print(json.dumps(dict(status='INDEPENDENT_SPECTRAL_AND_WEIGHT_AUDIT_PASS',
                          exact_determinants=determinant_checks,
                          six_set_capacity_checks=total_capacities,
                          weights=results), indent=2))


if __name__ == '__main__':
    main()
