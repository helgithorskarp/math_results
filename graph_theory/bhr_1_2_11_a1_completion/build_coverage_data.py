#!/usr/bin/env python3
"""Extract the compact coverage data used by the a=1 completion audit."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--dead", type=Path, required=True)
    parser.add_argument("--trimodal", type=Path, required=True)
    parser.add_argument("--small-a-c3", type=Path, required=True)
    parser.add_argument("--mantle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    source = json.loads(args.source.read_bytes())
    dead = json.loads(args.dead.read_bytes())
    trimodal = json.loads(args.trimodal.read_bytes())
    small_a_c3 = json.loads(args.small_a_c3.read_bytes())
    mantle = json.loads(args.mantle.read_bytes())

    data = {
        "schema": "bhr-1-2-11-a1-coverage-data-v1",
        "upstream_sha256": {
            "source": digest(args.source),
            "dead": digest(args.dead),
            "trimodal": digest(args.trimodal),
            "small_a_c3": digest(args.small_a_c3),
            "mantle": digest(args.mantle),
        },
        "cases": [],
        "dead_orthants": [],
        "trimodal": [],
        "small_a_c3_seed": small_a_c3["seed"]["counts"],
        "mantle": [],
    }
    for case in sorted(source["cases"], key=lambda item: tuple(item["base"])):
        maxima = [
            max(witness["counts"][coordinate] for witness in case["witnesses"])
            for coordinate in range(3)
        ]
        data["cases"].append(
            {
                "base": case["base"],
                "maxima": maxima,
                "witnesses": [
                    {"counts": witness["counts"], "grow": witness["grow"]}
                    for witness in case["witnesses"]
                ],
            }
        )
    for record in sorted(dead["repairs"], key=lambda item: tuple(item["residue_case"])):
        data["dead_orthants"].append(
            {
                "base": record["residue_case"],
                "seed": record["boundary_seed"]["counts"],
            }
        )
    for record in sorted(trimodal["cases"], key=lambda item: tuple(item["residue_case"])):
        data["trimodal"].append(
            {
                "base": record["residue_case"],
                "safe_seed": record["safe_seed"]["counts"],
                "cap_seed": record["cap_seed"]["counts"],
            }
        )
    for record in sorted(mantle["cases"], key=lambda item: tuple(item["residue_case"])):
        data["mantle"].append(
            {"base": record["residue_case"], "seed": record["safe_seed"]["counts"]}
        )

    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(f"output_sha256={hashlib.sha256(args.output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
