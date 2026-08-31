#!/usr/bin/env python3
"""Solver-free verifier for a 30-word locating-dominating code in Q_7."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations


DIMENSION = 7
CODE = frozenset(
    {
        0,
        6,
        11,
        19,
        21,
        26,
        29,
        34,
        37,
        40,
        47,
        48,
        55,
        57,
        60,
        66,
        71,
        73,
        76,
        85,
        86,
        88,
        95,
        97,
        100,
        107,
        110,
        119,
        122,
        125,
    }
)


def closed_neighborhood(vertex: int) -> frozenset[int]:
    return frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )


def main() -> None:
    assert len(CODE) == 30
    signatures: dict[frozenset[int], int] = {}
    signature_sizes: Counter[int] = Counter()
    for vertex in range(1 << DIMENSION):
        if vertex in CODE:
            continue
        signature = frozenset(CODE & closed_neighborhood(vertex))
        assert signature, f"undominated non-codeword: {vertex:07b}"
        assert signature not in signatures, (
            f"equal signatures at {signatures.get(signature):07b} and {vertex:07b}"
        )
        signatures[signature] = vertex
        signature_sizes[len(signature)] += 1

    assert len(signatures) == 98
    assert signature_sizes == Counter({1: 22, 2: 54, 3: 15, 4: 6, 5: 1})

    pair_distances = Counter(
        (first ^ second).bit_count()
        for first, second in combinations(sorted(CODE), 2)
    )
    assert pair_distances == Counter({1: 3, 2: 73, 3: 156, 4: 98, 5: 66, 6: 39})

    n = DIMENSION
    lower_bound = Fraction(
        n * n * (1 << (n + 1)), n**3 + 2 * n * n + 3 * n - 2
    )
    lower_ceiling = (
        lower_bound.numerator + lower_bound.denominator - 1
    ) // lower_bound.denominator
    assert lower_bound == Fraction(3136, 115)
    assert lower_ceiling == 28

    print(f"code size: {len(CODE)}")
    print(f"non-codeword signatures: {len(signatures)} distinct, 0 empty")
    print("signature-size distribution: 1:22 2:54 3:15 4:6 5:1")
    print("unordered pair-distance distribution: 1:3 2:73 3:156 4:98 5:66 6:39")
    print(f"published lower-bound ceiling at n=7: {lower_ceiling}")
    print("verified: 28 <= gamma^LD(Q_7) <= 30")


if __name__ == "__main__":
    main()
