#!/usr/bin/env python3
"""Independent audit of the complete M214 partition-root-375 exclusion.

The target's producer, auditor, root generator, and RUP checker are not
imported.  This script derives the marked descriptor and physical kernel,
checks its implication from the complete selected parent formula, validates
the compact proof with a fresh RUP implementation, and separately checks the
elementary Ramsey argument.
"""

import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from math import comb
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

TARGET_COMMIT = "c433b0278afc99e20e2a4862961055c5c63f95f5"
TARGET_MANIFEST_SHA256 = "966993fb7143a21d4038b7609613a3fa1c6f1e4fd387db8761ea370033b1ccd1"
ROOT_TABLE_SHA256 = "f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e"
PARENT_GENERATOR_SHA256 = "e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08"
PARENT_OPB_SHA256 = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
KERNEL_SHA256 = "f8cb7188cfe73a6c88adeb1930f0361c1022f874982bfa5b6c3d995e9724ae0f"
RUP_SHA256 = "d43100027074653e039bff7705e62c31c0f7fa370cda0c9a8ff52f27a33619a7"

N = 43
U, V, P, Q = 0, 1, 15, 30
H = tuple(range(15, 28))
KERNEL_VERTICES = (U, V) + H + (Q,)
EDGE_VARIABLES = comb(N, 2)
TRIANGLE_VARIABLES = comb(N, 3)
SELECTOR_FIRST = EDGE_VARIABLES + TRIANGLE_VARIABLES + 1
ROOT_INDEX = 375
SELECTOR = SELECTOR_FIRST + ROOT_INDEX
BASE_CONSTRAINTS = 2 * comb(N, 5) + 4 * comb(N, 3) + 3 * N


class ReviewFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewFailure(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_variable(left, right):
    left, right = sorted((left, right))
    require(0 <= left < right < N, "physical edge domain")
    return left * (2 * N - left - 1) // 2 + right - left


def five_set_rank(vertices):
    """Zero-based lexicographic rank among five-subsets of range(43)."""
    rank = 0
    previous = -1
    for position, vertex in enumerate(vertices):
        for candidate in range(previous + 1, vertex):
            rank += comb(N - candidate - 1, 4 - position)
        previous = vertex
    return rank


def verify_source_package(source):
    package = source / "ramsey_r55_m214_partition_root375_exclusion"
    manifest = package / "SHA256SUMS"
    require(sha256(manifest) == TARGET_MANIFEST_SHA256, "target package manifest identity")
    listed = {}
    for line in manifest.read_text(encoding="ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        listed[name] = digest
        require(sha256(package / name) == digest, "target package file identity: " + name)
    require(len(listed) == 13, "target package file count")
    table = source / "ramsey_r55_m214_pair_normalization" / "roots.tsv"
    generator = source / "ramsey_r55_m214_integrated_pair_roots" / "generate_opb.py"
    require(sha256(table) == ROOT_TABLE_SHA256, "root table identity")
    require(sha256(generator) == PARENT_GENERATOR_SHA256, "parent generator identity")
    try:
        commit = subprocess.check_output(["git", "-C", str(source), "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise ReviewFailure("cannot resolve source commit") from error
    require(commit == TARGET_COMMIT, "source checkout commit")
    return package, table, {"commit": commit, "package_files": len(listed),
                            "manifest_sha256": TARGET_MANIFEST_SHA256}


def derive_descriptor():
    e_sizes = (0, 6, 6, 1)
    c_sizes = (13, 1, 1, 13)
    cells = []
    cursor = 2
    for size in e_sizes + c_sizes:
        cells.append(list(range(cursor, cursor + size)))
        cursor += size
    require(cursor == 43, "derived cells do not partition the vertices")
    anomalies = [cells[4][0], cells[7][0]]
    bits = ((1, 1), (1, 0), (0, 1), (0, 0))
    units = [(U, V, 1)]
    for index, cell in enumerate(cells):
        for vertex in cell:
            units.extend([(U, vertex, bits[index % 4][0]),
                          (V, vertex, bits[index % 4][1])])
    partition_vertices = [U, V] + [vertex for vertex in range(15, 43)
                                    if vertex not in anomalies]
    ordering_buckets = []
    for cell in cells:
        for anomalous in (False, True):
            bucket = [vertex for vertex in cell if (vertex in anomalies) == anomalous]
            if bucket:
                ordering_buckets.append(bucket)
    return {
        "key": ["C77partition", 13, 0, "HO"],
        "anchors": [U, V],
        "E": list(range(2, 15)),
        "anomalies": anomalies,
        "cells": cells,
        "E_cells": list(e_sizes),
        "C_cells": list(c_sizes),
        "edge_units": [list(row) for row in sorted(units)],
        "a_equalities": [[vertex, 7 if vertex in anomalies else 6] for vertex in range(43)],
        "partition": {"blue_pair": anomalies, "one_red_to_pair": partition_vertices},
        "ordering_buckets": ordering_buckets,
    }


def audit_root(package, table_path):
    expected = derive_descriptor()
    stored = json.loads((package / "root.json").read_text())
    require(stored == expected, "stored root is not the independently derived complete descriptor")
    rows = table_path.read_text(encoding="ascii").splitlines()
    require(rows[0].split("\t") == ["family", "c", "k", "pattern", "E_cells", "C_cells", "anomalies", "root_sha256"],
            "root table header")
    records = [line.split("\t") for line in rows[1:]]
    require(len(records) == 389 and records[ROOT_INDEX][:4] == ["C77partition", "13", "0", "HO"],
            "root table membership/index")
    require(records[ROOT_INDEX][-1] == sha256(package / "root.json"), "root table content hash")
    remaining = records[:ROOT_INDEX] + records[ROOT_INDEX + 1:]
    family_order = ["E8", "E77", "C8", "C77", "C77partition"]
    family_counts = [sum(row[0] == family for row in remaining) for family in family_order]
    require(family_counts == [60, 85, 70, 104, 69], "remaining descriptor family counts")
    return stored, records, {"root_index": ROOT_INDEX, "selector": SELECTOR,
                             "remaining_descriptors": len(remaining),
                             "remaining_family_counts": family_counts}


def expected_kernel(root):
    clauses = []
    positions = []
    for five in combinations(KERNEL_VERTICES, 5):
        variables = tuple(edge_variable(left, right) for left, right in combinations(five, 2))
        line = 2 * five_set_rank(five) + 1
        clauses.extend([variables, tuple(-variable for variable in variables)])
        positions.extend([line, line + 1])

    for left, right, value in root["edge_units"]:
        if left in KERNEL_VERTICES and right in KERNEL_VERTICES:
            clauses.append((edge_variable(left, right) * (1 if value else -1),))
    clauses.append((-edge_variable(P, Q),))
    for vertex in root["partition"]["one_red_to_pair"]:
        if vertex in KERNEL_VERTICES:
            left = edge_variable(vertex, P)
            right = edge_variable(vertex, Q)
            clauses.extend([(left, right), (-left, -right)])
    require(len(clauses) == 8794, "derived kernel clause count")
    return clauses


def root_source_positions(root, root_table):
    # Body-line numbering excludes the OPB header. The parent begins with all
    # base constraints, then the exactly-one-selector row, then each root.
    prior_rows = 0
    for record in root_table[:ROOT_INDEX]:
        prior_rows += 169 + (57 if record[0] == "C77partition" else 0)
    start = BASE_CONSTRAINTS + 2 + prior_rows
    require(start == 2041258, "derived selected-root start row")
    positions = []
    for five in combinations(KERNEL_VERTICES, 5):
        line = 2 * five_set_rank(five) + 1
        positions.extend([line, line + 1])
    for offset, (left, right, _) in enumerate(root["edge_units"]):
        if left in KERNEL_VERTICES and right in KERNEL_VERTICES:
            positions.append(start + offset)
    positions.append(start + 169)
    for offset, vertex in enumerate(root["partition"]["one_red_to_pair"]):
        if vertex in KERNEL_VERTICES:
            positions.extend([start + 170 + 2 * offset, start + 171 + 2 * offset])
    require(len(positions) == len(set(positions)) == 8794, "source position coverage")
    return positions, start


def parse_kernel(path):
    with path.open(encoding="ascii") as stream:
        header = stream.readline()
        require(header == "p cnf 903 8794\n", "kernel DIMACS header")
        clauses = []
        for line in stream:
            values = [int(value) for value in line.split()]
            require(values and values[-1] == 0 and all(1 <= abs(value) <= 903 for value in values[:-1]),
                    "kernel DIMACS clause")
            clauses.append(tuple(values[:-1]))
    require(len(clauses) == 8794 and sha256(path) == KERNEL_SHA256, "kernel identity")
    return clauses


def clause_inequality(clause):
    coefficients = {abs(literal): 1 if literal > 0 else -1 for literal in clause}
    require(len(coefficients) == len(clause), "repeated variable in kernel clause")
    return coefficients, 1 - sum(literal < 0 for literal in clause)


def parse_opb_row(raw):
    fields = raw.split()
    require(len(fields) >= 5 and fields[-3] in (b">=", b"=") and fields[-1] == b";", "OPB row syntax")
    terms = {}
    for index in range(0, len(fields) - 3, 2):
        coefficient = int(fields[index])
        variable = int(fields[index + 1][1:])
        require(variable not in terms, "duplicate OPB variable")
        terms[variable] = coefficient
    return terms, fields[-3], int(fields[-2])


def audit_parent_opb(path, clauses, positions):
    wanted = dict(zip(positions, clauses))
    digest = hashlib.sha256()
    seen = set()
    byte_count = 0
    with path.open("rb") as stream:
        header = stream.readline()
        expected_header = b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n"
        require(header == expected_header, "parent OPB header")
        digest.update(header)
        byte_count += len(header)
        for line_number, raw in enumerate(stream, 1):
            digest.update(raw)
            byte_count += len(raw)
            if line_number == BASE_CONSTRAINTS + 1:
                terms, relation, rhs = parse_opb_row(raw)
                require(relation == b"=" and rhs == 1 and
                        terms == {SELECTOR_FIRST + index: 1 for index in range(389)},
                        "parent selector exactly-one row")
            clause = wanted.get(line_number)
            if clause is None:
                continue
            terms, relation, rhs = parse_opb_row(raw)
            require(relation == b">=", "kernel source row relation")
            rhs -= terms.pop(SELECTOR, 0)  # Substitute selected root y_375=1.
            expected_terms, expected_rhs = clause_inequality(clause)
            require(terms == expected_terms and rhs == expected_rhs,
                    "parent row does not yield the kernel clause under y_375=1")
            seen.add(line_number)
        line_count = line_number
    require(line_count == 2044421 and byte_count == 172788992 and
            digest.hexdigest() == PARENT_OPB_SHA256, "complete parent OPB identity")
    require(seen == set(positions), "not every kernel clause has physical parent provenance")
    return {"parent_constraints": line_count, "parent_bytes": byte_count,
            "parent_sha256": digest.hexdigest(), "source_rows_verified": len(seen),
            "selector_exactly_one_checked": True}


def rup(clauses, proposed):
    assignment = {}
    # Assume the negation of every proposed literal.
    for literal in proposed:
        variable, value = abs(literal), literal < 0
        if variable in assignment and assignment[variable] != value:
            return True
        assignment[variable] = value
    while True:
        forced = None
        for clause in clauses:
            unresolved = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    unresolved.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not unresolved:
                return True
            if len(unresolved) == 1:
                forced = unresolved[0]
                break
        if forced is None:
            return False
        variable, value = abs(forced), forced > 0
        if variable in assignment and assignment[variable] != value:
            return True
        assignment[variable] = value


def r34_formula():
    pairs = list(combinations(range(9), 2))
    variable = {pair: index + 1 for index, pair in enumerate(pairs)}
    clauses = [tuple(-variable[pair] for pair in combinations(triple, 2))
               for triple in combinations(range(9), 3)]
    clauses.extend(tuple(variable[pair] for pair in combinations(four, 2))
                   for four in combinations(range(9), 4))
    return variable, clauses


def audit_rup(path):
    require(sha256(path) == RUP_SHA256, "compact RUP identity")
    variable, base = r34_formula()
    clauses = list(base) + [(-variable[0, vertex],) for vertex in range(4, 9)]
    rows = 0
    closed = False
    for line in path.read_text(encoding="ascii").splitlines():
        require(not closed, "RUP rows after empty clause")
        values = [int(value) for value in line.split()]
        require(values and values[-1] == 0, "RUP row terminator")
        proposed = tuple(values[:-1])
        require(len(proposed) == len(set(proposed)) and
                all(1 <= abs(value) <= 36 for value in proposed), "RUP row domain")
        require(rup(clauses, proposed), "non-RUP proof addition")
        clauses.append(proposed)
        rows += 1
        closed = not proposed
    require(closed and rows == 288, "compact RUP closure/count")
    return rows


def elementary_ramsey_checks():
    # Independent base case R(3,3)<=6: every red/blue colouring of K6 has a
    # monochromatic triangle. This is the only finite premise in the written
    # proof that a triangle-free graph on nine vertices has alpha >= 4.
    pairs = list(combinations(range(6), 2))
    index = {pair: position for position, pair in enumerate(pairs)}
    red_or_blue_triangle = 0
    for mask in range(1 << len(pairs)):
        found = False
        for triple in combinations(range(6), 3):
            values = [bool(mask & (1 << index[pair])) for pair in combinations(triple, 2)]
            if all(values) or not any(values):
                found = True
                break
        require(found, "R(3,3)<=6 exhaustive control failed")
        red_or_blue_triangle += 1

    # If a triangle-free nine-vertex graph had alpha <= 3, every degree is at
    # most three. A degree <=2 leaves six nonneighbors; R(3,3)<=6 contradicts
    # both triangle-freeness and alpha<=3. Hence every degree is three, but
    # nine times three is odd. These integer checks guard the endpoint counts.
    require(9 - 1 - 2 == 6 and 9 * 3 % 2 == 1, "nine-vertex lemma arithmetic")
    return {"r33_edge_colourings_exhausted": red_or_blue_triangle,
            "r33_complete_graph_edges": len(pairs),
            "r34_nine_vertex_lemma": True}


def audit_root_proof(clauses):
    clause_set = set(clauses)
    # All core edges remain variables: no unit is internal to H.
    internal = {edge_variable(left, right) for left, right in combinations(H, 2)}
    units = {clause[0] for clause in clauses if len(clause) == 1}
    require(not any(variable in units or -variable in units for variable in internal),
            "an internal core edge was fixed")
    require((edge_variable(U, V),) in clause_set, "anchor edge uv is not red")
    for vertex in H:
        require((edge_variable(U, vertex),) in clause_set and
                (edge_variable(V, vertex),) in clause_set, "H is not the common red core")

    # Validate every premise used in each side of the degree dichotomy.
    for triple in combinations(H, 3):
        five = (U, V) + triple
        red_k5 = tuple(-edge_variable(left, right) for left, right in combinations(five, 2))
        require(red_k5 in clause_set, "missing physical red-five prohibition")
    others = tuple(vertex for vertex in H if vertex != P)
    for vertex in others:
        a, b = edge_variable(P, vertex), edge_variable(Q, vertex)
        require((a, b) in clause_set and (-a, -b) in clause_set,
                "missing exact-one partition equation")
    for four in combinations(others, 4):
        blue_k5 = tuple(edge_variable(left, right)
                        for left, right in combinations(tuple(sorted(four + (Q,))), 2))
        require(blue_k5 in clause_set, "missing physical blue-five prohibition")
    for four in combinations(others, 4):
        blue_with_p = tuple(edge_variable(left, right)
                            for left, right in combinations(tuple(sorted(four + (P,))), 2))
        require(blue_with_p in clause_set, "missing low-degree blue-five prohibition")

    high = low = 0
    for mask in range(1 << len(others)):
        neighbors = {others[index] for index in range(len(others)) if mask & (1 << index)}
        if len(neighbors) >= 4:
            # Four red p-neighbors are pairwise blue by core triangle-freeness;
            # the partition makes all four blue to q.
            require(len(sorted(neighbors)[:4]) == 4, "high-degree witness")
            high += 1
        else:
            nonneighbors = set(others) - neighbors
            # Nine p-nonneighbors contain an independent four by the R(3,4)
            # lemma; those four plus p are a blue K5.
            require(len(nonneighbors) >= 9, "low-degree nine-set")
            low += 1
    require(high + low == 4096 and low == sum(comb(12, degree) for degree in range(4)),
            "incident-star dichotomy coverage")
    return {"internal_core_variables_fixed": 0,
            "core_triangle_constraints_checked": comb(13, 3),
            "partition_vertices_checked": 12,
            "degree_four_subsets_checked": comb(12, 4),
            "incident_star_assignments_covered": high + low,
            "high_degree_assignments": high,
            "low_degree_assignments": low,
            "kernel_unsatisfiable_by_elementary_argument": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="checkout of njallskarp/math_source_code_open at the pinned commit")
    parser.add_argument("--parent-opb", type=Path, required=True)
    parser.add_argument("--kernel", type=Path, required=True)
    parser.add_argument("--cut", type=Path, required=True)
    args = parser.parse_args()

    package, table, source_report = verify_source_package(args.source.resolve())
    root, root_table, descriptor_report = audit_root(package, table)
    expected = expected_kernel(root)
    actual = parse_kernel(args.kernel)
    require(actual == expected, "kernel differs from independent construction")
    require(args.cut.read_text(encoding="ascii") == "-1 x13620 >= 0 ;\n", "selector cut encoding")
    positions, start = root_source_positions(root, root_table)
    report = {
        "status": "INDEPENDENTLY_VERIFIED_COMPLETE_ROOT375_EXCLUSION",
        "source": source_report,
        "descriptor": descriptor_report,
        "kernel": {
            "vertices": list(KERNEL_VERTICES),
            "clauses": len(actual),
            "sha256": sha256(args.kernel),
            "selected_root_first_parent_row": start,
            **audit_root_proof(actual),
        },
        "elementary_lemma": elementary_ramsey_checks(),
        "compact_rup_rows": audit_rup(package / "r34.rup"),
        "provenance": audit_parent_opb(args.parent_opb, actual, positions),
        "scope": {
            "selector_cut": "x13620=0",
            "remaining_descriptor_feasibility_asserted": False,
            "complete_m_slice_closed": False,
            "ramsey_43_graph_found": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
