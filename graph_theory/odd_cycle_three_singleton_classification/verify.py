#!/usr/bin/env python3
"""Definition-level audit for the critical three-singleton theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Sequence


ROOT = Path(__file__).resolve().parent


def transfer(value: int) -> int:
    if value <= 1:
        return 2 * value - 3
    if value % 2 == 0:
        return value // 2
    return (value - 3) // 2


def path_scores(path: Sequence[int]) -> tuple[int, ...]:
    piles = tuple(path)
    left = [0] * len(piles)
    right = [0] * len(piles)
    occupied = False
    message = 0
    for vertex in range(len(piles) - 1):
        occupied = occupied or piles[vertex] > 0
        if occupied:
            message = transfer(piles[vertex] + message)
        left[vertex + 1] = message
    occupied = False
    message = 0
    for vertex in range(len(piles) - 1, 0, -1):
        occupied = occupied or piles[vertex] > 0
        if occupied:
            message = transfer(piles[vertex] + message)
        right[vertex - 1] = message
    return tuple(piles[i] + left[i] + right[i] for i in range(len(piles)))


def split_path(configuration: Sequence[int], cut: int, left: int) -> tuple[int, ...]:
    piles = tuple(configuration)
    if len(piles) < 3 or any(type(x) is not int or x < 0 for x in piles):
        raise ValueError("invalid configuration")
    if type(cut) is not int or not 0 <= cut < len(piles):
        raise ValueError("invalid cut")
    if type(left) is not int or not 0 <= left <= piles[cut]:
        raise ValueError("invalid split")
    return ((left,)
            + tuple(piles[(cut + j) % len(piles)] for j in range(1, len(piles)))
            + (piles[cut] - left,))


def configuration(k: int, singleton_positions: Sequence[int]) -> tuple[int, ...]:
    positions = tuple(sorted(singleton_positions))
    if type(k) is not int or k < 3:
        raise ValueError("k must be at least three")
    if len(positions) != 3 or len(set(positions)) != 3:
        raise ValueError("exactly three distinct positions are required")
    if any(type(x) is not int or not 1 <= x <= 2 * k for x in positions):
        raise ValueError("a singleton position is out of range")
    piles = [0] * (2 * k + 1)
    piles[0] = 5 * (1 << (k - 1)) - 7
    for position in positions:
        piles[position] = 1
    return tuple(piles)


def canonical_family(k: int, positions: Sequence[int]) -> tuple[int, int] | None:
    a, b, c = sorted(positions)
    if (b, c) == (k - 1, k + 1) and 1 <= a <= k - 2:
        return 1, a
    if (b, c) == (k, k + 1) and 1 <= a <= k - 1:
        return 2, a
    if (b, c) == (k, k + 2) and 1 <= a <= k - 1:
        return 3, a
    return None


def exception_family(k: int, positions: Sequence[int]) -> tuple[int, int, bool] | None:
    positions = tuple(sorted(positions))
    direct = canonical_family(k, positions)
    if direct is not None:
        return direct[0], direct[1], False
    order = 2 * k + 1
    reflected = tuple(sorted((order - x) % order for x in positions))
    reverse = canonical_family(k, reflected)
    if reverse is not None:
        return reverse[0], reverse[1], True
    return None


@dataclass(frozen=True)
class Witness:
    cut: int
    left: int
    target: int
    score: int


def canonical_exception_witness(k: int, family: int, a: int) -> Witness:
    power = 1 << k
    if family == 1:
        if a == 2:
            return Witness(k - 1, 0, 2, 1)
        if a % 2 == 1 and k % 2 == 0:
            return Witness(0, power - (1 << a), k - 2, 1)
        if a % 2 == 1:
            return Witness(0, power // 2 - (1 << a), k - 1, 1)
        return Witness(0, power // 2 - (1 << a), k, 1)
    if family == 2:
        if a % 2 == 1 and k % 2 == 0:
            return Witness(0, power - (1 << a), 0, 3)
        if a % 2 == 1:
            return Witness(0, power // 2 - (1 << a), k - 2, 1)
        return Witness(0, 3 * power // 4 - (1 << a), k - 3, 1)
    if family != 3:
        raise ValueError("unknown family")
    if (k, a) == (3, 1):
        return Witness(0, 6, 3, 1)
    if a == 2:
        return Witness(k, 0, 1, 1)
    if a % 2 == 1 and k % 2 == 0:
        return Witness(0, power // 2 - (1 << a), k - 2, 1)
    if a % 2 == 1:
        return Witness(0, 3 * power // 4 - (1 << a), k - 3, 1)
    return Witness(0, power - (1 << a), 0, 3)


def reflect_witness(k: int, piles: Sequence[int], witness: Witness) -> Witness:
    order = 2 * k + 1
    reflected_cut = (-witness.cut) % order
    reflected_left = piles[reflected_cut] - witness.left
    return Witness(reflected_cut, reflected_left, order - witness.target, witness.score)


def theorem_witness(k: int, positions: Sequence[int]) -> Witness:
    piles = configuration(k, positions)
    antipodal = Witness(k, 0, k + 1, 0)
    score = path_scores(split_path(piles, antipodal.cut, antipodal.left))[antipodal.target]
    exceptional = exception_family(k, positions)
    if exceptional is None:
        if score < 1:
            raise AssertionError("antipodal reduction failed")
        return Witness(antipodal.cut, antipodal.left, antipodal.target, score)
    if score >= 1:
        raise AssertionError("exception family unexpectedly has positive heavy score")
    family, a, reflected = exceptional
    witness = canonical_exception_witness(k, family, a)
    if reflected:
        witness = reflect_witness(k, piles, witness)
    return witness


def verify_witness(k: int, positions: Sequence[int], witness: object) -> bool:
    if not isinstance(witness, Witness):
        return False
    try:
        piles = configuration(k, positions)
        path = split_path(piles, witness.cut, witness.left)
    except (TypeError, ValueError):
        return False
    if not 0 <= witness.target < len(path):
        return False
    score = path_scores(path)[witness.target]
    return score == witness.score and score >= 1


def audit(max_k: int) -> dict[str, int | str]:
    if max_k < 3:
        raise ValueError("max_k must be at least three")
    triples = 0
    antipodal = 0
    exceptions = 0
    score_one = 0
    records = []
    for k in range(3, max_k + 1):
        for positions in combinations(range(1, 2 * k + 1), 3):
            triples += 1
            family = exception_family(k, positions)
            witness = theorem_witness(k, positions)
            if not verify_witness(k, positions, witness):
                raise AssertionError((k, positions, witness))
            if family is None:
                antipodal += 1
            else:
                exceptions += 1
            score_one += witness.score == 1
            records.append(
                f"{k}|{positions}|{witness.cut}|{witness.left}|"
                f"{witness.target}|{witness.score}"
            )
    digest = hashlib.sha256(("\n".join(records) + "\n").encode()).hexdigest()
    return {
        "max_k": max_k,
        "triples": triples,
        "antipodal_witnesses": antipodal,
        "exception_family_witnesses": exceptions,
        "score_one_witnesses": score_one,
        "record_sha256": digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=32)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.max_k)
    if args.check_expected:
        expected = json.loads((ROOT / "EXPECTED.json").read_text())
        if result != expected:
            raise AssertionError((result, expected))
    for key, value in result.items():
        print(f"{key}={value}")
    print("THREE-SINGLETON CLASSIFICATION VERIFIED")


if __name__ == "__main__":
    main()
