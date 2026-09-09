#!/usr/bin/env python3
"""Independent audit of the h4015 induced-P5 extension certificates.

No module from the reviewed package is imported.  This checker transcribes the
two published cores independently, builds each complete 18-vertex constraint
set from forbidden truth tables, and checks the text proofs using repeated
definition-level unit-propagation scans over bit-mask clauses.
"""

from __future__ import annotations

import argparse
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path


SOURCE_DIRECTORY = "ramsey_r55_one_sided_induced_path"
SOURCE_MANIFEST_SHA256 = (
    "f18a606f5f3bc0a90a1a3795bea30f48c38d079979fe99a5910ecc922fc9ab10"
)
INPUTS_SHA256 = (
    "961de1773450315d120f73a6cfbf8189b91d5c427ffa6496bb6d02a9ab3ab9bd"
)
EXPECTED_CASES = {
    "G1": {
        "order": 13,
        "variables": 75,
        "clauses": 57_596,
        "cnf_sha256":
            "f42c13a6b9505c7372c9bed3b99288c303ce7a83d3b173d28bdd9f544371997a",
        "proof_sha256":
            "16adf69c694fb10ffec56869b7e12ced6a3593283d87cce860f194c4223aad5a",
        "additions": 275,
        "deletions": 88,
    },
    "G2": {
        "order": 14,
        "variables": 62,
        "clauses": 34_197,
        "cnf_sha256":
            "306c0b69e9a6d33d84533802861ba4f685e39bb0dae373a8b6457d87aa38a650",
        "proof_sha256":
            "708a13a0487c23c04705ffdcb3514e1e8ef26bd63f9b02c377b46bf9284dfa0c",
        "additions": 77,
        "deletions": 24,
    },
}

# Appendix adjacency lists in Cameron--Goedgebeur--Huang--Shi,
# arXiv:2005.03441v1.  They are intentionally independent of INPUTS.json.
PUBLISHED_ADJACENCY = {
    "G1": (
        "0:1 2 10 12;1:0 8 10 12;2:0 9 10 12;3:4 5 11 12;"
        "4:3 6 11 12;5:3 7 11 12;6:4 7 11 12;7:5 6 11 12;"
        "8:1 9 10 12;9:2 8 10 12;10:0 1 2 8 9 11;"
        "11:3 4 5 6 7 10;12:0 1 2 3 4 5 6 7 8 9"
    ),
    "G2": (
        "0:1 2 12 13;1:0 3 12 13;2:0 4 12 13;3:1 4 12 13;"
        "4:2 3 12 13;5:6 7 9 11 12;6:5 8 10 11 13;"
        "7:5 8 9 11 13;8:6 7 10 11 12;9:5 7 10 12 13;"
        "10:6 8 9 12 13;11:5 6 7 8 12 13;"
        "12:0 1 2 3 4 5 8 9 10 11;13:0 1 2 3 4 6 7 9 10 11"
    ),
}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_source(source):
    manifest = source / "SHA256SUMS"
    need(file_sha256(manifest) == SOURCE_MANIFEST_SHA256,
         "source manifest identity")
    names = []
    for line in manifest.read_text().splitlines():
        digest, name = line.split("  ", 1)
        need(Path(name).name == name and name not in names, "manifest path")
        need(file_sha256(source / name) == digest, "source hash " + name)
        names.append(name)
    actual = {path.name for path in source.iterdir() if path.is_file()}
    need(len(names) == 17 and set(names) == actual - {"SHA256SUMS"},
         "source manifest file set")
    need(file_sha256(source / "INPUTS.json") == INPUTS_SHA256,
         "source input identity")
    return names


def parse_published(case):
    entries = PUBLISHED_ADJACENCY[case].split(";")
    rows = []
    for expected_vertex, entry in enumerate(entries):
        head, tail = entry.split(":", 1)
        need(int(head) == expected_vertex, "published vertex order")
        rows.append([int(value) for value in tail.split()])
    return rows


def validate_rows(rows):
    order = len(rows)
    need(all(len(row) == len(set(row)) for row in rows), "duplicate neighbor")
    for vertex, row in enumerate(rows):
        need(vertex not in row, "loop")
        need(all(0 <= other < order and vertex in rows[other] for other in row),
             "asymmetric or out-of-range adjacency")
    return [sum(1 << other for other in row) for row in rows]


def is_path_word(word, pairs):
    rows = [0] * 5
    for bit, (left, right) in enumerate(pairs):
        if word >> bit & 1:
            rows[left] |= 1 << right
            rows[right] |= 1 << left
    if sorted(row.bit_count() for row in rows) != [1, 1, 2, 2, 2]:
        return False
    reached = 1
    frontier = 1
    while frontier:
        neighbors = 0
        scan = frontier
        while scan:
            bit = scan & -scan
            scan ^= bit
            neighbors |= rows[bit.bit_length() - 1]
        frontier = neighbors & ~reached
        reached |= frontier
    return reached == 31


def contains_pattern(rows, size, accepted_words):
    for chosen in combinations(range(len(rows)), size):
        word = 0
        for bit, (left, right) in enumerate(combinations(chosen, 2)):
            if rows[left] >> right & 1:
                word |= 1 << bit
        if word in accepted_words:
            return True
    return False


def colorable(rows, colors, removed=None):
    order = len(rows)
    active = ((1 << order) - 1) ^ (0 if removed is None else 1 << removed)
    assigned = [-1] * order

    def search(uncolored):
        if not uncolored:
            return True
        best = None
        best_key = None
        scan = uncolored
        while scan:
            bit = scan & -scan
            scan ^= bit
            vertex = bit.bit_length() - 1
            neighbor_colors = {assigned[other]
                               for other in range(order)
                               if rows[vertex] >> other & 1 and assigned[other] >= 0}
            key = (len(neighbor_colors),
                   (rows[vertex] & uncolored).bit_count(), -vertex)
            if best_key is None or key > best_key:
                best, best_key = vertex, key
        forbidden = {assigned[other] for other in range(order)
                     if rows[best] >> other & 1 and assigned[other] >= 0}
        for color in range(colors):
            if color not in forbidden:
                assigned[best] = color
                if search(uncolored ^ (1 << best)):
                    return True
                assigned[best] = -1
        return False

    return search(active)


def audit_core(case, source_rows):
    published = parse_published(case)
    need(source_rows == published, "source core differs from paper appendix")
    rows = validate_rows(published)
    pairs5 = list(combinations(range(5), 2))
    paths = {word for word in range(1 << 10) if is_path_word(word, pairs5)}
    need(len(paths) == 60, "induced path truth-table size")
    need(not contains_pattern(rows, 4, {63}), "core K4")
    need(not contains_pattern(rows, 5, {0}), "core independent five-set")
    need(not contains_pattern(rows, 5, paths), "core induced P5")
    need(not colorable(rows, 4) and colorable(rows, 5), "core chromatic number")
    need(all(colorable(rows, 4, vertex) for vertex in range(len(rows))),
         "core vertex criticality")
    return rows, paths


def build_formula(core_rows, path_words):
    core_order = len(core_rows)
    all_pairs = list(combinations(range(18), 2))
    fixed = {edge: int(core_rows[edge[0]] >> edge[1] & 1)
             for edge in all_pairs if edge[1] < core_order}
    free = [edge for edge in all_pairs if edge not in fixed]
    variables = {edge: index + 1 for index, edge in enumerate(free)}
    clauses = set()

    def forbid(vertices, word):
        clause = []
        for bit, edge in enumerate(combinations(vertices, 2)):
            desired = word >> bit & 1
            if edge in fixed:
                if fixed[edge] != desired:
                    return
            else:
                variable = variables[edge]
                clause.append(-variable if desired else variable)
        clauses.add(tuple(sorted(clause)))

    for chosen in combinations(range(18), 4):
        forbid(chosen, 63)
    forbidden_five_words = [0] + sorted(path_words)
    for chosen in combinations(range(18), 5):
        for word in forbidden_five_words:
            forbid(chosen, word)
    ordered = sorted(clauses, key=lambda clause: (len(clause), clause))
    need(() not in clauses, "fixed core is already inconsistent")
    return free, ordered


def dimacs(variables, clauses):
    return (f"p cnf {variables} {len(clauses)}\n"
            + "".join(" ".join(map(str, clause)) + " 0\n"
                      for clause in clauses))


def parse_proof(path, variables):
    actions = []
    for number, line in enumerate(path.read_text().splitlines(), 1):
        tokens = line.split()
        need(tokens, f"blank proof line {number}")
        deleting = tokens[0] == "d"
        values = list(map(int, tokens[1:] if deleting else tokens))
        need(values and values[-1] == 0 and 0 not in values[:-1],
             f"malformed proof line {number}")
        clause = tuple(values[:-1])
        need(all(1 <= abs(value) <= variables for value in clause),
             f"proof variable range line {number}")
        need(len(set(clause)) == len(clause)
             and not any(-value in clause for value in clause),
             f"noncanonical proof clause line {number}")
        actions.append((deleting, clause))
    return actions


def mask_clause(clause):
    positive = negative = 0
    for literal in clause:
        bit = 1 << (abs(literal) - 1)
        if literal > 0:
            positive |= bit
        else:
            negative |= bit
    return positive, negative


def rup_by_full_scans(masked_formula, candidate):
    """Definition-level RUP with no occurrence lists or source checker code."""
    true = false = 0
    for literal in candidate:
        bit = 1 << (abs(literal) - 1)
        if literal > 0:
            need(not (true & bit), "contradictory candidate assumptions")
            false |= bit
        else:
            need(not (false & bit), "contradictory candidate assumptions")
            true |= bit
    passes = 0
    propagated = 0
    while True:
        passes += 1
        changed = False
        assigned = true | false
        for positive, negative in masked_formula:
            if positive & true or negative & false:
                continue
            unassigned = (positive | negative) & ~assigned
            if not unassigned:
                return True, passes, propagated
            if unassigned & (unassigned - 1):
                continue
            bit = unassigned
            if positive & bit:
                true |= bit
            else:
                false |= bit
            assigned |= bit
            propagated += 1
            changed = True
        if not changed:
            return False, passes, propagated


def verify_proof(path, variables, clauses):
    actions = parse_proof(path, variables)
    masked = [mask_clause(clause) for clause in clauses]
    additions = deletions = 0
    total_passes = total_propagated = 0
    empty = False
    for deleting, clause in actions:
        if deleting:
            # Retention is sound because every retained original or RUP-added
            # clause is already a consequence of the original formula.
            deletions += 1
            continue
        valid, passes, propagated = rup_by_full_scans(masked, clause)
        need(valid, f"non-RUP addition {additions + deletions + 1}")
        masked.append(mask_clause(clause))
        additions += 1
        total_passes += passes
        total_propagated += propagated
        empty |= not clause
    need(empty, "proof does not derive the empty clause")
    return additions, deletions, total_passes, total_propagated


def incidence_bounds():
    rows = []
    for red_degree in range(18, 25):
        blue_degree = 42 - red_degree
        red_paths = (comb(red_degree, 5) + comb(18, 5) - 1) // comb(18, 5)
        blue_paths = (comb(blue_degree, 5) + comb(18, 5) - 1) // comb(18, 5)
        rows.append([red_degree, red_paths, blue_degree, blue_paths,
                     red_paths + blue_paths])
    need(min(row[-1] for row in rows) == 6, "two-color incidence bound")
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot_root", type=Path)
    args = parser.parse_args()
    source = args.snapshot_root.resolve() / SOURCE_DIRECTORY
    need(source.is_dir(), "snapshot source directory")
    manifest_entries = verify_source(source)
    saved_inputs = json.loads((source / "INPUTS.json").read_text())["graphs"]
    case_receipts = {}
    for case in ("G1", "G2"):
        core_rows, path_words = audit_core(case, saved_inputs[case])
        free, clauses = build_formula(core_rows, path_words)
        expected = EXPECTED_CASES[case]
        need(len(core_rows) == expected["order"], "core order")
        need(len(free) == expected["variables"], "variable count")
        need(len(clauses) == expected["clauses"], "clause count")
        encoded = dimacs(len(free), clauses).encode()
        need(sha256(encoded).hexdigest() == expected["cnf_sha256"],
             "canonical formula identity")
        proof = source / f"{case}.proof"
        need(file_sha256(proof) == expected["proof_sha256"], "proof identity")
        additions, deletions, passes, propagated = verify_proof(
            proof, len(free), clauses
        )
        need((additions, deletions) ==
             (expected["additions"], expected["deletions"]),
             "proof action counts")
        case_receipts[case] = {
            "clauses": len(clauses),
            "core_order": len(core_rows),
            "core_vertex_critical": True,
            "free_physical_pairs": len(free),
            "proof_additions": additions,
            "proof_deletions_ignored_soundly": deletions,
            "rup_full_scan_passes": passes,
            "rup_propagations": propagated,
            "unsat": True,
        }
    degree_rows = incidence_bounds()
    receipt = {
        "cases": case_receipts,
        "degree_path_rows": degree_rows,
        "formula_builder": "independent forbidden truth-table enumeration",
        "independent_proof_method": "repeated full bit-mask clause scans",
        "manifest_entries": len(manifest_entries),
        "minimum_rooted_path_incidences_per_vertex": 6,
        "path_truth_words": 60,
        "rooted_path_incidences_across_both_colors": 258,
        "status": "INDEPENDENTLY_VERIFIED_H4015_EXTENSION_FAMILIES",
        "surviving_extension_families": 0,
        "target_good43_constructed": False,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
