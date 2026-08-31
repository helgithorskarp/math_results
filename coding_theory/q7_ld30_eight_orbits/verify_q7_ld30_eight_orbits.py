#!/usr/bin/env python3
"""Solver-free certificate for eight inequivalent size-30 LD codes in Q_7."""

from __future__ import annotations

import itertools
import math
from collections import Counter


DIMENSION = 7
VERTEX_COUNT = 1 << DIMENSION
GROUP_ORDER = VERTEX_COUNT * math.factorial(DIMENSION)


def words(text: str) -> frozenset[int]:
    return frozenset(int(word, 2) for word in text.split())


CODES = (
    words(
        """
0000000 0000001 0000110 0001010 0001111 0010011 0011100 0100011
0100100 0101101 0110010 0110101 0111000 0111011 0111110 1000011
1000101 1000110 1001100 1010100 1011001 1011010 1011111 1100000
1101001 1101010 1101111 1110001 1110111 1111100
"""
    ),
    words(
        """
0000000 0000001 0000100 0001111 0010011 0010101 0011001 0011010
0100111 0101010 0101101 0110000 0110110 0111011 0111100 1000010
1000101 1001011 1001100 1010000 1010110 1011111 1100011 1100100
1101000 1101110 1110001 1110111 1111010 1111101
"""
    ),
    words(
        """
0000000 0000101 0001011 0001100 0010010 0010111 0011001 0011110
0100001 0100111 0101110 0110100 0111000 0111011 0111101 1000011
1000110 1001010 1001101 1010000 1010101 1011011 1100010 1100100
1101001 1101111 1110001 1110110 1111010 1111100
"""
    ),
    words(
        """
0000000 0000001 0000110 0000111 0001100 0010011 0010100 0011010
0011101 0100101 0101011 0110010 0111001 0111100 0111111 1000001
1000010 1000100 1001011 1010111 1011000 1011110 1100011 1101000
1101101 1101110 1110000 1110101 1110110 1111011
"""
    ),
    words(
        """
0000000 0000010 0000111 0001001 0001100 0001110 0010010 0010100
0011000 0011110 0100101 0101010 0110001 0110110 0111011 0111101
1000101 1001000 1001011 1010001 1010110 1011101 1100011 1100110
1101001 1101111 1110000 1110111 1111010 1111100
"""
    ),
    words(
        """
0000000 0000001 0000010 0000111 0001101 0010101 0011011 0011100
0100100 0100101 0100110 0101000 0101011 0110010 0111001 0111111
1000100 1001011 1001110 1010011 1010110 1011000 1011101 1100010
1101001 1101111 1110000 1110111 1111010 1111100
"""
    ),
    words(
        """
0000000 0000011 0000101 0001001 0001110 0010111 0011010 0011100
0100111 0101000 0110001 0110010 0110100 0111111 1000110 1001000
1001111 1010001 1010010 1010100 1011110 1100001 1101010 1101011
1101100 1101101 1110000 1110111 1111011 1111101
"""
    ),
    words(
        """
0000000 0000001 0001010 0001111 0010011 0010110 0011000 0011101
0100011 0101001 0101100 0101110 0110010 0110100 0111111 1000011
1000100 1001101 1010000 1010111 1011001 1011110 1100010 1100101
1101000 1101111 1110001 1110111 1111010 1111100
"""
    ),
)

EXPECTED_SIGNATURES = (
    Counter({1: 20, 2: 54, 3: 18, 4: 6}),
    Counter({1: 20, 2: 55, 3: 16, 4: 7}),
    Counter({1: 21, 2: 49, 3: 21, 4: 7}),
    Counter({1: 22, 2: 54, 3: 15, 4: 6, 5: 1}),
    Counter({1: 24, 2: 54, 3: 12, 4: 6, 5: 2}),
    Counter({1: 25, 2: 52, 3: 12, 4: 8, 5: 1}),
    Counter({1: 26, 2: 52, 3: 8, 4: 12}),
    Counter({1: 28, 2: 36, 3: 32, 4: 2}),
)

EXPECTED_DISTANCES = (
    Counter({1: 2, 2: 72, 3: 158, 4: 100, 5: 64, 6: 39}),
    Counter({1: 2, 2: 73, 3: 156, 4: 100, 5: 66, 6: 38}),
    Counter({2: 77, 3: 154, 4: 98, 5: 70, 6: 35, 7: 1}),
    Counter({1: 3, 2: 73, 3: 156, 4: 98, 5: 66, 6: 39}),
    Counter({1: 4, 2: 74, 3: 154, 4: 97, 5: 66, 6: 40}),
    Counter({1: 4, 2: 74, 3: 152, 4: 98, 5: 69, 6: 38}),
    Counter({1: 4, 2: 75, 3: 148, 4: 100, 5: 72, 6: 36}),
    Counter({1: 3, 2: 72, 3: 153, 4: 104, 5: 67, 6: 34, 7: 2}),
)

EXPECTED_STABILIZER_ORDERS = (2, 2, 14, 1, 4, 2, 4, 2)

# This set has pairwise-distinct signatures on its 99 non-codewords, but the
# signature of 0000100 is empty.  Every word in that vertex's closed ball
# completes it to a size-30 locating-dominating code.
ONE_DEFECT_CODE = frozenset(
    {
        2,
        8,
        11,
        13,
        21,
        25,
        30,
        33,
        39,
        46,
        51,
        52,
        58,
        61,
        65,
        70,
        74,
        80,
        83,
        92,
        95,
        98,
        100,
        105,
        111,
        117,
        118,
        120,
        123,
    }
)
DEFECT_VERTEX = 4


def neighborhood(vertex: int) -> frozenset[int]:
    return frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )


NEIGHBORHOODS = tuple(neighborhood(vertex) for vertex in range(VERTEX_COUNT))


def signature_distribution(code: frozenset[int]) -> Counter[int]:
    assert len(code) == 30
    seen: set[frozenset[int]] = set()
    distribution: Counter[int] = Counter()
    for vertex in range(VERTEX_COUNT):
        if vertex in code:
            continue
        signature = code & NEIGHBORHOODS[vertex]
        assert signature, f"undominated vertex {vertex:07b}"
        assert signature not in seen, f"repeated signature at {vertex:07b}"
        seen.add(signature)
        distribution[len(signature)] += 1
    assert len(seen) == VERTEX_COUNT - len(code)
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


def transform(
    code: frozenset[int], permutation: tuple[int, ...], translation: int
) -> frozenset[int]:
    return frozenset(
        permute_word(word, permutation) ^ translation for word in code
    )


def stabilizer(code: frozenset[int]) -> list[tuple[tuple[int, ...], int]]:
    """Enumerate the complete affine-coordinate stabilizer of a code.

    Each displayed code contains zero.  A stabilizing map sends zero to its
    translation, so it suffices to test the 30 codewords as translations.
    """
    assert 0 in code
    result: list[tuple[tuple[int, ...], int]] = []
    for permutation in itertools.permutations(range(DIMENSION)):
        permuted = frozenset(permute_word(word, permutation) for word in code)
        for translation in code:
            if frozenset(word ^ translation for word in permuted) == code:
                result.append((permutation, translation))
    return result


def verify_one_defect_bridge() -> None:
    assert len(ONE_DEFECT_CODE) == 29
    signatures: dict[frozenset[int], int] = {}
    for vertex in range(VERTEX_COUNT):
        if vertex in ONE_DEFECT_CODE:
            continue
        signature = ONE_DEFECT_CODE & NEIGHBORHOODS[vertex]
        assert signature not in signatures
        signatures[signature] = vertex
    assert signatures[frozenset()] == DEFECT_VERTEX
    assert len(signatures) == 99

    completion_profiles: Counter[tuple[tuple[int, int], ...]] = Counter()
    for added_word in sorted(NEIGHBORHOODS[DEFECT_VERTEX]):
        completion = ONE_DEFECT_CODE | {added_word}
        profile = tuple(sorted(signature_distribution(completion).items()))
        completion_profiles[profile] += 1
    assert completion_profiles == Counter(
        {
            tuple(sorted(EXPECTED_SIGNATURES[1].items())): 7,
            tuple(sorted(EXPECTED_SIGNATURES[2].items())): 1,
        }
    )


def verify_bridges_to_previous_representatives() -> None:
    previous_a = words(
        """
0000000 0000110 0001011 0010011 0010101 0011010 0011101 0100010
0100101 0101000 0101111 0110000 0110111 0111001 0111100 1000010
1000111 1001001 1001100 1010101 1010110 1011000 1011111 1100001
1100100 1101011 1101110 1110111 1111010 1111101
"""
    )
    previous_b = words(
        """
0000000 0000011 0001101 0001110 0010100 0010111 0011000 0100111
0101000 0101010 0101100 0110001 0110010 0111011 0111110 1000010
1000101 1001001 1001100 1010001 1010110 1011010 1011111 1100001
1100110 1101111 1110011 1110100 1111000 1111101
"""
    )
    assert transform(CODES[1], (1, 3, 2, 0, 4, 6, 5), 40) == previous_b
    assert transform(CODES[3], (6, 5, 1, 0, 4, 2, 3), 85) == previous_a


def main() -> None:
    assert GROUP_ORDER == 645_120
    observed_profiles: set[tuple[tuple[int, int], ...]] = set()
    orbit_sizes: list[int] = []
    for index, code in enumerate(CODES):
        assert len(code) == 30
        signatures = signature_distribution(code)
        distances = distance_distribution(code)
        assert signatures == EXPECTED_SIGNATURES[index]
        assert distances == EXPECTED_DISTANCES[index]
        assert sum(distances.values()) == math.comb(30, 2)
        # Incidence cross-check: sum over all closed balls equals 8|C|.
        assert sum(size * count for size, count in signatures.items()) + 30 + 2 * distances[1] == 8 * 30
        profile = tuple(sorted(signatures.items()))
        assert profile not in observed_profiles
        observed_profiles.add(profile)

        automorphisms = stabilizer(code)
        order = len(automorphisms)
        assert order == EXPECTED_STABILIZER_ORDERS[index]
        assert GROUP_ORDER % order == 0
        orbit_sizes.append(GROUP_ORDER // order)

    assert orbit_sizes == [
        322_560,
        322_560,
        46_080,
        645_120,
        161_280,
        322_560,
        161_280,
        322_560,
    ]
    assert sum(orbit_sizes) == 2_304_000
    verify_one_defect_bridge()
    verify_bridges_to_previous_representatives()

    print("all eight displayed sets are size-30 locating-dominating codes in Q_7")
    print("their eight signature-size distributions are pairwise distinct")
    print("stabilizer orders:", " ".join(map(str, EXPECTED_STABILIZER_ORDERS)))
    print("orbit sizes:", " ".join(map(str, orbit_sizes)))
    print("disjoint labelled solutions certified: 2304000")
    print("one-defect 29-set has seven profile-2 and one profile-3 completions")
    print("verified: at least eight automorphism orbits of size-30 codes in Q_7")


if __name__ == "__main__":
    main()
