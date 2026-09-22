#!/usr/bin/env python3
"""Definition-level audit for consecutive-multiplier spider packing."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from itertools import combinations_with_replacement
from typing import Iterable


@dataclass(frozen=True)
class Plan:
    closure_length: int
    other_lengths: tuple[int, ...]
    multipliers: tuple[int, ...]
    q_base: int
    fixed_edges: int
    minimum_leaves: int
    total_edges_at_threshold: int


def closure_parameters(c: int) -> tuple[int, int]:
    """Return (P_c,M_c) from THEOREM.md."""
    if c < 2:
        raise ValueError("closure length must be at least two")
    if c == 2:
        return 0, 2
    if c == 3:
        return 0, 3
    p = 2 ** (c - 4)
    return p, p + 3


def make_plan(c: int, other_lengths: Iterable[int]) -> Plan:
    lengths = tuple(sorted(other_lengths, reverse=True))
    if not lengths or any(length < 2 for length in lengths):
        raise ValueError("at least one other nontrivial arm is required")
    p_c, m_c = closure_parameters(c)
    r = len(lengths)
    largest = lengths[0]
    q_base = max(1, p_c, (largest - 1) * r - largest + 1)
    multipliers = tuple(q_base + i for i in range(1, r + 1))
    fixed_edges = c + sum(lengths)
    required_edges = max(
        m_c,
        3 + max(length * q for length, q in zip(lengths, multipliers)),
    )
    minimum_leaves = max(0, required_edges - fixed_edges)
    return Plan(
        closure_length=c,
        other_lengths=lengths,
        multipliers=multipliers,
        q_base=q_base,
        fixed_edges=fixed_edges,
        minimum_leaves=minimum_leaves,
        total_edges_at_threshold=fixed_edges + minimum_leaves,
    )


def best_plan(lengths: Iterable[int]) -> tuple[int, Plan]:
    arms = tuple(lengths)
    if len(arms) < 2 or any(length < 2 for length in arms):
        raise ValueError("at least two nontrivial arms are required")
    candidates = [
        (index, make_plan(c, arms[:index] + arms[index + 1 :]))
        for index, c in enumerate(arms)
    ]
    return min(
        candidates,
        key=lambda item: (
            item[1].minimum_leaves,
            item[1].total_edges_at_threshold,
            item[0],
        ),
    )


def closure_path(c: int, m: int) -> tuple[int, ...]:
    _, minimum_m = closure_parameters(c)
    if m < minimum_m:
        raise ValueError("ambient maximum is below the closure cutoff")
    if c == 2:
        return (1, m, 0)
    if c == 3:
        return (1, m - 1, 0, m)
    low = tuple(2**power + 1 for power in range(c - 4, -1, -1))
    return (1,) + low + (m, 0, m - 1)


def multiplicative_path(length: int, q: int, m: int) -> tuple[int, ...]:
    if length < 2 or q < 1 or m + 1 < length * q + 2:
        raise ValueError("invalid multiplicative path parameters")
    labels = []
    for position in range(1, length + 1):
        coefficient = (
            length - (position - 1) // 2
            if position % 2
            else position // 2
        )
        labels.append(coefficient * q + 1)
    return (1,) + tuple(labels)


def tau(label: int, m: int) -> int:
    if label == 0:
        return m
    if 2 <= label <= m:
        return label - 1
    raise ValueError("label is not in the non-hub alphabet")


def path_differences(path: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(abs(left - right) for left, right in zip(path, path[1:]))


def is_self_matched(path: tuple[int, ...], m: int) -> bool:
    if not path or path[0] != 1 or len(set(path)) != len(path):
        return False
    try:
        target = {tau(label, m) for label in path[1:]}
    except ValueError:
        return False
    differences = path_differences(path)
    return len(set(differences)) == len(differences) and set(differences) == target


def construct(plan: Plan, leaves: int | None = None) -> dict[str, object]:
    if leaves is None:
        leaves = plan.minimum_leaves
    if leaves < plan.minimum_leaves:
        raise ValueError("leaf count is below the proved threshold")
    m = plan.fixed_edges + leaves
    paths = [closure_path(plan.closure_length, m)]
    paths.extend(
        multiplicative_path(length, q, m)
        for length, q in zip(plan.other_lengths, plan.multipliers)
    )
    used = {1}
    for path in paths:
        for label in path[1:]:
            if label in used:
                raise AssertionError("non-hub label collision")
            used.add(label)
    leaf_labels = tuple(label for label in range(m + 1) if label not in used)
    return {"m": m, "paths": tuple(paths), "leaf_labels": leaf_labels}


def check_graceful(construction: dict[str, object]) -> bool:
    m = construction.get("m")
    paths = construction.get("paths")
    leaves = construction.get("leaf_labels")
    if not isinstance(m, int) or not isinstance(paths, tuple) or not isinstance(leaves, tuple):
        return False
    labels = [1]
    differences = []
    for path in paths:
        if not isinstance(path, tuple) or not path or path[0] != 1:
            return False
        labels.extend(path[1:])
        differences.extend(path_differences(path))
    for label in leaves:
        labels.append(label)
        differences.append(abs(label - 1))
    return (
        len(labels) == len(set(labels))
        and set(labels) == set(range(m + 1))
        and len(differences) == len(set(differences))
        and set(differences) == set(range(1, m + 1))
    )


def superdock_required_edges(lengths: Iterable[int]) -> int:
    ordered = sorted(lengths, reverse=True)
    return max((2 * index - 1) * 2 ** (length - 1) for index, length in enumerate(ordered, 1))


def old_exponential_plan_edges(c: int, other_lengths: Iterable[int]) -> int:
    lengths = tuple(sorted(other_lengths, reverse=True))
    _, m_c = closure_parameters(c)
    base = max((m_c,) + lengths) + 1
    return max(
        m_c,
        3 + max(length * base**index for index, length in enumerate(lengths, 1)),
    )


def audit() -> dict[str, object]:
    digest = hashlib.sha256()
    profiles = 0
    maximum_m = 0
    for c in range(2, 11):
        for r in range(1, 6):
            for lengths in combinations_with_replacement(range(2, 10), r):
                plan = make_plan(c, lengths)
                construction = construct(plan)
                assert check_graceful(construction)
                assert all(is_self_matched(path, construction["m"]) for path in construction["paths"])
                # The theorem is monotone in the number of added hub leaves.
                assert check_graceful(construct(plan, plan.minimum_leaves + 3))
                profiles += 1
                maximum_m = max(maximum_m, construction["m"])
                digest.update(
                    f"{c}:{plan.other_lengths}:{plan.q_base}:"
                    f"{plan.multipliers}:{plan.minimum_leaves}:"
                    f"{construction['m']}:{construction['paths']}\n".encode()
                )

    examples = {}
    for arms in ((2, 10, 10, 10), (3, 20, 15, 10, 5), (4,) + (25,) * 8):
        closure_index, plan = best_plan(arms)
        examples[str(arms)] = {
            "chosen_closure_index": closure_index,
            "chosen_closure_length": plan.closure_length,
            "new_required_edges": plan.total_edges_at_threshold,
            "new_required_leaves": plan.minimum_leaves,
            "old_exponential_packing_edges": old_exponential_plan_edges(
                plan.closure_length, plan.other_lengths
            ),
            "superdock_spider_criterion_edges": superdock_required_edges(arms),
        }

    return {
        "claim": "consecutive multipliers give the explicit threshold in THEOREM.md",
        "examples": examples,
        "maximum_threshold_edges_in_grid": maximum_m,
        "profile_digest_sha256": digest.hexdigest(),
        "profiles_checked": profiles,
        "test_grid": {
            "closure_lengths": [2, 10],
            "other_arm_count": [1, 5],
            "other_arm_lengths": [2, 9],
        },
        "trust_boundary": "the universal claim rests on THEOREM.md; code audits formulas and definitions",
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
