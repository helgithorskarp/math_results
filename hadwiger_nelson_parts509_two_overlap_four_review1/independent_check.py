#!/usr/bin/env python3
"""Clean-room transcript and colour-certificate audit for the four-edge stratum."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


TRANSCRIPT_SHA256 = "dfdff4b9fde77a9afb45de38b7c5564cd38906fda3f8e88cf393eaba38f015e5"
PROFILES = (
    "L1_S4", "L4_S1", "L2_S2", "L2_S3", "L2_S4", "L3_S2",
    "L3_S3", "L3_S4", "L4_S2", "L4_S3", "L4_S4",
)
EXPECTED_PROFILES = (6922, 18380, 0, 24, 10814, 60, 3916, 30802, 23510, 32130, 53676)
GLOBAL_COUNTS = {
    "exactly_two_overlap_placements": 2373802,
    "with_zero_genuinely_new_cross_edges": 179074,
    "with_exactly_one_genuinely_new_cross_edge": 189738,
    "with_exactly_two_genuinely_new_cross_edges": 194946,
    "with_exactly_three_genuinely_new_cross_edges": 180216,
    "with_exactly_four_genuinely_new_cross_edges": 180234,
    "with_at_least_five_genuinely_new_cross_edges": 1449594,
    "four_new_edges_absorbed_by_explicit_libraries": 180234,
    "four_new_edges_unresolved_by_explicit_libraries": 0,
}
PRIMES = (3, 5, 11)
SCALE = 96


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            result.update(block)
    return result.hexdigest()


def parse_transcript(path: Path) -> tuple[list[dict[str, int]], dict[str, int], set[str]]:
    if sha256(path) != TRANSCRIPT_SHA256:
        raise AssertionError("full transcript digest mismatch")
    lines = path.read_text(encoding="ascii").splitlines()
    if len(lines) != 2913:
        raise AssertionError(("transcript line count", len(lines)))
    rows = []
    scalars = {}
    flags = set()
    for line in lines:
        if line.startswith("orientation="):
            fields = dict(item.split("=", 1) for item in line.split(";"))
            if len(fields) != len(line.split(";")):
                raise AssertionError("duplicate row field")
            rows.append({key: int(value) for key, value in fields.items()})
        elif "=" in line:
            key, value = line.split("=", 1)
            if key in scalars or key in flags:
                raise AssertionError(f"duplicate global field: {key}")
            if value == "true":
                flags.add(key)
            else:
                scalars[key] = int(value)
        else:
            raise AssertionError(f"malformed line: {line}")
    return rows, scalars, flags


def audit_transcript(path: Path) -> None:
    rows, scalars, flags = parse_transcript(path)
    if len(rows) != 2840 or [row["orientation"] for row in rows] != list(range(2840)):
        raise AssertionError("orientation sequence")
    if any(row["reflected"] != (index >= 1420) for index, row in enumerate(rows)):
        raise AssertionError("reflection partition")
    if flags != {"exact_two_overlap_cross_census"}:
        raise AssertionError(flags)
    for key, expected in GLOBAL_COUNTS.items():
        if scalars.get(key) != expected:
            raise AssertionError((key, scalars.get(key), expected))

    category_fields = (
        "genuine_zero", "genuine_one", "genuine_two", "genuine_three",
        "genuine_four", "genuine_five_plus",
    )
    for row in rows:
        if sum(row[key] for key in category_fields) != row["exactly_two"]:
            raise AssertionError("row categories do not partition")
        if sum(row[f"four_{profile}"] for profile in PROFILES) != row["genuine_four"]:
            raise AssertionError("row profiles do not partition")
        if row["four_library_absorbed"] != row["genuine_four"]:
            raise AssertionError("row has unresolved four-edge placement")
        if any(
            row[f"absorbed_four_{profile}"] != row[f"four_{profile}"]
            for profile in PROFILES
        ):
            raise AssertionError("row profile has unresolved placement")
        if row["interval_candidates"] != row["exact_checks"]:
            raise AssertionError("row exact-check accounting")

    row_to_global = {
        "exactly_two": "exactly_two_overlap_placements",
        "genuine_zero": "with_zero_genuinely_new_cross_edges",
        "genuine_one": "with_exactly_one_genuinely_new_cross_edge",
        "genuine_two": "with_exactly_two_genuinely_new_cross_edges",
        "genuine_three": "with_exactly_three_genuinely_new_cross_edges",
        "genuine_four": "with_exactly_four_genuinely_new_cross_edges",
        "genuine_five_plus": "with_at_least_five_genuinely_new_cross_edges",
        "four_library_absorbed": "four_new_edges_absorbed_by_explicit_libraries",
        **{f"four_{profile}": f"four_new_edges_{profile}" for profile in PROFILES},
        **{
            f"absorbed_four_{profile}": f"absorbed_four_new_edges_{profile}"
            for profile in PROFILES
        },
    }
    for local, global_name in row_to_global.items():
        if sum(row[local] for row in rows) != scalars[global_name]:
            raise AssertionError((local, global_name))

    rotations, reflections = rows[:1420], rows[1420:]
    for field in row_to_global:
        if sum(row[field] for row in rotations) != sum(row[field] for row in reflections):
            raise AssertionError(f"rotation/reflection mismatch: {field}")

    observed_profiles = tuple(scalars[f"four_new_edges_{profile}"] for profile in PROFILES)
    if observed_profiles != EXPECTED_PROFILES or sum(observed_profiles) != 180234:
        raise AssertionError(observed_profiles)
    possible_profiles = {
        (len({edge // 4 for edge in edges}), len({edge % 4 for edge in edges}))
        for edges in itertools.combinations(range(16), 4)
    }
    named_profiles = {
        tuple(map(int, profile[1:].split("_S"))) for profile in PROFILES
    }
    if possible_profiles != named_profiles:
        raise AssertionError("profile list is not exhaustive")
    closed = sum(GLOBAL_COUNTS[key] for key in (
        "with_zero_genuinely_new_cross_edges",
        "with_exactly_one_genuinely_new_cross_edge",
        "with_exactly_two_genuinely_new_cross_edges",
        "with_exactly_three_genuinely_new_cross_edges",
        "with_exactly_four_genuinely_new_cross_edges",
    ))
    if closed != 924208 or GLOBAL_COUNTS["exactly_two_overlap_placements"] - closed != 1449594:
        raise AssertionError("closed/residual arithmetic")

    print(f"transcript_sha256={TRANSCRIPT_SHA256}")
    print("transcript_lines=2913")
    print("orientations=2840,rotations=1420,reflections=1420")
    print("exactly_two_overlap_placements=2373802")
    print("exactly_four_new_edges=180234")
    print("four_edge_profiles=" + ",".join(map(str, observed_profiles)))
    print("four_edge_library_absorbed=180234")
    print("rotation_reflection_profile_sums_match=true")
    print("closed_through_four=924208,residual_at_least_five=1449594")


def multiply(first: tuple[int, ...], second: tuple[int, ...]) -> tuple[int, ...]:
    result = [0] * 8
    for left_index, left_value in enumerate(first):
        for right_index, right_value in enumerate(second):
            coefficient = left_value * right_value
            for bit, prime in enumerate(PRIMES):
                if (left_index & right_index) & (1 << bit):
                    coefficient *= prime
            result[left_index ^ right_index] += coefficient
    return tuple(result)


def squared_distance(first: tuple[tuple[int, ...], tuple[int, ...]], second) -> tuple[int, ...]:
    differences = tuple(
        tuple(a - b for a, b in zip(first[axis], second[axis], strict=True))
        for axis in range(2)
    )
    return tuple(
        x + y
        for x, y in zip(multiply(differences[0], differences[0]),
                        multiply(differences[1], differences[1]), strict=True)
    )


def read_points(path: Path) -> list[tuple[tuple[int, ...], tuple[int, ...]]]:
    points = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        values = tuple(map(int, line.split()))
        if len(values) != 16:
            raise AssertionError("bad point")
        points.append((values[:8], values[8:]))
    if len(points) != 509 or len(set(points)) != 509:
        raise AssertionError("point census")
    return points


def edge_set(points) -> set[tuple[int, int]]:
    unit = (SCALE * SCALE,) + (0,) * 7
    return {
        (first, second)
        for second in range(1, len(points))
        for first in range(second)
        if squared_distance(points[first], points[second]) == unit
    }


def audit_libraries(points_path: Path, library_path: Path) -> None:
    points = read_points(points_path)
    left_points = points[:374]
    small_points = [points[0], *points[374:]]
    left_edges = edge_set(left_points)
    small_edges = edge_set(small_points)
    if (len(left_edges), len(small_edges)) != (1860, 564):
        raise AssertionError((len(left_edges), len(small_edges)))

    left_colourings = []
    small_colourings = []
    for line in library_path.read_text(encoding="ascii").splitlines():
        if line.startswith("L:"):
            left_colourings.append(tuple(map(int, line[2:])))
        elif line.startswith("S:"):
            small_colourings.append(tuple(map(int, line[2:])))
        else:
            raise AssertionError("bad library prefix")
    if (len(left_colourings), len(small_colourings)) != (135, 194):
        raise AssertionError("library census")

    def proper(colourings, order, edges) -> bool:
        return all(
            len(colouring) == order
            and set(colouring) <= {0, 1, 2, 3}
            and all(colouring[first] != colouring[second] for first, second in edges)
            for colouring in colourings
        )

    if not proper(left_colourings, 374, left_edges):
        raise AssertionError("improper L witness")
    if not proper(small_colourings, 136, small_edges):
        raise AssertionError("improper S+ witness")

    print("exact_internal_edges=1860_L,564_Splus")
    print("proper_colour_libraries=135_L,194_Splus")
    print("gluing_constraints=2_equal,4_unequal")
    print("independent_checks=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript", type=Path)
    parser.add_argument("points", type=Path)
    parser.add_argument("libraries", type=Path)
    arguments = parser.parse_args()
    audit_transcript(arguments.transcript)
    audit_libraries(arguments.points, arguments.libraries)


if __name__ == "__main__":
    main()
