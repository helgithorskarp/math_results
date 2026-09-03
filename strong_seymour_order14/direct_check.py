#!/usr/bin/env python3
"""Definition-level checks for the strong-Seymour order-14 contribution."""

from __future__ import annotations

import itertools
import json


Q_OUT = (
    (1, 4, 5),
    (3, 4, 5),
    (0, 1, 3),
    (0, 4),
    (2, 5),
    (2, 3),
)


def blowup(sizes: tuple[int, ...]) -> list[int]:
    starts: list[int] = []
    n = 0
    for size in sizes:
        starts.append(n)
        n += size
    rows = [0] * n
    for i, size in enumerate(sizes):
        for a in range(starts[i], starts[i] + size):
            for b in range(a + 1, starts[i] + size):
                rows[a] |= 1 << b
        for j in Q_OUT[i]:
            target = ((1 << sizes[j]) - 1) << starts[j]
            for a in range(starts[i], starts[i] + size):
                rows[a] |= target
    return rows


def check_tournament(rows: list[int]) -> None:
    n = len(rows)
    for i in range(n):
        if rows[i] >> i & 1:
            raise AssertionError("loop")
        for j in range(i + 1, n):
            if ((rows[i] >> j) & 1) + ((rows[j] >> i) & 1) != 1:
                raise AssertionError("not a tournament")


def max_matching(rows: list[int], left: int, right: int) -> int:
    matched_to = [-1] * len(rows)
    size = 0
    while left:
        bit = left & -left
        y = bit.bit_length() - 1
        left ^= bit
        seen = 0

        def augment(u: int) -> bool:
            nonlocal seen
            candidates = rows[u] & right & ~seen
            while candidates:
                z_bit = candidates & -candidates
                z = z_bit.bit_length() - 1
                candidates ^= z_bit
                seen |= z_bit
                if matched_to[z] == -1 or augment(matched_to[z]):
                    matched_to[z] = u
                    return True
            return False

        size += augment(y)
    return size


def profile(rows: list[int]) -> list[tuple[int, int, int]]:
    n = len(rows)
    universe = (1 << n) - 1
    answer: list[tuple[int, int, int]] = []
    for x in range(n):
        first = rows[x]
        reachable = 0
        work = first
        while work:
            bit = work & -work
            work ^= bit
            reachable |= rows[bit.bit_length() - 1]
        second = reachable & ~(first | (1 << x)) & universe
        answer.append((first.bit_count(), second.bit_count(), max_matching(rows, first, second)))
    return answer


def inequalities(sizes: tuple[int, ...]) -> bool:
    n0, n1, n2, n3, n4, n5 = sizes
    return (
        n1 + n4 + n5 > n2 + n3
        and n4 + n5 > n2
        and n0 + n1 + n3 > n4 + n5
        and n0 > n1 + n5
        and n2 + n5 > n0 + n1 + n3
        and n2 > n0 + n1
    )


def minimum_inequality_solutions(limit: int = 36) -> tuple[int, list[tuple[int, ...]]]:
    for total in range(6, limit + 1):
        solutions: list[tuple[int, ...]] = []
        for cuts in itertools.combinations(range(1, total), 5):
            sizes = tuple(b - a for a, b in zip((0, *cuts), (*cuts, total)))
            if inequalities(sizes):
                solutions.append(sizes)
        if solutions:
            return total, solutions
    raise AssertionError("no solution through supplied limit")


def hand_regular_example() -> list[int]:
    """A regular 13-tournament where vertex 0, but not all vertices, fails Hall."""
    return [126, 500, 504, 498, 7776, 7872, 8064, 6929, 5681, 3087, 2191, 4367, 1551]


def main() -> None:
    published = blowup((7, 3, 11, 3, 9, 3))
    check_tournament(published)
    published_profile = profile(published)
    if any(degree == matching for degree, _, matching in published_profile):
        raise AssertionError("published counterexample unexpectedly has a strong vertex")

    hand = hand_regular_example()
    check_tournament(hand)
    hand_profile = profile(hand)
    if hand_profile[0] != (6, 6, 5):
        raise AssertionError("negative Hall fixture was not detected")
    if [i for i, (degree, _, matching) in enumerate(hand_profile) if degree == matching] != list(range(1, 13)):
        raise AssertionError("regular fixture has unexpected strong-vertex set")

    minimum, solutions = minimum_inequality_solutions()
    if (minimum, solutions) != (36, [(7, 3, 11, 3, 9, 3)]):
        raise AssertionError("unexpected blow-up inequality optimum")

    print(
        json.dumps(
            {
                "blowup_minimum": minimum,
                "blowup_unique_sizes": solutions[0],
                "published_order": len(published),
                "published_strong_vertices": [],
                "regular_fixture_profile_at_0": hand_profile[0],
                "regular_fixture_strong_vertices": list(range(1, 13)),
            },
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
