#!/usr/bin/env python3
"""Independent checker for the nineteen R55 complementary full formulas."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from itertools import combinations, product
from pathlib import Path


ALL_CURRENT = [
    92, 97, 109, 114, 118, 119, 122, 124, 154, 155, 159, 164, 167,
    168, 177, 180, 182, 185, 186, 188, 190, 191, 192, 193, 194,
]
TESTED = [
    92, 97, 109, 114, 118, 119, 122, 154, 164, 167, 177, 182, 185,
    186, 188, 190, 191, 192, 193,
]
EXCLUDED = [109, 114, 122, 154, 167, 177, 188]
UNKNOWN = [92, 97, 118, 119, 164, 182, 185, 186, 190, 191, 192, 193]
UNTESTED = [124, 155, 159, 168, 180, 194]


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
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


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
    need(len(ordered) == 320, "wrong primary-orbit count")
    ids = {
        edge: variable
        for variable, (_, orbit) in enumerate(ordered, 1)
        for edge in orbit
    }
    for fixed_vertex in range(33, 43):
        for cycle in range(11):
            expected = 211 + 11 * (fixed_vertex - 33) + cycle
            need(ids[tuple(sorted((3 * cycle, fixed_vertex)))] == expected,
                 "fixed-moving variable convention mismatch")
    need([ids[(33, vertex)] for vertex in range(34, 43)] == list(range(166, 175)),
         "first-fixed edge block mismatch")
    return ids


def tail_rows() -> list[tuple[int, ...]]:
    ids = primary_variables()
    links = [ids[(3 * cycle, 33)] for cycle in range(4, 11)]
    need(links == list(range(215, 222)), "blue-triangle link block mismatch")
    rows = list(combinations(links, 4))
    need(len(rows) == 35 and len(set(rows)) == 35, "wrong complementary tail")
    need(not any(166 <= literal <= 174 for row in rows for literal in row),
         "fixed edge leaked into tail")
    return rows


def check_arithmetic() -> dict[str, object]:
    rows = tail_rows()
    accepted = 0
    incidence_assignments = 0
    degree_valid = 0
    complementary = 0
    maximal = 0
    histogram: dict[int, int] = {}
    for moving in product((False, True), repeat=7):
        assignment = dict(zip(range(215, 222), moving))
        holds = all(any(assignment[literal] for literal in row) for row in rows)
        need(holds == (sum(moving) >= 4), "tail is not at least four red links")
        accepted += int(holds)
        for fixed in product((False, True), repeat=9):
            incidence_assignments += 1
            red_degree = 3 * sum(moving) + sum(fixed)
            blue_degree = 42 - red_degree
            blue_cycles = 7 - sum(moving)
            if 18 <= red_degree <= 24 and 18 <= blue_degree <= 24:
                degree_valid += 1
                histogram[blue_cycles] = histogram.get(blue_cycles, 0) + 1
                need(blue_cycles <= 4, "degree-valid assignment has b>4")
                if blue_cycles == 4:
                    need(all(fixed), "b=4 does not force all fixed edges red")
                    need((red_degree, blue_degree) == (18, 24), "wrong b=4 degrees")
                    maximal += 1
                if blue_cycles <= 3:
                    need(holds, "legal complementary assignment rejected")
                    complementary += 1
    need(accepted == 64, "wrong number of moving patterns")
    need(incidence_assignments == 65_536, "incomplete incidence truth table")
    need(degree_valid == 17_763 and maximal == 35 and complementary == 17_728,
         "wrong degree-window partition")
    return {
        "moving_assignments": 128,
        "tail_satisfying_patterns": accepted,
        "moving_fixed_assignments": incidence_assignments,
        "degree_valid_assignments": degree_valid,
        "degree_valid_blue_cycle_histogram": {
            str(key): histogram[key] for key in sorted(histogram)
        },
        "maximal_b4_assignments": maximal,
        "complementary_degree_valid_assignments": complementary,
    }


def load_manifests(source: Path) -> tuple[
        list[dict[str, object]], dict[int, dict[str, object]], dict[int, dict[str, object]]]:
    cases = json.loads((source / "cases.json").read_text())
    result = json.loads((source / "result.json").read_text())
    boundary = json.loads((source / "boundary.json").read_text())
    base_result = json.loads(
        (source.parent / "ramsey_r55_order3_eleven_empty_propagation" / "result.json").read_text()
    )
    branch_result = json.loads(
        (source.parent / "ramsey_r55_order3_eleven_empty_blue4" / "result.json").read_text()
    )
    need([case["index"] for case in cases] == TESTED, "wrong 19-case manifest")
    need(sum(int(case["labeled"]) for case in cases) == 13_608, "wrong tested multiplicity")
    need(branch_result["excluded"] == TESTED, "imported branch coverage mismatch")
    need(result["complete"] and not result["target_graph"], "published run incomplete or target claimed")
    need(result["excluded"] == EXCLUDED and result["open"] == UNKNOWN,
         "published decision partition mismatch")
    need(boundary["new_whole_core_exclusions"] == EXCLUDED, "boundary exclusion mismatch")
    need(boundary["tested_unknown"] == UNKNOWN and boundary["untested"] == UNTESTED,
         "boundary unresolved partition mismatch")
    base_rows = {row["index"]: row for row in base_result["cases"] if row["status"] == "open"}
    need(sorted(base_rows) == ALL_CURRENT, "unrestricted 25-core base boundary mismatch")
    branch_rows = {row["index"]: row for row in branch_result["cases"]}
    published_rows = {row["index"]: row for row in result["cases"]}
    need(sorted(published_rows) == TESTED, "published result lacks a tested case")
    for case in cases:
        index = int(case["index"])
        base = base_rows[index]
        published = published_rows[index]
        branch = branch_rows[index]
        for key in ("index", "bits", "labeled", "omitted", "formula"):
            need(case[key] == base[key], f"core {index}: unrestricted case mismatch")
        need(published["base"] == case["formula"], f"core {index}: wrong starting base")
        need(published["base"] == branch["base"], f"core {index}: branch base mismatch")
        need(published["base"] != branch["formula"], f"core {index}: contaminated branch child")
        expected_status = "excluded" if index in EXCLUDED else "open"
        need(published["status"] == expected_status, f"core {index}: status mismatch")
    return cases, published_rows, base_rows


def generate_and_check_formulas(
        source: Path, base_dir: Path, work: Path, generate: bool) -> dict[str, object]:
    cases, published_rows, _ = load_manifests(source)
    rows = tail_rows()
    formula_dir = work / "formulas"
    formula_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for case in cases:
        index = int(case["index"])
        base = base_dir / f"c{index}.cnf"
        child = formula_dir / f"c{index}.cnf"
        need(file_info(base) == case["formula"], f"core {index}: base hash mismatch")
        with base.open("rb") as inherited:
            header = inherited.readline().split()
        need(len(header) == 4 and header[:2] == [b"p", b"cnf"],
             f"core {index}: malformed base header")
        variables, base_clauses = map(int, header[2:])
        if generate:
            with base.open("rb") as inherited, child.open("wb") as output:
                need(inherited.readline() == b" ".join(header) + b"\n",
                     f"core {index}: noncanonical base header")
                output.write(f"p cnf {variables} {base_clauses + 35}\n".encode())
                for line in inherited:
                    output.write(line)
                for row in rows:
                    output.write((" ".join(map(str, row)) + " 0\n").encode())
        expected_formula = published_rows[index]["formula"]
        need(file_info(child) == expected_formula, f"core {index}: child hash mismatch")
        with base.open("rb") as inherited, child.open("rb") as formula:
            inherited.readline()
            need(formula.readline() == f"p cnf {variables} {base_clauses + 35}\n".encode(),
                 f"core {index}: wrong child header")
            count = 0
            for line in inherited:
                need(formula.readline() == line, f"core {index}: changed base clause")
                count += 1
            need(count == base_clauses, f"core {index}: base clause count mismatch")
            for row in rows:
                need(formula.readline() == (" ".join(map(str, row)) + " 0\n").encode(),
                     f"core {index}: wrong tail")
            need(not formula.read(), f"core {index}: extra formula content")
        entries.append({
            "index": index,
            "status": published_rows[index]["status"],
            "base": case["formula"],
            "formula": expected_formula,
            "variables": variables,
            "clauses": base_clauses + 35,
        })
    return {
        "complete_formulas_checked": len(entries),
        "entire_unrestricted_base_retained": True,
        "new_variables": 0,
        "positive_four_subset_clauses": 35,
        "added_fixed_edge_units": 0,
        "case_records_sha256": object_sha256(entries),
    }


def check_bookkeeping(source: Path) -> dict[str, object]:
    _, _, base_rows = load_manifests(source)
    removed = [base_rows[index] for index in EXCLUDED]
    remaining = [base_rows[index] for index in ALL_CURRENT if index not in EXCLUDED]
    remaining_ids = [int(row["index"]) for row in remaining]
    removed_labels = sum(int(row["labeled"]) for row in removed)
    remaining_labels = sum(int(row["labeled"]) for row in remaining)
    need(removed_labels == 6_480, "wrong newly excluded multiplicity")
    need(remaining_ids == [92, 97, 118, 119, 124, 155, 159, 164, 168, 180,
                           182, 185, 186, 190, 191, 192, 193, 194],
         "wrong residual core list")
    need(remaining_labels == 9_477, "wrong residual multiplicity")
    need(197 - len(remaining) == 179 and 115_543 - remaining_labels == 106_066,
         "wrong conditional cumulative totals")
    return {
        "new_whole_core_exclusions": EXCLUDED,
        "new_labeled_exclusions": removed_labels,
        "remaining_full_classes": len(remaining),
        "remaining_full_labeled": remaining_labels,
        "remaining_full_cores": remaining_ids,
        "cumulative_classes_excluded_conditional": 179,
        "cumulative_labeled_excluded_conditional": 106_066,
    }


def check_proofs(source: Path, proof_dir: Path | None) -> dict[str, object] | None:
    if proof_dir is None:
        return None
    published = {
        row["index"]: row for row in json.loads((source / "result.json").read_text())["cases"]
    }
    entries = []
    for index in EXCLUDED:
        proof = proof_dir / f"c{index}.review1.drat"
        solve_log = proof_dir / f"c{index}.review1.solve.log"
        replay_log = proof_dir / f"c{index}.review1.replay.log"
        info = file_info(proof)
        solve_text = solve_log.read_text(errors="replace").replace("\r", "")
        need("s UNSATISFIABLE" in solve_text and "c reviewer_exit 20" in solve_text,
             f"core {index}: missing fresh UNSAT exit")
        replay_text = replay_log.read_text(errors="replace").replace("\r", "")
        need("s VERIFIED" in replay_text, f"core {index}: fresh replay failed")
        match = re.search(r"(\d+) RAT lemmas in core", replay_text)
        need(match is not None, f"core {index}: missing RAT-core count")
        entries.append({
            "index": index,
            "proof": info,
            "matches_published": info == published[index]["proof"],
            "rat_core_lemmas": int(match.group(1)),
            "verified": True,
        })
    all_match = all(bool(row["matches_published"]) for row in entries)
    if all_match:
        need(sum(int(row["proof"]["bytes"]) for row in entries) == 153_723_022,
             "published-size total mismatch")
        need(sum(int(row["rat_core_lemmas"]) for row in entries) == 5_580,
             "published RAT-core total mismatch")
    return {
        "proofs_checked": len(entries),
        "all_match_published": all_match,
        "total_bytes": sum(int(row["proof"]["bytes"]) for row in entries),
        "largest_proof_bytes": max(int(row["proof"]["bytes"]) for row in entries),
        "rat_core_lemmas": sum(int(row["rat_core_lemmas"]) for row in entries),
        "proof_records_sha256": object_sha256(entries),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--base-dir", type=Path, required=True)
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
        "scope": "nineteen unrestricted full extensions after imported b=4 closure",
        "arithmetic": check_arithmetic(),
        "formula_check": generate_and_check_formulas(
            args.source, args.base_dir, args.work, args.generate
        ),
        "proof_check": check_proofs(args.source, args.proof_dir),
        "bookkeeping": check_bookkeeping(args.source),
        "tested_unknown_not_resolved_here": UNKNOWN,
        "untested_no_imported_bound": UNTESTED,
        "target_graph_claimed": False,
        "cumulative_counts_conditional_on_older_exclusions": True,
        "tools": tools,
    }
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS 19 exact complementary formulas, arithmetic, bookkeeping, and available proofs")


if __name__ == "__main__":
    main()
