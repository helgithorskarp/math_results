#!/usr/bin/env python3
"""Exact matching- and Lagrange-cover computation for D(n,n-1).

All comparisons use Python integers and fractions.  A path is a tuple with
R=1 and U=0.  Canonical pair hashes serialize a cover as ``lower;upper``.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def rational_dyck_paths(n: int):
    """Yield D(n,n-1) in the same deterministic order as the source notebook."""
    if n < 2:
        raise ValueError("n must be at least 2")
    length = 2 * n - 1
    for zero_positions in itertools.combinations(range(1, length), n - 1):
        zeros = set(zero_positions)
        path = tuple(0 if index in zeros else 1 for index in range(length))
        balance = 0
        for step in path:
            balance += 1 if step else -1
            if balance < 1:
                break
        else:
            yield path


def continued_fraction_entries(path: tuple[int, ...]) -> tuple[int, ...]:
    entries: list[int] = []
    for left, right in zip(path, path[1:]):
        entries.extend((1, 1) if left == right else (2,))
    return tuple(entries)


def continued_fraction_matrix(entries: tuple[int, ...]) -> tuple[int, int, int, int]:
    """Return product of [[a,1],[1,0]] matrices as (p,r,q,s)."""
    p, r, q, s = 1, 0, 0, 1
    for entry in entries:
        p, r, q, s = p * entry + r, p, q * entry + s, q
    return p, r, q, s


def matching_number(path: tuple[int, ...]) -> int:
    return continued_fraction_matrix(continued_fraction_entries(path))[0]


def lagrange_data(path: tuple[int, ...]) -> tuple[Fraction, tuple[int, int], int]:
    """Return (L(path)^2, notebook raw key (D,q), first maximizing shift)."""
    period = (2,) + continued_fraction_entries(path)
    candidates: list[tuple[Fraction, int, int, int]] = []
    for shift in range(len(period)):
        rotated = period[shift:] + period[:shift]
        p, r, q, s = continued_fraction_matrix(rotated)
        discriminant = (p - s) ** 2 + 4 * r * q
        candidates.append((Fraction(discriminant, q * q), discriminant, q, shift))
    maximum = max(candidate[0] for candidate in candidates)
    score, discriminant, denominator, shift = next(
        candidate for candidate in candidates if candidate[0] == maximum
    )
    return score, (discriminant, denominator), shift


def adjacent_level_covers(levels: list[list[tuple[int, ...]]]):
    covers = set()
    for lower_level, upper_level in zip(levels, levels[1:]):
        covers.update((lower, upper) for lower in lower_level for upper in upper_level)
    return covers


def pair_hash(covers) -> str:
    digest = hashlib.sha256()
    for lower, upper in sorted(covers):
        digest.update(
            ("".join(map(str, lower)) + ";" + "".join(map(str, upper)) + "\n").encode()
        )
    return digest.hexdigest()


def compute(n: int = 10):
    paths = list(rational_dyck_paths(n))
    matching_groups = defaultdict(list)
    lagrange_groups = defaultdict(list)
    raw_lagrange_groups = defaultdict(list)
    lagrange_scores = {}
    for path in paths:
        matching_groups[matching_number(path)].append(path)
        score, raw_key, _ = lagrange_data(path)
        lagrange_groups[score].append(path)
        raw_lagrange_groups[raw_key].append(path)
        lagrange_scores[path] = score

    matching_levels = [matching_groups[key] for key in sorted(matching_groups)]
    lagrange_levels = [lagrange_groups[key] for key in sorted(lagrange_groups)]
    matching_covers = adjacent_level_covers(matching_levels)
    lagrange_covers = adjacent_level_covers(lagrange_levels)
    common_covers = matching_covers & lagrange_covers
    return {
        "paths": paths,
        "matching_groups": matching_groups,
        "lagrange_groups": lagrange_groups,
        "raw_lagrange_groups": raw_lagrange_groups,
        "lagrange_scores": lagrange_scores,
        "matching_covers": matching_covers,
        "lagrange_covers": lagrange_covers,
        "common_covers": common_covers,
    }


def exact_summary(data) -> dict[str, object]:
    matching = data["matching_covers"]
    lagrange = data["lagrange_covers"]
    common = data["common_covers"]
    return {
        "path_count": len(data["paths"]),
        "matching_level_count": len(data["matching_groups"]),
        "lagrange_level_count": len(data["lagrange_groups"]),
        "matching_cover_count": len(matching),
        "lagrange_cover_count": len(lagrange),
        "common_cover_count": len(common),
        "matching_only_count": len(matching - common),
        "lagrange_only_count": len(lagrange - common),
        "matching_cover_sha256": pair_hash(matching),
        "lagrange_cover_sha256": pair_hash(lagrange),
        "common_cover_sha256": pair_hash(common),
        "matching_only_sha256": pair_hash(matching - common),
        "lagrange_only_sha256": pair_hash(lagrange - common),
    }


def verify_source_example() -> None:
    first = tuple(1 if step == "R" else 0 for step in "RRRUURURU")
    second = tuple(1 if step == "R" else 0 for step in "RRRUURRUU")
    assert matching_number(first) == 1115
    assert matching_number(second) == 1177
    assert lagrange_data(first)[0] == Fraction(11390621, 1055**2)
    assert lagrange_data(second)[0] == Fraction(17**2 * 48893, 1177**2)
    assert lagrange_data(first)[0] > lagrange_data(second)[0]


def main() -> None:
    verify_source_example()
    actual = exact_summary(compute())
    expected = json.loads((ROOT / "certificate.json").read_text())["exact_D_10_9"]
    if actual != expected:
        raise SystemExit(
            "certificate mismatch:\n"
            + json.dumps({"expected": expected, "actual": actual}, indent=2, sort_keys=True)
        )
    print(json.dumps(actual, indent=2, sort_keys=True))
    print("EXACT COVER CERTIFICATE VERIFIED")


if __name__ == "__main__":
    main()
