#!/usr/bin/env python3
"""Exact proof replay for the Golomb--opposed-B214--native-A159 stop.

The coordinate checker uses integer coefficients at common scale 36 in the
basis 1,sqrt(3),sqrt(11),sqrt(33).  The negative relation certificate is a
RUP-only DRAT trace checked here with a small watched-literal implementation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import combinations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
A_SOURCE = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points159.tsv"
B_SOURCE = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv"
A_SHA256 = "4f72fa06d18434472ce77cebe38880333694ec04b94945ede073a4a1c6d5bc02"
B_SHA256 = "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f"
RADICANDS = (1, 3, 11, 33)
UNIT_SQUARED = (36 * 36, 0, 0, 0)
SEVEN_SQUARED = (7 * 36 * 36, 0, 0, 0)


def need(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = [0] * 4
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            d = math.gcd(RADICANDS[i], RADICANDS[j])
            out[RADICANDS.index(RADICANDS[i] * RADICANDS[j] // (d * d))] += x * y * d
    return tuple(out)


def squared_distance(p, q) -> tuple[int, ...]:
    dx = tuple(a - b for a, b in zip(p[0], q[0]))
    dy = tuple(a - b for a, b in zip(p[1], q[1]))
    xx, yy = multiply(dx, dx), multiply(dy, dy)
    return tuple(a + b for a, b in zip(xx, yy))


def read_parts(path: Path, expected_hash: str):
    need(hashlib.sha256(path.read_bytes()).hexdigest() == expected_hash,
         f"source hash: {path.name}")
    rows = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("#"):
            continue
        z = tuple(map(int, line.split()))
        need(len(z) == 16, "Parts coordinate arity")
        need(all(z[i] == 0 for i in (1, 2, 3, 4, 6, 7, 8, 10, 11, 13, 14, 15)),
             "source left Q(sqrt(3),sqrt(11))")
        # Source scale is 12; multiply coefficients by three for scale 36.
        rows.append(((3 * z[0], 0, 0, 3 * z[5]),
                     (0, 3 * z[9], 3 * z[12], 0)))
    return rows


def golomb():
    # The last row entry is an imaginary sqrt(11) coefficient at scale 12.
    rows = (
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 2), (-3, -3, 3, -1),
        (-3, 3, -3, -1),
    )
    return [((a, 0, 0, b), (0, c, 3 * d, 0)) for a, b, c, d in rows]


def strict_edges(points):
    return [(a, b) for a, b in combinations(range(len(points)), 2)
            if squared_distance(points[a], points[b]) == UNIT_SQUARED]


def shifted_b(points, side: int):
    need(side in (0, 1), "B side")
    out = []
    for x, y in points:
        if side == 0:
            xx = (x[0] - 18, x[1], x[2], x[3])
        else:
            xx = (-x[0] + 18, -x[1], -x[2], -x[3])
        out.append((xx, y))
    return out


def merge(labelled):
    points, index, image = [], {}, []
    for p in labelled:
        if p not in index:
            index[p] = len(points)
            points.append(p)
        image.append(index[p])
    return points, image


def stream_hash(rows) -> str:
    return hashlib.sha256(("\n".join(rows) + "\n").encode()).hexdigest()


def point_hash(points) -> str:
    return stream_hash(" ".join(map(str, x + y)) for x, y in points)


def edge_hash(edges) -> str:
    return stream_hash(f"{a} {b}" for a, b in edges)


def proper(word: str, vertices: int, edges) -> bool:
    return (isinstance(word, str) and len(word) == vertices
            and set(word) <= set("0123")
            and all(word[a] != word[b] for a, b in edges))


def canonical_golomb_patterns(g_edges):
    patterns = []
    for tail in product(range(4), repeat=7):
        word = (0, 1, 2) + tail
        if all(word[a] != word[b] for a, b in g_edges):
            patterns.append("".join(map(str, word)))
    return patterns


def colouring_cnf(vertices: int, edges, excluded_patterns):
    colour_count = 4

    def var(vertex, colour):
        return colour_count * vertex + colour + 1

    clauses = []
    for vertex in range(vertices):
        clauses.append([var(vertex, c) for c in range(colour_count)])
        for a, b in combinations(range(colour_count), 2):
            clauses.append([-var(vertex, a), -var(vertex, b)])
    for a, b in edges:
        for colour in range(colour_count):
            clauses.append([-var(a, colour), -var(b, colour)])
    for vertex, colour in enumerate((0, 1, 2)):
        clauses.append([var(vertex, colour)])
    selectors = [colour_count * vertices + i + 1
                 for i in range(len(excluded_patterns))]
    clauses.append(selectors)
    for selector, pattern in zip(selectors, excluded_patterns):
        for vertex, colour in enumerate(map(int, pattern)):
            clauses.append([-selector, var(vertex, colour)])
    return selectors[-1], clauses


def dimacs_bytes(variables: int, clauses) -> bytes:
    rows = [f"p cnf {variables} {len(clauses)}"]
    rows.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(rows) + "\n").encode()


class RupChecker:
    """RUP replay with persistent two-watched-literal positions.

    Clause deletions are absent from the trimmed certificate.  Retaining
    clauses would also be sound for RUP because unit-propagation conflict is
    monotone when clauses are added.
    """

    def __init__(self, variables: int, clauses):
        self.variables = variables
        self.clauses = []
        self.positions = []
        self.watches = {lit: [] for lit in range(-variables, variables + 1) if lit}
        self.units = []
        for clause in clauses:
            self.add(clause)

    def add(self, clause):
        clause = tuple(clause)
        cid = len(self.clauses)
        self.clauses.append(clause)
        if not clause:
            self.positions.append([0, 0])
            return
        second = 0 if len(clause) == 1 else 1
        self.positions.append([0, second])
        self.watches[clause[0]].append(cid)
        if second:
            self.watches[clause[second]].append(cid)
        else:
            self.units.append(clause[0])

    def is_rup(self, clause) -> bool:
        values = [0] * (self.variables + 1)
        queue = []

        def assign(lit):
            variable = abs(lit)
            value = 1 if lit > 0 else -1
            if values[variable]:
                return values[variable] == value
            values[variable] = value
            queue.append(lit)
            return True

        conflict = False
        for lit in self.units:
            if not assign(lit):
                conflict = True
                break
        if not conflict:
            for lit in clause:
                if not assign(-lit):
                    conflict = True
                    break

        head = 0
        while not conflict and head < len(queue):
            false_lit = -queue[head]
            head += 1
            watch_list = self.watches[false_lit]
            i = 0
            while i < len(watch_list):
                cid = watch_list[i]
                stored = self.clauses[cid]
                pos = self.positions[cid]
                if len(stored) == 1:
                    conflict = True
                    break
                if stored[pos[0]] == false_lit:
                    which, other = 0, 1
                elif stored[pos[1]] == false_lit:
                    which, other = 1, 0
                else:
                    raise ValueError("corrupt watch list")
                other_lit = stored[pos[other]]
                other_value = values[abs(other_lit)] * (1 if other_lit > 0 else -1)
                if other_value == 1:
                    i += 1
                    continue
                replacement = None
                for candidate, lit in enumerate(stored):
                    if candidate in pos:
                        continue
                    value = values[abs(lit)] * (1 if lit > 0 else -1)
                    if value != -1:
                        replacement = candidate
                        break
                if replacement is not None:
                    new_lit = stored[replacement]
                    pos[which] = replacement
                    watch_list[i] = watch_list[-1]
                    watch_list.pop()
                    self.watches[new_lit].append(cid)
                    continue
                if other_value == -1:
                    conflict = True
                    break
                if not assign(other_lit):
                    conflict = True
                    break
                i += 1
        return conflict


def check_rup(path: Path, variables: int, clauses):
    checker = RupChecker(variables, clauses)
    additions = 0
    last = None
    for line in path.read_text().splitlines():
        need(line and not line.startswith("d "), "proof is not deletion-free RUP")
        row = list(map(int, line.split()))
        need(row and row[-1] == 0, "RUP row terminator")
        clause = row[:-1]
        need(all(0 < abs(lit) <= variables for lit in clause), "RUP variable range")
        need(checker.is_rup(clause), f"non-RUP lemma {additions}")
        checker.add(clause)
        additions += 1
        last = clause
    need(last == [], "RUP trace does not finish with the empty clause")
    return additions


def run(certificate: Path, proof: Path):
    cert = json.loads(certificate.read_text())
    need(cert.get("schema") == "golomb-opposed-b214-native-a159-stop-v1", "schema")
    a_source = read_parts(A_SOURCE, A_SHA256)
    b_source = read_parts(B_SOURCE, B_SHA256)
    need((len(a_source), len(b_source)) == (159, 214), "source orders")
    a_edges, b_edges = strict_edges(a_source), strict_edges(b_source)
    need((len(a_edges), len(b_edges)) == (646, 977), "source edge counts")
    need(squared_distance(b_source[186], b_source[187]) == (9 * 36 * 36, 0, 0, 0),
         "B214 terminal distance")
    need(all(squared_distance(a_source[x], a_source[y]) == SEVEN_SQUARED
             for x, y in combinations((141, 142, 144), 2)), "A159 terminal triangle")

    g = golomb()
    g_edges = strict_edges(g)
    need(len(g) == 10 and len(g_edges) == 18, "Golomb graph")
    need(all(edge in g_edges for edge in ((0, 1), (0, 2), (1, 2))),
         "Golomb normalizing triangle")
    need(not any(all(word[x] != word[y] for x, y in g_edges)
                 for tail in product(range(3), repeat=7)
                 for word in [(0, 1, 2) + tail]), "Golomb should not be three-colourable")
    patterns = canonical_golomb_patterns(g_edges)
    need(len(patterns) == 95 and cert["canonical_golomb_patterns"] == patterns,
         "canonical Golomb census")

    left, right = shifted_b(b_source, 0), shifted_b(b_source, 1)
    need(left[186] == g[1] and left[187][0][0] == -72, "left B terminal frame")
    need(right[186] == g[4] and right[187][0][0] == 72, "right B terminal frame")
    left_map = [left.index(p) for p in g]
    right_map = [right.index(p) for p in g]
    need(left_map == [36, 186, 166, 86, 37, 89, 167, 87, 4, 103], "left Golomb embedding")
    need(right_map == [36, 37, 86, 166, 186, 167, 89, 58, 119, 29], "right Golomb embedding")
    cross_pattern = cert["cross_contact_witness_pattern"]
    need(cross_pattern == "0121212203", "cross-contact witness pattern")
    for word, mapping, name in ((cert["isolated_left_word"], left_map, "left"),
                                (cert["isolated_right_word"], right_map, "right")):
        need(proper(word, 214, b_edges), f"isolated {name} B word")
        need("".join(word[i] for i in mapping) == cross_pattern,
             f"isolated {name} Golomb projection")

    s343, image343 = merge(g + left + right)
    edges343 = strict_edges(s343)
    need((len(s343), len(edges343), 438 - len(s343)) == (343, 1782, 95),
         "S343 size/edge/collision counts")
    inherited343 = set(g_edges)
    inherited343.update(tuple(sorted((image343[10 + a], image343[10 + b])))
                        for a, b in b_edges)
    inherited343.update(tuple(sorted((image343[224 + a], image343[224 + b])))
                        for a, b in b_edges)
    need((len(inherited343), len(set(edges343) - inherited343)) == (1674, 108),
         "S343 inherited/private-contact edge split")
    long_adj = [set() for _ in s343]
    for x, y in combinations(range(len(s343)), 2):
        if squared_distance(s343[x], s343[y]) == SEVEN_SQUARED:
            long_adj[x].add(y)
            long_adj[y].add(x)
    need(sum(map(len, long_adj)) // 2 == 96, "S343 sqrt7-pair count")
    need(not any(any(z > y for z in long_adj[x] & long_adj[y])
                 for x in range(len(s343)) for y in long_adj[x] if x < y),
         "S343 unexpectedly contains a sqrt7 triangle")

    s359, image359 = merge(g + left + right + a_source)
    edges359 = strict_edges(s359)
    need((len(s359), len(edges359), 597 - len(s359)) == (359, 1893, 238),
         "S359 size/edge/collision counts")
    old = set(image359[:438])
    need((len(set(image359[438:]) - old), len(set(image359[438:]) & old)) == (16, 143),
         "native A159 new/overlap split")
    inherited359 = set(g_edges)
    inherited359.update(tuple(sorted((image359[10 + a], image359[10 + b])))
                        for a, b in b_edges)
    inherited359.update(tuple(sorted((image359[224 + a], image359[224 + b])))
                        for a, b in b_edges)
    inherited359.update(tuple(sorted((image359[438 + a], image359[438 + b])))
                        for a, b in a_edges)
    need((len(inherited359), len(set(edges359) - inherited359)) == (1770, 123),
         "S359 inherited/private-contact edge split")
    added_edges = len(set(edges359) - set(edges343))
    added_cross_contacts = len((set(edges359) - inherited359)
                               - (set(edges343) - inherited343))
    need(added_edges == 111, "native A159 added edge count")
    need(added_cross_contacts == 32, "native A159 new cross-contact count")

    need(point_hash(s343) == cert["s343_point_sha256"], "S343 point hash")
    need(edge_hash(edges343) == cert["s343_edge_sha256"], "S343 edge hash")
    need(point_hash(s359) == cert["s359_point_sha256"], "S359 point hash")
    need(edge_hash(edges359) == cert["s359_edge_sha256"], "S359 edge hash")
    surviving = cert["surviving_patterns"]
    excluded = cert["excluded_patterns"]
    need(surviving == sorted(surviving) and len(surviving) == 66, "surviving patterns")
    need(len(excluded) == 29 and [p for p in patterns if p not in surviving] == excluded,
         "excluded pattern complement")
    need(cross_pattern in excluded, "isolated pattern is not excluded jointly")
    for key, points, edges in (("s343_words", s343, edges343),
                               ("s359_words", s359, edges359)):
        rows = cert[key]
        need(sorted(rows) == surviving, f"{key} complete keys")
        for pattern, word in rows.items():
            need(proper(word, len(points), edges), f"improper witness in {key}")
            need(word[:10] == pattern, f"wrong Golomb projection in {key}")

    variables, clauses = colouring_cnf(len(s343), edges343, excluded)
    cnf = dimacs_bytes(variables, clauses)
    need((variables, len(clauses)) == (1401, 9823), "CNF dimensions")
    need(hashlib.sha256(cnf).hexdigest() == cert["excluded_cnf_sha256"], "CNF hash")
    need(hashlib.sha256(proof.read_bytes()).hexdigest()
         == "e3f5c84e89d442d9d5ced2246681defdbccc9fa8cf4eeaebdbd78fec7b966e29",
         "RUP proof hash")
    rup_additions = check_rup(proof, variables, clauses)
    need(rup_additions == 1382, "RUP lemma count")

    return {
        "status": "VERIFIED_OPPOSED_B214_STRICT_GAIN_AND_NATIVE_A159_NEUTRAL_STOP",
        "record_improved": False,
        "coordinate_scale": 36,
        "golomb_vertices": 10,
        "golomb_edges": 18,
        "golomb_chromatic_number": 4,
        "golomb_canonical_four_colour_patterns": 95,
        "isolated_pattern_extends_to_each_B214": cross_pattern,
        "opposed_b214_vertices": 343,
        "opposed_b214_edges": 1782,
        "opposed_b214_label_collisions": 95,
        "opposed_b214_private_contact_edges": 108,
        "opposed_b214_relation_patterns": 66,
        "opposed_b214_excluded_patterns": 29,
        "native_a159_completion_vertices": 359,
        "native_a159_completion_edges": 1893,
        "native_a159_overlaps": 143,
        "native_a159_new_points": 16,
        "native_a159_private_contact_edges": 123,
        "native_a159_added_edges": 111,
        "native_a159_new_cross_contact_edges": added_cross_contacts,
        "native_a159_relation_patterns": 66,
        "chromatic_number_of_both_supports": 4,
        "sqrt7_pairs_in_opposed_support": 96,
        "sqrt7_triangles_in_opposed_support": 0,
        "rup_variables": variables,
        "rup_clauses": len(clauses),
        "rup_lemmas": rup_additions,
        "positive_relation_words_checked": 132,
        "s343_point_sha256": cert["s343_point_sha256"],
        "s343_edge_sha256": cert["s343_edge_sha256"],
        "s359_point_sha256": cert["s359_point_sha256"],
        "s359_edge_sha256": cert["s359_edge_sha256"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=HERE / "certificate.json")
    parser.add_argument("--proof", type=Path, default=HERE / "excluded.rup")
    parser.add_argument("--write-cnf", type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = run(args.certificate, args.proof)
    if args.write_cnf is not None:
        cert = json.loads(args.certificate.read_text())
        b_source = read_parts(B_SOURCE, B_SHA256)
        g = golomb()
        points, _ = merge(g + shifted_b(b_source, 0) + shifted_b(b_source, 1))
        edges = strict_edges(points)
        variables, clauses = colouring_cnf(len(points), edges, cert["excluded_patterns"])
        args.write_cnf.write_bytes(dimacs_bytes(variables, clauses))
    if args.check_expected:
        need(result == json.loads((HERE / "expected.json").read_text()),
             "result differs from expected.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
