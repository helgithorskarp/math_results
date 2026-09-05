#!/usr/bin/env python3
"""Independent first-empty blue-four branch formula and proof checker."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from itertools import combinations, product
from pathlib import Path


ALL_CASES = [
    92, 97, 109, 114, 118, 119, 122, 124, 154, 155, 159, 164, 167,
    168, 177, 180, 182, 185, 186, 188, 190, 191, 192, 193, 194,
]
EXCLUDED = [
    92, 97, 109, 114, 118, 119, 122, 154, 164, 167, 177, 182, 185,
    186, 188, 190, 191, 192, 193,
]
OPEN = [124, 155, 159, 168, 180, 194]


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def object_sha256(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def rotate(vertex: int) -> int:
    if vertex >= 33:
        return vertex
    return 3 * (vertex // 3) + (vertex % 3 + 1) % 3


def primary_variables() -> dict[tuple[int, int], int]:
    unseen = set(combinations(range(43), 2))
    moving: list[tuple[tuple[int, int], set[tuple[int, int]]]] = []
    fixed: list[tuple[tuple[int, int], set[tuple[int, int]]]] = []
    links: list[tuple[tuple[int, int], set[tuple[int, int]]]] = []
    while unseen:
        edge = min(unseen)
        orbit = {edge}
        image = tuple(sorted((rotate(edge[0]), rotate(edge[1]))))
        while image != edge:
            orbit.add(image)
            image = tuple(sorted((rotate(image[0]), rotate(image[1]))))
        unseen -= orbit
        representative = min(orbit)
        a, b = representative
        if b < 33:
            if a // 3 != b // 3:
                moving.append((representative, orbit))
        elif a >= 33:
            fixed.append((representative, orbit))
        else:
            links.append((representative, orbit))
    moving.sort(key=lambda item: (
        item[0][0] // 3,
        item[0][1] // 3,
        (item[0][1] - item[0][0]) % 3,
    ))
    fixed.sort()
    links.sort(key=lambda item: (item[0][1], item[0][0] // 3))
    ordered = moving + fixed + links
    need(len(ordered) == 320, "wrong primary orbit count")
    ids = {
        edge: variable
        for variable, (_, orbit) in enumerate(ordered, 1)
        for edge in orbit
    }
    for fixed_vertex in range(33, 43):
        for cycle in range(11):
            expected = 211 + 11 * (fixed_vertex - 33) + cycle
            need(ids[tuple(sorted((3 * cycle, fixed_vertex)))] == expected,
                 "fixed-moving variable formula mismatch")
    fixed_edges = [ids[(33, vertex)] for vertex in range(34, 43)]
    need(fixed_edges == list(range(166, 175)), "first fixed-edge block mismatch")
    return ids


def tail_rows() -> list[tuple[int, ...]]:
    ids = primary_variables()
    links = [ids[(3 * cycle, 33)] for cycle in range(4, 11)]
    need(links == list(range(215, 222)), "blue-triangle link block mismatch")
    rows = list(combinations(links, 5))
    rows.extend(tuple(-value for value in group) for group in combinations(links, 4))
    rows.extend((ids[(33, vertex)],) for vertex in range(34, 43))
    need(len(rows) == 65 and len(set(rows)) == 65, "wrong branch tail")
    return rows


def check_arithmetic() -> dict[str, object]:
    cardinality_checked = 0
    accepted_patterns: list[list[int]] = []
    degree_checked = 0
    degree_valid = 0
    valid_blue_histogram: dict[int, int] = {}
    extremal = 0
    for moving in product((False, True), repeat=7):
        lower = all(any(moving[index] for index in five)
                    for five in combinations(range(7), 5))
        upper = all(not all(moving[index] for index in four)
                    for four in combinations(range(7), 4))
        holds = lower and upper
        need(holds == (sum(moving) == 3), "cardinality encoding mismatch")
        cardinality_checked += 1
        if holds:
            accepted_patterns.append([index for index, red in enumerate(moving) if not red])
        for fixed in product((False, True), repeat=9):
            red_degree = 3 * sum(moving) + sum(fixed)
            blue_degree = 42 - red_degree
            blue_cycles = 7 - sum(moving)
            degree_checked += 1
            if 18 <= red_degree <= 24 and 18 <= blue_degree <= 24:
                degree_valid += 1
                valid_blue_histogram[blue_cycles] = valid_blue_histogram.get(blue_cycles, 0) + 1
                need(blue_cycles <= 4, "degree-valid assignment has five blue moving triangles")
                if blue_cycles == 4:
                    need(all(fixed), "maximal branch does not saturate fixed red edges")
                    need((red_degree, blue_degree) == (18, 24), "wrong maximal degrees")
                    extremal += 1
    need(cardinality_checked == 128 and degree_checked == 65_536, "incomplete arithmetic domain")
    expected_blue_patterns = [list(choice) for choice in combinations(range(7), 4)]
    need(sorted(accepted_patterns) == expected_blue_patterns, "not all 35 blue-four choices retained")
    need(extremal == 35, "wrong maximal-branch assignment count")
    return {
        "cardinality_assignments": cardinality_checked,
        "degree_assignments": degree_checked,
        "degree_valid_assignments": degree_valid,
        "degree_valid_blue_cycle_histogram": {
            str(key): valid_blue_histogram[key] for key in sorted(valid_blue_histogram)
        },
        "blue_four_patterns": 35,
        "maximal_assignments": extremal,
        "maximal_degrees": [18, 24],
    }


def check_manifests(source: Path) -> tuple[list[dict[str, object]], dict[int, dict[str, object]]]:
    cases = json.loads((source / "cases.json").read_text())
    result = json.loads((source / "result.json").read_text())
    boundary = json.loads((source / "boundary.json").read_text())
    previous = json.loads((source.parent / "ramsey_r55_order3_eleven_empty_propagation" / "boundary.json").read_text())
    need([case["index"] for case in cases] == ALL_CASES, "wrong 25-case manifest")
    need(sum(case["labeled"] for case in cases) == 15_957, "wrong labeled multiplicity")
    need(previous["remaining_open"] == ALL_CASES, "inherited boundary identity mismatch")
    need(result["complete"] and not result["target_graph"], "published run incomplete or target claimed")
    need(result["excluded"] == EXCLUDED and result["open"] == OPEN, "published decision partition mismatch")
    need(boundary["blue4_excluded"] == EXCLUDED and boundary["blue4_open"] == OPEN,
         "published branch boundary mismatch")
    need(boundary["new_whole_core_exclusions"] == [], "branch result misreported as whole-core exclusion")
    need(boundary["remaining_full_cores"] == ALL_CASES, "whole-core boundary changed")
    rows = {row["index"]: row for row in result["cases"]}
    need(sorted(rows) == ALL_CASES, "published case result coverage mismatch")
    for case in cases:
        row = rows[case["index"]]
        for key in ("index", "bits", "labeled", "omitted"):
            need(row[key] == case[key], "case identity mismatch")
        need(row["base"] == case["formula"], "inherited base identity mismatch")
        need(row["status"] == ("excluded" if case["index"] in EXCLUDED else "open"),
             "case status mismatch")
    return cases, rows


def generate_and_check_formulas(source: Path, work: Path, generate: bool) -> dict[str, object]:
    cases, results = check_manifests(source)
    rows = tail_rows()
    formula_dir = work / "review_formulas"
    formula_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for case in cases:
        index = case["index"]
        base = work / "inherited" / f"c{index}.cnf"
        formula = formula_dir / f"c{index}.cnf"
        need(file_info(base) == case["formula"], f"core {index}: inherited base hash mismatch")
        variables = 34_280 + 10 * len(case["omitted"])
        base_clauses = 617_382 + 50 * len(case["omitted"])
        if generate:
            with base.open("rb") as inherited, formula.open("wb") as child:
                need(inherited.readline() == f"p cnf {variables} {base_clauses}\n".encode(),
                     f"core {index}: base header mismatch")
                child.write(f"p cnf {variables} {base_clauses + 65}\n".encode())
                for line in inherited:
                    child.write(line)
                for row in rows:
                    child.write((" ".join(map(str, row)) + " 0\n").encode())
        need(file_info(formula) == results[index]["formula"], f"core {index}: child hash mismatch")
        with base.open("rb") as inherited, formula.open("rb") as child:
            need(inherited.readline() == f"p cnf {variables} {base_clauses}\n".encode(),
                 f"core {index}: base header mismatch")
            need(child.readline() == f"p cnf {variables} {base_clauses + 65}\n".encode(),
                 f"core {index}: child header mismatch")
            count = 0
            for line in inherited:
                need(child.readline() == line, f"core {index}: inherited clause changed")
                count += 1
            need(count == base_clauses, f"core {index}: inherited clause count mismatch")
            for row in rows:
                expected = (" ".join(map(str, row)) + " 0\n").encode()
                need(child.readline() == expected, f"core {index}: wrong branch tail")
            need(not child.read(), f"core {index}: extra formula content")
        entries.append({
            "index": index,
            "status": results[index]["status"],
            "base": case["formula"],
            "formula": results[index]["formula"],
            "variables": variables,
            "clauses": base_clauses + 65,
        })
    return {
        "complete_formulas_checked": len(entries),
        "entire_base_retained": True,
        "new_variables": 0,
        "lower_clauses": 21,
        "upper_clauses": 35,
        "red_fixed_units": 9,
        "case_records_sha256": object_sha256(entries),
    }


def check_proofs(source: Path, work: Path, proof_dir: Path | None) -> dict[str, object] | None:
    if proof_dir is None:
        return None
    published = {row["index"]: row for row in json.loads((source / "result.json").read_text())["cases"]}
    entries = []
    total_bytes = 0
    total_rat = 0
    for index in EXCLUDED:
        proof = proof_dir / f"c{index}.review1.drat"
        solve_log = proof_dir / f"c{index}.review1.solve.log"
        replay_log = proof_dir / f"c{index}.review1.replay.log"
        info = file_info(proof)
        need(info == published[index]["proof"], f"core {index}: proof identity mismatch")
        solve_text = solve_log.read_text(errors="replace")
        need("s UNSATISFIABLE" in solve_text and "c exit 20" in solve_text,
             f"core {index}: solver did not report UNSAT exit 20")
        replay_text = replay_log.read_text(errors="replace").replace("\r", "")
        need("s VERIFIED" in replay_text, f"core {index}: proof replay failed")
        match = re.search(r"(\d+) RAT lemmas in core", replay_text)
        need(match is not None, f"core {index}: missing RAT core count")
        rat = int(match.group(1))
        need(rat == published[index]["replay"]["rat_core_lemmas"],
             f"core {index}: RAT count mismatch")
        total_bytes += int(info["bytes"])
        total_rat += rat
        entries.append({"index": index, "proof": info, "rat_core_lemmas": rat, "verified": True})
    need(total_bytes == 346_224_849, "wrong total verified proof bytes")
    need(total_rat == 10_915, "wrong total RAT core lemmas")
    return {
        "proofs_checked": len(entries),
        "all_match_published": True,
        "total_bytes": total_bytes,
        "largest_proof_bytes": max(int(row["proof"]["bytes"]) for row in entries),
        "rat_core_lemmas": total_rat,
        "proof_records_sha256": object_sha256(entries),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--proof-dir", type=Path)
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    tools = {}
    if args.kissat is not None:
        tools["kissat"] = file_info(args.kissat)
    if args.drat_trim is not None:
        tools["drat_trim"] = file_info(args.drat_trim)
    result = {
        "all_checks_passed": True,
        "scope": "first normalized empty fixed vertex blue to exactly four blue moving triangles",
        "arithmetic": check_arithmetic(),
        "case_manifest": {"classes": 25, "labeled": 15_957, "indices": ALL_CASES},
        "formula_check": generate_and_check_formulas(args.source, args.work, args.generate),
        "branch_exclusions": EXCLUDED,
        "unresolved_branches_not_resolved_here": OPEN,
        "proof_check": check_proofs(args.source, args.work, args.proof_dir),
        "new_whole_core_exclusions": [],
        "remaining_full_classes": 25,
        "remaining_full_labeled": 15_957,
        "cumulative_counts_conditional_on_older_exclusions": True,
        "target_graph_claimed": False,
        "tools": tools,
    }
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS 25 exact formulas, blue-four arithmetic, and available proof replays")


if __name__ == "__main__":
    main()
