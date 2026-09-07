#!/usr/bin/env python3
"""Exhaustive definition-level audit of every strict edge set and colour row."""

from collections import Counter
import json
from pathlib import Path

from colour import unpack_row, valid_colouring
from model import direct_unit_edges, enumerate_placements, union_points, unit_graph
from verify import decode_rows


HERE = Path(__file__).resolve().parent


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    expected = json.loads((HERE / "EXPECTED.json").read_text())
    base, raw_count, placements = enumerate_placements()
    packed_rows = decode_rows(certificate["colour_rows"], len(placements))
    histogram = Counter()
    checked_pairs = 0
    for index, ((_source, _target, _reflected, moved), packed) in enumerate(
            zip(placements, packed_rows)):
        points, _moved_indices = union_points(base, moved)
        direct = direct_unit_edges(points)
        _same_points, origin_case = unit_graph(base, moved)
        if direct != origin_case:
            raise AssertionError(f"edge constructions differ at placement {index}")
        row = unpack_row(packed, len(points))
        if not valid_colouring(len(points), direct, row):
            raise AssertionError(f"direct graph rejects row {index}")
        histogram[(len(points), len(direct))] += 1
        checked_pairs += len(points) * (len(points) - 1) // 2

    rows = [
        {"vertices": vertices, "edges": edges, "placements": count}
        for (vertices, edges), count in sorted(histogram.items())
    ]
    if raw_count != expected["raw_labeled_specifications"]:
        raise AssertionError("raw count differs from pinned value")
    if len(placements) != expected["distinct_moved_point_sets"]:
        raise AssertionError("placement count differs from pinned value")
    if rows != expected["histogram"]:
        raise AssertionError("direct histogram differs from pinned value")
    print(json.dumps({
        "status": "direct audit passed",
        "placements": len(placements),
        "definition_level_point_pairs": checked_pairs,
        "edge_sets_matched": len(placements),
        "four_colour_rows_checked": len(placements),
        "histogram": rows,
        "floating_point_operations": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
