#!/usr/bin/env python3
"""Write the compact exact-four pair and signature interface."""
from pathlib import Path
import argparse
import hashlib
import json
import produce as P

HERE = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=HERE / "exact_four_interface.json")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    if args.out.exists() and not args.force:
        raise FileExistsError(args.out)
    certificate, data = P.compute()
    raw = data["interface_raw"]
    args.out.write_bytes(raw)
    print(
        json.dumps(
            {
                "path": str(args.out),
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "pair_representatives": certificate["pair_frontier"][
                    "exact_four_compatible_orbits"
                ],
                "signature_patterns": certificate["exact_four"][
                    "no_circle_signature_patterns"
                ]
                + certificate["exact_four"]["with_circle_signature_patterns"],
            },
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
