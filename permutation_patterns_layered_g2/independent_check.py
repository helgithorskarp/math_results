#!/usr/bin/env python3
"""Definition-level check independent of the insertion representation."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations

from verify_layered_g2 import compositions, expected_g2, layered


Permutation = tuple[int, ...]


def standardize(values) -> Permutation:
    values = tuple(values)
    ranks = {value: rank + 1 for rank, value in enumerate(sorted(values))}
    return tuple(ranks[value] for value in values)


def contained_patterns(perm: Permutation, length: int) -> set[Permutation]:
    return {
        standardize(perm[index] for index in indices)
        for indices in combinations(range(len(perm)), length)
    }


def complement(perm: Permutation) -> Permutation:
    n = len(perm)
    return tuple(n + 1 - value for value in perm)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 7:
        parser.error("--max-n must lie between 1 and 7")

    for n in range(1, args.max_n + 1):
        targets = {layered(parts) for parts in compositions(n)}
        targets |= {complement(beta) for beta in targets}
        counts: Counter[Permutation] = Counter()
        for perm in permutations(range(1, n + 3)):
            counts.update(contained_patterns(perm, n) & targets)
        expected = expected_g2(n)
        failures = {beta: counts[beta] for beta in targets if counts[beta] != expected}
        if failures:
            raise AssertionError((n, expected, failures))
        print(
            f"n={n}: definition-level check of {len(targets)} layered/colayered "
            f"patterns gives g2={expected}"
        )
    print(f"independently verified layered and colayered g2 values through n={args.max_n}")


if __name__ == "__main__":
    main()
