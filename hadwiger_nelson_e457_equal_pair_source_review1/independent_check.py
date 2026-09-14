#!/usr/bin/env python3
"""Clean-room exact review of the E457 equal-terminal source.

No reviewed executable is imported. The audit reconstructs the complete
physical graph and canonical CNF, checks E477 provenance entrywise, and invokes
separately compiled clean-room DRUP and colouring decision implementations.
"""

import argparse
from collections import Counter, deque
from hashlib import sha256
from itertools import combinations
import json
import lzma
from pathlib import Path
import subprocess


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parent
TARGET = REPOSITORY / "hadwiger_nelson_e457_equal_pair_source"
PARENT = REPOSITORY / "hadwiger_nelson_overlapping_forcing_seed"
TARGET_COMMIT = "bdaed9e41ed6af88848f550173870117702dea07"
RECEIPT_COMMIT = "a0687ef4f86b86bd2e11815a6dbee9b5ccfe2311"
PARENT_COMMIT = "5b28dad38f14e0979a10feb436c95e453dbb34d5"

PINNED = {
    "hadwiger_nelson_e457_equal_pair_source/.gitignore":
        "af2a1dae44070b3efb3e66795b3aacee299d7804f9d89c5f6f728f1bac4c1685",
    "hadwiger_nelson_e457_equal_pair_source/DISCOVERY_RECEIPT.json":
        "1222320aa5093f2b3ae9102695a8001c0cbee51db7b498e368109be0231a160e",
    "hadwiger_nelson_e457_equal_pair_source/README.md":
        "0a0e5cdbdc73aae501ad85811a3e9d8b99e4a44ea00aacb5b1ccb69c30b30d7a",
    "hadwiger_nelson_e457_equal_pair_source/SHA256SUMS":
        "ffa365df0afd49f9ff7172911f9e7f5fb5bd43139642fb5f347bd1a8257b40f3",
    "hadwiger_nelson_e457_equal_pair_source/build.py":
        "c5eedc20a0c1436ee86a3a8bdeee8243bd8a700ae7abb3ace68bfc579ba20fb3",
    "hadwiger_nelson_e457_equal_pair_source/colour_check.cpp":
        "f526fed1c5aff8f2a1a17446327f411320b0f5816af05045475c0dd912c5442e",
    "hadwiger_nelson_e457_equal_pair_source/controls.py":
        "a577a3421ff85f94ba27fec9fbf347c415bb7b2ffa62062d8283da67733bddb5",
    "hadwiger_nelson_e457_equal_pair_source/core.json":
        "d377e9526d13cc76aba6762ecd6a79bd04fe12d61e03a0b585a5ea38820d833b",
    "hadwiger_nelson_e457_equal_pair_source/expected.json":
        "e8403170aaaa374aec7b948693ce8f3b82e366612e583f926336ac0fdc415bc7",
    "hadwiger_nelson_e457_equal_pair_source/state.cnf":
        "06a2ffe15011660eac5f88007afdaefb87a696c954d324141e8f8b6293f1ada6",
    "hadwiger_nelson_e457_equal_pair_source/state.drat.xz":
        "e47f0e407e85b1eed0cd3253c6918b28eb8038b7c65d0242a1ea82f978005512",
    "hadwiger_nelson_e457_equal_pair_source/validation.json":
        "c77994c055d8a3f7a81d37ebff1133404c0028e4c1eccf99822973855d080f10",
    "hadwiger_nelson_e457_equal_pair_source/verify.py":
        "f4817f71882d541bfeabd504b2dbe6d26c07329b69ce73893b26aa042194cf29",
    "hadwiger_nelson_overlapping_forcing_seed/certificate.json":
        "3a487318d1d417e812791a1fd66d679151a7816fcf325a5bfd6a0351a0663237",
}


def require(condition, detail):
    if not condition:
        raise RuntimeError(detail)


def file_digest(path):
    answer = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            answer.update(block)
    return answer.hexdigest()


def json_digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return sha256(raw).hexdigest()


def exact_edges(rows):
    answer = []
    for first, second in combinations(range(len(rows)), 2):
        a, b, c, d = (rows[first][q] - rows[second][q] for q in range(4))
        rational = 3*a*a + 11*b*b + c*c + 33*d*d
        radical = a*b + c*d
        if rational == 1296 and radical == 0:
            answer.append((first, second))
    return tuple(answer)


def graph_statistics(vertex_count, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    seen = {0}
    queue = deque([0])
    while queue:
        vertex = queue.popleft()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(neighbour)
    require(len(seen) == vertex_count, ("disconnected graph", len(seen)))
    degrees = tuple(len(row) for row in adjacency)
    triangles_times_three = sum(len(adjacency[a] & adjacency[b]) for a, b in edges)
    require(triangles_times_three % 3 == 0, "triangle divisibility")
    return adjacency, degrees, triangles_times_three // 3


def canonical_formula(vertex_count, edges):
    def variable(vertex, colour):
        return 4*vertex + colour + 1

    clauses = []
    for vertex in range(vertex_count):
        clauses.append(tuple(variable(vertex, colour) for colour in range(4)))
        for first, second in combinations(range(4), 2):
            clauses.append((-variable(vertex, first), -variable(vertex, second)))
    for first, second in edges:
        for colour in range(4):
            clauses.append((-variable(first, colour), -variable(second, colour)))
    clauses.extend(((variable(0, 0),), (variable(1, 1),)))
    lines = [f"p cnf {4*vertex_count} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return tuple(clauses), ("\n".join(lines) + "\n").encode("ascii")


def parse_dimacs(raw):
    variables = declared_clauses = None
    clauses = []
    for line_number, raw_line in enumerate(raw.decode("ascii").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        tokens = line.split()
        if tokens[0] == "p":
            require(variables is None and tokens[:2] == ["p", "cnf"] and len(tokens) == 4,
                    ("DIMACS header", line_number))
            variables, declared_clauses = map(int, tokens[2:])
            continue
        require(variables is not None, ("clause before header", line_number))
        values = tuple(map(int, tokens))
        require(values and values[-1] == 0 and 0 not in values[:-1],
                ("DIMACS terminator", line_number))
        clause = values[:-1]
        require(all(0 < abs(literal) <= variables for literal in clause),
                ("DIMACS literal range", line_number))
        require(len(clause) == len(set(clause)) and all(-literal not in clause for literal in clause),
                ("DIMACS repeated or tautological literal", line_number))
        clauses.append(clause)
    require(variables is not None and len(clauses) == declared_clauses,
            ("DIMACS clause count", len(clauses), declared_clauses))
    return variables, tuple(clauses)


def solver_input(vertex_count, edges, pins):
    lines = [f"{vertex_count} {len(edges)}"]
    lines.extend(f"{first} {second}" for first, second in edges)
    lines.append(str(len(pins)))
    lines.extend(f"{vertex} {colour}" for vertex, colour in pins)
    return "\n".join(lines) + "\n"


def run_solver(executable, vertex_count, edges, pins):
    process = subprocess.run(
        [str(executable)], input=solver_input(vertex_count, edges, pins), text=True,
        capture_output=True, check=True, timeout=180)
    result = json.loads(process.stdout)
    require(set(result) == {"satisfiable", "nodes", "conflicts", "maximum_depth", "colouring"},
            "independent solver output schema")
    if result["satisfiable"]:
        colouring = result["colouring"]
        require(len(colouring) == vertex_count and all(type(c) is int and 0 <= c < 4
                                                       for c in colouring),
                "independent solver colouring format")
        require(all(colouring[a] != colouring[b] for a, b in edges),
                "independent solver monochromatic edge")
        require(all(colouring[v] == c for v, c in pins),
                "independent solver pin failure")
    else:
        require(result["colouring"] == [], "UNSAT solver returned colouring")
    return result


def solver_controls(executable):
    positive = run_solver(executable, 4, tuple(combinations(range(4), 2)), ())
    negative = run_solver(executable, 5, tuple(combinations(range(5), 2)), ())
    require(positive["satisfiable"] and not negative["satisfiable"],
            "independent solver controls")
    return {"k4_satisfiable": True, "k5_four_colourable": False}


def compact_decision(result):
    answer = {key: result[key] for key in
              ("satisfiable", "nodes", "conflicts", "maximum_depth")}
    if result["satisfiable"]:
        answer["colouring_json_sha256"] = json_digest(result["colouring"])
    return answer


def run_drup_checker(executable, cnf_path, proof_raw):
    self_test = subprocess.run([str(executable), "--self-test"], capture_output=True,
                               text=True, check=True, timeout=10)
    controls = json.loads(self_test.stdout)
    require(controls == {
        "unit_conflict_empty_clause_rup": True,
        "unsupported_unit_rejected": True,
        "four_clause_derived_unit_rup": True,
    }, "DRUP checker self-test")
    process = subprocess.run([str(executable), str(cnf_path)], input=proof_raw,
                             capture_output=True, check=True, timeout=180)
    result = json.loads(process.stdout)
    expected_keys = {
        "drup_lines", "drup_additions_verified_by_watched_rup",
        "drup_deletion_lines_live", "drup_final_empty_clause_line",
        "drup_maximum_clause_length", "drup_propagated_assignments",
        "drup_watched_clause_inspections", "drup_replacement_literal_inspections",
        "drup_deletions_applied_after_liveness_check",
    }
    require(set(result) == expected_keys, "DRUP checker output schema")
    require(result["drup_lines"] == result["drup_final_empty_clause_line"] == 272901 and
            result["drup_additions_verified_by_watched_rup"] == 131322 and
            result["drup_deletion_lines_live"] == 141579 and
            result["drup_maximum_clause_length"] == 221 and
            result["drup_deletions_applied_after_liveness_check"],
            "DRUP checker principal counts")
    return controls, result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--colour-checker", type=Path, required=True)
    parser.add_argument("--drup-checker", type=Path, required=True)
    arguments = parser.parse_args()
    require(arguments.colour_checker.is_file(), "missing independent colouring checker")
    require(arguments.drup_checker.is_file(), "missing independent DRUP checker")

    for name, expected in PINNED.items():
        require(file_digest(REPOSITORY / name) == expected, ("pinned source hash", name))

    core = json.loads((TARGET / "core.json").read_text())
    require(set(core) == {"deleted_source_indices", "denominator", "equal_four_colouring",
                          "points", "schema", "source_indices", "source_parent"},
            "core schema keys")
    require(core["schema"] == "hn-e457-equal-pair-v1" and core["source_parent"] == "E477"
            and core["denominator"] == 1, "core metadata")
    rows = core["points"]
    require(len(rows) == 457 and len({tuple(row) for row in rows}) == 457,
            "point count or collision")
    require(all(len(row) == 4 and all(type(value) is int for value in row) for row in rows),
            "coordinate format")

    parent = json.loads((PARENT / "certificate.json").read_text())["equal"]
    source_indices = core["source_indices"]
    deleted = core["deleted_source_indices"]
    require(len(source_indices) == len(set(source_indices)) == 457 and
            source_indices == sorted(source_indices), "source index census")
    require(len(deleted) == len(set(deleted)) == 20 and
            set(source_indices).isdisjoint(deleted) and
            set(source_indices) | set(deleted) == set(range(477)),
            "source index partition")
    require(rows == [parent["points"][index] for index in source_indices],
            "E477 coordinate restriction")
    word = core["equal_four_colouring"]
    require(word == [parent["colouring"][index] for index in source_indices],
            "E477 colour-word restriction")

    edges = exact_edges(rows)
    require(len(edges) == 2329, ("complete unit edge count", len(edges)))
    adjacency, degrees, triangles = graph_statistics(len(rows), edges)
    require((min(degrees), max(degrees), triangles) == (4, 25, 847),
            "graph statistics")
    require((len(adjacency[0]), len(adjacency[1]), len(adjacency[0] & adjacency[1])) ==
            (17, 7, 0), "terminal graph statistics")

    require(rows[0] == [0, 0, 0, 0] and rows[1] == [0, 0, 96, 0],
            "terminal coordinates")
    require(len(word) == 457 and all(type(colour) is int and 0 <= colour < 4
                                     for colour in word), "colour word format")
    require(word[0] == word[1] and all(word[a] != word[b] for a, b in edges),
            "published equal-terminal colouring")

    clauses, cnf_raw = canonical_formula(len(rows), edges)
    published_cnf = (TARGET / "state.cnf").read_bytes()
    require(cnf_raw == published_cnf, "canonical CNF byte mismatch")
    variables, parsed_clauses = parse_dimacs(published_cnf)
    require(variables == 1828 and parsed_clauses == clauses and len(clauses) == 12517,
            "parsed CNF mismatch")
    clause_histogram = Counter(map(len, clauses))
    require(clause_histogram == {1: 2, 2: 12058, 4: 457}, "CNF clause histogram")

    proof_raw = lzma.open(TARGET / "state.drat.xz", "rb").read()
    require(sha256(proof_raw).hexdigest() ==
            "0987af3f985e83fb71377bf1c91c45c1edc449a443affe534dfbdd6c2144a1e8",
            "uncompressed DRAT hash")
    drup_controls, drup = run_drup_checker(arguments.drup_checker,
                                           TARGET / "state.cnf", proof_raw)
    colour_controls = solver_controls(arguments.colour_checker)
    equal_decision = run_solver(arguments.colour_checker, len(rows), edges,
                                ((0, 0), (1, 0)))
    unequal_decision = run_solver(arguments.colour_checker, len(rows), edges,
                                  ((0, 0), (1, 1)))
    require(equal_decision["satisfiable"] and not unequal_decision["satisfiable"],
            "independent terminal decisions")

    edge_stream = "".join(f"{first},{second}\n" for first, second in edges).encode()
    result = {
        "status": "EXACT PHYSICAL FORCING SOURCE INDEPENDENTLY REPRODUCED",
        "verdict": "ACCEPT_HIGH_CONFIDENCE_SCOPED",
        "reviewed_source_commit": TARGET_COMMIT,
        "reviewed_receipt_commit": RECEIPT_COMMIT,
        "parent_source_commit": PARENT_COMMIT,
        "imports_reviewed_code": False,
        "coordinate_field": "Q(sqrt(3),sqrt(11)) with fixed scale 1/36",
        "vertices": len(rows),
        "all_unordered_physical_pairs_checked": len(rows)*(len(rows)-1)//2,
        "distinct_physical_points": len(set(map(tuple, rows))),
        "complete_unit_edges": len(edges),
        "edge_stream_sha256": sha256(edge_stream).hexdigest(),
        "source_point_json_sha256": json_digest(rows),
        "source_edge_json_sha256": json_digest(edges),
        "connected": True,
        "degree_histogram": {str(degree): count for degree, count in
                             sorted(Counter(degrees).items())},
        "minimum_degree": min(degrees),
        "maximum_degree": max(degrees),
        "triangles": triangles,
        "terminal_squared_distance": "64/9",
        "terminal_degrees": [len(adjacency[0]), len(adjacency[1])],
        "terminal_common_neighbours": len(adjacency[0] & adjacency[1]),
        "published_equal_four_colouring_valid": True,
        "e477_source_indices": len(source_indices),
        "e477_deleted_indices": len(deleted),
        "e477_coordinates_restricted_entrywise": True,
        "e477_colour_word_restricted_entrywise": True,
        "cnf_variables": variables,
        "cnf_clauses": len(clauses),
        "cnf_clause_length_histogram": {str(size): count for size, count in
                                        sorted(clause_histogram.items())},
        "cnf_byte_reconstructed": True,
        "cnf_sha256": sha256(cnf_raw).hexdigest(),
        "compressed_drat_sha256": file_digest(TARGET / "state.drat.xz"),
        "uncompressed_drat_sha256": sha256(proof_raw).hexdigest(),
        **drup,
        "drup_checker_controls": drup_controls,
        "independent_search_method":
            "in-place maximum-saturation colouring with forced-domain propagation",
        "independent_equal_pin_search": compact_decision(equal_decision),
        "independent_unequal_pin_search": compact_decision(unequal_decision),
        "colour_checker_controls": colour_controls,
        "equal_in_every_proper_four_colouring": True,
        "physical_equal_pair_source": True,
        "connector_allowance_including_both_terminals": 53,
        "conditional_union_order": 508,
        "five_chromatic_graph_constructed": False,
        "global_hadwiger_nelson_progress": False,
        "record_candidate": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
