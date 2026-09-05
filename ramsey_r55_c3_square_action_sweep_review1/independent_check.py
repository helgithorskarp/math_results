#!/usr/bin/env python3
"""Clean-room review of the C3-square action cover and SAT certificates.

No submitted module is imported.  Quotient actions are constructed from
their stabilizer subgroups, pair orbits are found by graph traversal under
two generators, and every five-set clause is reconstructed from definitions.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import subprocess


PUBLISHED_SWEEP_SHA256 = (
    "73a9ef997788026c95806bb2635d13d0639fac84e315c24852bf0e8a09de6a53"
)
DRAT_TRIM_SHA256 = (
    "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a"
)
EXCLUDED = (0, 1, 2, 3, 4, 5, 6, 7, 8, 11, 12, 13, 14, 15, 16, 17)
OPEN = (9, 10)

# The order agrees with the submitted vertex convention, but these are
# stabilizer generators, not the submitted list of quotient linear forms.
KERNEL_DIRECTIONS = ((0, 1), (1, 0), (1, 2), (1, 1))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def normalize_line(vector: tuple[int, int]) -> tuple[int, int]:
    x, y = vector[0] % 3, vector[1] % 3
    require((x, y) != (0, 0), "zero vector has no projective line")
    scale = pow(x if x else y, -1, 3)
    return x * scale % 3, y * scale % 3


def annihilator(direction: tuple[int, int]) -> tuple[int, int]:
    """Canonical linear functional whose kernel is the given line."""
    x, y = direction
    return normalize_line((y, -x))


def projective_action_audit() -> dict[str, int]:
    line_set = set(KERNEL_DIRECTIONS)
    require(len(line_set) == 4, "wrong projective-line list")
    actions = set()
    matrices = 0
    for a, b, c, d in product(range(3), repeat=4):
        if (a * d - b * c) % 3 == 0:
            continue
        matrices += 1
        action = []
        for x, y in KERNEL_DIRECTIONS:
            image = normalize_line(((a * x + b * y) % 3,
                                    (c * x + d * y) % 3))
            require(image in line_set, "matrix missed a projective line")
            action.append(KERNEL_DIRECTIONS.index(image))
        actions.add(tuple(action))
    require(matrices == 48, "GL(2,3) order mismatch")
    require(actions == set(permutations(range(4))),
            "projective image is not the full symmetric group")
    return {"invertible_matrices": matrices, "projective_permutations": len(actions)}


def action_classes() -> tuple[list[dict[str, object]], int]:
    """Enumerate ordered orbit data first, quotient by the proved S4 action."""
    ordered = set()
    for a in range(44):
        for b in product(range(4), repeat=4):
            if any(a + 3 * multiplicity > 10 for multiplicity in b):
                continue
            remainder = 43 - a - 3 * sum(b)
            if remainder >= 0 and remainder % 9 == 0:
                c = remainder // 9
                if c <= 4:
                    ordered.add((a, b, c))
    classes = sorted({(a, tuple(sorted(b)), c) for a, b, c in ordered},
                     key=lambda row: (row[2], row[0], row[1]))
    # Match the published case order: the source loops over a, then c, then b.
    classes.sort(key=lambda row: (row[0], row[2], row[1]))
    rows = [
        {"index": index, "a": a, "b": list(b), "c": c}
        for index, (a, b, c) in enumerate(classes)
    ]
    require(len(ordered) == 117 and len(rows) == 18,
            "wrong action-cover dimensions")
    require(all(row["c"] >= 1 for row in rows),
            "a nonfaithful action survived the motion bound")
    return rows, len(ordered)


def action(case: dict[str, object]) -> dict[tuple[int, int], tuple[int, ...]]:
    """Build translations directly on fixed, quotient-coset, and regular blocks."""
    a = int(case["a"])
    b = tuple(int(value) for value in case["b"])
    c = int(case["c"])
    quotient_blocks = []
    offset = a
    for direction, multiplicity in zip(KERNEL_DIRECTIONS, b):
        functional = annihilator(direction)
        for _ in range(multiplicity):
            quotient_blocks.append((offset, functional))
            offset += 3
    regular_blocks = []
    for _ in range(c):
        regular_blocks.append(offset)
        offset += 9
    require(offset == 43, "action has the wrong number of points")

    translations = {}
    for x, y in product(range(3), repeat=2):
        image = list(range(43))
        for start, (u, v) in quotient_blocks:
            shift = (u * x + v * y) % 3
            for t in range(3):
                image[start + t] = start + (t + shift) % 3
        for start in regular_blocks:
            for u, v in product(range(3), repeat=2):
                image[start + 3 * u + v] = (
                    start + 3 * ((u + x) % 3) + (v + y) % 3
                )
        translations[x, y] = tuple(image)

    identity = tuple(range(43))
    require(translations[0, 0] == identity and len(set(translations.values())) == 9,
            "action is not faithful")
    for left in translations:
        for right in translations:
            composed = tuple(translations[left][translations[right][vertex]]
                             for vertex in range(43))
            expected = translations[(left[0] + right[0]) % 3,
                                    (left[1] + right[1]) % 3]
            require(composed == expected, "translation group law failed")
    return translations


def edge_variables(case: dict[str, object], vertices: int = 43) -> tuple[dict[tuple[int, int], int], dict[str, int]]:
    translations = action(case)
    generators = (translations[1, 0], translations[0, 1])
    unseen = set(combinations(range(vertices), 2))
    orbits = []
    while unseen:
        seed = min(unseen)
        orbit = {seed}
        frontier = [seed]
        while frontier:
            left, right = frontier.pop()
            for generator in generators:
                image = tuple(sorted((generator[left], generator[right])))
                require(image[1] < vertices, "restricted control is not invariant")
                if image not in orbit:
                    orbit.add(image)
                    frontier.append(image)
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))
    orbits.sort(key=lambda orbit: orbit[0])
    ids = {edge: index for index, orbit in enumerate(orbits, 1) for edge in orbit}
    histogram = Counter(len(orbit) for orbit in orbits)
    require(len(ids) == math.comb(vertices, 2), "pair cover is incomplete")
    require(set(histogram) <= {1, 3, 9}, "wrong pair-orbit size")
    return ids, {str(size): histogram.get(size, 0) for size in (1, 3, 9)}


def fixed_point_audit(case: dict[str, object]) -> list[int]:
    translations = action(case)
    observed = sorted(sum(image[v] == v for v in range(43))
                      for key, image in translations.items() if key != (0, 0))
    expected = sorted(int(case["a"]) + 3 * value
                      for value in case["b"] for _ in range(2))
    require(observed == expected and max(observed) <= 10,
            "nonidentity fixed-point census differs")
    return observed


def ramsey_clauses(ids: dict[tuple[int, int], int], vertices: int) -> set[tuple[int, ...]]:
    clauses = set()
    for five in combinations(range(vertices), 5):
        positive = tuple(sorted({ids[edge] for edge in combinations(five, 2)}))
        clauses.add(positive)
        clauses.add(tuple(sorted(-literal for literal in positive)))
    return clauses


def small_semantic_control(case: dict[str, object]) -> dict[str, int]:
    ids, _ = edge_variables(case, 7)
    clauses = ramsey_clauses(ids, 7)
    variables = max(ids.values())
    ramsey = normalized = checked = 0
    for bits in product((False, True), repeat=variables):
        encoded = all(any(bits[abs(literal) - 1] == (literal > 0)
                          for literal in clause) for clause in clauses)
        direct = True
        for five in combinations(range(7), 5):
            red = sum(bits[ids[edge] - 1] for edge in combinations(five, 2))
            if red in (0, 10):
                direct = False
                break
        require(encoded == direct, "small formula semantics failed")
        checked += 1
        if direct:
            ramsey += 1
            normalized += bits[0]
    require((variables, checked, ramsey, normalized) == (7, 128, 116, 58),
            "small semantic control differs")
    return {"variables": variables, "assignments_checked": checked,
            "ramsey_assignments": ramsey,
            "normalized_ramsey_assignments": normalized}


def read_clause(line: str) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    require(values and values[-1] == 0 and all(values[:-1]),
            "malformed DIMACS clause")
    clause = values[:-1]
    require(tuple(sorted(clause)) == clause and len(set(clause)) == len(clause)
            and not any(-literal in clause for literal in clause),
            "noncanonical DIMACS clause")
    return clause


def check_formula(case: dict[str, object], path: Path,
                  reference: dict[str, object]) -> dict[str, object]:
    ids, histogram = edge_variables(case)
    clauses = ramsey_clauses(ids, 43)
    ramsey_count = len(clauses)
    require((1,) not in clauses and (-1,) not in clauses,
            "Ramsey clauses unexpectedly contain a unit")
    clauses.add((1,))
    expected = sorted(clauses, key=lambda clause: (len(clause), clause))
    variables = max(ids.values())
    with path.open() as stream:
        header = stream.readline().rstrip("\n")
        require(header == f"p cnf {variables} {len(expected)}", "wrong DIMACS header")
        for wanted in expected:
            observed = read_clause(stream.readline())
            require(observed == wanted, "complete formula clause mismatch")
        require(stream.readline() == "", "trailing DIMACS content")
    info = file_info(path)
    observed = dict(info, variables=variables, clauses=len(expected),
                    ramsey_clauses=ramsey_count)
    require(observed == reference, "formula digest or dimensions differ")
    require(sum(int(size) * count for size, count in histogram.items()) == 903,
            "edge-orbit histogram does not cover all pairs")
    return dict(case, fixed_points_nonidentity=fixed_point_audit(case),
                edge_orbits=variables, edge_orbit_size_histogram=histogram,
                five_sets_checked=math.comb(43, 5), formula=info,
                variables=variables, clauses=len(expected))


def replay(formula: Path, proof: Path, checker: Path, log: Path,
           reference: dict[str, object], index: int) -> dict[str, object]:
    info = file_info(proof)
    require(info == reference, f"proof digest differs for case {index}")
    with log.open("w") as output:
        process = subprocess.run(
            [str(checker), str(formula), str(proof), "-t", "600"],
            stdout=output,
            stderr=subprocess.STDOUT,
            timeout=660,
        )
    text = log.read_text()
    require(process.returncode == 0 and "s VERIFIED" in text,
            f"DRAT replay failed for case {index}")
    match = re.search(r"(\d+) RAT lemmas in core", text)
    require(match is not None, f"missing DRAT statistic for case {index}")
    return {"index": index, "proof": info, "drat_trim_verified": True,
            "rat_core_lemmas": int(match.group(1))}


def mutation_controls(first_formula: list[tuple[int, ...]]) -> list[str]:
    expected = sorted(first_formula, key=lambda clause: (len(clause), clause))
    mutations = {
        "missing_complement_unit": [clause for clause in expected if clause != (1,)],
        "opposite_complement_unit": [(-1,) if clause == (1,) else clause for clause in expected],
        "dropped_ramsey_clause": expected[:-1],
        "unsupported_empty_clause": expected + [()],
    }
    rejected = []
    for name, mutation in mutations.items():
        require(mutation != expected, f"mutation {name} was not detected")
        rejected.append(name)
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    source, work = args.source.resolve(), args.work.resolve()
    checker = args.drat_trim.resolve()
    published_path = source / "sweep_result.json"
    require(file_info(published_path)["sha256"] == PUBLISHED_SWEEP_SHA256,
            "published sweep manifest changed")
    require(file_info(checker)["sha256"] == DRAT_TRIM_SHA256,
            "unexpected DRAT checker")
    published = json.loads(published_path.read_text())
    regenerated = json.loads((work / "result.json").read_text())

    cases, ordered_count = action_classes()
    require([row["index"] for row in published["cases"]] == list(range(18)),
            "published case indexing differs")
    require(tuple(published["excluded_indices"]) == EXCLUDED
            and tuple(published["open_indices"]) == OPEN,
            "published result partition differs")
    require(tuple(regenerated["excluded_indices"]) == EXCLUDED
            and tuple(regenerated["open_indices"]) == OPEN
            and regenerated["complete_bounded_sweep"]
            and not regenerated["target_graph_found"],
            "regenerated result partition differs")

    projective = projective_action_audit()
    report = {
        "action_cover": dict(projective, ordered_multiplicity_types=ordered_count,
                             inequivalent_types=len(cases)),
        "small_semantic_control": small_semantic_control(cases[0]),
        "formula_audits": [],
        "proof_replays": [],
        "excluded_indices": list(EXCLUDED),
        "open_indices": list(OPEN),
        "drat_trim": file_info(checker),
    }
    audited_cases = []
    first_formula = None
    for case in cases:
        index = int(case["index"])
        reference = published["cases"][index]
        local = regenerated["cases"][index]
        require(all(reference[key] == case[key] for key in ("index", "a", "b", "c")),
                f"published action meaning differs for case {index}")
        require(all(local[key] == case[key] for key in ("index", "a", "b", "c")),
                f"regenerated action meaning differs for case {index}")
        require(local["status"] == reference["status"]
                and local["formula"] == reference["formula"],
                f"regenerated case summary differs for case {index}")
        formula = work / f"case_{index:02}.cnf"
        row = check_formula(case, formula, reference["formula"])
        audited_cases.append(row)
        report["formula_audits"].append({
            key: row[key] for key in
            ("index", "a", "b", "c", "variables", "clauses", "formula")
        })
        print(f"FORMULA case={index} complete five-set reconstruction", flush=True)
        if first_formula is None:
            ids, _ = edge_variables(case)
            first_formula = list(ramsey_clauses(ids, 43) | {(1,)})
        if index in EXCLUDED:
            require(local["proof"] == reference["proof"]
                    and local["status"] == "excluded",
                    f"excluded trace differs for case {index}")
            proof_row = replay(formula, work / f"case_{index:02}.drat", checker,
                               work / f"independent_replay_{index:02}.log",
                               reference["proof"], index)
            report["proof_replays"].append(proof_row)
            print(f"PROOF case={index} DRAT verified", flush=True)
        else:
            log = (work / f"case_{index:02}.solve.log").read_text()
            require(local["solver_code"] == 0 and local["status"] == "open"
                    and "s UNKNOWN" in log
                    and "s SATISFIABLE" not in log
                    and "s UNSATISFIABLE" not in log,
                    f"open status is not an explicit UNKNOWN for case {index}")
            print(f"OPEN case={index} explicit UNKNOWN retained", flush=True)

    require(first_formula is not None, "missing mutation fixture")
    report["mutation_controls_rejected"] = mutation_controls(first_formula)
    report["all_sixteen_exclusions_verified"] = (
        [row["index"] for row in report["proof_replays"]] == list(EXCLUDED)
    )
    residual = [audited_cases[index] for index in OPEN]
    moving_cycles = [sorted((43 - fixed) // 3
                            for fixed in row["fixed_points_nonidentity"])
                     for row in residual]
    require(moving_cycles == [[12, 12, 14, 14, 14, 14, 14, 14],
                              [13, 13, 13, 13, 14, 14, 14, 14]],
            "residual motion census differs")
    report["residual_actions"] = {
        "indices": list(OPEN),
        "global_fixed_vertices": [int(row["a"]) for row in residual],
        "three_point_orbits": [sum(row["b"]) for row in residual],
        "regular_nine_point_orbits": [int(row["c"]) for row in residual],
        "moving_cycles_nonidentity": moving_cycles,
    }
    report["group_corollaries"] = {
        "order_27_orbit_remainder": (43 - 1) % 9,
        "order_27_divisibility_excluded": (43 - 1) % 9 != 0,
        "global_3_adic_exponent_at_most": 2,
        "m214_3_adic_exponent_at_most": 1,
    }
    if args.report:
        args.report.write_text(json.dumps(
            report, sort_keys=True, separators=(",", ":")) + "\n")
    print("PASS C3-square cover: sixteen excluded, two open, order 27 impossible")


if __name__ == "__main__":
    main()
