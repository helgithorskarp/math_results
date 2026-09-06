#!/usr/bin/env python3
"""Independent checker for the complete M214 c=13,k=0 weighted-cell exclusion.

This program imports none of the contribution's Python modules.  It rebuilds
the finite equality cover and every normalized CNF, checks the small R(3,4)
RUP proof with a fresh implementation, reconstructs all parent-OPB rows used
by the global consumer, verifies the exact coefficient identities, and asks
two separately built native checkers to validate each regenerated proof.
"""

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations, permutations, product
import json
from math import comb
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

SOURCE_COMMIT = "1f75c9bf4b1a5ced5fae6cb616e20dd0fc4a2460"
MANIFEST_SHA256 = "3fe3f13fe9aa7e26f989c5e81374325716f42b1dbf9522cdcebe25e93699d148"
ROOT_TABLE_SHA256 = "f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e"
PARENT_GENERATOR_SHA256 = "e6b26db8a05ee7c246b431b185bee2543697c2a7a720154bea70dfa2e10c8a08"
PARENT_OPB_SHA256 = "469879cf7bc1c2147996163cd14a588a8bff41a3353c14e9bcc498d084f3783f"
CATALOG_SHA256 = "eb4d3f787f07ed14c0a82a83bee170ed096c24b6a7e971fded185ca1a760798f"
R34_SHA256 = "d43100027074653e039bff7705e62c31c0f7fa370cda0c9a8ff52f27a33619a7"
CERTIFICATE_SHA256 = "ba759e1667ce5309b0edba40313f15a370c4349e0a4554c28dfb9bef89182d89"

N = 43
U, V, Z, X_A, X_B = 0, 1, 14, 28, 29
E = tuple(range(2, 15))
H = tuple(range(15, 28))
A = tuple(range(2, 8)) + (X_A,)
B = tuple(range(8, 14)) + (X_B,)
ROOTS = (48, 128, 129, 201, 202, 299, 300, 376)
ALL_C13_K0 = (48, 128, 129, 201, 202, 299, 300, 375, 376)
EDGE_COUNT = comb(N, 2)
TRIANGLE_COUNT = comb(N, 3)
SELECTOR_FIRST = EDGE_COUNT + TRIANGLE_COUNT + 1
BASE_ROWS = 2 * comb(N, 5) + 4 * comb(N, 3) + 3 * N


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def checked_run(command, label):
    completed = subprocess.run(command, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, check=False)
    require(completed.returncode == 0, label + " rejected")


def verify_source(source):
    package = source / "ramsey_r55_m214_c13_k0_weighted_cell_exclusion"
    manifest = package / "SHA256SUMS"
    require(sha256(manifest) == MANIFEST_SHA256, "contribution manifest identity")
    entries = {}
    for line in manifest.read_text(encoding="ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        require(name not in entries, "duplicate manifest path")
        entries[name] = digest
        require(sha256(package / name) == digest, "source file identity: " + name)
    require(len(entries) == 14, "source manifest entry count")
    table = source / "ramsey_r55_m214_pair_normalization" / "roots.tsv"
    generator = source / "ramsey_r55_m214_integrated_pair_roots" / "generate_opb.py"
    require(sha256(table) == ROOT_TABLE_SHA256, "root table identity")
    require(sha256(generator) == PARENT_GENERATOR_SHA256, "parent generator identity")
    commit = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    require(commit == SOURCE_COMMIT, "source checkout commit")
    return package, table, {
        "commit": commit,
        "manifest_entries": len(entries),
        "manifest_sha256": MANIFEST_SHA256,
    }


def edge(left, right):
    left, right = sorted((left, right))
    require(0 <= left < right < N, "physical edge domain")
    return left * (2 * N - left - 1) // 2 + right - left


def subset_rank(vertices, n=N):
    result = 0
    previous = -1
    size = len(vertices)
    for position, vertex in enumerate(vertices):
        result += sum(comb(n - candidate - 1, size - position - 1)
                      for candidate in range(previous + 1, vertex))
        previous = vertex
    return result


def triangle(vertices):
    return EDGE_COUNT + 1 + subset_rank(tuple(sorted(vertices)))


def is_rup(database, proposed):
    # Negate the proposed clause and propagate all unit consequences.
    assignment = {}
    for literal in proposed:
        variable, value = abs(literal), literal < 0
        if variable in assignment and assignment[variable] != value:
            return True
        assignment[variable] = value
    while True:
        changed = False
        for clause in database:
            open_literals = []
            satisfied = False
            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    open_literals.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not open_literals:
                return True
            if len(open_literals) == 1:
                literal = open_literals[0]
                variable, value = abs(literal), literal > 0
                if variable in assignment:
                    if assignment[variable] != value:
                        return True
                else:
                    assignment[variable] = value
                    changed = True
        if not changed:
            return False


def check_r34(package):
    proof = package / "r34.rup"
    require(sha256(proof) == R34_SHA256, "R(3,4) certificate identity")
    pairs = tuple(combinations(range(9), 2))
    number = {pair: index + 1 for index, pair in enumerate(pairs)}
    clauses = [tuple(-number[pair] for pair in combinations(q, 2))
               for q in combinations(range(9), 3)]
    clauses += [tuple(number[pair] for pair in combinations(q, 2))
                for q in combinations(range(9), 4)]
    clauses += [(-number[0, vertex],) for vertex in range(4, 9)]
    steps = 0
    closed = False
    for line in proof.read_text(encoding="ascii").splitlines():
        require(not closed, "RUP rows after terminal contradiction")
        fields = list(map(int, line.split()))
        require(fields and fields[-1] == 0, "RUP row terminator")
        row = tuple(fields[:-1])
        require(len(set(row)) == len(row), "RUP duplicate literal")
        require(all(1 <= abs(lit) <= 36 for lit in row), "RUP variable range")
        require(is_rup(clauses, row), "invalid RUP row " + str(steps + 1))
        clauses.append(row)
        steps += 1
        closed = not row
    require(closed and steps == 288, "complete R(3,4) RUP refutation")
    return steps


def decode_graph6(record):
    require(len(record) == 14 and record[0] - 63 == 13, "graph6 order/length")
    bits = "".join(f"{byte - 63:06b}" for byte in record[1:])
    pairs = ((left, right) for right in range(1, 13) for left in range(right))
    return {pair for pair, bit in zip(pairs, bits) if bit == "1"}


def finite_cover(package):
    # Exhaust all 2^15 six-vertex graphs; this separately obtains the sharp
    # edge bound and the complete K_2,2,2 equality family.
    pairs6 = tuple(combinations(range(6), 2))
    masks4 = [sum(1 << pairs6.index(pair) for pair in combinations(q, 2))
              for q in combinations(range(6), 4)]
    extremizers = []
    for graph in range(1 << len(pairs6)):
        if any(graph & mask == mask for mask in masks4):
            continue
        require(graph.bit_count() <= 12, "six-vertex extremal edge bound")
        if graph.bit_count() == 12:
            missing = [pair for index, pair in enumerate(pairs6)
                       if not (graph >> index) & 1]
            require(sorted(vertex for pair in missing for vertex in pair)
                    == list(range(6)), "equality graph is K_2,2,2")
            extremizers.append(graph)
    require(len(extremizers) == 15, "all six-vertex equality graphs")

    parts = ((0, 1), (2, 3), (4, 5))
    stars = Counter()
    for mask in range(64):
        selected = {vertex for vertex in range(6) if mask >> vertex & 1}
        pattern = tuple(sorted(len(selected & set(part)) for part in parts))
        if pattern[0] == 0:
            stars[pattern] += 1
    expected_patterns = {
        (0, 0, 0), (0, 0, 1), (0, 0, 2),
        (0, 1, 1), (0, 1, 2), (0, 2, 2),
    }
    require(set(stars) == expected_patterns and sum(stars.values()) == 37,
            "all admissible stars and normalized patterns")
    # Independently check that part permutations and swaps transport every
    # admissible star to the chosen normalized form.
    transports = []
    for order in permutations(range(3)):
        for flips in product((0, 1), repeat=3):
            transports.append(tuple(parts[order[index]][position ^ flips[index]]
                                    for index in range(3) for position in range(2)))
    for mask in range(64):
        selected = {vertex for vertex in range(6) if mask >> vertex & 1}
        pattern = tuple(sorted(len(selected & set(part)) for part in parts))
        if pattern[0]:
            continue
        target = {2 * index + position for index, amount in enumerate(pattern)
                  for position in range(amount)}
        require(any({transport[vertex] for vertex in selected} == target
                    for transport in transports), "star normalization coverage")

    catalog_path = package / "r35_13.g6"
    require(sha256(catalog_path) == CATALOG_SHA256, "catalog fixture identity")
    records = catalog_path.read_bytes().splitlines()
    require(len(records) == 1, "one bundled order-13 catalog record")
    catalog = decode_graph6(records[0])
    mapping = (0, 1, 5, 12, 8, 2, 3, 10, 11, 9, 6, 7, 4)
    cyclic = lambda a, b: (a - b) % 13 in (1, 5, 8, 12)
    require(set(mapping) == set(range(13)), "catalog-to-cyclic bijection")
    require(all(((a, b) in catalog) == cyclic(mapping[a], mapping[b])
                for a, b in combinations(range(13), 2)), "catalog transport")
    require(all(sum(cyclic(a, b) for b in range(13) if b != a) == 4
                for a in range(13)), "cyclic core is 4-regular")
    require(all(not all(cyclic(a, b) for a, b in combinations(q, 2))
                for q in combinations(range(13), 3)), "cyclic core triangle-free")
    require(all(any(cyclic(a, b) for a, b in combinations(q, 2))
                for q in combinations(range(13), 5)), "cyclic core alpha at most four")

    affine = {tuple((scale * vertex + shift) % 13 for vertex in range(13))
              for scale in (1, 5, 8, 12) for shift in range(13)}
    require(len(affine) == 52, "affine map count")
    require(all(all(cyclic(a, b) == cyclic(phi[a], phi[b])
                    for a, b in combinations(range(13), 2))
                for phi in affine), "all affine maps are automorphisms")

    cases = []
    census = []
    for pattern in sorted(stars):
        size = sum(pattern)
        target_edges = pattern[1] * pattern[2]
        allowed = {choice for choice in combinations(range(13), size)
                   if sum(cyclic(a, b) for a, b in combinations(choice, 2))
                   == target_edges}
        representatives = {min(tuple(sorted(phi[v] for v in choice))
                               for phi in affine) for choice in allowed}
        expanded = {tuple(sorted(phi[v] for v in representative))
                    for representative in representatives for phi in affine}
        require(expanded == allowed, "affine orbit cover for " + str(pattern))
        cases.extend((pattern, representative)
                     for representative in sorted(representatives))
        census.append({"pattern": list(pattern), "subsets": len(allowed),
                       "orbits": len(representatives)})
    require(len(cases) == 8, "eight normalized equality cases")
    return cases, {
        "six_vertex_graphs": 1 << 15,
        "turan_extremizers": len(extremizers),
        "x_star_assignments": 64,
        "admissible_x_stars": sum(stars.values()),
        "catalog_records": len(records),
        "catalog_completeness": "IMPORTED_PRIMARY_SOURCE",
        "catalog_transport": list(mapping),
        "verified_affine_automorphisms": len(affine),
        "orbit_census": census,
    }


def expected_cnf(pattern, omitted):
    # Vertices 0..12 are H; 13=v; 14=x; 15..20 are three blue pairs.
    vertices = range(21)
    pairs = tuple(combinations(vertices, 2))
    variable = {pair: index + 1 for index, pair in enumerate(pairs)}
    fixed = {}
    for w in vertices:
        if w != 13:
            fixed[variable[tuple(sorted((13, w)))]] = w < 13
    for a, b in combinations(range(13), 2):
        fixed[variable[a, b]] = (a - b) % 13 in (1, 5, 8, 12)
    parts = (tuple(range(15, 17)), tuple(range(17, 19)), tuple(range(19, 21)))
    for a, b in combinations(range(15, 21), 2):
        fixed[variable[a, b]] = not any(a in part and b in part for part in parts)
    red_tail = {w for part, amount in zip(parts, pattern) for w in part[:amount]}
    for w in range(15, 21):
        fixed[variable[14, w]] = w in red_tail
    for h in range(13):
        fixed[variable[h, 14]] = h not in omitted
    require(len(fixed) == 132, "normalized fixed-bit count")

    clauses = []
    for size, positive in ((4, False), (5, True)):
        for clique in combinations(vertices, size):
            literals = [variable[pair] * (1 if positive else -1)
                        for pair in combinations(clique, 2)]
            if any(abs(literal) in fixed
                   and fixed[abs(literal)] == (literal > 0)
                   for literal in literals):
                continue
            clauses.append(tuple(literal for literal in literals
                                 if abs(literal) not in fixed))
    clauses.extend(((variable_id if value else -variable_id,)
                    for variable_id, value in fixed.items()))
    raw = (f"p cnf 210 {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses
    )).encode("ascii")
    return raw, clauses


def verify_cnfs_and_proofs(cases, replay, proof_index, drat_trim, lrat_check):
    results = []
    require(len(proof_index) == 8, "proof index length")
    for case, (pattern, omitted) in enumerate(cases):
        cnf = replay / f"case-{case}.cnf"
        drat = replay / f"case-{case}.drat"
        lrat = replay / f"case-{case}.lrat"
        raw, clauses = expected_cnf(pattern, omitted)
        require(cnf.read_bytes() == raw, "independent CNF mismatch for case " + str(case))
        entry = proof_index[case]
        require(entry["case"] == case, "proof index ordering")
        for kind, path in (("cnf", cnf), ("drat", drat), ("lrat", lrat)):
            require(sha256(path) == entry[kind + "_sha256"],
                    kind + " hash for case " + str(case))
            if kind != "cnf":
                require(path.stat().st_size == entry[kind + "_bytes"],
                        kind + " size for case " + str(case))
        checked_run([str(drat_trim), str(cnf), str(drat)],
                    "DRAT case " + str(case))
        checked_run([str(lrat_check), str(cnf), str(lrat)],
                    "LRAT case " + str(case))
        results.append({
            "case": case,
            "pattern": list(pattern),
            "omitted_core": list(omitted),
            "clauses": len(clauses),
            "cnf_sha256": sha256(cnf),
            "drat_sha256": sha256(drat),
            "lrat_sha256": sha256(lrat),
            "drat_bytes": drat.stat().st_size,
            "lrat_bytes": lrat.stat().st_size,
        })
    return results


def put(wanted, row, terms, relation, rhs):
    normalized = (dict(terms), relation, rhs)
    require(row not in wanted or wanted[row] == normalized,
            "conflicting expected parent row")
    wanted[row] = normalized


def five_row(wanted, vertices, red):
    vertices = tuple(sorted(vertices))
    sign = -1 if red else 1
    put(wanted, 2 * subset_rank(vertices) + (2 if red else 1),
        [(edge(a, b), sign) for a, b in combinations(vertices, 2)],
        b">=", -9 if red else 1)


def load_roots(table):
    lines = table.read_text(encoding="ascii").splitlines()
    require(lines[0].split("\t") == [
        "family", "c", "k", "pattern", "E_cells", "C_cells",
        "anomalies", "root_sha256",
    ], "root table header")
    rows = [line.split("\t") for line in lines[1:]]
    require(len(rows) == 389, "root table size")
    selected = tuple(index for index, row in enumerate(rows)
                     if row[1:3] == ["13", "0"])
    require(selected == ALL_C13_K0, "complete c=13,k=0 table slice")
    expected = {
        48: ("E8", "A", "2"),
        128: ("E77", "BB", "8,9"),
        129: ("E77", "BO", "8,14"),
        201: ("C8", "B", "29"),
        202: ("C8", "O", "30"),
        299: ("C77", "BO", "29,30"),
        300: ("C77", "OO", "30,31"),
        375: ("C77partition", "HO", "15,30"),
        376: ("C77partition", "AB", "28,29"),
    }
    for index, signature in expected.items():
        row = rows[index]
        require((row[0], row[3], row[6]) == signature,
                "root signature " + str(index))
        require(row[4:6] == ["0,6,6,1", "13,1,1,13"],
                "cell sizes " + str(index))
    return rows


def expected_parent_rows(rows):
    wanted = {}
    for anchor, partner, cell in ((U, V, A), (V, U, B)):
        neighborhood = tuple(sorted((partner,) + H + cell))
        require(len(neighborhood) == 21, "anchor neighborhood size")
        for four in combinations(neighborhood, 4):
            five_row(wanted, (anchor,) + four, True)
        for five in combinations(neighborhood, 5):
            five_row(wanted, five, False)
    for four in combinations(H, 4):
        five_row(wanted, (Z,) + four, False)
    five_rows = len(wanted)
    require(five_rows == 51810, "physical five-set row count")

    for vertices in combinations(range(N), 3):
        if U not in vertices and V not in vertices:
            continue
        conjunction = triangle(vertices)
        variables = [edge(a, b) for a, b in combinations(vertices, 2)]
        first = 2 * comb(N, 5) + 4 * (conjunction - EDGE_COUNT - 1) + 1
        for offset, variable in enumerate(variables):
            put(wanted, first + offset, [(conjunction, -1), (variable, 1)], b">=", 0)
        put(wanted, first + 3,
            [(conjunction, 1)] + [(variable, -1) for variable in variables],
            b">=", -2)
    for anchor in (U, V):
        triangle_variables = [triangle((anchor, a, b))
                              for a, b in combinations(
                                  [w for w in range(N) if w != anchor], 2)]
        put(wanted, 2 * comb(N, 5) + 4 * comb(N, 3) + N + anchor + 1,
            [(variable, 1) for variable in triangle_variables], b"=", 100)
    put(wanted, BASE_ROWS + 1,
        [(SELECTOR_FIRST + index, 1) for index in range(389)], b"=", 1)

    cells = ((), tuple(range(2, 8)), tuple(range(8, 14)), (Z,), H,
             (X_A,), (X_B,), tuple(range(30, 43)))
    statuses = ((1, 1), (1, 0), (0, 1), (0, 0))
    units = [(U, V, 1)]
    for index, cell in enumerate(cells):
        left, right = statuses[index % 4]
        for vertex in cell:
            units.extend(((U, vertex, left), (V, vertex, right)))
    units.sort()
    require(len(units) == 83, "anchor-unit count")

    for root in ROOTS:
        first = BASE_ROWS + 2 + sum(
            169 + (57 if row[0] == "C77partition" else 0)
            for row in rows[:root]
        )
        selector = SELECTOR_FIRST + root
        anomalies = tuple(map(int, rows[root][6].split(",")))
        require(not set(anomalies) & set(H), "no core anomaly in uniform root")
        for offset, (a, b, value) in enumerate(units):
            put(wanted, first + offset,
                [(edge(a, b), 1 if value else -1), (selector, -1)],
                b">=", 0 if value else -1)
        for h in H:
            variables = [edge(h, e) for e in E]
            put(wanted, first + 83 + 2 * h,
                [(variable, 1) for variable in variables] + [(selector, -6)],
                b">=", 0)
            put(wanted, first + 84 + 2 * h,
                [(variable, -1) for variable in variables] + [(selector, -7)],
                b">=", -13)
    require(len(wanted) == 59409, "complete source-row reconstruction")
    return wanted, five_rows, units


def parse_opb_row(raw):
    fields = raw.split()
    require(len(fields) >= 5 and fields[-1] == b";", "OPB row syntax")
    relation = fields[-3]
    require(relation in (b">=", b"="), "OPB relation")
    terms = {}
    for index in range(0, len(fields) - 3, 2):
        coefficient = int(fields[index])
        token = fields[index + 1]
        require(token.startswith(b"x"), "OPB variable syntax")
        variable = int(token[1:])
        require(variable not in terms, "OPB repeated variable")
        terms[variable] = coefficient
    return terms, relation, int(fields[-2])


def check_parent(opb, wanted):
    digest = hashlib.sha256()
    seen = set()
    size = 0
    count = 0
    with opb.open("rb") as stream:
        header = stream.readline()
        expected_header = b"* #variable= 13633 #constraint= 2044421 #equal= 87 intsize= 64\n"
        require(header == expected_header, "parent OPB header")
        digest.update(header)
        size += len(header)
        for count, raw in enumerate(stream, 1):
            digest.update(raw)
            size += len(raw)
            if count in wanted:
                require(parse_opb_row(raw) == wanted[count],
                        "parent OPB semantic row " + str(count))
                seen.add(count)
    require(count == 2044421 and size == 172788992, "parent OPB row/byte count")
    require(digest.hexdigest() == PARENT_OPB_SHA256, "entire parent OPB identity")
    require(seen == set(wanted), "all reconstructed parent rows found")


def arithmetic(rows, units):
    fixed = {edge(a, b): value for a, b, value in units}
    left = Counter()
    constant = 0
    # Expand t_R(u)+t_R(v), using only the fixed anchor stars.
    for anchor in (U, V):
        outside = [w for w in range(N) if w != anchor]
        for a, b in combinations(outside, 2):
            if fixed[edge(anchor, a)] and fixed[edge(anchor, b)]:
                variable = edge(a, b)
                if variable in fixed:
                    constant += fixed[variable]
                else:
                    left[variable] += 1
    # Substitute the common-core incidence equality e(H,E)=78.
    for h in H:
        for e in E:
            left[edge(h, e)] -= 1
    right = Counter({edge(a, b): 2 for a, b in combinations(H, 2)})
    for cell, distinguished in ((A, X_A), (B, X_B)):
        right.update(edge(a, b) for a, b in combinations(cell, 2))
        right.update(edge(distinguished, h) for h in H)
    for h in H:
        right[edge(Z, h)] -= 1
    normalized_left = {variable: coefficient for variable, coefficient in left.items()
                       if coefficient}
    require(normalized_left == dict(right), "159-coordinate triangle identity")
    require(len(right) == 159 and constant == 26, "identity support/constant")
    identity_rhs = 200 - constant - 78
    require(identity_rhs == 96, "scalar equality RHS")
    require(104 + 52 + 24 + 24 - 5 == 199, "strict triangle upper bound")
    for a, b, c, conjunction in product((0, 1), repeat=4):
        inequalities = (conjunction <= a, conjunction <= b, conjunction <= c,
                        conjunction >= a + b + c - 2)
        require(all(inequalities) == (conjunction == a * b * c),
                "Boolean triangle conjunction semantics")

    residual = Counter(row[0] for index, row in enumerate(rows)
                       if index not in set(ALL_C13_K0))
    family_order = ("E8", "E77", "C8", "C77", "C77partition")
    counts = [residual[family] for family in family_order]
    require(counts == [59, 83, 68, 102, 68] and sum(counts) == 380,
            "residual descriptor census")
    return {
        "identity_coordinates": len(right),
        "identity_constant": constant,
        "common_core_incidence": 78,
        "identity_rhs": identity_rhs,
        "anchor_triangle_upper_bound": 199,
        "required_anchor_triangle_sum": 200,
        "current_excluded_roots": list(ROOTS),
        "cumulative_excluded_roots": list(ALL_C13_K0),
        "residual_counts": counts,
        "residual_descriptors": 380,
    }


def exact_certificate(package):
    path = package / "certificate.json"
    require(sha256(path) == CERTIFICATE_SHA256, "Farkas certificate identity")
    data = json.loads(path.read_text(encoding="ascii"))
    require(data["variables"] == [
        "weighted_A", "weighted_B", "twice_eH", "footprint_z"
    ], "Farkas coordinates")
    bounds = data["inequalities"]
    equality = data["equality"]
    multipliers = data["inequality_multipliers"]
    equality_multiplier = data["equality_multiplier"]
    coefficients = [
        sum(multipliers[row] * bounds[row]["coefficients"][column]
            for row in range(len(bounds)))
        + equality_multiplier * equality["coefficients"][column]
        for column in range(4)
    ]
    rhs = (sum(multiplier * bound["rhs"]
               for multiplier, bound in zip(multipliers, bounds))
           + equality_multiplier * equality["rhs"])
    require(coefficients == [0, 0, 0, 0] and rhs == -1,
            "exact Farkas contradiction")
    require(data["result"] == {"coefficients": coefficients, "rhs": rhs},
            "stored Farkas result")
    require(24 + 24 + 52 - 5 == 95, "root-375 zero-gap control")
    return rhs


def separator():
    # These are direct sums of the reviewed P4 point's pinned edge classes.
    # The old point's whole-system feasibility remains an imported dependency.
    a_edges = 5 * Fraction(5, 6) + 10 * Fraction(5, 6) + Fraction(8, 15) + 5 * Fraction(5, 6)
    b_edges = 15 * Fraction(4, 5) + 6 * Fraction(13, 15)
    footprints = (13 * Fraction(3, 5), 13 * Fraction(3, 5))
    require((a_edges, b_edges) == (Fraction(86, 5), Fraction(86, 5)),
            "P4 cell-edge sums")
    require(all(value == Fraction(39, 5) for value in footprints),
            "P4 core footprints")
    totals = (a_edges + footprints[0], b_edges + footprints[1])
    require(totals == (Fraction(25), Fraction(25)), "P4 separator values")
    return {
        "weighted_values": [str(value) for value in totals],
        "upper_bound": "24",
        "slacks": [str(Fraction(24) - value) for value in totals],
        "guarded_cut": "W+10*y<=34",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path, required=True)
    parser.add_argument("--lrat-check", type=Path, required=True)
    args = parser.parse_args()

    package, table, source_result = verify_source(args.source)
    require(sha256(args.drat_trim) == "9c09fe813af0b52f58d923837a1bc3ca5e6017987c1e9530d62fa5b4f018412a",
            "drat-trim binary identity")
    require(sha256(args.lrat_check) == "fb7e9f57ee5849afaa35e9d967e27a72cd76bad7aa72ee0499dc65207c08c4a7",
            "lrat-check binary identity")
    r34_steps = check_r34(package)
    cases, cover = finite_cover(package)
    proof_index = json.loads((package / "PROOF_RUN.json").read_text(encoding="ascii"))["proofs"]
    proofs = verify_cnfs_and_proofs(cases, args.replay, proof_index,
                                    args.drat_trim, args.lrat_check)
    rows = load_roots(table)
    wanted, five_rows, units = expected_parent_rows(rows)
    check_parent(args.replay / "parent.opb", wanted)
    result = {
        "status": "INDEPENDENT_ACCEPTANCE_M214_C13_K0_WEIGHTED_CELL_EXCLUSION",
        "source": source_result,
        "r34_rup_steps": r34_steps,
        "finite_cover": cover,
        "native_proofs": proofs,
        "physical_source_rows": len(wanted),
        "physical_five_set_rows": five_rows,
        "global": arithmetic(rows, units),
        "farkas_rhs": exact_certificate(package),
        "moment_separator": separator(),
        "trust_boundary": [
            "McKay catalog completeness for Ramsey(3,5;13)",
            "upstream complete-root cover and reviewed root-375 exclusion",
            "reviewed feasibility of the old P4 moment point",
            "Python/compiler/native-checker correctness and ordinary hardware",
        ],
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
