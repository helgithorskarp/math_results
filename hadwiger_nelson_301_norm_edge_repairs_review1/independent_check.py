#!/usr/bin/env python3
"""Independent exact checker for Discovery Net contribution h4007.

The checker deliberately does not import the producer's verifier.  It checks
the finite-family split, the six colouring witnesses, the twelve geometric
certificates, the combined selector CNF, and (when supplied) the omitted raw
LRAT proof using a separate Python RUP replay.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from collections import Counter
from fractions import Fraction
from math import isqrt
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SOURCE = ROOT / "hadwiger_nelson_h516_k23free_edge_repair"
INTERFACE = ROOT / "hadwiger_nelson_301_forbidden_subgraph_interface"
TARGET = ROOT / "hadwiger_nelson_301_norm_edge_repairs"

GRAPH_SHA256 = "7be0344d1811866429181436b2f85653fc801272a7a3efddad6125539e50cbbb"
FIVE_SHA256 = "720466c1b6403de7d8247a33bb2844fccca306dfa21cc339b763968e6b2aea1d"
INTERFACE_SHA256 = "7119f912d305b5ae20439bd1a138d161277cd7fc95a82a09b23feec775f3de5c"
REPAIR_SHA256 = "2e525fb48c247195fb20e6f4c323da5e0b87611c9f0ea25974485e94dbd3dfe3"
CLASSIFICATION_SHA256 = "ac2699cfc073b858cdfdb0004033af20b26d9a9fb8d39cd43e6ae0fd4e57ad3b"
CNF_SHA256 = "60055ca362217f4c8f5121a7d245de67c146c1283dc0adf04457224e7db6ad86"
LRAT_SHA256 = "1d8bb23ff2caca290b6f3f77637c134c36ce9efb8d10961e768dffaac954413b"
LRAT_SIZE = 28_590_220
FRESH_RANK_PRIME = 998_244_353
ANCHOR = (1, 189, 192)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text())


def prime(n: int) -> bool:
    return n >= 2 and all(n % d for d in range(2, isqrt(n) + 1))


def rank_mod_reverse(rows: list[dict[int, int]], modulus: int) -> int:
    """Sparse elimination with the largest column as pivot.

    This uses a different prime and pivot direction from the target checker.
    A rank-r result modulo a prime proves an integer r-minor is nonzero.
    """
    basis: dict[int, dict[int, int]] = {}
    for input_row in rows:
        row = {c: a % modulus for c, a in input_row.items() if a % modulus}
        while row:
            pivot = max(row)
            coefficient = row[pivot]
            if pivot not in basis:
                inverse = pow(coefficient, -1, modulus)
                basis[pivot] = {c: a * inverse % modulus for c, a in row.items()}
                break
            pivot_row = basis[pivot]
            for c, a in pivot_row.items():
                value = (row.get(c, 0) - coefficient * a) % modulus
                if value:
                    row[c] = value
                else:
                    row.pop(c, None)
    return len(basis)


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = None
    declared = None
    clauses: list[tuple[int, ...]] = []
    current: list[int] = []
    for raw in path.read_text().splitlines():
        fields = raw.split()
        if not fields or fields[0] == "c":
            continue
        if fields[0] == "p":
            require(variables is None and fields[:2] == ["p", "cnf"] and len(fields) == 4,
                    "bad DIMACS header")
            variables, declared = map(int, fields[2:])
            require(variables > 0 and declared >= 0, "bad DIMACS dimensions")
            continue
        require(variables is not None, "DIMACS data before header")
        for field in fields:
            literal = int(field)
            if literal:
                require(abs(literal) <= variables, "DIMACS literal out of range")
                current.append(literal)
            else:
                clauses.append(tuple(current))
                current.clear()
    require(variables is not None and not current and len(clauses) == declared,
            "DIMACS clause count")
    return variables, clauses


def source_and_family():
    require(digest(SOURCE / "graph.json") == GRAPH_SHA256, "source graph hash")
    require(digest(SOURCE / "five_colouring.json") == FIVE_SHA256, "source five-colouring hash")
    require(digest(INTERFACE / "certificate.json") == INTERFACE_SHA256, "interface hash")
    require(digest(INTERFACE / "repair_clause.cnf") == REPAIR_SHA256, "repair clause hash")
    require(digest(TARGET / "classification.json") == CLASSIFICATION_SHA256, "classification hash")

    graph = load_json(SOURCE / "graph.json")
    labels = graph["labels"]
    edges = [tuple(edge) for edge in graph["edges"]]
    require(labels == sorted(set(labels)) and len(labels) == 301, "source labels")
    require(edges == sorted(set(edges)) and len(edges) == 1452, "source edges")
    require(all(u < v and u in set(labels) and v in set(labels) for u, v in edges),
            "source edge convention")
    edge_set = set(edges)

    interface = load_json(INTERFACE / "certificate.json")
    support = {tuple(row[:2]) for row in interface["norm_weights"] if row[2] != 0}
    require(len(support) == 18 and support <= edge_set, "18-edge norm support")

    repair_variables, repair_clauses = parse_dimacs(INTERFACE / "repair_clause.cnf")
    require(repair_variables == len(edges) and len(repair_clauses) == 1,
            "repair clause dimensions")
    repair_clause = repair_clauses[0]
    require(len(repair_clause) == 690 and len(set(repair_clause)) == 690 and
            all(literal < 0 for literal in repair_clause), "repair clause literals")
    repair_edges = {edges[-literal - 1] for literal in repair_clause}
    require(support <= repair_edges, "norm support outside necessary repair clause")

    classification = load_json(TARGET / "classification.json")
    cases = classification["cases"]
    require(len(cases) == 18 and {tuple(row["edge"]) for row in cases} == support,
            "classification does not cover support exactly")
    require(len({row["source_edge_index_one_based"] for row in cases}) == 18,
            "duplicate source indices")
    for row in cases:
        edge = tuple(row["edge"])
        require(edges[row["source_edge_index_one_based"] - 1] == edge,
                "wrong source edge index")

    four = [row for row in cases if row["classification"] == "FOUR_COLOURABLE"]
    geometric = [row for row in cases
                 if row["classification"] == "EXACTLY_FIVE_CHROMATIC_AND_NO_PLANE_UNIT_EDGE_MAP"]
    require(len(four) == classification["four_colourable_cases"] == 6,
            "four-colourable count")
    require(len(geometric) == classification["exactly_five_nonrealizable_cases"] == 12,
            "geometric case count")
    require(len(four) + len(geometric) == len(cases), "unknown classification tag")

    position = {label: index for index, label in enumerate(labels)}
    for row in four:
        deleted = tuple(row["edge"])
        word = row["four_colouring_word"]
        require(len(word) == len(labels) and set(word) <= set("0123"),
                "malformed four-colouring")
        colours = {label: int(word[position[label]]) for label in labels}
        require(all(edge == deleted or colours[edge[0]] != colours[edge[1]] for edge in edges),
                "improper four-colouring")

    five = load_json(SOURCE / "five_colouring.json")["colours"]
    require(set(five) == {str(label) for label in labels}, "five-colouring labels")
    require(set(five.values()) == set(range(5)), "five-colouring palette")
    require(all(five[str(u)] != five[str(v)] for u, v in edges), "improper five-colouring")

    require(all(tuple(sorted(pair)) in edge_set for pair in
                ((ANCHOR[0], ANCHOR[1]), (ANCHOR[0], ANCHOR[2]), (ANCHOR[1], ANCHOR[2]))),
            "anchor is not a triangle")
    require(not support.intersection({tuple(sorted(pair)) for pair in
                                      ((ANCHOR[0], ANCHOR[1]), (ANCHOR[0], ANCHOR[2]),
                                       (ANCHOR[1], ANCHOR[2]))}),
            "anchor edge is deletable")
    return graph, edges, classification, four, geometric


def quotient_has_edge(edges: set[tuple[int, int]], identified: tuple[int, int],
                      first: int, second: int) -> bool:
    left, right = identified
    require(first != right and second != right, "noncanonical quotient label")
    first_preimages = (left, right) if first == left else (first,)
    second_preimages = (left, right) if second == left else (second,)
    return first != second and any(tuple(sorted((u, v))) in edges
                                   for u in first_preimages for v in second_preimages)


def check_geometry(graph, row) -> dict[str, int]:
    deleted = tuple(row["edge"])
    edges = set(map(tuple, graph["edges"])) - {deleted}
    labels = graph["labels"]
    label_set = set(labels)
    position = {label: i for i, label in enumerate(labels)}
    cert_path = TARGET / row["geometric_certificate"]
    require(digest(cert_path) == row["geometric_certificate_sha256"],
            "geometric certificate hash")
    cert = load_json(cert_path)
    require(cert["receipt"] == row["geometric_receipt"], "geometric receipt link")

    equations: list[dict[int, int]] = []
    used_diagonals: set[str] = set()
    edge_witnesses = 0
    wheel_witnesses = 0
    for cycle in cert["cycles"]:
        require(len(cycle) == 4 and len(set(cycle)) == 4 and set(cycle) <= label_set,
                "bad four-cycle")
        require(all(tuple(sorted(pair)) in edges for pair in
                    zip(cycle, cycle[1:] + cycle[:1])), "missing four-cycle edge")
        for offset in (0, 1):
            identified = tuple(sorted((cycle[offset], cycle[offset + 2])))
            key = f"{identified[0]},{identified[1]}"
            require(key in cert["diagonal_obstructions"], "unproved distinct diagonal")
            if key in used_diagonals:
                continue
            used_diagonals.add(key)
            witness = cert["diagonal_obstructions"][key]
            if witness["type"] == "edge":
                require(identified in edges, "invalid direct diagonal witness")
                edge_witnesses += 1
            elif witness["type"] == "odd_wheel":
                left, right = identified
                hub = witness["hub"]
                rim = witness["rim"]
                require(len(rim) >= 3 and len(rim) % 2 == 1 and len(set(rim)) == len(rim),
                        "rim is not a simple odd cycle")
                require(hub in label_set and set(rim) <= label_set and hub not in rim and
                        right not in rim and hub != right, "invalid quotient wheel labels")
                require(all(quotient_has_edge(edges, identified, hub, vertex) for vertex in rim),
                        "missing quotient wheel spoke")
                require(all(quotient_has_edge(edges, identified, u, v) for u, v in
                            zip(rim, rim[1:] + rim[:1])), "missing quotient wheel rim edge")
                wheel_witnesses += 1
            else:
                raise ValueError("unknown diagonal witness")
        equations.append({position[cycle[i]]: 1 if i % 2 == 0 else -1 for i in range(4)})
    require(used_diagonals == set(cert["diagonal_obstructions"]),
            "unused diagonal witness")

    anchor = cert["translation_anchor"]
    require(anchor in label_set, "bad translation anchor")
    equations.append({position[anchor]: 1})

    free_labels = cert["free_labels"]
    require(len(free_labels) == len(set(free_labels)) and set(free_labels) <= label_set,
            "bad free labels")
    raw_parameter_rows = cert["parametrization"]
    require(len(raw_parameter_rows) == len(labels), "wrong parametrization height")
    parameter_rows: list[dict[int, Fraction]] = []
    for raw_entries in raw_parameter_rows:
        parsed: dict[int, Fraction] = {}
        for column, numerator, denominator in raw_entries:
            require(isinstance(column, int) and 0 <= column < len(free_labels) and
                    column not in parsed, "bad parameter column")
            require(isinstance(numerator, int) and isinstance(denominator, int) and
                    numerator != 0 and denominator > 0, "bad rational entry")
            parsed[column] = Fraction(numerator, denominator)
        parameter_rows.append(parsed)
    for column, label in enumerate(free_labels):
        require(parameter_rows[position[label]] == {column: Fraction(1)},
                "free rows do not contain an identity matrix")

    for equation in equations:
        image: dict[int, Fraction] = {}
        for source_row, coefficient in equation.items():
            for column, value in parameter_rows[source_row].items():
                image[column] = image.get(column, Fraction(0)) + coefficient * value
        require(not any(image.values()), "parametrization violates a linear equation")

    fresh_rank = rank_mod_reverse(equations, FRESH_RANK_PRIME)
    expected_rank = len(labels) - len(free_labels)
    require(fresh_rank == expected_rank, "fresh-prime rank/nullity failure")

    gram: dict[tuple[int, int], Fraction] = {}
    norm_edge_set: set[tuple[int, int]] = set()
    weight_sum = 0
    for left, right, weight in cert["norm_weights"]:
        edge = (left, right)
        require(edge in edges and edge not in norm_edge_set and isinstance(weight, int) and weight,
                "bad norm-identity edge")
        norm_edge_set.add(edge)
        weight_sum += weight
        difference = parameter_rows[position[left]].copy()
        for column, value in parameter_rows[position[right]].items():
            difference[column] = difference.get(column, Fraction(0)) - value
        difference = {column: value for column, value in difference.items() if value}
        terms = sorted(difference.items())
        for i, (first_column, first_value) in enumerate(terms):
            for second_column, second_value in terms[i:]:
                key = (first_column, second_column)
                gram[key] = gram.get(key, Fraction(0)) + weight * first_value * second_value
    require(weight_sum == cert["weight_sum"] and weight_sum != 0,
            "norm coefficient sum")
    require(not any(gram.values()), "weighted Gram identity is nonzero")

    return {
        "cycles": len(cert["cycles"]),
        "diagonals": len(used_diagonals),
        "edge_witnesses": edge_witnesses,
        "wheel_witnesses": wheel_witnesses,
        "rank": fresh_rank,
        "parameters": len(free_labels),
        "norm_edges": len(norm_edge_set),
        "norm_sum": weight_sum,
    }


def expected_cnf(labels: list[int], edges: list[tuple[int, int]],
                 geometric_rows) -> tuple[int, list[tuple[int, ...]]]:
    position = {label: i for i, label in enumerate(labels)}
    cases = [tuple(row["edge"]) for row in geometric_rows]
    gates = [4 * len(labels) + i + 1 for i in range(len(cases))]
    gate_for = dict(zip(cases, gates))
    auxiliaries = [4 * len(labels) + len(cases) + i + 1 for i in range(len(cases) - 1)]
    clauses: list[tuple[int, ...]] = []
    for label in labels:
        clauses.append(tuple(4 * position[label] + colour + 1 for colour in range(4)))
    for left, right in edges:
        prefix = (gate_for[(left, right)],) if (left, right) in gate_for else ()
        for colour in range(4):
            clauses.append(prefix + (-4 * position[left] - colour - 1,
                                     -4 * position[right] - colour - 1))
    for colour, label in enumerate(ANCHOR):
        clauses.append((4 * position[label] + colour + 1,))
    clauses.append(tuple(gates))
    clauses.append((-gates[0], auxiliaries[0]))
    for i in range(1, len(gates) - 1):
        clauses.extend(((-gates[i], auxiliaries[i]),
                        (-auxiliaries[i - 1], auxiliaries[i]),
                        (-gates[i], -auxiliaries[i - 1])))
    clauses.append((-gates[-1], -auxiliaries[-1]))
    return 4 * len(labels) + len(gates) + len(auxiliaries), clauses


def check_cnf(graph, edges, geometric_rows) -> tuple[int, int]:
    cnf_path = TARGET / "five_chromatic_repairs.cnf"
    require(digest(cnf_path) == CNF_SHA256, "combined CNF hash")
    variables, clauses = parse_dimacs(cnf_path)
    expected_variables, expected_clauses = expected_cnf(graph["labels"], edges, geometric_rows)
    require(variables == expected_variables and Counter(clauses) == Counter(expected_clauses),
            "combined CNF semantic reconstruction")
    return variables, len(clauses)


def replay_lrat(cnf_path: Path, proof_path: Path) -> dict[str, int | str | bool]:
    require(proof_path.is_file() and proof_path.stat().st_size == LRAT_SIZE,
            "raw LRAT size")
    require(digest(proof_path) == LRAT_SHA256, "raw LRAT hash")
    variables, original = parse_dimacs(cnf_path)
    database: dict[int, tuple[int, ...]] = {
        index: clause for index, clause in enumerate(original, 1)
    }
    last_id = len(original)
    additions = deletions = hints_used = proof_lines = 0
    empty_checked = False

    with proof_path.open() as stream:
        for raw in stream:
            proof_lines += 1
            tokens = raw.split()
            if not tokens or tokens[0] == "c":
                continue
            require(len(tokens) >= 3, "short LRAT line")
            step = int(tokens[0])
            if tokens[1] == "d":
                deleted_ids = list(map(int, tokens[2:]))
                require(deleted_ids and deleted_ids[-1] == 0 and
                        all(identifier > 0 for identifier in deleted_ids[:-1]),
                        "bad LRAT deletion line")
                for identifier in deleted_ids[:-1]:
                    require(identifier in database, "deletion of absent LRAT clause")
                    del database[identifier]
                    deletions += 1
                continue

            require(step > last_id, "LRAT addition IDs are not increasing")
            last_id = step
            integers = list(map(int, tokens[1:]))
            require(integers.count(0) == 2 and integers[-1] == 0,
                    "LRAT addition delimiters")
            split = integers.index(0)
            clause = tuple(integers[:split])
            hints = integers[split + 1:-1]
            require(all(0 < hint for hint in hints), "non-RUP LRAT hint")
            require(all(abs(literal) <= variables for literal in clause),
                    "LRAT literal out of range")

            assignment: dict[int, bool] = {}
            conflict = False
            for literal in clause:
                variable = abs(literal)
                forced_value = literal < 0
                if variable in assignment and assignment[variable] != forced_value:
                    conflict = True
                assignment[variable] = forced_value

            for hint in hints:
                require(hint in database, "LRAT hint names absent clause")
                if conflict:
                    continue
                hints_used += 1
                satisfied = False
                unassigned: set[int] = set()
                for literal in database[hint]:
                    variable = abs(literal)
                    if variable in assignment:
                        if assignment[variable] == (literal > 0):
                            satisfied = True
                            break
                    else:
                        unassigned.add(literal)
                if satisfied:
                    continue
                require(len(unassigned) <= 1, "LRAT hint is neither unit nor conflicting")
                if not unassigned:
                    conflict = True
                else:
                    literal = next(iter(unassigned))
                    assignment[abs(literal)] = literal > 0
            require(conflict, "LRAT hint chain does not reach conflict")
            database[step] = clause
            additions += 1
            if not clause:
                empty_checked = True

    require(empty_checked, "no checked empty clause")
    require((additions, deletions, hints_used, proof_lines) ==
            (66_120, 72_205, 4_202_594, 98_052), "LRAT receipt mismatch")
    return {
        "checked": True,
        "sha256": LRAT_SHA256,
        "size_bytes": LRAT_SIZE,
        "additions": additions,
        "deletions": deletions,
        "hints_used": hints_used,
        "proof_lines": proof_lines,
    }


def controls(graph, classification, geometric_rows) -> list[str]:
    rejected: list[str] = []

    altered = copy.deepcopy(classification)
    altered["cases"].pop()
    try:
        support = {tuple(row[:2]) for row in load_json(INTERFACE / "certificate.json")["norm_weights"]
                   if row[2]}
        require({tuple(row["edge"]) for row in altered["cases"]} == support,
                "coverage mutation")
    except ValueError:
        rejected.append("missing_family_case")
    else:
        raise ValueError("coverage mutation accepted")

    certificate = load_json(TARGET / geometric_rows[0]["geometric_certificate"])
    certificate["norm_weights"][0][2] += 1
    certificate["weight_sum"] += 1
    try:
        position = {label: i for i, label in enumerate(graph["labels"])}
        parameter_rows = []
        for entries in certificate["parametrization"]:
            parameter_rows.append({c: Fraction(n, d) for c, n, d in entries})
        gram = {}
        for left, right, weight in certificate["norm_weights"]:
            difference = parameter_rows[position[left]].copy()
            for column, value in parameter_rows[position[right]].items():
                difference[column] = difference.get(column, Fraction(0)) - value
            terms = sorted((column, value) for column, value in difference.items() if value)
            for i, (a, x) in enumerate(terms):
                for b, y in terms[i:]:
                    gram[a, b] = gram.get((a, b), Fraction(0)) + weight * x * y
        require(not any(gram.values()), "norm mutation")
    except ValueError:
        rejected.append("changed_norm_identity")
    else:
        raise ValueError("norm mutation accepted")
    return rejected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lrat", type=Path, help="byte-identical raw omitted LRAT archive")
    parser.add_argument("--controls", action="store_true")
    args = parser.parse_args()

    require(prime(FRESH_RANK_PRIME), "fresh rank modulus is not prime")
    graph, edges, classification, four_rows, geometric_rows = source_and_family()
    geometry = [check_geometry(graph, row) for row in geometric_rows]
    variables, clauses = check_cnf(graph, edges, geometric_rows)
    receipt = {
        "status": "INDEPENDENT_H4007_ACCEPT",
        "source_vertices": len(graph["labels"]),
        "source_edges": len(edges),
        "repair_clause_edges": 690,
        "norm_support_cases": len(classification["cases"]),
        "four_colourable_cases": len(four_rows),
        "five_chromatic_nonrealizable_cases": len(geometric_rows),
        "geometry": {
            "certificates": len(geometry),
            "cycles": sum(row["cycles"] for row in geometry),
            "diagonal_witnesses": sum(row["diagonals"] for row in geometry),
            "edge_witnesses": sum(row["edge_witnesses"] for row in geometry),
            "odd_wheel_witnesses": sum(row["wheel_witnesses"] for row in geometry),
            "rank_range": [min(row["rank"] for row in geometry),
                           max(row["rank"] for row in geometry)],
            "fresh_rank_prime": FRESH_RANK_PRIME,
            "norm_edge_count_set": sorted({row["norm_edges"] for row in geometry}),
            "norm_sum_set": sorted({row["norm_sum"] for row in geometry}),
        },
        "cnf": {"variables": variables, "clauses": clauses, "sha256": CNF_SHA256},
        "lrat": {"checked": False, "required_for_exact_chromatic_subclaim": True},
        "family_closure_does_not_require_lrat": True,
    }
    if args.lrat:
        receipt["lrat"] = replay_lrat(TARGET / "five_chromatic_repairs.cnf", args.lrat)
    if args.controls:
        receipt["rejected_controls"] = controls(graph, classification, geometric_rows)
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
