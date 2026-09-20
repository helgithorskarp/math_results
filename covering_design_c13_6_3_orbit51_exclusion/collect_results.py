#!/usr/bin/env python3
"""Collect compact hashes and verification outcomes from completed case runs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("case_dirs", nargs="+", type=Path)
    args = parser.parse_args()
    cases = []
    for directory in args.case_dirs:
        for metadata_path in sorted(directory.glob("*.json")):
            stem = metadata_path.stem
            cnf = directory / f"{stem}.cnf"
            proof = directory / f"{stem}.drat"
            solver_log = directory / f"{stem}.solver.log"
            checker_log = directory / f"{stem}.check.log"
            status = (directory / f"{stem}.status").read_text().split()
            checked = (directory / f"{stem}.check.status").read_text().split()
            assert status == [stem, "20"]
            assert checked == [stem, "VERIFIED"]
            assert "s UNSATISFIABLE" in solver_log.read_text(errors="replace")
            assert "s VERIFIED" in checker_log.read_text(errors="replace")
            metadata = json.loads(metadata_path.read_text())
            assert sha256(cnf) == metadata["cnf_sha256"]
            cases.append({
                "name": stem,
                "case": metadata["qfree_case"],
                "qpair_pattern": metadata["qpair_pattern"],
                "qthrough_type": metadata["qthrough_type"],
                "qaway_triple_intersection": metadata["qaway_triple_intersection"],
                "designated_qfree_residue": metadata["designated_qfree_residue"],
                "variables": metadata["variables"],
                "clauses": metadata["clauses"],
                "cnf_bytes": cnf.stat().st_size,
                "cnf_sha256": metadata["cnf_sha256"],
                "proof_bytes": proof.stat().st_size,
                "proof_sha256": sha256(proof),
                "solver": "CaDiCaL 3.0.1",
                "solver_exit": 20,
                "checker": "drat-trim 2.2",
                "checker_status": "VERIFIED",
            })
    names = [item["name"] for item in cases]
    assert len(names) == len(set(names)) == 91
    result = {
        "case_count": len(cases),
        "total_cnf_bytes": sum(item["cnf_bytes"] for item in cases),
        "total_proof_bytes": sum(item["proof_bytes"] for item in cases),
        "cases": sorted(cases, key=lambda item: item["name"]),
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "cases"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
