#!/usr/bin/env python3
"""Physical input clauses plus an exact forward DRAT check; no SAT trust."""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
from physical import catalog, decode, rows, check_physical, require

DRAT_SOURCE = Path(__file__).resolve().parent.parent / "ramsey_r55_paley41_switch_family/check_certificate.py"
DRAT_SHA = "c11cb9ced4987bdb8384cc57a87c455c9d59c33f28df56da53918351c0516e2c"
require(sha256(DRAT_SOURCE.read_bytes()).hexdigest() == DRAT_SHA, "Shared proof-checker hash")
spec = importlib.util.spec_from_file_location("checked_drat", DRAT_SOURCE)
drat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(drat)


def check(record, core, proof):
    graph = decode(record)
    clauses = rows(core, 2*len(graph)-1)
    physical = check_physical(graph, clauses)
    proof_report = drat.verify_proof(clauses, proof)
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
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records = catalog(args.catalog)
    require(0 <= args.parent < len(records), "Parent index")
    report = check(records[args.parent], args.core, args.proof)
    report["parent"] = args.parent
    text = json.dumps(report, indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
