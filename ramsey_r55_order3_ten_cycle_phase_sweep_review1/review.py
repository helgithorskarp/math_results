#!/usr/bin/env python3
"""Clean-room review of the ten-cycle minority-core phase classification.

No module from the contribution under review is imported.  The checker uses
literal graphs for the phase quotient, independently reconstructs the case
tails and certificate support, and can replay every compact DRAT certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from itertools import combinations, product, permutations
from pathlib import Path


BASE_SHA256 = "f01c990a1dae17fb7bc1cd633d785cd819ba9f4d1a1eeacd69b4034663af104e"
MATCHING = {frozenset((0, 1)), frozenset((2, 3))}
PHASE_PAIRS = ((1, 2), (1, 3), (2, 3))
CLASS_REPRESENTATIVES = (
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 2),
    (1, 1, 1),
    (1, 2, 2),
)
EXPECTED_CLASS_SIZES = (1, 4, 8, 8, 4, 2)
ANCHORS = (64, 65, 67, 69)
ANCHOR_WEIGHTS = (
    (1, 2, 2, 1, 1, 1, 1, 2, 2),
    (1, 2, 2, 1, 1, 1, 2, 2, 2),
    (1, 2, 2, 1, 1, 2, 2, 2, 2),
    (1, 2, 2, 1, 2, 2, 2, 2, 2),
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def file_info(path: Path) -> dict[str, object]:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return {"bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def rotated(base: tuple[int, int, int], shift: int) -> tuple[int, int, int]:
    return base[shift:] + base[:shift]


def phase_graph(phase: tuple[int, int, int]) -> dict[tuple[int, int], bool]:
    words = {
        (0, 1): (1, 0, 0),
        (0, 2): (1, 1, 0),
        (0, 3): (1, 1, 0),
        (1, 2): rotated((1, 1, 0), phase[0]),
        (1, 3): rotated((1, 1, 0), phase[1]),
        (2, 3): rotated((1, 0, 0), phase[2]),
    }
    graph = {}
    for a, b in combinations(range(12), 2):
        i, u = divmod(a, 3)
        j, v = divmod(b, 3)
        graph[a, b] = True if i == j else bool(words[i, j][(v - u) % 3])
    return graph


def graph_key(graph: dict[tuple[int, int], bool]) -> tuple[bool, ...]:
    return tuple(graph[edge] for edge in combinations(range(12), 2))


def transform_graph(
    graph: dict[tuple[int, int], bool],
    cycle_permutation: tuple[int, ...],
    orientation: int,
    shifts: tuple[int, ...],
) -> tuple[bool, ...]:
    """Pull back a literal graph through a full normalizer permutation."""
    mapping = [
        3 * cycle_permutation[cycle] + (orientation * coordinate + shifts[cycle]) % 3
        for cycle in range(4)
        for coordinate in range(3)
    ]
    return tuple(
        graph[tuple(sorted((mapping[a], mapping[b])))]
        for a, b in combinations(range(12), 2)
    )


def independent_phase_orbits() -> list[dict[str, object]]:
    phases = list(product(range(3), repeat=3))
    graphs = {phase: phase_graph(phase) for phase in phases}
    lookup = {graph_key(graph): phase for phase, graph in graphs.items()}
    require(len(lookup) == 27, "distinct phase triples produced duplicate graphs")
    stabilizer = [
        perm for perm in permutations(range(4))
        if {frozenset((perm[0], perm[1])), frozenset((perm[2], perm[3]))} == MATCHING
    ]
    require(len(stabilizer) == 8, "wrong matching stabilizer")
    orbits = {}
    maps_tested = 0
    for phase, graph in graphs.items():
        equivalent = set()
        for perm in stabilizer:
            for orientation in (-1, 1):
                for shifts in product(range(3), repeat=4):
                    key = transform_graph(graph, perm, orientation, shifts)
                    target = lookup.get(key)
                    if target is not None:
                        equivalent.add(target)
                    maps_tested += 1
        require(phase in equivalent, "identity equivalence missing")
        orbits[phase] = equivalent
    for phase, orbit in orbits.items():
        require(all(orbits[other] == orbit for other in orbit), "normalizer orbit is not closed")
    unique = sorted({min(orbit) for orbit in orbits.values()})
    require(tuple(unique) == CLASS_REPRESENTATIVES, "phase representatives differ")
    require(tuple(len(orbits[rep]) for rep in unique) == EXPECTED_CLASS_SIZES,
            "phase class sizes differ")
    covered = [phase for rep in unique for phase in sorted(orbits[rep])]
    require(sorted(covered) == phases and len(set(covered)) == 27, "phase quotient is not a partition")
    return [
        {"representative": list(rep), "size": len(orbits[rep]),
         "members": [list(phase) for phase in sorted(orbits[rep])]}
        for rep in unique
    ] + [{"normalizer_maps_tested": maps_tested}]


def inspect_forced_core(source: Path) -> dict[str, object]:
    graph = phase_graph((0, 0, 0))
    lines = (source / "minority_core.edges").read_text().splitlines()
    require(lines[0] == "12 42", "wrong literal-core header")
    stored = {tuple(map(int, line.split())) for line in lines[1:]}
    expected = {edge for edge, red in graph.items() if red}
    require(stored == expected and len(stored) == 42, "literal core differs from theorem")
    degrees = [
        sum(graph[tuple(sorted((vertex, other)))] for other in range(12) if other != vertex)
        for vertex in range(12)
    ]
    require(degrees == [7] * 12, "forced core is not red 7-regular")
    clique_counts = {
        str(color): {
            str(order): sum(
                all(graph[edge] == bool(color) for edge in combinations(vertices, 2))
                for vertices in combinations(range(12), order)
            )
            for order in range(2, 6)
        }
        for color in (0, 1)
    }
    expected_counts = {
        "0": {"2": 24, "3": 0, "4": 0, "5": 0},
        "1": {"2": 42, "3": 52, "4": 18, "5": 0},
    }
    require(clique_counts == expected_counts, "forced-core clique census differs")
    fixed_signatures = []
    for signature in product((False, True), repeat=4):
        extended = dict(graph)
        for vertex in range(12):
            extended[vertex, 12] = signature[vertex // 3]
        valid = not any(
            len({extended[edge] for edge in combinations(vertices, 2)}) == 1
            for vertices in combinations(range(13), 5)
        )
        require(valid == (sum(signature) <= 2), "fixed-signature criterion differs")
        if valid:
            fixed_signatures.append([int(value) for value in signature])
    require(len(fixed_signatures) == 11, "wrong number of local fixed signatures")
    return {
        "red_edges": len(expected),
        "red_degree": degrees[0],
        "clique_counts": clique_counts,
        "permitted_fixed_signatures": len(fixed_signatures),
        "fixed_extensions_checked": 16,
    }


def edge_variables() -> tuple[dict[tuple[int, int], int], int]:
    sigma = tuple(3 * (v // 3) + (v + 1) % 3 if v < 30 else v for v in range(43))
    unseen = set(combinations(range(43), 2))
    orbits = []
    while unseen:
        edge = min(unseen)
        orbit = set()
        while edge not in orbit:
            orbit.add(edge)
            edge = tuple(sorted((sigma[edge[0]], sigma[edge[1]])))
        unseen -= orbit
        orbits.append(tuple(sorted(orbit)))
    cross = sorted(
        (orbit for orbit in orbits if orbit[0][1] < 30 and orbit[0][0] // 3 != orbit[0][1] // 3),
        key=lambda orbit: orbit[0],
    )
    fixed = sorted((orbit for orbit in orbits if orbit[0][0] >= 30), key=lambda orbit: orbit[0])
    links = sorted(
        (orbit for orbit in orbits if orbit[0][0] < 30 <= orbit[0][1]),
        key=lambda orbit: (orbit[0][1], orbit[0][0]),
    )
    require((len(orbits), len(cross), len(fixed), len(links)) == (353, 135, 78, 130),
            "wrong actual pair-orbit census")
    variables = {}
    for number, orbit in enumerate(cross + fixed + links, 1):
        for edge in orbit:
            variables[edge] = number
    return variables, len(orbits)


def falsified_clause(bits: tuple[int, ...], values: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(sorted(-variable if value else variable for variable, value in zip(bits, values)))


def common_tail(variables: dict[tuple[int, int], int]) -> list[tuple[int, ...]]:
    clauses = []
    for left, right in combinations(range(4), 2):
        bits = tuple(variables[3 * left, 3 * right + offset] for offset in range(3))
        required_weight = 1 if frozenset((left, right)) in MATCHING else 2
        for values in product((0, 1), repeat=3):
            if sum(values) != required_weight:
                clauses.append(falsified_clause(bits, values))
    for minority in range(4):
        row = []
        for majority in range(4, 10):
            bits = tuple(variables[3 * minority, 3 * majority + offset] for offset in range(3))
            clauses.extend((tuple(sorted(bits)), tuple(sorted(-bit for bit in bits))))
            gate = 28951 + 6 * minority + majority - 4
            row.append(gate)
            for values in product((0, 1), repeat=3):
                gate_literal = gate if sum(values) == 1 else -gate
                clauses.append(tuple(sorted(falsified_clause(bits, values) + (gate_literal,))))
        clauses.append(tuple(row))
        clauses.extend(tuple(sorted(-gate for gate in subset)) for subset in combinations(row, 5))
    require(len(clauses) == len(set(clauses)) == 298, "wrong common-tail dimensions")
    return clauses


def case_tail(
    phase: tuple[int, int, int],
    weights: tuple[int, ...],
    variables: dict[tuple[int, int], int],
) -> set[tuple[int, ...]]:
    clauses = list(common_tail(variables))
    for block, weight in enumerate(weights, 1):
        for offset in range(3):
            variable = variables[0, 3 * block + offset]
            clauses.append((variable if offset < weight else -variable,))
    graph = phase_graph(phase)
    for left, right in PHASE_PAIRS:
        for offset in range(3):
            edge = (3 * left, 3 * right + offset)
            variable = variables[edge]
            clauses.append((variable if graph[edge] else -variable,))
    result = set(clauses)
    require(len(clauses) == len(result) == 334, "wrong case-tail dimensions")
    return result


def read_core(path: Path) -> list[tuple[int, ...]]:
    lines = path.read_text().splitlines()
    require(bool(lines), f"empty certificate core: {path}")
    header = lines[0].split()
    require(header[:3] == ["p", "cnf", "28974"] and int(header[3]) == len(lines) - 1,
            f"wrong certificate header: {path}")
    clauses = []
    for line in lines[1:]:
        values = [int(token) for token in line.split()]
        require(values and values[-1] == 0, f"missing clause terminator: {path}")
        clause = tuple(sorted(values[:-1]))
        require(all(1 <= abs(literal) <= 28974 for literal in clause), f"literal out of range: {path}")
        require(len(clause) == len(set(clause)) and not any(-literal in clause for literal in clause),
                f"noncanonical certificate clause: {path}")
        clauses.append(clause)
    return clauses


def expected_cases(orbits: list[dict[str, object]]) -> list[dict[str, object]]:
    classes = orbits[:-1]
    cases = []
    for class_index, orbit in enumerate(classes):
        for anchor_index, (anchor, weights) in enumerate(zip(ANCHORS, ANCHOR_WEIGHTS)):
            cases.append({
                "index": 4 * class_index + anchor_index,
                "phase": orbit["representative"],
                "anchor": anchor,
                "weights": list(weights),
            })
    return cases


def check_certificates(
    source: Path,
    base: Path,
    drat_trim: Path,
    work: Path,
    orbits: list[dict[str, object]],
) -> dict[str, object]:
    manifest = json.loads((source / "certificate_manifest.json").read_text())
    cases = expected_cases(orbits)
    sweep = manifest["sweep"]
    require([row["index"] for row in sweep["cases"]] == list(range(24)), "sweep cases are incomplete")
    for observed, expected in zip(sweep["cases"], cases):
        require(all(observed[key] == value for key, value in expected.items()), "sweep case meaning differs")
    require(sweep["excluded_indices"] == list(range(4, 24)), "wrong excluded-index claim")
    require(sweep["open_indices"] == list(range(4)), "wrong open-index claim")
    require(sweep["complete_bounded_sweep"] and not sweep["all_cases_excluded"]
            and not sweep["target_graph_found"], "wrong bounded-sweep scope")
    certificate_rows = manifest["cases"]
    require([row["index"] for row in certificate_rows] == list(range(4, 24)),
            "certificate coverage differs")

    variables, orbit_count = edge_variables()
    require(file_info(base)["sha256"] == BASE_SHA256, "fresh parent formula hash differs")
    wanted = set()
    occurrences = 0
    rat_counts = {}
    work.mkdir(parents=True, exist_ok=True)
    for row in certificate_rows:
        expected = cases[row["index"]]
        require(all(row[key] == value for key, value in expected.items()), "certificate case meaning differs")
        core = source / "certificates" / f"case_{row['index']:02}.cnf"
        proof = source / "certificates" / f"case_{row['index']:02}.drat"
        require(file_info(core) == row["core"] and file_info(proof) == row["proof"],
                "certificate digest differs")
        tail = case_tail(tuple(row["phase"]), tuple(row["weights"]), variables)
        clauses = read_core(core)
        occurrences += len(clauses)
        wanted.update(clause for clause in clauses if clause not in tail)
        log = work / f"replay_{row['index']:02}.log"
        with log.open("w") as output:
            process = subprocess.run(
                [str(drat_trim), str(core), str(proof), "-t", "120"],
                stdout=output,
                stderr=subprocess.STDOUT,
                timeout=180,
            )
        text = log.read_text()
        require(process.returncode == 0 and "s VERIFIED" in text,
                f"independent DRAT replay failed: {row['index']}")
        match = re.search(r"(\d+) RAT lemmas in core", text)
        require(match is not None, "DRAT checker omitted RAT statistic")
        rat = int(match.group(1))
        require(rat == row["rat_core_lemmas"], "RAT count differs")
        rat_counts[str(row["index"])] = rat

    obligations = len(wanted)
    with base.open("r") as stream:
        require(stream.readline() == "p cnf 28950 927000\n", "wrong fresh parent header")
        for line in stream:
            literals = tuple(int(token) for token in line.split())
            require(literals and literals[-1] == 0, "malformed parent clause")
            wanted.discard(tuple(sorted(literals[:-1])))
    require(not wanted, "certificate core contains a clause outside its own formula")
    require((occurrences, obligations) == (4992, 992), "certificate support counts differ")
    # A standalone new-auxiliary unit is neither a parent nor any case-tail clause.
    require((28974,) not in case_tail((0, 0, 1), ANCHOR_WEIGHTS[0], variables),
            "false auxiliary unit unexpectedly allowed")
    require(rat_counts == {str(i): (3 if i == 20 else 0) for i in range(4, 24)},
            "unexpected RAT profile")
    return {
        "verified_indices": list(range(4, 24)),
        "open_indices": list(range(4)),
        "core_clause_occurrences": occurrences,
        "distinct_parent_obligations": obligations,
        "certificate_bytes": manifest["certificate_bytes"],
        "rat_counts": rat_counts,
        "pair_orbits": orbit_count,
        "common_tail_clauses": 298,
        "case_tail_clauses": 334,
        "fresh_parent": file_info(base),
        "drat_trim": file_info(drat_trim),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--base", required=True, type=Path)
    parser.add_argument("--drat-trim", required=True, type=Path)
    parser.add_argument("--work", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    work = args.work.resolve()
    require(not work.is_relative_to(source.parent), "review work must be outside Git")
    orbits = independent_phase_orbits()
    report = {
        "reviewed_artifact_ref": "bafkreihqofvnf5car4vmnaxdlix67tmzfgrbvtceadcejqpil7lrlbsc74",
        "reviewed_source_commit": "8fcff86287b7bd48d321b95ab62f6412f799ddf1",
        "verdict": "accepted_conditional_on_imported_internal_color_split",
        "phase_quotient": {
            "classes": orbits[:-1],
            "normalizer_maps_tested": orbits[-1]["normalizer_maps_tested"],
        },
        "forced_core": inspect_forced_core(source),
        "certificates": check_certificates(
            source, args.base.resolve(), args.drat_trim.resolve(), work, orbits
        ),
        "scope": {
            "ten_cycle_type_excluded": False,
            "target_graph_found": False,
            "open_full_extensions": 4,
        },
        "dependencies": {
            "minority_matching_review": "bafkreicgerqxysxxxhechqnteewe6jq5w3ftk65xdyc3yeyxuxq4larqu4",
            "unreviewed_internal_color_split": "bafkreic67hnft4wp63c7xz2qh3gkry46k7p2qwqxqy7giawdc36kg6fs44",
        },
    }
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
