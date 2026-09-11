#!/usr/bin/env python3
"""Generate the exact (U,U) white-graph or fixed-star branch family."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--encoder", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument(
        "--fixed-star",
        action="store_true",
        help="split each white-graph branch into its six anchored-star cases",
    )
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    records = []
    star_cases = range(6) if args.fixed_star else (None,)
    for omega in ("z4", "z2xz2"):
        for p0 in ("p0a", "p0b", "p0c"):
            for orbit in range(9):
                for star in star_cases:
                    stem = f"UU-{omega}-{p0}-whitegraph-{orbit}"
                    if star is not None:
                        stem += f"-fixedstar-{star}"
                    cnf = args.out / f"{stem}.cnf"
                    command = [
                        "python3", str(args.encoder), "UU", "-triple",
                        "-direct-extension", "-distinguished-subsquare",
                        "-pairwise-onehot", f"-{omega}", f"-{p0}",
                        f"-whitegraph-{orbit}",
                    ]
                    if star is not None:
                        command.append(f"-fixedstar-{star}")
                    with cnf.open("wb") as output:
                        subprocess.run(command, stdout=output, check=True)
                    with cnf.open(encoding="ascii") as handle:
                        header = handle.readline().strip()
                    records.append({
                        "id": stem,
                        "omega": omega,
                        "p0": p0,
                        "whitegraph_orbit": orbit,
                        "fixedstar_case": star,
                        "cnf": cnf.name,
                        "header": header,
                        "sha256": sha256(cnf),
                        "command": command,
                    })

    expected = 324 if args.fixed_star else 54
    assert len(records) == expected
    coverage = "2 omega classes x 3 P-row forms x 9 joint white-graph orbits"
    if args.fixed_star:
        coverage += " x 6 anchored-star partial transversals"
    args.manifest.write_text(
        json.dumps({"coverage": coverage, "instances": records}, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"generated {len(records)} instances")
    print(f"manifest {args.manifest}")


if __name__ == "__main__":
    main()
