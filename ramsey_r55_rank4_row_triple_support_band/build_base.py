#!/usr/bin/env python3
"""Build one unsplit row-full completion formula and its variable map."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import time

from joint_completion import build_formula, file_sha256, row_orbits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--orbit", type=int, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--support-symmetry", action="store_true",
                        help="encode inverse-transpose stabilizer canonicality")
    parser.add_argument("--support-maximum", type=int)
    args = parser.parse_args()
    orbits, census = row_orbits()
    if not 0 <= args.orbit < len(orbits):
        raise ValueError("orbit index out of range")
    started = time.monotonic()
    metadata = build_formula(orbits[args.orbit], args.cnf,
                             nonzero_support_maximum=args.support_maximum,
                             support_symmetry_break=args.support_symmetry)
    result = {
        "schema": "rank4-row-full-base-formula-v1",
        "row_orbit_census": census,
        "row_orbit": orbits[args.orbit],
        "formula": {
            "variables": metadata["variables"],
            "clauses": metadata["clauses"],
            "ramsey_clauses": metadata["ramsey_clauses"],
            "bytes": args.cnf.stat().st_size,
            "sha256": file_sha256(args.cnf),
            "generation_seconds": time.monotonic() - started,
        },
        "variable_map": metadata,
    }
    args.metadata.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "formula": result["formula"],
        "orbit": args.orbit,
        "support_variables": metadata["support_variables"],
        "support_symmetry_clauses": metadata["support_symmetry_clauses"],
        "canonical_valid_supports": metadata["canonical_valid_supports"],
        "row_stabilizer_size": metadata["row_stabilizer_size"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
