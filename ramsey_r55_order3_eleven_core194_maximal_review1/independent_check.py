#!/usr/bin/env python3
"""Independent definition-level review of the Core194 maximal branch."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from itertools import combinations, permutations, product
from pathlib import Path


CORE_BITS = "100110110110110100"
SEED_SHA256 = "41d4c7939f74d60ff1716787923afca5349829cc90fd5c79be95f8c1e82b1178"
PRIOR_BOUNDARY_SHA256 = "9195e8c27426bd7829814c5e085fdd03fa623753faa6153a9654219576bfedd4"
CLASSIFICATION_SHA256 = "4702868099d8670de2bf989e0c87573ac22437adae6dd887dddb9693d6711eee"
EXTENSION_SHA256 = "847412ca901bafa697deca4011e5e21e68448c5b403bc473095436d93ff16f8d"
CLASSIFICATION_PROOF_SHA256 = "f1ec8b1b91feead05e56f04b066a17d9b5244ee0bda444dc893a2a995182a0ff"
EXTENSION_PROOF_SHA256 = "8f724078ce768c89ab2a41267097020b33a2a3578f497b4fa0b802b8a559c7a3"
WORDS_SHA256 = "1dde3b1dbff2d04201427a7114b147a1560c12618037cedf5efdf57dd0be0748"
EXPECTED_REPRESENTATIVES = (
    "7ddf8dd2a8c94eb7b48d9",
    "7ddfaa8cdd094eb7b48d9",
    "bf5fa5caa5498f37b48d9",
    "bf5faa565c898f37b48d9",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> dict[str, int | str]:
    data = path.read_bytes()
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def read_seed(path: Path) -> frozenset[tuple[int, int]]:
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == SEED_SHA256, "unexpected seed identity")
    lines = raw.decode("ascii").splitlines()
    require(lines and lines[0] == "24 156", "unexpected seed header")
    edges: set[tuple[int, int]] = set()
    for line in lines[1:]:
        fields = line.split()
        require(len(fields) == 2, "malformed seed row")
        a, b = map(int, fields)
        require(0 <= a < b < 24 and (a, b) not in edges, "invalid seed edge")
        edges.add((a, b))
    require(len(edges) == 156, "unexpected seed edge count")
    return frozenset(edges)


def step(vertex: int) -> int:
    if vertex >= 33:
        return vertex
    cycle, phase = divmod(vertex, 3)
    return 3 * cycle + (phase + 1) % 3


def edge_orbits(n: int, seed: frozenset[tuple[int, int]]) -> tuple[dict[tuple[int, int], bool | int], list[tuple[tuple[int, int], ...]]]:
    remaining = set(combinations(range(n), 2))
    unknown: list[tuple[tuple[int, int], ...]] = []
    constants: dict[tuple[int, int], bool] = {}
    while remaining:
        start = min(remaining)
        orbit: set[tuple[int, int]] = set()
        pair = start
        while pair not in orbit:
            orbit.add(pair)
            pair = tuple(sorted((step(pair[0]), step(pair[1]))))
        remaining.difference_update(orbit)
        a, b = start
        constant: bool | None = None
        if n == 24 and a // 3 == b // 3:
            constant = a < 12
        elif n == 43 and b < 24:
            constant = start in seed
        elif n == 43 and 33 in start:
            other = b if a == 33 else a
            constant = other >= 24
        elif n == 43 and b < 33 and a // 3 == b // 3:
            constant = False
        if constant is None:
            unknown.append(tuple(sorted(orbit)))
        else:
            constants.update({edge: constant for edge in orbit})
    unknown.sort(key=lambda orbit: orbit[0])
    result: dict[tuple[int, int], bool | int] = dict(constants)
    for variable, orbit in enumerate(unknown, 1):
        for edge in orbit:
            result[edge] = variable
    require(len(result) == n * (n - 1) // 2, "edge orbit partition is incomplete")
    return result, unknown


def monochromatic_clauses(
    n: int,
    edges: dict[tuple[int, int], bool | int],
    size: int,
    red: bool,
) -> set[tuple[int, ...]]:
    clauses: set[tuple[int, ...]] = set()
    for vertices in combinations(range(n), size):
        literals: set[int] = set()
        possible = True
        for edge in combinations(vertices, 2):
            value = edges[edge]
            if isinstance(value, bool):
                if value != red:
                    possible = False
                    break
            else:
                literals.add(-value if red else value)
        if possible:
            clauses.add(tuple(sorted(literals)))
    require(() not in clauses, "fixed monochromatic clique found")
    return clauses


def local_columns(edges: dict[tuple[int, int], bool | int]) -> list[list[int]]:
    columns: list[list[int]] = []
    for blue_cycle in range(4, 8):
        column = []
        for red_cycle in range(4):
            for phase in range(3):
                value = edges[(3 * red_cycle, 3 * blue_cycle + phase)]
                require(type(value) is int, "contact is not a primary variable")
                column.append(value)
        columns.append(column)
    return columns


def rotate_contact(bits: tuple[int, ...], shift: int) -> tuple[int, ...]:
    return tuple(bits[3 * block + (phase + shift) % 3] for block in range(4) for phase in range(3))


def phase_clauses(columns: list[list[int]]) -> list[tuple[int, ...]]:
    bad_words = []
    for mask in range(1 << 12):
        bits = tuple((mask >> (11 - position)) & 1 for position in range(12))
        if bits != min(rotate_contact(bits, shift) for shift in range(3)):
            bad_words.append(bits)
    require(len(bad_words) == 2720, "unexpected nonminimal phase count")
    return [
        tuple(-variable if bit else variable for variable, bit in zip(column, bits))
        for column in columns
        for bits in bad_words
    ]


def ordering_clauses(columns: list[list[int]]) -> tuple[list[tuple[int, ...]], int]:
    rows: list[tuple[int, ...]] = []
    top = 84
    for left, right in zip(columns, columns[1:]):
        previous: int | None = None
        for position, (a, b) in enumerate(zip(left, right)):
            prefix = [-previous] if previous is not None else []
            rows.append(tuple(prefix + [-a, b]))
            if position == 11:
                continue
            top += 1
            q = top
            if previous is not None:
                rows.append((-q, previous))
            rows.extend(
                [
                    (-q, -a, b),
                    (-q, a, -b),
                    tuple(prefix + [-a, -b, q]),
                    tuple(prefix + [a, b, q]),
                ]
            )
            previous = q
    require(top == 117 and len(rows) == 198, "unexpected comparator encoding size")
    return rows, top


def formula_bytes(variables: int, clauses: list[tuple[int, ...]]) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


def graph_from_word(word: str, local_edges: dict[tuple[int, int], bool | int]) -> frozenset[tuple[int, int]]:
    require(len(word) == 21 and all(character in "0123456789abcdef" for character in word), "malformed representative word")
    mask = int(word, 16)
    return frozenset(
        edge
        for edge, value in local_edges.items()
        if (value if isinstance(value, bool) else bool(mask & (1 << (value - 1))))
    )


def literal_graph_checks(red: frozenset[tuple[int, int]]) -> dict[str, object]:
    require(all(((step(a), step(b)) if step(a) < step(b) else (step(b), step(a))) in red for a, b in red), "seed is not invariant")
    for cycle in range(8):
        expected = cycle < 4
        for a, b in combinations(range(3 * cycle, 3 * cycle + 3), 2):
            require(((a, b) in red) == expected, "unexpected internal cycle color")
    require(
        not any(all(edge in red for edge in combinations(vertices, 2)) for vertices in combinations(range(24), 5)),
        "red K5 in local graph",
    )
    require(
        not any(all(edge not in red for edge in combinations(vertices, 2)) for vertices in combinations(range(24), 4)),
        "blue K4 in local graph",
    )
    bits = "".join(
        "1" if (3 * i, 3 * j + phase) in red else "0"
        for i, j in combinations(range(4), 2)
        for phase in range(3)
    )
    require(bits == CORE_BITS, "wrong Core194 bits")
    degrees = [sum(tuple(sorted((vertex, other))) in red for other in range(24) if other != vertex) for vertex in range(24)]
    return {"red_edges": len(red), "red_degrees": degrees, "red_K5": 0, "blue_K4": 0}


def derived_representatives(seed: frozenset[tuple[int, int]], local_edges: dict[tuple[int, int], bool | int]) -> tuple[list[dict[str, object]], int]:
    records: dict[str, list[int]] = {}
    stabilizer = 0
    for cycle_permutation in permutations(range(4)):
        for phases in product(range(3), repeat=4):
            pullback = [
                3 * cycle_permutation[cycle] + (phase + phases[cycle]) % 3
                for cycle in range(4)
                for phase in range(3)
            ]
            preserved = True
            for offset, (i, j, phase) in enumerate(
                (triple for i, j in combinations(range(4), 2) for phase in range(3) for triple in [(i, j, phase)])
            ):
                edge = tuple(sorted((pullback[3 * i], pullback[3 * j + phase])))
                if ((edge in seed) != (CORE_BITS[offset] == "1")):
                    preserved = False
                    break
            if not preserved:
                continue
            stabilizer += 1
            contacts = []
            for blue_cycle in range(4, 8):
                options = []
                for shift in range(3):
                    contact = tuple(
                        int(tuple(sorted((pullback[3 * red_cycle], 3 * blue_cycle + (phase + shift) % 3))) in seed)
                        for red_cycle in range(4)
                        for phase in range(3)
                    )
                    options.append((contact, shift))
                contact, shift = min(options)
                contacts.append((contact, blue_cycle, shift))
            for _contact, blue_cycle, shift in sorted(contacts):
                pullback.extend(3 * blue_cycle + (phase + shift) % 3 for phase in range(3))
            word_value = 0
            for edge, variable in local_edges.items():
                if type(variable) is not int:
                    continue
                image = tuple(sorted((pullback[edge[0]], pullback[edge[1]])))
                if image in seed:
                    word_value |= 1 << (variable - 1)
            word = f"{word_value:021x}"
            if word not in records or pullback < records[word]:
                records[word] = pullback
    require(stabilizer == 24, "unexpected Core194 stabilizer")
    require(tuple(sorted(records)) == EXPECTED_REPRESENTATIVES, "unexpected normalized representatives")
    return ([{"word": word, "pullback_permutation": records[word]} for word in sorted(records)], stabilizer)


def verify_representative_file(path: Path, derived: list[dict[str, object]], stabilizer: int, seed: frozenset[tuple[int, int]], local_edges: dict[tuple[int, int], bool | int]) -> list[frozenset[tuple[int, int]]]:
    supplied = json.loads(path.read_text())
    require(supplied == {"red_stabilizer": stabilizer, "representatives": derived}, "representative file differs from independent derivation")
    graphs = []
    for record in derived:
        graph = graph_from_word(str(record["word"]), local_edges)
        checks = literal_graph_checks(graph)
        require(checks["red_degrees"] == [13] * 24, "representative is not red 13-regular")
        permutation = record["pullback_permutation"]
        require(sorted(permutation) == list(range(24)), "invalid pullback permutation")
        require(all((vertex < 12) == (permutation[vertex] < 12) for vertex in range(24)), "pullback exchanges color parts")
        require(all(permutation[step(vertex)] == step(permutation[vertex]) for vertex in range(24)), "pullback does not commute with action")
        require(
            all((edge in graph) == (tuple(sorted((permutation[edge[0]], permutation[edge[1]]))) in seed) for edge in combinations(range(24), 2)),
            "pullback does not map representative to seed",
        )
        graphs.append(graph)
    return graphs


def blue_orbit_check(graphs: list[frozenset[tuple[int, int]]], local_edges: dict[tuple[int, int], bool | int]) -> dict[str, object]:
    all_words: set[int] = set()
    orbit_sizes = []
    for graph in graphs:
        orbit: set[int] = set()
        for permuted_cycles in permutations(range(4, 8)):
            for phases in product(range(3), repeat=4):
                pullback = list(range(12))
                for position in range(4):
                    pullback.extend(3 * permuted_cycles[position] + (phase + phases[position]) % 3 for phase in range(3))
                word = 0
                for edge, variable in local_edges.items():
                    if type(variable) is not int:
                        continue
                    image = tuple(sorted((pullback[edge[0]], pullback[edge[1]])))
                    if image in graph:
                        word |= 1 << (variable - 1)
                orbit.add(word)
        require(len(orbit) == 1944, "blue-cycle action is not free")
        require(not (orbit & all_words), "canonical representative orbits overlap")
        orbit_sizes.append(len(orbit))
        all_words.update(orbit)
    encoded = "".join(f"{word:021x}\n" for word in sorted(all_words)).encode("ascii")
    require(len(all_words) == 7776, "unexpected labeled local-family size")
    require(hashlib.sha256(encoded).hexdigest() == WORDS_SHA256, "unexpected local-family digest")
    return {"orbit_sizes": orbit_sizes, "labeled_local_graphs": len(all_words), "words_sha256": hashlib.sha256(encoded).hexdigest()}


def clauses_satisfied(clauses: list[tuple[int, ...]], values: dict[int, bool]) -> bool:
    return all(any(values[abs(literal)] == (literal > 0) for literal in clause) for clause in clauses)


def normalization_semantics(columns: list[list[int]], phase_rows: list[tuple[int, ...]], order_rows: list[tuple[int, ...]]) -> dict[str, int]:
    bad_first = set(phase_rows[:2720])
    phase_words = 0
    for mask in range(1 << 12):
        bits = tuple((mask >> (11 - position)) & 1 for position in range(12))
        assignment_clause = tuple(-variable if bit else variable for variable, bit in zip(columns[0], bits))
        allowed = assignment_clause not in bad_first
        require(allowed == (bits == min(rotate_contact(bits, shift) for shift in range(3))), "phase-normalization semantics failed")
        phase_words += 1
    comparator_pairs = 0
    first_comparator = order_rows[:66]
    for left_bits in product((0, 1), repeat=6):
        for right_bits in product((0, 1), repeat=6):
            left = left_bits + (0,) * 6
            right = right_bits + (0,) * 6
            values = {variable: bool(bit) for variable, bit in zip(columns[0], left)}
            values.update({variable: bool(bit) for variable, bit in zip(columns[1], right)})
            for position in range(11):
                values[85 + position] = left[: position + 1] == right[: position + 1]
            require(clauses_satisfied(first_comparator, values) == (left <= right), "lexicographic comparator semantics failed")
            comparator_pairs += 1
    return {"phase_words": phase_words, "six_bit_comparator_pairs": comparator_pairs}


def construct_formulas(seed: frozenset[tuple[int, int]], representatives: list[dict[str, object]]) -> tuple[dict[str, bytes], dict[str, object]]:
    local_edges, local_orbits = edge_orbits(24, seed)
    require(len(local_orbits) == 84, "unexpected local primary count")
    local_red = monochromatic_clauses(24, local_edges, 5, True)
    local_blue = monochromatic_clauses(24, local_edges, 4, False)
    local_base = sorted(local_red | local_blue)
    core_variables = [
        local_edges[(3 * i, 3 * j + phase)]
        for i, j in combinations(range(4), 2)
        for phase in range(3)
    ]
    require(all(type(variable) is int for variable in core_variables), "Core194 edge is not variable")
    core_rows = [(variable if bit == "1" else -variable,) for variable, bit in zip(core_variables, CORE_BITS)]
    columns = local_columns(local_edges)
    phases = phase_clauses(columns)
    ordering, local_variables = ordering_clauses(columns)
    blockers = [
        tuple(-(variable + 1) if int(str(record["word"]), 16) & (1 << variable) else variable + 1 for variable in range(84))
        for record in representatives
    ]
    unblocked_rows = local_base + core_rows + phases + ordering
    for record in representatives:
        mask = int(str(record["word"]), 16)
        values = {variable: bool(mask & (1 << (variable - 1))) for variable in range(1, 85)}
        for comparator, (left, right) in enumerate(zip(columns, columns[1:])):
            for position in range(11):
                values[85 + 11 * comparator + position] = all(
                    values[left[index]] == values[right[index]] for index in range(position + 1)
                )
        require(clauses_satisfied(unblocked_rows, values), "canonical representative lacks a normalization extension")
        require(sum(not clauses_satisfied([blocker], values) for blocker in blockers) == 1, "blockers do not isolate representatives")
    local_rows = local_base + core_rows + phases + ordering + blockers
    local_data = formula_bytes(local_variables, local_rows)
    require(len(local_base) + len(core_rows) == 11584, "unexpected local Ramsey/core base size")
    require(len(local_rows) == 22666, "unexpected classification clause count")
    require(hashlib.sha256(local_data).hexdigest() == CLASSIFICATION_SHA256, "classification formula digest mismatch")

    full_edges, full_orbits = edge_orbits(43, seed)
    require(len(full_orbits) == 216, "unexpected extension primary count")
    require(all(full_edges[edge] == (edge in seed) for edge in combinations(range(24), 2)), "full formula does not fix the seed exactly")
    require(all(full_edges[(vertex, 33)] is False for vertex in range(24)), "distinguished vertex is not blue to H")
    require(all(full_edges[tuple(sorted((vertex, 33)))] is True for vertex in list(range(24, 33)) + list(range(34, 43))), "distinguished vertex is not red outside H")
    require(all(len(orbit) in (1, 3) for orbit in full_orbits), "unexpected physical orbit size")
    full_red = monochromatic_clauses(43, full_edges, 5, True)
    full_blue = monochromatic_clauses(43, full_edges, 5, False)
    full_rows = sorted(full_red | full_blue)
    full_data = formula_bytes(216, full_rows)
    require(len(full_rows) == 131652, "unexpected extension clause count")
    require(hashlib.sha256(full_data).hexdigest() == EXTENSION_SHA256, "extension formula digest mismatch")
    return (
        {"classification": local_data, "extension": full_data},
        {
            "classification": {
                "variables": local_variables,
                "clauses": len(local_rows),
                "base_clauses": len(local_base) + len(core_rows),
                "ramsey_clauses": len(local_base),
                "red_forbidden_clauses": len(local_red),
                "blue_forbidden_clauses": len(local_blue),
                "core_units": len(core_rows),
                "phase_clauses": len(phases),
                "order_clauses": len(ordering),
                "blockers": len(blockers),
                "representatives_satisfying_unblocked_formula": len(representatives),
                "normalization_semantics": normalization_semantics(columns, phases, ordering),
            },
            "extension": {
                "variables": 216,
                "clauses": len(full_rows),
                "red_forbidden_clauses": len(full_red),
                "blue_forbidden_clauses": len(full_blue),
                "constant_red_pairs": sum(value is True for value in full_edges.values()),
                "constant_blue_pairs": sum(value is False for value in full_edges.values()),
                "variable_pair_orbits": len(full_orbits),
                "variable_orbit_sizes": {
                    "1": sum(len(orbit) == 1 for orbit in full_orbits),
                    "3": sum(len(orbit) == 3 for orbit in full_orbits),
                },
            },
        },
    )


def write_or_compare(path: Path, data: bytes, generate: bool) -> dict[str, int | str]:
    if generate:
        path.write_bytes(data)
    require(path.read_bytes() == data, f"formula mismatch: {path}")
    return digest(path)


def proof_check(proof: Path, solve_log: Path, replay_log: Path, expected_hash: str, solver_exit: int) -> dict[str, object]:
    require(solver_exit == 20, "solver exit was not UNSAT")
    require("s UNSATISFIABLE" in solve_log.read_text(errors="replace"), "solver log lacks UNSAT status")
    replay = replay_log.read_text(errors="replace")
    match = re.search(r"(\d+) RAT lemmas in core", replay)
    require("s VERIFIED" in replay and match is not None, "proof replay did not verify in full mode")
    identity = digest(proof)
    return {
        "solver_exit_code": solver_exit,
        "proof": identity,
        "matches_published_proof": identity["sha256"] == expected_hash,
        "replay_verified": True,
        "rat_core_lemmas": int(match.group(1)),
    }


def reduction_check() -> dict[str, object]:
    valid = []
    for blue_cycles in range(8):
        for red_fixed in range(10):
            red_degree = 3 * (7 - blue_cycles) + red_fixed
            blue_degree = 21 + 3 * blue_cycles - red_fixed
            if 18 <= red_degree <= 24 and 18 <= blue_degree <= 24:
                valid.append([blue_cycles, red_fixed, red_degree, blue_degree])
    require(max(row[0] for row in valid) == 4, "degree window does not give b<=4")
    maximal = [row for row in valid if row[0] == 4]
    require(maximal == [[4, 9, 18, 24]], "unexpected maximal degree case")
    return {"valid_pairs": valid, "maximum_blue_cycles": 4, "maximal_pair": maximal[0]}


def boundary_check(cover_path: Path, prior_path: Path, source_boundary_path: Path) -> dict[str, object]:
    require(digest(prior_path)["sha256"] == PRIOR_BOUNDARY_SHA256, "unexpected prior boundary identity")
    cover = json.loads(cover_path.read_text())
    prior = json.loads(prior_path.read_text())
    source = json.loads(source_boundary_path.read_text())
    cases = [case for case in cover["cases"] if case["index"] == 194]
    require(len(cases) == 1, "Core194 cover entry missing")
    case = cases[0]
    require(case["bits"] == CORE_BITS and case["labeled"] == 81, "Core194 cover metadata mismatch")
    require(cover["classes"] == 197 and cover["labeled_valid"] == 115543, "core-cover totals mismatch")
    require(prior["remaining_maximal_full_branches"] == [194], "Core194 was not the sole prior maximal branch")
    require(source["new_maximal_branch_exclusions"] == [194] and source["new_whole_core_exclusions"] == [], "source scope mismatch")
    require(source["remaining_full_classes"] == prior["remaining_full_classes"] == 17, "whole-core class boundary changed")
    require(source["remaining_full_labeled"] == prior["remaining_full_labeled"] == 9153, "whole-core labeled boundary changed")
    require(source["remaining_maximal_full_branches"] == [], "maximal branch remains in source boundary")
    return {
        "core_index": 194,
        "core_bits": case["bits"],
        "labeled_multiplicity": case["labeled"],
        "prior_maximal_branches": prior["remaining_maximal_full_branches"],
        "new_maximal_branch_exclusions": source["new_maximal_branch_exclusions"],
        "new_whole_core_exclusions": source["new_whole_core_exclusions"],
        "remaining_full_classes": source["remaining_full_classes"],
        "remaining_full_labeled": source["remaining_full_labeled"],
        "cumulative_full_classes_excluded": source["cumulative_full_classes_excluded"],
        "cumulative_full_labeled_excluded": source["cumulative_full_labeled_excluded"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--cover", type=Path, required=True)
    parser.add_argument("--prior-boundary", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--classification-proof", type=Path)
    parser.add_argument("--classification-solve-log", type=Path)
    parser.add_argument("--classification-replay-log", type=Path)
    parser.add_argument("--classification-solver-exit", type=int)
    parser.add_argument("--extension-proof", type=Path)
    parser.add_argument("--extension-solve-log", type=Path)
    parser.add_argument("--extension-replay-log", type=Path)
    parser.add_argument("--extension-solver-exit", type=int)
    parser.add_argument("--kissat", type=Path)
    parser.add_argument("--drat-trim", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)

    seed = read_seed(args.seed)
    seed_summary = literal_graph_checks(seed)
    local_edges, _ = edge_orbits(24, seed)
    representatives, stabilizer = derived_representatives(seed, local_edges)
    graphs = verify_representative_file(args.source / "representatives.json", representatives, stabilizer, seed, local_edges)
    orbit_summary = blue_orbit_check(graphs, local_edges)
    formulas, formula_summary = construct_formulas(seed, representatives)
    formula_identities = {
        kind: write_or_compare(args.work / f"{kind}.review1.cnf", data, args.generate)
        for kind, data in formulas.items()
    }
    require(formula_identities["classification"]["sha256"] == CLASSIFICATION_SHA256, "classification identity changed")
    require(formula_identities["extension"]["sha256"] == EXTENSION_SHA256, "extension identity changed")

    proof_args = [
        args.classification_proof,
        args.classification_solve_log,
        args.classification_replay_log,
        args.classification_solver_exit,
        args.extension_proof,
        args.extension_solve_log,
        args.extension_replay_log,
        args.extension_solver_exit,
    ]
    have_proofs = all(value is not None for value in proof_args)
    require(have_proofs or not any(value is not None for value in proof_args), "partial proof evidence supplied")
    proofs = None
    if have_proofs:
        proofs = {
            "classification": proof_check(
                args.classification_proof,
                args.classification_solve_log,
                args.classification_replay_log,
                CLASSIFICATION_PROOF_SHA256,
                args.classification_solver_exit,
            ),
            "extension": proof_check(
                args.extension_proof,
                args.extension_solve_log,
                args.extension_replay_log,
                EXTENSION_PROOF_SHA256,
                args.extension_solver_exit,
            ),
        }
        require(all(row["rat_core_lemmas"] == 0 for row in proofs.values()), "unexpected RAT core lemmas")

    tools = None
    if args.kissat is not None or args.drat_trim is not None:
        require(args.kissat is not None and args.drat_trim is not None, "partial tool identities supplied")
        tools = {"kissat": digest(args.kissat), "drat_trim": digest(args.drat_trim)}

    result = {
        "all_checks_passed": True,
        "verdict_supported": have_proofs,
        "scope": "Core194 maximal b=4 attachment branch only; no whole-core exclusion",
        "reduction": reduction_check(),
        "seed": {"identity": digest(args.seed), **seed_summary},
        "classification": {
            "red_core_stabilizer": stabilizer,
            "canonical_representatives": [record["word"] for record in representatives],
            **orbit_summary,
            **formula_summary["classification"],
            "formula": formula_identities["classification"],
        },
        "extension": {**formula_summary["extension"], "formula": formula_identities["extension"]},
        "proofs": proofs,
        "tools": tools,
        "boundary": boundary_check(args.cover, args.prior_boundary, args.source / "boundary.json"),
        "source_compact_evidence": {
            "result": digest(args.source / "result.json"),
            "verification": digest(args.source / "verification.json"),
            "representatives": digest(args.source / "representatives.json"),
            "boundary": digest(args.source / "boundary.json"),
        },
        "trust_boundary": [
            "R(4,5)=25 degree window and accepted parent reduction",
            "earlier Core194 seed review and canonical core-cover completeness",
            "unformalized normalization and family-transfer argument",
            "Python runtime, SHA-256, Kissat proof production, and full drat-trim checker",
        ],
    }
    args.report.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS Core194 classification and maximal-branch review" if have_proofs else "PASS Core194 formula and classification precheck")


if __name__ == "__main__":
    main()
