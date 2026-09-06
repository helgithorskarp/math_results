#!/usr/bin/env python3
"""Independent formula construction and serial proof replay for the a6 closure."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "ramsey_r55_order3_eleven_core194_a6_fixed"
DIRECT = ROOT / "ramsey_r55_order3_eleven_core194_direct"
CASES = (
    ("x0_y5_z3", (0, 5, 3), 56, (23, 24)),
    ("x0_y6_z2", (0, 6, 2), 28, (24, 23)),
    ("x1_y5_z2", (1, 5, 2), 168, (24, 24)),
)
BASE_IDENTITY = {
    "bytes": 14_883_777,
    "sha256": "f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c",
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def read_census(path: Path) -> dict:
    summary: dict[str, int] = {}
    rows: list[dict] = []
    for line in path.read_text().splitlines():
        fields = line.split()
        require(fields, "blank census line")
        if fields[0] == "row":
            require(len(fields) == 7, "malformed census row")
            x, y, z, weight, red_u, red_v = map(int, fields[1:])
            rows.append({"fixed_counts": [x, y, z], "fixed_words": weight,
                         "red_degrees": [red_u, red_v]})
        else:
            require(len(fields) == 2 and fields[0] not in summary, "malformed census summary")
            summary[fields[0]] = int(fields[1])
    require(summary == {"total": 3**8, "allowed": 252, "profiles": 3,
                        "sorting_permutations": 223}, "complete fixed-word census")
    expected = [
        {"fixed_counts": list(counts), "fixed_words": weight, "red_degrees": list(degrees)}
        for _, counts, weight, degrees in CASES
    ]
    require(rows == expected and sum(row["fixed_words"] for row in rows) == 252,
            "three exact fixed profiles")
    return {**summary, "rows": rows, "method": "direct C++ enumeration of all 3^8 words"}


def contact_units(fixed_counts: tuple[int, int, int]) -> list[int]:
    # The independently reviewed direct formula numbers fixed-moving orbit
    # (f, cycle) as 211 + 11*(f-33) + cycle, with positive meaning red.
    units: list[int] = []
    moving_contacts = [0] * 6 + [2]  # RR x6, then BR x1.
    for cycle, contact in enumerate(moving_contacts, start=4):
        u_var = 211 + cycle
        v_var = 222 + cycle
        units.extend((u_var if contact != 2 else -u_var,
                      v_var if contact != 1 else -v_var))

    fixed_contacts = [contact for contact, count in enumerate(fixed_counts) for _ in range(count)]
    require(len(fixed_contacts) == 8, "eight other fixed vertices")
    for offset, contact in enumerate(fixed_contacts):
        # Physical pairs (33,35+offset) and (34,35+offset).
        u_var = 167 + offset
        v_var = 175 + offset
        units.extend((u_var if contact != 2 else -u_var,
                      v_var if contact != 1 else -v_var))
    require(len(units) == 30 and len({abs(unit) for unit in units}) == 30,
            "thirty distinct contact units")
    return units


def construct_child(base: Path, child: Path, fixed_counts: tuple[int, int, int]) -> list[int]:
    with base.open("rb") as source, child.open("wb") as destination:
        require(source.readline() == b"p cnf 320 366069\n", "accepted BLUE base header")
        destination.write(b"p cnf 320 366099\n")
        while block := source.read(1 << 20):
            destination.write(block)
        units = contact_units(fixed_counts)
        for unit in units:
            destination.write(f"{unit} 0\n".encode())
    return units


def inspect_child(base: Path, child: Path, expected_units: list[int]) -> None:
    with base.open("rb") as source, child.open("rb") as candidate:
        require(source.readline() == b"p cnf 320 366069\n", "base header")
        require(candidate.readline() == b"p cnf 320 366099\n", "child header")
        while block := source.read(1 << 20):
            require(candidate.read(len(block)) == block, "entire accepted base body retained")
        tail = []
        for line in candidate:
            fields = line.split()
            require(len(fields) == 2 and fields[1] == b"0", "unit-clause tail")
            tail.append(int(fields[0]))
    require(tail == expected_units, "exact physical 30-unit tail and EOF")


def exact_status(path: Path, expected: str) -> None:
    statuses = [line for line in path.read_text().splitlines() if line.startswith("s ")]
    require(statuses == [expected], "unexpected solver status transcript")


def main() -> None:
    if not __debug__:
        raise RuntimeError("run without -O")
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--kissat", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--solve-seconds", type=int, default=90)
    parser.add_argument("--replay-seconds", type=int, default=600)
    args = parser.parse_args()
    require(not args.work.exists(), "work directory must be fresh")
    require(args.solve_seconds > 0 and args.replay_seconds > 0, "positive limits")
    args.work.mkdir(parents=True)

    target_profiles = json.loads((TARGET / "profiles.json").read_text())
    target_result = json.loads((TARGET / "result.json").read_text())
    public_cases = {row["id"]: row for row in target_result["cases"]}
    require(target_result["complete"] and target_result["excluded"] == [case[0] for case in CASES],
            "public complete claim")
    census = read_census(args.census)
    for row, (case_id, fixed_counts, fixed_words, degrees) in zip(target_profiles, CASES):
        require(row["counts"] == [6, 0, 1, *fixed_counts], "public fixed profile counts")
        require(row["red_degrees"] == list(degrees), "public red degrees")
        require(row["labeled_assignments"] == 14 * fixed_words, "public full-star weight")
        require(row["units"] == contact_units(fixed_counts), "public physical unit meanings")

    base = args.work / "blue.cnf"
    generated = subprocess.run(
        [sys.executable, "-B", str(DIRECT / "generate.py"), "--color", "blue", "--output", str(base)],
        text=True, capture_output=True, check=True,
    )
    base_report = json.loads(generated.stdout)
    require(identity(base) == BASE_IDENTITY == base_report["formula"], "accepted base regenerated exactly")

    version = subprocess.run([str(args.kissat), "--version"], text=True,
                             capture_output=True, check=True).stdout.strip()
    require(version == "4.0.4", "unexpected Kissat version")
    start = time.monotonic()
    rows = []
    for case_id, fixed_counts, _, _ in CASES:
        public = public_cases[case_id]
        cnf = args.work / f"{case_id}.cnf"
        units = construct_child(base, cnf, fixed_counts)
        inspect_child(base, cnf, units)
        formula = identity(cnf)
        require(formula == public["formula"], "fresh formula differs from public formula")

        trace = args.work / f"{case_id}.drat"
        solve_log = args.work / f"{case_id}.solve.log"
        solve_start = time.monotonic()
        with solve_log.open("w") as output:
            solved = subprocess.run(
                [str(args.kissat), f"--time={args.solve_seconds}", str(cnf), str(trace)],
                stdout=output, stderr=subprocess.STDOUT, timeout=args.solve_seconds + 60,
            )
        exact_status(solve_log, "s UNSATISFIABLE")
        require(solved.returncode == 20, "Kissat did not return UNSAT")

        replay_log = args.work / f"{case_id}.replay.log"
        replay_start = time.monotonic()
        with replay_log.open("w") as output:
            checked = subprocess.run(
                [str(args.drat_trim), str(cnf), str(trace), "-t", str(args.replay_seconds)],
                stdout=output, stderr=subprocess.STDOUT, timeout=args.replay_seconds + 60,
            )
        replay_text = replay_log.read_text()
        require(checked.returncode == 0 and "s VERIFIED" in replay_text, "full DRAT replay failed")
        rat = re.search(r"(\d+) RAT lemmas in core", replay_text)
        require(rat is not None, "missing full DRAT RAT statistics")
        proof = identity(trace)
        rows.append({
            "id": case_id,
            "fixed_counts": list(fixed_counts),
            "formula": formula,
            "proof": proof,
            "published_proof_match": proof == public["trace"],
            "rat_core_lemmas": int(rat.group(1)),
            "solve_seconds": round(replay_start - solve_start, 6),
            "replay_seconds": round(time.monotonic() - replay_start, 6),
        })
        print(f"VERIFIED {case_id}", flush=True)

    # Exercise the checker on one deliberately invalid refutation.
    sat = args.work / "sat.cnf"
    false_trace = args.work / "false.drat"
    sat.write_text("p cnf 1 1\n1 0\n")
    false_trace.write_text("0\n")
    false_log = args.work / "false.replay.log"
    with false_log.open("w") as output:
        false_check = subprocess.run(
            [str(args.drat_trim), str(sat), str(false_trace), "-t", "10"],
            stdout=output, stderr=subprocess.STDOUT, timeout=20,
        )
    require(false_check.returncode != 0 and "s VERIFIED" not in false_log.read_text(),
            "checker accepted false refutation")

    report = {
        "status": "PASS",
        "verdict": "the complete Core194 (6,0,1) moving type is excluded",
        "census": census,
        "base_formula": identity(base),
        "cases": rows,
        "all_three_refuted": len(rows) == 3,
        "proofs_match_published": all(row["published_proof_match"] for row in rows),
        "false_refutation_rejected": True,
        "execution": "serial; one solver or checker process at a time",
        "kissat_version": version,
        "kissat_binary": identity(args.kissat),
        "drat_trim_binary": identity(args.drat_trim),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "remaining_moving_types": [[4, 1, 2], [5, 0, 2], [5, 1, 1]],
        "whole_core194_excluded": False,
        "red_pair_branch_resolved": False,
        "target_graph_found": False,
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "cases": [row["id"] for row in rows]}, sort_keys=True))


if __name__ == "__main__":
    main()
