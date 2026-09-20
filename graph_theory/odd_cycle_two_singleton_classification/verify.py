#!/usr/bin/env python3
"""Exact direct audit of the critical two-singleton classification."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from classify import (
    critical_configuration,
    explicit_witness,
    stable_pair,
    verify_witness,
)


def audit(max_k: int) -> dict[str, int | str]:
    if max_k < 3:
        raise ValueError("max_k must be at least three")
    records: list[str] = []
    stackable = 0
    stable = 0
    score_one = 0
    for k in range(3, max_k + 1):
        for a in range(1, 2 * k + 1):
            for b in range(a + 1, 2 * k + 1):
                critical_configuration(k, a, b)
                witness = explicit_witness(k, a, b)
                if stable_pair(k, a, b):
                    if witness is not None:
                        raise AssertionError("stable obstruction received a witness")
                    stable += 1
                    records.append(f"N|{k}|{a}|{b}")
                    continue
                if witness is None or not verify_witness(k, a, b, witness):
                    raise AssertionError((k, a, b, witness))
                stackable += 1
                score_one += witness.root_score == 1
                records.append(
                    f"Y|{k}|{a}|{b}|{witness.cut}|{witness.left_pile}|"
                    f"{witness.target}|{witness.root_score}"
                )
    digest = hashlib.sha256(("\n".join(records) + "\n").encode("ascii")).hexdigest()
    return {
        "max_k": max_k,
        "pairs_checked": stackable + stable,
        "stackable_witnesses": stackable,
        "stable_obstructions": stable,
        "score_one_witnesses": score_one,
        "record_sha256": digest,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-k", type=int, default=64)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = audit(args.max_k)
    if args.check_expected:
        expected = json.loads(Path("EXPECTED.json").read_text(encoding="utf-8"))
        if result != expected:
            raise AssertionError((result, expected))
    for key, value in result.items():
        print(f"{key}={value}")
    print("TWO-SINGLETON CLASSIFICATION WITNESSES VERIFIED")


if __name__ == "__main__":
    main()
