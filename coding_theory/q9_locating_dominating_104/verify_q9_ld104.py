#!/usr/bin/env python3
"""Direct exact verifier for a 104-word locating-dominating code in Q_9."""

from collections import Counter

DIMENSION = 9
VERTEX_COUNT = 1 << DIMENSION

WORDS = """
000000011 000000111 000001001 000001110 000010000 000011010
000100001 000100100 000101010 000101100 000110110 000111011
000111101 001000100 001000111 001001010 001010010 001011100
001011101 001100000 001100110 001101101 001110001 001110101
001111000 001111111 010000010 010001101 010010100 010010101
010011001 010100011 010100100 010101000 010101111 010110000
010110111 010111110 011000001 011000110 011001000 011001011
011010011 011010100 011011111 011100100 011100101 011101011
011110010 011111001 011111010 011111100 100000010 100000101
100001111 100010001 100010110 100011100 100011111 100100000
100100111 100101001 100110011 100111010 100111110 101001001
101001100 101001111 101010000 101010011 101011011 101100011
101100110 101110011 101110100 101110101 101111010 101111101
110000001 110000100 110000111 110001000 110001010 110010010
110011011 110011100 110100010 110101101 110110101 110111001
110111110 111000010 111000111 111001101 111010101 111011000
111011110 111100001 111101000 111101011 111101110 111110000
111110110 111111111
""".split()


def closed_neighborhood(vertex: int) -> set[int]:
    return {vertex} | {vertex ^ (1 << coordinate) for coordinate in range(DIMENSION)}


def main() -> None:
    assert all(len(word) == DIMENSION and set(word) <= {"0", "1"} for word in WORDS)
    code = {int(word, 2) for word in WORDS}
    assert len(WORDS) == len(code) == 104

    signatures: dict[tuple[int, ...], int] = {}
    signature_sizes: Counter[int] = Counter()
    incidence_count = 0
    for vertex in range(VERTEX_COUNT):
        if vertex in code:
            continue
        signature = tuple(sorted(code & closed_neighborhood(vertex)))
        assert signature, f"undominated non-codeword {vertex:09b}"
        assert signature not in signatures, (
            f"equal signatures at {signatures[signature]:09b} and {vertex:09b}"
        )
        signatures[signature] = vertex
        signature_sizes[len(signature)] += 1
        incidence_count += len(signature)

    assert len(signatures) == VERTEX_COUNT - len(code) == 408

    pair_distances: Counter[int] = Counter()
    sorted_code = sorted(code)
    for index, first in enumerate(sorted_code):
        for second in sorted_code[index + 1 :]:
            pair_distances[(first ^ second).bit_count()] += 1
    assert sum(pair_distances.values()) == len(code) * (len(code) - 1) // 2

    internal_edges = pair_distances[1]
    assert incidence_count + len(code) + 2 * internal_edges == (DIMENSION + 1) * len(code)

    # Honkala--Laihonen--Ranto, Theorem 15, specialized exactly at n=9.
    numerator = DIMENSION**2 * 2 ** (DIMENSION + 1)
    denominator = DIMENSION**3 + 2 * DIMENSION**2 + 3 * DIMENSION - 2
    lower_bound = (numerator + denominator - 1) // denominator
    assert (numerator, denominator, lower_bound) == (82944, 916, 91)

    print("verified: 104-word locating-dominating code in Q_9")
    print(f"non-codewords: {len(signatures)}; distinct nonempty signatures: {len(signatures)}")
    print("signature sizes:", " ".join(f"{size}:{count}" for size, count in sorted(signature_sizes.items())))
    print("pair distances:", " ".join(f"{distance}:{count}" for distance, count in sorted(pair_distances.items())))
    print(
        f"incidence check: {incidence_count} + 104 + 2*{internal_edges} "
        f"= 10*104 = {(DIMENSION + 1) * len(code)}"
    )
    print("certified interval: 91 <= gamma^LD(Q_9) <= 104")


if __name__ == "__main__":
    main()
