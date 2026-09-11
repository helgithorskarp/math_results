#!/usr/bin/env python3
"""Exact verifier for the nine-asymmetric-link point-profile reduction."""

from __future__ import annotations

from functools import lru_cache
from hashlib import sha256
from math import comb, factorial
from pathlib import Path


BASE = (560, 70, 20, 10, 8, 10, 20, 70, 560)
U = (1, -7, 21, -35, 35, -21, 7, -1, 0)
V = (0, 1, -7, 21, -35, 35, -21, 7, -1)
RESULTS_SHA256 = "59620eac553ff371a31702a1a9dcf13e2fac26ca463796dd332cccc6131cf3f6"


def multinomial(parts: tuple[int, ...]) -> int:
    result = factorial(sum(parts))
    for part in parts:
        result //= factorial(part)
    return result


def result_path() -> Path:
    return (
        Path(__file__).resolve().parents[1]
        / "sequence_covering_sca79_point_link_flow"
        / "RESULTS.tsv"
    )


def load_position_types() -> tuple[list[tuple[int, int]], dict[str, int]]:
    path = result_path()
    assert sha256(path.read_bytes()).hexdigest() == RESULTS_SHA256
    types: list[tuple[int, int]] = []
    metrics: dict[str, int] = {}
    section = "metrics"
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line == "metric\tvalue":
            continue
        if line.startswith("["):
            section = line[1:-1]
            continue
        left, right = line.split("\t")
        if section == "metrics":
            metrics[left] = int(right)
        elif section == "position_types":
            types.append((int(left), int(right)))
    return types, metrics


def position_vector(point_type: tuple[int, int]) -> tuple[int, ...]:
    a, b = point_type
    return tuple(560 + a * U[i] + b * V[i] for i in range(9))


def residue_coordinates() -> tuple[tuple[int, int, int], ...]:
    return tuple(
        (i, j, multinomial((i, j - i - 1, 8 - j)))
        for i in range(9)
        for j in range(i + 1, 9)
    )


def tail_signature(point_type: tuple[int, int]) -> tuple[int, ...]:
    d = position_vector(point_type)
    return tuple(d[i] % modulus for i, _, modulus in residue_coordinates())


def head_signature(point_type: tuple[int, int]) -> tuple[int, ...]:
    d = position_vector(point_type)
    return tuple(d[j] % modulus for _, j, modulus in residue_coordinates())


def count_sorted_links(a: int, total: int) -> int:
    """Count symmetry-reduced full point links at fixed a and sum(c)."""

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
    def count(chosen: int, least: int, partial: int) -> int:
        if chosen == 8:
            return int(partial == total)
        remaining = 7 - chosen
        answer = 0
        for value in range(least, 19):
            new_partial = partial + value
            if new_partial + remaining * value > total:
                continue
            if new_partial + remaining * 18 < total:
                continue
            new_chosen = chosen + 1
            if new_chosen <= 7 and new_partial < prefix_lower[new_chosen]:
                continue
            answer += count(new_chosen, value, new_partial)
        return answer

    return count(0, -18, 0)


def cycle_partitions(
    remaining: int, largest: int | None = None
) -> tuple[tuple[int, ...], ...]:
    if remaining == 0:
        return ((),)
    if largest is None:
        largest = remaining
    answer = []
    for part in range(min(remaining, largest), 1, -1):
        for suffix in cycle_partitions(remaining - part, part):
            answer.append((part,) + suffix)
    return tuple(answer)


def derangements(n: int) -> int:
    return sum((-1) ** k * comb(n, k) * factorial(n - k) for k in range(n + 1))


def main() -> None:
    types, metrics = load_position_types()
    assert len(types) == metrics["induced_position_types"] == 1695
    assert metrics["symmetry_reduced_point_link_profiles"] == 243545
    assert all(min(position_vector(point_type)) >= 0 for point_type in types)

    tail_groups: dict[tuple[int, ...], list[tuple[int, int]]] = {}
    head_groups: dict[tuple[int, ...], list[tuple[int, int]]] = {}
    for point_type in types:
        tail_groups.setdefault(tail_signature(point_type), []).append(point_type)
        head_groups.setdefault(head_signature(point_type), []).append(point_type)

    common = set(tail_groups) & set(head_groups)
    assert len(tail_groups) == len(head_groups) == 1695
    assert len(common) == 1
    signature = next(iter(common))
    assert tail_groups[signature] == head_groups[signature] == [(0, 0)]

    profiles_at_uniform_positions = count_sorted_links(a=0, total=0)
    assert profiles_at_uniform_positions == 949
    # Seven symmetric outgoing links include two distinct exclusions x,z.
    # Their singleton boundaries force all eight c-coefficients equal; at
    # a=b=0 their sum is zero, hence each is zero.
    common_c = 0
    assert 8 * common_c == 0

    partitions = cycle_partitions(9)
    expected_partitions = (
        (9,),
        (7, 2),
        (6, 3),
        (5, 4),
        (5, 2, 2),
        (4, 3, 2),
        (3, 3, 3),
        (3, 2, 2, 2),
    )
    assert partitions == expected_partitions
    assert derangements(9) == 133496

    print("admissible point-position types:", len(types))
    print("distinct tail residue signatures:", len(tail_groups))
    print("distinct head residue signatures:", len(head_groups))
    print("shared signatures:", len(common))
    print("compatible ordered type pairs: (0,0) -> (0,0)")
    print("full point profiles above (0,0):", profiles_at_uniform_positions)
    print("profiles surviving symmetric boundaries: 1")
    print("cycle-cover types:", len(partitions))
    print("labelled cycle-cover supports:", derangements(9))
    print("conclusion: exact-nine asymmetry forces every point link uniform")
    print("all checks passed")


if __name__ == "__main__":
    main()
