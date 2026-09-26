#!/usr/bin/env python3
"""Exact, standard-library-only proof computation for cubic 8-circulant nuts."""

import argparse
import hashlib
import itertools
import json
import time
from collections import Counter, defaultdict


def canonical(matrix):
    """Canonical simultaneous row/column ordering by exhaustive refinement.

    Refinement only splits invariant cells. Every vertex in a chosen cell is
    individualized; no heuristic branch pruning is used.
    """
    n = len(matrix)
    buckets = defaultdict(list)
    for i, row in enumerate(matrix):
        buckets[(row[i], sum(row))].append(i)
    partition = tuple(tuple(buckets[k]) for k in sorted(buckets))

    def visit(part):
        while True:
            refined = []
            for cell in part:
                blocks = defaultdict(list)
                for v in cell:
                    signature = tuple(sum(matrix[v][w] for w in target) for target in part)
                    blocks[signature].append(v)
                refined.extend(tuple(blocks[k]) for k in sorted(blocks))
            refined = tuple(refined)
            if refined == part:
                break
            part = refined
        pos = next((i for i, cell in enumerate(part) if len(cell) > 1), None)
        if pos is None:
            order = [cell[0] for cell in part]
            return tuple(tuple(matrix[i][j] for j in order) for i in order)
        cell = part[pos]
        return min(visit(part[:pos] + ((v,), tuple(w for w in cell if w != v)) + part[pos + 1:])
                   for v in cell)

    assert n and all(len(row) == n for row in matrix)
    return visit(partition)


def supports(max_order):
    """All connected simple subcubic graphs, by non-cut-vertex augmentation."""
    graphs = {((0,),)}
    counts = [1]
    for n in range(2, max_order + 1):
        following = set()
        for old in sorted(graphs):
            available = [i for i, row in enumerate(old) if sum(row) < 3]
            for size in range(1, min(3, len(available)) + 1):
                for adjacent in itertools.combinations(available, size):
                    new = [list(row) + [int(i in adjacent)] for i, row in enumerate(old)]
                    new.append([int(i in adjacent) for i in range(n - 1)] + [0])
                    following.add(canonical(new))
        graphs = following
        counts.append(len(graphs))
    return sorted(graphs), counts


def pregraphs(graphs):
    """Complete cubic quotients: double a matching, then fill diagonals."""
    result = set()
    for graph in graphs:
        n = len(graph)
        available = [(i, j) for i in range(n) for j in range(i + 1, n)
                     if graph[i][j] and sum(graph[i]) < 3 and sum(graph[j]) < 3]

        def augment(pos, used, doubled):
            if pos == len(available):
                matrix = [list(row) for row in graph]
                for i, j in doubled:
                    matrix[i][j] = matrix[j][i] = 2
                for i in range(n):
                    matrix[i][i] = 3 - sum(matrix[i])
                    assert matrix[i][i] in (0, 1, 2)
                result.add(canonical(matrix))
                return
            augment(pos + 1, used, doubled)
            i, j = available[pos]
            if i not in used and j not in used:
                augment(pos + 1, used | {i, j}, doubled + [(i, j)])

        augment(0, set(), [])
    return sorted(result)


def determinant(matrix):
    """Fraction-free Bareiss elimination, with checked exact divisions."""
    n = len(matrix)
    if n == 0:
        return 1
    a = [list(row) for row in matrix]
    sign, previous = 1, 1
    for k in range(n - 1):
        pivot_row = next((r for r in range(k, n) if a[r][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                quotient, remainder = divmod(numerator, previous)
                assert remainder == 0
                a[i][j] = quotient
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1]


def classify(matrix):
    """Return exact determinant and principal cofactors when singular.

    For a singular real symmetric matrix, nullity one with a full kernel
    vector is equivalent to all principal cofactors being nonzero.
    """
    det = determinant(matrix)
    if det:
        return 'invertible', det, ()
    cofactors = tuple(determinant([[x for j, x in enumerate(row) if j != k]
                                  for i, row in enumerate(matrix) if i != k])
                      for k in range(len(matrix)))
    if all(cofactors):
        return 'full', det, cofactors
    return ('zero-entry' if any(cofactors) else 'nullity>1'), det, cofactors


def signings(matrix):
    """All necessary -1-character matrices modulo diagonal sign switching."""
    n = len(matrix)
    reached, todo, tree = {0}, [0], set()
    while todo:
        i = todo.pop(0)
        for j in range(n):
            if i != j and matrix[i][j] and j not in reached:
                reached.add(j)
                todo.append(j)
                tree.add(tuple(sorted((i, j))))
    assert len(reached) == n
    free = [(i, j) for i in range(n) for j in range(i, n)
            if matrix[i][j] and (i != j or matrix[i][i] == 2) and (i, j) not in tree]
    semi_signs = (1, -1) if any(matrix[i][i] == 1 for i in range(n)) else (1,)
    for semi in semi_signs:
        for signs in itertools.product((1, -1), repeat=len(free)):
            signed = [list(row) for row in matrix]
            for (i, j), sign in zip(free, signs):
                signed[i][j] = signed[j][i] = sign * matrix[i][j]
            for i in range(n):
                if matrix[i][i] == 1:
                    signed[i][i] = semi
            yield tuple(tuple(row) for row in signed)


def encoded(value):
    return json.dumps(value, separators=(',', ':')).encode('ascii')


def verify(order):
    started = time.monotonic()
    graphs, counts = supports(order)
    quotients = pregraphs(graphs)
    stats = Counter()
    digest = hashlib.sha256()
    survivors = []
    for matrix in quotients:
        classification = classify(matrix)
        kind = classification[0]
        stats['ordinary:' + kind] += 1
        digest.update(encoded(('ordinary', matrix, classification)) + b'\n')
        if kind == 'full':
            survivors.append(('+', matrix))
        if kind != 'invertible':
            continue
        for signed in signings(matrix):
            classification = classify(signed)
            stats['signed:' + classification[0]] += 1
            digest.update(encoded(('signed', matrix, signed, classification)) + b'\n')
            if classification[0] == 'full':
                survivors.append(('-', signed))
    return {
        'order': order,
        'connected_subcubic_counts': counts,
        'quotient_count': len(quotients),
        'quotient_sha256': hashlib.sha256(encoded(quotients)).hexdigest(),
        'classification_counts': dict(sorted(stats.items())),
        'survivor_count': len(survivors),
        'audit_sha256': digest.hexdigest(),
        'elapsed_seconds': round(time.monotonic() - started, 3),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--order', type=int, default=8, choices=range(3, 9))
    parser.add_argument('--expect-no-survivors', action='store_true')
    args = parser.parse_args()
    report = verify(args.order)
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.expect_no_survivors and report['survivor_count']:
        raise SystemExit('A surviving case prevents the claimed exclusion.')


if __name__ == '__main__':
    main()
