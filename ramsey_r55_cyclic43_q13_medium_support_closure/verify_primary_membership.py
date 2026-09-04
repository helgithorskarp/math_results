#!/usr/bin/env python3
"""Verify q=7,8,9,10 endpoints against pinned primary-layer arrays."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


M = 903
EXPECTED = {
    "7": (
        "43a57b3891158d76a8404de8dc8aa51a4719fea2faddf23704b4ba814c978b78",
        "objective_seven_component_rotation_representatives",
    ),
    "8": (
        "740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a",
        "objective_eight_component_rotation_representatives",
    ),
    "9": (
        "ed95024d463512eb0ade0af77725dd8031ffc712e258283499cff6c06144a693",
        "objective_nine_rotation_representatives",
    ),
    "10": (
        "9b5b3b4747fedfba8b0191f052c9e6d2847aa9c910465f6c29358c2336977df4",
        "objective_ten_rotation_representatives",
    ),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pack(edges: list[int]) -> int:
    if edges != sorted(set(edges)) or any(not 0 <= edge < M for edge in edges):
        raise AssertionError("malformed edge list")
    return sum(1 << edge for edge in edges)


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("objective_seven", type=Path)
    parser.add_argument("objective_eight", type=Path)
    parser.add_argument("objective_nine", type=Path)
    parser.add_argument("objective_ten", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=here / "primary_membership.json")
    args = parser.parse_args()
    paths = {
        "7": args.objective_seven,
        "8": args.objective_eight,
        "9": args.objective_nine,
        "10": args.objective_ten,
    }
    certificate = json.loads(args.certificate.read_text())
    result = {
        "format": "cyclic43-q13-medium-support-primary-membership-v1",
        "closure_certificate_sha256": digest(args.certificate),
        "layers": {},
    }
    for objective in ("7", "8", "9", "10"):
        expected_hash, field = EXPECTED[objective]
        path = paths[objective]
        if digest(path) != expected_hash:
            raise AssertionError(f"unexpected objective-{objective} source hash")
        representatives = [pack(item) for item in json.loads(path.read_text())[field]]
        position = {state: number for number, state in enumerate(representatives)}
        if len(position) != len(representatives):
            raise AssertionError(f"duplicate objective-{objective} source representative")
        endpoints = [
            pack(item)
            for item in certificate["sublevel_endpoint_states_by_objective"][objective]
        ]
        missing = [state for state in endpoints if state not in position]
        if missing:
            raise AssertionError(
                f"{len(missing)} objective-{objective} endpoints are absent from the primary array"
            )
        result["layers"][objective] = {
            "source_sha256": expected_hash,
            "source_field": field,
            "source_representative_count": len(representatives),
            "endpoint_count": len(endpoints),
            "all_endpoints_present": True,
            "endpoint_indices_in_certificate_order": [position[state] for state in endpoints],
        }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS all q=7,8,9,10 endpoints occur in pinned primary-layer arrays")
    print(
        "endpoint_counts="
        + str({objective: result["layers"][objective]["endpoint_count"] for objective in result["layers"]})
    )
    print(f"output_sha256={digest(args.output)}")


if __name__ == "__main__":
    main()
