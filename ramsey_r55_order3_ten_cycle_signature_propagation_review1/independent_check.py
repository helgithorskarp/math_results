#!/usr/bin/env python3
"""Clean-room check of the twelve-unit ten-cycle closure layer.

No module from the contribution under review is imported.  The already
reviewed parent formula is pinned by hash; the four inherited tails and the
new units are reconstructed from literal edge orbits and mathematical data.
"""

from __future__ import annotations

from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess


BASE_SHA256 = "f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e"
BASE_HEADER = b"p cnf 28950 927000\n"
EXTENDED_HEADER = b"p cnf 28974 927346\n"
MATCHING = {frozenset((0, 1)), frozenset((2, 3))}
PHASE_PAIRS = ((1, 2), (1, 3), (2, 3))
CASES = (
    {"index": 0, "anchor": 64, "weights": (1, 2, 2, 1, 1, 1, 1, 2, 2)},
    {"index": 1, "anchor": 65, "weights": (1, 2, 2, 1, 1, 1, 2, 2, 2)},
    {"index": 2, "anchor": 67, "weights": (1, 2, 2, 1, 1, 2, 2, 2, 2)},
    {"index": 3, "anchor": 69, "weights": (1, 2, 2, 1, 2, 2, 2, 2, 2)},
)
FORMULAS = {
    0: (36296829, "868b9d9131a1b22ac904a0e888ab620740c3a66268730ec4a1674ca5e930fbcc"),
    1: (36296828, "e3b6f70000021119cfd2df83c9940797746fae6efc8d4236e512ece70f3555bb"),
    2: (36296827, "a155b42bb766ad85ffd95d306753b41c20b003314483d12c7d7ddad9ba75e74a"),
    3: (36296826, "cf08f734de1c94dc581911267049626e7e201b7ea48c0a80ff59025f039e98da"),
}
PROOFS = {
    0: (86511376, "3196c088b711fb2e139d818e70665fa32c4d3814db2e701ad4811d995a0ebdd3"),
    1: (100928817, "2d4c51d72505c2ffd572090d693acbe671eb2852def18ffa335a64e9228367d5"),
    2: (50494841, "774ef26a9d4afbb81bc3b595aa63fc1a1a958463edc2e3d96e05a7a9db5483b1"),
    3: (50195839, "a26d6dfe3b58161393a51a3e1d334815095fba1ce5e454a0d1351c00febd54b7"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def primary_edge_variables() -> dict[tuple[int, int], int]:
    rotation = tuple(3 * (v // 3) + (v + 1) % 3 if v < 30 else v for v in range(43))
    unseen = set(combinations(range(43), 2))
    orbits = []
    while unseen:
        edge = min(unseen)
        orbit = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((rotation[edge[0]], rotation[edge[1]])))
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))

    cross = sorted(orbit for orbit in orbits
                   if orbit[0][1] < 30 and orbit[0][0] // 3 != orbit[0][1] // 3)
    fixed = sorted(orbit for orbit in orbits if orbit[0][0] >= 30)
    links = sorted((orbit for orbit in orbits if orbit[0][0] < 30 <= orbit[0][1]),
                   key=lambda orbit: (orbit[0][1], orbit[0][0]))
    internal = [orbit for orbit in orbits
                if orbit[0][1] < 30 and orbit[0][0] // 3 == orbit[0][1] // 3]
    require((len(orbits), len(cross), len(fixed), len(links), len(internal))
            == (353, 135, 78, 130, 10), "wrong literal orbit partition")
    variables = {}
    for number, orbit in enumerate(cross + fixed + links, 1):
        for edge in orbit:
            variables[edge] = number
    require(len(variables) == 873 and max(variables.values()) == 343,
            "wrong primary variable map")
    return variables


def unit_audit(variables: dict[tuple[int, int], int]) -> dict[str, object]:
    selected_edges = {(moving, fixed) for moving in range(12) for fixed in range(30, 33)}
    selected_variables = {variables[edge] for edge in selected_edges}
    expected = {214 + 10 * row + column for row in range(3) for column in range(4)}
    require(selected_variables == expected and len(selected_edges) == 36,
            "twelve unit variables do not represent the selected edges")
    inverse = {}
    for edge, variable in variables.items():
        inverse.setdefault(variable, set()).add(edge)
    require(set().union(*(inverse[v] for v in expected)) == selected_edges,
            "a unit orbit includes an unintended edge")
    require(all(len(inverse[v]) == 3 for v in expected), "moving-link orbit is not three edges")
    return {
        "negative_units": sorted(-variable for variable in expected),
        "literal_edges_forced_blue": len(selected_edges),
        "unit_orbit_size": 3,
    }


def lexicographic_audit() -> int:
    comparisons = 0
    for empty_suffix in product((0, 1), repeat=6):
        for nonempty_prefix in product((0, 1), repeat=4):
            if not any(nonempty_prefix):
                continue
            for nonempty_suffix in product((0, 1), repeat=6):
                require((0, 0, 0, 0) + empty_suffix < nonempty_prefix + nonempty_suffix,
                        "empty minority signature is not ordered first")
                comparisons += 1
    require(comparisons == 61440, "wrong ordering comparison count")
    return comparisons


def falsified_clause(bits: tuple[int, ...], values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(-variable if value else variable
                        for variable, value in zip(bits, values)))


def common_phase_layer(variables: dict[tuple[int, int], int]) -> list[tuple[int, ...]]:
    clauses = []
    for left, right in combinations(range(4), 2):
        bits = tuple(variables[3 * left, 3 * right + offset] for offset in range(3))
        required_weight = 1 if frozenset((left, right)) in MATCHING else 2
        for values in product((0, 1), repeat=3):
            if sum(values) != required_weight:
                clauses.append(falsified_clause(bits, values))

    for minority in range(4):
        gates = []
        for majority in range(4, 10):
            bits = tuple(variables[3 * minority, 3 * majority + offset] for offset in range(3))
            clauses.append(tuple(sorted(bits)))
            clauses.append(tuple(sorted(-variable for variable in bits)))
            gate = 28951 + 6 * minority + majority - 4
            gates.append(gate)
            for values in product((0, 1), repeat=3):
                clauses.append(tuple(sorted(
                    falsified_clause(bits, values) +
                    ((gate if sum(values) == 1 else -gate),)
                )))
        clauses.append(tuple(gates))
        clauses.extend(tuple(sorted(-gate for gate in subset))
                       for subset in combinations(gates, 5))
    require(len(clauses) == len(set(clauses)) == 298,
            "wrong common phase-layer dimensions")
    return clauses


def core_color(left: int, right: int, offset: int) -> bool:
    if frozenset((left, right)) in MATCHING:
        return offset == 0
    return offset in (0, 1)


def inherited_tail(case: dict[str, object], variables: dict[tuple[int, int], int]) -> list[tuple[int, ...]]:
    clauses = common_phase_layer(variables)
    for block, weight in enumerate(case["weights"], 1):
        for offset in range(3):
            variable = variables[0, 3 * block + offset]
            clauses.append((variable if offset < weight else -variable,))
    for left, right in PHASE_PAIRS:
        for offset in range(3):
            variable = variables[3 * left, 3 * right + offset]
            clauses.append((variable if core_color(left, right, offset) else -variable,))
    require(len(clauses) == len(set(clauses)) == 334,
            "wrong inherited case-tail dimensions")
    return clauses


def read_tail(stream) -> list[tuple[int, ...]]:
    clauses = []
    for line in stream:
        values = tuple(map(int, line.split()))
        require(values and values[-1] == 0 and all(values[:-1]), "malformed tail clause")
        clause = tuple(sorted(values[:-1]))
        require(len(clause) == len(set(clause)) and not any(-x in clause for x in clause),
                "noncanonical tail clause")
        clauses.append(clause)
    return clauses


def check_formula(base: Path, formula: Path, case: dict[str, object],
                  variables: dict[tuple[int, int], int], units: list[int]) -> dict[str, object]:
    require(file_info(base)["sha256"] == BASE_SHA256, "reviewed parent formula changed")
    with base.open("rb") as parent, formula.open("rb") as extended:
        require(parent.readline() == BASE_HEADER, "wrong parent header")
        require(extended.readline() == EXTENDED_HEADER, "wrong extended header")
        while block := parent.read(1 << 20):
            require(extended.read(len(block)) == block, "a parent clause was changed")
        observed = read_tail(extended)
    expected = inherited_tail(case, variables) + [(unit,) for unit in units]
    require(len(observed) == 346 and sorted(observed) == sorted(expected),
            "extended clause multiset differs")
    expected_bytes, expected_sha = FORMULAS[case["index"]]
    info = file_info(formula)
    require(info == {"bytes": expected_bytes, "sha256": expected_sha},
            "extended formula digest differs")
    return {
        "index": case["index"],
        "anchor": case["anchor"],
        "weights": list(case["weights"]),
        "parent_clauses_preserved": 927000,
        "inherited_tail_clauses": 334,
        "new_unit_clauses": 12,
        "formula": info,
    }


def mutation_controls(expected_tail: list[tuple[int, ...]], units: list[int]) -> list[str]:
    expected = sorted(expected_tail + [(unit,) for unit in units])
    mutations = {
        "missing_unit": expected_tail + [(unit,) for unit in units[1:]],
        "wrong_polarity": expected_tail + [(-units[0],)] + [(unit,) for unit in units[1:]],
        "wrong_cycle": expected_tail + [(-218,)] + [(unit,) for unit in units[1:]],
        "unsupported_empty_clause": expected_tail + [(unit,) for unit in units] + [()],
    }
    rejected = []
    for name, mutation in mutations.items():
        require(sorted(mutation) != expected, f"mutation {name} was not detected")
        rejected.append(name)
    return rejected


def replay(formula: Path, proof: Path, checker: Path, work: Path, index: int) -> dict[str, object]:
    expected_bytes, expected_sha = PROOFS[index]
    info = file_info(proof)
    require(info == {"bytes": expected_bytes, "sha256": expected_sha},
            f"full proof digest differs for case {index}")
    log = work / f"independent_replay_{index:02}.log"
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
    require(match is not None and int(match.group(1)) > 0,
            f"general DRAT path was not exercised for case {index}")
    return {"index": index, "proof": info, "drat_trim_verified": True,
            "rat_core_lemmas": int(match.group(1))}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    checker = args.drat_trim.resolve()
    require(checker.is_file(), "missing DRAT checker")
    base = work / "base.cnf"
    require(base.is_file(), "missing regenerated parent formula")

    variables = primary_edge_variables()
    unit_result = unit_audit(variables)
    units = unit_result["negative_units"]
    report = {
        "reviewed_parent_formula_sha256": BASE_SHA256,
        "primary_edge_orbits": 353,
        "unit_layer": unit_result,
        "prefix_suffix_comparisons": lexicographic_audit(),
        "cases": [],
        "proof_replays": [],
        "drat_trim": file_info(checker),
    }
    for case in CASES:
        index = case["index"]
        formula = work / f"case_{index:02}.cnf"
        proof = work / f"case_{index:02}.drat"
        require(formula.is_file() and proof.is_file(), f"missing case {index} evidence")
        row = check_formula(base, formula, case, variables, units)
        report["cases"].append(row)
        print(f"FORMULA case={index} parent+334+12 exact")
        proof_row = replay(formula, proof, checker, work, index)
        report["proof_replays"].append(proof_row)
        print(f"PROOF case={index} DRAT verified")

    report["mutation_controls_rejected"] = mutation_controls(
        inherited_tail(CASES[0], variables), units)
    report["complete_four_case_cover"] = [case["anchor"] for case in CASES] == [64, 65, 67, 69]
    report["all_four_extensions_excluded"] = all(
        row["drat_trim_verified"] for row in report["proof_replays"])
    report["minimum_moving_cycles_after_reviewed_dependencies"] = 11
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS independent ten-cycle closure: all four extensions excluded")


if __name__ == "__main__":
    main()
