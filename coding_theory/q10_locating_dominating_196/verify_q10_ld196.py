#!/usr/bin/env python3
"""Direct certificate checker for the 196-word LD code in Q_10."""

from __future__ import annotations

import collections
import itertools
import pathlib


DIMENSION = 10
VERTEX_COUNT = 1 << DIMENSION
CODE_PATH = pathlib.Path(__file__).with_name("code.txt")


def closed_neighborhood(vertex: int) -> frozenset[int]:
    return frozenset(
        {vertex, *(vertex ^ (1 << coordinate) for coordinate in range(DIMENSION))}
    )


def main() -> None:
    words = CODE_PATH.read_text(encoding="ascii").split()
    assert all(len(word) == DIMENSION and set(word) <= {"0", "1"} for word in words)
    code = frozenset(int(word, 2) for word in words)
    assert len(words) == len(code) == 196

    signatures: dict[frozenset[int], int] = {}
    signature_sizes: collections.Counter[int] = collections.Counter()
    incidence_count = 0
    for vertex in range(VERTEX_COUNT):
        if vertex in code:
            continue
        signature = code & closed_neighborhood(vertex)
        assert signature, f"undominated non-codeword {vertex:010b}"
        assert signature not in signatures, (
            f"duplicate signature for {signatures[signature]:010b} and {vertex:010b}"
        )
        signatures[signature] = vertex
        signature_sizes[len(signature)] += 1
        incidence_count += len(signature)

    assert len(signatures) == 828
    assert signature_sizes == {1: 162, 2: 403, 3: 201, 4: 55, 5: 7}

    distance_counts: collections.Counter[int] = collections.Counter(
        (first ^ second).bit_count()
        for first, second in itertools.combinations(sorted(code), 2)
    )
    expected_distances = {
        1: 67,
        2: 722,
        3: 2574,
        4: 3895,
        5: 4450,
        6: 4092,
        7: 2311,
        8: 781,
        9: 198,
        10: 20,
    }
    assert distance_counts == expected_distances
    assert sum(distance_counts.values()) == 196 * 195 // 2

    internal_edges = distance_counts[1]
    assert incidence_count == 1826
    assert incidence_count + len(code) + 2 * internal_edges == 11 * len(code)

    # Junnila--Laihonen--Lehtila: gamma^LD(Q_n) >= 2^(n+1)/(n+2), n >= 10.
    lower_bound = ((1 << (DIMENSION + 1)) + DIMENSION + 1) // (DIMENSION + 2)
    assert lower_bound == 171

    print("verified: 196-word locating-dominating code in Q_10")
    print("non-codewords: 828; distinct nonempty signatures: 828")
    print(
        "signature sizes:",
        " ".join(f"{size}:{signature_sizes[size]}" for size in sorted(signature_sizes)),
    )
    print(
        "pair distances:",
        " ".join(f"{distance}:{distance_counts[distance]}" for distance in range(1, 11)),
    )
    print("incidence check: 1826 + 196 + 2*67 = 11*196 = 2156")
    print("certified interval: 171 <= gamma^LD(Q_10) <= 196")


if __name__ == "__main__":
    main()
