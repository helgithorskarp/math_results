#!/usr/bin/env python3
"""Independent audit of the complete M214 partition-root-376 exclusion.

Nothing from the target's producer, auditor, root generator, or RUP checker is
imported.  This script reconstructs the marked descriptor and every parent OPB
row used by the proof, replays the compact small-Ramsey certificate with a
fresh checker, and verifies the elementary triangle-count contradiction.
"""

import argparse
from collections import Counter
import hashlib
from itertools import combinations, product
import json
from math import comb
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

TARGET_COMMIT = "5cb7a179c691a413b20e939b26cf5910d593a578"
TARGET_MANIFEST_SHA256 = "af567b371eccbf850077e67256effa6e17dfc01564adc62169f65cb053a0ccf6"
ROOT_TABLE_SHA256 = "f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e"
PARENT_GENERATOR_SHA256 = "e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08"
PARENT_OPB_SHA256 = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
CERTIFICATE_SHA256 = "21e4db1f231bbde4697d571014495703e9cc2ff33cafce058ef3934b9812fb80"
RUP_SHA256 = "d43100027074653e039bff7705e62c31c0f7fa370cda0c9a8ff52f27a33619a7"

N = 43
U, V, Z, P, Q = 0, 1, 14, 28, 29
E = tuple(range(2, 15))
H = tuple(range(15, 28))
A = tuple(range(2, 8)) + (P,)
B = tuple(range(8, 14)) + (Q,)
ROOT_INDEX = 376
EDGE_VARIABLES = comb(N, 2)
TRIANGLE_VARIABLES = comb(N, 3)
SELECTOR_FIRST = EDGE_VARIABLES + TRIANGLE_VARIABLES + 1
SELECTOR = SELECTOR_FIRST + ROOT_INDEX
BASE_CONSTRAINTS = 2 * comb(N, 5) + 4 * comb(N, 3) + 3 * N


class ReviewFailure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise ReviewFailure(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge(left, right):
    left, right = sorted((left, right))
    require(0 <= left < right < N, "physical edge domain")
    return left * (2 * N - left - 1) // 2 + right - left


def subset_rank(vertices, n=N):
    rank = 0
    previous = -1
    size = len(vertices)
    for position, vertex in enumerate(vertices):
        for candidate in range(previous + 1, vertex):
            rank += comb(n - candidate - 1, size - position - 1)
        previous = vertex
    return rank


def triangle(vertex_set):
    return EDGE_VARIABLES + 1 + subset_rank(tuple(sorted(vertex_set)))


def verify_source_package(source):
    package = source / "ramsey_r55_m214_partition_root376_triangle_certificate"
    manifest = package / "SHA256SUMS"
    require(sha256(manifest) == TARGET_MANIFEST_SHA256, "target manifest identity")
    listed = {}
    for line in manifest.read_text(encoding="ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        listed[name] = digest
        require(sha256(package / name) == digest, "target file identity: " + name)
    require(len(listed) == 11, "target manifest entry count")
    table = source / "ramsey_r55_m214_pair_normalization" / "roots.tsv"
    generator = source / "ramsey_r55_m214_integrated_pair_roots" / "generate_opb.py"
    require(sha256(table) == ROOT_TABLE_SHA256, "root table identity")
    require(sha256(generator) == PARENT_GENERATOR_SHA256, "parent generator identity")
    try:
        commit = subprocess.check_output(
            ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError) as error:
        raise ReviewFailure("cannot resolve source commit") from error
    require(commit == TARGET_COMMIT, "source checkout commit")
    return package, table, {
        "commit": commit,
        "manifest_entries": len(listed),
        "manifest_sha256": TARGET_MANIFEST_SHA256,
    }


def derive_descriptor():
    e_sizes = (0, 6, 6, 1)
    c_sizes = (13, 1, 1, 13)
    cells = []
    cursor = 2
    for size in e_sizes + c_sizes:
        cells.append(list(range(cursor, cursor + size)))
        cursor += size
    require(cursor == N, "cell partition")
    anomalies = [cells[5][0], cells[6][0]]
    status_bits = ((1, 1), (1, 0), (0, 1), (0, 0))
    units = [(U, V, 1)]
    for index, cell in enumerate(cells):
        for vertex in cell:
            left, right = status_bits[index % 4]
            units.extend(((U, vertex, left), (V, vertex, right)))
    central = [U, V] + [w for w in range(15, N) if w not in anomalies]
    buckets = []
    for cell in cells:
        for anomalous in (False, True):
            bucket = [w for w in cell if (w in anomalies) == anomalous]
            if bucket:
                buckets.append(bucket)
    return {
        "key": ["C77partition", 13, 0, "AB"],
        "anchors": [U, V],
        "E": list(E),
        "anomalies": anomalies,
        "cells": cells,
        "E_cells": list(e_sizes),
        "C_cells": list(c_sizes),
        "edge_units": [list(row) for row in sorted(units)],
        "a_equalities": [[w, 7 if w in anomalies else 6] for w in range(N)],
        "partition": {"blue_pair": anomalies, "one_red_to_pair": central},
        "ordering_buckets": buckets,
    }


def audit_descriptor(package, table_path):
    root_path = package / "root.json"
    stored = json.loads(root_path.read_text(encoding="ascii"))
    require(stored == derive_descriptor(), "stored root differs from independent descriptor")
    rows = table_path.read_text(encoding="ascii").splitlines()
    require(
        rows[0].split("\t")
        == ["family", "c", "k", "pattern", "E_cells", "C_cells", "anomalies", "root_sha256"],
        "root table header",
    )
    records = [line.split("\t") for line in rows[1:]]
    require(len(records) == 389, "root table size")
    require(records[ROOT_INDEX][:4] == ["C77partition", "13", "0", "AB"], "root index/key")
    require(records[ROOT_INDEX][-1] == sha256(root_path), "root table descriptor hash")
    slice_rows = [(index, row[3]) for index, row in enumerate(records)
                  if row[:3] == ["C77partition", "13", "0"]]
    require(slice_rows == [(375, "HO"), (376, "AB")], "complete c13 k0 partition slice")
    retained = [row for index, row in enumerate(records) if index not in (375, 376)]
    families = ["E8", "E77", "C8", "C77", "C77partition"]
    counts = [sum(row[0] == family for row in retained) for family in families]
    require(counts == [60, 85, 70, 104, 68], "remaining family census")
    return stored, records, {
        "root_index": ROOT_INDEX,
        "selector": SELECTOR,
        "two_pattern_slice": slice_rows,
        "remaining_after_both_cuts": len(retained),
        "remaining_family_counts": counts,
    }


def put(wanted, row, terms, relation, rhs):
    normalized = (dict(terms), relation, rhs)
    require(row not in wanted or wanted[row] == normalized, "conflicting expected OPB row")
    wanted[row] = normalized


def five_row(wanted, vertices, red):
    vertices = tuple(sorted(vertices))
    signed = [edge(a, b) * (-1 if red else 1) for a, b in combinations(vertices, 2)]
    row = 2 * subset_rank(vertices) + (2 if red else 1)
    put(wanted, row, [(abs(value), 1 if value > 0 else -1) for value in signed],
        b">=", -9 if red else 1)


def root_first_row(records):
    prior = sum(169 + (57 if row[0] == "C77partition" else 0)
                for row in records[:ROOT_INDEX])
    first = BASE_CONSTRAINTS + 2 + prior
    require(first == 2041484, "selected-root first row")
    return first


def expected_parent_rows(root, records):
    wanted = {}
    first = root_first_row(records)

    # All physical clique clauses used by the three local bounds.
    for triple in combinations(H, 3):
        five_row(wanted, (U, V) + triple, True)
    for five in combinations(H, 5):
        five_row(wanted, five, False)
    for four in combinations(H, 4):
        five_row(wanted, (Z,) + four, False)
    for anchor, cell in ((U, A), (V, B)):
        for four in combinations(cell, 4):
            five_row(wanted, (anchor,) + four, True)
    clique_rows = len(wanted)
    require(clique_rows == 2358, "proof-used five-set row count")

    # All anchor units, the H-to-E equations, and the H anomaly partition.
    for offset, (a, b, value) in enumerate(root["edge_units"]):
        variable = edge(a, b)
        put(wanted, first + offset,
            [(variable, 1 if value else -1), (SELECTOR, -1)],
            b">=", 0 if value else -1)
    for h in H:
        variables = [edge(h, e) for e in E]
        put(wanted, first + 83 + 2 * h,
            [(variable, 1) for variable in variables] + [(SELECTOR, -6)], b">=", 0)
        put(wanted, first + 84 + 2 * h,
            [(variable, -1) for variable in variables] + [(SELECTOR, -7)], b">=", -13)
        offset = root["partition"]["one_red_to_pair"].index(h)
        variables = [edge(h, P), edge(h, Q)]
        put(wanted, first + 170 + 2 * offset,
            [(variable, 1) for variable in variables] + [(SELECTOR, -1)], b">=", 0)
        put(wanted, first + 171 + 2 * offset,
            [(variable, -1) for variable in variables] + [(SELECTOR, -1)], b">=", -2)

    # Exact conjunction rows for every triangle incident with u or v.
    incident_triangles = 0
    for vertices in combinations(range(N), 3):
        if U not in vertices and V not in vertices:
            continue
        z = triangle(vertices)
        variables = [edge(a, b) for a, b in combinations(vertices, 2)]
        row = 2 * comb(N, 5) + 4 * (z - EDGE_VARIABLES - 1) + 1
        for index, variable in enumerate(variables):
            put(wanted, row + index, [(z, -1), (variable, 1)], b">=", 0)
        put(wanted, row + 3, [(z, 1)] + [(variable, -1) for variable in variables], b">=", -2)
        incident_triangles += 1
    require(incident_triangles == 1681, "incident triangle count")

    for anchor in (U, V):
        variables = [triangle((anchor, a, b))
                     for a, b in combinations([w for w in range(N) if w != anchor], 2)]
        row = 2 * comb(N, 5) + 4 * comb(N, 3) + N + anchor + 1
        put(wanted, row, [(variable, 1) for variable in variables], b"=", 100)

    put(wanted, BASE_CONSTRAINTS + 1,
        [(SELECTOR_FIRST + index, 1) for index in range(389)], b"=", 1)
    require(len(wanted) == 9220, "complete proof-used source row count")
    return wanted, first, clique_rows, incident_triangles


def parse_opb_row(raw):
    fields = raw.split()
    require(len(fields) >= 5 and fields[-3] in (b">=", b"=") and fields[-1] == b";",
            "OPB row syntax")
    terms = {}
    for index in range(0, len(fields) - 3, 2):
        coefficient = int(fields[index])
        variable = int(fields[index + 1][1:])
        require(variable not in terms, "duplicate OPB variable")
        terms[variable] = coefficient
    return terms, fields[-3], int(fields[-2])


def audit_parent(path, wanted):
    digest = hashlib.sha256()
    seen = set()
    byte_count = 0
    with path.open("rb") as stream:
        header = stream.readline()
        require(header == b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n",
                "parent OPB header")
        digest.update(header)
        byte_count += len(header)
        for row, raw in enumerate(stream, 1):
            digest.update(raw)
            byte_count += len(raw)
            expected = wanted.get(row)
            if expected is None:
                continue
            require(parse_opb_row(raw) == expected, "parent row mismatch: " + str(row))
            seen.add(row)
        row_count = row
    require((row_count, byte_count) == (2044421, 172788992), "parent dimensions")
    require(digest.hexdigest() == PARENT_OPB_SHA256, "parent OPB identity")
    require(seen == set(wanted), "missing proof-used parent row")
    return {
        "constraints": row_count,
        "bytes": byte_count,
        "sha256": digest.hexdigest(),
        "proof_used_rows_verified": len(seen),
    }


def rup(clauses, proposed):
    assignment = {}
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


def audit_small_ramsey(rup_path):
    require(sha256(rup_path) == RUP_SHA256, "small-Ramsey RUP identity")
    pairs = list(combinations(range(9), 2))
    variable = {pair: index + 1 for index, pair in enumerate(pairs)}
    base = [tuple(-variable[pair] for pair in combinations(triple, 2))
            for triple in combinations(range(9), 3)]
    base.extend(tuple(variable[pair] for pair in combinations(four, 2))
                for four in combinations(range(9), 4))
    clauses = base + [(-variable[0, w],) for w in range(4, 9)]
    rows = 0
    closed = False
    for line in rup_path.read_text(encoding="ascii").splitlines():
        require(not closed, "RUP rows after empty clause")
        values = [int(value) for value in line.split()]
        require(values and values[-1] == 0, "RUP terminator")
        proposed = tuple(values[:-1])
        require(rup(clauses, proposed), "invalid RUP addition")
        clauses.append(proposed)
        rows += 1
        closed = not proposed
    require(closed and rows == 288, "RUP closure/count")

    # A separate exhaustive check of R(3,3)<=6 validates the only finite
    # premise in the short proof of R(3,4)<=9.
    k6_pairs = list(combinations(range(6), 2))
    positions = {pair: index for index, pair in enumerate(k6_pairs)}
    checked = 0
    for mask in range(1 << len(k6_pairs)):
        found = False
        for triple in combinations(range(6), 3):
            colors = [bool(mask & (1 << positions[pair]))
                      for pair in combinations(triple, 2)]
            if all(colors) or not any(colors):
                found = True
                break
        require(found, "R(3,3)<=6 exhaustion")
        checked += 1
    require(9 - 1 - 2 == 6 and (9 * 3) % 2 == 1, "R(3,4) proof arithmetic")
    return {
        "rup_rows": rows,
        "k6_edge_colorings_exhausted": checked,
        "r34_upper_bound": 9,
    }


def audit_turan_seven():
    pairs = list(combinations(range(7), 2))
    index = {pair: position for position, pair in enumerate(pairs)}
    k4_masks = [sum(1 << index[pair] for pair in combinations(four, 2))
                for four in combinations(range(7), 4)]
    violating_domain = 0
    for mask in range(1 << len(pairs)):
        if mask.bit_count() <= 16:
            continue
        violating_domain += 1
        require(any(mask & k4 == k4 for k4 in k4_masks), "K4-free graph above 16 edges")
    blocks = ({0, 1, 2}, {3, 4}, {5, 6})
    sharp = {pair for pair in pairs if not any(set(pair) <= block for block in blocks)}
    require(len(sharp) == 16, "sharp Turan witness size")
    require(all(not all(pair in sharp for pair in combinations(four, 2))
                for four in combinations(range(7), 4)), "sharp Turan witness K4-free")
    return {"graphs_with_at_least_17_edges_exhausted": violating_domain,
            "maximum_k4_free_edges": 16, "sharp_witness_checked": True}


def triangle_identity(root):
    fixed = {edge(a, b): value for a, b, value in root["edge_units"]}
    polynomial = Counter()
    constant = 0
    for anchor in (U, V):
        others = [w for w in range(N) if w != anchor]
        for a, b in combinations(others, 2):
            if fixed[edge(anchor, a)] and fixed[edge(anchor, b)]:
                variable = edge(a, b)
                if variable in fixed:
                    constant += fixed[variable]
                else:
                    polynomial[variable] += 1

    # Subtract the 13 H-to-E equations (right side 78) and the 13 anomaly
    # partition equations.  This is independent symbolic elimination in the
    # physical edge coordinates.
    for h in H:
        for e in E:
            polynomial[edge(h, e)] -= 1
        for anomaly in (P, Q):
            polynomial[edge(h, anomaly)] -= 1
    expected = Counter()
    for a, b in combinations(H, 2):
        expected[edge(a, b)] += 2
    for cell in (A, B):
        for a, b in combinations(cell, 2):
            expected[edge(a, b)] += 1
    for h in H:
        expected[edge(Z, h)] -= 1
    nonzero = Counter({variable: coefficient for variable, coefficient in polynomial.items()
                       if coefficient})
    require(dict(nonzero) == dict(expected), "physical triangle identity coefficients")
    require(constant == 26, "physical triangle identity constant")
    rhs = 200 - 13 * 6 - 13 - constant
    require(rhs == 83, "reduced triangle identity right side")

    # Check Boolean conjunction semantics separately from the target code.
    truth_cases = 0
    for a, b, c, z in product((0, 1), repeat=4):
        encoded = (z <= a and z <= b and z <= c and z >= a + b + c - 2)
        require(encoded == (z == a * b * c), "triangle product encoding")
        truth_cases += 1
    return {"nonzero_physical_coordinates": len(expected), "constant": constant,
            "reduced_rhs": rhs, "triangle_product_truth_cases": truth_cases}


def audit_scalar_certificate(path):
    require(sha256(path) == CERTIFICATE_SHA256, "scalar certificate identity")
    certificate = json.loads(path.read_text(encoding="ascii"))
    require(certificate["variables"] == ["eA", "eB", "twice_eH", "footprint_z"],
            "certificate coordinates")
    expected_rows = [([1, 0, 0, 0], 16), ([0, 1, 0, 0], 16),
                     ([0, 0, 1, 0], 52), ([0, 0, 0, -1], -5)]
    rows = [(row["coefficients"], row["rhs"]) for row in certificate["inequalities"]]
    require(rows == expected_rows, "certificate inequality rows")
    equality = certificate["equality"]
    require((equality["coefficients"], equality["rhs"]) == ([1, 1, 1, -1], 83),
            "certificate equality")
    multipliers = certificate["inequality_multipliers"]
    equality_multiplier = certificate["equality_multiplier"]
    require(multipliers == [1, 1, 1, 1] and equality_multiplier == -1,
            "certificate multipliers")
    coefficients = [sum(multiplier * row["coefficients"][column]
                        for multiplier, row in zip(multipliers, certificate["inequalities"]))
                    + equality_multiplier * equality["coefficients"][column]
                    for column in range(4)]
    rhs = sum(multiplier * row["rhs"]
              for multiplier, row in zip(multipliers, certificate["inequalities"]))
    rhs += equality_multiplier * equality["rhs"]
    require(coefficients == [0, 0, 0, 0] and rhs == -4, "exact Farkas contradiction")
    require(certificate["result"] == {"coefficients": coefficients, "rhs": rhs},
            "certificate recorded result")
    return {"coefficients": coefficients, "rhs": rhs}


def audit_mathematical_bounds():
    # H is triangle-free.  Five red neighbors of a core vertex would be an
    # independent five-set, so Delta(H)<=4 and 2e(H)<=13*4.
    require(13 * 4 == 52, "core degree bound")
    # If z has at most four red H-neighbors, at least nine are blue to z;
    # R(3,4)<=9 gives a red triangle or blue K4 in H.  The former is already
    # impossible and the latter extends through z.
    require(13 - 4 == 9, "outside footprint bound")
    # Both seven-vertex A/B graphs are K4-free, hence each has at most 16
    # edges.  The exact identity then contradicts the required triangle sum.
    upper = 52 + 117 - 5 + 16 + 16
    require(upper == 196 and upper < 200, "four-unit triangle gap")
    return {"twice_core_edge_upper_bound": 52, "footprint_lower_bound": 5,
            "off_diagonal_sum_upper_bound": 32,
            "anchor_triangle_upper_bound": upper,
            "required_anchor_triangle_sum": 200,
            "gap": 200 - upper}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True,
                        help="checkout of njallskarp/math_source_code_open at the pinned commit")
    parser.add_argument("--parent-opb", type=Path, required=True)
    parser.add_argument("--cut", type=Path, required=True)
    arguments = parser.parse_args()

    package, table, source_report = verify_source_package(arguments.source.resolve())
    root, records, descriptor_report = audit_descriptor(package, table)
    wanted, first, clique_rows, incident_triangles = expected_parent_rows(root, records)
    require(arguments.cut.read_text(encoding="ascii") == "-1 x13621 >= 0 ;\n",
            "selector cut encoding")
    report = {
        "status": "INDEPENDENTLY_VERIFIED_COMPLETE_ROOT376_TRIANGLE_EXCLUSION",
        "source": source_report,
        "descriptor": descriptor_report,
        "physical_formula": {
            "selected_root_first_row": first,
            "proof_used_five_set_rows": clique_rows,
            "incident_triangles_reconstructed": incident_triangles,
            **audit_parent(arguments.parent_opb, wanted),
        },
        "triangle_identity": triangle_identity(root),
        "small_ramsey": audit_small_ramsey(package / "r34.rup"),
        "turan_seven": audit_turan_seven(),
        "bounds": audit_mathematical_bounds(),
        "farkas": audit_scalar_certificate(package / "certificate.json"),
        "scope": {
            "selector_cut": "x13621=0",
            "root_core_variables_fixed": 0,
            "remaining_descriptor_feasibility_asserted": False,
            "complete_m_slice_closed": False,
            "ramsey_43_graph_found": False,
            "ramsey_bound_changed": False,
        },
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
