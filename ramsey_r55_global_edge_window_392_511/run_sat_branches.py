#!/usr/bin/env python3
"""Solve and proof-trim every endpoint residual branch into one certificate."""

import argparse
import collections
import json
import subprocess
import tempfile
import time
from pathlib import Path

import sat_endpoint_t5


def write_cnf(path, variables, clauses):
    with path.open("w") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")


def parse_cnf(path):
    clauses = []
    variables = None
    for raw in path.read_text().splitlines():
        if not raw or raw.startswith("c"):
            continue
        if raw.startswith("p cnf "):
            _, _, variables_raw, count_raw = raw.split()
            variables = int(variables_raw)
            expected = int(count_raw)
            continue
        values = list(map(int, raw.split()))
        if not values or values[-1] != 0:
            raise ValueError("malformed core clause")
        clauses.append(values[:-1])
    if variables is None or len(clauses) != expected:
        raise ValueError("core header")
    return variables, clauses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--physical", required=True)
    parser.add_argument("--ct", required=True)
    parser.add_argument("--cadical", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    ct = json.loads(Path(args.ct).read_text())
    branch_keys = [(item["residual_index"], index)
                   for item in ct["results"]
                   for index in range(item["ct_feasible_deltas"])]
    records = []
    statuses = collections.Counter()
    started = time.time()
    with tempfile.TemporaryDirectory(prefix="r55-e512-t5-",
                                     dir=args.output.parent) as raw_tmp:
        tmp = Path(raw_tmp)
        for branch_index, (residual_index, delta_index) in enumerate(branch_keys):
            clauses, metadata = sat_endpoint_t5.build(
                args.catalog, args.physical, args.ct,
                residual_index, delta_index)
            cnf = tmp / "branch.cnf"
            proof = tmp / "branch.drat"
            core = tmp / "branch.core"
            trimmed = tmp / "branch.trimmed.drat"
            write_cnf(cnf, metadata["variables"], clauses)
            solve = subprocess.run(
                [str(args.cadical), "-t", "60", "-c", "1000000",
                 str(cnf), str(proof)], capture_output=True, text=True,
                timeout=65)
            if solve.returncode == 10:
                status = "SAT"
                statuses[status] += 1
                records.append({"metadata": metadata, "status": status,
                                "solver_stdout": solve.stdout})
                print(json.dumps({"branch_index": branch_index,
                                  "residual_index": residual_index,
                                  "delta_index": delta_index,
                                  "status": status}), flush=True)
                continue
            if solve.returncode != 20 or "s UNSATISFIABLE" not in solve.stdout:
                status = "UNKNOWN_OR_ERROR"
                statuses[status] += 1
                records.append({"metadata": metadata, "status": status,
                                "solver_returncode": solve.returncode,
                                "solver_stdout": solve.stdout,
                                "solver_stderr": solve.stderr})
                print(json.dumps({"branch_index": branch_index,
                                  "residual_index": residual_index,
                                  "delta_index": delta_index,
                                  "status": status}), flush=True)
                continue
            trim = subprocess.run(
                [str(args.drat_trim), str(cnf), str(proof),
                 "-c", str(core), "-l", str(trimmed)],
                capture_output=True, text=True, timeout=65)
            trim_text = trim.stdout + trim.stderr
            if trim.returncode != 0 or "s VERIFIED" not in trim_text:
                raise ValueError("proof trim failed: " + trim_text[-2000:])
            core_variables, core_clauses = parse_cnf(core)
            full_set = {tuple(sorted(clause)) for clause in clauses}
            if any(tuple(sorted(clause)) not in full_set for clause in core_clauses):
                raise ValueError("core contains non-input clause")
            check = subprocess.run(
                [str(args.drat_trim), str(core), str(trimmed)],
                capture_output=True, text=True, timeout=65)
            check_text = check.stdout + check.stderr
            if check.returncode != 0 or "s VERIFIED" not in check_text:
                raise ValueError("trimmed proof recheck failed: " + check_text[-2000:])
            status = "UNSAT_VERIFIED"
            statuses[status] += 1
            record = {
                "metadata": metadata,
                "status": status,
                "core_variables": core_variables,
                "core_clauses": core_clauses,
                "trimmed_drat": trimmed.read_text().splitlines(),
            }
            records.append(record)
            print(json.dumps({"branch_index": branch_index,
                              "residual_index": residual_index,
                              "delta_index": delta_index,
                              "status": status,
                              "core_clauses": len(core_clauses),
                              "trimmed_drat_lines": len(record["trimmed_drat"])},
                             sort_keys=True), flush=True)
    output = {
        "status": ("COMPLETE_ALL_ENDPOINT_BRANCHES_UNSAT_VERIFIED" if
                   statuses == {"UNSAT_VERIFIED": len(branch_keys)} else
                   "INCOMPLETE_OR_SAT_ENDPOINT_BRANCHES"),
        "branches": len(branch_keys),
        "status_counts": dict(statuses),
        "elapsed_seconds": time.time() - started,
        "records": records,
    }
    args.output.write_text(json.dumps(output, sort_keys=True) + "\n")
    print(json.dumps({key: output[key] for key in
                      ("status", "branches", "status_counts",
                       "elapsed_seconds")}, sort_keys=True))


if __name__ == "__main__":
    main()
