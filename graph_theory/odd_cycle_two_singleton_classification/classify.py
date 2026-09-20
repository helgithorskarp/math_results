#!/usr/bin/env python3
"""Uniform witnesses for the critical two-singleton slice on odd cycles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


def transfer(effective: int) -> int:
    """Exact signed message of a nonempty path branch."""

    if effective <= 1:
        return 2 * effective - 3
    if effective % 2 == 0:
        return effective // 2
    return (effective - 3) // 2


def branch_message(branch: Sequence[int]) -> int:
    """Message of a branch listed from its leaf toward its target."""

    occupied = False
    message = 0
    for pile in branch:
        occupied = occupied or pile > 0
        if occupied:
            message = transfer(pile + message)
    return message


def split_path(
    configuration: Sequence[int], cut: int, left_pile: int
) -> tuple[int, ...]:
    """Split ``cut`` into the endpoints of a clockwise opened path."""

    piles = tuple(configuration)
    order = len(piles)
    if order < 3 or any(type(value) is not int or value < 0 for value in piles):
        raise ValueError("invalid cycle configuration")
    if type(cut) is not int or not 0 <= cut < order:
        raise ValueError("invalid cut")
    if type(left_pile) is not int or not 0 <= left_pile <= piles[cut]:
        raise ValueError("invalid split")
    return (
        (left_pile,)
        + tuple(piles[(cut + offset) % order] for offset in range(1, order))
        + (piles[cut] - left_pile,)
    )


def target_score(path: Sequence[int], target: int) -> int:
    """Evaluate one path target by the exact signed-transfer rule."""

    piles = tuple(path)
    if type(target) is not int or not 0 <= target < len(piles):
        raise ValueError("invalid target")
    return (
        piles[target]
        + branch_message(piles[:target])
        + branch_message(tuple(reversed(piles[target + 1 :])))
    )


def critical_heavy(k: int) -> int:
    if type(k) is not int or k < 3:
        raise ValueError("k must be at least three")
    return 5 * (1 << (k - 1)) - 6


def critical_configuration(k: int, a: int, b: int) -> tuple[int, ...]:
    """Return ``M_k e_0 + e_a + e_b``, requiring ``0<a<b<=2k``."""

    critical_heavy(k)
    if type(a) is not int or type(b) is not int or not 0 < a < b <= 2 * k:
        raise ValueError("singleton positions must satisfy 0 < a < b <= 2k")
    result = [0] * (2 * k + 1)
    result[0] = critical_heavy(k)
    result[a] = result[b] = 1
    return tuple(result)


def stable_pair(k: int, a: int, b: int) -> bool:
    """Test membership in the dihedral orbit of the certified obstruction."""

    critical_configuration(k, a, b)
    return (a, b) in ((k - 1, k + 1), (k, k + 2))


@dataclass(frozen=True)
class Witness:
    cut: int
    left_pile: int
    target: int
    root_score: int


def explicit_witness(k: int, a: int, b: int) -> Witness | None:
    """Return the theorem's split witness, or ``None`` for the stable orbit."""

    configuration = critical_configuration(k, a, b)
    order = 2 * k + 1
    if stable_pair(k, a, b):
        return None

    if (a, b) == (k - 2, k + 1):
        witness = Witness(0, 3 * (1 << (k - 2)), k - 1, 1)
    elif (a, b) in ((k, k + 1), (k, k + 3)):
        witness = Witness(0, 0, k - 1, 1)
    elif b <= k:
        cut = b + 1
        witness = Witness(cut, 0, (-cut) % order, 0)
    elif a >= k + 1:
        witness = Witness(1, 0, order - 1, 0)
    else:
        cut = a + 1
        witness = Witness(cut, 0, (-cut) % order, 0)

    path = split_path(configuration, witness.cut, witness.left_pile)
    score = target_score(path, witness.target)
    if witness.root_score == 0:
        witness = Witness(witness.cut, witness.left_pile, witness.target, score)
    if score != witness.root_score or score < 1:
        raise AssertionError((k, a, b, witness, score))
    return witness


def verify_witness(k: int, a: int, b: int, witness: object) -> bool:
    """Check a claimed witness directly, rejecting malformed objects."""

    if not isinstance(witness, Witness):
        return False
    try:
        configuration = critical_configuration(k, a, b)
        path = split_path(configuration, witness.cut, witness.left_pile)
        score = target_score(path, witness.target)
    except (TypeError, ValueError):
        return False
    return score == witness.root_score and score >= 1
