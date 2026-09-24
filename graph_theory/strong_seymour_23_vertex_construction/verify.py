#!/usr/bin/env python3
"""Exact Hall-table and symbolic-certificate audit, no solver dependency."""
from __future__ import annotations
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from construction import OUT, SOURCES, TYPES, blowup, matrix_text, weights

HERE = Path(__file__).resolve().parent


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def validate(graph: list[int]) -> None:
    n = len(graph)
    need(n > 0, 'empty graph')
    for i, row in enumerate(graph):
        need(type(row) is int and 0 <= row < 1 << n and not row >> i & 1, 'invalid row')
        for j in range(i):
            need(((row >> j) & 1) + ((graph[j] >> i) & 1) == 1, 'not a tournament')


def target(graph: list[int], root: int, source: list[int] | tuple[int, ...]) -> list[int]:
    need(len(source) == len(set(source)) and all(type(x) is int and 0 <= x < len(graph)
         and graph[root] >> x & 1 for x in source), 'source is not an out-neighbor subset')
    union = 0
    for x in source:
        union |= graph[x]
    # Every in-neighbor reached from this source is at exact distance two.
    mask = union & (((1 << len(graph)) - 1) ^ (graph[root] | (1 << root)))
    return [x for x in range(len(graph)) if mask >> x & 1]


def check_hall(graph: list[int], root: int, source: list[int], claimed: list[int]) -> None:
    need(target(graph, root, source) == claimed, 'wrong target set')
    need(len(source) > len(claimed), 'Hall inequality is not strict')


def closed_rows(graph: list[int], root: int) -> tuple[list[dict], int]:
    outs = [i for i in range(len(graph)) if graph[root] >> i & 1]
    records = []
    for mask in range(1, 1 << len(outs)):
        source = [x for j, x in enumerate(outs) if mask >> j & 1]
        neighbors = target(graph, root, source)
        closure = [x for x in outs if set(target(graph, root, [x])) <= set(neighbors)]
        if source == closure:
            row = [int(j in source) - int(j in neighbors) for j in range(len(graph))]
            coeff = [sum(row[j] for j, t in enumerate(TYPES) if t == k) for k in range(3)]
            records.append({'source': source, 'target': neighbors, 'coeff': coeff})
    return records, (1 << len(outs)) - 1


def determinant(matrix: list[list[int]]) -> Fraction:
    a = [list(map(Fraction, row)) for row in matrix]
    det = Fraction(1)
    for col in range(len(a)):
        pivot = next((i for i in range(col, len(a)) if a[i][col]), None)
        if pivot is None:
            return Fraction(0)
        if pivot != col:
            a[col], a[pivot] = a[pivot], a[col]
            det = -det
        factor = a[col][col]
        det *= factor
        for j in range(col, len(a)):
            a[col][j] /= factor
        for i in range(col + 1, len(a)):
            scale = a[i][col]
            for j in range(col, len(a)):
                a[i][j] -= scale * a[col][j]
    return det


def main() -> None:
    cert = json.loads((HERE / 'certificate.json').read_text())
    need(cert['schema'] == 1, 'unknown schema')
    q = [sum(1 << j for j in row) for row in OUT]
    validate(q)
    w = weights(1, 2, 4)
    need(cert['weights'] == w and cert['out'] == [list(row) for row in OUT], 'quotient mismatch')
    matrix, hall = [], []
    for i, source in enumerate(SOURCES):
        neighbors = target(q, i, source)
        row = [int(j in source) - int(j in neighbors) for j in range(13)]
        need(sum(x * y for x, y in zip(row, w)) == 1, 'base deficiency is not one')
        matrix.append(row)
        hall.append({'root': i, 'source': list(source), 'target': neighbors,
                     'coeff': [sum(row[j] for j, t in enumerate(TYPES) if t == k) for k in range(3)]})
    need(hall == cert['hall'], 'Hall table mismatch')
    complete, maximal, subsets = [], [], 0
    for i in range(13):
        records, count = closed_rows(q, i)
        complete.append(records)
        subsets += count
        coefficients = {tuple(row['coeff']) for row in records} | {(0, 0, 0)}
        maximal.append([list(r) for r in sorted(coefficients) if not any(
            r != t and all(a <= b for a, b in zip(r, t)) for t in coefficients)])
    need(complete == cert['closed_rows'], 'complete closure certificate mismatch')
    need(maximal == cert['max_coefficients'], 'maximum deficiency formula mismatch')
    numerators = cert['dual_numerators']
    denominator = cert['dual_denominator']
    need(denominator == 40 and len(numerators) == 13 and all(type(x) is int and x > 0 for x in numerators), 'invalid dual')
    need(all(sum(numerators[i] * matrix[i][j] for i in range(13)) == denominator
             for j in range(13)), 'dual identity fails')
    need(sum(numerators) == 23 * denominator and determinant(matrix) == 40, 'dual minimum / uniqueness fails')
    base, parts = blowup()
    literal = (HERE / 'tournament23.txt').read_bytes()
    need(literal == matrix_text(base).encode('ascii'), 'literal matrix mismatch')
    checked = 0
    for a, b, c in ((1, 2, 4), (2, 4, 8)):
        for internal in ('transitive', 'reverse', 'balanced'):
            graph, parts = blowup(a, b, c, internal)
            validate(graph)
            for i, part in enumerate(parts):
                source = [x for j in SOURCES[i] for x in parts[j]]
                expected = sorted(x for j in hall[i]['target'] for x in parts[j])
                for v in part:
                    check_hall(graph, v, source, expected)
                    checked += 1
    # A malformed graph, source, target, and non-strict witness must be rejected.
    bad = base[:]
    bad[0] |= 1
    bad_edge = base[:]
    bad_edge[0] ^= 1 << 1
    _, parts = blowup()
    source0 = [x for j in SOURCES[0] for x in parts[j]]
    target0 = target(base, 0, source0)
    rejected = 0
    for action in (lambda: validate(bad), lambda: validate(bad_edge),
                   lambda: target(base, 0, [0]),
                   lambda: check_hall(base, 0, source0, target0[:-1]),
                   lambda: check_hall(base, 0, [], []),
                   lambda: weights(0, 2, 4)):
        try:
            action()
        except ValueError:
            rejected += 1
        else:
            raise ValueError('negative fixture was accepted')
    print(json.dumps({'status': 'HALL AND SYMBOLIC CHECK PASSED',
        'order': len(base), 'parts': 13, 'selected_deficiencies': [1] * 13,
        'quotient_source_subsets': subsets, 'closed_rows': sum(map(len, complete)),
        'selected_matrix_determinant': 40, 'selected_certificate_minimum': 23,
        'expanded_hall_checks': checked, 'negative_fixtures_rejected': rejected,
        'tournament_sha256': hashlib.sha256(literal).hexdigest()}, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
