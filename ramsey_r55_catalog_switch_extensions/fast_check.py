#!/usr/bin/env python3
"""Unchanged physical clause checking, with a native forward DRAT checker."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from physical import catalog, decode, rows, check_physical, require


def check(record, core, proof, checker):
    graph = decode(record)
    clauses = rows(core, 2*len(graph)-1)
    physical = check_physical(graph, clauses)
    checked = subprocess.run([str(checker.resolve()), str(core), str(proof)],
                             capture_output=True, text=True, timeout=120, check=True)
    proof_report = json.loads(checked.stdout)
    return {"status": "CHECKED_SWITCH_EXTENSION_EXCLUSION", "core_clauses": len(clauses),
            "physical": physical, "proof": proof_report,
            "core_sha256": sha256(core.read_bytes()).hexdigest(),
            "proof_sha256": sha256(proof.read_bytes()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("catalog", type=Path)
    parser.add_argument("parent", type=int)
    parser.add_argument("core", type=Path)
    parser.add_argument("proof", type=Path)
    parser.add_argument("--checker", type=Path, required=True)
    args = parser.parse_args()
    records = catalog(args.catalog)
    require(0 <= args.parent < len(records), "Parent index")
    print(json.dumps(check(records[args.parent], args.core, args.proof, args.checker), indent=2))


if __name__ == "__main__":
    main()
