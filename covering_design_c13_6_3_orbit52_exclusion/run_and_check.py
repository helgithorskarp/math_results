#!/usr/bin/env python3
"""Deterministically generate, solve, and proof-check all orbit-52 cases."""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import subprocess
from pathlib import Path

from generate_orbit52_cnf import (
    QFREE_TYPES,
    build,
    qaway_values,
    qthrough_types,
    render,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def specs():
    for case in sorted(QFREE_TYPES):
        for qpattern in ("111", "211"):
            yield case, qpattern, None, None
        for qpattern in ("221", "222"):
            for qthrough in qthrough_types(qpattern):
                for qaway in qaway_values(qpattern, qthrough):
                    yield case, qpattern, qthrough, qaway


def name_of(spec) -> str:
    case, qpattern, qthrough, qaway = spec
    suffix = "" if qthrough is None else "_" + "".join(map(str, qthrough)) + f"_{qaway}"
    return f"{case}_{qpattern}{suffix}"


def generate(spec, output: Path) -> tuple[str, dict[str, object]]:
    name = name_of(spec)
    case, qpattern, qthrough, qaway = spec
    formula, metadata = build(case, qpattern, qthrough, qaway)
    data = render(formula)
    cnf_path = output / f"{name}.cnf"
    cnf_path.write_bytes(data)
    metadata["cnf_sha256"] = hashlib.sha256(data).hexdigest()
    (output / f"{name}.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n"
    )
    return name, metadata


def solve_and_check(name: str, output: Path, cadical: Path, drat_trim: Path):
    cnf = output / f"{name}.cnf"
    proof = output / f"{name}.drat"
    solver_log = output / f"{name}.solver.log"
    checker_log = output / f"{name}.checker.log"
    with solver_log.open("wb") as log:
        solved = subprocess.run(
            [str(cadical), "--unsat", str(cnf), str(proof)],
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if solved.returncode != 20:
        raise RuntimeError(f"{name}: CaDiCaL exit {solved.returncode}")
    if b"s UNSATISFIABLE" not in solver_log.read_bytes():
        raise RuntimeError(f"{name}: missing UNSAT marker")
    with checker_log.open("wb") as log:
        checked = subprocess.run(
            [str(drat_trim), str(cnf), str(proof)],
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if checked.returncode != 0 or b"s VERIFIED" not in checker_log.read_bytes():
        raise RuntimeError(f"{name}: DRAT verification failed")
    return {
        "name": name,
        "proof_bytes": proof.stat().st_size,
        "proof_sha256": sha256(proof),
        "solver": "CaDiCaL 3.0.1 c60730422e758ef1cebe7aeddf2dda31c996bf04",
        "solver_exit": 20,
        "checker": "drat-trim 2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
        "checker_status": "VERIFIED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("cadical", type=Path)
    parser.add_argument("drat_trim", type=Path)
    parser.add_argument("--jobs", type=int, default=1)
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    args.output.mkdir(parents=True, exist_ok=True)

    generated = [generate(spec, args.output) for spec in specs()]
    assert len(generated) == len({name for name, _ in generated}) == 221
    metadata = {name: item for name, item in generated}
    print(json.dumps({"generated": len(generated)}), flush=True)

    checked_rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [
            pool.submit(solve_and_check, name, args.output, args.cadical, args.drat_trim)
            for name, _ in generated
        ]
        for future in concurrent.futures.as_completed(futures):
            row = future.result()
            checked_rows.append(row)
            print(json.dumps({"verified": row["name"]}), flush=True)

    cases = []
    for checked in checked_rows:
        name = checked.pop("name")
        item = metadata[name]
        cnf = args.output / f"{name}.cnf"
        cases.append({
            "name": name,
            "case": item["qfree_case"],
            "qpair_pattern": item["qpair_pattern"],
            "qthrough_type": item["qthrough_type"],
            "qaway_triple_intersection": item["qaway_triple_intersection"],
            "designated_qfree_residue": item["designated_qfree_residue"],
            "variables": item["variables"],
            "clauses": item["clauses"],
            "cnf_bytes": cnf.stat().st_size,
            "cnf_sha256": item["cnf_sha256"],
            **checked,
        })
    result = {
        "case_count": len(cases),
        "total_cnf_bytes": sum(item["cnf_bytes"] for item in cases),
        "total_proof_bytes": sum(item["proof_bytes"] for item in cases),
        "cases": sorted(cases, key=lambda item: item["name"]),
    }
    observed = args.output / "OBSERVED.json"
    observed.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")

    expected_path = Path(__file__).with_name("EXPECTED.json")
    if expected_path.exists():
        expected = json.loads(expected_path.read_text())
        if result != expected:
            raise RuntimeError("observed certificate manifest differs from EXPECTED.json")
    print(json.dumps({key: value for key, value in result.items() if key != "cases"},
                     sort_keys=True))


if __name__ == "__main__":
    main()
