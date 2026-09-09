#!/usr/bin/env python3
"""Generate the full quotient lists locally; the generated file is not committed."""
from pathlib import Path
import argparse
import hashlib
import json
import produce as P


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise FileExistsError(args.out)
    certificate, data = P.compute()
    output = {
        "schema": "hn-complex-radix-d3-explicit-quotient-v1",
        "source_commit": certificate["source_commit"],
        "source_factor_inventory_sha256": certificate["source_factor_inventory_sha256"],
        "source_pair_inventory_sha256": certificate["source_pair_inventory_sha256"],
        "source_collision_inventory_sha256": certificate["source_collision_inventory_sha256"],
        "parameter_action": certificate["parameter_action"],
        "curve_orbits": [
            {"representative": representative, "members": sorted({action[representative] for action in data["curve_group"]})}
            for representative in data["curve_representatives"]
        ],
        "pair_system_representatives": data["pair_representatives"],
        "collision_polynomial_representatives": [
            data["collisions"][item] for item in data["collision_representatives"]
        ],
    }
    raw = (json.dumps(output, sort_keys=True, separators=(",", ":")) + "\n").encode()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(raw)
    print(
        json.dumps(
            {
                "path": str(args.out),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "curve_orbits": len(output["curve_orbits"]),
                "pair_system_representatives": len(output["pair_system_representatives"]),
                "collision_polynomial_representatives": len(output["collision_polynomial_representatives"]),
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
