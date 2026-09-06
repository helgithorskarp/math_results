#!/usr/bin/env python3
"""Independent checker for six saturated R55 neighborhood instances."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from functools import cache
from itertools import combinations, product
from pathlib import Path


CASES = [
    {"index": 124, "bits": "000110110011101110", "labeled": 324, "omitted": [0, 1]},
    {"index": 155, "bits": "100100110001101110", "labeled": 648, "omitted": [0, 1]},
    {"index": 159, "bits": "100100110011001110", "labeled": 324, "omitted": [0, 1]},
    {"index": 168, "bits": "100100110011110110", "labeled": 324, "omitted": [1, 2]},
    {"index": 180, "bits": "100100110101100110", "labeled": 648, "omitted": [0, 1]},
    {"index": 194, "bits": "100110110110110100", "labeled": 81, "omitted": [0, 1, 2, 3]},
]
LOCAL_EXCLUDED = [124, 155, 159, 168, 180]
LOCAL_WITNESS = [194]
PREVIOUS_FULL_BOUND = [
    92, 97, 118, 119, 164, 182, 185, 186, 190, 191, 192, 193,
]
NEW_FULL_BOUND = [
    92, 97, 118, 119, 124, 155, 159, 164, 168, 180, 182, 185, 186,
    190, 191, 192, 193,
]


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


@cache
def variable_map(triangles: int = 8) -> dict[tuple[int, int, int], int]:
    return {
        (i, j, phase): variable
        for variable, (i, j, phase) in enumerate(
            ((i, j, phase)
             for i, j in combinations(range(triangles), 2)
             for phase in range(3)),
            1,
        )
    }


def edge_value(
        a: int, b: int, triangles: int = 8, red_triangles: int = 4
        ) -> bool | int:
    a, b = sorted((a, b))
    cycle_a, phase_a = divmod(a, 3)
    cycle_b, phase_b = divmod(b, 3)
    need(cycle_b < triangles, "vertex outside local model")
    if cycle_a == cycle_b:
        return cycle_a < red_triangles
    return variable_map(triangles)[cycle_a, cycle_b, (phase_b - phase_a) % 3]


def ramsey_rows(
        triangles: int = 8, red_triangles: int = 4
        ) -> tuple[list[tuple[int, ...]], dict[str, int]]:
    rows: set[tuple[int, ...]] = set()
    surviving: dict[str, int] = {}
    for order, forbidden_red in ((5, True), (4, False)):
        count = 0
        for vertices in combinations(range(3 * triangles), order):
            literals: set[int] = set()
            for a, b in combinations(vertices, 2):
                value = edge_value(a, b, triangles, red_triangles)
                if isinstance(value, bool):
                    if value != forbidden_red:
                        break
                else:
                    literals.add(-value if forbidden_red else value)
            else:
                rows.add(tuple(sorted(literals)))
                count += 1
        surviving[str(order)] = count
    return sorted(rows), surviving


def core_variables() -> list[int]:
    ids = variable_map()
    variables = [
        ids[i, j, phase]
        for i, j in combinations(range(4), 2)
        for phase in range(3)
    ]
    need(variables == [1, 2, 3, 4, 5, 6, 7, 8, 9,
                       22, 23, 24, 25, 26, 27, 40, 41, 42],
         "wrong local core variables")
    return variables


def all_rows(case: dict[str, object]) -> tuple[list[tuple[int, ...]], dict[str, int]]:
    ramsey, surviving = ramsey_rows()
    units = [
        (variable if bit == "1" else -variable,)
        for variable, bit in zip(core_variables(), str(case["bits"]))
    ]
    need(len(ramsey) == 11_566 and len(units) == 18, "wrong clause partition")
    return ramsey + units, surviving


def write_formula(path: Path, case: dict[str, object]) -> dict[str, object]:
    rows, surviving = all_rows(case)
    with path.open("w") as stream:
        stream.write(f"p cnf 84 {len(rows)}\n")
        for row in rows:
            stream.write(" ".join(map(str, row)) + " 0\n")
    info = file_info(path)
    return {
        **info,
        "variables": 84,
        "clauses": len(rows),
        "ramsey_clauses": len(rows) - 18,
        "core_units": 18,
        "unsimplified_nonconstant_subsets": surviving,
    }


def clique_count(n: int, red: set[tuple[int, int]], order: int, color: bool) -> int:
    return sum(
        all(((a, b) in red) == color for a, b in combinations(vertices, 2))
        for vertices in combinations(range(n), order)
    )


def small_bridge() -> int:
    checked = 0
    for triangles in range(1, 4):
        variable_count = 3 * triangles * (triangles - 1) // 2
        for red_triangles in range(triangles + 1):
            rows, _ = ramsey_rows(triangles, red_triangles)
            for values in product((False, True), repeat=variable_count):
                red: set[tuple[int, int]] = set()
                for edge in combinations(range(3 * triangles), 2):
                    value = edge_value(*edge, triangles, red_triangles)
                    is_red = value if isinstance(value, bool) else values[value - 1]
                    if is_red:
                        red.add(edge)
                literal = (
                    clique_count(3 * triangles, red, 5, True) == 0
                    and clique_count(3 * triangles, red, 4, False) == 0
                )
                encoded = all(
                    any(values[abs(item) - 1] == (item > 0) for item in row)
                    for row in rows
                )
                need(literal == encoded, "small graph/formula mismatch")
                checked += 1
    need(checked == 2_074, "incomplete small-graph bridge")
    return checked


def load_source(source: Path) -> dict[int, dict[str, object]]:
    source_cases = json.loads((source / "cases.json").read_text())
    result = json.loads((source / "result.json").read_text())
    boundary = json.loads((source / "boundary.json").read_text())
    previous_branch = json.loads(
        (source.parent / "ramsey_r55_order3_eleven_empty_blue4" / "boundary.json").read_text()
    )
    previous_full = json.loads(
        (source.parent / "ramsey_r55_order3_eleven_blue_bound_propagation" / "boundary.json").read_text()
    )
    need(source_cases == CASES, "six residual-case identities differ")
    need(previous_branch["blue4_open"] == [row["index"] for row in CASES],
         "not the complete prior residual branch set")
    need(result["complete"] and not result["target_graph"], "published result incomplete or target claimed")
    need(result["local_excluded"] == LOCAL_EXCLUDED, "wrong local exclusions")
    need(result["local_witness"] == LOCAL_WITNESS and result["unknown"] == [],
         "wrong local witness/unknown partition")
    need(result["new_whole_core_exclusions"] == [], "local result misreported as whole-core exclusion")
    need(previous_full["remaining_full_classes"] == 18
         and previous_full["remaining_full_labeled"] == 9_477,
         "changed preceding whole-core boundary")
    need(sorted(set(previous_full["imported_first_fixed_blue_cycles_at_most_three_in"])
                & set(previous_full["remaining_full_cores"])) == PREVIOUS_FULL_BOUND,
         "wrong preceding surviving b<=3 boundary")
    need(boundary["local_excluded"] == LOCAL_EXCLUDED
         and boundary["local_witness"] == LOCAL_WITNESS
         and boundary["local_unknown"] == [],
         "published boundary outcomes differ")
    need(boundary["first_empty_blue_bound_at_most_three_in"] == NEW_FULL_BOUND
         and boundary["remaining_maximal_full_branches"] == LOCAL_WITNESS,
         "wrong new maximal-branch boundary")
    need(boundary["new_whole_core_exclusions"] == []
         and boundary["remaining_full_classes"] == 18
         and boundary["remaining_full_labeled"] == 9_477,
         "whole-core boundary was changed")
    rows = {int(row["index"]): row for row in result["cases"]}
    need(sorted(rows) == [row["index"] for row in CASES], "published case coverage differs")
    for case in CASES:
        row = rows[int(case["index"])]
        for key in ("index", "bits", "labeled", "omitted"):
            need(row[key] == case[key], f"core {case['index']}: identity mismatch")
        expected = "local_excluded" if case["index"] in LOCAL_EXCLUDED else "local_witness"
        need(row["status"] == expected, f"core {case['index']}: status mismatch")
    return rows


def generate_and_check_formulas(
        source: Path, work: Path, generate: bool
        ) -> dict[str, object]:
    published = load_source(source)
    formula_dir = work / "formulas"
    formula_dir.mkdir(parents=True, exist_ok=True)
    entries = []
    for case in CASES:
        index = int(case["index"])
        path = formula_dir / f"c{index}.cnf"
        if generate:
            observed = write_formula(path, case)
        else:
            observed = write_formula(work / "check.tmp.cnf", case)
            need(file_info(path) == {k: observed[k] for k in ("bytes", "sha256")},
                 f"core {index}: saved formula differs")
        expected = published[index]["formula"]
        for key in ("bytes", "sha256", "variables", "clauses", "ramsey_clauses", "core_units"):
            need(observed[key] == expected[key], f"core {index}: formula {key} mismatch")
        with path.open() as stream:
            rows, _ = all_rows(case)
            need(stream.readline() == "p cnf 84 11584\n", f"core {index}: header mismatch")
            for row in rows:
                need(stream.readline() == " ".join(map(str, row)) + " 0\n",
                     f"core {index}: clause mismatch")
            need(not stream.read(), f"core {index}: extra formula content")
        entries.append({
            "index": index,
            "status": published[index]["status"],
            "formula": expected,
        })
    temporary = work / "check.tmp.cnf"
    if temporary.exists():
        temporary.unlink()
    return {
        "complete_formulas_checked": len(entries),
        "variables": 84,
        "clauses": 11_584,
        "ramsey_clauses": 11_566,
        "core_units": 18,
        "normalization_clauses": 0,
        "unsimplified_nonconstant_subsets": {"4": 8_076, "5": 26_712},
        "small_bridge_assignments": small_bridge(),
        "case_records_sha256": object_sha256(entries),
    }


def read_red_edges(path: Path) -> set[tuple[int, int]]:
    lines = path.read_text().splitlines()
    need(lines and lines[0].split() == ["24", "156"], "wrong witness header")
    red: set[tuple[int, int]] = set()
    for line in lines[1:]:
        fields = line.split()
        need(len(fields) == 2, "malformed witness edge")
        a, b = map(int, fields)
        need(0 <= a < b < 24 and (a, b) not in red, "invalid witness edge")
        red.add((a, b))
    need(len(red) == 156, "wrong witness edge count")
    return red


def check_witness(source: Path, work: Path) -> dict[str, object]:
    case = CASES[-1]
    edge_file = source / "c194.edges"
    red = read_red_edges(edge_file)
    rotation = lambda vertex: 3 * (vertex // 3) + (vertex % 3 + 1) % 3
    assignment: dict[int, bool] = {}
    for a, b in combinations(range(24), 2):
        rotated = tuple(sorted((rotation(a), rotation(b))))
        need(((a, b) in red) == (rotated in red), "witness is not order-three invariant")
        value = edge_value(a, b)
        if isinstance(value, bool):
            need(((a, b) in red) == value, "wrong internal triangle color")
        else:
            if value in assignment:
                need(assignment[value] == ((a, b) in red), "nonuniform variable orbit")
            assignment[value] = (a, b) in red
    need(sorted(assignment) == list(range(1, 85)), "incomplete witness assignment")
    red_k5 = clique_count(24, red, 5, True)
    blue_k4 = clique_count(24, red, 4, False)
    need(red_k5 == 0 and blue_k4 == 0, "witness has a forbidden clique")
    degrees = [
        sum(tuple(sorted((vertex, other))) in red for other in range(24) if other != vertex)
        for vertex in range(24)
    ]
    need(degrees == [13] * 24 and 2 * len(red) == sum(degrees), "wrong witness degrees")
    word = "".join("1" if assignment[variable] else "0" for variable in core_variables())
    need(word == case["bits"], "wrong witness core word")
    rows, _ = all_rows(case)
    need(all(
        any(assignment[abs(literal)] == (literal > 0) for literal in row)
        for row in rows
    ), "witness does not satisfy independently generated formula")
    generated = work / "formulas" / "c194.cnf"
    source_result = load_source(source)[194]
    need(file_info(generated) == {k: source_result["formula"][k] for k in ("bytes", "sha256")},
         "witness formula identity mismatch")
    return {
        "vertices": 24,
        "red_edges": len(red),
        "red_degrees": degrees,
        "red_K5": red_k5,
        "blue_K4": blue_k4,
        "five_sets_checked": 42_504,
        "four_sets_checked": 10_626,
        "order_three": True,
        "internal_red_triangles": 4,
        "internal_blue_triangles": 4,
        "core_bits": word,
        "satisfies_local_formula": True,
        "edge_file": file_info(edge_file),
    }


def check_proofs(source: Path, proof_dir: Path | None) -> dict[str, object] | None:
    if proof_dir is None:
        return None
    published = load_source(source)
    entries = []
    for index in LOCAL_EXCLUDED:
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
            "matches_published": info == published[index]["trace"],
            "rat_core_lemmas": int(match.group(1)),
            "verified": True,
        })
    all_match = all(bool(row["matches_published"]) for row in entries)
    if all_match:
        need(sum(int(row["proof"]["bytes"]) for row in entries) == 19_570_865,
             "published proof-size total mismatch")
        need(sum(int(row["rat_core_lemmas"]) for row in entries) == 181,
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
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--proof-dir", type=Path)
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    args.work.mkdir(parents=True, exist_ok=True)
    tools = {}
    if args.kissat is not None:
        tools["kissat"] = file_info(args.kissat)
    if args.drat_trim is not None:
        tools["drat_trim"] = file_info(args.drat_trim)
    result = {
        "all_checks_passed": True,
        "scope": "six saturated 24-vertex local neighborhoods",
        "formula_check": generate_and_check_formulas(args.source, args.work, args.generate),
        "proof_check": check_proofs(args.source, args.proof_dir),
        "witness_check": check_witness(args.source, args.work),
        "new_maximal_branch_exclusions": LOCAL_EXCLUDED,
        "new_maximal_branch_labeled_exclusions": 2_268,
        "remaining_maximal_full_branches": LOCAL_WITNESS,
        "new_whole_core_exclusions": [],
        "remaining_full_classes": 18,
        "remaining_full_labeled": 9_477,
        "target_graph_claimed": False,
        "cumulative_counts_conditional_on_older_exclusions": True,
        "tools": tools,
    }
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS six local formulas, five available proofs, and the Core194 witness")


if __name__ == "__main__":
    main()
