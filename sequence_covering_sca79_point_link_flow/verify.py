#!/usr/bin/env python3
"""Independent exact checker for the SCA(5040;7,9) point-link census."""

from __future__ import annotations

import argparse
from functools import lru_cache
from itertools import combinations
from math import factorial
from pathlib import Path


BASE = (560, 70, 20, 10, 8, 10, 20, 70, 560)
U = (1, -7, 21, -35, 35, -21, 7, -1, 0)
V = (0, 1, -7, 21, -35, 35, -21, 7, -1)
H = U[:8]


def parse_results(path: Path):
    metrics: dict[str, int] = {}
    sections: dict[str, list[tuple[int, int]]] = {}
    section = "metrics"
    for raw in path.read_text(encoding="ascii").splitlines():
        if not raw or raw == "metric\tvalue":
            continue
        if raw.startswith("[") and raw.endswith("]"):
            section = raw[1:-1]
            sections[section] = []
            continue
        left, right = raw.split("\t")
        if section == "metrics":
            metrics[left] = int(right)
        else:
            sections[section].append((int(left), int(right)))
    return metrics, sections


def count_sorted_links(a: int, total: int) -> int:
    """Count sorted c_1,...,c_8 with the full 256-cell inequalities.

    This dynamic program is independent of the fast enumerator.  For a sorted
    tuple, the odd-cardinality constraints concern the smallest prefix and the
    even-cardinality constraints concern the largest suffix.  With the total
    fixed, all of them become lower bounds on prefix sums.
    """

    prefix_lower = {
        1: a - 70,
        2: total - a - 20,
        3: a - 10,
        4: total - a - 8,
        5: a - 10,
        6: total - a - 20,
        7: a - 70,
    }
    if total - a > 560:
        return 0

    @lru_cache(maxsize=None)
    def dp(chosen: int, least: int, partial: int) -> int:
        if chosen == 8:
            return int(partial == total)
        remaining_after = 7 - chosen
        answer = 0
        for value in range(least, 19):
            new_partial = partial + value
            # The remaining sorted entries lie between value and 18.
            if new_partial + remaining_after * value > total:
                continue
            if new_partial + remaining_after * 18 < total:
                continue
            new_chosen = chosen + 1
            if new_chosen <= 7 and new_partial < prefix_lower[new_chosen]:
                continue
            answer += dp(new_chosen, value, new_partial)
        return answer

    return dp(0, -18, 0)


def point_link_census():
    profiles_by_a: dict[int, int] = {}
    position_types: set[tuple[int, int]] = set()
    # The size-2 and size-3 inequalities with c_i in [-18,18] imply
    # -56 <= a <= 64.  The total of the eight c_i is in [-144,144].
    for a in range(-56, 65):
        count_for_a = 0
        for total in range(-144, 145):
            count = count_sorted_links(a, total)
            if count:
                count_for_a += count
                position_types.add((a, total - a))
        if count_for_a:
            profiles_by_a[a] = count_for_a
    return profiles_by_a, position_types


def independently_deletion_admissible() -> set[tuple[int, int]]:
    answer: set[tuple[int, int]] = set()
    # Positions 0,1,7,8 imply that every nonnegative distribution lies in
    # this square: a >= -560, b <= 560, a <= 160, and b >= -160.
    for a in range(-560, 561):
        for b in range(-560, 561):
            d = [560 + a * U[j] + b * V[j] for j in range(9)]
            if min(d) < 0:
                continue
            compatible = []
            for c in range(-18, 19):
                delta = 0
                ok = True
                for k in range(8):
                    deleted = 630 + c * H[k]
                    delta += deleted - d[k]
                    if not 0 <= delta <= deleted:
                        ok = False
                if ok:
                    compatible.append(c)
            if not compatible:
                continue
            assert compatible == list(range(compatible[0], compatible[-1] + 1))
            if 8 * compatible[0] <= a + b <= 8 * compatible[-1]:
                answer.add((a, b))
    return answer


def check_linear_algebra_identities() -> None:
    assert all(
        BASE[r] + 2 * BASE[r + 1] + BASE[r + 2]
        == factorial(r) * factorial(6 - r)
        for r in range(7)
    )

    # Check the moment-nullspace basis used for position distributions.
    for power in range(7):
        assert sum((j**power) * U[j] for j in range(9)) == 0
        assert sum((j**power) * V[j] for j in range(9)) == 0

    # Directly check every two-face on a basis of the homogeneous family.
    for basis in range(9):
        a = int(basis == 0)
        c = [0] * 8
        if basis:
            c[basis - 1] = 1
        for i, j in combinations(range(8), 2):
            remaining = [x for x in range(8) if x not in (i, j)]
            for fixed_bits in range(64):
                fixed = {remaining[k] for k in range(6) if fixed_bits >> k & 1}
                face_sum = 0
                for extra_bits in range(4):
                    subset = set(fixed)
                    if extra_bits & 1:
                        subset.add(i)
                    if extra_bits & 2:
                        subset.add(j)
                    size = len(subset)
                    face_sum += (-1 if size % 2 == 0 else 1) * (
                        sum(c[x] for x in subset) - a
                    )
                assert face_sum == 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "results",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("RESULTS.tsv"),
    )
    args = parser.parse_args()

    check_linear_algebra_identities()
    metrics, sections = parse_results(args.results)
    profiles_by_a, position_types = point_link_census()
    deletion_types = independently_deletion_admissible()
    excluded = deletion_types - position_types

    assert sum(profiles_by_a.values()) == 243545
    assert len(position_types) == 1695
    assert len(deletion_types) == 1769
    assert len(excluded) == 74
    assert metrics == {
        "symmetry_reduced_point_link_profiles": 243545,
        "induced_position_types": 1695,
        "independent_deletion_types": 1769,
        "newly_excluded_position_types": 74,
    }
    assert sections["profiles_by_a"] == sorted(profiles_by_a.items())
    assert sections["position_types"] == sorted(position_types)
    assert sections["newly_excluded_position_types"] == sorted(excluded)

    print("linear identities: OK")
    print("symmetry-reduced point-link profiles: 243545")
    print("induced position types: 1695")
    print("independent-deletion types: 1769")
    print("newly excluded position types: 74")
    print("RESULTS.tsv: exact match")


if __name__ == "__main__":
    main()
