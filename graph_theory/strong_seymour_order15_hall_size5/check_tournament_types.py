#!/usr/bin/env python3
"""Independent orbit-expansion check of the eight strict tournament types."""

from __future__ import annotations

import hashlib
import itertools
import json


REPRESENTATIVES = [2, 4, 8, 10, 12, 40, 41, 76]
EXPECTED_ORBIT_SIZES = [40, 120, 120, 120, 120, 40, 120, 24]
EXPECTED_UNION_SHA256 = (
    "d96a749ce921425cf5644e3369b78c8f9828ac9f7ed99b44e3ef173e673bc299"
)
PAIRS = [(first, second) for first in range(5) for second in range(first + 1, 5)]


def adjacency(bits: int) -> list[list[bool]]:
    graph = [[False] * 5 for _ in range(5)]
    for shift, (first, second) in enumerate(PAIRS):
        graph[first][second] = bool(bits & (1 << shift))
        graph[second][first] = not graph[first][second]
    return graph


def relabel(bits: int, permutation: tuple[int, ...]) -> int:
    graph = adjacency(bits)
    return sum(
        int(graph[permutation[first]][permutation[second]]) << shift
        for shift, (first, second) in enumerate(PAIRS)
    )


def digest(values: set[int]) -> str:
    payload = "\n".join(str(value) for value in sorted(values)) + "\n"
    return hashlib.sha256(payload.encode()).hexdigest()


def main() -> None:
    permutations = list(itertools.permutations(range(5)))
    expanded: set[int] = set()
    measured = []
    scores = []
    for representative, expected_size in zip(
        REPRESENTATIVES, EXPECTED_ORBIT_SIZES, strict=True
    ):
        orbit = {relabel(representative, permutation) for permutation in permutations}
        assert len(orbit) == expected_size
        assert expanded.isdisjoint(orbit)
        expanded.update(orbit)
        measured.append(len(orbit))
        scores.append(sorted(sum(row) for row in adjacency(representative)))

    direct = {
        bits
        for bits in range(1 << len(PAIRS))
        if min(sum(row) for row in adjacency(bits)) >= 1
    }
    assert expanded == direct
    assert len(expanded) == 704
    union_sha256 = digest(expanded)
    assert union_sha256 == EXPECTED_UNION_SHA256
    print(
        json.dumps(
            {
                "labeled_tournaments": len(expanded),
                "orbit_sizes": measured,
                "score_sequences": scores,
                "status": "VERIFIED",
                "union_sha256": union_sha256,
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
