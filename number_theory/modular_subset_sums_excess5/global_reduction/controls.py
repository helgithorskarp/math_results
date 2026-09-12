#!/usr/bin/env python3
"""Independent literal sums and direct matrix determinants for proof controls.

No import of sieve.py; no floating point or computer algebra dependency.
"""
from itertools import combinations
from math import gcd


def subset_sums(values, N):
    values = list(values)
    sums = [0]
    for a in values:
        sums += [(s + a) % N for s in sums]
    return sums


def sign_classes(values, N):
    return tuple(sorted(min(a % N, -a % N) for a in values))


def centered_holes(values, N):
    sums = subset_sums(values, N)
    assert len(sums) == len(set(sums))
    center = sum(values) * pow(2, -1, N) % N
    return tuple(sorted((x - center) % N for x in set(range(N)) - set(sums)))


def has_cycle(values, N):
    vertices = set(sign_classes(values, N))
    for a in vertices:
        visited = set()
        while a in vertices:
            if a in visited:
                return True
            visited.add(a)
            a = min(2 * a % N, -2 * a % N)
    return False


def determinant_mod(matrix, p):
    """Direct Gaussian elimination over F_p, independent of spectral products."""
    rows = [row[:] for row in matrix]
    value = 1
    for i in range(len(rows)):
        pivot = next((j for j in range(i, len(rows)) if rows[j][i] % p), None)
        if pivot is None:
            return 0
        if pivot != i:
            rows[pivot], rows[i] = rows[i], rows[pivot]
            value = -value
        a = rows[i][i] % p
        value = value * a % p
        inverse = pow(a, -1, p)
        for j in range(i + 1, len(rows)):
            factor = rows[j][i] * inverse % p
            if factor:
                rows[j] = [(x - factor * y) % p for x, y in zip(rows[j], rows[i])]
    return value % p


def matrix_controls():
    counts = []
    for N, p, root in [(37, 149, 16), (69, 139, 4)]:
        surviving = []
        candidates = [b for b in range(2, N // 2 + 1) if gcd(b, N) in (1, 3)]
        for b in candidates:
            holes = {0, 1, N - 1, b, N - b}
            matrix = [[int((i - j) % N in holes) for j in range(N)] for i in range(N)]
            determinant = determinant_mod(matrix, p)
            # Independent scalar evaluation with modular powers, not the recurrence.
            spectral = 5
            for j in range(1, N):
                spectral = spectral * sum(pow(root, j * h % N, p) for h in holes) % p
            assert determinant == spectral
            if determinant == (20 if gcd(b, N) == 3 else 5):
                surviving.append(b)
        counts.append({'N': N, 'matrices_checked': len(candidates),
                       'survivors': surviving})
    return counts


def sharpness_controls():
    result = []
    for k in range(1, 7):
        d = 2 ** k + 1
        N, n, t = d * d, 2 * k, 2 * d - 1
        powers = [2 ** i for i in range(k)]
        A = powers + [d * a for a in powers]
        sums = subset_sums(A, N)
        assert len(sums) == len(set(sums)) == 2 ** n
        assert N == 2 ** n + t and 4 * 2 ** n == (t - 1) ** 2
        assert has_cycle(A, N)
        assert set(sums) == {x + d * y for x in range(d - 1) for y in range(d - 1)}
        result.append({'k': k, 'n': n, 'N': N, 't': t,
                       'subset_sums': len(sums), 'cycle_present': True})
    # A proper-subgroup move is genuinely nontrivial at the sharp boundary.
    N, d = 289, 17
    A = [1, 2, 4, 8, 17, 34, 68, 136]
    B = [1, 2, 4, 8] + [d * ((3 * 2 ** i) % d) for i in range(4)]
    assert sign_classes(A, N) != sign_classes(B, N)
    assert centered_holes(A, N) == centered_holes(B, N)
    assert set(subset_sums(B, N)) == {(s - 34) % N for s in subset_sums(A, N)}
    return {'sharp_family': result,
            'proper_subgroup_boundary_example': {'N': N, 'A': A, 'B': B,
                                                'subset_sum_translation': -34,
                                                'same_centered_holes': True,
                                                'different_sign_classes': True}}


def finite_theorem_controls():
    results = []
    for t in [3, 5, 7, 9]:
        for n in range(2, 6):
            N = 2 ** n + t
            count, seen = 0, {}
            above_threshold = 4 * 2 ** n > (t - 1) ** 2
            for A in combinations(range(1, N // 2 + 1), n):
                sums = subset_sums(A, N)
                if len(sums) != len(set(sums)):
                    continue
                count += 1
                if above_threshold:
                    assert not has_cycle(A, N)
                    holes = centered_holes(A, N)
                    assert holes not in seen
                    seen[holes] = A
            results.append({'n': n, 't': t, 'N': N, 'admissible_sign_classes': count,
                            'strict_threshold_holds': above_threshold,
                            'centered_hole_injectivity_checked': above_threshold})
    return results


def known_type_controls():
    result = []
    for n in range(5, 11):
        N = 2 ** n + 5
        powers = [2 ** i for i in range(n)]
        types = [powers, powers[:-1] + [powers[-1] + 1],
                 powers[:-2] + [powers[-2] + 1, powers[-1] + 1]]
        expected_pairs = [(1, 2), (1, 3), (3, 4)]
        for kind, A in enumerate(types):
            holes = centered_holes(A, N)
            expected = {0, expected_pairs[kind][0], -expected_pairs[kind][0] % N,
                        expected_pairs[kind][1], -expected_pairs[kind][1] % N}
            unit = [1, 2, 4][kind]
            assert {unit * h % N for h in holes} == expected
            result.append({'n': n, 'type': kind, 'hole_dilation': unit})
    return result


def check():
    return {'status': 'INDEPENDENT_ALGEBRAIC_CONTROLS_VERIFIED',
            'matrix_controls': matrix_controls(),
            'sharpness': sharpness_controls(),
            'finite_theorem_controls': finite_theorem_controls(),
            'known_type_controls': known_type_controls()}
