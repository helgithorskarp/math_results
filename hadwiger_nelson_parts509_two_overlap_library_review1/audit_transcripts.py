#!/usr/bin/env python3
"""Independently audit primary and reverse-matcher full census transcripts."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


EXPECTED_CENSUS_SHA256 = "b44b48122f698b539f96fe16f4aa2432dd4eb763bff2dcc050195bc337a77f22"
EXPECTED_RESIDUAL_SHA256 = "cca94363716ec704032c98bd16e065ba1b8dde27ad9ef5b631f143f1cd116d33"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines()]


def parse_histogram(value: object) -> dict[int, tuple[int, int]]:
    if not isinstance(value, list):
        raise ValueError("histogram is not a list")
    result: dict[int, tuple[int, int]] = {}
    for item in value:
        if (not isinstance(item, list) or len(item) != 3
                or any(type(x) is not int for x in item)):
            raise ValueError("malformed histogram cell")
        edge_count, total, coloured = item
        if edge_count < 0 or not 0 <= coloured <= total or edge_count in result:
            raise ValueError("invalid histogram cell")
        result[edge_count] = (total, coloured)
    if list(result) != sorted(result):
        raise ValueError("histogram is not sorted")
    return result


def audit(census_path: Path, residual_path: Path, seed_path: Path) -> None:
    if digest(census_path) != EXPECTED_CENSUS_SHA256:
        raise ValueError("unexpected primary census digest")
    if digest(residual_path) != EXPECTED_RESIDUAL_SHA256:
        raise ValueError("unexpected primary residual digest")

    data = records(census_path)
    if len(data) != 2842:
        raise ValueError("full census must contain header, 2840 rows, and completion")
    header, rows, final = data[0], data[1:-1], data[-1]
    if header != {"type": "header", "first": 0, "end": 2840, "orientations": 2840,
                  "left_colourings": 135, "small_colourings": 194,
                  "expanded_small_colourings": 4656}:
        raise ValueError("unexpected full-run header")

    total_fields = Counter()
    histogram_total = Counter()
    histogram_coloured = Counter()
    residual_by_cell = Counter()
    row_fields = {"type", "orientation", "reflected", "multi", "pairs", "two", "checks",
                  "coloured", "unresolved", "dense_checks", "histogram"}
    for index, row in enumerate(rows):
        if (set(row) != row_fields or row.get("type") != "orientation"
                or row.get("orientation") != index):
            raise ValueError("missing or unordered orientation row")
        if row.get("reflected") is not (index >= 1420):
            raise ValueError("incorrect orientation parity")
        histogram = parse_histogram(row.get("histogram"))
        if sum(n for n, _ in histogram.values()) != row.get("two"):
            raise ValueError("orientation placement count mismatch")
        if sum(c for _, c in histogram.values()) != row.get("coloured"):
            raise ValueError("orientation colouring count mismatch")
        if row.get("two") != row.get("coloured") + row.get("unresolved"):
            raise ValueError("orientation residual count mismatch")
        for field in ("multi", "pairs", "two", "checks", "coloured", "unresolved",
                      "dense_checks"):
            if type(row.get(field)) is not int or row[field] < 0:
                raise ValueError("invalid orientation counter")
            total_fields[field] += row[field]
        for edges, (total, coloured) in histogram.items():
            histogram_total[edges] += total
            histogram_coloured[edges] += coloured

    cases = records(residual_path)
    compact_seeds = [tuple(map(int, line.split())) for line in seed_path.read_text().splitlines()
                     if line and not line.startswith("#")]
    observed_seeds = []
    for case in cases:
        if set(case) != {"orientation", "denominator", "x", "y", "overlaps", "edges"}:
            raise ValueError("unexpected residual schema")
        overlaps = case["overlaps"]
        edges = case["edges"]
        if (not 0 <= case["orientation"] < 2840 or type(case["denominator"]) is not int
                or case["denominator"] <= 0
                or any(not isinstance(case[key], list) or len(case[key]) != 8
                       or any(type(x) is not int for x in case[key]) for key in ("x", "y"))
                or len(overlaps) != 2 or any(type(x) is not int or not 0 <= x < 374 * 136
                                             for x in overlaps)
                or overlaps[0] >= overlaps[1]
                or overlaps[0] // 136 == overlaps[1] // 136
                or overlaps[0] % 136 == overlaps[1] % 136
                or edges != sorted(set(edges))
                or any(type(edge) is not int or not 0 <= edge // 510 < 374
                       or not 374 <= edge % 510 < 510 for edge in edges)):
            raise ValueError("malformed residual")
        observed_seeds.append((case["orientation"], overlaps[0], overlaps[1]))
        residual_by_cell[case["orientation"], len(edges)] += 1
    if observed_seeds != compact_seeds or len(observed_seeds) != len(set(observed_seeds)):
        raise ValueError("compact residual seeds do not match the full transcript")

    for row in rows:
        histogram = parse_histogram(row["histogram"])
        for edges, (total, coloured) in histogram.items():
            if residual_by_cell[row["orientation"], edges] != total - coloured:
                raise ValueError("residuals do not reconcile with orientation histogram")

    expected_final = {
        "type": "complete", "first": 0, "end": 2840,
        "multi": 2992078, "pairs": 17658256, "two": 2373802,
        "checks": 75228956, "coloured": 2371030, "unresolved": 2772,
        "dense_checks": 21,
    }
    for key, value in expected_final.items():
        if final.get(key) != value:
            raise ValueError(f"unexpected final value for {key}")
    for key in ("multi", "pairs", "two", "checks", "coloured", "unresolved",
                "dense_checks"):
        if total_fields[key] != final[key]:
            raise ValueError(f"global row sum mismatch for {key}")
    final_histogram = parse_histogram(final.get("histogram"))
    if final_histogram != {
        edges: (histogram_total[edges], histogram_coloured[edges])
        for edges in sorted(histogram_total)
    }:
        raise ValueError("global histogram does not equal row totals")
    residual_edges = [edges for edges, (total, coloured) in final_histogram.items()
                      if total != coloured]
    if min(residual_edges) != 29 or max(final_histogram) != 131:
        raise ValueError("claimed edge thresholds do not follow from histogram")
    if sum(total for edges, (total, _) in final_histogram.items() if edges <= 28) != 2282030:
        raise ValueError("through-28 placement count mismatch")

    print("orientations=2840")
    print("exactly_two_overlap_placements=2373802")
    print("library_coloured_placements=2371030")
    print("residual_placements=2772")
    print("through_28_coloured_placements=2282030")
    print("minimum_residual_new_edges=29 maximum_new_edges=131")
    print("primary_transcripts_and_compact_seeds_reconcile=true")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("primary_census", type=Path)
    parser.add_argument("primary_residual", type=Path)
    parser.add_argument("reverse_census", type=Path)
    parser.add_argument("reverse_residual", type=Path)
    parser.add_argument("seed_file", type=Path)
    args = parser.parse_args()
    audit(args.primary_census, args.primary_residual, args.seed_file)
    if args.primary_census.read_bytes() != args.reverse_census.read_bytes():
        raise ValueError("reverse-matcher census differs from primary census")
    if args.primary_residual.read_bytes() != args.reverse_residual.read_bytes():
        raise ValueError("reverse-matcher residuals differ from primary residuals")
    print("reverse_matcher_full_transcripts_byte_identical=true")


if __name__ == "__main__":
    main()
