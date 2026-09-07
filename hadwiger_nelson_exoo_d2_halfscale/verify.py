#!/usr/bin/env python3
"""Standard-library verifier for the half-scale family certificate."""

import argparse
from base64 import b85decode
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import zlib

from colour import ROW_BYTES, colour_graph, unpack_row, valid_colouring
from model import (
    ROWS,
    descriptor_digest,
    enumerate_placements,
    point_set_digest,
    source_distance_edges,
    unit_graph,
)


HERE = Path(__file__).resolve().parent


def decode_rows(section, count):
    if section["rows"] != count or section["bytes_per_row"] != ROW_BYTES:
        raise AssertionError("colour-row dimensions disagree with enumeration")
    compressed = b85decode(section["data"].encode("ascii"))
    if len(compressed) != section["compressed_bytes"]:
        raise AssertionError("compressed byte count mismatch")
    raw = zlib.decompress(compressed)
    if len(raw) != section["raw_bytes"] or len(raw) != count * ROW_BYTES:
        raise AssertionError("raw colour byte count mismatch")
    if sha256(raw).hexdigest() != section["raw_sha256"]:
        raise AssertionError("raw colour digest mismatch")
    return tuple(
        raw[index * ROW_BYTES:(index + 1) * ROW_BYTES]
        for index in range(count)
    )


def verify(certificate, expected):
    if certificate["schema"] != "hn-exoo-d2-halfscale-certificate-v1":
        raise AssertionError("unknown certificate schema")
    if certificate["source"]["coordinate_rows"] != [list(row) for row in ROWS]:
        raise AssertionError("certificate changed the fixed source coordinates")

    base, raw_count, placements = enumerate_placements()
    family = certificate["family"]
    actual_digests = {
        "descriptor_sha256": descriptor_digest(placements),
        "point_sets_sha256": point_set_digest(placements),
    }
    if raw_count != family["raw_labeled_specifications"]:
        raise AssertionError("raw specification count mismatch")
    if len(placements) != family["distinct_moved_point_sets"]:
        raise AssertionError("distinct point-set count mismatch")
    for key, value in actual_digests.items():
        if family[key] != value:
            raise AssertionError(f"{key} mismatch")

    unit, long = source_distance_edges(base)
    source = certificate["source"]
    if (len(base), len(unit), len(long)) != (
            source["vertices"], source["unit_edges"], source["length_two_edges"]):
        raise AssertionError("source distance counts mismatch")
    source_edges = tuple(sorted(unit + long))
    if source["four_colourable"] is not False:
        raise AssertionError("malformed source chromatic claim")
    four_row, four_nodes = colour_graph(len(base), source_edges, 4)
    if four_row is not None:
        raise AssertionError("source two-distance graph is four-colourable")
    if four_nodes != source["four_colour_search_nodes"]:
        raise AssertionError("source four-colour search trace mismatch")
    if not valid_colouring(
            len(base), source_edges, source["five_colouring"], colours=5):
        raise AssertionError("invalid source five-colouring")

    packed_rows = decode_rows(certificate["colour_rows"], len(placements))
    histogram = Counter()
    for index, ((_source, _target, _reflected, moved), packed) in enumerate(
            zip(placements, packed_rows)):
        points, edges = unit_graph(base, moved)
        row = unpack_row(packed, len(points))
        if not valid_colouring(len(points), edges, row):
            raise AssertionError(f"invalid four-colouring at placement {index}")
        histogram[(len(points), len(edges))] += 1

    histogram_rows = [
        {"vertices": vertices, "edges": edges, "placements": count}
        for (vertices, edges), count in sorted(histogram.items())
    ]
    if histogram_rows != family["histogram"]:
        raise AssertionError("family histogram mismatch")
    if family["non_four_colourable"] != 0:
        raise AssertionError("certificate does not state the proved outcome")

    actual = {
        "raw_labeled_specifications": raw_count,
        "distinct_moved_point_sets": len(placements),
        **actual_digests,
        "histogram": histogram_rows,
        "source_vertices": len(base),
        "source_unit_edges": len(unit),
        "source_length_two_edges": len(long),
        "source_four_colour_search_nodes": four_nodes,
        "colour_rows_sha256": certificate["colour_rows"]["raw_sha256"],
        "record_target_met": False,
    }
    if actual != expected:
        raise AssertionError("verified values disagree with EXPECTED.json")
    return actual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--expected", type=Path, default=HERE / "EXPECTED.json")
    parser.add_argument("--write-validation", type=Path)
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    expected = json.loads(args.expected.read_text())
    result = verify(certificate, expected)
    output = {"status": "verified", **result}
    if args.write_validation:
        args.write_validation.write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
