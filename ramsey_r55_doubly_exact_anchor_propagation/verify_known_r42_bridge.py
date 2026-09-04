#!/usr/bin/env python3
"""Audit the singleton normal form against the published known R(5,5;42) catalog."""

from __future__ import annotations

from collections import Counter
import hashlib
from pathlib import Path

from verify_anchor_propagation import complement_adjacency, decode_short_graph6


CATALOG_PATH = (
    Path(__file__).parent.parent
    / "ramsey_r55_catalog_edge_radius3_classification"
    / "r55_42some.g6"
)
CATALOG_SHA256 = "067902e853d87b49bcef0d1d4c0e3bbadd238ee18bc65341b079a3ca4780eccb"
RADIUS4_MAP_PATH = (
    Path(__file__).parent.parent
    / "ramsey_r55_catalog_edge_radius4_classification"
    / "EDGE_RADIUS4_MAP.tsv"
)
RADIUS4_MAP_SHA256 = "b7265672d34b876ceb1f371ab8b8a6cde7c970a0d0fbf4daed1d783a860a9b3b"
TARGET_DEGREES = (20,) * 22 + (21,) * 20
COMPLEMENT_TARGET_DEGREES = (20,) * 20 + (21,) * 22


def degree_multiset(adjacency) -> tuple[int, ...]:
    return tuple(sorted(sum(row) for row in adjacency))


def format_degrees(degrees: tuple[int, ...]) -> str:
    counts = Counter(degrees)
    return ",".join(f"{degree}^{counts[degree]}" for degree in sorted(counts))


def main() -> None:
    raw = CATALOG_PATH.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CATALOG_SHA256:
        raise AssertionError("known R(5,5;42) catalog digest changed")
    lines = raw.decode("ascii").splitlines()
    if len(lines) != 328 or len(lines) != len(set(lines)):
        raise AssertionError("wrong known-catalog record count")

    distance_histogram = Counter()
    closest_records = []
    target_count = 0
    catalog = []
    for index, encoded in enumerate(lines):
        base = decode_short_graph6(encoded)
        if len(base) != 42:
            raise AssertionError("wrong known-catalog graph order")
        catalog.append(base)
        for orientation, adjacency in (
            ("base", base),
            ("complement", complement_adjacency(base)),
        ):
            degrees = degree_multiset(adjacency)
            if degrees == TARGET_DEGREES:
                target_count += 1
            l1_distance = sum(
                abs(observed - target)
                for observed, target in zip(degrees, TARGET_DEGREES, strict=True)
            )
            if l1_distance % 2:
                raise AssertionError("degree-edit lower bound is not integral")
            edge_edit_lower_bound = l1_distance // 2
            distance_histogram[edge_edit_lower_bound] += 1
            closest_records.append(
                (edge_edit_lower_bound, index, orientation, degrees)
            )

    expected_histogram = {
        4: 1, 5: 17, 6: 72, 7: 146, 8: 187,
        9: 152, 10: 67, 11: 13, 12: 1,
    }
    if target_count != 0 or dict(sorted(distance_histogram.items())) != expected_histogram:
        raise AssertionError((target_count, distance_histogram))
    minimum = min(record[0] for record in closest_records)
    closest = [record for record in closest_records if record[0] == minimum]
    expected_degrees = (19,) * 4 + (20,) * 20 + (21,) * 16 + (22,) * 2
    if closest != [(4, 93, "base", expected_degrees)]:
        raise AssertionError(closest)

    # The companion radius-four artifact exhaustively lists every
    # Ramsey-preserving exactly-four flip from each stored parent.  A target
    # at distance four from a stored parent appears with TARGET_DEGREES; one
    # at distance four from a complemented parent appears, after color
    # complementation, with COMPLEMENT_TARGET_DEGREES.
    radius4_raw = RADIUS4_MAP_PATH.read_bytes()
    if hashlib.sha256(radius4_raw).hexdigest() != RADIUS4_MAP_SHA256:
        raise AssertionError("radius-four map digest changed")
    radius4_lines = radius4_raw.decode("ascii").splitlines()
    expected_header = (
        "parent\tedge_1\tedge_2\tedge_3\tedge_4\ttarget_kind\ttarget_index"
    )
    expected_summary = (
        "# SUMMARY transitions=8408 base_transitions=8284 "
        "complement_transitions=124 distinct_targets=380 "
        "base_targets=318 complement_targets=62"
    )
    if (
        len(radius4_lines) != 8410
        or len(radius4_lines) != len(set(radius4_lines))
        or radius4_lines[0] != expected_header
        or radius4_lines[-1] != expected_summary
    ):
        raise AssertionError("wrong radius-four map record count")
    radius4_target_hits = Counter()
    for line in radius4_lines[1:-1]:
        fields = line.split("\t")
        if len(fields) != 7:
            raise AssertionError(f"malformed radius-four row: {line!r}")
        parent = int(fields[0])
        if not 0 <= parent < len(catalog):
            raise AssertionError(f"bad radius-four parent: {parent}")
        adjacency = [list(row) for row in catalog[parent]]
        edges = []
        for field in fields[1:5]:
            pair = tuple(map(int, field.split(",")))
            if len(pair) != 2 or not 0 <= pair[0] < pair[1] < 42:
                raise AssertionError(f"bad radius-four edge: {field!r}")
            edges.append(pair)
        if len(set(edges)) != 4:
            raise AssertionError(f"repeated radius-four edge: {edges}")
        for first, second in edges:
            adjacency[first][second] = not adjacency[first][second]
            adjacency[second][first] = not adjacency[second][first]
        degrees = degree_multiset(adjacency)
        if degrees == TARGET_DEGREES:
            radius4_target_hits["target"] += 1
        if degrees == COMPLEMENT_TARGET_DEGREES:
            radius4_target_hits["complement-target"] += 1
    if radius4_target_hits:
        raise AssertionError(radius4_target_hits)

    histogram_text = ",".join(
        f"{distance}:{count}" for distance, count in sorted(distance_histogram.items())
    )
    print("PASS known R(5,5;42) catalog records=328 orientations=656 "
          f"sha256={CATALOG_SHA256}")
    print("PASS singleton-deletion degree target 20^22,21^20 occurs 0 times")
    print("PASS degree-edit lower-bound histogram=" + histogram_text)
    print("PASS unique closest orientation=base index=93 "
          "degrees=" + format_degrees(expected_degrees))
    print("PASS radius-four map records=8408 target/complement-target hits=0/0 "
          f"sha256={RADIUS4_MAP_SHA256}")
    print("PASS singleton-deletion catalog edge distance is at least 5")


if __name__ == "__main__":
    main()
