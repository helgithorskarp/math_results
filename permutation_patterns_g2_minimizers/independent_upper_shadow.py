#!/usr/bin/env python3
"""Definition-level upper-shadow census, independent of rooted lenses."""

from __future__ import annotations

import argparse
from collections import defaultdict
from itertools import combinations, permutations


Permutation = tuple[int, ...]


def standardize(values) -> Permutation:
    values = tuple(values)
    order = {value: rank for rank, value in enumerate(sorted(values), 1)}
    return tuple(order[value] for value in values)


def avoids(beta: Permutation, forbidden: set[Permutation]) -> bool:
    for indices in combinations(range(len(beta)), 3):
        if standardize(beta[index] for index in indices) in forbidden:
            return False
    return True


def is_predicted_minimizer(beta: Permutation) -> bool:
    layered_basis = {(2, 3, 1), (3, 1, 2)}
    colayered_basis = {(1, 3, 2), (2, 1, 3)}
    return avoids(beta, layered_basis) or avoids(beta, colayered_basis)


def direct_g2_counts(n: int) -> dict[Permutation, int]:
    counts: dict[Permutation, int] = defaultdict(int)
    for upper in permutations(range(1, n + 3)):
        contained = set()
        for deleted in combinations(range(n + 2), 2):
            deleted_set = set(deleted)
            contained.add(
                standardize(
                    value for index, value in enumerate(upper)
                    if index not in deleted_set
                )
            )
        for beta in contained:
            counts[beta] += 1
    return counts


def expected_minimum(n: int) -> int:
    return (n**4 + 2 * n**3 + n**2 + 2 * n + 6) // 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=7)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 8:
        parser.error("--max-n must lie between 1 and 8")

    for n in range(1, args.max_n + 1):
        counts = direct_g2_counts(n)
        minimum = min(counts.values())
        minimizers = {beta for beta, count in counts.items() if count == minimum}
        predicted = {
            beta for beta in permutations(range(1, n + 1))
            if is_predicted_minimizer(beta)
        }
        if minimum != expected_minimum(n):
            raise AssertionError((n, minimum, expected_minimum(n)))
        if minimizers != predicted:
            raise AssertionError((n, minimizers - predicted, predicted - minimizers))
        print(
            f"n={n}: direct minimum g2={minimum}; minimizers={len(minimizers)}",
            flush=True,
        )

    print(
        f"direct upper-shadow census verified exact minimizers through n={args.max_n}"
    )


if __name__ == "__main__":
    main()
