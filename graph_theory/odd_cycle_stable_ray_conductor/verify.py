#!/usr/bin/env python3
"""Direct exact checker for the stable odd-cycle stacking-ray certificates."""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass


def transfer(effective: int) -> int:
    """Exact message of a nonempty path branch."""

    if effective <= 1:
        return 2 * effective - 3
    if effective % 2 == 0:
        return effective // 2
    return (effective - 3) // 2


def branch_message(branch: tuple[int, ...]) -> int:
    """Message of piles listed from a leaf toward (but excluding) the target."""

    occupied = False
    message = 0
    for pile in branch:
        occupied = occupied or pile > 0
        if occupied:
            message = transfer(pile + message)
    return message


def split_path(
    configuration: tuple[int, ...], cut: int, left_pile: int
) -> tuple[int, ...]:
    """Open the cycle at ``cut`` and split its pile between the endpoints."""

    order = len(configuration)
    if order < 3 or any(type(x) is not int or x < 0 for x in configuration):
        raise ValueError("invalid cycle configuration")
    if type(cut) is not int or not 0 <= cut < order:
        raise ValueError("invalid cut")
    if type(left_pile) is not int or not 0 <= left_pile <= configuration[cut]:
        raise ValueError("invalid split")
    return (
        (left_pile,)
        + tuple(configuration[(cut + offset) % order] for offset in range(1, order))
        + (configuration[cut] - left_pile,)
    )


def target_score(path: tuple[int, ...], target: int) -> int:
    """Return the exact signed score at one path target."""

    if type(target) is not int or not 0 <= target < len(path):
        raise ValueError("invalid target")
    return (
        path[target]
        + branch_message(path[:target])
        + branch_message(tuple(reversed(path[target + 1 :])))
    )


def conductor(k: int) -> int:
    if type(k) is not int or k < 3:
        raise ValueError("k must be at least three")
    return 5 * (1 << (k - 1)) - 5


def stable_configuration(k: int, heavy: int) -> tuple[int, ...]:
    if heavy < 0:
        raise ValueError("heavy pile must be nonnegative")
    result = [0] * (2 * k + 1)
    result[0] = heavy
    result[k] = 1
    result[k + 2] = 1
    return tuple(result)


@dataclass(frozen=True)
class Witness:
    cut: int
    left_pile: int
    target: int
    root_score: int


def explicit_witness(k: int, heavy: int) -> Witness:
    """Return the theorem's four-case witness for ``heavy >= conductor(k)``."""

    base = conductor(k)
    if type(heavy) is not int or heavy < base:
        raise ValueError("the explicit ray witness starts at the conductor")
    power = 1 << k
    excess = heavy - base
    if excess == 0:
        return Witness(0, power - 8, 2, 1)
    if excess == 1:
        return Witness(0, power - 4, 1, 1)
    if excess == 2:
        return Witness(k, 0, 1, 1)
    return Witness(0, power + excess - 5, 0, excess - 2)


def verify_witness(k: int, heavy: int, witness: object) -> bool:
    """Check a witness from the split and transfer definitions."""

    if not isinstance(witness, Witness):
        return False
    try:
        path = split_path(
            stable_configuration(k, heavy), witness.cut, witness.left_pile
        )
        score = target_score(path, witness.target)
    except (TypeError, ValueError):
        return False
    return score == witness.root_score and score >= 1


def audit(max_k: int, max_excess: int) -> dict[str, int | str]:
    if max_k < 3 or max_excess < 3:
        raise ValueError("audit bounds are too small")
    records: list[str] = []
    direct = 0
    large = 0
    for k in range(3, max_k + 1):
        base = conductor(k)
        for excess in range(max_excess + 1):
            heavy = base + excess
            witness = explicit_witness(k, heavy)
            if not verify_witness(k, heavy, witness):
                raise AssertionError((k, excess, witness))
            expected = 1 if excess <= 2 else excess - 2
            if witness.root_score != expected:
                raise AssertionError("closed score formula failed")
            records.append(
                f"{k}|{excess}|{witness.cut}|{witness.left_pile}|"
                f"{witness.target}|{witness.root_score}"
            )
            direct += 1

        for excess in (
            (1 << k) + 17,
            (1 << (k + 1)) + 3,
            10**40 + k,
        ):
            heavy = base + excess
            witness = explicit_witness(k, heavy)
            if not verify_witness(k, heavy, witness):
                raise AssertionError((k, excess, witness))
            records.append(
                f"L|{k}|{excess}|{witness.left_pile}|{witness.root_score}"
            )
            large += 1

    digest = hashlib.sha256(("\n".join(records) + "\n").encode("ascii")).hexdigest()
    return {
        "max_k": max_k,
        "max_excess": max_excess,
        "direct_witnesses": direct,
        "large_excess_witnesses": large,
        "record_sha256": digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=512)
    parser.add_argument("--max-excess", type=int, default=24)
    args = parser.parse_args()
    result = audit(args.max_k, args.max_excess)
    for key, value in result.items():
        print(f"{key}={value}")
    print("DIRECT STABLE-RAY CERTIFICATES VERIFIED")


if __name__ == "__main__":
    main()
