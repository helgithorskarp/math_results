#!/usr/bin/env python3
"""Independent completeness audit for the 13 strict size-six signatures."""

from __future__ import annotations

from collections import Counter
import hashlib
import itertools
import json
import math


SCORE_SEQUENCES = [
    (1, 1, 1, 3, 4, 5),
    (1, 1, 1, 4, 4, 4),
    (1, 1, 2, 2, 4, 5),
    (1, 1, 2, 3, 3, 5),
    (1, 1, 2, 3, 4, 4),
    (1, 1, 3, 3, 3, 4),
    (1, 2, 2, 2, 3, 5),
    (1, 2, 2, 2, 4, 4),
    (1, 2, 2, 3, 3, 4),
    (1, 2, 3, 3, 3, 3),
    (2, 2, 2, 2, 2, 5),
    (2, 2, 2, 2, 3, 4),
    (2, 2, 2, 3, 3, 3),
]
EXPECTED_LABELED_COUNTS = [
    240,
    80,
    720,
    1440,
    2880,
    1680,
    1680,
    1680,
    8640,
    2400,
    144,
    2400,
    2640,
]
EXPECTED_SEQUENCE_SHA256 = (
    "f58605f97fb4ee29323660d0ba50c33f52cf1c674762346426517620b93e8ad1"
)
PAIRS = [(first, second) for first in range(6) for second in range(first + 1, 6)]


def landau_sequences() -> list[tuple[int, ...]]:
    """Enumerate positive score sequences using Landau's criterion."""
    return [
        scores
        for scores in itertools.combinations_with_replacement(range(1, 6), 6)
        if sum(scores) == 15
        and all(
            sum(scores[:size]) >= math.comb(size, 2)
            for size in range(1, 7)
        )
    ]


def direct_counts() -> Counter[tuple[int, ...]]:
    """Classify all 2^15 labeled tournaments directly from edge bits."""
    counts: Counter[tuple[int, ...]] = Counter()
    for bits in range(1 << len(PAIRS)):
        scores = [0] * 6
        for shift, (first, second) in enumerate(PAIRS):
            winner, loser = (
                (first, second) if bits & (1 << shift) else (second, first)
            )
            scores[winner] += 1
        if min(scores) >= 1:
            counts[tuple(sorted(scores))] += 1
    return counts


def digest(sequences: list[tuple[int, ...]]) -> str:
    payload = "\n".join(",".join(map(str, sequence)) for sequence in sequences) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> None:
    landau = landau_sequences()
    counts = direct_counts()
    assert landau == SCORE_SEQUENCES
    assert sorted(counts) == SCORE_SEQUENCES
    assert [counts[sequence] for sequence in SCORE_SEQUENCES] == EXPECTED_LABELED_COUNTS
    assert sum(counts.values()) == 26624
    sequence_sha256 = digest(landau)
    assert sequence_sha256 == EXPECTED_SEQUENCE_SHA256
    print(
        json.dumps(
            {
                "labeled_counts": EXPECTED_LABELED_COUNTS,
                "positive_labeled_tournaments": sum(counts.values()),
                "score_sequences": len(landau),
                "sequence_sha256": sequence_sha256,
                "status": "VERIFIED",
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
