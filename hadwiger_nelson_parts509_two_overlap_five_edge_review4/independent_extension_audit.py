#!/usr/bin/env python3
"""Independent audit of the five-edge extension of the Parts census.

This checker imports no submitted module.  It derives colour-partition
compatibility via injective matching and checks every row of an optional full
five-edge transcript.  The inherited geometry/library base is reviewed in
the sibling through-four review.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import sys
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_parts509_two_overlap_cross_census"

EXPECTED_HASHES = {
    TARGET / "census.cpp": "d9992d421d20fcb2246692353ab7b7aa3b7c0357b2779e40d0126a8ce03d1ca3",
    TARGET / "verify.py": "1d595cf8215250c69c2336b43afef476575a8c40e161d08535dc7097ab5170dc",
    TARGET / "expected_five_summary.txt": "bee53871486313d1245d17dd2e9fc282ef00dbc304ccfa4cd731cdcd49ad65de",
    TARGET / "colour_libraries.txt": "91f5f39f1533e5780edfa30130f36bee3f90428bd7d442e788e8311d029b4169",
}
EXPECTED_TRANSCRIPT_SHA256 = "bcfb26d2c2dcf7a03c956d6e57186d519c9cd200267cee43cbfe62168b35ddaa"
EXPECTED_CATEGORIES = (179074, 189738, 194946, 180216, 180234, 173230, 1276364)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_partition(pattern):
    rename, result = {}, []
    for colour in pattern:
        if colour not in rename:
            rename[colour] = len(rename)
        result.append(rename[colour])
    return tuple(result)


def restricted_growth_partitions(length=7, maximum_blocks=4):
    result = []

    def extend(prefix, largest):
        if len(prefix) == length:
            result.append(tuple(prefix))
            return
        for value in range(min(largest + 1, maximum_blocks - 1) + 1):
            prefix.append(value)
            extend(prefix, max(largest, value))
            prefix.pop()

    extend([0], 0)
    return result


def compatible_by_matching(small, left):
    """Existence of a colour bijection: two equalities, five inequalities."""
    fixed, used_targets = {}, set()
    for position in (0, 1):
        source, target = small[position], left[position]
        if source in fixed and fixed[source] != target:
            return False
        if source not in fixed and target in used_targets:
            return False
        fixed[source] = target
        used_targets.add(target)

    forbidden = {source: set() for source in set(small)}
    for position in range(2, 7):
        forbidden[small[position]].add(left[position])
    if any(target in forbidden[source] for source, target in fixed.items()):
        return False

    remaining = sorted(set(small) - set(fixed))

    def match(index, occupied):
        if index == len(remaining):
            return True
        source = remaining[index]
        return any(
            target not in occupied
            and target not in forbidden[source]
            and match(index + 1, occupied | {target})
            for target in range(4)
        )

    return match(0, used_targets)


def audit_partitions():
    partitions = restricted_growth_partitions()
    if len(partitions) != 715 or len(set(partitions)) != 715:
        raise ValueError("restricted-growth partition count mismatch")
    block_histogram = Counter(max(row) + 1 for row in partitions)
    if block_histogram != Counter({1: 1, 2: 63, 3: 301, 4: 350}):
        raise ValueError("Stirling partition histogram mismatch")

    raw_histogram = Counter(
        canonical_partition(row)
        for row in itertools.product(range(4), repeat=7)
    )
    if set(raw_histogram) != set(partitions) or sum(raw_histogram.values()) != 4**7:
        raise ValueError("raw patterns do not quotient to the partition inventory")
    falling_factorial = {1: 4, 2: 12, 3: 24, 4: 24}
    if any(raw_histogram[row] != falling_factorial[max(row) + 1] for row in partitions):
        raise ValueError("colour-relabeling orbit size mismatch")

    compatible_pairs = sum(
        compatible_by_matching(small, left)
        for small in partitions for left in partitions
    )
    if compatible_pairs != 124925:
        raise ValueError("partition compatibility count mismatch")
    return len(partitions), compatible_pairs


def parse_summary():
    scalars, flags = {}, set()
    for line in (TARGET / "expected_five_summary.txt").read_text(encoding="ascii").splitlines():
        key, value = line.split("=", 1)
        if value == "true":
            flags.add(key)
        else:
            scalars[key] = int(value)
    if flags != {"exact_two_overlap_cross_census"}:
        raise ValueError("bad compact-summary trailer")
    expected = {
        "exactly_two_overlap_placements": 2373802,
        "with_exactly_five_genuinely_new_cross_edges": 173230,
        "with_at_least_six_genuinely_new_cross_edges": 1276364,
        "five_new_edges_absorbed_by_explicit_libraries": 173230,
        "five_new_edges_unresolved_by_explicit_libraries": 0,
        "interval_candidates": 55803809,
        "exact_distance_checks": 55803809,
    }
    if any(scalars.get(key) != value for key, value in expected.items()):
        raise ValueError("bad compact five-edge summary")
    category_names = (
        "with_zero_genuinely_new_cross_edges",
        "with_exactly_one_genuinely_new_cross_edge",
        "with_exactly_two_genuinely_new_cross_edges",
        "with_exactly_three_genuinely_new_cross_edges",
        "with_exactly_four_genuinely_new_cross_edges",
        "with_exactly_five_genuinely_new_cross_edges",
        "with_at_least_six_genuinely_new_cross_edges",
    )
    if tuple(scalars[name] for name in category_names) != EXPECTED_CATEGORIES:
        raise ValueError("compact category vector mismatch")
    if sum(EXPECTED_CATEGORIES) != scalars["exactly_two_overlap_placements"]:
        raise ValueError("compact categories do not partition placements")
    return scalars


def audit_transcript(path, summary):
    if sha256(path) != EXPECTED_TRANSCRIPT_SHA256:
        raise ValueError("five-edge transcript hash mismatch")
    rows, scalars, flags = [], {}, set()
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("orientation="):
            fields = dict(item.split("=", 1) for item in line.split(";"))
            rows.append({key: int(value) for key, value in fields.items()})
        elif ";" not in line:
            key, value = line.split("=", 1)
            if value == "true":
                flags.add(key)
            elif value.isdigit():
                scalars[key] = int(value)
    if len(rows) != 2840 or [row["orientation"] for row in rows] != list(range(2840)):
        raise ValueError("incomplete orientation rows")
    if any(row["reflected"] != (index >= 1420) for index, row in enumerate(rows)):
        raise ValueError("bad rotation/reflection boundary")
    if flags != {"exact_two_overlap_cross_census"}:
        raise ValueError("bad transcript trailer")
    if scalars.get("canonical_seven_label_colour_partitions") != 715:
        raise ValueError("transcript partition count mismatch")
    if scalars.get("compatible_seven_label_partition_pairs") != 124925:
        raise ValueError("transcript compatibility count mismatch")
    for key, value in summary.items():
        if scalars.get(key) != value:
            raise ValueError(f"transcript global mismatch: {key}")

    categories = (
        "genuine_zero", "genuine_one", "genuine_two", "genuine_three",
        "genuine_four", "genuine_five", "genuine_six_plus",
    )
    if any(sum(row[key] for key in categories) != row["exactly_two"] for row in rows):
        raise ValueError("row categories do not partition placements")
    if any(row["with_cross"] != row["exactly_two"] for row in rows):
        raise ValueError("row has two-overlap placement without a cross pair")
    if any(row["five_library_absorbed"] != row["genuine_five"] for row in rows):
        raise ValueError("row has an unabsorbed five-edge placement")
    if any(row["interval_candidates"] != row["exact_checks"] for row in rows):
        raise ValueError("row exact-check accounting mismatch")

    mapping = {
        "exactly_two": "exactly_two_overlap_placements",
        "genuine_zero": "with_zero_genuinely_new_cross_edges",
        "genuine_one": "with_exactly_one_genuinely_new_cross_edge",
        "genuine_two": "with_exactly_two_genuinely_new_cross_edges",
        "genuine_three": "with_exactly_three_genuinely_new_cross_edges",
        "genuine_four": "with_exactly_four_genuinely_new_cross_edges",
        "genuine_five": "with_exactly_five_genuinely_new_cross_edges",
        "genuine_six_plus": "with_at_least_six_genuinely_new_cross_edges",
        "five_library_absorbed": "five_new_edges_absorbed_by_explicit_libraries",
        "interval_candidates": "interval_candidates",
        "exact_checks": "exact_distance_checks",
    }
    for local, global_name in mapping.items():
        if sum(row[local] for row in rows) != scalars[global_name]:
            raise ValueError(f"row/global sum mismatch: {local}")
    rotations, reflections = rows[:1420], rows[1420:]
    for key in mapping:
        if key in {"interval_candidates", "exact_checks"}:
            continue
        if sum(row[key] for row in rotations) != sum(row[key] for row in reflections):
            raise ValueError(f"rotation/reflection mismatch: {key}")
    if sum(row["genuine_five"] for row in rotations) != 86615:
        raise ValueError("five-edge half-total mismatch")
    if sum(row["genuine_six_plus"] for row in rotations) != 638182:
        raise ValueError("six-plus half-total mismatch")
    return len(rows), scalars["exact_distance_checks"]


def main():
    for path, expected in EXPECTED_HASHES.items():
        if sha256(path) != expected:
            raise ValueError(f"source hash mismatch: {path}")
    partitions, compatible_pairs = audit_partitions()
    summary = parse_summary()
    result = {
        "all_checks": True,
        "canonical_partitions": partitions,
        "compatible_partition_pairs": compatible_pairs,
        "exactly_five": summary["with_exactly_five_genuinely_new_cross_edges"],
        "absorbed_five": summary["five_new_edges_absorbed_by_explicit_libraries"],
    }
    if len(sys.argv) == 2:
        rows, checks = audit_transcript(Path(sys.argv[1]), summary)
        result.update({
            "orientation_rows": rows,
            "exact_distance_checks": checks,
            "transcript_sha256": EXPECTED_TRANSCRIPT_SHA256,
        })
    elif len(sys.argv) != 1:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [full-five-edge-transcript]")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
