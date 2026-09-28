#!/usr/bin/env python3
"""Independent all-geodesic-pair audit of a small hard graph6 stream."""

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "planar_two_geodesic_finite"))
import check  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stream", type=Path)
    parser.add_argument("--expected", type=int, required=True)
    args = parser.parse_args()
    digest = hashlib.sha256()
    count = 0
    for raw in args.stream.open("rb"):
        digest.update(raw)
        adj = check.decode_graph6(raw)
        if len(adj) != 16:
            raise ValueError("wrong graph order")
        paths = sorted(
            check.geodesic_masks(adj, check.distances(adj)),
            key=lambda mask: -mask.bit_count(),
        )
        if not any(
            check.largest_component(adj, p | q) <= 4
            for p in paths
            for q in paths
        ):
            raise ValueError(f"no four-residual pair at record {count}: {raw!r}")
        count += 1
    if count != args.expected:
        raise ValueError(f"expected {args.expected} records, found {count}")
    print(json.dumps({"records": count, "failures": 0, "sha256": digest.hexdigest()}, sort_keys=True))


if __name__ == "__main__":
    main()
