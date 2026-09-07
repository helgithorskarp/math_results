#!/usr/bin/env python3
"""Produce explicit four-colour rows for every exact family member."""

import argparse
from base64 import b85encode
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import zlib

from colour import ROW_BYTES, ROW_VERTICES, colour_graph, pack_row, valid_colouring
from model import (
    ROWS,
    descriptor_digest,
    enumerate_placements,
    point_set_digest,
    source_distance_edges,
    unit_graph,
)


HERE = Path(__file__).resolve().parent


def build_certificate():
    base, raw_count, placements = enumerate_placements()
    print(f"enumerated {raw_count} specifications and {len(placements)} point sets",
          flush=True)

    unit, long = source_distance_edges(base)
    two_distance_edges = tuple(sorted(unit + long))
    four_row, four_nodes = colour_graph(len(base), two_distance_edges, 4)
    if four_row is not None:
        raise AssertionError("source two-distance graph unexpectedly four-colourable")
    five_row, five_nodes = colour_graph(len(base), two_distance_edges, 5)
    if five_row is None or not valid_colouring(
            len(base), two_distance_edges, five_row, colours=5):
        raise AssertionError("failed to find a valid source five-colouring")

    histogram = Counter()
    packed = bytearray()
    total_nodes = 0
    maximum_nodes = 0
    for index, (_source, _target, _reflected, moved) in enumerate(placements):
        points, edges = unit_graph(base, moved)
        row, nodes = colour_graph(len(points), edges, 4)
        if row is None or not valid_colouring(len(points), edges, row):
            raise AssertionError(f"placement {index} has no checked four-colouring")
        packed.extend(pack_row(row))
        histogram[(len(points), len(edges))] += 1
        total_nodes += nodes
        maximum_nodes = max(maximum_nodes, nodes)
        if (index + 1) % 200 == 0:
            print(f"coloured {index + 1}/{len(placements)} point sets", flush=True)

    compressed = zlib.compress(bytes(packed), level=9)
    return {
        "schema": "hn-exoo-d2-halfscale-certificate-v1",
        "claim": (
            "Every strict unit-distance graph B union ((1/2)R(B)+t) in "
            "the two-coincidence family is four-colourable."
        ),
        "source": {
            "coordinate_rows": [list(row) for row in ROWS],
            "vertices": len(base),
            "unit_edges": len(unit),
            "length_two_edges": len(long),
            "four_colourable": False,
            "four_colour_search_nodes": four_nodes,
            "five_colouring": list(five_row),
            "five_colour_search_nodes": five_nodes,
        },
        "family": {
            "raw_labeled_specifications": raw_count,
            "distinct_moved_point_sets": len(placements),
            "descriptor_sha256": descriptor_digest(placements),
            "point_sets_sha256": point_set_digest(placements),
            "histogram": [
                {"vertices": vertices, "edges": edges, "placements": count}
                for (vertices, edges), count in sorted(histogram.items())
            ],
            "non_four_colourable": 0,
        },
        "colour_rows": {
            "packing": "four little-endian 2-bit colours per byte; zero-pad to 52",
            "compression": "zlib level 9, then RFC 1924 base85",
            "rows": len(placements),
            "vertices_per_packed_row": ROW_VERTICES,
            "bytes_per_row": ROW_BYTES,
            "raw_bytes": len(packed),
            "raw_sha256": sha256(packed).hexdigest(),
            "compressed_bytes": len(compressed),
            "data": b85encode(compressed).decode("ascii"),
        },
        "production": {
            "colour_search": "deterministic DSATUR backtracking",
            "family_colour_search_nodes_total": total_nodes,
            "family_colour_search_nodes_maximum": maximum_nodes,
            "floating_point_operations": 0,
        },
        "record_target_met": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", type=Path, default=HERE / "certificate.generated.json"
    )
    args = parser.parse_args()
    certificate = build_certificate()
    args.output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({
        "output": str(args.output),
        "family": certificate["family"],
        "raw_colour_sha256": certificate["colour_rows"]["raw_sha256"],
        "production": certificate["production"],
    }, indent=2))


if __name__ == "__main__":
    main()
