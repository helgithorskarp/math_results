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
TARGET_DEGREES = (20,) * 22 + (21,) * 20


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
    for index, encoded in enumerate(lines):
        base = decode_short_graph6(encoded)
        if len(base) != 42:
            raise AssertionError("wrong known-catalog graph order")
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

    histogram_text = ",".join(
        f"{distance}:{count}" for distance, count in sorted(distance_histogram.items())
    )
    print("PASS known R(5,5;42) catalog records=328 orientations=656 "
          f"sha256={CATALOG_SHA256}")
    print("PASS singleton-deletion degree target 20^22,21^20 occurs 0 times")
    print("PASS degree-edit lower-bound histogram=" + histogram_text)
    print("PASS unique closest orientation=base index=93 "
          "degrees=" + format_degrees(expected_degrees))


if __name__ == "__main__":
    main()
