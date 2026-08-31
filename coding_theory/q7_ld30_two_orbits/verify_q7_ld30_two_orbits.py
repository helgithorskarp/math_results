#!/usr/bin/env python3
"""Solver-free certificate for two inequivalent size-30 LD codes in Q_7."""

from __future__ import annotations

import itertools
import math
from collections import Counter


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION
GROUP_ORDER = VERTEX_COUNT * math.factorial(DIMENSION)

CODE_A = frozenset(
    int(word, 2)
    for word in """
0000000 0000110 0001011 0010011 0010101 0011010 0011101 0100010
0100101 0101000 0101111 0110000 0110111 0111001 0111100 1000010
1000111 1001001 1001100 1010101 1010110 1011000 1011111 1100001
1100100 1101011 1101110 1110111 1111010 1111101
""".split()
)

CODE_B = frozenset(
    int(word, 2)
    for word in """
0000000 0000011 0001101 0001110 0010100 0010111 0011000 0100111
0101000 0101010 0101100 0110001 0110010 0111011 0111110 1000010
1000101 1001001 1001100 1010001 1010110 1011010 1011111 1100001
1100110 1101111 1110011 1110100 1111000 1111101
""".split()
)


def neighborhood(vertex: int) -> frozenset[int]:
    return frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )


def signature_distribution(code: frozenset[int]) -> Counter[int]:
    assert len(code) == 30
    seen: set[frozenset[int]] = set()
    distribution: Counter[int] = Counter()
    for vertex in range(VERTEX_COUNT):
        if vertex in code:
            continue
        identifying_set = code & neighborhood(vertex)
        assert identifying_set, f"undominated vertex {vertex:07b}"
        assert identifying_set not in seen, f"repeated signature at {vertex:07b}"
        seen.add(identifying_set)
        distribution[len(identifying_set)] += 1
    assert len(seen) == 98
    return distribution


def distance_distribution(code: frozenset[int]) -> Counter[int]:
    return Counter(
        (first ^ second).bit_count()
        for first, second in itertools.combinations(sorted(code), 2)
    )


def permute_word(word: int, permutation: tuple[int, ...]) -> int:
    image = 0
    for source, destination in enumerate(permutation):
        image |= ((word >> source) & 1) << destination
    return image


def maps_between(
    source: frozenset[int], target: frozenset[int]
) -> list[tuple[tuple[int, ...], int]]:
    """Enumerate all cube automorphisms carrying source to target.

    Both displayed codes contain zero. A coordinate permutation fixes zero,
    so the translation of any such map must be a word of the target. Testing
    only those 30 translations is therefore exhaustive.
    """
    assert 0 in source and 0 in target
    maps: list[tuple[tuple[int, ...], int]] = []
    for permutation in itertools.permutations(range(DIMENSION)):
        permuted = {permute_word(word, permutation) for word in source}
        for translation in target:
            if {word ^ translation for word in permuted} == target:
                maps.append((permutation, translation))
    return maps


def main() -> None:
    signature_a = signature_distribution(CODE_A)
    signature_b = signature_distribution(CODE_B)
    assert signature_a == Counter({1: 22, 2: 54, 3: 15, 4: 6, 5: 1})
    assert signature_b == Counter({1: 20, 2: 55, 3: 16, 4: 7})
    # Signature sizes are preserved by every cube automorphism, so this
    # already proves inequivalence without trusting the group enumeration.
    assert signature_a != signature_b

    distance_a = distance_distribution(CODE_A)
    distance_b = distance_distribution(CODE_B)
    assert distance_a == Counter({1: 3, 2: 73, 3: 156, 4: 98, 5: 66, 6: 39})
    assert distance_b == Counter({1: 2, 2: 73, 3: 156, 4: 100, 5: 66, 6: 38})

    maps_a_to_b = maps_between(CODE_A, CODE_B)
    stabilizer_a = maps_between(CODE_A, CODE_A)
    stabilizer_b = maps_between(CODE_B, CODE_B)
    assert not maps_a_to_b
    assert stabilizer_a == [((0, 1, 2, 3, 4, 5, 6), 0)]
    assert stabilizer_b == [
        ((0, 1, 2, 3, 4, 5, 6), 0),
        ((0, 2, 1, 6, 5, 4, 3), 0b1111000),
    ]
    assert GROUP_ORDER == 645_120
    orbit_a = GROUP_ORDER // len(stabilizer_a)
    orbit_b = GROUP_ORDER // len(stabilizer_b)
    assert orbit_a == 645_120 and orbit_b == 322_560

    print("both size-30 codes are locating-dominating in Q_7")
    print("code A signature sizes: 1:22 2:54 3:15 4:6 5:1")
    print("code B signature sizes: 1:20 2:55 3:16 4:7")
    print("automorphisms A -> B: 0")
    print("code A stabilizer order: 1; labelled orbit size: 645120")
    print("code B stabilizer order: 2; labelled orbit size: 322560")
    print("verified: at least two automorphism orbits of size-30 codes in Q_7")


if __name__ == "__main__":
    main()
