#!/usr/bin/env python3
"""Independent cover, formula-tail, and fresh-proof audit for Core194."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
COVER = ROOT / "ramsey_r55_order3_eleven_core194_attachments"
TARGET = ROOT / "ramsey_r55_order3_eleven_core194_attachment_decisions"
ALL_CASES = (
    "a1_b3_c3", "a2_b2_c3", "a3_b1_c3", "a3_b2_c2", "a4_b0_c3",
    "a4_b1_c2", "a5_b0_c2", "a5_b1_c1", "a6_b0_c1",
)
EXCLUDED = ALL_CASES[:5]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def identity(path: Path) -> dict:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def read_census(path: Path) -> tuple[dict, dict]:
    summary = {}
    rows = {}
    for line in path.read_text().splitlines():
        fields = line.split()
        require(fields, "blank census line")
        if fields[0] == "row":
            require(len(fields) == 8, "malformed census row")
            counts = tuple(map(int, fields[1:7]))
            require(counts not in rows, "duplicate census profile")
            rows[counts] = int(fields[7])
        else:
            require(len(fields) == 2 and fields[0] not in summary, "malformed census header")
            summary[fields[0]] = int(fields[1])
    require(summary == {"total": 3**15, "allowed": 4_806_900, "profiles": 119}, "census totals")
    require(len(rows) == 119 and sum(rows.values()) == summary["allowed"], "complete census")
    return summary, rows


def expected_moving_units(counts: tuple[int, int, int]) -> list[int]:
    units = []
    cycle = 4
    for contact, amount in enumerate(counts):
        for _ in range(amount):
            # Direct primary numbering: fixed-moving orbit (f, cycle) is
            # 211 + 11*(f-33) + cycle. Positive means red.
            u = 211 + cycle
            v = 222 + cycle
            units.extend((u if contact != 2 else -u, v if contact != 1 else -v))
            cycle += 1
    require(cycle == 11 and len(units) == 14, "seven normalized moving triangles")
    return units


def audit_cover(census_path: Path) -> tuple[dict, dict]:
    summary, census = read_census(census_path)
    certificate = json.loads((COVER / "certificate.json").read_text())
    require(certificate["all_no_BB_assignments"] == summary["total"], "raw assignment count")
    require(certificate["allowed_labeled_assignments"] == summary["allowed"], "allowed assignment count")
    public = {tuple(row["counts"]): row for row in certificate["profiles"]}
    require(set(public) == set(census), "entrywise profile domain")
    for counts, weight in census.items():
        row = public[counts]
        a, b, c, x, y, z = counts
        require(row["labeled_assignments"] == weight, "profile orbit weight")
        require(row["red_degrees"] == [3 * (a + b) + x + y, 3 * (a + c) + x + z], "root degrees")
        require(18 <= row["red_degrees"][0] <= 24 and 18 <= row["red_degrees"][1] <= 24, "degree window")
    grouped = defaultdict(list)
    for counts, weight in census.items():
        grouped[counts[:3]].append((counts, weight))
    require(tuple(sorted(grouped)) == tuple(tuple(map(int, case[1:].replace("_b", " ").replace("_c", " ").split())) for case in ALL_CASES), "nine moving types")
    moving = certificate["moving_cases"]
    require([row["id"] for row in moving] == list(ALL_CASES), "public moving order")
    for row in moving:
        counts = tuple(row["counts"])
        require(row["units"] == expected_moving_units(counts), "physical fourteen-unit attachment")
        require(row["joint_profiles"] == len(grouped[counts]), "moving profile count")
        require(row["labeled_assignments"] == sum(weight for _, weight in grouped[counts]), "moving labeled weight")
    excluded_profiles = sum(len(grouped[tuple(row["counts"])]) for row in moving[:5])
    excluded_weight = sum(sum(weight for _, weight in grouped[tuple(row["counts"])]) for row in moving[:5])
    require((excluded_profiles, excluded_weight) == (70, 3_504_900), "excluded cover mass")
    return {
        **summary,
        "moving_types": len(grouped),
        "excluded_profiles": excluded_profiles,
        "excluded_labeled_assignments": excluded_weight,
        "remaining_profiles": 119 - excluded_profiles,
        "remaining_labeled_assignments": summary["allowed"] - excluded_weight,
        "enumeration": "direct C++ sweep of all 3^15 labeled assignments",
    }, {row["id"]: row for row in moving}


def read_units(stream) -> list[int]:
    units = []
    for line in stream:
        fields = line.split()
        require(len(fields) == 2 and fields[1] == b"0", "unit-clause tail")
        units.append(int(fields[0]))
    return units


def audit_formulas(work: Path, moving: dict, target_rows: dict) -> list[dict]:
    base = work / "blue.cnf"
    with base.open("rb") as stream:
        require(stream.readline() == b"p cnf 320 366069\n", "base header")
        base_body = stream.read()
    require(identity(base) == {"bytes": 14883777, "sha256": "f3314485280b2080f3459774b944e010beeb175788673d53703d60cba091e84c"}, "reviewed base identity")
    result = []
    for case in ALL_CASES:
        path = work / f"{case}.cnf"
        with path.open("rb") as stream:
            require(stream.readline() == b"p cnf 320 366083\n", "child header")
            require(stream.read(len(base_body)) == base_body, "complete base body retained")
            tail = read_units(stream)
        require(tail == expected_moving_units(tuple(moving[case]["counts"])), "exact physical child tail")
        actual = identity(path)
        require(actual == target_rows[case]["formula"], "published formula identity")
        result.append({"id": case, "counts": moving[case]["counts"], "formula": actual, "tail_units": len(tail)})
    return result


def audit_proofs(work: Path, public_rows: dict) -> tuple[list[dict], dict]:
    record = json.loads((work / "proofs.json").read_text())
    require(record["status"] == "PASS" and record["execution"].startswith("serial"), "complete serial proof run")
    require([row["id"] for row in record["cases"]] == list(EXCLUDED), "five proof cases")
    rows = []
    for row in record["cases"]:
        case = row["id"]
        public = public_rows[case]
        require(identity(work / f"{case}.drat") == row["proof"], "fresh proof file identity")
        require(identity(work / f"{case}.solve.log") == row["solver_log"], "fresh solver-log identity")
        require(identity(work / f"{case}.replay.log") == row["replay_log"], "fresh replay-log identity")
        require(row["formula"] == public["formula"], "proof input formula")
        require(row["proof"] == public["trace"], "fresh proof reproduces published trace")
        require(row["rat_core_lemmas"] == public["replay"]["rat_core_lemmas"], "full RAT statistics")
        solve_text = (work / f"{case}.solve.log").read_text()
        statuses = [line for line in solve_text.splitlines() if line.startswith("s ")]
        require(statuses == ["s UNSATISFIABLE"], "exact fresh solver status")
        replay_text = (work / f"{case}.replay.log").read_text()
        require("s VERIFIED" in replay_text and re.search(r"\d+ RAT lemmas in core", replay_text), "fresh full DRAT replay")
        rows.append({
            "id": case,
            "formula": row["formula"],
            "proof": row["proof"],
            "rat_core_lemmas": row["rat_core_lemmas"],
        })
    require(record["drat_trim_binary"]["sha256"] == "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a", "pinned DRAT-trim")
    return rows, {
        "execution": record["execution"],
        "kissat_version": record["kissat_version"],
        "kissat_binary": record["kissat_binary"],
        "drat_trim_binary": record["drat_trim_binary"],
    }


def main() -> None:
    if not __debug__:
        raise RuntimeError("run with assertions enabled (omit -O)")
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--formula-work", type=Path, required=True)
    parser.add_argument("--proof-work", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    cover, moving = audit_cover(args.census)
    public_result = json.loads((TARGET / "result.json").read_text())
    public_rows = {row["id"]: row for row in public_result["cases"]}
    require(set(public_rows) == set(ALL_CASES), "public nine-case record")
    require([public_rows[c]["status"] for c in ALL_CASES] == ["excluded"] * 5 + ["open"] * 4, "published status boundary")
    formulas = audit_formulas(args.formula_work, moving, public_rows)
    proofs, proof_tools = audit_proofs(args.proof_work, public_rows)
    result = {
        "status": "PASS",
        "verdict": "five complete blue-pair attachment types independently refuted",
        "cover": cover,
        "formulas": formulas,
        "proofs": proofs,
        "proof_tools": proof_tools,
        "excluded_types": list(EXCLUDED),
        "remaining_types": list(ALL_CASES[5:]),
        "consequence": "a>=4; if a=4 then (a,b,c)=(4,1,2)",
        "whole_core194_excluded": False,
        "red_pair_branch_resolved": False,
        "target_graph_found": False,
        "solver_or_checker_parallelism": 1,
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.report:
        args.report.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
