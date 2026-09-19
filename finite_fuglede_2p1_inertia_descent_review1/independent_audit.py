#!/usr/bin/env python3
"""Independent exact audits for the 2p+1 positive-inertia descent review.

This deliberately does not import the target checker.  It tests the finite
profile reduction, block-Gram inertia, the general PSD-difference inertia
bound on an exhaustive smallest factor space, cyclotomic field degrees, and
the graph-lift tiling step using only standard-library exact arithmetic.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import gcd


def partitions(total: int, length: int, least: int = 1):
    if length == 0:
        if total == 0:
            yield ()
        return
    for first in range(least, total // length + 1):
        for rest in partitions(total - first, length - 1, first):
            yield (first,) + rest


def admissible_profiles(p: int):
    return tuple(
        q
        for q in partitions(2 * p + 1, p)
        if 1 not in q or all(x == 1 or x >= p for x in q)
    )


def transpose(a):
    return [list(row) for row in zip(*a)]


def matmul(a, b):
    bt = transpose(b)
    return [[sum(x * y for x, y in zip(row, col)) for col in bt] for row in a]


def subtract(a, b):
    return [[x - y for x, y in zip(arow, brow)] for arow, brow in zip(a, b)]


def rank(matrix) -> int:
    a = [[Fraction(x) for x in row] for row in matrix]
    rows = len(a)
    cols = len(a[0]) if rows else 0
    pivot_row = 0
    for col in range(cols):
        pivot = next((i for i in range(pivot_row, rows) if a[i][col]), None)
        if pivot is None:
            continue
        a[pivot_row], a[pivot] = a[pivot], a[pivot_row]
        d = a[pivot_row][col]
        a[pivot_row] = [x / d for x in a[pivot_row]]
        for i in range(rows):
            if i != pivot_row and a[i][col]:
                c = a[i][col]
                a[i] = [x - c * y for x, y in zip(a[i], a[pivot_row])]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def swap_symmetric(a, i: int, j: int) -> None:
    if i == j:
        return
    a[i], a[j] = a[j], a[i]
    for row in a:
        row[i], row[j] = row[j], row[i]


def inertia(matrix) -> tuple[int, int, int]:
    """Exact inertia by symmetric congruence, including zero 2x2 pivots."""
    a = [[Fraction(x) for x in row] for row in matrix]
    n = len(a)
    assert all(len(row) == n for row in a)
    assert all(a[i][j] == a[j][i] for i in range(n) for j in range(n))
    pos = neg = zero = 0
    k = 0
    while k < n:
        diagonal = next((i for i in range(k, n) if a[i][i]), None)
        if diagonal is not None:
            swap_symmetric(a, k, diagonal)
            d = a[k][k]
            pos += d > 0
            neg += d < 0
            for i in range(k + 1, n):
                for j in range(i, n):
                    a[i][j] -= a[i][k] * a[k][j] / d
                    a[j][i] = a[i][j]
            k += 1
            continue
        offdiag = next(
            ((i, j) for i in range(k, n) for j in range(i + 1, n) if a[i][j]),
            None,
        )
        if offdiag is None:
            zero += n - k
            break
        i, j = offdiag
        swap_symmetric(a, k, i)
        if j == k:
            j = i
        swap_symmetric(a, k + 1, j)
        d = a[k][k + 1]
        assert a[k][k] == a[k + 1][k + 1] == 0 and d
        pos += 1
        neg += 1
        for i in range(k + 2, n):
            for j in range(i, n):
                correction = (a[i][k] * a[k + 1][j] + a[i][k + 1] * a[k][j]) / d
                a[i][j] -= correction
                a[j][i] = a[i][j]
        k += 2
    return pos, neg, zero


def block_gram(p: int, r: int):
    s = p - 1
    k = r + s
    g = [[0] * k for _ in range(k)]
    for i in range(r):
        for j in range(r):
            g[i][j] = (k if i == j else 0) - s
    for i in range(r, k):
        for j in range(r, k):
            g[i][j] = (r - 1 if i == j else 0) + 1
    for i in range(r):
        for j in range(r, k):
            g[i][j] = g[j][i] = 1
    return g


def quadratic(matrix, vector):
    return sum(vector[i] * matrix[i][j] * vector[j]
               for i in range(len(vector)) for j in range(len(vector)))


def euler_phi(n: int) -> int:
    result = n
    q = 2
    while q * q <= n:
        if n % q == 0:
            while n % q == 0:
                n //= q
            result -= result // q
        q += 1
    if n > 1:
        result -= result // n
    return result


def check_profiles(records: list[str]) -> None:
    expected3 = ((1, 1, 5), (1, 3, 3), (2, 2, 3))
    assert admissible_profiles(3) == expected3
    records.append("p=3 profiles=(1,1,5),(1,3,3),(2,2,3) boundary-not-closed")
    for p in (5, 7, 11, 13, 17, 19, 23):
        got = admissible_profiles(p)
        want = ((1,) * (p - 1) + (p + 2,), (2,) * (p - 1) + (3,))
        assert got == want
        records.append(f"p={p} surviving_profiles=2")


def check_block_gram(records: list[str]) -> None:
    cases = 0
    for p in (3, 5, 7, 11, 13):
        for r in range(2, 2 * p + 4):
            g = block_gram(p, r)
            k = r + p - 1
            assert inertia(g) == (k - 1, 1, 0)
            witness = [k - 1] * r + [-r] * (p - 1)
            want = -r * (k - 1) * (r - 1) * (p - 2) * k
            assert quadratic(g, witness) == want < 0
            cases += 1
    records.append(f"block_gram_cases={cases} exact_inertia=(k-1,1,0)")


def check_psd_difference_bound(records: list[str]) -> None:
    """Exhaust the smallest nontrivial integer Gram-factor universe."""
    rows3 = tuple(product((-1, 0, 1), repeat=2))
    factors3 = tuple(tuple(rows) for rows in product(rows3, repeat=3))
    rows2 = tuple(product((-1, 0, 1), repeat=2))
    factors2 = tuple(tuple(rows) for rows in product(rows2, repeat=2))
    cases = 0
    for x in factors3:
        v = matmul(transpose(x), x)
        rv = rank(v)
        for y in factors2:
            w = matmul(transpose(y), y)
            assert inertia(subtract(v, w))[0] <= rv
            cases += 1
    assert cases == 59049
    records.append(f"psd_difference_factor_pairs={cases} positive_index_le_rankV")


def check_field_degrees(records: list[str]) -> None:
    cases = 0
    for p in (3, 5, 7, 11, 13):
        for d in range(1, 121):
            if gcd(d, p) == 1:
                assert euler_phi(d * p) == euler_phi(d) * (p - 1)
                cases += 1
    records.append(f"coprime_cyclotomic_degree_cases={cases}")


def is_unique_tiling(a, t, n: int, p: int) -> bool:
    sums = [((x + u) % n, (y + v) % p) for x, y in a for u, v in t]
    return len(sums) == n * p and len(set(sums)) == n * p


def check_graph_lifts(records: list[str]) -> None:
    lift_cases = 0
    examples = (
        (6, 5, (0, 2, 4), (0, 1)),
        (6, 5, (0, 3), (0, 1, 2)),
    )
    for n, p, b, c in examples:
        assert {(x + y) % n for x in b for y in c} == set(range(n))
        assert len(b) * len(c) == n
        complement = tuple((x, y) for x in c for y in range(p))
        for values in product(range(p), repeat=len(b)):
            graph = tuple(zip(b, values))
            assert is_unique_tiling(graph, complement, n, p)
            lift_cases += 1
    assert lift_cases == 150
    records.append(f"graph_lift_functions={lift_cases} all_tile_uniquely")


def check_small_boundaries(records: list[str]) -> None:
    # At p=5,n=3,k=11, every 11-subset of Z_15 has a collision after
    # projection to Z_3.  Such a collision would force Phi_5 into the
    # opposite 11-point mask, impossible because Phi_5(1)=5 does not divide 11.
    collision_cases = 0
    for subset in combinations(range(15), 11):
        residues = [x % 3 for x in subset]
        assert len(set(residues)) < len(residues)
        collision_cases += 1
    assert collision_cases == 1365 and 11 % 5

    # Positive example at p=5,n=11: a graph over all of Z_11 has spectrum
    # Z_11 x {0}; orthogonality is the complete residue sum modulo 11.
    graph = tuple((x, x * x % 5) for x in range(11))
    spectrum = tuple((u, 0) for u in range(11))
    for i, left in enumerate(spectrum):
        for right in spectrum[i + 1:]:
            difference = (left[0] - right[0]) % 11
            residues = [difference * x % 11 for x, _ in graph]
            assert sorted(residues) == list(range(11))
    complement = ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))
    assert is_unique_tiling(graph, complement, 11, 5)
    records.append(
        f"small_boundaries=Z15_collision_subsets:{collision_cases},Z55_graph_pair:verified"
    )


def main() -> None:
    records: list[str] = []
    check_profiles(records)
    check_block_gram(records)
    check_psd_difference_bound(records)
    check_field_degrees(records)
    check_graph_lifts(records)
    check_small_boundaries(records)
    for record in records:
        print(record)
    digest = sha256(("\n".join(records) + "\n").encode()).hexdigest()
    print(f"review_audit_sha256={digest}")
    print("ALL_INDEPENDENT_AUDITS_PASS")


if __name__ == "__main__":
    main()
