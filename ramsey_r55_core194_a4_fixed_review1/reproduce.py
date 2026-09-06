#!/usr/bin/env python3
"""Independent cover, physical normalization, child construction, and DRAT replay."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import re
import subprocess
import sys
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "ramsey_r55_order3_eleven_core194_a4_fixed"
DIRECT = ROOT / "ramsey_r55_order3_eleven_core194_direct"
MOVING = (4, 1, 2)
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


def variable(a: int, b: int) -> int:
    """Physical primary numbering of the independently accepted direct base."""
    require(0 <= a < b < 43, "physical pair")
    if b < 33:
        i, phase_a = divmod(a, 3)
        j, phase_b = divmod(b, 3)
        if i == j:
            return 321 if i < 4 else -321
        rank = i * (21 - i) // 2 + j - i - 1
        return 1 + 3 * rank + (phase_b - phase_a) % 3
    if a >= 33:
        i, j = a - 33, b - 33
        return 166 + i * (19 - i) // 2 + j - i - 1
    return 211 + 11 * (b - 33) + a // 3


def contact_units(fixed: tuple[int, int, int]) -> list[int]:
    units: list[int] = []
    moving_contacts = [kind for kind, count in enumerate(MOVING) for _ in range(count)]
    for cycle, contact in enumerate(moving_contacts, start=4):
        u_var = 211 + cycle
        v_var = 222 + cycle
        units.extend((u_var if contact != 2 else -u_var,
                      v_var if contact != 1 else -v_var))

    fixed_contacts = [kind for kind, count in enumerate(fixed) for _ in range(count)]
    require(len(fixed_contacts) == 8, "eight other fixed vertices")
    for offset, contact in enumerate(fixed_contacts):
        u_var = 167 + offset
        v_var = 175 + offset
        units.extend((u_var if contact != 2 else -u_var,
                      v_var if contact != 1 else -v_var))
    require(len(units) == 30 and len({abs(unit) for unit in units}) == 30,
            "thirty distinct physical contact units")
    return units


def case_id(fixed: tuple[int, int, int]) -> str:
    return "a4_b1_c2_x%d_y%d_z%d" % fixed


def multinomial8(fixed: tuple[int, int, int]) -> int:
    x, y, z = fixed
    return math.comb(8, x) * math.comb(8 - x, y) * math.comb(z, z)


def read_census(path: Path) -> dict:
    summary: dict[str, int] | None = None
    rows = []
    for line in path.read_text().splitlines():
        fields = line.split()
        require(fields, "blank census line")
        if fields[0] == "summary":
            require(len(fields) == 11 and fields[1::2] ==
                    ["total", "allowed", "profiles", "permutations", "labeled"],
                    "malformed census summary")
            summary = {
                "fixed_words": int(fields[2]),
                "allowed_fixed_words": int(fields[4]),
                "normalized_profiles": int(fields[6]),
                "distinct_sorting_permutations": int(fields[8]),
                "labeled_full_star_weight": int(fields[10]),
            }
        elif fields[0] == "row":
            require(len(fields) == 8, "malformed census row")
            x, y, z, words, red_u, red_v, labeled = map(int, fields[1:])
            fixed = (x, y, z)
            require(x + y + z == 8 and y >= 2 and z <= 5, "admissible profile definition")
            require(words == multinomial8(fixed), "fixed-word multinomial")
            require((red_u, red_v) == (23 - z, 26 - y), "endpoint red-degree formula")
            require(labeled == 210 * words, "labeled full-star multiplicity")
            rows.append({
                "counts": [*MOVING, *fixed],
                "fixed_words": words,
                "red_degrees": [red_u, red_v],
                "labeled_assignments": labeled,
                "id": case_id(fixed),
            })
        else:
            raise RuntimeError("unknown census record")

    require(summary == {
        "fixed_words": 6561,
        "allowed_fixed_words": 5253,
        "normalized_profiles": 27,
        "distinct_sorting_permutations": 4019,
        "labeled_full_star_weight": 1103130,
    }, "complete independent census summary")
    require(len(rows) == 27 and sum(row["fixed_words"] for row in rows) == 5253,
            "complete twenty-seven-row cover")
    require(sum(row["labeled_assignments"] for row in rows) == 1103130,
            "complete labeled star weight")
    return {**summary, "rows": rows,
            "method": "direct C++ enumeration of all 3^8 fixed-contact words"}


def rotation(vertex: int) -> int:
    if vertex >= 33:
        return vertex
    return vertex - vertex % 3 + (vertex + 1) % 3


def primary_mapping(vertices: tuple[int, ...] | list[int]) -> dict[int, int]:
    require(sorted(vertices) == list(range(43)), "vertex bijection")
    require(all(vertices[rotation(v)] == rotation(vertices[v]) for v in range(43)),
            "vertex map commutes with C3")
    mapping: dict[int, int] = {}
    for a, b in itertools.combinations(range(43), 2):
        source = variable(a, b)
        c, d = sorted((vertices[a], vertices[b]))
        image = variable(c, d)
        if abs(source) == 321:
            require(image == source, "constant physical color preserved")
            continue
        require(1 <= source <= 320 and 1 <= image <= 320, "primary maps to primary")
        require(source not in mapping or mapping[source] == image, "orbit map is well defined")
        mapping[source] = image
    require(sorted(mapping) == list(range(1, 321)), "all primaries mapped")
    require(sorted(mapping.values()) == list(range(1, 321)), "primary-variable bijection")
    return mapping


def transport_literals(literals, mapping: dict[int, int]) -> tuple[int, ...]:
    return tuple(sorted(mapping[abs(literal)] if literal > 0 else -mapping[abs(literal)]
                        for literal in literals))


def sorting_map(word: tuple[int, ...]) -> tuple[int, ...]:
    vertices = list(range(43))
    order = sorted(range(8), key=lambda index: word[index])
    for destination, source in enumerate(order):
        vertices[35 + source] = 35 + destination
    return tuple(vertices)


def transported_physical_star(word: tuple[int, ...], vertices: tuple[int, ...]) -> set[int]:
    contacts = [kind for kind, count in enumerate(MOVING) for _ in range(count)]
    placed = list(zip(range(12, 33, 3), contacts)) + list(zip(range(35, 43), word))
    answer = set()
    for source, contact in placed:
        for endpoint, red in ((33, contact != 2), (34, contact != 1)):
            a, b = sorted((vertices[source], vertices[endpoint]))
            primary = variable(a, b)
            require(1 <= primary <= 320, "contact maps to physical primary")
            answer.add(primary if red else -primary)
    require(len(answer) == 30, "transported complete star")
    return answer


def normalization_audit() -> dict:
    permutations = set()
    admissible_words = 0
    literal_images = 0
    for word in itertools.product(range(3), repeat=8):
        fixed = tuple(word.count(kind) for kind in range(3))
        x, y, z = fixed
        red_u = 15 + x + y
        red_v = 18 + x + z
        if not (18 <= red_u <= 24 and 18 <= red_v <= 24):
            continue
        admissible_words += 1
        vertices = sorting_map(word)
        require(vertices[:35] == tuple(range(35)), "sorting fixes moving vertices and pair")
        require(transported_physical_star(word, vertices) == set(contact_units(fixed)),
                "actual physical full-star sorting transport")
        literal_images += 30
        permutations.add(vertices)
    require(admissible_words == 5253 and len(permutations) == 4019,
            "complete physical sorting census")
    for vertices in permutations:
        primary_mapping(vertices)
    return {
        "admissible_fixed_words": admissible_words,
        "distinct_sorting_permutations": len(permutations),
        "physical_full_stars_checked": admissible_words,
        "contact_literal_images_checked": literal_images,
        "primary_bijections_checked": len(permutations),
        "endpoint_swaps_used": 0,
    }


def vertex_mapping(kind: str) -> list[int]:
    vertices = list(range(43))
    if kind == "endpoint_only":
        vertices[33], vertices[34] = 34, 33
    elif kind.startswith("fixed_"):
        left = int(kind.split("_")[1])
        vertices[left], vertices[left + 1] = left + 1, left
    else:
        raise RuntimeError("unknown vertex mapping")
    return vertices


def complete_symmetry_audit(base: Path) -> dict:
    with base.open() as stream:
        require(stream.readline() == "p cnf 320 366069\n", "complete BLUE base header")
        clauses = {tuple(sorted(map(int, line.split()[:-1]))) for line in stream}
    require(len(clauses) == 366069, "all complete base clauses are distinct")

    moving_units = set(contact_units((8, 0, 0))[:14])
    names = [f"fixed_{vertex}" for vertex in range(35, 42)] + ["endpoint_only"]
    results = []
    for name in names:
        mapping = primary_mapping(vertex_mapping(name))
        for clause in clauses:
            require(transport_literals(clause, mapping) in clauses, f"complete base symmetry {name}")
        moved = set(transport_literals(moving_units, mapping))
        if name == "endpoint_only":
            require(moved != moving_units, "endpoint swap must not normalize ordered moving type")
        else:
            require(moved == moving_units, f"fixed sorting generator preserves moving child {name}")
        results.append({"name": name, "clause_images": len(clauses),
                        "ordered_moving_child_preserved": moved == moving_units})
    return {
        "complete_base_clauses": len(clauses),
        "generators": results,
        "clause_images_checked": len(clauses) * len(names),
        "endpoint_swap_as_normalizer_rejected": True,
    }


def construct_child(base: Path, child: Path, fixed: tuple[int, int, int]) -> list[int]:
    with base.open("rb") as source, child.open("wb") as destination:
        require(source.readline() == b"p cnf 320 366069\n", "accepted BLUE base header")
        destination.write(b"p cnf 320 366099\n")
        while block := source.read(1 << 20):
            destination.write(block)
        units = contact_units(fixed)
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

    census = read_census(args.census)
    public_profiles = json.loads((TARGET / "profiles.json").read_text())
    public_result = json.loads((TARGET / "result.json").read_text())
    require(public_result["complete"] and not public_result["open"], "public complete claim")
    require(not public_result["target_graph"] and not public_result["whole_core_exclusions"],
            "public scope is a conditional color-branch exclusion")
    public_cases = {row["id"]: row for row in public_result["cases"]}
    expected_ids = [row["id"] for row in census["rows"]]
    require(public_result["excluded"] == expected_ids and sorted(public_cases) == sorted(expected_ids),
            "public twenty-seven-case cover")

    for public, independent in zip(public_profiles, census["rows"]):
        fixed = tuple(independent["counts"][3:])
        require(public["counts"] == independent["counts"], "public canonical counts")
        require(public["red_degrees"] == independent["red_degrees"], "public endpoint degrees")
        require(public["labeled_assignments"] == independent["labeled_assignments"],
                "public labeled profile weight")
        require(public["units"] == contact_units(fixed), "public physical unit meanings")

    multiplicity = json.loads((ROOT / "ramsey_r55_order3_eleven_core194_multiplicity_review1" /
                               "result.json").read_text())
    require(multiplicity["all_checks_passed"] and
            multiplicity["conclusion"]["one_empty_branch_excluded"] and
            not multiplicity["conclusion"]["multiple_empty_branch_tested"],
            "accepted imported lower-bound review scope")
    prior_a5 = json.loads((ROOT / "ramsey_r55_core194_a5_fixed_review1" / "result.json").read_text())
    require(prior_a5["status"] == "PASS" and prior_a5["all_nineteen_refuted"],
            "accepted imported a5 review")

    normalization = normalization_audit()
    base = args.work / "blue.cnf"
    generated = subprocess.run(
        [sys.executable, "-B", str(DIRECT / "generate.py"), "--color", "blue", "--output", str(base)],
        text=True, capture_output=True, check=True,
    )
    base_report = json.loads(generated.stdout)
    require(identity(base) == BASE_IDENTITY == base_report["formula"], "accepted direct base regenerated exactly")
    symmetries = complete_symmetry_audit(base)

    version = subprocess.run([str(args.kissat), "--version"], text=True,
                             capture_output=True, check=True).stdout.strip()
    require(version == "4.0.4", "unexpected Kissat version")
    start = time.monotonic()
    cases = []
    for independent in census["rows"]:
        fixed = tuple(independent["counts"][3:])
        identifier = independent["id"]
        public = public_cases[identifier]
        cnf = args.work / f"{identifier}.cnf"
        units = construct_child(base, cnf, fixed)
        inspect_child(base, cnf, units)
        formula = identity(cnf)
        require(formula == public["formula"], "fresh formula differs from public formula")

        trace = args.work / f"{identifier}.drat"
        solve_log = args.work / f"{identifier}.solve.log"
        solve_start = time.monotonic()
        with solve_log.open("w") as output:
            solved = subprocess.run(
                [str(args.kissat), f"--time={args.solve_seconds}", str(cnf), str(trace)],
                stdout=output, stderr=subprocess.STDOUT, timeout=args.solve_seconds + 60,
            )
        exact_status(solve_log, "s UNSATISFIABLE")
        require(solved.returncode == 20, "Kissat did not return UNSAT")

        replay_log = args.work / f"{identifier}.replay.log"
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
        cases.append({
            "id": identifier,
            "fixed_counts": list(fixed),
            "formula": formula,
            "proof": proof,
            "published_proof_match": proof == public["trace"],
            "rat_core_lemmas": int(rat.group(1)),
            "solve_seconds": round(replay_start - solve_start, 6),
            "replay_seconds": round(time.monotonic() - replay_start, 6),
        })
        print(f"VERIFIED {identifier}", flush=True)

    first_child = args.work / f"{expected_ids[0]}.cnf"
    wrong_units = contact_units(tuple(census["rows"][0]["counts"][3:]))
    wrong_units[-1] *= -1
    inspector_rejected_wrong_unit = False
    try:
        inspect_child(base, first_child, wrong_units)
    except RuntimeError:
        inspector_rejected_wrong_unit = True
    require(inspector_rejected_wrong_unit, "formula inspector accepted wrong physical unit")

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
            "DRAT checker accepted false refutation")

    report = {
        "status": "PASS",
        "verdict": "the complete Core194 BLUE empty-pair branch is excluded",
        "source_commit": "5737e2ee57db6a270602626ec48a9cace8a094c2",
        "census": census,
        "normalization_audit": normalization,
        "base_formula": identity(base),
        "symmetry_audit": symmetries,
        "cases": cases,
        "all_twenty_seven_refuted": len(cases) == 27,
        "all_formulas_match_published": all(row["formula"] == public_cases[row["id"]]["formula"] for row in cases),
        "all_proofs_match_published": all(row["published_proof_match"] for row in cases),
        "proof_bytes": sum(row["proof"]["bytes"] for row in cases),
        "inspector_rejected_wrong_unit": inspector_rejected_wrong_unit,
        "false_refutation_rejected": True,
        "execution": "serial; one solver or proof-checker process at a time",
        "kissat_version": version,
        "kissat_binary": identity(args.kissat),
        "drat_trim_binary": identity(args.drat_trim),
        "elapsed_seconds": round(time.monotonic() - start, 6),
        "combined_corollary": {
            "blue_empty_fixed_pair_exists": False,
            "empty_fixed_vertices_induce": "red clique",
            "cardinality_lower_bound": 2,
            "lower_bound_import": "accepted one-empty-branch multiplicity review",
            "cardinality_upper_bound": 4,
            "upper_bound_reason": "a red K5 is forbidden",
            "necessary_possible_cardinalities": [2, 3, 4],
        },
        "red_pair_branch_resolved": False,
        "whole_core194_excluded": False,
        "target_graph_found": False,
        "ramsey_bound_improved": False,
    }
    args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "PASS", "cases": len(cases),
                      "proof_bytes": report["proof_bytes"]}, sort_keys=True))


if __name__ == "__main__":
    main()
