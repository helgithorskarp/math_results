#!/usr/bin/env python3
"""Generate the complete 36-instance (U,U) dark-column orbit family."""

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
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    records = []
    for omega in ("z4", "z2xz2"):
        for p0 in ("p0a", "p0b", "p0c"):
            for orbit in range(6):
                stem = f"UU-{omega}-{p0}-darkcol0-{orbit}"
                cnf = args.out / f"{stem}.cnf"
                command = [
                    "python3", str(args.encoder), "UU", "-triple",
                    "-direct-extension", "-distinguished-subsquare",
                    "-pairwise-onehot", f"-{omega}", f"-{p0}",
                    f"-darkcol0-{orbit}",
                ]
                with cnf.open("wb") as output:
                    subprocess.run(command, stdout=output, check=True)
                header = cnf.open(encoding="ascii").readline().strip()
                records.append({
                    "id": stem,
                    "omega": omega,
                    "p0": p0,
                    "darkcol0_orbit": orbit,
                    "cnf": cnf.name,
                    "header": header,
                    "sha256": sha256(cnf),
                    "command": command,
                })

    assert len(records) == 36
    args.manifest.write_text(json.dumps({
        "coverage": "2 omega classes x 3 P-row normal forms x 6 dark-column matching orbits",
        "instances": records,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"generated {len(records)} instances")
    print(f"manifest {args.manifest}")


if __name__ == "__main__":
    main()
