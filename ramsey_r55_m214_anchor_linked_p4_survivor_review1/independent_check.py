#!/usr/bin/env python3
"""Independent exact audit of the anchor-linked M214/P4 survivor.

This checker imports no contribution module.  It expands the orbit-compressed
certificate, reconstructs every inherited physical coordinate, evaluates the
complete retained OPB, checks every semantic suffix and P4 marginal, and
independently derives the anchor-link and forbidden-state claims.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import combinations, combinations_with_replacement, permutations
import json
from math import comb
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

N = 43
EXCEPTIONAL = frozenset(range(2, 15))
REMOVED = (48, 128, 129, 201, 202, 299, 300, 375, 376)
TARGET_COMMIT = "11a6ff8ea2421de256a87aca794477f91defbba1"
TARGET_MANIFEST_SHA256 = "8b701fe57bb3896b8779d266187289d1a39b000f2126abc2bc14f68c297c38a6"
ROOT_TABLE_SHA256 = "f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e"
CERTIFICATE_SHA256 = "576f7675a093293dcfb8f03f4bf11540ecfacb485b21d608844d29183e734715"
BASE_SHA256 = "9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609"
LINK_SHA256 = "f2bef9213e141982f863601df3dc57d07ee20b1d5f0b9bcb559799a2187bafa1"
FORBIDDEN_SHA256 = "5c1a658ea797e95ab7cb9076373bd6f055220a923c445c00ac38854210f44318"
BASE_HEADER = b"* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64\n"
PAIRS4 = tuple(combinations(range(4), 2))


class Failure(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise Failure(message)


def file_hash(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_source(source):
    package = source / "ramsey_r55_m214_anchor_linked_p4_survivor"
    manifest = package / "SHA256SUMS"
    require(file_hash(manifest) == TARGET_MANIFEST_SHA256, "target manifest identity")
    entries = {}
    for line in manifest.read_text(encoding="ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        require(name not in entries, "duplicate manifest entry")
        entries[name] = digest
        require(file_hash(package / name) == digest, "target source identity: " + name)
    require(len(entries) == 9, "target manifest entry count")
    commit = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    require(commit == TARGET_COMMIT, "target source commit")
    root_table = source / "ramsey_r55_m214_pair_normalization" / "roots.tsv"
    require(file_hash(root_table) == ROOT_TABLE_SHA256, "root-table identity")
    return package, root_table, {
        "commit": commit,
        "manifest_entries": len(entries),
        "manifest_sha256": TARGET_MANIFEST_SHA256,
    }


def edge_index(a, b):
    a, b = sorted((a, b))
    require(0 <= a < b < N, "edge domain")
    return a * (2 * N - a - 1) // 2 + b - a


def subset_rank(vertices, n):
    require(tuple(sorted(set(vertices))) == vertices, "ranked subset order")
    rank = 0
    previous = -1
    size = len(vertices)
    for position, vertex in enumerate(vertices):
        require(0 <= vertex < n, "ranked subset domain")
        rank += sum(
            comb(n - candidate - 1, size - position - 1)
            for candidate in range(previous + 1, vertex)
        )
        previous = vertex
    return rank


def enumerate_roots(root_table):
    families = (
        ("E8", ("H", "A")),
        ("E77", ("BB", "BO", "OO")),
        ("C8", ("B", "O")),
        ("C77", ("BB", "BO", "OO")),
        ("C77partition", ("HO", "AB")),
    )
    roots = []
    table_keys = []
    for family_number, (family_name, patterns) in enumerate(families):
        for c in range(9, 14):
            for k in range(7):
                sizes = (k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k)
                cells = []
                cursor = 2
                for size in sizes:
                    cells.append(tuple(range(cursor, cursor + size)))
                    cursor += size
                require(cursor == N, "root cell partition")
                for pattern in patterns:
                    offset = 0 if family_number < 2 else 4
                    if any(pattern.count(label) > sizes[offset + j]
                           for j, label in enumerate("HABO")):
                        continue
                    core = tuple(sorted(cells[0] + cells[4]))
                    outside = tuple(v for v in range(2, N) if v not in core)
                    units = {(0, 1): 1}
                    states = ((1, 1), (1, 0), (0, 1), (0, 0))
                    for cell_number, cell in enumerate(cells):
                        for vertex in cell:
                            units[(0, vertex)] = states[cell_number % 4][0]
                            units[(1, vertex)] = states[cell_number % 4][1]
                    require(len(units) == 83, "complete two-anchor root star")
                    roots.append({
                        "key": (family_number, c, k, pattern),
                        "core": core,
                        "outside": outside,
                        "units": units,
                    })
                    table_keys.append((family_name, str(c), str(k), pattern))
    require(len(roots) == 389, "root count")
    removed = tuple(i for i, root in enumerate(roots)
                    if root["key"][1:3] == (13, 0))
    require(removed == REMOVED, "nine excluded root indices")
    require(roots[278]["key"] == (3, 12, 0, "BB"), "selected root identity")

    lines = root_table.read_text(encoding="ascii").splitlines()
    require(lines[0].split("\t")[:4] == ["family", "c", "k", "pattern"],
            "root-table header")
    rows = [line.split("\t") for line in lines[1:]]
    require(len(rows) == 389, "root-table row count")
    require(all(tuple(row[:4]) == key for row, key in zip(rows, table_keys)),
            "independent root ordering")
    return roots


def transported_state(state, permutation):
    """Relabel a six-edge state by a position permutation."""
    result = 0
    for new_bit, (a, b) in enumerate(PAIRS4):
        old_pair = tuple(sorted((permutation[a], permutation[b])))
        old_bit = PAIRS4.index(old_pair)
        result |= ((state >> old_bit) & 1) << new_bit
    return result


def load_certificate(path):
    require(file_hash(path) == CERTIFICATE_SHA256, "certificate identity")
    raw = json.loads(path.read_text(encoding="ascii"))
    require(set(raw) == {"format", "denominator", "cells",
                         "active_selectors", "four_tables"},
            "certificate schema")
    require(raw["format"] == "class-state-orbits-v1", "certificate format")
    denominator = raw["denominator"]
    require(type(denominator) is int and denominator > 0, "certificate denominator")
    cells = raw["cells"]
    require(cells and all(isinstance(cell, list) and cell for cell in cells),
            "certificate cells")
    require(sum(cells, []) == list(range(N)), "ordered contiguous cell partition")
    class_of = {vertex: number for number, cell in enumerate(cells)
                for vertex in cell}
    require(all(all((vertex in EXCEPTIONAL) == (cell[0] in EXCEPTIONAL)
                    for vertex in cell) for cell in cells),
            "degree-homogeneous certificate cells")
    sizes = tuple(map(len, cells))
    require(raw["active_selectors"] == [278], "one-hot selector metadata")

    tables = {}
    orbit_entries = 0
    expanded_nonzero = 0
    for row in raw["four_tables"]:
        require(set(row) == {"types", "orbits"}, "four-table fields")
        types = tuple(row["types"])
        require(len(types) == 4 and tuple(sorted(types)) == types,
                "canonical four-table type order")
        require(all(type(t) is int and 0 <= t < len(cells) for t in types),
                "four-table type domain")
        require(all(types.count(t) <= sizes[t] for t in set(types)),
                "four-table type capacity")
        require(types not in tables, "duplicate four-table type")
        automorphisms = [
            permutation for permutation in permutations(range(4))
            if tuple(types[j] for j in permutation) == types
        ]
        distribution = [0] * 64
        covered = set()
        for key, mass in row["orbits"].items():
            representative = int(key)
            require(str(representative) == key and 0 <= representative < 64,
                    "canonical state key")
            require(type(mass) is int and 0 < mass <= denominator,
                    "positive integer orbit mass")
            orbit = {transported_state(representative, p) for p in automorphisms}
            require(representative == min(orbit), "noncanonical state representative")
            require(not covered.intersection(orbit), "overlapping state orbits")
            covered.update(orbit)
            for state in orbit:
                distribution[state] = mass
            orbit_entries += 1
        require(sum(distribution) == denominator, "four-table normalization")
        tables[types] = tuple(distribution)
        expanded_nonzero += sum(mass > 0 for mass in distribution)
    expected = {
        types for types in combinations_with_replacement(range(len(cells)), 4)
        if all(types.count(t) <= sizes[t] for t in set(types))
    }
    require(set(tables) == expected and len(tables) == 345,
            "complete feasible four-class multisets")
    require(orbit_entries == 3076 and expanded_nonzero == 4699,
            "orbit certificate census")
    return {
        "D": denominator,
        "cells": cells,
        "class_of": class_of,
        "tables": tables,
        "orbit_entries": orbit_entries,
        "expanded_nonzero": expanded_nonzero,
    }


def project_four(distribution, positions):
    require(tuple(sorted(positions)) == positions and len(positions) == 3,
            "four-to-three projection positions")
    edge_bits = [PAIRS4.index(pair) for pair in combinations(positions, 2)]
    result = [0] * 8
    for state, mass in enumerate(distribution):
        projected = sum(((state >> bit) & 1) << j
                        for j, bit in enumerate(edge_bits))
        result[projected] += mass
    return tuple(result)


class PhysicalPoint:
    def __init__(self, certificate, roots):
        self.D = certificate["D"]
        self.cells = certificate["cells"]
        self.class_of = certificate["class_of"]
        self.tables = certificate["tables"]
        self.roots = roots
        self.edge = {pair: i for i, pair in enumerate(combinations(range(N), 2), 1)}
        self.triangle = {
            vertices: 904 + i
            for i, vertices in enumerate(combinations(range(N), 3))
        }

        missed_keys = set()
        footprint_keys = set()
        for root in roots:
            for a, b in combinations(root["outside"], 2):
                missed_keys.update((a, b, h) for h in root["core"])
                footprint_keys.update(
                    (a, b, i, j) for i, j in combinations(root["core"], 2)
                )
        require((len(missed_keys), len(footprint_keys)) == (10612, 74513),
                "inherited coordinate support")
        self.missed = {key: 13634 + i for i, key in enumerate(sorted(missed_keys))}
        self.footprint = {
            key: 24246 + i for i, key in enumerate(sorted(footprint_keys))
        }

        self.triples = {}
        for vertices in combinations(range(N), 3):
            extra = next(v for v in range(N) if v not in vertices)
            four = tuple(sorted(vertices + (extra,)))
            positions = tuple(four.index(v) for v in vertices)
            self.triples[vertices] = project_four(self.four(four), positions)

        self.edges = {}
        for pair in combinations(range(N), 2):
            third = next(v for v in range(N) if v not in pair)
            triple = tuple(sorted(pair + (third,)))
            bit = tuple(combinations(triple, 2)).index(pair)
            self.edges[pair] = sum(
                mass for state, mass in enumerate(self.triples[triple])
                if (state >> bit) & 1
            )

        edge_marginal_checks = 0
        for triple, distribution in self.triples.items():
            for bit, pair in enumerate(combinations(triple, 2)):
                value = sum(mass for state, mass in enumerate(distribution)
                            if (state >> bit) & 1)
                require(value == self.edges[pair], "shared physical edge marginal")
                edge_marginal_checks += 1
        require(edge_marginal_checks == 37023, "all triple-to-edge marginals")

        self.V = [0] * 98759
        assigned = set()

        def assign(index, value):
            require(index not in assigned and 0 <= value <= self.D,
                    "coordinate uniqueness and box")
            assigned.add(index)
            self.V[index] = value

        for pair, index in self.edge.items():
            assign(index, self.edges[pair])
        for vertices, index in self.triangle.items():
            assign(index, self.triples[vertices][7])
        for root in range(389):
            assign(13245 + root, self.D if root == 278 else 0)
        for key, index in self.missed.items():
            assign(index, self.blue_wedge(*key))
        for (a, b, i, j), index in self.footprint.items():
            four = tuple(sorted((a, b, i, j)))
            distribution = self.four(four)
            pairs = tuple(combinations(four, 2))
            red_bit = pairs.index((i, j))
            blue_bits = [pairs.index(tuple(sorted(pair)))
                         for pair in ((a, i), (a, j), (b, i), (b, j))]
            value = sum(
                mass for state, mass in enumerate(distribution)
                if ((state >> red_bit) & 1)
                and not any((state >> bit) & 1 for bit in blue_bits)
            )
            assign(index, value)
        require(assigned == set(range(1, 98759)), "complete parent coordinate decoder")

        self.all_blue_wedges = {
            (a, b, h): self.blue_wedge(a, b, h)
            for a, b in combinations(range(N), 2)
            for h in range(N) if h not in (a, b)
        }
        require(len(self.all_blue_wedges) == 37023,
                "complete physical wedge support")

    def four(self, vertices):
        require(tuple(sorted(vertices)) == vertices and len(vertices) == 4,
                "physical four-set order")
        types = tuple(self.class_of[v] for v in vertices)
        require(tuple(sorted(types)) == types, "contiguous class transport")
        return self.tables[types]

    def blue_wedge(self, a, b, center):
        triple = tuple(sorted((a, b, center)))
        distribution = self.triples[triple]
        pairs = tuple(combinations(triple, 2))
        bits = (pairs.index(tuple(sorted((a, center)))),
                pairs.index(tuple(sorted((b, center)))))
        return sum(mass for state, mass in enumerate(distribution)
                   if not any((state >> bit) & 1 for bit in bits))


def parse_opb_row(raw):
    fields = raw.split()
    require(len(fields) >= 5 and len(fields) % 2 == 1 and fields[-1] == b";",
            "OPB row syntax")
    relation = fields[-3]
    require(relation in (b">=", b"="), "OPB row relation")
    rhs = int(fields[-2])
    terms = {}
    for offset in range(0, len(fields) - 3, 2):
        coefficient = int(fields[offset])
        token = fields[offset + 1]
        require(token.startswith(b"x"), "OPB variable token")
        variable = int(token[1:])
        require(1 <= variable <= 98758 and variable not in terms,
                "OPB variable identity")
        terms[variable] = coefficient
    return terms, relation, rhs


def root_row_spec(point):
    rows = {}
    number = 1974691
    for root_number, root in enumerate(point.roots):
        selector = 13245 + root_number
        for offset, (pair, bit) in enumerate(sorted(root["units"].items())):
            if bit:
                rows[number + offset] = ({point.edge[pair]: 1, selector: -1}, b">=", 0)
            else:
                rows[number + offset] = ({point.edge[pair]: -1, selector: -1}, b">=", -1)
        number += 169 + (57 if root["key"][0] == 4 else 0)
    require(number == 2044422 and len(rows) == 32287,
            "complete root-row location map")
    return rows


def forbidden_family(point):
    anchor = {
        pair: bit for pair, bit in point.roots[0]["units"].items() if 0 in pair
    }
    require(len(anchor) == 42, "complete anchor-zero star")
    require(all(all(root["units"][pair] == bit for pair, bit in anchor.items())
                for root in point.roots), "root-independent anchor-zero star")
    red = tuple(vertex for vertex in range(1, N) if anchor[(0, vertex)] == 1)
    blue = tuple(vertex for vertex in range(1, N) if anchor[(0, vertex)] == 0)
    require(red == (1, *range(2, 8), *range(15, 29)), "red anchor neighborhood")
    require(blue == (*range(8, 15), *range(29, 43)), "blue anchor neighborhood")
    rows = []
    for color, neighbors, state in ((0, blue, 0), (1, red, 63)):
        for four in combinations(neighbors, 4):
            variable = 125170 + 64 * subset_rank(four, N) + state
            source_row = 2 * subset_rank((0,) + four, N) + (2 if color else 1)
            rows.append((color, four, state, variable, source_row))
    require(len(rows) == 2 * comb(21, 4) == 11970,
            "complete forbidden-state family")
    require(len({row[3] for row in rows}) == 11970, "distinct forbidden variables")
    return rows


def five_clause_row_spec(point):
    rows = {}
    for color, four, _state, _variable, source_row in forbidden_family(point):
        coefficients = {
            point.edge[pair]: (-1 if color else 1)
            for pair in combinations((0,) + four, 2)
        }
        rows[source_row] = (coefficients, b">=", -9 if color else 1)
    require(len(rows) == 11970, "distinct source five-set clauses")
    return rows


def audit_base(path, point):
    expected = root_row_spec(point)
    five_rows = five_clause_row_spec(point)
    require(not set(expected).intersection(five_rows), "semantic row families disjoint")
    expected.update(five_rows)
    seen = set()
    digest = hashlib.sha256()
    byte_count = 0
    equalities = 0
    minimum = None
    with path.open("rb") as stream:
        header = next(stream, b"")
        require(header == BASE_HEADER, "retained OPB header")
        digest.update(header)
        byte_count += len(header)
        number = 0
        for number, raw in enumerate(stream, 1):
            digest.update(raw)
            byte_count += len(raw)
            terms, relation, rhs = parse_opb_row(raw)
            if number in expected:
                require((terms, relation, rhs) == expected[number],
                        "semantic retained row " + str(number))
                seen.add(number)
            slack = sum(coefficient * point.V[index]
                        for index, coefficient in terms.items()) - rhs * point.D
            if relation == b"=":
                equalities += 1
                require(slack == 0, "retained OPB equality " + str(number))
            else:
                require(slack >= 0, "retained OPB inequality " + str(number))
                minimum = slack if minimum is None else min(minimum, slack)
    require((number, equalities, byte_count) == (2983003, 87, 511537255),
            "entire retained OPB coverage")
    require(digest.hexdigest() == BASE_SHA256, "retained OPB identity")
    require(seen == set(expected), "all semantic retained rows observed")
    return {
        "base_rows": number,
        "base_equalities": equalities,
        "base_bytes": byte_count,
        "base_sha256": digest.hexdigest(),
        "minimum_base_slack": str(Q(minimum, point.D)),
        "physical_root_unit_rows": 32287,
        "physical_five_clause_rows": 11970,
        "total_semantic_source_rows": len(seen),
    }


def audit_anchor_links(path, point):
    require(file_hash(path) == LINK_SHA256, "anchor-link identity")
    require(sum(point.V[13245:13634]) == point.D, "selector sum")
    require(all(point.V[13245 + root] == 0 for root in REMOVED), "nine cuts")
    require(point.V[13245 + 278] == point.D, "root 278 selected")
    require(sum(value != 0 for value in point.V[13245:13634]) == 1,
            "one-hot selector")
    anchor_edges = sorted(point.roots[0]["units"])
    lines = path.read_bytes().splitlines()
    require(len(anchor_edges) == len(lines) == 83, "anchor-link row count")
    for pair, raw in zip(anchor_edges, lines):
        terms, relation, rhs = parse_opb_row(raw)
        wanted = {point.edge[pair]: 1}
        wanted.update({
            13245 + root_number: -1
            for root_number, root in enumerate(point.roots)
            if root["units"][pair]
        })
        require((terms, relation, rhs) == (wanted, b"=", 0),
                "anchor-link coefficients")
        require(sum(coefficient * point.V[index]
                    for index, coefficient in terms.items()) == 0,
                "anchor-link equality")
    return {
        "anchor_link_equations": 83,
        "anchor_link_sha256": file_hash(path),
        "nonzero_selectors": [278],
        "selector_values": ["1"],
        "selected_root": ["C77", 12, 0, "BB"],
    }


def audit_suffix(point):
    D, V = point.D, point.V
    red_slacks = []
    for pair, edge_variable in point.edge.items():
        triangles = sum(
            V[point.triangle[tuple(sorted(pair + (h,)))]]
            for h in range(N) if h not in pair
        )
        red_slacks.append(13 * V[edge_variable] - triangles)
    require(min(red_slacks) >= 0, "red codegree constraints")

    coupled_rows = 0
    facet_rows = 0
    minimum_coupled = None
    minimum_facet = None
    for root_number, root in enumerate(point.roots):
        selector = V[13245 + root_number]
        core, outside = root["core"], root["outside"]
        core_size = len(core)
        outside_pairs = comb(len(outside), 2)
        for i, j in combinations(core, 2):
            degree_sum = (20 if i in EXCEPTIONAL else 21) + (
                20 if j in EXCEPTIONAL else 21)
            K = 64 - core_size - degree_sum
            edge_value = V[point.edge[(i, j)]]
            Qsum = sum(V[point.footprint[(a, b, i, j)]]
                       for a, b in combinations(outside, 2))
            internal = sum(
                V[point.edge[tuple(sorted((h, w)))]]
                for h in (i, j) for w in core if h != w
            )
            external_triangles = sum(
                V[point.triangle[tuple(sorted((i, j, w)))]] for w in outside
            )
            constant = 45 - core_size - degree_sum
            S = constant * D + internal + external_triangles
            bend = comb(K, 2)
            gap = bend * edge_value + (outside_pairs - bend) * (D - selector) - Qsum
            require(gap >= 0, "coupled-column inequality")
            coupled_rows += 1
            minimum_coupled = gap if minimum_coupled is None else min(minimum_coupled, gap)
            for tangent in range(K):
                guard = (tangent * constant - comb(tangent + 1, 2)
                         + tangent * (core_size + 39))
                require(guard >= 0, "lower-hull guard")
                intercept = (Qsum - tangent * S + comb(tangent + 1, 2) * D
                             + guard * (2 * D - edge_value))
                gap = intercept - guard * selector
                require(gap >= 0, "lower-hull facet")
                facet_rows += 1
                minimum_facet = gap if minimum_facet is None else min(minimum_facet, gap)
            guard = -(K - 1) * constant + 2 * outside_pairs
            require(guard > 0, "upper-hull guard")
            intercept = (K - 1) * S - 2 * Qsum + guard * (2 * D - edge_value)
            gap = intercept - guard * selector
            require(gap >= 0, "upper-hull facet")
            facet_rows += 1
            minimum_facet = min(minimum_facet, gap)
    require((coupled_rows, facet_rows) == (21762, 264560),
            "complete semantic suffix")
    return {
        "red_codegree_rows": 903,
        "red_codegree_minimum_slack": str(Q(min(red_slacks), D)),
        "coupled_column_rows": coupled_rows,
        "moment_hull_rows": facet_rows,
        "minimum_coupled_slack": str(Q(minimum_coupled, D)),
        "minimum_hull_slack": str(Q(minimum_facet, D)),
    }


def audit_global_moments(point):
    D, V = point.D, point.V
    local_red = [0] * N
    local_blue = [0] * N
    blue_codegrees = Counter()
    atom_rows = 0
    for vertices, triangle_variable in point.triangle.items():
        pairs = tuple(combinations(vertices, 2))
        a, b, c = (V[point.edge[pair]] for pair in pairs)
        wedge = []
        for center in vertices:
            leaves = tuple(v for v in vertices if v != center)
            wedge.append(point.all_blue_wedges[(leaves[0], leaves[1], center)])
        u = wedge[0] + a + b - D
        v = wedge[1] + a + c - D
        w = wedge[2] + b + c - D
        z = V[triangle_variable]
        recovered = (
            D-a-b-c+u+v+w-z,
            a-u-v+z,
            b-u-w+z,
            u-z,
            c-v-w+z,
            v-z,
            w-z,
            z,
        )
        require(recovered == point.triples[vertices], "triangle atom inversion")
        require(min(recovered) >= 0 and sum(recovered) == D,
                "triangle probability distribution")
        for pair in pairs:
            blue_codegrees[pair] += recovered[0]
        for vertex in vertices:
            local_red[vertex] += recovered[7]
            local_blue[vertex] += recovered[0]
        atom_rows += 8

    star_equalities = 0
    for center in range(N):
        degree = 20 if center in EXCEPTIONAL else 21
        for first in range(N):
            if first == center:
                continue
            edge_value = V[point.edge[tuple(sorted((first, center)))]]
            red_sum = 0
            blue_sum = 0
            for second in range(N):
                if second in (center, first):
                    continue
                wedge = point.all_blue_wedges[
                    tuple(sorted((first, second))) + (center,)
                ]
                blue_sum += wedge
                red_sum += (
                    wedge + edge_value
                    + V[point.edge[tuple(sorted((second, center)))]] - D
                )
            require(red_sum == (degree - 1) * edge_value,
                    "red degree-star equality")
            require(blue_sum == (41 - degree) * (D - edge_value),
                    "blue degree-star equality")
            star_equalities += 1
    require(star_equalities == 1806, "global star equality count")

    blue_slacks = [
        13 * (D - V[point.edge[pair]]) - blue_codegrees[pair]
        for pair in point.edge
    ]
    require(min(blue_slacks) >= 0, "blue codegree constraints")
    expected_red = [93 if v in EXCEPTIONAL else 100 for v in range(N)]
    expected_blue = [
        107 if v in EXCEPTIONAL else (99 if v in (29, 30) else 100)
        for v in range(N)
    ]
    require(local_red == [value * D for value in expected_red],
            "red local triangle totals")
    require(local_blue == [value * D for value in expected_blue],
            "blue local triangle totals")
    require(sum((100 if v in EXCEPTIONAL else 107) * D - local_red[v]
                for v in range(N)) == 301 * D, "red deficiency sum")
    require(sum((114 if v in EXCEPTIONAL else 107) * D - local_blue[v]
                for v in range(N)) == 303 * D, "blue deficiency sum")
    require(atom_rows == 98728, "triangle atom row count")
    return {
        "triangle_atom_rows": atom_rows,
        "global_star_equalities": star_equalities,
        "blue_codegree_rows": 903,
        "blue_codegree_minimum_slack": str(Q(min(blue_slacks), D)),
        "red_deficiency_sum": 301,
        "blue_deficiency_sum": 303,
        "blue_totals": list(map(str, expected_blue)),
    }


def audit_four_hull(point):
    by_four = defaultdict(list)
    for key, variable in point.footprint.items():
        by_four[tuple(sorted(key))].append((key, variable))
    four_sets = 0
    marginal_equalities = 0
    footprint_equalities = 0
    census = Counter()
    minimum_mass = None
    for vertices in combinations(range(N), 4):
        distribution = point.four(vertices)
        require(sum(distribution) == point.D and min(distribution) >= 0,
                "physical four-state simplex")
        minimum_mass = min(distribution) if minimum_mass is None else min(
            minimum_mass, min(distribution))
        census[sum(v in EXCEPTIONAL for v in vertices)] += 1
        for positions in combinations(range(4), 3):
            triple = tuple(vertices[position] for position in positions)
            require(project_four(distribution, positions) == point.triples[triple],
                    "shared physical triple marginal")
            marginal_equalities += 8
        pairs = tuple(combinations(vertices, 2))
        for (a, b, i, j), variable in by_four[vertices]:
            red_bit = pairs.index((i, j))
            blue_bits = [pairs.index(tuple(sorted(pair)))
                         for pair in ((a, i), (a, j), (b, i), (b, j))]
            mass = sum(
                value for state, value in enumerate(distribution)
                if ((state >> red_bit) & 1)
                and not any((state >> bit) & 1 for bit in blue_bits)
            )
            require(mass == point.V[variable], "physical footprint marginal")
            footprint_equalities += 1
        four_sets += 1
    require((four_sets, marginal_equalities, footprint_equalities)
            == (123410, 3949120, 74513), "complete P4 lift")
    expected_census = [comb(13, q) * comb(30, 4-q) for q in range(5)]
    require([census[q] for q in range(5)] == expected_census,
            "physical four-set census")
    return {
        "four_sets": four_sets,
        "four_nonnegative_rows": 64 * four_sets,
        "four_normalizations": four_sets,
        "triangle_marginal_equalities": marginal_equalities,
        "footprint_equalities": footprint_equalities,
        "physical_four_set_census": expected_census,
        "four_state_minimum_mass": str(Q(minimum_mass, point.D)),
    }


def audit_forbidden(path, point):
    require(file_hash(path) == FORBIDDEN_SHA256, "forbidden-row file identity")
    family = forbidden_family(point)
    lines = path.read_bytes().splitlines()
    require(len(lines) == len(family) == 11970, "forbidden-row count")
    positive = Counter()
    target = None
    for (color, four, state, variable, _source), raw in zip(family, lines):
        require(raw == f"-1 x{variable} >= 0 ;".encode("ascii"),
                "forbidden-state literal row")
        mass = point.four(four)[state]
        if mass:
            positive[color] += 1
        if color == 0 and four == (39, 40, 41, 42):
            target = Q(mass, point.D)
    require((positive[0], positive[1]) == (3813, 0),
            "forbidden-state violation census")
    require(target is not None and target > Q(11, 100),
            "strict displayed blue separator")

    implication_cases = 0
    five_pairs = tuple(combinations(range(5), 2))
    anchor_bits = [i for i, pair in enumerate(five_pairs) if 0 in pair]
    inner_bits = [i for i, pair in enumerate(five_pairs) if 0 not in pair]
    for color in (0, 1):
        for state in range(1 << 10):
            fixed_star = all(((state >> bit) & 1) == color for bit in anchor_bits)
            avoids_monochromatic_five = (
                state.bit_count() <= 9 if color else state.bit_count() >= 1
            )
            monochromatic_inner = all(
                ((state >> bit) & 1) == color for bit in inner_bits
            )
            require(not (fixed_star and avoids_monochromatic_five
                         and monochromatic_inner),
                    "five-vertex forbidden-event implication")
            implication_cases += 1
    require(implication_cases == 2048, "Boolean implication case count")
    return {
        "forbidden_state_rows": 11970,
        "forbidden_state_sha256": file_hash(path),
        "violated_blue_forbidden_states": positive[0],
        "violated_red_forbidden_states": positive[1],
        "separating_anchor": 0,
        "separating_four": [39, 40, 41, 42],
        "separating_blue_mass": str(target),
        "separation_gap_strict_lower_bound": "11/100",
        "boolean_implication_cases": implication_cases,
        "next_system_rows": 15429010,
        "next_system_equalities": 4149019,
        "next_system_status": "UNDECIDED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    args = parser.parse_args()

    package, root_table, source = verify_source(args.source)
    roots = enumerate_roots(root_table)
    certificate = load_certificate(package / "certificate.json")
    point = PhysicalPoint(certificate, roots)
    result = {
        "status": "INDEPENDENT_ACCEPTANCE_M214_ANCHOR_LINKED_P4_SURVIVOR",
        "source": source,
        "certificate_sha256": CERTIFICATE_SHA256,
        "common_denominator": str(point.D),
        "certificate_four_class_tables": len(certificate["tables"]),
        "certificate_orbit_entries": certificate["orbit_entries"],
        "certificate_expanded_nonzero_states": certificate["expanded_nonzero"],
        "total_variables": 8023409,
        "total_rows": 15417040,
        "total_equalities": 4149019,
        **audit_anchor_links(args.replay / "anchor-links.opbpart", point),
        **audit_global_moments(point),
        **audit_four_hull(point),
        **audit_suffix(point),
        **audit_base(args.replay / "m214-3323.opb", point),
        **audit_forbidden(args.replay / "forbidden.opbpart", point),
        "trust_boundary": [
            "upstream reviewed M214/P4 formulation and coordinate semantics",
            "Ramsey interpretation of the nine imported Boolean exclusions",
            "independent unformalized decoder, CPython exact arithmetic, SHA-256, and ordinary hardware",
        ],
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
