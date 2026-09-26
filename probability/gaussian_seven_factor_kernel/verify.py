#!/usr/bin/env python3
"""Independent exact polynomial reconstruction and fraction-free PSD check.

This verifier uses a second matrix construction and Bareiss congruence;
it does not use the spectral roots or their annihilation test.
"""
from collections import defaultdict
from fractions import Fraction as Q
from itertools import combinations, permutations
import hashlib
import json
from pathlib import Path


def require(ok, message):
    if not ok:
        raise ValueError(message)


def entry_monomial(left, right):
    return tuple(sorted(tuple(sorted(pair)) for pair in zip(left, right)))


def alternate_matrix(k):
    ids = list(permutations(range(7), k))
    B = [[0] * len(ids) for _ in ids]
    numerator = {2: [35, 14, 4], 3: [315, 126, 36, 8]}[k]
    for i, left in enumerate(ids):
        for j, right in enumerate(ids):
            mon = entry_monomial(left, right)
            loops = [a for a, b in mon if a == b]
            edges = [(a, b) for a, b in mon if a != b]
            vertices = loops + [v for e in edges for v in e]
            if len(vertices) == len(set(vertices)):
                B[i][j] += numerator[len(edges)]
            if k == 3:
                # The correction is exactly an odd permutation of one
                # 3-set: one loop and the other edge occurring twice.
                if len(loops) == 1 and len(edges) == 2 and edges[0] == edges[1]:
                    B[i][j] -= 21
    return ids, B


def bareiss_psd(matrix):
    A = [row[:] for row in matrix]
    n = len(A)
    previous = 1
    pivots = []
    rank = 0
    maxbits = 1
    for k in range(n):
        require(all(A[i][i] >= 0 for i in range(k, n)), 'negative residual diagonal')
        pivot_index = next((i for i in range(k, n) if A[i][i]), None)
        if pivot_index is None:
            require(all(A[i][j] == 0 for i in range(k, n) for j in range(k, n)),
                    'nonzero residual at zero diagonal')
            break
        if pivot_index != k:
            A[k], A[pivot_index] = A[pivot_index], A[k]
            for row in A:
                row[k], row[pivot_index] = row[pivot_index], row[k]
        pivot = A[k][k]
        require(pivot > 0 and previous > 0, 'nonpositive Bareiss pivot')
        pivots.append(pivot)
        for i in range(k + 1, n):
            for j in range(i, n):
                value, remainder = divmod(pivot * A[i][j] - A[i][k] * A[k][j], previous)
                require(remainder == 0, 'nonexact Bareiss division')
                A[i][j] = A[j][i] = value
                maxbits = max(maxbits, abs(value).bit_length())
        for i in range(k+1, n):
            A[k][i] = A[i][k] = 0
        previous = pivot
        rank += 1
    return rank, maxbits, hashlib.sha256(json.dumps(pivots, separators=(',', ':')).encode()).hexdigest()


def target_polynomial(k):
    # Select diagonal vertices first, then a subset of remaining vertices
    # and a perfect matching. This reverses the production enumeration.
    out = defaultdict(Q)
    alpha = Q(5, 2)
    for m in range(k + 1):
        coef = Q(1, 2 ** (k-m))
        for h in range(m):
            coef /= alpha+h
        for diagonal in combinations(range(7), k-m):
            remaining = [i for i in range(7) if i not in diagonal]
            for endpoints in combinations(remaining, 2*m):
                for pairing in perfect_matchings(endpoints):
                    mon = tuple(sorted([(i, i) for i in diagonal] + list(pairing)))
                    out[mon] += coef
    return dict(out)


def perfect_matchings(labels):
    if not labels:
        yield ()
    else:
        a = labels[0]
        for b in labels[1:]:
            for rest in perfect_matchings(tuple(i for i in labels[1:] if i != b)):
                yield ((a, b),) + rest


def matrix_polynomial(ids, matrix, denominator):
    out = defaultdict(Q)
    for i, left in enumerate(ids):
        for j, right in enumerate(ids):
            if matrix[i][j]:
                out[entry_monomial(left, right)] += Q(matrix[i][j], denominator)
    return out


def main():
    records = []
    for k, denominator, expected_rank in [(2, 280, 42), (3, 15120, 190)]:
        ids, B = alternate_matrix(k)
        got = matrix_polynomial(ids, B, denominator)
        if k == 3:
            # Add 63*(per-det) /15120 = 126/15120 times
            # G_ii G_jk^2 for each choice of singleton in a triple.
            for triple in combinations(range(7), 3):
                for i in triple:
                    j, h = [v for v in triple if v != i]
                    got[tuple(sorted([(i, i), (j, h), (j, h)]))] += Q(126, denominator)
        got = {m: c for m, c in got.items() if c}
        require(got == target_polynomial(k), f'coefficient identity k={k}')
        rank, bits, pivot_hash = bareiss_psd(B)
        require(rank == expected_rank, 'rank mismatch')
        records.append({'k': k, 'dimension': len(ids), 'exact_rank': rank,
                        'polynomial_terms': len(got), 'maximum_residual_bits': bits,
                        'positive_pivot_stream_sha256': pivot_hash,
                        'integer_matrix_sha256': hashlib.sha256(json.dumps(B, separators=(',', ':')).encode()).hexdigest()})
    # Homogeneous decomposition and inversion are compared coefficientwise.
    # Import only the matching generator, not either matrix construction.
    from audit_recentring import polynomial, rising
    forms = [target_polynomial(k) for k in range(8)]
    total = 0
    for coef, pairs, diagonal in polynomial(7):
        degree = len(pairs) + len(diagonal)
        mon = tuple(sorted(list(pairs) + [(i, i) for i in diagonal]))
        require(coef == rising(Q(5, 2), 7-degree) * forms[degree][mon],
                'homogeneous decomposition')
        total += 1
    inversion_terms = 0
    for k in range(4):
        transformed = {}
        for mon, coef in forms[k].items():
            edges = [(a,b) for a,b in mon if a != b]
            used = {v for pair in mon for v in pair}
            opposite = tuple(sorted(edges + [(i,i) for i in range(7) if i not in used]))
            transformed[opposite] = coef * Q(2) ** (2*k-7)
            inversion_terms += 1
        require(transformed == forms[7-k], 'inversion identity')
    rejected = 0
    for bad in [[[-1]], [[0,1],[1,0]], [[1,2],[2,1]]]:
        try:
            bareiss_psd(bad)
        except ValueError:
            rejected += 1
        else:
            raise ValueError('indefinite matrix was accepted')
    result = {'status': 'exact coefficient and independent PSD checks passed', 'matrices': records,
              'homogeneous_terms': total, 'inversion_terms': inversion_terms,
              'indefinite_matrices_rejected': rejected}
    expected = json.loads(Path(__file__).with_name('EXPECTED.json').read_text())['algebra']
    require(result == expected, 'EXPECTED.json algebra mismatch')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
