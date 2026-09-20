#!/usr/bin/env python3
"""Mass-independent split search for stackability on an undirected cycle.

The split-path theorem reduces cycle stackability to path lifts obtained by
splitting one cycle pile.  This module compresses the possible allocations:
for each cut and target it tests only dyadic boundary representatives, whose
number depends on the cycle order but not on the total mass.
"""

from __future__ import annotations

from typing import Sequence


def transfer(effective: int) -> int:
    """Exact signed message of a nonempty path branch."""

    if effective <= 1:
        return 2 * effective - 3
    if effective % 2 == 0:
        return effective // 2
    return (effective - 3) // 2


def safe_threshold(depth: int) -> int:
    """A uniform threshold above which a depth-``depth`` branch is dyadic."""

    if type(depth) is not int or depth < 0:
        raise ValueError("depth must be a nonnegative integer")
    return 0 if depth == 0 else (1 << (depth + 1)) - 2


def candidate_splits(pile: int, left_depth: int, right_depth: int) -> tuple[int, ...]:
    """Return a complete mass-independent split set for one path target.

    ``pile`` is split as ``x + (pile-x)``.  The two split endpoints are at
    distances ``left_depth`` and ``right_depth`` from the target, so their
    sum is the length of the opened path.  On the central safe interval the
    target score changes by a fixed amount when ``x`` is increased by
    ``2**max(left_depth, right_depth)``.  Hence one extremal representative
    from each residue class suffices.
    """

    if type(pile) is not int or pile < 0:
        raise ValueError("pile must be a nonnegative integer")
    if (
        type(left_depth) is not int
        or type(right_depth) is not int
        or left_depth < 0
        or right_depth < 0
    ):
        raise ValueError("depths must be nonnegative integers")

    left_safe = safe_threshold(left_depth)
    right_safe = safe_threshold(right_depth)
    result: set[int] = set()

    # Every allocation outside the interval where both branches are safe.
    result.update(range(0, min(pile + 1, left_safe)))
    right_start = max(0, pile - right_safe + 1)
    result.update(range(right_start, pile + 1))

    low = left_safe
    high = pile - right_safe
    if low <= high:
        period = 1 << max(left_depth, right_depth)
        delta = (period >> left_depth) - (period >> right_depth)
        for residue in range(period):
            first = low + ((residue - low) % period)
            if first > high:
                continue
            if delta > 0:
                representative = first + ((high - first) // period) * period
            else:
                representative = first
            result.add(representative)

    return tuple(sorted(result))


def _configuration(values: Sequence[int]) -> tuple[int, ...]:
    piles = tuple(values)
    if len(piles) < 3:
        raise ValueError("a cycle needs at least three vertices")
    if any(type(value) is not int or value < 0 for value in piles):
        raise ValueError("piles must be nonnegative integers")
    return piles


def split_path(configuration: Sequence[int], cut: int, left_pile: int) -> tuple[int, ...]:
    """Open a cycle at ``cut`` and split its pile between the path endpoints."""

    piles = _configuration(configuration)
    order = len(piles)
    if type(cut) is not int or not 0 <= cut < order:
        raise ValueError("cut is outside the cycle")
    if type(left_pile) is not int or not 0 <= left_pile <= piles[cut]:
        raise ValueError("invalid endpoint split")
    return (
        (left_pile,)
        + tuple(piles[(cut + offset) % order] for offset in range(1, order))
        + (piles[cut] - left_pile,)
    )


def branch_message(branch: Sequence[int]) -> int:
    """Message sent by a path branch listed from its leaf toward its root."""

    occupied = False
    message = 0
    for pile in branch:
        occupied = occupied or pile > 0
        if occupied:
            message = transfer(pile + message)
    return message


def target_score(path: Sequence[int], target: int) -> int:
    """Exact signed transfer score at one target of a path."""

    if type(target) is not int or not 0 <= target < len(path):
        raise ValueError("target is outside the path")
    return (
        path[target]
        + branch_message(path[:target])
        + branch_message(tuple(reversed(path[target + 1 :])))
    )


def compressed_cycle_witness(configuration: Sequence[int]) -> dict[str, int] | None:
    """Return an exact split-path witness using dyadic split compression."""

    piles = _configuration(configuration)
    order = len(piles)
    for cut, pile in enumerate(piles):
        for target in range(order + 1):
            for left_pile in candidate_splits(pile, target, order - target):
                score = target_score(split_path(piles, cut, left_pile), target)
                if score >= 1:
                    return {
                        "cut": cut,
                        "left_pile": left_pile,
                        "target": target,
                        "root_score": score,
                    }
    return None

def verify_witness(configuration: Sequence[int], witness: object) -> bool:
    """Check a positive certificate directly, without trusting compression."""

    if not isinstance(witness, dict):
        return False
    if set(witness) != {"cut", "left_pile", "target", "root_score"}:
        return False
    if any(type(witness[key]) is not int for key in witness):
        return False
    try:
        path = split_path(configuration, witness["cut"], witness["left_pile"])
        score = target_score(path, witness["target"])
    except ValueError:
        return False
    return score == witness["root_score"] and score >= 1


def exhaustive_cycle_witness(configuration: Sequence[int]) -> dict[str, int] | None:
    """Reference split scan, used only by the verifier on bounded inputs."""

    piles = _configuration(configuration)
    order = len(piles)
    for cut, pile in enumerate(piles):
        for target in range(order + 1):
            for left_pile in range(pile + 1):
                score = target_score(split_path(piles, cut, left_pile), target)
                if score >= 1:
                    return {
                        "cut": cut,
                        "left_pile": left_pile,
                        "target": target,
                        "root_score": score,
                    }
    return None
