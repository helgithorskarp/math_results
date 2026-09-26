"""Independent token enumeration of mixed quotients and full AGL(2,5) audit."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent


def catalogue() -> list[str]:
    words: set[str] = set()
    for total in (8, 9):
        for tokens in combinations_with_replacement(range(16), total):
            interior = [0] * 16
            for token in tokens:
                interior[token] += 1
            if max(interior) > 4:
                continue
            row_sums = [sum(interior[4 * row + column] for column in range(4)) for row in range(4)]
            column_sums = [sum(interior[4 * row + column] for row in range(4)) for column in range(4)]
            if any(value > 3 for value in row_sums):
                continue
            if not 1 <= column_sums[0] <= 4 or any(value > 3 for value in column_sums[1:]):
                continue

            deficit = [0] * 25
            deficit[0] = total - 5
            for row in range(4):
                deficit[5 * (row + 1)] = 4 - row_sums[row]
            margins = (5, 4, 4, 4)
            for column in range(4):
                deficit[column + 1] = margins[column] - column_sums[column]
            for row in range(4):
                for column in range(4):
                    deficit[5 * (row + 1) + column + 1] = interior[4 * row + column]

            admissible = True
            for slope in range(1, 5):
                for offset in range(5):
                    if sum(deficit[5 * x + (slope * x + offset) % 5] for x in range(5)) < 4:
                        admissible = False
                        break
                if not admissible:
                    break
            if admissible:
                words.add("".join(str(4 - value) for value in deficit))
    return sorted(words)


def profile_counts(word: str) -> Counter[int]:
    weights = tuple(map(int, word))
    counts: Counter[int] = Counter()
    for slope in range(5):
        for offset in range(5):
            counts[sum(weights[5 * x + (slope * x + offset) % 5] for x in range(5))] += 1
    for x in range(5):
        counts[sum(weights[5 * x + y] for y in range(5))] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=True)

    words = catalogue()
    if len(words) != 5428:
        raise RuntimeError(f"expected 5428 mixed quotients, found {len(words)}")
    catalogue_path = out / "catalogue.txt"
    catalogue_path.write_text("\n".join(words) + "\n")
    digest = hashlib.sha256(catalogue_path.read_bytes()).hexdigest()
    if digest != "765937a860439729986f457b6cad703d362aa87a71ae6b3cb30631fbe5038792":
        raise RuntimeError("independent catalogue hash mismatch")
    discarded = sum(profile_counts(word)[8] >= 2 for word in words)
    if discarded != 144:
        raise RuntimeError(f"expected 144 inherited exclusions, found {discarded}")

    executable = out / "full_affine_check"
    subprocess.run(
        ["g++", "-O3", "-std=c++20", "-Wall", "-Wextra", "-Wconversion",
         str(HERE / "full_affine_check.cpp"), "-o", str(executable)],
        check=True,
    )
    orbit_result = json.loads(
        subprocess.check_output(
            [str(executable), str(catalogue_path), str(HERE.parent / "no_eight_planes72" / "orbits.json")],
            text=True,
        )
    )
    expected = {
        "affine_maps": 12000,
        "representatives": 1252,
        "normalized_images": 5284,
        "overlaps": 0,
        "published_orbit_sizes_match": True,
    }
    if orbit_result != expected:
        raise RuntimeError(f"full affine audit disagrees: {orbit_result}")
    result = {
        "status": "INDEPENDENT_CATALOGUE_AND_FULL_AFFINE_AUDIT_VERIFIED",
        "labeled_mixed_quotients": len(words),
        "inherited_two_eight_exclusions": discarded,
        "remaining_mixed_quotients": len(words) - discarded,
        "catalogue_sha256": digest,
        **orbit_result,
    }
    (out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
