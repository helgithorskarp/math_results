#!/usr/bin/env python3
"""Exact finite PSD certificates; no floating-point arithmetic.

The full matrices are defined by label-equivariant integer rules.
An annihilating polynomial checked on all columns proves that every
eigenvalue is one of the listed nonnegative integers.
"""
from itertools import permutations
from math import factorial
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def matrix(k):
    require(k in (2, 3), 'k must be 2 or 3')
    indices = list(permutations(range(7), k))
    weights = [35, 14, 4] if k == 2 else [315, 126, 36, 8]
    rows = []
    for x in indices:
        row = []
        for y in indices:
            aligned = all(a not in y or a == y[i] for i, a in enumerate(x))
            value = weights[sum(a != b for a, b in zip(x, y))] if aligned else 0
            if k == 3 and set(x) == set(y):
                rel = [x.index(a) for a in y]
                inversions = sum(rel[i] > rel[j] for i in range(k) for j in range(i+1, k))
                if inversions % 2:
                    value -= 21
            row.append(value)
        rows.append(row)
    return indices, rows


def product_apply(B, roots, basis):
    v = [int(i == basis) for i in range(len(B))]
    maximum_bits = 1
    for root in roots:
        v = [sum(x * y for x, y in zip(row, v)) - root * v[i]
             for i, row in enumerate(B)]
        maximum_bits = max(maximum_bits, max(abs(x).bit_length() for x in v))
    return v, maximum_bits


def main():
    results = []
    for k, roots in [(2, [7, 15, 45, 105, 255]),
                     (3, [0, 42, 45, 117, 132, 522, 585, 882, 1755, 3252])]:
        ids, B = matrix(k)
        n = len(B)
        require(n == factorial(7)//factorial(7-k), 'dimension')
        require(all(B[i][j] == B[j][i] for i in range(n) for j in range(n)), 'symmetry')
        max_bits = 0
        # Check every column rather than relying on transitivity for the
        # mathematical implication. All entries must vanish exactly.
        for column in range(n):
            v, bits = product_apply(B, roots, column)
            require(not any(v), f'annihilation failure k={k} column={column}')
            max_bits = max(max_bits, bits)
        require(min(roots) >= 0 and len(set(roots)) == len(roots), 'nonnegative distinct roots')
        data = json.dumps(B, separators=(',', ':')).encode()
        results.append({'k': k, 'dimension': n, 'roots': roots,
                        'annihilated_columns': n, 'maximum_intermediate_bits': max_bits,
                        'integer_matrix_sha256': hashlib.sha256(data).hexdigest()})
    result = {'status': 'exact PSD certificates verified', 'matrices': results}
    expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())['spectral']
    require(result == expected, 'EXPECTED.json spectral mismatch')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
