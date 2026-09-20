#!/usr/bin/env python3
"""Exact split-path boundary test for stacking on an undirected cycle.

The implementation uses only integer arithmetic.  A witness cuts one cycle
vertex into the two endpoints of a path, splits that vertex's pile between
the endpoints, and gives a path target with positive transfer score.
"""

from __future__ import annotations

from typing import Sequence


def transfer(effective: int) -> int:
    """Maximum net transfer of a nonempty tree branch to its parent."""

    if effective <= 1:
        return 2 * effective - 3
    if effective % 2 == 0:
        return effective // 2
    return (effective - 3) // 2


def _configuration(values: Sequence[int], minimum_length: int) -> tuple[int, ...]:
    result = tuple(values)
    if len(result) < minimum_length:
        raise ValueError(f"configuration needs at least {minimum_length} vertices")
    if any(type(value) is not int or value < 0 for value in result):
        raise ValueError("piles must be nonnegative integers")
    return result


def path_root_scores(configuration: Sequence[int]) -> tuple[int, ...]:
    """Return the exact tree-transfer score at every target of a path."""

    piles = _configuration(configuration, 1)
    order = len(piles)
    left = [0] * order
    right = [0] * order

    occupied = False
    message = 0
    for vertex in range(order - 1):
        occupied = occupied or piles[vertex] > 0
        effective = piles[vertex] + message
        message = transfer(effective) if occupied else 0
        left[vertex + 1] = message

    occupied = False
    message = 0
    for vertex in range(order - 1, 0, -1):
        occupied = occupied or piles[vertex] > 0
        effective = piles[vertex] + message
        message = transfer(effective) if occupied else 0
        right[vertex - 1] = message

    return tuple(
        piles[vertex] + left[vertex] + right[vertex]
        for vertex in range(order)
    )


def split_lift(
    configuration: Sequence[int], cut: int, left_pile: int
) -> tuple[int, ...]:
    """Split ``cut`` into the endpoints of a clockwise path.

    The path order is
    ``cut_left, cut+1, ..., cut-1, cut_right`` modulo the cycle order.
    """

    piles = _configuration(configuration, 3)
    order = len(piles)
    if type(cut) is not int or not 0 <= cut < order:
        raise ValueError("cut is outside the cycle")
    if type(left_pile) is not int or not 0 <= left_pile <= piles[cut]:
        raise ValueError("invalid endpoint split")
    interior = tuple(piles[(cut + offset) % order] for offset in range(1, order))
    return (left_pile,) + interior + (piles[cut] - left_pile,)


def cycle_split_witness(configuration: Sequence[int]) -> dict[str, int] | None:
    """Return a compact positive stackability witness, or ``None``.

    By the split-path theorem, ``None`` is also an exact negative answer, not
    merely failure of a sufficient test.
    """

    piles = _configuration(configuration, 3)
    for cut, pile in enumerate(piles):
        for left_pile in range(pile + 1):
            scores = path_root_scores(split_lift(piles, cut, left_pile))
            for target, score in enumerate(scores):
                if score >= 1:
                    return {
                        "cut": cut,
                        "left_pile": left_pile,
                        "target": target,
                        "root_score": score,
                    }
    return None


def verify_witness(configuration: Sequence[int], witness: object) -> bool:
    """Check a split witness from its definition, rejecting malformed data."""

    if not isinstance(witness, dict):
        return False
    if set(witness) != {"cut", "left_pile", "target", "root_score"}:
        return False
    if any(type(witness[key]) is not int for key in witness):
        return False
    try:
        lifted = split_lift(
            configuration, witness["cut"], witness["left_pile"]
        )
    except ValueError:
        return False
    target = witness["target"]
    if not 0 <= target < len(lifted):
        return False
    score = path_root_scores(lifted)[target]
    return score == witness["root_score"] and score >= 1


def spanning_path_stackable(configuration: Sequence[int]) -> bool:
    """Test whether deleting some cycle edge already suffices.

    This deliberately does not split a pile.  It is included to distinguish
    the split theorem from the strictly weaker spanning-path shortcut.
    """

    piles = _configuration(configuration, 3)
    order = len(piles)
    for first in range(order):
        path = tuple(piles[(first + offset) % order] for offset in range(order))
        if max(path_root_scores(path)) >= 1:
            return True
    return False
