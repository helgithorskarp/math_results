#!/usr/bin/env python3
"""Independent formula, reduction, proof-log, and boundary check for Core159."""

from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
from itertools import combinations, product
import json
import math
from pathlib import Path
import re


BASE_INFO = {
    "bytes": 24954137,
    "sha256": "9772e64d76c977c28c2124ca2fe8a86f7f0ca91ece107a082f71c15f4ac76199",
}
FORMULA_INFO = {
    "bytes": 24954767,
    "sha256": "41e63a4cd59da7c2445025d3e00c567d8322700f5c9cc0f7b046b99f20972ff4",
}
PUBLISHED_PROOF = {
    "bytes": 21652748,
    "sha256": "7f6596418b637d855b0ff4406fcdf7ded9a44e56b736fa3a325d5fe234555653",
}
CORE_BITS = "100100110011001110"
SELECTED = [124, 155, 159, 168, 180]


class CheckError(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise CheckError(message)


def file_info(path):
    digest = sha256()
    size = 0
    with path.open("rb") as stream:
        while True:
            block = stream.read(1 << 20)
            if not block:
                break
            size += len(block)
            digest.update(block)
    return {"bytes": size, "sha256": digest.hexdigest()}


def primary_variables():
    """Recover primary edge-orbit IDs from the literal order-three action."""
    def rotate(vertex):
        if vertex >= 33:
            return vertex
        return 3 * (vertex // 3) + (vertex + 1) % 3

    remaining = set(combinations(range(43), 2))
    moving, fixed, links = [], [], []
    while remaining:
        edge = min(remaining)
        orbit = {edge}
        nxt = tuple(sorted(rotate(v) for v in edge))
        while nxt != edge:
            orbit.add(nxt)
            nxt = tuple(sorted(rotate(v) for v in nxt))
        remaining -= orbit
        representative = min(orbit)
        a, b = representative
        if a < 33 and b < 33:
            if a // 3 != b // 3:
                moving.append((representative, orbit))
        elif a >= 33:
            fixed.append((representative, orbit))
        else:
            links.append((representative, orbit))
    moving.sort(key=lambda row: (row[0][0] // 3, row[0][1] // 3,
                                 (row[0][1] - row[0][0]) % 3))
    fixed.sort()
    links.sort(key=lambda row: (row[0][1], row[0][0] // 3))
    ordered = moving + fixed + links
    need((len(moving), len(fixed), len(links), len(ordered)) == (165, 45, 110, 320),
         "primary orbit partition")
    mapping = {edge: index for index, (_, orbit) in enumerate(ordered, 1)
               for edge in orbit}
    return mapping


def tail_clauses():
    ids = primary_variables()
    moving_links = [ids[tuple(sorted((3 * cycle, 33)))] for cycle in range(4, 11)]
    need(moving_links == list(range(215, 222)), "first-fixed blue-cycle variables")
    clauses = list(combinations(moving_links, 4))
    need(len(clauses) == 35 and len(set(clauses)) == 35, "complete four-subset tail")
    return moving_links, clauses


def tail_bytes(clauses):
    return b"".join((" ".join(map(str, clause)) + " 0\n").encode() for clause in clauses)


def generate_formula(base, formula, clauses):
    need(not formula.exists(), "refusing to overwrite formula")
    with base.open("rb") as source, formula.open("xb") as output:
        need(source.readline() == b"p cnf 34300 617482\n", "base header before generation")
        output.write(b"p cnf 34300 617517\n")
        while True:
            block = source.read(1 << 20)
            if not block:
                break
            output.write(block)
        output.write(tail_bytes(clauses))


def parse_dimacs(path):
    with path.open("rb") as stream:
        header = stream.readline()
        fields = header.split()
        need(len(fields) == 4 and fields[:2] == [b"p", b"cnf"], "DIMACS header")
        variables, declared = map(int, fields[2:])
        count = max_seen = units = 0
        signs = Counter()
        for raw in stream:
            need(raw.endswith(b"\n"), "unterminated DIMACS line")
            values = list(map(int, raw.split()))
            need(values and values[-1] == 0 and 0 not in values[:-1], "DIMACS clause terminator")
            clause = values[:-1]
            need(clause, "empty input clause")
            need(len(set(clause)) == len(clause), "duplicate literal in clause")
            need(not any(-literal in clause for literal in clause), "tautological clause")
            max_seen = max(max_seen, *(abs(literal) for literal in clause))
            units += len(clause) == 1
            for literal in clause:
                signs[literal > 0] += 1
            count += 1
    need(count == declared and max_seen <= variables, "DIMACS counts")
    return {"variables": variables, "clauses": count, "max_variable": max_seen,
            "unit_clauses": units, "positive_literals": signs[True],
            "negative_literals": signs[False]}


def check_formula(base, formula, clauses):
    need(file_info(base) == BASE_INFO, "unrestricted Core159 base identity")
    need(file_info(formula) == FORMULA_INFO, "strengthened Core159 formula identity")
    with base.open("rb") as source, formula.open("rb") as child:
        need(source.readline() == b"p cnf 34300 617482\n", "base header")
        need(child.readline() == b"p cnf 34300 617517\n", "formula header")
        base_body = source.read()
        child_body = child.read()
    tail = tail_bytes(clauses)
    need(child_body == base_body + tail, "formula is not exact base plus independent tail")
    base_counts = parse_dimacs(base)
    formula_counts = parse_dimacs(formula)
    need(base_counts["variables"] == formula_counts["variables"] == 34300,
         "variable preservation")
    need(formula_counts["clauses"] - base_counts["clauses"] == 35,
         "clause increment")
    return {"base": BASE_INFO, "formula": FORMULA_INFO,
            "base_dimacs": base_counts, "formula_dimacs": formula_counts,
            "new_variables": 0, "tail_sha256": sha256(tail).hexdigest(),
            "tail_bytes": len(tail), "entire_base_preserved": True}


def check_semantics(moving_links, clauses):
    patterns = satisfying = 0
    by_red_count = Counter()
    for bits in product((False, True), repeat=7):
        assignment = dict(zip(moving_links, bits))
        holds = all(any(assignment[var] for var in clause) for clause in clauses)
        red = sum(bits)
        need(holds == (red >= 4), "tail truth-table equivalence")
        patterns += 1
        satisfying += holds
        if holds:
            by_red_count[red] += 1

    degree_pairs = []
    for blue_cycles in range(8):
        for red_fixed in range(10):
            red_degree = 3 * (7 - blue_cycles) + red_fixed
            blue_degree = 21 + 3 * blue_cycles - red_fixed
            if 18 <= red_degree <= 24 and 18 <= blue_degree <= 24:
                degree_pairs.append((blue_cycles, red_fixed, red_degree, blue_degree))
    need(max(row[0] for row in degree_pairs) == 4, "degree window must give b<=4")
    need([row for row in degree_pairs if row[0] == 4] == [(4, 9, 18, 24)],
         "maximal branch must have h=9")
    need(patterns == 128 and satisfying == 64, "moving truth-table count")
    return {"moving_link_variables": moving_links,
            "tail_clause_count": len(clauses),
            "moving_patterns": patterns,
            "satisfying_patterns": satisfying,
            "satisfying_by_red_link_count": dict(sorted(by_red_count.items())),
            "degree_valid_pairs": degree_pairs,
            "maximum_blue_cycles": 4,
            "maximal_pair": {"blue_cycles": 4, "red_fixed_neighbors": 9,
                             "red_degree": 18, "blue_degree": 24},
            "logical_bridge": "local b=4 exclusion plus full base-and-tail UNSAT excludes the whole core"}


def check_source(source):
    cases = json.loads((source / "cases.json").read_text())
    result = json.loads((source / "result.json").read_text())
    boundary = json.loads((source / "boundary.json").read_text())
    old_path = source.parent / "ramsey_r55_order3_eleven_neighborhood24" / "boundary.json"
    old = json.loads(old_path.read_text())
    need([row["index"] for row in cases] == SELECTED, "selected case list")
    case = next(row for row in cases if row["index"] == 159)
    need(case["bits"] == CORE_BITS and case["labeled"] == 324 and case["omitted"] == [0, 1],
         "Core159 identity")
    need(case["formula"] == BASE_INFO, "published base identity")
    result_case = next(row for row in result["cases"] if row["index"] == 159)
    need(result["complete"] and not result["target_graph"], "bounded result completion")
    need(result["excluded"] == [159] and result["open"] == [124, 155, 168, 180],
         "bounded result outcomes")
    need(result_case["status"] == "excluded" and result_case["formula"] == FORMULA_INFO,
         "published Core159 outcome")
    need(result_case["proof"] == PUBLISHED_PROOF and result_case["replay"]["verified"],
         "published proof record")
    expected_remaining = [index for index in old["remaining_full_cores"] if index != 159]
    need(boundary["remaining_full_cores"] == expected_remaining, "remaining core list")
    need(boundary["remaining_full_classes"] == old["remaining_full_classes"] - 1 == 17,
         "remaining class count")
    need(boundary["remaining_full_labeled"] == old["remaining_full_labeled"] - 324 == 9153,
         "remaining labeled count")
    need(boundary["cumulative_full_classes_excluded"] ==
         old["cumulative_full_classes_excluded"] + 1 == 180, "cumulative class count")
    need(boundary["cumulative_full_labeled_excluded"] ==
         old["cumulative_full_labeled_excluded"] + 324 == 106390,
         "cumulative labeled count")
    need(boundary["target_graph"] is False and boundary["new_whole_core_exclusions"] == [159],
         "boundary scope")
    need(boundary["tested_unknown"] == [124, 155, 168, 180], "UNKNOWN cases")
    return {"source_result": file_info(source / "result.json"),
            "source_boundary": file_info(source / "boundary.json"),
            "prior_boundary": file_info(old_path),
            "core_bits": CORE_BITS, "labeled_multiplicity": 324,
            "new_whole_core_exclusions": [159],
            "tested_unknown": [124, 155, 168, 180],
            "remaining_full_classes": 17, "remaining_full_labeled": 9153,
            "cumulative_excluded_classes": 180, "cumulative_excluded_labeled": 106390,
            "target_graph_claimed": False}


def check_proof(proof, replay_log, solver_log, kissat, drat_trim):
    info = file_info(proof)
    replay = replay_log.read_text(errors="replace").replace("\r", "")
    solve = solver_log.read_text(errors="replace")
    need("s VERIFIED" in replay, "proof replay not verified")
    need("s UNSATISFIABLE" in solve and "c reviewer_exit 20" in solve,
         "fresh solver outcome")
    byte_match = re.search(r"read ([0-9]+) bytes from proof file", replay)
    rat_match = re.search(r"([0-9]+) RAT lemmas in core", replay)
    need(byte_match and int(byte_match.group(1)) == info["bytes"], "replay proof byte count")
    need(rat_match, "RAT count missing")
    return {"proof": info, "matches_published_proof": info == PUBLISHED_PROOF,
            "replay_verified": True, "rat_core_lemmas": int(rat_match.group(1)),
            "solver_exit_code": 20,
            "kissat": file_info(kissat), "drat_trim": file_info(drat_trim)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--replay-log", type=Path)
    parser.add_argument("--solver-log", type=Path)
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    moving_links, clauses = tail_clauses()
    if args.generate:
        generate_formula(args.base, args.formula, clauses)
    formula = check_formula(args.base, args.formula, clauses)
    semantics = check_semantics(moving_links, clauses)
    source = check_source(args.source)
    supplied = [args.proof, args.replay_log, args.solver_log, args.kissat, args.drat_trim]
    need(all(item is not None for item in supplied) or all(item is None for item in supplied),
         "provide all proof arguments or none")
    proof = None if args.proof is None else check_proof(
        args.proof, args.replay_log, args.solver_log, args.kissat, args.drat_trim)
    report = {"all_checks_passed": True, "scope": "full Core159 after local b=4 exclusion",
              "formula_check": formula, "semantic_check": semantics,
              "source_and_boundary_check": source, "proof_check": proof}
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    status = "formula and reduction" if proof is None else "formula, reduction, and fresh proof"
    print("PASS Core159 " + status)


if __name__ == "__main__":
    main()
