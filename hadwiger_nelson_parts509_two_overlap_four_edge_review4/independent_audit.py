#!/usr/bin/env python3
"""Independent consistency audit for the Parts two-overlap four-edge census.

This standard-library checker does not import submitted modules.  It rebuilds
the strict internal unit-distance graphs from integer-basis coordinates,
checks every stored colouring, and audits the complete optional census
transcript row by row.  It does not independently re-enumerate placements.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POINTS = ROOT / "hadwiger_nelson_parts509_completion_census_degree9" / "points.tsv"
TARGET = ROOT / "hadwiger_nelson_parts509_two_overlap_cross_census"
LIBRARY = TARGET / "colour_libraries.txt"
SUMMARY = TARGET / "expected_four_summary.txt"

EXPECTED_HASHES = {
    POINTS: "f69ce1adef2f47c666f57c5e2096cb766fbc16654d75e3b24fbf0f5913d5be50",
    TARGET / "census.cpp": "ee2b9690428103d736f079907deaae2a68b60f006fc1756e37eb840ce4bdb772",
    LIBRARY: "91f5f39f1533e5780edfa30130f36bee3f90428bd7d442e788e8311d029b4169",
    SUMMARY: "e4c3f2d098ae43e69dfab345a6d9025e3061a5110d1d470e80ccb64160cd0814",
}
EXPECTED_TRANSCRIPT_HASH = "dfdff4b9fde77a9afb45de38b7c5564cd38906fda3f8e88cf393eaba38f015e5"
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
RAD_INDEX = {value: index for index, value in enumerate(RADICANDS)}
ZERO = (Fraction(0),) * 8
ONE = (Fraction(1),) + (Fraction(0),) * 7

FOUR_PROFILES = (
    "L1_S4", "L4_S1", "L2_S2", "L2_S3", "L2_S4", "L3_S2",
    "L3_S3", "L3_S4", "L4_S2", "L4_S3", "L4_S4",
)
THREE_PROFILES = ("L1_S3", "L3_S1", "L2_S2", "L2_S3", "L3_S2", "L3_S3")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def add(left, right):
    return tuple(a + b for a, b in zip(left, right, strict=True))


def neg(value):
    return tuple(-coefficient for coefficient in value)


def multiply(left, right):
    result = [Fraction(0)] * 8
    for i, a in enumerate(left):
        if not a:
            continue
        for j, b in enumerate(right):
            if not b:
                continue
            common = math.gcd(RADICANDS[i], RADICANDS[j])
            radical = RADICANDS[i] * RADICANDS[j] // (common * common)
            result[RAD_INDEX[radical]] += a * b * common
    return tuple(result)


def subtract(left, right):
    return add(left, neg(right))


def squared_distance(left, right):
    dx = subtract(left[0], right[0])
    dy = subtract(left[1], right[1])
    return add(multiply(dx, dx), multiply(dy, dy))


def read_points():
    rows = []
    for line in POINTS.read_text(encoding="ascii").splitlines():
        if line.startswith("#"):
            continue
        values = list(map(int, line.split()))
        if len(values) != 16:
            raise ValueError("bad point row")
        x = tuple(Fraction(value, 96) for value in values[:8])
        y = tuple(Fraction(value, 96) for value in values[8:])
        rows.append((x, y))
    if len(rows) != 509 or rows[0] != (ZERO, ZERO):
        raise ValueError("bad point inventory")
    return rows


def build_edges(points):
    return [
        (u, v)
        for u, v in itertools.combinations(range(len(points)), 2)
        if squared_distance(points[u], points[v]) == ONE
    ]


def read_colourings():
    left, small = [], []
    for line in LIBRARY.read_text(encoding="ascii").splitlines():
        prefix, encoded = line.split(":", 1)
        colours = tuple(map(int, encoded))
        if prefix == "L" and len(colours) == 374:
            left.append(colours)
        elif prefix == "S" and len(colours) == 136:
            small.append(colours)
        else:
            raise ValueError("bad colour-library row")
    if len(left) != 135 or len(small) != 194:
        raise ValueError("bad colour-library inventory")
    return left, small


def parse_kv_line(line):
    return dict(item.split("=", 1) for item in line.split(";"))


def read_summary():
    values, flags = {}, set()
    for line in SUMMARY.read_text(encoding="ascii").splitlines():
        key, raw = line.split("=", 1)
        if raw == "true":
            flags.add(key)
        else:
            values[key] = int(raw)
    return values, flags


def audit_transcript(path: Path):
    if sha256(path) != EXPECTED_TRANSCRIPT_HASH:
        raise ValueError("full transcript hash mismatch")
    rows, scalars, flags = [], {}, set()
    for line in path.read_text(encoding="ascii").splitlines():
        if line.startswith("orientation="):
            rows.append({key: int(value) for key, value in parse_kv_line(line).items()})
        elif ";" not in line:
            key, value = line.split("=", 1)
            if value == "true":
                flags.add(key)
            elif value.isdigit():
                scalars[key] = int(value)

    expected, expected_flags = read_summary()
    for key, value in expected.items():
        if scalars.get(key) != value:
            raise ValueError(f"global scalar mismatch: {key}")
    if flags != expected_flags:
        raise ValueError("global flag mismatch")
    if len(rows) != 2840 or [row["orientation"] for row in rows] != list(range(2840)):
        raise ValueError("orientation rows are incomplete")
    if any(row["reflected"] != (index >= 1420) for index, row in enumerate(rows)):
        raise ValueError("rotation/reflection row boundary is wrong")

    category_fields = (
        "genuine_zero", "genuine_one", "genuine_two", "genuine_three",
        "genuine_four", "genuine_five_plus",
    )
    if any(sum(row[field] for field in category_fields) != row["exactly_two"] for row in rows):
        raise ValueError("genuine-edge categories do not partition a row")
    if any(row["with_cross"] != row["exactly_two"] for row in rows):
        raise ValueError("a two-overlap placement lacks a cross unit-label pair")
    if any(
        row["two_share_left"] + row["two_share_small"] + row["two_disjoint"]
        != row["genuine_two"] for row in rows
    ):
        raise ValueError("two-edge topologies do not partition a row")
    if any(
        row["disjoint_adj00"] + row["disjoint_adj01"]
        + row["disjoint_adj10"] + row["disjoint_adj11"]
        != row["two_disjoint"] for row in rows
    ):
        raise ValueError("disjoint two-edge subtypes do not partition a row")
    if any(
        sum(row[f"three_{profile}"] for profile in THREE_PROFILES) != row["genuine_three"]
        for row in rows
    ):
        raise ValueError("three-edge profiles do not partition a row")
    if any(
        sum(row[f"four_{profile}"] for profile in FOUR_PROFILES) != row["genuine_four"]
        for row in rows
    ):
        raise ValueError("four-edge profiles do not partition a row")
    if any(
        row["two_library_absorbed"] != row["genuine_two"]
        or row["absorbed_share_left"] != row["two_share_left"]
        or row["absorbed_share_small"] != row["two_share_small"]
        or row["absorbed_disjoint"] != row["two_disjoint"]
        or row["three_library_absorbed"] != row["genuine_three"]
        or row["four_library_absorbed"] != row["genuine_four"]
        for row in rows
    ):
        raise ValueError("an enumerated row has an unabsorbed at-most-four-edge placement")
    for row in rows:
        if any(row[f"absorbed_three_{p}"] != row[f"three_{p}"] for p in THREE_PROFILES):
            raise ValueError("three-edge absorbed profile mismatch")
        if any(row[f"absorbed_four_{p}"] != row[f"four_{p}"] for p in FOUR_PROFILES):
            raise ValueError("four-edge absorbed profile mismatch")
        if row["interval_candidates"] != row["exact_checks"]:
            raise ValueError("interval/exact-check accounting mismatch")

    mappings = {
        "exactly_two": "exactly_two_overlap_placements",
        "with_cross": "with_any_cross_unit_label_pair",
        "with_genuine": "with_genuinely_new_cross_edge",
        "genuine_zero": "with_zero_genuinely_new_cross_edges",
        "genuine_one": "with_exactly_one_genuinely_new_cross_edge",
        "genuine_two": "with_exactly_two_genuinely_new_cross_edges",
        "genuine_three": "with_exactly_three_genuinely_new_cross_edges",
        "genuine_four": "with_exactly_four_genuinely_new_cross_edges",
        "genuine_five_plus": "with_at_least_five_genuinely_new_cross_edges",
        "two_share_left": "two_new_edges_share_left_endpoint",
        "two_share_small": "two_new_edges_share_small_endpoint",
        "two_disjoint": "two_new_edges_vertex_disjoint",
        "disjoint_adj00": "disjoint_two_edges_left_nonedge_small_nonedge",
        "disjoint_adj01": "disjoint_two_edges_left_nonedge_small_edge",
        "disjoint_adj10": "disjoint_two_edges_left_edge_small_nonedge",
        "disjoint_adj11": "disjoint_two_edges_left_edge_small_edge",
        "two_library_absorbed": "two_new_edges_absorbed_by_explicit_libraries",
        "absorbed_share_left": "absorbed_two_edges_share_left_endpoint",
        "absorbed_share_small": "absorbed_two_edges_share_small_endpoint",
        "absorbed_disjoint": "absorbed_two_edges_vertex_disjoint",
        "three_library_absorbed": "three_new_edges_absorbed_by_explicit_libraries",
        "four_library_absorbed": "four_new_edges_absorbed_by_explicit_libraries",
        "interval_candidates": "interval_candidates",
        "exact_checks": "exact_distance_checks",
    }
    mappings.update({f"three_{p}": f"three_new_edges_{p}" for p in THREE_PROFILES})
    mappings.update({f"absorbed_three_{p}": f"absorbed_three_new_edges_{p}" for p in THREE_PROFILES})
    mappings.update({f"four_{p}": f"four_new_edges_{p}" for p in FOUR_PROFILES})
    mappings.update({f"absorbed_four_{p}": f"absorbed_four_new_edges_{p}" for p in FOUR_PROFILES})
    for local, global_name in mappings.items():
        if sum(row[local] for row in rows) != scalars[global_name]:
            raise ValueError(f"row/global sum mismatch: {local}")

    symmetry_fields = tuple(key for key in mappings if key not in {"interval_candidates", "exact_checks"})
    rotations, reflections = rows[:1420], rows[1420:]
    if any(
        sum(row[field] for row in rotations) != sum(row[field] for row in reflections)
        for field in symmetry_fields
    ):
        raise ValueError("rotation/reflection aggregate mismatch")
    return {
        "orientation_rows": len(rows),
        "transcript_sha256": EXPECTED_TRANSCRIPT_HASH,
        "exact_distance_checks": scalars["exact_distance_checks"],
        "exactly_four": scalars["with_exactly_four_genuinely_new_cross_edges"],
        "absorbed_four": scalars["four_new_edges_absorbed_by_explicit_libraries"],
    }


def main():
    for path, expected in EXPECTED_HASHES.items():
        if sha256(path) != expected:
            raise ValueError(f"source hash mismatch: {path}")

    points = read_points()
    left_points = points[:374]
    small_points = [points[0], *points[374:]]
    left_edges = build_edges(left_points)
    small_edges = build_edges(small_points)
    if len(left_edges) != 1860 or len(small_edges) != 564:
        raise ValueError("strict internal edge census mismatch")

    left_colours, small_colours = read_colourings()
    left_checks = sum(len(left_edges) for _ in left_colours)
    small_checks = sum(len(small_edges) for _ in small_colours)
    if any(c[u] == c[v] for c in left_colours for u, v in left_edges):
        raise ValueError("improper L colouring")
    if any(c[u] == c[v] for c in small_colours for u, v in small_edges):
        raise ValueError("improper S+ colouring")

    possible_profiles = {
        (len({edge // 4 for edge in subset}), len({edge % 4 for edge in subset}))
        for subset in itertools.combinations(range(16), 4)
    }
    named_profiles = {tuple(map(int, name[1:].split("_S"))) for name in FOUR_PROFILES}
    if possible_profiles != named_profiles:
        raise ValueError("four-edge endpoint-profile list is not exhaustive")

    result = {
        "all_checks": True,
        "left_edges": len(left_edges),
        "small_edges": len(small_edges),
        "left_colourings": len(left_colours),
        "small_colourings": len(small_colours),
        "colouring_edge_checks": left_checks + small_checks,
        "four_edge_profiles": len(possible_profiles),
    }
    if len(sys.argv) == 2:
        result.update(audit_transcript(Path(sys.argv[1])))
    elif len(sys.argv) != 1:
        raise SystemExit(f"usage: {Path(sys.argv[0]).name} [full-transcript]")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
