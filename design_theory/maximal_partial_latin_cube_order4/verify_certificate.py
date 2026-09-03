#!/usr/bin/env python3
"""Definition-level verifier for maximal partial Latin hypercube certificates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path


Word = tuple[int, ...]


def hamming_distance(left: Word, right: Word) -> int:
    return sum(a != b for a, b in zip(left, right, strict=True))


def verify(path: Path) -> dict[str, object]:
    raw = path.read_bytes()
    payload = json.loads(raw)
    q = int(payload["order"])
    dimension = int(payload["dimension"])
    listed = [tuple(map(int, word)) for word in payload["selected_words"]]
    selected = set(listed)
    if q < 2 or dimension < 2:
        raise ValueError("order and dimension must both be at least two")
    if len(selected) != len(listed):
        raise ValueError("selected_words contains a duplicate")
    if any(len(word) != dimension for word in selected):
        raise ValueError("a word has the wrong dimension")
    if any(value < 0 or value >= q for word in selected for value in word):
        raise ValueError("a word coordinate is outside range(order)")

    minimum_distance = dimension + 1
    for left, right in itertools.combinations(selected, 2):
        distance = hamming_distance(left, right)
        minimum_distance = min(minimum_distance, distance)
        if distance < 2:
            raise ValueError(f"incompatible selected words: {left}, {right}")

    coverage_counts: list[int] = []
    for word in itertools.product(range(q), repeat=dimension):
        coverage = sum(hamming_distance(word, codeword) <= 1 for codeword in selected)
        if coverage == 0:
            raise ValueError(f"selected set is not maximal; addable word: {word}")
        coverage_counts.append(coverage)

    canonical = "".join(",".join(map(str, word)) + "\n" for word in sorted(selected))
    coverage_histogram = {
        str(value): coverage_counts.count(value) for value in sorted(set(coverage_counts))
    }
    coordinate_slice_counts = [
        [sum(word[coordinate] == value for word in selected) for value in range(q)]
        for coordinate in range(dimension)
    ]
    return {
        "status": "VERIFIED",
        "order": q,
        "dimension": dimension,
        "selected_words": len(selected),
        "minimum_pairwise_hamming_distance": minimum_distance,
        "universe_words": q**dimension,
        "minimum_closed_neighborhood_coverage": min(coverage_counts),
        "maximum_closed_neighborhood_coverage": max(coverage_counts),
        "coverage_histogram": coverage_histogram,
        "coordinate_slice_counts": coordinate_slice_counts,
        "canonical_selected_words_sha256": hashlib.sha256(canonical.encode("ascii")).hexdigest(),
        "certificate_file_sha256": hashlib.sha256(raw).hexdigest(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.certificate)
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SystemExit(f"verification failed: {exc}") from exc
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
