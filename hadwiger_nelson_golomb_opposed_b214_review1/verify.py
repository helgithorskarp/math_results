#!/usr/bin/env python3
"""Independent exact review of the opposed-B214/A159 construction.

Geometry is reconstructed in the full eight-term multiquadratic basis.  The
negative colour certificate is replayed with occurrence-count propagation,
not the target's four-term formulas or watched-literal implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import deque
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_golomb_opposed_b214_stop"
A_SOURCE = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points159.tsv"
B_SOURCE = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv"

PINNED = {
    TARGET / "certificate.json": "3f6a4a13ead37de71ceb3cd1818d21a9036ea0273e151461fc54d9df1a8c2e19",
    TARGET / "excluded.rup": "e3f5c84e89d442d9d5ced2246681defdbccc9fa8cf4eeaebdbd78fec7b966e29",
    A_SOURCE: "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02",
    B_SOURCE: "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
}

PRIMES = (3, 5, 11)
BASIS_SIZE = 8
SCALE = 36
UNIT_SQUARED = (SCALE * SCALE,) + (0,) * 7
SEVEN_SQUARED = (7 * SCALE * SCALE,) + (0,) * 7


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stream_hash(rows) -> str:
    return sha256_bytes(("\n".join(rows) + "\n").encode())


def basis_product(i: int, j: int) -> tuple[int, int]:
    """Return coefficient and basis mask for sqrt(r_i)*sqrt(r_j)."""
    common = i & j
    coefficient = 1
    for bit, prime in enumerate(PRIMES):
        if common & (1 << bit):
            coefficient *= prime
    return coefficient, i ^ j


PRODUCT_TABLE = tuple(
    tuple(basis_product(i, j) for j in range(BASIS_SIZE))
    for i in range(BASIS_SIZE)
)


def multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * BASIS_SIZE
    for i, x in enumerate(a):
        if not x:
            continue
        for j, y in enumerate(b):
            if y:
                coefficient, mask = PRODUCT_TABLE[i][j]
                out[mask] += coefficient * x * y
    return tuple(out)


def squared_distance(p, q) -> tuple[int, ...]:
    dx = tuple(x - y for x, y in zip(p[0], q[0]))
    dy = tuple(x - y for x, y in zip(p[1], q[1]))
    xx = multiply(dx, dx)
    yy = multiply(dy, dy)
    return tuple(x + y for x, y in zip(xx, yy))


def read_parts(path: Path):
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        need(len(row) == 16, f"coordinate arity in {path.name}")
        rows.append((tuple(3 * x for x in row[:8]),
                     tuple(3 * x for x in row[8:])))
    return rows


def golomb():
    rows = (
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 2), (-3, -3, 3, -1),
        (-3, 3, -3, -1),
    )
    points = []
    for rational_x, sqrt33_x, sqrt3_y, sqrt11_y_at_scale12 in rows:
        x = [0] * 8
        y = [0] * 8
        x[0], x[5] = rational_x, sqrt33_x
        y[1], y[4] = sqrt3_y, 3 * sqrt11_y_at_scale12
        points.append((tuple(x), tuple(y)))
    return points


def shifted_b(points, reflected: bool):
    out = []
    for x, y in points:
        xx = tuple(-v for v in x) if reflected else x
        xx = (xx[0] + (18 if reflected else -18),) + xx[1:]
        out.append((xx, y))
    return out


def merge(labelled):
    points = []
    index = {}
    image = []
    for point in labelled:
        if point not in index:
            index[point] = len(points)
            points.append(point)
        image.append(index[point])
    return points, image


def exact_edges(points, squared=UNIT_SQUARED):
    return [
        (a, b)
        for a, b in combinations(range(len(points)), 2)
        if squared_distance(points[a], points[b]) == squared
    ]


def target_point_hash(points):
    # The target writes the subbasis (1,sqrt(3),sqrt(11),sqrt(33)).
    order = (0, 1, 4, 5)
    need(all(all(c == 0 for i, c in enumerate(axis) if i not in order)
             for point in points for axis in point), "point left target subfield")
    return stream_hash(
        " ".join(map(str,
                     tuple(point[0][i] for i in order)
                     + tuple(point[1][i] for i in order)))
        for point in points
    )


def edge_hash(edges):
    return stream_hash(f"{a} {b}" for a, b in edges)


def proper(word: str, vertices: int, edges) -> bool:
    return (isinstance(word, str) and len(word) == vertices
            and set(word) <= set("0123")
            and all(word[a] != word[b] for a, b in edges))


def canonical_golomb_patterns(edges):
    out = []
    for tail in product(range(4), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[a] != word[b] for a, b in edges):
            out.append("".join(map(str, word)))
    return out


def build_cnf(vertices: int, edges, excluded_patterns):
    def var(vertex, colour):
        return 4 * vertex + colour + 1

    clauses = []
    for vertex in range(vertices):
        clauses.append(tuple(var(vertex, colour) for colour in range(4)))
        clauses.extend((-var(vertex, a), -var(vertex, b))
                       for a, b in combinations(range(4), 2))
    clauses.extend((-var(a, colour), -var(b, colour))
                   for a, b in edges for colour in range(4))
    clauses.extend(((var(vertex, colour),)
                    for vertex, colour in enumerate((0, 1, 2))))
    selectors = tuple(4 * vertices + i + 1
                      for i in range(len(excluded_patterns)))
    clauses.append(selectors)
    for selector, pattern in zip(selectors, excluded_patterns):
        clauses.extend((-selector, var(vertex, int(colour)))
                       for vertex, colour in enumerate(pattern))
    return selectors[-1], clauses


def dimacs_bytes(variables: int, clauses) -> bytes:
    rows = [f"p cnf {variables} {len(clauses)}"]
    rows.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(rows) + "\n").encode()


class OccurrenceRup:
    """RUP checker using literal occurrences and remaining-literal counts."""

    def __init__(self, variables: int, clauses):
        self.variables = variables
        self.clauses = []
        self.occurrences = {lit: [] for lit in range(-variables, variables + 1)
                            if lit}
        self.units = []
        for clause in clauses:
            self.add(clause)

    def add(self, clause):
        clause = tuple(clause)
        need(len(clause) == len(set(clause)), "duplicate literal")
        need(not any(-lit in clause for lit in clause), "tautological clause")
        need(all(0 < abs(lit) <= self.variables for lit in clause),
             "literal outside variable range")
        cid = len(self.clauses)
        self.clauses.append(clause)
        for lit in clause:
            self.occurrences[lit].append(cid)
        if len(clause) == 1:
            self.units.append(clause[0])

    def is_rup(self, candidate) -> bool:
        values = [0] * (self.variables + 1)
        remaining = [len(clause) for clause in self.clauses]
        satisfied = bytearray(len(self.clauses))
        queue = deque()

        def assign(lit):
            variable = abs(lit)
            value = 1 if lit > 0 else -1
            if values[variable]:
                return values[variable] == value
            values[variable] = value
            queue.append(lit)
            return True

        for lit in self.units:
            if not assign(lit):
                return True
        for lit in candidate:
            if not assign(-lit):
                return True

        while queue:
            true_lit = queue.popleft()
            for cid in self.occurrences[true_lit]:
                satisfied[cid] = 1
            for cid in self.occurrences[-true_lit]:
                if satisfied[cid]:
                    continue
                remaining[cid] -= 1
                if remaining[cid] > 1:
                    continue
                unassigned = 0
                forced = 0
                clause_satisfied = False
                for lit in self.clauses[cid]:
                    value = values[abs(lit)]
                    signed = value if lit > 0 else -value
                    if signed == 1:
                        clause_satisfied = True
                        break
                    if not value:
                        unassigned += 1
                        forced = lit
                if clause_satisfied:
                    satisfied[cid] = 1
                elif not unassigned:
                    return True
                elif unassigned == 1 and not assign(forced):
                    return True
        return False


def parse_rup(path: Path, variables: int):
    rows = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        need(line and not line.startswith("d "), f"deletion at line {line_number}")
        row = tuple(map(int, line.split()))
        need(row and row[-1] == 0, f"terminator at line {line_number}")
        clause = row[:-1]
        need(all(0 < abs(lit) <= variables for lit in clause),
             f"variable range at line {line_number}")
        rows.append(clause)
    return rows


def replay_rup(variables: int, clauses, proof_rows):
    checker = OccurrenceRup(variables, clauses)
    for index, clause in enumerate(proof_rows):
        need(checker.is_rup(clause), f"non-RUP lemma {index}")
        checker.add(clause)
    need(proof_rows and proof_rows[-1] == (), "proof does not end empty")


def colour_graph(vertices: int, edges, fixed, colour_order=(3, 2, 1, 0)):
    adjacency = [set() for _ in range(vertices)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colours = [-1] * vertices
    for vertex, colour in fixed.items():
        need(0 <= vertex < vertices and 0 <= colour < 4, "bad fixed colour")
        if colours[vertex] not in (-1, colour):
            return None
        colours[vertex] = colour
    if any(colours[a] == colours[b] != -1 for a, b in edges):
        return None

    def search():
        best = None
        best_domain = None
        best_key = None
        for vertex in range(vertices):
            if colours[vertex] != -1:
                continue
            forbidden = {colours[w] for w in adjacency[vertex] if colours[w] != -1}
            domain = tuple(c for c in colour_order if c not in forbidden)
            if not domain:
                return False
            saturation = len(forbidden)
            key = (-len(domain), saturation, len(adjacency[vertex]), -vertex)
            if best_key is None or key > best_key:
                best, best_domain, best_key = vertex, domain, key
        if best is None:
            return True
        for colour in best_domain:
            colours[best] = colour
            if search():
                return True
        colours[best] = -1
        return False

    if search():
        return "".join(map(str, colours))
    return None


def inherited_edges(image, offset, source_edges):
    return {
        tuple(sorted((image[offset + a], image[offset + b])))
        for a, b in source_edges
    }


def cut_structure(vertices: int, edges):
    adjacency = [set() for _ in range(vertices)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    discovery = [-1] * vertices
    low = [0] * vertices
    parent = [-1] * vertices
    articulations = set()
    bridges = []
    clock = 0

    def visit(vertex):
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for neighbour in sorted(adjacency[vertex]):
            if discovery[neighbour] == -1:
                parent[neighbour] = vertex
                children += 1
                visit(neighbour)
                low[vertex] = min(low[vertex], low[neighbour])
                if parent[vertex] == -1 and children > 1:
                    articulations.add(vertex)
                if parent[vertex] != -1 and low[neighbour] >= discovery[vertex]:
                    articulations.add(vertex)
                if low[neighbour] > discovery[vertex]:
                    bridges.append((vertex, neighbour))
            elif neighbour != parent[vertex]:
                low[vertex] = min(low[vertex], discovery[neighbour])

    components = 0
    for vertex in range(vertices):
        if discovery[vertex] == -1:
            components += 1
            visit(vertex)
    return {
        "articulation_vertices": sorted(articulations),
        "bridges": sorted(tuple(sorted(edge)) for edge in bridges),
        "components": components,
        "minimum_degree": min(map(len, adjacency), default=0),
    }


def run():
    for path, digest in PINNED.items():
        need(sha256_bytes(path.read_bytes()) == digest, f"input hash: {path.name}")
    cert = json.loads((TARGET / "certificate.json").read_text())
    need(cert.get("schema") == "golomb-opposed-b214-native-a159-stop-v1",
         "target certificate schema")

    a_source = read_parts(A_SOURCE)
    b_source = read_parts(B_SOURCE)
    need((len(a_source), len(b_source)) == (159, 214), "source orders")
    a_edges = exact_edges(a_source)
    b_edges = exact_edges(b_source)
    need((len(a_edges), len(b_edges)) == (646, 977), "source edge counts")
    need(squared_distance(b_source[186], b_source[187])
         == (9 * SCALE * SCALE,) + (0,) * 7, "B214 terminal distance")
    need(all(squared_distance(a_source[x], a_source[y]) == SEVEN_SQUARED
             for x, y in combinations((141, 142, 144), 2)),
         "A159 terminal triangle")

    g = golomb()
    g_edges = exact_edges(g)
    need((len(g), len(g_edges)) == (10, 18), "Golomb geometry")
    patterns = canonical_golomb_patterns(g_edges)
    need(len(patterns) == 95 and patterns == cert["canonical_golomb_patterns"],
         "Golomb four-colour census")
    need(not any(all(word[a] != word[b] for a, b in g_edges)
                 for tail in product(range(3), repeat=7)
                 for word in [(0, 1, 2) + tail]), "Golomb is three-colourable")

    left = shifted_b(b_source, False)
    right = shifted_b(b_source, True)
    left_index = {point: i for i, point in enumerate(left)}
    right_index = {point: i for i, point in enumerate(right)}
    need(len(left_index) == len(left) and len(right_index) == len(right),
         "B214 collision")
    need(all(point in left_index and point in right_index for point in g),
         "Golomb is not contained in each B214 copy")
    left_map = [left_index[point] for point in g]
    right_map = [right_index[point] for point in g]

    cross_pattern = cert["cross_contact_witness_pattern"]
    for word, mapping in ((cert["isolated_left_word"], left_map),
                          (cert["isolated_right_word"], right_map)):
        need(proper(word, 214, b_edges), "improper isolated-copy witness")
        need("".join(word[i] for i in mapping) == cross_pattern,
             "wrong isolated-copy projection")

    s343, image343 = merge(g + left + right)
    edges343 = exact_edges(s343)
    inherited343 = set(g_edges)
    inherited343 |= inherited_edges(image343, 10, b_edges)
    inherited343 |= inherited_edges(image343, 224, b_edges)
    contacts343 = set(edges343) - inherited343
    need((len(s343), len(edges343), 438 - len(s343)) == (343, 1782, 95),
         "S343 size/edge/collision count")
    need((len(inherited343), len(contacts343)) == (1674, 108),
         "S343 inherited/contact split")
    cuts343 = cut_structure(len(s343), edges343)
    need(cuts343 == {"articulation_vertices": [], "bridges": [],
                     "components": 1, "minimum_degree": 5},
         "S343 cut structure")

    s359, image359 = merge(g + left + right + a_source)
    edges359 = exact_edges(s359)
    need(image359[:438] == image343, "S343 indices changed in S359")
    inherited359 = set(g_edges)
    inherited359 |= inherited_edges(image359, 10, b_edges)
    inherited359 |= inherited_edges(image359, 224, b_edges)
    inherited359 |= inherited_edges(image359, 438, a_edges)
    contacts359 = set(edges359) - inherited359
    old = set(image359[:438])
    a_image = set(image359[438:])
    need((len(s359), len(edges359), len(a_image - old), len(a_image & old))
         == (359, 1893, 16, 143), "S359 size/edge/overlap count")
    need((len(inherited359), len(contacts359)) == (1770, 123),
         "S359 inherited/contact split")
    need((len(set(edges359) - set(edges343)),
          len(contacts359 - contacts343)) == (111, 32),
         "A159 added-edge/contact count")
    cuts359 = cut_structure(len(s359), edges359)
    need(cuts359 == {"articulation_vertices": [], "bridges": [],
                     "components": 1, "minimum_degree": 5},
         "S359 cut structure")

    need(target_point_hash(s343) == cert["s343_point_sha256"],
         "S343 point stream")
    need(edge_hash(edges343) == cert["s343_edge_sha256"], "S343 edge stream")
    need(target_point_hash(s359) == cert["s359_point_sha256"],
         "S359 point stream")
    need(edge_hash(edges359) == cert["s359_edge_sha256"], "S359 edge stream")

    sqrt7_edges = exact_edges(s343, SEVEN_SQUARED)
    long_adjacency = [set() for _ in s343]
    for a, b in sqrt7_edges:
        long_adjacency[a].add(b)
        long_adjacency[b].add(a)
    sqrt7_triangles = sum(
        1 for a, b in sqrt7_edges for c in long_adjacency[a] & long_adjacency[b]
        if b < c
    )
    need((len(sqrt7_edges), sqrt7_triangles) == (96, 0), "sqrt7 census")

    surviving = cert["surviving_patterns"]
    excluded = cert["excluded_patterns"]
    need(surviving == sorted(surviving) and len(surviving) == 66,
         "surviving relation")
    need(excluded == [pattern for pattern in patterns if pattern not in surviving]
         and len(excluded) == 29, "excluded relation complement")
    need(cross_pattern in excluded, "cross pattern not jointly excluded")
    for key, vertices, edges in (("s343_words", 343, edges343),
                                 ("s359_words", 359, edges359)):
        words = cert[key]
        need(sorted(words) == surviving, f"{key} pattern set")
        need(all(word[:10] == pattern and proper(word, vertices, edges)
                 for pattern, word in words.items()), f"{key} witness")

    variables, clauses = build_cnf(343, edges343, excluded)
    need((variables, len(clauses)) == (1401, 9823), "CNF dimensions")
    need(sha256_bytes(dimacs_bytes(variables, clauses))
         == cert["excluded_cnf_sha256"], "CNF stream")
    proof_rows = parse_rup(TARGET / "excluded.rup", variables)
    need(len(proof_rows) == 1382, "RUP row count")
    replay_rup(variables, clauses, proof_rows)

    # Fresh positive witnesses use a different branch order from the producer.
    fresh_pattern = surviving[0]
    fixed = {i: int(colour) for i, colour in enumerate(fresh_pattern)}
    fresh343 = colour_graph(343, edges343, fixed)
    fresh359 = colour_graph(359, edges359, fixed)
    need(fresh343 is not None and proper(fresh343, 343, edges343),
         "fresh S343 witness")
    need(fresh359 is not None and proper(fresh359, 359, edges359),
         "fresh S359 witness")

    isolated_witness_rows = [
        f"{cross_pattern} {cert['isolated_left_word']} {cert['isolated_right_word']}"
    ]

    return {
        "a159_source_edges": len(a_edges),
        "a159_source_points": len(a_source),
        "all_target_positive_words_checked": 132,
        "b214_source_edges": len(b_edges),
        "b214_source_points": len(b_source),
        "chromatic_number_of_both_supports": 4,
        "excluded_patterns": len(excluded),
        "fresh_s343_difference_from_target": sum(
            a != b for a, b in zip(fresh343, cert["s343_words"][fresh_pattern])),
        "fresh_s343_word": fresh343,
        "fresh_s359_difference_from_target": sum(
            a != b for a, b in zip(fresh359, cert["s359_words"][fresh_pattern])),
        "fresh_s359_word": fresh359,
        "fresh_witness_pattern": fresh_pattern,
        "golomb_patterns": len(patterns),
        "interaction_only_excluded_patterns_proved_at_least": 1,
        "interaction_only_witness_pattern": cross_pattern,
        "isolated_witness_stream_sha256": stream_hash(isolated_witness_rows),
        "native_a159_completion_edges": len(edges359),
        "native_a159_completion_points": len(s359),
        "native_a159_relation_patterns": len(surviving),
        "opposed_b214_edges": len(edges343),
        "opposed_b214_points": len(s343),
        "opposed_b214_relation_patterns": len(surviving),
        "rup_clauses": len(clauses),
        "rup_lemmas": len(proof_rows),
        "rup_variables": variables,
        "s343_edge_sha256": edge_hash(edges343),
        "s343_point_sha256": target_point_hash(s343),
        "s343_cut_structure": cuts343,
        "s359_edge_sha256": edge_hash(edges359),
        "s359_point_sha256": target_point_hash(s359),
        "s359_cut_structure": cuts359,
        "sqrt7_pairs_triangles": [len(sqrt7_edges), sqrt7_triangles],
        "verdict": "ACCEPT_WITH_STRICT_FIXED_COMPOSITION_AND_NEUTRAL_COMPLETION_LIMITATION",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run()
    if args.check_expected:
        need(result == json.loads((HERE / "EXPECTED.json").read_text()),
             "result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
