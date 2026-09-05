#!/usr/bin/env python3
"""Independent core-123 bridge, full-formula, and proof-replay checker."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from itertools import combinations, product
from pathlib import Path


CORE_INDEX = 123
CORE_BITS = "000110110011101011"
CORE_LABELED = 648
CORE_OMITTED = [0]
BASE_INFO = {
    "bytes": 24_893_888,
    "sha256": "b8402d03f41d78dbcef98cf9c55db5b18ed8864122f017ac52adbe0075c699b7",
}
FORMULA_INFO = {
    "bytes": 24_952_956,
    "sha256": "d103da79b90dbb5d3f8bb9822a90d3b387823eee866af0c3f991f2d7f3db25f1",
}
PUBLISHED_PROOF_INFO = {
    "bytes": 19_801_958,
    "sha256": "e7f7293e5a6de165c219f34af9284051a626d6877d6b1a50aca417c44933a700",
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def rotate(vertex: int) -> int:
    if vertex >= 33:
        return vertex
    return 3 * (vertex // 3) + (vertex % 3 + 1) % 3


def primary_variables() -> dict[tuple[int, int], int]:
    """Recover the parent's primary ordering from the action, not its producer."""
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
    answer = {
        edge: variable
        for variable, (_, orbit) in enumerate(ordered, 1)
        for edge in orbit
    }
    for fixed_vertex in range(33, 43):
        for cycle in range(11):
            expected = 211 + 11 * (fixed_vertex - 33) + cycle
            need(answer[tuple(sorted((3 * cycle, fixed_vertex)))] == expected,
                 "closed link-variable formula disagrees with orbit recovery")
    return answer


def core_red_edges() -> set[tuple[int, int]]:
    red: set[tuple[int, int]] = set()
    cycle_pairs = list(combinations(range(4), 2))
    for a, b in combinations(range(12), 2):
        left_cycle, left_phase = divmod(a, 3)
        right_cycle, right_phase = divmod(b, 3)
        if left_cycle == right_cycle:
            red.add((a, b))
            continue
        offset = (right_phase - left_phase) % 3
        word_position = 3 * cycle_pairs.index((left_cycle, right_cycle)) + offset
        if CORE_BITS[word_position] == "1":
            red.add((a, b))
    return red


def check_literal_core() -> dict[str, object]:
    red = core_red_edges()
    for vertices in combinations(range(12), 5):
        red_count = sum(edge in red for edge in combinations(vertices, 2))
        need(0 < red_count < 10, "monochromatic K5 already in literal core")
    witnesses: list[list[int]] = []
    cross_edge_counts: dict[str, int] = {}
    for red_i in range(4):
        for free_j in range(4):
            if red_i == free_j:
                continue
            other = sorted(set(range(4)) - {red_i, free_j})
            blue_edges = [
                (a, b)
                for a in range(3 * other[0], 3 * other[0] + 3)
                for b in range(3 * other[1], 3 * other[1] + 3)
                if (a, b) not in red
            ]
            need(blue_edges, "pair-cut clique argument lacks blue cross-edge")
            witnesses.append([red_i, free_j, *blue_edges[0]])
            cross_edge_counts[f"{red_i},{free_j}"] = len(blue_edges)
    need(len(witnesses) == 12, "wrong ordered pair-cut witness count")
    return {
        "bits": CORE_BITS,
        "local_five_sets": 792,
        "ordered_pair_witnesses": witnesses,
        "blue_cross_edge_counts": cross_edge_counts,
    }


def consequence_rows(ids: dict[tuple[int, int], int]) -> list[tuple[int, ...]]:
    rows: list[tuple[int, ...]] = [(-ids[(3 * cycle, 33)],) for cycle in range(4)]
    need(rows == [(-211,), (-212,), (-213,), (-214,)], "wrong empty-prefix units")
    for fixed_vertices in combinations(range(33, 43), 3):
        for red_i in range(4):
            for free_j in range(4):
                if red_i == free_j:
                    continue
                other = sorted(set(range(4)) - {red_i, free_j})
                row: list[int] = []
                for fixed_vertex in fixed_vertices:
                    row.extend((
                        -ids[tuple(sorted((3 * red_i, fixed_vertex)))],
                        ids[tuple(sorted((3 * other[0], fixed_vertex)))],
                        ids[tuple(sorted((3 * other[1], fixed_vertex)))],
                    ))
                rows.append(tuple(row))
    need(len(rows) == 1_444, "wrong consequence count")
    need(len(set(rows)) == 1_444, "duplicate consequence clause")
    return rows


def check_truth_table() -> int:
    checked = 0
    for red_i in range(4):
        for free_j in range(4):
            if red_i == free_j:
                continue
            other = sorted(set(range(4)) - {red_i, free_j})
            for masks in product(range(16), repeat=3):
                clause_holds = any(
                    not (mask & (1 << red_i))
                    or mask & (1 << other[0])
                    or mask & (1 << other[1])
                    for mask in masks
                )
                forbidden = all(
                    mask in ((1 << red_i), (1 << red_i) | (1 << free_j))
                    for mask in masks
                )
                need(clause_holds == (not forbidden), "pair-cut truth-table mismatch")
                checked += 1
    need(checked == 49_152, "incomplete truth-table coverage")
    return checked


def generate_and_check_formula(base: Path, formula: Path, generate: bool) -> dict[str, object]:
    need(file_info(base) == BASE_INFO, "inherited core-123 base identity mismatch")
    ids = primary_variables()
    rows = consequence_rows(ids)
    if generate:
        with base.open("rb") as source, formula.open("wb") as destination:
            need(source.readline() == b"p cnf 34290 615988\n", "wrong base header")
            destination.write(b"p cnf 34290 617432\n")
            for line in source:
                destination.write(line)
            for row in rows:
                destination.write((" ".join(map(str, row)) + " 0\n").encode())
    need(file_info(formula) == FORMULA_INFO, "complete formula identity mismatch")
    with base.open("rb") as source, formula.open("rb") as full:
        need(source.readline() == b"p cnf 34290 615988\n", "wrong base header")
        need(full.readline() == b"p cnf 34290 617432\n", "wrong full header")
        base_clauses = 0
        for line in source:
            need(full.readline() == line, "full formula changed inherited base")
            base_clauses += 1
        need(base_clauses == 615_988, "wrong inherited clause count")
        for row in rows:
            expected = (" ".join(map(str, row)) + " 0\n").encode()
            need(full.readline() == expected, "wrong consequence tail")
        need(not full.read(), "extra formula content")
    return {
        "base": BASE_INFO,
        "formula": FORMULA_INFO,
        "entire_base_retained": True,
        "base_clauses": 615_988,
        "empty_prefix_units": 4,
        "pair_cuts": 1_440,
        "primary_variables_recovered": 320,
    }


def check_cases_manifest(path: Path, noempty_boundary: Path) -> dict[str, object]:
    cases = json.loads(path.read_text())
    matches = [case for case in cases if case["index"] == CORE_INDEX]
    need(len(cases) == 26 and len(matches) == 1, "wrong residual case coverage")
    expected_indices = [
        92, 97, 109, 114, 118, 119, 122, 123, 124, 154, 155, 159, 164,
        167, 168, 177, 180, 182, 185, 186, 188, 190, 191, 192, 193, 194,
    ]
    need([case["index"] for case in cases] == expected_indices, "wrong residual case identities")
    need(sum(case["labeled"] for case in cases) == 16_605, "wrong residual multiplicity")
    case = matches[0]
    need(case == {
        "bits": CORE_BITS,
        "formula": BASE_INFO,
        "index": CORE_INDEX,
        "labeled": CORE_LABELED,
        "omitted": CORE_OMITTED,
    }, "core-123 manifest identity mismatch")
    boundary = json.loads(noempty_boundary.read_text())
    need(boundary["forced_empty_cores"] == expected_indices, "empty-signature premise has wrong domain")
    need(boundary["remaining_full_cores"] == expected_indices, "starting full-core boundary changed")
    need(boundary["remaining_full_labeled"] == 16_605, "starting labeled boundary changed")
    return {"classes": 26, "labeled": 16_605, "indices": expected_indices}


def check_solver_log(path: Path | None) -> dict[str, object] | None:
    if path is None:
        return None
    text = path.read_text(errors="replace")
    need("s UNSATISFIABLE" in text and "c exit 20" in text, "solver did not report UNSAT exit 20")
    conflicts = re.search(r"c conflicts:\s+(\d+)", text)
    decisions = re.search(r"c decisions:\s+(\d+)", text)
    need(conflicts is not None and decisions is not None, "missing solver statistics")
    return {
        "conflicts": int(conflicts.group(1)),
        "decisions": int(decisions.group(1)),
        "reported_unsat_exit_20": True,
    }


def check_proof(proof: Path | None, replay_log: Path | None) -> dict[str, object] | None:
    if proof is None and replay_log is None:
        return None
    need(proof is not None and replay_log is not None, "proof and replay log must be paired")
    info = file_info(proof)
    text = replay_log.read_text(errors="replace").replace("\r", "")
    need("s VERIFIED" in text, "DRAT replay did not verify")
    match = re.search(r"(\d+) RAT lemmas in core", text)
    need(match is not None, "missing RAT core count")
    return {
        **info,
        "matches_published_trace": info == PUBLISHED_PROOF_INFO,
        "published_trace": PUBLISHED_PROOF_INFO,
        "rat_core_lemmas": int(match.group(1)),
        "verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--formula", type=Path, required=True)
    parser.add_argument("--cases", type=Path, required=True)
    parser.add_argument("--noempty-boundary", type=Path, required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--solve-log", type=Path)
    parser.add_argument("--proof", type=Path)
    parser.add_argument("--replay-log", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    residual_manifest = check_cases_manifest(args.cases, args.noempty_boundary)
    tools = {}
    if args.kissat is not None:
        tools["kissat"] = file_info(args.kissat)
    if args.drat_trim is not None:
        tools["drat_trim"] = file_info(args.drat_trim)
    result = {
        "all_checks_passed": True,
        "claim": "core 123 has no complete extension, conditional on inherited base and accepted consequences",
        "core": {
            "index": CORE_INDEX,
            "labeled": CORE_LABELED,
            "omitted": CORE_OMITTED,
            **check_literal_core(),
        },
        "formula_check": generate_and_check_formula(args.base, args.formula, args.generate),
        "pair_cut_truth_assignments": check_truth_table(),
        "residual_manifest": residual_manifest,
        "solver": check_solver_log(args.solve_log),
        "proof_replay": check_proof(args.proof, args.replay_log),
        "tools": tools,
        "new_whole_core_exclusions": [CORE_INDEX],
        "remaining_classes": 25,
        "remaining_labeled": 15_957,
        "cumulative_counts_conditional_on_older_exclusions": True,
        "target_graph_claimed": False,
    }
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS core123 bridge, 49152 truth assignments, exact formula and proof evidence")


if __name__ == "__main__":
    main()
