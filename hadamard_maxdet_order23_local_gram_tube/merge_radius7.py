#!/usr/bin/env python3
"""Merge a complete deterministic set of radius-seven shard certificates."""

from __future__ import annotations

import json
import sys
from pathlib import Path


EXPECTED_ORBITS = 1_503_560_419
EXPECTED_RADIUS6_CONNECTED = 4_361_518
EXPECTED_STORED_PARTITIONS = (
    "5+2",
    "5+1+1",
    "4+3",
    "4+2+1",
    "4+1+1+1",
    "3+3+1",
    "3+2+2",
    "3+2+1+1",
    "3+1+1+1+1",
    "2+2+2+1",
    "2+2+1+1+1",
    "2+1+1+1+1+1",
    "1+1+1+1+1+1+1",
)


def sum_multiplicity(parts: list[dict], key: str) -> dict[str, int]:
    canonical_values = {
        part[key]["canonical_count_vectors"] for part in parts
    }
    assert len(canonical_values) == 1
    canonical = canonical_values.pop()
    assigned = sum(part[key]["assigned_count_vectors"] for part in parts)
    assert assigned == canonical
    return {
        "canonical_count_vectors": canonical,
        "assignment_leaves": sum(
            part[key]["assignment_leaves"] for part in parts
        ),
        "symmetry_classes": sum(
            part[key]["symmetry_classes"] for part in parts
        ),
    }


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(
            "usage: python3 merge_radius7.py [-o RESULT.json] PART.json [...]"
        )
    arguments = sys.argv[1:]
    output_path = None
    if arguments[:1] == ["-o"]:
        if len(arguments) < 3:
            raise SystemExit("-o requires an output path and shard paths")
        output_path = Path(arguments[1])
        arguments = arguments[2:]
    paths = [Path(argument) for argument in arguments]
    parts = [json.loads(path.read_text()) for path in paths]
    shard_counts = {part["shard_count"] for part in parts}
    assert len(shard_counts) == 1
    shard_count = shard_counts.pop()
    assert len(parts) == shard_count
    assert {part["shard"] for part in parts} == set(range(shard_count))
    parts.sort(key=lambda part: part["shard"])

    fixed = {
        (
            part["schema"],
            part["order"],
            part["radius"],
            part["expected_global_symmetry_classes"],
            part["radius_six_connected_regression"],
            part["stored_connected_shapes_through_five"],
            part["stored_colored_connected_variants_through_five"],
            part["connected_six_edge_shapes"],
            part["connected_seven_edge_shapes"],
            tuple(part["witness_primes"]),
        )
        for part in parts
    }
    assert len(fixed) == 1
    (
        schema,
        order,
        radius,
        expected,
        regression,
        stored_shapes,
        stored_variants,
        six_shapes,
        seven_shapes,
        witness_primes,
    ) = fixed.pop()
    assert schema == "radius7-shard-v1"
    assert order == 23 and radius == 7
    assert expected == EXPECTED_ORBITS
    assert regression == EXPECTED_RADIUS6_CONNECTED
    assert stored_shapes == 22 and stored_variants == 2_593_788
    assert six_shapes == 30 and seven_shapes == 79
    assert len(witness_primes) == 48

    connected = sum_multiplicity(parts, "connected")
    six_plus_one = sum_multiplicity(parts, "six_plus_one")

    partition_maps = []
    for part in parts:
        mapping = {
            item["partition"]: item for item in part["stored_partitions"]
        }
        assert tuple(mapping) == EXPECTED_STORED_PARTITIONS
        assert sum(
            item["internally_colored_graphs"] for item in mapping.values()
        ) == part["stored_partition_internally_colored_graphs"]
        assert sum(item["symmetry_classes"] for item in mapping.values()) == (
            part["stored_partition_symmetry_classes"]
        )
        partition_maps.append(mapping)
    stored_partitions = [
        {
            "partition": name,
            "internally_colored_graphs": sum(
                mapping[name]["internally_colored_graphs"]
                for mapping in partition_maps
            ),
            "symmetry_classes": sum(
                mapping[name]["symmetry_classes"]
                for mapping in partition_maps
            ),
        }
        for name in EXPECTED_STORED_PARTITIONS
    ]
    stored_internal = sum(
        item["internally_colored_graphs"] for item in stored_partitions
    )
    stored_classes = sum(
        item["symmetry_classes"] for item in stored_partitions
    )

    symmetry_classes = sum(part["symmetry_classes"] for part in parts)
    assert symmetry_classes == (
        connected["symmetry_classes"]
        + six_plus_one["symmetry_classes"]
        + stored_classes
    )
    assert symmetry_classes == EXPECTED_ORBITS
    witness_counts = [
        sum(part["witness_counts"][index] for part in parts)
        for index in range(len(witness_primes))
    ]
    survivors = sorted(
        tuple(item)
        for part in parts
        for item in part["survivor_edge_indices"]
    )
    assert all(
        len(item) == 7
        and tuple(sorted(item)) == item
        and len(set(item)) == 7
        and all(0 <= edge < 253 for edge in item)
        for item in survivors
    )
    assert len(survivors) == len(set(survivors))
    assert sum(witness_counts) + len(survivors) == symmetry_classes

    result = {
        "schema": "radius7-certificate-v1",
        "order": order,
        "radius": radius,
        "shard_count": shard_count,
        "witness_primes": list(witness_primes),
        "stored_connected_shapes_through_five": stored_shapes,
        "stored_colored_connected_variants_through_five": stored_variants,
        "connected_six_edge_shapes": six_shapes,
        "connected_seven_edge_shapes": seven_shapes,
        "radius_six_connected_regression": regression,
        "connected": connected,
        "six_plus_one": six_plus_one,
        "stored_partitions": stored_partitions,
        "stored_partition_internally_colored_graphs": stored_internal,
        "stored_partition_symmetry_classes": stored_classes,
        "symmetry_classes": symmetry_classes,
        "witness_counts": witness_counts,
        "survives_48_nonsquare_tests": len(survivors),
        "survivor_edge_indices": [list(item) for item in survivors],
    }
    encoded = json.dumps(result, indent=2) + "\n"
    if output_path is None:
        sys.stdout.write(encoded)
    else:
        output_path.write_text(encoded)
        print(f"wrote {output_path}")


if __name__ == "__main__":
    main()
