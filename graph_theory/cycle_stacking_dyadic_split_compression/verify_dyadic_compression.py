#!/usr/bin/env python3
"""Independent finite checks for dyadic split compression."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import random
from pathlib import Path

from cycle_dyadic_compression import (
    branch_message,
    candidate_splits,
    compressed_cycle_witness,
    exhaustive_cycle_witness,
    safe_threshold,
    split_path,
    target_score,
    verify_witness,
)


def weak_compositions(total: int, length: int):
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for suffix in weak_compositions(total - first, length - 1):
            yield (first,) + suffix


def branch_shift_checks() -> int:
    rng = random.Random(20260920)
    checks = 0
    for depth in range(1, 13):
        threshold = safe_threshold(depth)
        period = 1 << depth
        for _ in range(500):
            interior = tuple(rng.randrange(0, 40) for _ in range(depth - 1))
            x = threshold + rng.randrange(0, 10_000)
            left = branch_message((x,) + interior)
            right = branch_message((x + period,) + interior)
            if right != left + 1:
                raise AssertionError((depth, interior, x, left, right))
            checks += 1
    return checks


def target_max_checks() -> int:
    rng = random.Random(17320508)
    checks = 0
    for order in range(3, 11):
        for _ in range(800):
            piles = tuple(rng.randrange(0, 250) for _ in range(order))
            cut = rng.randrange(order)
            target = rng.randrange(order + 1)
            full = [
                target_score(split_path(piles, cut, x), target)
                for x in range(piles[cut] + 1)
            ]
            candidates = candidate_splits(piles[cut], target, order - target)
            compressed_max = max(full[x] for x in candidates)
            if compressed_max != max(full):
                raise AssertionError((piles, cut, target, candidates, full))
            checks += 1
    return checks


def exhaustive_cycle_checks() -> tuple[int, str]:
    entries: list[str] = []
    checked = 0
    limits = {3: 11, 4: 10, 5: 9, 6: 8, 7: 7}
    for order, mass_limit in limits.items():
        for mass in range(mass_limit + 1):
            for piles in weak_compositions(mass, order):
                expected = exhaustive_cycle_witness(piles)
                observed = compressed_cycle_witness(piles)
                if (expected is None) != (observed is None):
                    raise AssertionError((piles, expected, observed))
                if observed is not None and not verify_witness(piles, observed):
                    raise AssertionError((piles, observed))
                entries.append(f"{order}:{','.join(map(str, piles))}:{observed is not None}")
                checked += 1
    digest = hashlib.sha256("\n".join(entries).encode()).hexdigest()
    return checked, digest


def huge_mass_checks() -> tuple[int, int]:
    rng = random.Random(27182818)
    checks = 0
    maximum_candidates = 0
    for order in range(3, 18):
        for _ in range(100):
            pile = 10**100 + rng.randrange(0, 10**12)
            target = rng.randrange(order + 1)
            candidates = candidate_splits(pile, target, order - target)
            theoretical = (
                safe_threshold(target)
                + safe_threshold(order - target)
                + (1 << max(target, order - target))
            )
            if len(candidates) > theoretical:
                raise AssertionError((order, target, len(candidates), theoretical))
            if candidates[0] < 0 or candidates[-1] > pile:
                raise AssertionError((pile, candidates[0], candidates[-1]))
            maximum_candidates = max(maximum_candidates, len(candidates))
            checks += 1
    return checks, maximum_candidates


def malformed_checks() -> int:
    bad_calls = [
        lambda: candidate_splits(-1, 1, 2),
        lambda: candidate_splits(4, -1, 2),
        lambda: candidate_splits(4, 1, -2),
        lambda: split_path((1, 2), 0, 0),
        lambda: split_path((1, 2, 3), 3, 0),
        lambda: split_path((1, 2, 3), 0, 2),
    ]
    for call in bad_calls:
        try:
            call()
        except ValueError:
            pass
        else:
            raise AssertionError("malformed input was accepted")
    return len(bad_calls)


def run() -> dict[str, int | str]:
    branch_checks = branch_shift_checks()
    maximum_checks = target_max_checks()
    cycle_checks, digest = exhaustive_cycle_checks()
    huge_checks, maximum_candidates = huge_mass_checks()
    bad_checks = malformed_checks()
    return {
        "branch_shift_checks": branch_checks,
        "target_max_checks": maximum_checks,
        "exhaustive_cycle_configurations": cycle_checks,
        "entry_digest": digest,
        "huge_mass_checks": huge_checks,
        "maximum_huge_mass_candidates": maximum_candidates,
        "malformed_checks": bad_checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run()
    print(json.dumps(result, indent=2, sort_keys=True))
    if args.check_expected:
        expected = json.loads(Path("EXPECTED.json").read_text())
        if result != expected:
            raise SystemExit("result differs from EXPECTED.json")


if __name__ == "__main__":
    main()
