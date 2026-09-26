#!/usr/bin/env python3
"""Check the catalogue against published graph6 data and determinants by subsets.

This shares the production quotient/signing enumeration. Its arithmetic is
independent (Leibniz expansion by subsets instead of elimination). The support
catalogue is compared entry by entry with the authors' nauty-generated list.
"""

import hashlib
import itertools
import json
from pathlib import Path

import verify


def graph6(line):
    values = [c - 63 for c in line.strip()]
    if not values or not 0 <= values[0] < 63:
        raise ValueError('Expected a short graph6 encoding')
    n = values[0]
    if len(values) != 1 + (n * (n - 1) // 2 + 5) // 6:
        raise ValueError('Incorrect graph6 length')
    bits = [(x >> k) & 1 for x in values[1:] for k in range(5, -1, -1)]
    a, offset = [[0] * n for _ in range(n)], 0
    for j in range(1, n):
        for i in range(j):
            a[i][j] = a[j][i] = bits[offset]
            offset += 1
    if any(bits[offset:]):
        raise ValueError('Nonzero padding')
    return a


def det_by_subsets(matrix):
    """Leibniz formula: append the column used in the next row.

    The new inversions are the previously selected columns greater than the
    appended column. No division, pivoting, or modular arithmetic is used.
    """
    n = len(matrix)
    dp = [0] * (1 << n)
    dp[0] = 1
    for mask in range(1 << n):
        row = mask.bit_count()
        if row == n or not dp[mask]:
            continue
        for column in range(n):
            if mask & (1 << column):
                continue
            inversions = (mask >> (column + 1)).bit_count()
            term = dp[mask] * matrix[row][column]
            dp[mask | (1 << column)] += -term if inversions % 2 else term
    return dp[-1]


def rank_fraction(matrix):
    from fractions import Fraction
    a = [[Fraction(x) for x in row] for row in matrix]
    row = 0
    for col in range(len(a)):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        divisor = a[row][col]
        a[row] = [x / divisor for x in a[row]]
        for i in range(row + 1, len(a)):
            multiple = a[i][col]
            a[i] = [x - multiple * y for x, y in zip(a[i], a[row])]
        row += 1
    return row


def check_matrix(matrix):
    kind, determinant, cofactors = verify.classify(matrix)
    assert det_by_subsets(matrix) == determinant
    if determinant == 0:
        rank = rank_fraction(matrix)
        if kind in ('zero-entry', 'full'):
            assert rank == len(matrix) - 1
        else:
            assert rank <= len(matrix) - 2
        for k, cofactor in enumerate(cofactors):
            minor = [[x for j, x in enumerate(row) if j != k]
                     for i, row in enumerate(matrix) if i != k]
            assert det_by_subsets(minor) == cofactor
        assert kind != 'full'
    return 1 + len(cofactors)


def main():
    fixture = Path(__file__).with_name('underlying_8.g6').read_bytes()
    assert hashlib.sha256(fixture).hexdigest() == '5d638c645a77d48c861b75bd3c29cb0765feb0ff11f4dcde16e1696ba713643e'
    published = [verify.canonical(graph6(line)) for line in fixture.splitlines() if line.strip()]
    generated, _ = verify.supports(8)
    assert len(published) == len(set(published)) == 194
    assert set(published) == set(generated)
    determinants, matrices = 0, 0
    for matrix in verify.pregraphs(generated):
        determinants += check_matrix(matrix)
        matrices += 1
        if det_by_subsets(matrix):
            for signed in verify.signings(matrix):
                determinants += check_matrix(signed)
                matrices += 1
    controls = {}
    for order in (3, 4, 5, 6, 7):
        report = verify.verify(order)
        assert bool(report['survivor_count']) == (order in (3, 6, 7))
        controls[str(order)] = report['survivor_count']
    # Canonical labelling must be invariant under relabelling; try every
    # permutation on the two three-vertex supports and six four-vertex ones.
    relabellings = 0
    for order in (3, 4):
        for matrix in verify.supports(order)[0]:
            for permutation in itertools.permutations(range(order)):
                relabelled = [[matrix[i][j] for j in permutation] for i in permutation]
                assert verify.canonical(relabelled) == matrix
                relabellings += 1
    print(json.dumps({
        'support_catalogue_matches_entrywise': True,
        'matrices_checked': matrices,
        'determinants_and_cofactors_checked': determinants,
        'small_order_survivors': controls,
        'canonical_relabellings_checked': relabellings,
        'status': 'PASS',
    }, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
