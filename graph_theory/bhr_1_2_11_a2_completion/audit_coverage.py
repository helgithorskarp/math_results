#!/usr/bin/env python3
"""Audit that three new safe mantles close the symbolic a=2 frontier."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path

SUPPORT = (1, 2, 11)
EXPECTED_COVERAGE_SHA256 = "26aaf6f8ac7beefb5674868add54a47ad23ae57476b60763c6a63c3d6d996e74"
EXPECTED_UPSTREAM = {
    "source": "e92ba9b84512e8829400bdeaf0fd0ef0082b56b26e6720e882ba2c2bbb8fbc6c",
    "dead": "33d53244922865533b379d8f40d91063e1758f5997362e940f5d1ea503e7686d",
    "trimodal": "532470ffe31ff3e5acb4da51a78c15f172d2d00db6816dd43d5dc44a243bc059",
    "small_a_c3": "1e2af60896b1f3e5970c877cb630fe8d4171eb0b1e5335d063689767b9187e1f",
    "mantle": "7669175bf86a2ad4938bc1cd8a1aae8e7a64b5e59bcfc4904b6e6b4d7646a192",
}
EXPECTED_PRIOR_RESIDUAL_SHA256 = "3ab670922ba56d55e49d9af729b8a1c1b4829a11f20e03cf667edf32f95dcc0e"


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(str(message))


def pattern_has_admissible_lift(
    counts: tuple[int, int, int], high: tuple[bool, bool, bool]
) -> bool:
    if not any(high):
        a, b, _ = counts
        order = sum(counts) + 1
        return order >= 22 and (order % 11 != 0 or a + b >= 10)
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


def audit(coverage_path: Path, certificate_path: Path) -> dict[str, object]:
    raw = coverage_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == EXPECTED_COVERAGE_SHA256, "coverage hash")
    data = json.loads(raw)
    certificate = json.loads(certificate_path.read_bytes())
    require(data["schema"] == "bhr-1-2-11-a1-coverage-data-v1", "coverage schema")
    require(data["upstream_sha256"] == EXPECTED_UPSTREAM, "upstream hashes")
    require(len(data["cases"]) == 22, "residue cases")
    require(certificate["schema"] == "bhr-1-2-11-a2-completion-v1", "certificate schema")

    dead = {
        tuple(record["base"]): tuple(record["seed"])
        for record in data["dead_orthants"]
    }
    tri = {
        tuple(record["base"]): tuple(record["safe_seed"])
        for record in data["trimodal"]
    }
    cap = {
        tuple(record["base"]): tuple(record["cap_seed"])
        for record in data["trimodal"]
    }
    small_a_c3 = tuple(data["small_a_c3_seed"])
    new_seeds = [tuple(record["counts"]) for record in certificate["seeds"]]
    require(
        new_seeds == [(2, 8, 28), (2, 8, 29), (2, 8, 30)],
        ("new seed corners", new_seeds),
    )

    patterns = 0
    prior_residual = []
    final_residual = []
    for case in data["cases"]:
        base = tuple(case["base"])
        maxima = tuple(case["maxima"])
        axes = [
            [2],
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
            if covered:
                continue
            record = (base, target, high)
            prior_residual.append(record)
            if not any(in_orthant(target, seed, {2, 11}) for seed in new_seeds):
                final_residual.append(record)

    canonical = json.dumps(prior_residual, separators=(",", ":"))
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    require(patterns == 521, ("symbolic patterns", patterns))
    require(len(prior_residual) == 19, ("prior residual", len(prior_residual)))
    require(digest == EXPECTED_PRIOR_RESIDUAL_SHA256, ("residual digest", digest))
    require(not final_residual, ("uncovered", final_residual))
    return {
        "coverage_data_sha256": hashlib.sha256(raw).hexdigest(),
        "a2_symbolic_patterns": patterns,
        "prior_residual_patterns": len(prior_residual),
        "prior_residual_sha256": digest,
        "new_safe_orthants": len(new_seeds),
        "final_residual_patterns": len(final_residual),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("coverage_data", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    for key, value in audit(args.coverage_data, args.certificate).items():
        print(f"{key}={value}")
    print("AUDITED")


if __name__ == "__main__":
    main()
