#!/usr/bin/env python3
"""Clean-room reconstruction and certificate replay for the ten-cycle split.

This checker imports no submitted Python or C++ module.  It reconstructs each
complete formula from literal edge orbits and declarative constraints, compares
the canonical DIMACS stream, and replays every claimed DRAT proof.
"""

from __future__ import annotations

from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import argparse
import hashlib
import json
import subprocess


ROOT = Path(__file__).resolve().parent
TARGET = ROOT.parent / "ramsey_r55_order3_ten_cycle_obstruction"
CONSTANT = 1_000_000_000
EXCLUDED = (0, 1, 2, 3, 5)
EXPECTED = {
    0: (28878, 922248, "6a3a8f0c8c710f828039c50108a058889022ee3679faa66235c2948a772db6a3"),
    1: (28905, 924030, "4ea4e41b6b1931a815d1dc97c5a38e300ca425e12e5f939bd9ac099fc5e60a76"),
    2: (28926, 925416, "b0cbe934038d1a051923fce89353a1ebb175e27b17b687a1731d7909fdba8ddd"),
    3: (28941, 926406, "51cc8fac0f7739c5053edd70655103eca8b5fa62e12f2eae13c74f73fe5789ff"),
    4: (28950, 927000, "f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e"),
    5: (28953, 927198, "06743ada133505e9a1faad6e45cc03d47166d4fb9e8db5fa2e6a91b40a0a3567"),
}
REFERENCE_PROOFS = {
    0: (8147052, "e0ece299d9f9d03bc10a4445dc2fe027444bf44882f45883f0cce789089a2cb3"),
    1: (21566390, "3a1b0fec20bb4506deea080dde377c3c8968fab147c27eca827e89e2390277d8"),
    2: (34396400, "80ce6e4e0c7bfdc84bc7b3461dd31ac19532a0d1960b66e8f419b484a9fc3870"),
    3: (105710182, "91163ad8bc53e3d2a34d9b712d8c421f6f561e624bb2c2a3efb589d3b465d0f1"),
    5: (3889980, "98b9dda66d758255346827c3e3f18eb96f1abb813139590fd2d0467ac949b34f"),
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


def pair_orbits(red_cycles: int) -> tuple[dict[tuple[int, int], int], int]:
    rotation = tuple(3 * (v // 3) + (v + 1) % 3 if v < 30 else v for v in range(43))
    unseen = set(combinations(range(43), 2))
    orbits: list[tuple[tuple[int, int], ...]] = []
    while unseen:
        seed = min(unseen)
        orbit = set()
        edge = seed
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((rotation[edge[0]], rotation[edge[1]])))
        unseen.difference_update(orbit)
        orbits.append(tuple(sorted(orbit)))

    moving_cross = sorted(
        orbit for orbit in orbits
        if orbit[0][1] < 30 and orbit[0][0] // 3 != orbit[0][1] // 3
    )
    fixed_fixed = sorted(orbit for orbit in orbits if orbit[0][0] >= 30)
    fixed_moving = sorted(
        (orbit for orbit in orbits if orbit[0][0] < 30 <= orbit[0][1]),
        key=lambda orbit: (orbit[0][1], orbit[0][0]),
    )
    internal = [
        orbit for orbit in orbits
        if orbit[0][1] < 30 and orbit[0][0] // 3 == orbit[0][1] // 3
    ]
    require((len(orbits), len(moving_cross), len(fixed_fixed), len(fixed_moving), len(internal))
            == (353, 135, 78, 130, 10), "wrong edge-orbit partition")

    edge_value: dict[tuple[int, int], int] = {}
    for variable, orbit in enumerate(moving_cross + fixed_fixed + fixed_moving, 1):
        for edge in orbit:
            edge_value[edge] = variable
    for orbit in internal:
        color = orbit[0][0] // 3 < red_cycles
        for edge in orbit:
            edge_value[edge] = CONSTANT if color else -CONSTANT
    require(len(edge_value) == 903, "not every literal edge was assigned")
    return edge_value, len(orbits)


def reconstruct_formula(red_cycles: int) -> tuple[int, set[tuple[int, ...]], dict[str, int]]:
    edge_value, orbit_count = pair_orbits(red_cycles)
    clauses: set[tuple[int, ...]] = set()

    def edge(a: int, b: int) -> int:
        return edge_value[tuple(sorted((a, b)))]

    def add(literals) -> None:
        row = set(literals)
        if CONSTANT in row:
            return
        row.discard(-CONSTANT)
        if any(-literal in row for literal in row):
            return
        clauses.add(tuple(sorted(row)))

    five_sets = 0
    for vertices in combinations(range(43), 5):
        five_sets += 1
        pairs = [edge(a, b) for a, b in combinations(vertices, 2)]
        add(-literal for literal in pairs)
        add(pairs)
    require(five_sets == 962598, "wrong five-set coverage")
    ramsey_clauses = len(clauses)

    next_variable = 343
    colors = [int(i < red_cycles) for i in range(10)]
    deficits: list[list[int]] = [[] for _ in range(10)]
    complete_blocks: list[list[int]] = [[] for _ in range(10)]
    gate_truth_rows = 0
    for left, right in combinations(range(10), 2):
        bits = tuple(edge(3 * left, 3 * right + offset) for offset in range(3))
        gates: dict[int, tuple[int, int, int]] = {}
        for color in sorted({colors[left], colors[right]}):
            one, two, complete = next_variable + 1, next_variable + 2, next_variable + 3
            next_variable += 3
            gates[color] = (one, two, complete)
            for values in product((0, 1), repeat=3):
                weight = sum(value == color for value in values)
                deficit = 2 if weight in (0, 3) else 2 - weight
                falsified_assignment = [
                    -variable if value else variable for variable, value in zip(bits, values)
                ]
                add(falsified_assignment + [one if deficit >= 1 else -one])
                add(falsified_assignment + [two if deficit >= 2 else -two])
                add(falsified_assignment + [complete if weight == 3 else -complete])
                gate_truth_rows += 1
        for endpoint in (left, right):
            one, two, complete = gates[colors[endpoint]]
            deficits[endpoint].extend((one, two))
            complete_blocks[endpoint].append(complete)
        if left == 0:
            add((-bits[1], bits[0]))
            add((-bits[2], bits[1]))

    for row in deficits:
        require(len(row) == 18, "wrong deficit-token row")
        for seven in combinations(row, 7):
            add(-literal for literal in seven)

    def at_most(inputs: list[int], bound: int) -> None:
        nonlocal next_variable
        cells: dict[tuple[int, int], int] = {}
        for prefix in range(1, len(inputs) + 1):
            for threshold in range(1, min(prefix, bound + 1) + 1):
                next_variable += 1
                cells[prefix, threshold] = next_variable
        for prefix, literal in enumerate(inputs, 1):
            for threshold in range(1, min(prefix, bound + 1) + 1):
                cell = cells[prefix, threshold]
                if threshold == 1:
                    add((-literal, cell))
                if (prefix - 1, threshold) in cells:
                    add((-cells[prefix - 1, threshold], cell))
                if threshold > 1 and (prefix - 1, threshold - 1) in cells:
                    add((-literal, -cells[prefix - 1, threshold - 1], cell))
        if (len(inputs), bound + 1) in cells:
            add((-cells[len(inputs), bound + 1],))

    triangle_pairs = tuple(combinations(range(10), 2))
    for triangle in range(10):
        own_sign = 1 if triangle < red_cycles else -1
        fixed_own = [own_sign * edge(3 * triangle, fixed) for fixed in range(30, 43)]
        common = fixed_own + [gate for gate in complete_blocks[triangle] for _ in range(3)]
        require(len(common) == 40, "wrong common-neighborhood counter input")
        at_most(common, 4)
        moving_own = [
            own_sign * edge(3 * left, 3 * right + offset)
            for left, right in triangle_pairs if triangle in (left, right)
            for offset in range(3)
        ]
        outside_own = fixed_own + moving_own
        require(len(outside_own) == 40, "wrong moving-degree counter input")
        at_most([-literal for literal in outside_own], 24)

    for fixed in range(30, 43):
        incident = [edge(fixed, other) for other in range(30, 43) if other != fixed]
        incident.extend(edge(3 * moving, fixed) for moving in range(10) for _ in range(3))
        require(len(incident) == 42, "wrong fixed-degree counter input")
        at_most(incident, 24)
        at_most([-literal for literal in incident], 24)

    for fixed in range(30, 42):
        left = [edge(3 * moving, fixed) for moving in range(10)]
        right = [edge(3 * moving, fixed + 1) for moving in range(10)]
        for position in range(10):
            for prefix in product((0, 1), repeat=position):
                row: list[int] = []
                for coordinate, value in enumerate(prefix):
                    row.extend((-left[coordinate], -right[coordinate])
                               if value else (left[coordinate], right[coordinate]))
                row.extend((-left[position], right[position]))
                add(row)

    return next_variable, clauses, {
        "edge_orbits": orbit_count,
        "five_sets": five_sets,
        "ramsey_clauses": ramsey_clauses,
        "gate_truth_rows": gate_truth_rows,
    }


def compare_dimacs(red_cycles: int, path: Path) -> dict[str, object]:
    variables, clauses, audit = reconstruct_formula(red_cycles)
    expected_variables, expected_clauses, expected_sha = EXPECTED[red_cycles]
    require((variables, len(clauses)) == (expected_variables, expected_clauses),
            f"independent dimensions differ for r={red_cycles}")
    info = file_info(path)
    require(info["sha256"] == expected_sha, f"formula digest differs for r={red_cycles}")
    ordered = sorted(clauses, key=lambda clause: (len(clause), clause))
    with path.open() as stream:
        require(stream.readline() == f"p cnf {variables} {len(ordered)}\n",
                f"formula header differs for r={red_cycles}")
        for index, expected in enumerate(ordered, 1):
            values = tuple(map(int, stream.readline().split()))
            require(values and values[-1] == 0 and values[:-1] == expected,
                    f"canonical formula mismatch at clause {index}, r={red_cycles}")
        require(stream.readline() == "", f"trailing formula data for r={red_cycles}")
    audit.update({
        "red_cycles": red_cycles,
        "variables": variables,
        "clauses": len(clauses),
        "formula": info,
        "exact_canonical_match": True,
    })
    return audit


def replay(red_cycles: int, formula: Path, proof: Path, checker: Path, work: Path) -> dict[str, object]:
    proof_info = file_info(proof)
    reference_bytes, reference_sha = REFERENCE_PROOFS[red_cycles]
    require(proof_info == {"bytes": reference_bytes, "sha256": reference_sha},
            f"regenerated proof differs for r={red_cycles}")
    log = work / f"review_replay_r{red_cycles}.log"
    with log.open("w") as output:
        process = subprocess.run(
            [str(checker), str(formula), str(proof), "-t", "240"],
            stdout=output,
            stderr=subprocess.STDOUT,
            timeout=360,
        )
    text = log.read_text()
    require(process.returncode == 0 and "s VERIFIED" in text,
            f"independent DRAT replay failed for r={red_cycles}")
    return {
        "red_cycles": red_cycles,
        "proof": proof_info,
        "drat_trim_verified": True,
    }


def local_arithmetic() -> dict[str, int]:
    feasible = 0
    deficit_only_false = 0
    for weights in product(range(4), repeat=9):
        complete = weights.count(3)
        deficit = sum(2 - weight + 3 * (weight == 3) for weight in weights)
        admissible = [fixed for fixed in range(14)
                      if fixed + 3 * complete <= 4
                      and 18 <= 2 + fixed + sum(weights) <= 24]
        require(bool(admissible) == (deficit <= 6 and complete <= 1),
                "local interval equivalence failed")
        feasible += len(admissible)
        deficit_only_false += deficit <= 6 and not admissible
    require((feasible, deficit_only_false) == (10679, 1380),
            "local arithmetic census differs")
    return {
        "weight_vectors": 4 ** 9,
        "fixed_count_pairs": 14 * 4 ** 9,
        "feasible_pairs": feasible,
        "deficit_only_false_vectors": deficit_only_false,
    }


def normalization_audit() -> dict[str, int]:
    rotations_checked = 0
    for word in product((0, 1), repeat=3):
        rotations = [word[shift:] + word[:shift] for shift in range(3)]
        require(any(candidate == tuple(sorted(candidate, reverse=True)) for candidate in rotations),
                "binary anchor word lacks a normalized rotation")
        rotations_checked += len(rotations)
    require({min(red, 10 - red) for red in range(11)} == set(range(6)),
            "complemented internal-color cases are incomplete")

    lex_checked = 0
    for left in product((0, 1), repeat=4):
        for right in product((0, 1), repeat=4):
            clauses = []
            for position in range(4):
                for prefix in product((0, 1), repeat=position):
                    row = []
                    for coordinate, value in enumerate(prefix):
                        row.extend((not left[coordinate], not right[coordinate])
                                   if value else (left[coordinate], right[coordinate]))
                    row.extend((not left[position], right[position]))
                    clauses.append(any(row))
            require(all(clauses) == (left <= right), "lexicographic clauses differ")
            lex_checked += 1
    return {"three_bit_rotations_checked": rotations_checked,
            "internal_red_counts_covered": 6,
            "lexicographic_assignments_checked": lex_checked}


def fixture_audit() -> dict[str, object]:
    path = TARGET / "moving30.edges"
    require(file_info(path) == {
        "bytes": 1163,
        "sha256": "464e148ef328230b5937ab3f8eacf833653d87e6f749424b8319784a3d256fdf",
    }, "moving fixture digest differs")
    lines = path.read_text().splitlines()
    require(lines[0] == "30 219" and len(lines) == 220, "moving fixture dimensions differ")
    red = {tuple(map(int, line.split())) for line in lines[1:]}
    require(len(red) == 219 and all(0 <= a < b < 30 for a, b in red),
            "moving fixture edge list is malformed")
    bad = 0
    checked = 0
    for vertices in combinations(range(30), 5):
        checked += 1
        red_pairs = sum(pair in red for pair in combinations(vertices, 2))
        bad += red_pairs in (0, 10)
    require(checked == 142506 and bad == 0, "moving fixture has a monochromatic K5")
    rotation = [3 * (v // 3) + (v + 1) % 3 for v in range(30)]
    require({tuple(sorted((rotation[a], rotation[b]))) for a, b in red} == red,
            "moving fixture is not invariant")
    return {"vertices": 30, "red_edges": len(red), "five_sets_checked": checked,
            "monochromatic_five_sets": bad, "rotation_invariant": True}


def anchor_audit() -> dict[str, int]:
    rows = set()
    for red_weights in combinations_with_replacement(range(3), 3):
        for blue_weights in combinations_with_replacement(range(4), 6):
            weights = red_weights + blue_weights
            if weights.count(3) <= 1 and sum(2 - w + 3 * (w == 3) for w in weights) <= 6:
                rows.add(weights)
    stored = json.loads((TARGET / "anchor_r4.json").read_text())
    require(stored["red_cycles"] == 4 and stored["blue_cycles"] == 6,
            "anchor split metadata differs")
    require(rows == {tuple(row) for row in stored["weights"]} and len(rows) == 98,
            "anchor frontier differs")
    return {"canonical_profiles": len(rows)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    work = args.work.resolve()
    checker = args.drat_trim.resolve()
    require(checker.is_file(), "missing DRAT checker")

    report: dict[str, object] = {
        "local_arithmetic": local_arithmetic(),
        "normalization": normalization_audit(),
        "fixture": fixture_audit(),
        "anchor_frontier": anchor_audit(),
        "formulas": [],
        "certificate_replays": [],
        "drat_trim": file_info(checker),
    }
    for red_cycles in range(6):
        formula = work / f"full_r{red_cycles}.cnf"
        require(formula.is_file(), f"missing generated formula r={red_cycles}")
        report["formulas"].append(compare_dimacs(red_cycles, formula))
        print(f"FORMULA r={red_cycles} exact canonical match")
        if red_cycles in EXCLUDED:
            proof = work / f"full_r{red_cycles}.drat"
            require(proof.is_file(), f"missing generated proof r={red_cycles}")
            report["certificate_replays"].append(
                replay(red_cycles, formula, proof, checker, work)
            )
            print(f"PROOF r={red_cycles} DRAT verified")
        else:
            require(red_cycles == 4, "unexpected unresolved case")

    report["excluded_red_counts"] = list(EXCLUDED)
    report["unresolved_red_counts"] = [4]
    report["all_claimed_exclusions_verified"] = True
    if args.report:
        args.report.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print("PASS independent split review: r=0,1,2,3,5 verified; r=4 remains open")


if __name__ == "__main__":
    main()
