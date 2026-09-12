#!/usr/bin/env python3
"""Definition-level verification of the code and the recorded exchange."""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


def load_words(path: Path) -> list[str]:
    words = [line.strip() for line in path.read_text(encoding="ascii").splitlines() if line.strip()]
    if any(len(word) != 32 or set(word) - {"0", "1"} for word in words):
        raise ValueError(f"malformed binary word in {path}")
    return words


def distance(left: str, right: str) -> int:
    return sum(a != b for a, b in zip(left, right, strict=True))


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit("usage: verify.py INCUMBENT CODE EXCHANGE_JSON")
    incumbent_path, code_path, witness_path = map(Path, sys.argv[1:])
    incumbent = load_words(incumbent_path)
    code = load_words(code_path)
    witness = json.loads(witness_path.read_text(encoding="utf-8"))

    if hashlib.sha256(incumbent_path.read_bytes()).hexdigest() != witness["source_sha256"]:
        raise ValueError("incumbent SHA-256 mismatch")
    if len(incumbent) != 1667 or len(set(incumbent)) != 1667:
        raise ValueError("invalid incumbent cardinality")
    if len(code) != 1668 or len(set(code)) != 1668:
        raise ValueError("invalid constructed-code cardinality")
    if any(word.count("1") != 8 for word in incumbent + code):
        raise ValueError("non-weight-eight word")

    removed_indices = tuple(entry["zero_based_index"] for entry in witness["removed"])
    removed_words = tuple(entry["word"] for entry in witness["removed"])
    if len(set(removed_indices)) != 5 or tuple(incumbent[i] for i in removed_indices) != removed_words:
        raise ValueError("removal witness does not match incumbent")
    added = tuple(entry["word"] for entry in witness["added"])
    reconstructed = [word for index, word in enumerate(incumbent) if index not in removed_indices]
    reconstructed.extend(added)
    if Counter(reconstructed) != Counter(code):
        raise ValueError("code is not the recorded five-for-six exchange")

    distance_histogram: Counter[int] = Counter()
    minimum_distance = 33
    for first, second in itertools.combinations(code, 2):
        value = distance(first, second)
        distance_histogram[value] += 1
        minimum_distance = min(minimum_distance, value)
    if minimum_distance < 8:
        raise ValueError("minimum distance below eight")

    blocker_sets = []
    for word in added:
        blockers = tuple(index for index, old in enumerate(incumbent) if distance(word, old) < 8)
        blocker_sets.append(blockers)
    expected_blockers = [
        (142, 348, 1520),
        (1520,),
        (142, 452),
        (348,),
        (267, 452),
        (267,),
    ]
    if blocker_sets != expected_blockers:
        raise ValueError("unexpected blocker sets for added words")
    if any(distance(left, right) < 8 for left, right in itertools.combinations(added, 2)):
        raise ValueError("added words are not pairwise compatible")

    hall_minima = []
    blocker_set_values = [set(blockers) for blockers in blocker_sets]
    for size in range(1, 7):
        hall_minima.append(
            min(len(set().union(*(blocker_set_values[i] for i in indices)))
                for indices in itertools.combinations(range(6), size))
        )
    if hall_minima != [1, 2, 3, 4, 5, 5]:
        raise ValueError("blocker family is not the expected Hall circuit")

    print(f"incumbent_size={len(incumbent)}")
    print(f"constructed_size={len(code)}")
    print(f"distinct_words={len(set(code))}")
    print("constant_weight=8")
    print(f"pairs_checked={sum(distance_histogram.values())}")
    print(f"minimum_distance={minimum_distance}")
    print("distance_histogram=" + ",".join(f"{key}:{distance_histogram[key]}" for key in sorted(distance_histogram)))
    print("removed_zero_based=" + ",".join(map(str, removed_indices)))
    print("added_blockers=" + ";".join(",".join(map(str, blockers)) for blockers in blocker_sets))
    print("hall_union_minima=" + ",".join(map(str, hall_minima)))
    print("kissing_bound_tau_32=346560")
    print("verification=PASS")


if __name__ == "__main__":
    main()
