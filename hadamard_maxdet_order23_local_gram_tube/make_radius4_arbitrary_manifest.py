#!/usr/bin/env python3
"""Create compact deterministic checkpoints for radius-four search shards."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
LEGAL_VALUES = tuple(range(-21, 20, 4))
PARTITIONS = ("4", "3+1", "2+2", "2+1+1", "1+1+1+1")
EXPECTED_INTERNAL = 1_886_683
EXPECTED_ORBITS = 197_931
EXPECTED_EVALUATIONS = 1_979_310_000


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def survivor_digest(items: list[list[list[int]]]) -> str:
    value_indices = {value: index for index, value in enumerate(LEGAL_VALUES)}
    digest = hashlib.sha256()
    previous = None
    for item in items:
        edits = tuple((int(edge), int(value)) for edge, value in item)
        edges = tuple(edge for edge, _ in edits)
        values = tuple(value for _, value in edits)
        assert len(edits) == 4
        assert edges == tuple(sorted(edges)) and len(set(edges)) == 4
        assert all(0 <= edge < 253 for edge in edges)
        assert all(value in value_indices for value in values)
        key = ",".join(f"{edge:03d}" for edge in edges)
        key += "|" + ",".join(f"{value_indices[value]:02d}" for value in values)
        assert previous is None or previous < key
        previous = key
        digest.update((key + "\n").encode("ascii"))
    return digest.hexdigest()


def main() -> None:
    if len(sys.argv) < 4 or sys.argv[1] != "-o":
        raise SystemExit(
            "usage: python3 make_radius4_arbitrary_manifest.py "
            "-o MANIFEST.json CERTIFICATE.json PART.json [...]"
        )
    output_path = Path(sys.argv[2])
    certificate_path = Path(sys.argv[3])
    paths = [Path(argument) for argument in sys.argv[4:]]
    certificate_bytes = certificate_path.read_bytes()
    certificate = json.loads(certificate_bytes)
    assert certificate["schema"] == "radius4-arbitrary-certificate-v1"
    shard_count = int(certificate["shard_count"])
    assert len(paths) == shard_count

    shards = []
    observed = set()
    for path in paths:
        data = path.read_bytes()
        part = json.loads(data)
        assert part["schema"] == "radius4-arbitrary-shard-v1"
        assert part["shard_count"] == shard_count
        shard = int(part["shard"])
        assert 0 <= shard < shard_count and shard not in observed
        observed.add(shard)
        partitions = part["partitions"]
        assert tuple(item["partition"] for item in partitions) == PARTITIONS
        assert sum(item["internally_colored_graphs"] for item in partitions) == (
            part["internally_colored_underlying_graphs"]
        )
        assert sum(item["underlying_edit_set_orbits"] for item in partitions) == (
            part["underlying_edit_set_orbits"]
        )
        assert part["normalized_cover_evaluations"] == (
            10_000 * part["underlying_edit_set_orbits"]
        )
        survivors = part["survivor_edits"]
        assert len(survivors) == part["survives_48_nonsquare_tests"]
        assert sum(part["witness_counts"]) + len(survivors) == part[
            "normalized_cover_evaluations"
        ]
        shards.append(
            {
                "shard": shard,
                "json_size_bytes": len(data),
                "json_sha256": sha256_bytes(data),
                "partitions": partitions,
                "internally_colored_underlying_graphs": part[
                    "internally_colored_underlying_graphs"
                ],
                "underlying_edit_set_orbits": part["underlying_edit_set_orbits"],
                "normalized_cover_evaluations": part[
                    "normalized_cover_evaluations"
                ],
                "witness_counts": part["witness_counts"],
                "survives_48_nonsquare_tests": len(survivors),
                "survivor_encoding_sha256": survivor_digest(survivors),
            }
        )
    assert observed == set(range(shard_count))
    shards.sort(key=lambda item: item["shard"])

    totals = {
        "internally_colored_underlying_graphs": sum(
            item["internally_colored_underlying_graphs"] for item in shards
        ),
        "underlying_edit_set_orbits": sum(
            item["underlying_edit_set_orbits"] for item in shards
        ),
        "normalized_cover_evaluations": sum(
            item["normalized_cover_evaluations"] for item in shards
        ),
        "survives_48_nonsquare_tests": sum(
            item["survives_48_nonsquare_tests"] for item in shards
        ),
        "witness_counts": [
            sum(item["witness_counts"][index] for item in shards)
            for index in range(48)
        ],
    }
    assert totals["internally_colored_underlying_graphs"] == EXPECTED_INTERNAL
    assert totals["underlying_edit_set_orbits"] == EXPECTED_ORBITS
    assert totals["normalized_cover_evaluations"] == EXPECTED_EVALUATIONS
    assert totals["survives_48_nonsquare_tests"] == certificate[
        "survives_48_nonsquare_tests"
    ]
    assert totals["witness_counts"] == certificate["witness_counts"]

    manifest = {
        "schema": "radius4-arbitrary-shard-manifest-v1",
        "shard_count": shard_count,
        "generator_sha256": sha256_bytes((HERE / "radius4_arbitrary.cpp").read_bytes()),
        "merger_sha256": sha256_bytes((HERE / "merge_radius4_arbitrary.py").read_bytes()),
        "certificate_sha256": sha256_bytes(certificate_bytes),
        "certificate_survivor_encoding_sha256": certificate[
            "survivor_encoding_sha256"
        ],
        "totals": totals,
        "shards": shards,
    }
    output_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
