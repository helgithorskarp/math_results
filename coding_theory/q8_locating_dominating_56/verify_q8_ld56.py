#!/usr/bin/env python3
"""Solver-free certificate for a 56-word locating-dominating code in Q_8."""

from __future__ import annotations

import itertools
from collections import Counter
from fractions import Fraction


DIMENSION = 8
VERTEX_COUNT = 1 << DIMENSION

WORDS = """
00000000 00000011 00001111 00010101 00010110 00011001 00011100
00100110 00101001 00101010 00110000 00111011 00111101 01000110
01001011 01001101 01010000 01011010 01011111 01100010 01100100
01100111 01101001 01110001 01110101 01111000 01111110 10000010
10000101 10001000 10001110 10010001 10010100 10011111 10100011
10100101 10101011 10101100 10110010 10110111 10111000 10111111
11000001 11000101 11000111 11001000 11010011 11011010 11011100
11011101 11100000 11101101 11101110 11110000 11110110 11111011
""".split()

CODE = frozenset(int(word, 2) for word in WORDS)


def closed_neighborhood(vertex: int) -> frozenset[int]:
    return frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )


def signature_distribution(code: frozenset[int]) -> Counter[int]:
    seen: set[frozenset[int]] = set()
    distribution: Counter[int] = Counter()
    for vertex in range(VERTEX_COUNT):
        if vertex in code:
            continue
        signature = code & closed_neighborhood(vertex)
        assert signature, f"undominated vertex {vertex:08b}"
        assert signature not in seen, f"repeated signature at {vertex:08b}"
        seen.add(signature)
        distribution[len(signature)] += 1
    assert len(seen) == VERTEX_COUNT - len(code)
    return distribution


def distance_distribution(code: frozenset[int]) -> Counter[int]:
    return Counter(
        (first ^ second).bit_count()
        for first, second in itertools.combinations(sorted(code), 2)
    )


def main() -> None:
    assert len(WORDS) == len(CODE) == 56
    assert all(len(word) == DIMENSION and set(word) <= {"0", "1"} for word in WORDS)

    signatures = signature_distribution(CODE)
    distances = distance_distribution(CODE)
    assert signatures == Counter({1: 48, 2: 95, 3: 46, 4: 9, 5: 2})
    assert distances == Counter(
        {1: 13, 2: 156, 3: 405, 4: 399, 5: 321, 6: 198, 7: 44, 8: 4}
    )
    assert sum(distances.values()) == 56 * 55 // 2

    # Count code/non-code incidences two ways.  Each codeword is incident
    # with itself, its eight cube neighbors, and both ends of every internal
    # code edge are removed from the code/non-code boundary.
    incidence_count = sum(size * count for size, count in signatures.items())
    assert incidence_count + len(CODE) + 2 * distances[1] == 9 * len(CODE)

    lower_bound = Fraction(8**2 * 2**9, 8**3 + 2 * 8**2 + 3 * 8 - 2)
    assert lower_bound == Fraction(16384, 331)
    assert (lower_bound.numerator + lower_bound.denominator - 1) // lower_bound.denominator == 50

    print("verified: 56-word locating-dominating code in Q_8")
    print("non-codewords: 200; distinct nonempty signatures: 200")
    print("signature sizes: 1:48 2:95 3:46 4:9 5:2")
    print("pair distances: 1:13 2:156 3:405 4:399 5:321 6:198 7:44 8:4")
    print("incidence check: 422 + 56 + 2*13 = 9*56 = 504")
    print("certified interval: 50 <= gamma^LD(Q_8) <= 56")


if __name__ == "__main__":
    main()
