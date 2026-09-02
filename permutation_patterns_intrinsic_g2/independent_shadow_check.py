#!/usr/bin/env python3
"""Definition-level check independent of insertion triples and track matrices."""

from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations, permutations
from math import factorial

from intrinsic_g2 import intrinsic_j, standardize


Permutation = tuple[int, ...]


def contained_patterns(tau: Permutation, length: int) -> set[Permutation]:
    return {
        standardize(tau[index] for index in indices)
        for indices in combinations(range(len(tau)), length)
    }


def expected_j_from_g2(n: int, g2: int) -> int:
    numerator = n**4 + 2 * n**3 + n**2 + 4 * n + 4 - 2 * g2
    if numerator % 2:
        raise AssertionError((n, g2, numerator))
    return numerator // 2


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.max_n <= 7:
        parser.error("--max-n must lie between 1 and 7")

    for n in range(1, args.max_n + 1):
        counts: Counter[Permutation] = Counter()
        for tau in permutations(range(1, n + 3)):
            counts.update(contained_patterns(tau, n))
        if len(counts) != factorial(n):
            raise AssertionError((n, len(counts), factorial(n)))

        for beta, g2 in counts.items():
            if intrinsic_j(beta) != expected_j_from_g2(n, g2):
                raise AssertionError((beta, g2, intrinsic_j(beta)))
        print(
            f"n={n}: definition-level check of {len(counts)} patterns; "
            f"g2_range={min(counts.values())}..{max(counts.values())}",
            flush=True,
        )
    print(
        f"definition-level upper-shadow counts agree with intrinsic j "
        f"through n={args.max_n}"
    )


if __name__ == "__main__":
    main()
