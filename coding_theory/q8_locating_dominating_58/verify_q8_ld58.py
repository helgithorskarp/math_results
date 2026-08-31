#!/usr/bin/env python3
"""Solver-free certificate for a 58-word locating-dominating code in Q_8."""

from __future__ import annotations

import itertools
from collections import Counter


DIMENSION = 8
VERTEX_COUNT = 1 << DIMENSION

CODE = frozenset(
    int(word, 2)
    for word in """
00000000 00000001 00000110 00000111 00010100 00011010 00011011 00011100
00011101 00101000 00101110 00101111 00110000 00110001 01001110
01001111 01010000 01010001 01010100 01010101 01011000 01011001 01100010
01100011 01100100 01100101 01110110 01110111 01111001 01111100 01111101 10000101
10001010 10001011 10010010 10010011 10011000 10011001 10100010 10100011
10101100 10101101 10110101 10111110 10111111 11000010 11000011 11001100
11001101 11011110 11011111 11100110 11100111 11101000 11110000
11110001 11111010 11111011
""".split()
)

BASE_CODE = frozenset(
    int(word, 2)
    for word in """
0000000 0000011 0001101 0001110 0010100 0010111 0011000 0100111
0101000 0101010 0101100 0110001 0110010 0111011 0111110 1000010
1000101 1001001 1001100 1010001 1010110 1011010 1011111 1100001
1100110 1101111 1110011 1110100 1111000 1111101
""".split()
)


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
    assert len(CODE) == 58
    assert all(0 <= word < VERTEX_COUNT for word in CODE)

    # The construction is a two-for-one exchange in the two-layer lift of
    # the 30-word Q_7 code.  The last bit is the new layer coordinate.
    lift = frozenset(2 * word + layer for word in BASE_CODE for layer in (0, 1))
    assert len(lift) == 60
    assert CODE == (
        lift - {0b00101001, 0b10000100, 0b10110100, 0b11101001}
    ) | {0b00010100, 0b01111001}

    signatures = signature_distribution(CODE)
    distances = distance_distribution(CODE)
    assert signatures == Counter({1: 56, 2: 102, 3: 24, 4: 16})
    assert distances == Counter({1: 34, 2: 144, 3: 428, 4: 470,
                                 5: 305, 6: 198, 7: 74})
    assert sum(distances.values()) == 58 * 57 // 2

    print("verified: 58-word locating-dominating code in Q_8")
    print("non-codewords: 198; distinct nonempty signatures: 198")
    print("signature sizes: 1:56 2:102 3:24 4:16")
    print("pair distances: 1:34 2:144 3:428 4:470 5:305 6:198 7:74")


if __name__ == "__main__":
    main()
