#!/usr/bin/env python3
"""Definition-level verification of Bluskov's cyclic 78-block C(13,7,5) cover."""

from __future__ import annotations

from collections import Counter
from itertools import combinations


V = 13
LINE_BASE = (1, 2, 4, 10)
COVER_BASES = (
    (1, 2, 3, 4, 5, 10, 11),
    (1, 2, 3, 4, 6, 10, 12),
    (1, 2, 3, 4, 7, 8, 10),
    (1, 2, 3, 5, 6, 8, 11),
    (1, 2, 3, 5, 7, 11, 12),
    (1, 2, 4, 5, 9, 10, 12),
)


def translate(block: tuple[int, ...], shift: int) -> tuple[int, ...]:
    return tuple(sorted(((point - 1 + shift) % V) + 1 for point in block))


def main() -> None:
    lines = {translate(LINE_BASE, shift) for shift in range(V)}
    if len(lines) != 13:
        raise AssertionError("line orbit is not full")
    pair_multiplicity = Counter(
        pair for line in lines for pair in combinations(line, 2)
    )
    if len(pair_multiplicity) != 78 or set(pair_multiplicity.values()) != {1}:
        raise AssertionError("line orbit is not a 2-(13,4,1) design")

    line_unions = {
        tuple(sorted(set(first) | set(second)))
        for first, second in combinations(lines, 2)
    }
    if len(line_unions) != 78 or any(len(block) != 7 for block in line_unions):
        raise AssertionError("pairs of lines do not give 78 distinct seven-blocks")

    developed = {
        translate(base, shift) for base in COVER_BASES for shift in range(V)
    }
    if developed != line_unions:
        raise AssertionError("listed base-block development differs from line unions")

    print("projective-plane lines: 13; every point-pair occurs once")
    print("distinct unions of two lines: 78")
    print("six cyclic base orbits equal the line-union construction")
    for t in range(1, 6):
        multiplicity = Counter()
        for target in combinations(range(1, V + 1), t):
            count = sum(set(target) <= set(block) for block in developed)
            multiplicity[count] += 1
        if min(multiplicity) == 0:
            raise AssertionError(f"uncovered {t}-set")
        print(
            f"t={t} total={sum(multiplicity.values())} min={min(multiplicity)} "
            f"max={max(multiplicity)} histogram="
            + ",".join(f"{value}:{multiplicity[value]}" for value in sorted(multiplicity))
        )


if __name__ == "__main__":
    main()
