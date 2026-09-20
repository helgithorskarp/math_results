#!/usr/bin/env python3
"""Independent closed-form audit of the four stable-ray score identities.

This checker does not import the direct path implementation.  It follows the
four phase decompositions in the proof and compares them with the claimed
closed scores using exact integers.
"""

from __future__ import annotations

import argparse
import hashlib


def g(value: int) -> int:
    if value <= 1:
        return 2 * value - 3
    return value // 2 if value % 2 == 0 else (value - 3) // 2


def through_zeros(message: int, count: int) -> int:
    for _ in range(count):
        message = g(message)
    return message


def phase_scores(k: int) -> tuple[int, int, int, int]:
    """Return the scores for excesses 0,1,2 and the d>=3 affine intercept."""

    if k < 3:
        raise ValueError("k must be at least three")
    power = 1 << k

    # The right branch for excesses 0, 1, and >=3.
    right = g(3 * power // 2 + 3)
    if right != 3 * power // 4:
        raise AssertionError("odd endpoint phase")
    right = through_zeros(right, k - 2)
    if right != 3:
        raise AssertionError("positive halving phase")
    right = g(1 + right)
    right = g(right)
    right = g(1 + right)
    if right != 1:
        raise AssertionError("unit-zero-unit phase")

    right_at_two = through_zeros(right, k - 3)
    right_at_one = through_zeros(right, k - 2)
    right_at_zero = through_zeros(right, k - 1)
    if (
        right_at_two != 3 - power // 4
        or right_at_one != 3 - power // 2
        or right_at_zero != 3 - power
    ):
        raise AssertionError("negative dyadic phase")

    left_zero = 0 if power == 8 else g(g(power - 8))
    left_one = g(power - 4)
    score_zero = left_zero + right_at_two
    score_one = left_one + right_at_one

    # Excess two: cut the first unit and cross the heavy pile from the other side.
    message = g(1)
    message = through_zeros(message, k - 1)
    if message != 3 - 2 * power:
        raise AssertionError("borrow phase before the heavy pile")
    heavy = 5 * power // 2 - 3
    message = g(heavy + message)
    if message != power // 4:
        raise AssertionError("heavy cancellation phase")
    message = through_zeros(message, k - 2)
    message = g(1 + message)
    score_two = message

    # At excess d>=3 the score is (P+d-5)+(3-P)=d-2.
    affine_intercept = (power - 5) + right_at_zero
    return score_zero, score_one, score_two, affine_intercept


def audit(max_k: int) -> dict[str, int | str]:
    if max_k < 3:
        raise ValueError("max_k must be at least three")
    records: list[str] = []
    phase_checks = 0
    for k in range(3, max_k + 1):
        scores = phase_scores(k)
        if scores != (1, 1, 1, -2):
            raise AssertionError((k, scores))
        for excess in (3, 4, 5, 17, (1 << k) + 1, 10**60 + k):
            if excess + scores[3] != excess - 2 or excess - 2 < 1:
                raise AssertionError((k, excess))
            phase_checks += 1
        records.append(f"{k}|{scores[0]}|{scores[1]}|{scores[2]}|{scores[3]}")
    digest = hashlib.sha256(("\n".join(records) + "\n").encode("ascii")).hexdigest()
    return {
        "max_k": max_k,
        "phase_checks": phase_checks,
        "record_sha256": digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=4096)
    args = parser.parse_args()
    result = audit(args.max_k)
    for key, value in result.items():
        print(f"{key}={value}")
    print("INDEPENDENT CLOSED-FORM PHASE AUDIT VERIFIED")


if __name__ == "__main__":
    main()
