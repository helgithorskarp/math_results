#!/usr/bin/env python3
"""Audit that five new safe mantles close the complete symbolic a=1 frontier."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
EXPECTED_UPSTREAM = {
    "source": "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c",
    "dead": "33d53244922865533b379d8f40d91063e1758f5997362e940f5d1ea503e7686d",
    "trimodal": "532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059",
    "small_a_c3": "1e2af60896b1f3e5970c877cb630fe8d4171eb0b1e5335d063689767b9187e1f",
    "mantle": "7669175bf86a2ad4938bc1cd8a1aae8e7a64b5e59bcfc4904b6e6b4d7646a192",
}


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(str(message))


def admissible(counts: tuple[int, int, int]) -> bool:
    a, b, _ = counts
    order = sum(counts) + 1
    return order >= 22 and (order % 11 != 0 or a + b >= 10)


def pattern_has_admissible_lift(
    counts: tuple[int, int, int], high: tuple[bool, bool, bool]
) -> bool:
    if not any(high):
        return admissible(counts)
    if high[0] or high[1]:
        return True
    a, b, _ = counts
    return (sum(counts) + 1) % 11 != 0 or a + b >= 10


def exact_point_or_ray(witnesses: list[dict], target: tuple[int, int, int]) -> bool:
    for witness in witnesses:
        start = tuple(witness["counts"])
        if target == start:
            return True
        for mode in witness["grow"]:
            coordinate = SUPPORT.index(mode)
            if all(target[i] == start[i] for i in range(3) if i != coordinate):
                if target[coordinate] >= start[coordinate]:
                    if (target[coordinate] - start[coordinate]) % mode == 0:
                        return True
    return False


def in_orthant(
    target: tuple[int, int, int], seed: tuple[int, int, int], modes: set[int]
) -> bool:
    for coordinate, mode in enumerate(SUPPORT):
        if mode in modes:
            if target[coordinate] < seed[coordinate]:
                return False
            if (target[coordinate] - seed[coordinate]) % mode:
                return False
        elif target[coordinate] != seed[coordinate]:
            return False
    return True


def completed_c1(target: tuple[int, int, int]) -> bool:
    a, b, c = target
    return c == 1 and a >= 1 and b >= 1 and a + b >= 20


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("coverage_data", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    raw = args.coverage_data.read_bytes()
    data = json.loads(raw)
    certificate = json.loads(args.certificate.read_bytes())
    require(data["schema"] == "bhr-1-2-11-a1-coverage-data-v1", "coverage schema")
    require(data["upstream_sha256"] == EXPECTED_UPSTREAM, "upstream hashes")
    require(len(data["cases"]) == 22, "residue cases")

    dead = {tuple(record["base"]): tuple(record["seed"]) for record in data["dead_orthants"]}
    tri = {tuple(record["base"]): tuple(record["safe_seed"]) for record in data["trimodal"]}
    cap = {tuple(record["base"]): tuple(record["cap_seed"]) for record in data["trimodal"]}
    mantle = {tuple(record["base"]): tuple(record["seed"]) for record in data["mantle"]}
    small_a_c3 = tuple(data["small_a_c3_seed"])
    new_seeds = [tuple(record["counts"]) for record in certificate["seeds"]]

    patterns = 0
    prior_residual = []
    final_residual = []
    for case in data["cases"]:
        base = tuple(case["base"])
        maxima = tuple(case["maxima"])
        axes = [
            [1],
            list(range(base[1], maxima[1] + 1, 2)) + [maxima[1] + 2],
            list(range(base[2], maxima[2] + 1, 11)) + [maxima[2] + 11],
        ]
        for target in itertools.product(*axes):
            high = (False, target[1] > maxima[1], target[2] > maxima[2])
            if not pattern_has_admissible_lift(target, high):
                continue
            patterns += 1
            covered = exact_point_or_ray(case["witnesses"], target)
            if not covered and base in dead:
                covered = in_orthant(target, dead[base], {1, 2})
            if not covered:
                covered = in_orthant(target, tri[base], set(SUPPORT))
            if not covered:
                covered = in_orthant(target, cap[base], set(SUPPORT))
            if not covered:
                covered = completed_c1(target)
            if not covered:
                covered = in_orthant(target, small_a_c3, {2, 11})
            if not covered and base in mantle:
                covered = in_orthant(target, mantle[base], {2, 11})
            if covered:
                continue
            record = (base, target, high)
            prior_residual.append(record)
            if not any(in_orthant(target, seed, {2, 11}) for seed in new_seeds):
                final_residual.append(record)

    canonical = json.dumps(prior_residual, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    require(patterns == 502, ("symbolic patterns", patterns))
    require(len(prior_residual) == 29, ("prior residual", len(prior_residual)))
    require(
        digest == "7d6b7ae4fb95c220d9a0a11835baaf1fc3aef8216be3db36445f7122a671c88c",
        ("residual digest", digest),
    )
    require(not final_residual, ("uncovered", final_residual))
    print(f"coverage_data_sha256={hashlib.sha256(raw).hexdigest()}")
    print(f"a1_symbolic_patterns={patterns}")
    print(f"prior_residual_patterns={len(prior_residual)}")
    print(f"prior_residual_sha256={digest}")
    print("new_safe_orthants=5")
    print("final_residual_patterns=0")
    print("AUDITED")


if __name__ == "__main__":
    main()
