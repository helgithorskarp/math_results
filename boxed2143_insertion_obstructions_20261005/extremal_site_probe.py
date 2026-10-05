#!/usr/bin/env python3
"""Falsify Lyra's pointwise L_max+L_min>=n+2 hypothesis; finite evidence only."""

from __future__ import annotations

import argparse
from itertools import permutations
import json
import platform
import time

from kernel import boxed_occurrences, legal_maximum_gaps


def reverse_complement(p: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(len(p) + 1 - x for x in reversed(p))


def probe(max_n: int) -> dict:
    started = time.monotonic()
    rows = []
    for n in range(max_n + 1):
        minimum = None
        first_minimizer = None
        avoiding_parents = 0
        for p in permutations(range(1, n + 1)):
            if boxed_occurrences(p):
                continue
            avoiding_parents += 1
            max_gaps = legal_maximum_gaps(p)
            reflected = legal_maximum_gaps(reverse_complement(p))
            min_gaps = tuple(sorted(n - g for g in reflected))
            total = len(max_gaps) + len(min_gaps)
            if minimum is None or total < minimum:
                minimum, first_minimizer = total, p
            if total < n + 2:
                return {
                    "status": "COUNTEREXAMPLE_TO_PROPOSED_SITE_BOUND",
                    "hypothesis": "Every boxed2143 avoider p of length n has L_max(p)+L_min(p)>=n+2",
                    "source_chat_id": 438,
                    "rows_for_smaller_sizes": rows,
                    "counterexample": {"n": n, "permutation": p,
                                       "max_gaps": max_gaps, "min_gaps": min_gaps,
                                       "site_sum": total, "proposed_lower_bound": n + 2},
                    "scope": "First failure in increasing size and lexicographic permutation order; confirm by definition checker",
                    "python": platform.python_version(),
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "full_growth_target_solved": False,
                }
        rows.append({"n": n, "avoiders_checked": avoiding_parents,
                     "minimum_site_sum": minimum, "first_minimizer": first_minimizer})
    return {
        "status": "NO_FAILURE_IN_FINITE_RANGE",
        "hypothesis": "Every boxed2143 avoider p of length n has L_max(p)+L_min(p)>=n+2",
        "source_chat_id": 438,
        "rows": rows,
        "max_n": max_n,
        "scope": "Finite test only, no inference for larger n",
        "python": platform.python_version(),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "full_growth_target_solved": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-n", type=int, default=8)
    args = parser.parse_args()
    if not 0 <= args.max_n <= 9:
        parser.error("max-n must be between 0 and 9")
    print(json.dumps(probe(args.max_n), indent=2))


if __name__ == "__main__":
    main()
