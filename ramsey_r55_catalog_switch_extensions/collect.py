#!/usr/bin/env python3
"""Replay all 328 certificates; only then produce the whole-union report."""
import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from hashlib import sha256
import json
from pathlib import Path
from fast_check import check
from physical import catalog, require, CATALOG_SHA


def verify(task):
    index, record, folder, checker = task
    result = json.loads((folder/"result.json").read_text())
    require(result["parent"] == index and result["seed"] == record, "Wrong parent")
    require(result["status"] == "CHECKED_SWITCH_EXTENSION_EXCLUSION", "Unresolved parent")
    direct = check(record, folder/"core.cnf", folder/"trimmed.drat", checker)
    require(direct == result["certificate"], "Certificate report mismatch")
    # Full formula and original trace are provenance, not trusted proof premises.
    for name, description in result["files"].items():
        data = (folder/name).read_bytes()
        require(len(data) == description["bytes"] and sha256(data).hexdigest() == description["sha256"],
                "Changed run file: "+str(folder/name))
    cnf = (folder/"family.cnf").read_bytes()
    require(sha256(cnf).hexdigest() == result["cnf_sha256"], "Full-formula hash mismatch")
    header = cnf.splitlines()[0].split()
    require(header[:3] == [b"p", b"cnf", b"83"] and len(header) == 4, "Full-formula header")
    return {"parent": index, "cnf_clauses": int(header[3]), "cnf_sha256": result["cnf_sha256"],
            "core_bytes": (folder/"core.cnf").stat().st_size,
            "proof_bytes": (folder/"trimmed.drat").stat().st_size, **direct}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("run", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--checker", type=Path, required=True)
    parser.add_argument("--jobs", type=int, default=4)
    args = parser.parse_args()
    require(1 <= args.jobs <= 4, "Worker bound")
    records = catalog(Path(__file__).with_name("r55_42some.g6"))
    tasks = [(i, row, args.run/f"parent{i:03d}", args.checker.resolve()) for i, row in enumerate(records)]
    with ProcessPoolExecutor(max_workers=args.jobs) as pool:
        results = list(pool.map(verify, tasks))
    require([r["parent"] for r in results] == list(range(328)), "Incomplete coverage")
    physical, proof = Counter(), Counter()
    for result in results:
        physical.update(result["physical"])
        proof.update(result["proof"])
    columns = ["parent", "cnf_clauses", "core_clauses", "core_bytes", "proof_bytes", "cnf_sha256", "core_sha256", "proof_sha256"]
    table = "\t".join(columns)+"\n"
    table += "".join("\t".join(str(row[key]) for key in columns)+"\n" for row in results)
    report = {"status": "CHECKED_ENTIRE_CATALOG_SWITCH_EXTENSION_UNION", "parents": 328,
              "normalized_variables_per_parent": 83, "catalog_sha256": CATALOG_SHA,
              "cases_tsv_sha256": sha256(table.encode()).hexdigest(),
              "cnf_clauses_total": sum(r["cnf_clauses"] for r in results),
              "core_clauses_total": sum(r["core_clauses"] for r in results),
              "core_bytes_total": sum(r["core_bytes"] for r in results),
              "trimmed_proof_bytes_total": sum(r["proof_bytes"] for r in results),
              "physical_clauses": dict(sorted(physical.items())), "proof_steps": dict(sorted(proof.items())),
              "core_clause_range": [min(r["core_clauses"] for r in results), max(r["core_clauses"] for r in results)],
              "unresolved": 0, "targets": 0, "external_review": False}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/"cases.tsv").write_text(table)
    (args.output/"report.json").write_text(json.dumps(report, indent=2)+"\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
