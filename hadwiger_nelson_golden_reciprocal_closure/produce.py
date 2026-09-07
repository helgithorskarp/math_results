#!/usr/bin/env python3
"""Produce the exact closure census and its explicit four-colouring."""

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from colour import colour_graph, valid_colouring
from model import (
    GOLDEN_NORM,
    SOURCE,
    UNIT_NORM,
    build_closures,
    canonical_key,
    digest_rows,
    source_edges,
)

HERE = Path(__file__).resolve().parent
SOURCE_CLIQUE = (0, 1, 2, 4, 5)


def copy_digest(groups):
    rows = []
    for scale_index, name in enumerate(("down", "up")):
        copies = groups[name][1]
        point_sets = sorted(
            tuple(sorted(canonical_key(point) for point in copy[-1]))
            for copy in copies
        )
        for index, point_set in enumerate(point_sets):
            rows.append((scale_index, index,
                         *(value for point in point_set for value in point)))
    return digest_rows(rows)


def build_certificate():
    unit = source_edges(UNIT_NORM)
    golden = source_edges(GOLDEN_NORM)
    source_graph = tuple(sorted(unit + golden))
    clique_edges = {
        tuple(sorted(pair))
        for index, left in enumerate(SOURCE_CLIQUE)
        for pair in ((left, right) for right in SOURCE_CLIQUE[index + 1:])
    }
    if not clique_edges.issubset(source_graph):
        raise AssertionError("the claimed source K5 is absent")
    five_colouring, five_nodes = colour_graph(len(SOURCE), source_graph, 5)
    if not valid_colouring(len(SOURCE), source_graph, five_colouring, colours=5):
        raise AssertionError("failed to construct the source five-colouring")

    groups, one_scale, keys, points, edges = build_closures()
    colour_row, colour_nodes = colour_graph(len(points), edges, 4)
    if not valid_colouring(len(points), edges, colour_row):
        raise AssertionError("failed to construct the closure four-colouring")

    source_keys = {canonical_key(point) for point in SOURCE}
    scales = []
    copy_key_sets = {}
    for name in ("down", "up"):
        raw, copies = groups[name]
        copy_key_sets[name] = {
            key for copy in copies for key in map(canonical_key, copy[-1])
        }
        overlap_histogram = Counter(
            sum(canonical_key(point) in source_keys for point in copy[-1])
            for copy in copies
        )
        one_keys, _one_points, one_edges = one_scale[name]
        scales.append({
            "name": name,
            "scale": "1/phi" if name == "down" else "phi",
            "raw_labeled_specifications": raw,
            "distinct_copy_point_sets": len(copies),
            "copy_base_overlap_histogram": [
                {"coincident_points": overlap, "copies": count}
                for overlap, count in sorted(overlap_histogram.items())
            ],
            "closure_vertices": len(one_keys),
            "closure_edges": len(one_edges),
            "closure_point_sha256": digest_rows(one_keys),
            "closure_edge_sha256": digest_rows(one_edges),
        })

    colour_word = "".join(str(value) for value in colour_row)
    return {
        "schema": "hn-golden-reciprocal-closure-v1",
        "claim": (
            "The strict unit-distance graph on the closure of all compatible "
            "phi and 1/phi copies of Parts's G16 is four-colourable."
        ),
        "source": {
            "vertices": len(SOURCE),
            "unit_edges": len(unit),
            "golden_edges": len(golden),
            "clique_labels_one_based": [value + 1 for value in SOURCE_CLIQUE],
            "chromatic_number": 5,
            "five_colouring": list(five_colouring),
            "five_colour_search_nodes": five_nodes,
        },
        "family": {
            "scales": scales,
            "distinct_copies_total": sum(len(row[1]) for row in groups.values()),
            "copy_point_sets_sha256": copy_digest(groups),
            "scale_closure_intersection_vertices": len(
                copy_key_sets["down"] & copy_key_sets["up"]
            ),
        },
        "full_closure": {
            "vertices": len(points),
            "edges": len(edges),
            "point_sha256": digest_rows(keys),
            "edge_sha256": digest_rows(edges),
            "four_colouring": colour_word,
            "four_colouring_sha256": sha256(colour_word.encode()).hexdigest(),
            "colour_search_nodes": colour_nodes,
        },
        "production": {
            "arithmetic": "exact Q(zeta_5), then integer edge checks",
            "colour_search": "deterministic DSATUR",
            "floating_point_operations": 0,
        },
        "record_target_met": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path,
                        default=HERE / "certificate.generated.json")
    args = parser.parse_args()
    certificate = build_certificate()
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "source": certificate["source"],
        "family": certificate["family"],
        "full_closure": {
            key: value for key, value in certificate["full_closure"].items()
            if key != "four_colouring"
        },
    }, indent=2))


if __name__ == "__main__":
    main()
