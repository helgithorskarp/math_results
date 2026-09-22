#!/usr/bin/env python3
"""Exact corroborating audit; the universal proof is in THEOREM.md.

Standard library only. All checks remain active under python -O.
Binary vectors use bit i for coordinate i; subspace masks use bit v for
nonzero vector v. Adjacency rows and Plucker coordinates are also bitsets,
with their distinct index sets documented at the construction sites.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


@lru_cache(maxsize=None)
def gaussian(n: int, k: int, q: int = 2) -> int:
    require(n >= 0 and q >= 2, "invalid Gaussian parameters")
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    return gaussian(n - 1, k - 1, q) + q**k * gaussian(n - 1, k, q)


def gaussian_product(n: int, k: int, q: int = 2) -> int:
    require(n >= 0 and q >= 2, "invalid Gaussian parameters")
    if k < 0 or k > n:
        return 0
    top = bottom = 1
    for j in range(k):
        top *= q ** (n - j) - 1
        bottom *= q ** (k - j) - 1
    require(top % bottom == 0, "nonintegral Gaussian product")
    return top // bottom


def bits(mask: int):
    require(mask >= 0, "negative bitset")
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def gf2_rank(rows: list[int] | tuple[int, ...]) -> int:
    pivots: dict[int, int] = {}
    for row in rows:
        require(row >= 0, "negative binary matrix row")
        while row:
            lead = row.bit_length() - 1
            if lead not in pivots:
                pivots[lead] = row
                break
            row ^= pivots[lead]
    return len(pivots)


def span_mask(basis: tuple[int, ...]) -> int:
    vectors = [0]
    for row in basis:
        require(row > 0 and row not in vectors, "dependent or invalid basis")
        vectors += [v ^ row for v in vectors]
    return sum(1 << v for v in vectors if v)


def rref_bases(n: int, k: int) -> list[tuple[int, ...]]:
    """All RREF bases, with the pivot as the lowest occupied coordinate."""
    require(0 <= k <= n, "invalid subspace dimensions")
    result = []
    for pivots in combinations(range(n), k):
        free = [
            (i, j)
            for i, pivot in enumerate(pivots)
            for j in range(pivot + 1, n)
            if j not in pivots
        ]
        for assignment in range(1 << len(free)):
            rows = [1 << pivot for pivot in pivots]
            for b, (i, j) in enumerate(free):
                if (assignment >> b) & 1:
                    rows[i] |= 1 << j
            result.append(tuple(rows))
    return result


@lru_cache(maxsize=None)
def extension_subspaces(n: int, k: int) -> frozenset[int]:
    """Independent enumeration: extend smaller literal vector spans."""
    require(0 <= k <= n, "invalid subspace dimensions")
    if k == 0:
        return frozenset((0,))
    result: set[int] = set()
    for old in extension_subspaces(n, k - 1):
        old_vectors = tuple(bits(old))
        for v in range(1, 1 << n):
            if (old >> v) & 1:
                continue
            new = old | (1 << v)
            for w in old_vectors:
                new |= 1 << (v ^ w)
            result.add(new)
    return frozenset(result)


def adjacency_masks(spaces: list[int]) -> list[int]:
    require(len(set(spaces)) == len(spaces), "duplicate subspace")
    adjacency = [0] * len(spaces)
    for i, left in enumerate(spaces):
        for j in range(i):
            if left & spaces[j] == 0:
                adjacency[i] |= 1 << j
                adjacency[j] |= 1 << i
    return adjacency


def plucker_coordinates(basis: tuple[int, ...], n: int) -> int:
    """Minor determinants; index j is the jth lexicographic column subset."""
    k = len(basis)
    require(all(0 < row < 1 << n for row in basis), "basis outside ambient space")
    require(gf2_rank(basis) == k, "dependent Plucker basis")
    result = 0
    for j, columns in enumerate(combinations(range(n), k)):
        restricted = [
            sum(((row >> col) & 1) << pos for pos, col in enumerate(columns))
            for row in basis
        ]
        if gf2_rank(restricted) == k:
            result |= 1 << j
    return result


def complement_permutation(n: int, r: int) -> list[int]:
    require(n == 2 * r, "wedge pairing requires n=2r")
    coordinates = list(combinations(range(n), r))
    index = {cols: i for i, cols in enumerate(coordinates)}
    return [index[tuple(j for j in range(n) if j not in cols)] for cols in coordinates]


def check_factorization(adjacency: list[int], plucker: list[int], r: int) -> int:
    require(len(adjacency) == len(plucker), "factorization dimension mismatch")
    permutation = complement_permutation(2 * r, r)
    require(all(0 <= p < 1 << len(permutation) for p in plucker), "invalid Plucker row")
    paired = [sum(1 << permutation[j] for j in bits(p)) for p in plucker]
    checks = 0
    for i, row in enumerate(adjacency):
        require(0 <= row < 1 << len(adjacency), "invalid adjacency row")
        for j in range(i + 1):
            value = (plucker[i] & paired[j]).bit_count() % 2
            require(((row >> j) & 1) == value, f"wedge mismatch at {(i, j)}")
            require(((adjacency[j] >> i) & 1) == value, "asymmetric adjacency")
            checks += 1
    return checks


def check_incidence_actions(spaces: list[int], adjacency: list[int], r: int) -> int:
    """Check every Af_T count over integers, for all T of dimensions 0..r."""
    checks = 0
    mobius = [
        sum((-1)**j * 2 ** comb(j, 2) * gaussian(b, j) for j in range(b + 1))
        for b in range(r + 1)
    ]
    require(mobius == [1] + [0] * r, "subspace Mobius identity")
    for j in range(r + 1):
        for basis in rref_bases(2 * r, j):
            T = span_mask(basis)
            incidence = sum(1 << u for u, U in enumerate(spaces) if U & T == T)
            require(incidence.bit_count() == gaussian(2 * r - j, r - j), "incidence size")
            for u, U in enumerate(spaces):
                actual = (adjacency[u] & incidence).bit_count()
                intersection_size = (U & T).bit_count() + 1
                require(intersection_size & (intersection_size - 1) == 0, "bad intersection")
                b = intersection_size.bit_length() - 1
                expected = 2 ** (r * (r - j)) * mobius[b]
                require(actual == expected, f"incidence action mismatch r={r}, j={j}, u={u}")
                checks += 1
    return checks


def audit_binary_graph(r: int) -> dict[str, int]:
    require(1 <= r <= 3, "definition-level audit is bounded to r<=3")
    n = 2 * r
    bases = rref_bases(n, r)
    spaces = [span_mask(basis) for basis in bases]
    require(len(spaces) == gaussian(n, r), "RREF enumeration count")
    require(len(set(spaces)) == len(spaces), "nonunique RREF enumeration")
    require(all(U.bit_count() == 2**r - 1 for U in spaces), "subspace size")
    require(set(spaces) == extension_subspaces(n, r), "independent enumerations disagree")
    adjacency = adjacency_masks(spaces)
    N, d = len(spaces), 2 ** (r * r)
    require(all(row.bit_count() == d for row in adjacency), "degree count")
    plucker = [plucker_coordinates(basis, n) for basis in bases]
    wedge_checks = check_factorization(adjacency, plucker, r)
    rank = gf2_rank(adjacency)
    require(rank == comb(2 * r, r), "binary adjacency rank")
    incidence_checks = check_incidence_actions(spaces, adjacency, r)

    # A concrete EKR star: all spaces containing vector 1.
    star = sum(1 << i for i, U in enumerate(spaces) if (U >> 1) & 1)
    require(star.bit_count() == gaussian(2 * r - 1, r - 1), "star cardinality")
    require(all(adjacency[i] & star == 0 for i in bits(star)), "star not independent")
    return {
        "r": r,
        "vertices": N,
        "edges": N * d // 2,
        "degree": d,
        "binary_adjacency_rank": rank,
        "star_size": star.bit_count(),
        "unordered_wedge_checks_including_diagonal": wedge_checks,
        "integer_incidence_action_checks": incidence_checks,
    }


def audit_small_components() -> int:
    checks = 0
    for size in range(1, 4):
        pairs = list(combinations(range(size), 2))
        for mask in range(1 << len(pairs)):
            rows = [0] * size
            for j, (u, v) in enumerate(pairs):
                if (mask >> j) & 1:
                    rows[u] |= 1 << v
                    rows[v] |= 1 << u
            e = mask.bit_count()
            rank = gf2_rank(rows)
            require(2 * e <= 3 * rank, "three-component edge/rank inequality")
            checks += 1
    return checks


def audit_scalar_formulas() -> dict[str, object]:
    records = []
    q_values = (2, 3, 4, 5, 7, 8, 9, 11, 13, 16)
    for q in q_values:
        for r in range(1, 11):
            for n in range(2 * r, 2 * r + 6):
                N = gaussian(n, r, q)
                require(N == gaussian_product(n, r, q), "Gaussian implementations disagree")
                d = q ** (r * r) * gaussian(n - r, r, q)
                s = q ** (r * (r - 1)) * gaussian(n - r - 1, r - 1, q)
                a = gaussian(n - 1, r - 1, q)
                require(N * s == a * (d + s), "Hoffman threshold")
                require(N - a == q**r * gaussian(n - 1, r, q), "gonality Pascal identity")
                exceptional = q == 2 and n == 2 * r and r >= 2
                require((2 * d < N) if exceptional else (2 * d > N), "density classification")
                theta = [
                    (-1)**j * q ** (r * (r - j) + comb(j, 2))
                    * gaussian(n - r - j, r - j, q)
                    for j in range(r + 1)
                ]
                require(theta[0] == d and min(theta) == -s, "spectral extremes")
                if r >= 2:
                    require(max(theta[1:]) == theta[2], "nonconstant spectral maximum")
                multiplicities = [1] + [
                    gaussian(n, j, q) - gaussian(n, j - 1, q) for j in range(1, r + 1)
                ]
                require(sum(multiplicities) == N, "spectrum dimension")
                require(sum(t * m for t, m in zip(theta, multiplicities)) == 0, "spectrum trace")
                require(sum(t * t * m for t, m in zip(theta, multiplicities)) == N * d, "spectrum trace square")
                records.append((q, n, r, N, d, a))

    for r in range(3, 65):
        N = gaussian(2 * r, r)
        d, s, t = 2 ** (r * r), 2 ** (r * (r - 1)), 2 ** (r * r - 2 * r + 1)
        R = comb(2 * r, r)
        require(s > 3 * R, "rank-Hoffman inequality")
        require(2 * N < 7 * d, "Gaussian density upper bound")
        require(32 * (d - t) >= 31 * d, "Laplacian gap")
        require(5 * (d - t) * (N - 5) > 4 * d * N, "large-side cut inequality")
        require(4 * d - 12 > N, "four-egg cut beats vertex count")
        require(2 ** (2 * r) * comb(2 * r, r) > comb(2 * r + 2, r + 1), "induction growth")

    # Rank-two egg cuts: m=2 by simplicity; all other smaller sides by spectrum.
    require(2 * 16 - 2 == 30 > 28, "rank-two edge cut")
    for m in range(3, 18):
        require(14 * m * (35 - m) > 30 * 35, "rank-two spectral cut")

    canonical = json.dumps(records, separators=(",", ":"))
    return {
        "general_parameter_records": len(records),
        "general_parameter_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "prime_powers_audited": list(q_values),
        "general_rank_range": [1, 10],
        "general_excess_dimension_range": [0, 5],
        "binary_structural_rank_range": [3, 64],
        "binary_structural_checks": 62,
        "rank_two_larger_side_checks": 15,
    }


def run_audit() -> dict[str, object]:
    return {
        "status": "VERIFIED",
        "arithmetic": "exact Python integers; finite-field rank over F_2",
        "small_component_graphs": audit_small_components(),
        "scalar_formulas": audit_scalar_formulas(),
        "definition_level_graphs": [audit_binary_graph(r) for r in range(1, 4)],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare with bundled expected output")
    args = parser.parse_args()
    result = run_audit()
    if args.check:
        expected = json.loads(Path(__file__).with_name("EXPECTED_OUTPUT.json").read_text())
        require(result == expected, "expected-output mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
