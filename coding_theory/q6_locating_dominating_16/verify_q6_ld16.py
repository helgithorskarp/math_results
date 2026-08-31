#!/usr/bin/env python3
"""Solver-free certificate checker for gamma^LD(Q_6) = 16."""

from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction


DIMENSION = 6
EXPECTED_WORDS = {
    "000000", "000101", "001011", "001110",
    "010010", "010111", "011001", "011100",
    "100010", "100100", "101001", "101111",
    "110011", "110101", "111000", "111110",
}


def algebraic_code() -> set[int]:
    """Return C, encoding the displayed word x1...x6 as a binary integer."""
    code: set[int] = set()
    for x1 in (0, 1):
        for x4 in (0, 1):
            for x5 in (0, 1):
                for x6 in (0, 1):
                    x2 = x1 ^ x4 ^ x5 ^ x6
                    x3 = x1 ^ x4 ^ x6 ^ (x1 & x5) ^ (x1 & x6)
                    word = (x1, x2, x3, x4, x5, x6)
                    code.add(int("".join(map(str, word)), 2))
    return code


def closed_neighborhood(vertex: int) -> set[int]:
    return {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-signatures", action="store_true")
    args = parser.parse_args()

    code = algebraic_code()
    expected = {int(word, 2) for word in EXPECTED_WORDS}
    assert code == expected
    assert len(code) == 16

    signatures: dict[frozenset[int], int] = {}
    sizes: Counter[int] = Counter()
    for vertex in range(1 << DIMENSION):
        if vertex in code:
            continue
        signature = frozenset(code & closed_neighborhood(vertex))
        assert signature, f"undominated non-codeword: {vertex:06b}"
        assert signature not in signatures, (
            f"equal signatures at {signatures.get(signature):06b} and {vertex:06b}"
        )
        signatures[signature] = vertex
        sizes[len(signature)] += 1
        if args.show_signatures:
            words = " ".join(f"{word:06b}" for word in sorted(signature))
            print(f"{vertex:06b}: {words}")

    assert len(signatures) == 48
    assert sizes == Counter({1: 16, 2: 16, 3: 16})

    n = DIMENSION
    lower_bound = Fraction(n * n * (1 << (n + 1)), n**3 + 2 * n * n + 3 * n - 2)
    lower_ceiling = (lower_bound.numerator + lower_bound.denominator - 1) // lower_bound.denominator
    assert lower_ceiling == 16

    print(f"code size: {len(code)}")
    print(f"non-codeword signatures: {len(signatures)} distinct, 0 empty")
    print("signature-size distribution: 1:16 2:16 3:16")
    print(f"published lower-bound ceiling at n=6: {lower_ceiling}")
    print("verified: gamma^LD(Q_6) = 16")


if __name__ == "__main__":
    main()
