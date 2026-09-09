#!/usr/bin/env python3
"""Collect a checked 238-source run into compact, source-indexed certificates."""
from hashlib import sha256
from pathlib import Path
import argparse
import json
import statistics

from generate import INPUT_SHA256, sources


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return {"bytes": path.stat().st_size,
            "sha256": sha256(path.read_bytes()).hexdigest()}


def values(reports, path):
    result = []
    for report in reports:
        value = report
        for key in path:
            value = value[key]
        result.append(value)
    return result


def summary(numbers):
    return {"min": min(numbers), "max": max(numbers), "sum": sum(numbers),
            "median": statistics.median(numbers)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    run = args.run.resolve()
    output = args.output.resolve()
    source_rows = sources()
    full = json.loads((run / "census.json").read_text())
    need(full["status"] == "VERIFIED_COMPLETE_238_SOURCE_SWITCH_CLASS_EXCLUSION",
         "run is not a complete exclusion")
    reports = full["results"]
    need(len(reports) == len(source_rows) == 238, "source count")
    cases = []
    with (output / "cores.dimacs").open("x") as cores_out, \
            (output / "proofs.drat").open("x") as proofs_out:
        for index, (toggles, expected) in enumerate(zip(source_rows, reports)):
            folder = run / f"source-{index:03d}"
            report = json.loads((folder / "result.json").read_text())
            need(report == expected, f"source {index}: census/result mismatch")
            need(report["source_index"] == index and
                 report["toggle_indices"] == toggles and
                 report["status"] == "VERIFIED_UNSAT", f"source {index}: identity/status")
            core = folder / "core.cnf"
            proof = folder / "proof.trimmed.drat"
            need(digest(core) == report["core"], f"source {index}: core identity")
            need(digest(proof) == report["trimmed_proof"],
                 f"source {index}: proof identity")
            core_text = core.read_text()
            proof_text = proof.read_text()
            need(core_text.startswith("p cnf 42 ") and core_text.endswith("\n"),
                 f"source {index}: core format")
            need(proof_text.endswith("0\n"), f"source {index}: proof termination")
            cores_out.write(f"c source {index}\n{core_text}")
            proofs_out.write(f"c source {index}\n{proof_text}")
            cases.append({
                "source_index": index, "toggle_count": len(toggles),
                "clauses": report["formula_counts"]["clauses"],
                "coherent_five_sets": report["formula_counts"]["coherent_five_sets"],
                "formula_sha256": report["formula"]["sha256"],
                "core_bytes": report["core"]["bytes"],
                "core_sha256": report["core"]["sha256"],
                "proof_bytes": report["trimmed_proof"]["bytes"],
                "proof_sha256": report["trimmed_proof"]["sha256"],
                "solver_seconds": report["solver_seconds"],
                "proof_check_seconds": report["proof_check_seconds"],
            })
    columns = list(cases[0])
    with (output / "cases.tsv").open("x") as stream:
        stream.write("\t".join(columns) + "\n")
        for case in cases:
            stream.write("\t".join(str(case[key]) for key in columns) + "\n")
    compact = {
        "status": "VERIFIED_COMPLETE_238_SOURCE_SWITCH_CLASS_EXCLUSION",
        "source_count": 238,
        "normalization": "s_0=0",
        "switch_variables": 42,
        "distinct_labeled_graphs_per_source": str(2 ** 42),
        "source_indexed_graph_count": str(238 * 2 ** 42),
        "pinned_source_sha256": INPUT_SHA256,
        "formula_clause_statistics": summary(values(reports, ("formula_counts", "clauses"))),
        "coherent_five_set_statistics": summary(values(
            reports, ("formula_counts", "coherent_five_sets"))),
        "full_formula_byte_statistics": summary(values(reports, ("formula", "bytes"))),
        "compact_core_byte_statistics": summary(values(reports, ("core", "bytes"))),
        "compact_proof_byte_statistics": summary(values(
            reports, ("trimmed_proof", "bytes"))),
        "solver_second_statistics": summary(values(reports, ("solver_seconds",))),
        "proof_check_second_statistics": summary(values(reports, ("proof_check_seconds",))),
        "production_wall_seconds": full["wall_seconds"],
        "production_jobs": full["jobs"],
        "kissat": full["kissat"],
        "drat_trim": full["drat_trim"],
        "certificates": {
            "cores.dimacs": digest(output / "cores.dimacs"),
            "proofs.drat": digest(output / "proofs.drat"),
            "cases.tsv": digest(output / "cases.tsv"),
        },
    }
    (output / "census.json").write_text(json.dumps(compact, indent=2,
                                                    sort_keys=True) + "\n")
    print(json.dumps(compact, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
