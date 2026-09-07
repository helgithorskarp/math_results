#!/usr/bin/env python3
"""Definition-level audit of the row-triple/support-5--8 aggregate CNF.

No submitted module is imported.  GL(4,2) is obtained by filtering all 2^16
binary matrices.  The checker reconstructs the inverse-transpose support
orbits and every CNF clause directly from the mathematical definitions.
"""

from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
from pathlib import Path
import argparse
import json


N = 43
A = 20
B = 23
EXPECTED_CNF_SHA256 = "e12f321f059f59b98e530042c61c965167f5b50c401681ec858b807819b99cc5"
EXPECTED_PROOF_SHA256 = "a3780cdf12fcb0467a88e1fa5277451101c9628967c4bd597e81bd3bc8c24819"
EXPECTED_SECTIONS = {
    "column_span_four": 15,
    "contact_truth_tables": 5520,
    "degree_18_24": 162722,
    "equal_column_pair_distance": 158631,
    "equal_row_pair_distance": 2514,
    "nonzero_multiplicity_cap_five": 270,
    "one_hot_columns": 2783,
    "physical_five_sets": 1817142,
    "sorted_columns": 2640,
    "support_equivalences": 360,
    "support_symmetry": 32212,
    "support_upper_bound": 230,
    "tripled_row_contacts": 2324,
    "zero_forbidden_on_columns": 23,
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def binary_rank(values):
    basis = {}
    for value in values:
        while value:
            bit = value.bit_length() - 1
            if bit in basis:
                value ^= basis[bit]
            else:
                basis[bit] = value
                break
    return len(basis)


def dot(x, y):
    return (x & y).bit_count() & 1


def matrix_group():
    result = []
    for encoded in range(1 << 16):
        columns = tuple((encoded >> (4 * k)) & 15 for k in range(4))
        if binary_rank(columns) != 4:
            continue
        image = []
        for value in range(16):
            moved = 0
            for k, column in enumerate(columns):
                if value >> k & 1:
                    moved ^= column
            image.append(moved)
        result.append(tuple(image))
    require(len(result) == 20160 and len(set(result)) == 20160, "GL(4,2) census")
    return result


def inverse_transpose(image):
    dual = []
    for value in range(16):
        candidates = [
            candidate for candidate in range(16)
            if all(dot(image[1 << k], candidate) == (value >> k & 1) for k in range(4))
        ]
        require(len(candidates) == 1, "dual map existence")
        dual.append(candidates[0])
    require(
        all(dot(image[x], dual[y]) == dot(x, y) for x in range(16) for y in range(16)),
        "dual map dot products",
    )
    return tuple(dual)


def move_mask(mask, image):
    result = 0
    while mask:
        low = mask & -mask
        value = low.bit_length()
        result |= 1 << (image[value] - 1)
        mask ^= low
    return result


def support_audit(target):
    group = matrix_group()
    row_population = Counter([0] + list(range(1, 16)) + [1, 1, 2, 2])
    row_stabilizer = [
        image for image in group
        if Counter(image[value] for value in row_population.elements()) == row_population
    ]
    require(len(row_stabilizer) == 192, "row stabilizer order")
    dual_group = [inverse_transpose(image) for image in row_stabilizer]
    require(len(set(dual_group)) == 192, "dual stabilizer order")

    canonical = []
    for mask in range(1 << 15):
        canonical.append(min(move_mask(mask, image) for image in dual_group))
    groups = defaultdict(set)
    for mask in range(1 << 15):
        labels = [value for value in range(1, 16) if mask >> (value - 1) & 1]
        if len(labels) >= 5 and binary_rank(labels) == 4:
            groups[canonical[mask]].add(mask)
    records = []
    for representative, members in sorted(groups.items()):
        orbit = {move_mask(representative, image) for image in dual_group}
        require(orbit == members, ("incomplete support orbit", representative))
        records.append({
            "labels": [value for value in range(1, 16) if representative >> (value - 1) & 1],
            "mask": representative,
            "orbit_size": len(orbit),
            "support_size": representative.bit_count(),
        })
    published = json.loads((target / "support_orbits.json").read_text())
    require(published["records"] == records, "published support orbit table")
    require(published["column_action"] == "inverse-transpose of row stabilizer", "declared action")
    by_size = Counter(record["support_size"] for record in records)
    sets_by_size = Counter()
    for record in records:
        sets_by_size[record["support_size"]] += record["orbit_size"]
    require(len(records) == 475 and sum(map(len, groups.values())) == 30392, "support census")
    require(sum(by_size[size] for size in range(5, 9)) == 288, "band orbit census")
    require(sum(sets_by_size[size] for size in range(5, 9)) == 20443, "band support census")
    require(sum(mask != representative for mask, representative in enumerate(canonical)) == 32212,
            "support symmetry clause count")
    return group, dual_group, canonical, by_size, sets_by_size


def file_sha256(path):
    digest = sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


class ClauseAudit:
    def __init__(self, path):
        self.handle = path.open("r", encoding="ascii")
        header = self.handle.readline().split()
        require(len(header) == 4 and header[:2] == ["p", "cnf"], "DIMACS header")
        self.declared_variables = int(header[2])
        self.declared_clauses = int(header[3])
        self.variables = 0
        self.clauses = 0
        self.sections = Counter()

    def new_var(self):
        self.variables += 1
        return self.variables

    def add(self, literals, section):
        unique = []
        seen = set()
        for literal in literals:
            require(type(literal) is int and literal, "invalid expected literal")
            if -literal in seen:
                return
            if literal not in seen:
                seen.add(literal)
                unique.append(literal)
        line = self.handle.readline()
        require(line, ("premature DIMACS end", section, self.clauses))
        actual = tuple(map(int, line.split()))
        expected = tuple(unique) + (0,)
        require(actual == expected, ("clause mismatch", section, self.clauses, actual[:20], expected[:20]))
        self.clauses += 1
        self.sections[section] += 1

    def at_most(self, literals, bound, section, gate=None):
        def emit(clause):
            self.add(([-gate] if gate is not None else []) + list(clause), section)

        n = len(literals)
        if bound >= n:
            return
        if bound < 0:
            emit([])
            return
        if bound == 0:
            for literal in literals:
                emit([-literal])
            return
        state = [[self.new_var() for _ in range(bound)] for _ in range(n - 1)]
        emit([-literals[0], state[0][0]])
        for j in range(1, bound):
            emit([-state[0][j]])
        for i in range(1, n - 1):
            emit([-literals[i], state[i][0]])
            emit([-state[i - 1][0], state[i][0]])
            for j in range(1, bound):
                emit([-literals[i], -state[i - 1][j - 1], state[i][j]])
                emit([-state[i - 1][j], state[i][j]])
        for i in range(1, n):
            emit([-literals[i], -state[i - 1][bound - 1]])

    def at_least(self, literals, bound, section, gate=None):
        self.at_most([-literal for literal in literals], len(literals) - bound, section, gate)

    def finish(self):
        require(self.variables == self.declared_variables == 155551, "variable count")
        require(self.clauses == self.declared_clauses == 2187386, "clause count")
        require(self.sections == Counter(EXPECTED_SECTIONS), ("section counts", self.sections))
        require(self.handle.read() == "", "extra DIMACS content")
        self.handle.close()


def exact_formula_audit(cnf, canonical):
    audit = ClauseAudit(cnf)
    rows = [0] + list(range(1, 16)) + [1, 1, 2, 2]
    require(len(rows) == A and binary_rank(rows) == 4, "row factor")

    internal = {}
    for side in (range(A), range(A, N)):
        for edge in combinations(side, 2):
            internal[edge] = audit.new_var()
    require(len(internal) == 443, "internal edge allocation")
    labels = [[audit.new_var() for _ in range(16)] for _ in range(B)]
    contacts = {(u, j): audit.new_var() for u in range(1, 16) for j in range(B)}

    for row in labels:
        audit.add(row, "one_hot_columns")
        for first, second in combinations(row, 2):
            audit.add([-first, -second], "one_hot_columns")
    for j in range(B - 1):
        for larger in range(1, 16):
            for smaller in range(larger):
                audit.add([-labels[j][larger], -labels[j + 1][smaller]], "sorted_columns")
    for j in range(B):
        audit.add([-labels[j][0]], "zero_forbidden_on_columns")
    for value in range(1, 16):
        for j in range(B - 5):
            audit.add([-labels[j][value], -labels[j + 5][value]],
                      "nonzero_multiplicity_cap_five")

    support = [audit.new_var() for _ in range(15)]
    for value in range(1, 16):
        used = support[value - 1]
        for j in range(B):
            audit.add([-labels[j][value], used], "support_equivalences")
        audit.add([-used] + [labels[j][value] for j in range(B)], "support_equivalences")
    audit.at_most(support, 8, "support_upper_bound")
    for mask, representative in enumerate(canonical):
        if mask != representative:
            audit.add([
                -support[index] if mask >> index & 1 else support[index]
                for index in range(15)
            ], "support_symmetry")

    for normal in range(1, 16):
        audit.add([
            labels[j][value]
            for j in range(B)
            for value in range(16)
            if dot(normal, value)
        ], "column_span_four")
    for u in range(1, 16):
        for j in range(B):
            contact = contacts[u, j]
            for value in range(16):
                audit.add([-labels[j][value], contact if dot(u, value) else -contact],
                          "contact_truth_tables")

    for value in (1, 2):
        incident = [contacts[value, j] for j in range(B)]
        audit.at_least(incident, 10, "tripled_row_contacts")
        audit.at_most(incident, 13, "tripled_row_contacts")

    for value in range(1, 16):
        vertices = [index for index, label in enumerate(rows) if label == value]
        for first, second in combinations(vertices, 2):
            differences = []
            for other in range(A):
                if other in (first, second):
                    continue
                edge_a = internal[tuple(sorted((first, other)))]
                edge_b = internal[tuple(sorted((second, other)))]
                difference = audit.new_var()
                differences.append(difference)
                for clause in (
                    [edge_a, edge_b, -difference],
                    [edge_a, -edge_b, difference],
                    [-edge_a, edge_b, difference],
                    [-edge_a, -edge_b, -difference],
                ):
                    audit.add(clause, "equal_row_pair_distance")
            audit.at_least(differences, 8, "equal_row_pair_distance")

    for first, second in combinations(range(B), 2):
        equal = audit.new_var()
        for value in range(16):
            audit.add([-labels[first][value], -labels[second][value], equal],
                      "equal_column_pair_distance")
        differences = []
        for other in range(B):
            if other in (first, second):
                continue
            edge_a = internal[tuple(sorted((A + first, A + other)))]
            edge_b = internal[tuple(sorted((A + second, A + other)))]
            difference = audit.new_var()
            differences.append(difference)
            for clause in (
                [edge_a, edge_b, -difference],
                [edge_a, -edge_b, difference],
                [-edge_a, edge_b, difference],
                [-edge_a, -edge_b, -difference],
            ):
                audit.add(clause, "equal_column_pair_distance")
        audit.at_least(differences, 8, "equal_column_pair_distance", equal)

    def edge_variable(first, second):
        if first > second:
            first, second = second, first
        if second < A or first >= A:
            return internal[first, second]
        row_label = rows[first]
        return None if row_label == 0 else contacts[row_label, second - A]

    for vertex in range(N):
        incident = [
            edge_variable(vertex, other)
            for other in range(N)
            if other != vertex and edge_variable(vertex, other) is not None
        ]
        audit.at_least(incident, 18, "degree_18_24")
        audit.at_most(incident, 24, "degree_18_24")

    for vertices in combinations(range(N), 5):
        edges = [edge_variable(*edge) for edge in combinations(vertices, 2)]
        if None not in edges:
            audit.add([-edge for edge in edges], "physical_five_sets")
        audit.add([edge for edge in edges if edge is not None], "physical_five_sets")
    audit.finish()
    return dict(audit.sections)


def bounded_compositions(parts, total=23, cap=5):
    counts = [0] * (total + 1)
    counts[0] = 1
    for _ in range(parts):
        updated = [0] * (total + 1)
        for subtotal, count in enumerate(counts):
            for value in range(1, cap + 1):
                if subtotal + value <= total:
                    updated[subtotal + value] += count
        counts = updated
    return counts[total]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", type=Path)
    parser.add_argument("cnf", type=Path)
    parser.add_argument("proof", type=Path)
    parser.add_argument("proof_result", type=Path)
    args = parser.parse_args()
    require(file_sha256(args.cnf) == EXPECTED_CNF_SHA256, "CNF SHA-256")
    require(args.cnf.stat().st_size == 93795698, "CNF byte count")
    require(file_sha256(args.proof) == EXPECTED_PROOF_SHA256, "proof SHA-256")
    require(args.proof.stat().st_size == 125479174, "proof byte count")
    proof_result = json.loads(args.proof_result.read_text())
    require(proof_result["status"] == "UNSAT_PROOF_VERIFIED", "fresh proof status")
    require(proof_result["cnf_sha256"] == EXPECTED_CNF_SHA256, "proof/CNF identity")
    require(proof_result["proof_sha256"] == EXPECTED_PROOF_SHA256, "proof identity")

    group, dual_group, canonical, by_size, sets_by_size = support_audit(args.target)
    sections = exact_formula_audit(args.cnf, canonical)
    compositions = {size: bounded_compositions(size) for size in range(5, 9)}
    factor_pairs = 105 * sum(sets_by_size[size] * compositions[size] for size in range(5, 9))
    require(compositions == {5: 15, 6: 666, 7: 7140, 8: 37080}, "composition counts")
    require(factor_pairs == 30213993600, "factor-multiset count")
    print(json.dumps({
        "band_support_orbits": sum(by_size[size] for size in range(5, 9)),
        "band_support_sets": sum(sets_by_size[size] for size in range(5, 9)),
        "clauses_checked_entrywise": sum(sections.values()),
        "cnf_sha256": EXPECTED_CNF_SHA256,
        "factor_multiset_pairs": factor_pairs,
        "gl4_size": len(group),
        "proof_sha256": EXPECTED_PROOF_SHA256,
        "row_stabilizer_size": len(dual_group),
        "section_counts": sections,
        "status": "VERIFIED_INDEPENDENT_ROW_TRIPLE_SUPPORT_BAND_REVIEW",
    }, sort_keys=True))


if __name__ == "__main__":
    main()
