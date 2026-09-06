#!/usr/bin/env python3
"""Independent exact audit of the M214 post-cut selector fiber.

No contribution module is imported.  The checker reconstructs the five
four-edge-state tables from the four published rational parameters, decodes
all inherited coordinates, evaluates the complete parent OPB over the entire
selector box, checks the semantic suffix/P4 lift, and derives the selector
fiber, anchor linkage, and rank-one integer cut independently.
"""

import argparse
from collections import Counter, defaultdict
from fractions import Fraction as Q
import hashlib
from itertools import combinations, product
import json
from math import comb, gcd, lcm
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True

SOURCE_COMMIT = "e133a3d7364b1c3d96846d1e0ba83b1eef898ab2"
SOURCE_MANIFEST_SHA256 = "1d9d1f2b326797b94e17db55c28eb193a3599185fe458cae151816e08a617948"
ROOT_TABLE_SHA256 = "f7148c9f6e631f1efae81ba1700c0afeb38660aa7556b79ead2c34d67cac978e"
PARENT_SHA256 = "9a3f66683a9cfad87d4ed0cdeb6bd14e5955540b05a8b48576b9f5653dcbd609"
PARENT_HEADER = b"* #variable= 98758 #constraint= 2983003 #equal= 87 intsize= 64\n"
CERTIFICATE_SHA256 = "6da7466019c96be2af879b98bc7164a5208479cb8921f8c00c91e0bd2809e231"
LINKS_SHA256 = "f2bef9213e141982f863601df3dc57d07ee20b1d5f0b9bcb559799a2187bafa1"

N = 43
EXCEPTIONAL = frozenset(range(2, 15))
REMOVED = (48, 128, 129, 201, 202, 299, 300, 375, 376)
SELECTOR_FIRST = 13245
EDGE_PAIRS4 = tuple(combinations(range(4), 2))


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


def edge_index(left, right):
    left, right = sorted((left, right))
    require(0 <= left < right < N, "edge domain")
    return left * (2 * N - left - 1) // 2 + right - left


def verify_source(source):
    package = source / "ramsey_r55_m214_postcut_selector_fiber"
    manifest = package / "SHA256SUMS"
    require(file_hash(manifest) == SOURCE_MANIFEST_SHA256, "source manifest identity")
    entries = {}
    for line in manifest.read_text(encoding="ascii").splitlines():
        digest, name = line.split(maxsplit=1)
        require(name not in entries, "duplicate manifest entry")
        entries[name] = digest
        require(file_hash(package / name) == digest, "source identity: " + name)
    require(len(entries) == 11, "manifest entry count")
    table = source / "ramsey_r55_m214_pair_normalization" / "roots.tsv"
    require(file_hash(table) == ROOT_TABLE_SHA256, "root-table identity")
    commit = subprocess.check_output(
        ["git", "-C", str(source), "rev-parse", "HEAD"], text=True
    ).strip()
    require(commit == SOURCE_COMMIT, "source commit")
    return package, table, {
        "commit": commit,
        "manifest_sha256": SOURCE_MANIFEST_SHA256,
        "manifest_entries": len(entries),
    }


def make_roots(table):
    """Re-enumerate the 389 keys and their two-anchor units."""
    family_data = (
        ("E8", ("H", "A")),
        ("E77", ("BB", "BO", "OO")),
        ("C8", ("B", "O")),
        ("C77", ("BB", "BO", "OO")),
        ("C77partition", ("HO", "AB")),
    )
    roots = []
    expected_table_keys = []
    for family_number, (family, patterns) in enumerate(family_data):
        for c in range(9, 14):
            for k in range(7):
                sizes = (k, 6-k, 6-k, 1+k, c-k, 14-c+k, 14-c+k, c-k)
                cells = []
                cursor = 2
                for size in sizes:
                    cells.append(tuple(range(cursor, cursor + size)))
                    cursor += size
                require(cursor == 43, "cell partition")
                for pattern in patterns:
                    first = 0 if family_number < 2 else 4
                    if any(pattern.count(label) > sizes[first + offset]
                           for offset, label in enumerate("HABO")):
                        continue
                    core = tuple(sorted(cells[0] + cells[4]))
                    exterior = tuple(v for v in range(2, 43) if v not in core)
                    units = {(0, 1): 1}
                    states = ((1, 1), (1, 0), (0, 1), (0, 0))
                    for cell_number, cell in enumerate(cells):
                        for vertex in cell:
                            units[0, vertex] = states[cell_number % 4][0]
                            units[1, vertex] = states[cell_number % 4][1]
                    require(len(units) == 83, "complete two-anchor star")
                    roots.append({
                        "key": (family_number, c, k, pattern),
                        "core": core,
                        "exterior": exterior,
                        "units": units,
                    })
                    expected_table_keys.append((family, str(c), str(k), pattern))
    require(len(roots) == 389, "root count")
    selected = tuple(i for i, root in enumerate(roots)
                     if root["key"][1:3] == (13, 0))
    require(selected == REMOVED, "nine c=13,k=0 root indices")

    lines = table.read_text(encoding="ascii").splitlines()
    require(lines[0].split("\t")[:4] == ["family", "c", "k", "pattern"],
            "root table header")
    records = [line.split("\t") for line in lines[1:]]
    require(len(records) == 389, "root table record count")
    require(all(tuple(row[:4]) == key
                for row, key in zip(records, expected_table_keys)),
            "independent root ordering")
    return roots


def walsh_tables(parameters):
    require(set(parameters) == {"u", "v", "t1", "t2"}, "parameter fields")
    u, v, t1, t2 = (Q(parameters[name])
                     for name in ("u", "v", "t1", "t2"))
    p_ee, p_ec, p_cc = Q(20, 39), Q(6, 13), Q(15, 29)
    wedge = {
        (1, 2): (19*p_ee - 30*u) / 11,
        (1, 1): u,
        (1, 0): (19*p_ec - 12*u) / 29,
        (0, 2): (20*p_ec - 29*v) / 12,
        (0, 1): v,
        (0, 0): (20*p_cc - 13*v) / 28,
    }
    triangle = {
        3: (93 - 360*t2 - 435*t1) / 66,
        2: t2,
        1: t1,
        0: (100 - 78*t2 - 377*t1) / 406,
    }
    tables = []
    for exceptional_count in range(5):
        types = tuple(int(vertex < exceptional_count) for vertex in range(4))

        def edge_probability(pair):
            return (p_cc, p_ec, p_ee)[types[pair[0]] + types[pair[1]]]

        coefficients = {0: Q(1)}
        for bit, pair in enumerate(EDGE_PAIRS4):
            coefficients[1 << bit] = 1 - 2*edge_probability(pair)
        for bit1, bit2 in combinations(range(6), 2):
            common = set(EDGE_PAIRS4[bit1]) & set(EDGE_PAIRS4[bit2])
            if not common:
                continue
            center = next(iter(common))
            leaves = (set(EDGE_PAIRS4[bit1]) | set(EDGE_PAIRS4[bit2])) - {center}
            joint = wedge[types[center], sum(types[leaf] for leaf in leaves)]
            coefficients[(1 << bit1) | (1 << bit2)] = (
                1 - 2*edge_probability(EDGE_PAIRS4[bit1])
                - 2*edge_probability(EDGE_PAIRS4[bit2]) + 4*joint
            )
        for vertices in combinations(range(4), 3):
            edge_bits = [EDGE_PAIRS4.index(pair) for pair in combinations(vertices, 2)]
            joints = sum(
                wedge[types[center],
                      sum(types[leaf] for leaf in vertices if leaf != center)]
                for center in vertices
            )
            mask = sum(1 << bit for bit in edge_bits)
            coefficients[mask] = (
                1 - 2*sum(edge_probability(EDGE_PAIRS4[bit]) for bit in edge_bits)
                + 4*joints - 8*triangle[sum(types[vertex] for vertex in vertices)]
            )
        require(len(coefficients) == 23, "specified Walsh support")
        atoms = [
            sum(value * (-1)**((mask & subset).bit_count())
                for subset, value in coefficients.items()) / 64
            for mask in range(64)
        ]
        require(sum(atoms) == 1 and min(atoms) > 0, "positive probability table")
        tables.append(tuple(atoms))
    denominator = lcm(*(value.denominator for table in tables for value in table))
    return denominator, tables


def load_certificate(package, parameters):
    path = package / "certificate.json"
    require(file_hash(path) == CERTIFICATE_SHA256, "certificate identity")
    data = json.loads(path.read_text(encoding="ascii"))
    denominator, tables = walsh_tables(parameters)
    require(data["denominator"] == denominator == 2533440000,
            "probability denominator")
    encoded = []
    for count, table in enumerate(tables):
        row = data["four_vertex_atoms"][count]
        require(row["exceptional_count"] == count, "table order")
        numerators = tuple(int(value * denominator) for value in table)
        require(row["numerators"] == list(numerators), "reconstructed table " + str(count))
        encoded.append(numerators)
    minimum = min(value for row in tables for value in row)
    require(minimum == Q(226211, 60320000), "minimum table mass")
    return denominator, encoded


def physical_distribution(canonical, physical_types):
    """Transport an exceptional-first table to a physical vertex ordering."""
    order = (tuple(i for i, kind in enumerate(physical_types) if kind)
             + tuple(i for i, kind in enumerate(physical_types) if not kind))
    answer = []
    for physical_mask in range(64):
        canonical_mask = 0
        for bit, (left, right) in enumerate(EDGE_PAIRS4):
            physical_pair = tuple(sorted((order[left], order[right])))
            source_bit = EDGE_PAIRS4.index(physical_pair)
            canonical_mask |= ((physical_mask >> source_bit) & 1) << bit
        answer.append(canonical[canonical_mask])
    return tuple(answer)


def project_to_three(distribution, positions):
    bits = [EDGE_PAIRS4.index(pair) for pair in combinations(positions, 2)]
    result = [0] * 8
    for state, mass in enumerate(distribution):
        target = sum(((state >> bit) & 1) << offset
                     for offset, bit in enumerate(bits))
        result[target] += mass
    return tuple(result)


class MomentPoint:
    def __init__(self, denominator, canonical_tables, roots):
        self.D = denominator
        self.roots = roots
        self.four = {}
        for types in product((0, 1), repeat=4):
            self.four[types] = physical_distribution(
                canonical_tables[sum(types)], types
            )
        self.triples = {
            types: project_to_three(self.four[types + (0,)], (0, 1, 2))
            for types in product((0, 1), repeat=3)
        }
        self.edges = {
            types: sum(mass for state, mass in enumerate(self.triples[types + (0,)])
                       if state & 1)
            for types in product((0, 1), repeat=2)
        }
        self.edge_variables = {
            pair: index for index, pair in enumerate(combinations(range(N), 2), 1)
        }
        self.triangle_variables = {
            vertices: index
            for index, vertices in enumerate(combinations(range(N), 3), 904)
        }
        missing_keys = set()
        footprint_keys = set()
        for root in roots:
            for a, b in combinations(root["exterior"], 2):
                missing_keys.update((a, b, h) for h in root["core"])
                footprint_keys.update((a, b, i, j)
                                      for i, j in combinations(root["core"], 2))
        require((len(missing_keys), len(footprint_keys)) == (10612, 74513),
                "extended-coordinate support")
        self.missing_variables = {
            key: 13634 + index for index, key in enumerate(sorted(missing_keys))
        }
        self.footprint_variables = {
            key: 24246 + index for index, key in enumerate(sorted(footprint_keys))
        }
        self.values = [0] * 98759
        defined = set()

        def set_value(index, value):
            require(index not in defined and 0 <= value <= self.D,
                    "coordinate domain/uniqueness")
            defined.add(index)
            self.values[index] = value

        for pair, index in self.edge_variables.items():
            set_value(index, self.edges[self.types(pair)])
        for vertices, index in self.triangle_variables.items():
            set_value(index, self.triples[self.types(vertices)][7])
        for root in range(389):
            set_value(SELECTOR_FIRST + root, 0)
        for key, index in self.missing_variables.items():
            set_value(index, self.blue_wedge(*key))
        for key, index in self.footprint_variables.items():
            dist = self.four[self.types(key)]
            set_value(index, dist[32] + dist[33])
        require(defined == set(range(1, 98759)), "all base coordinates decoded")
        self.all_blue_wedges = {
            (a, b, h): self.blue_wedge(a, b, h)
            for a, b in combinations(range(N), 2)
            for h in range(N) if h not in (a, b)
        }
        require(len(self.all_blue_wedges) == 37023, "all physical wedges")

    @staticmethod
    def types(vertices):
        return tuple(int(vertex in EXCEPTIONAL) for vertex in vertices)

    def blue_wedge(self, a, b, center):
        # In triple order (a,b,center), states 0 and 1 leave both
        # center incidences blue while the edge ab is unrestricted.
        dist = self.triples[self.types((a, b, center))]
        return dist[0] + dist[1]


def root_unit_rows(point):
    wanted = {}
    first = 1974691
    for root_number, root in enumerate(point.roots):
        selector = SELECTOR_FIRST + root_number
        for offset, (pair, bit) in enumerate(sorted(root["units"].items())):
            wanted[first + offset] = (
                {point.edge_variables[pair]: 1 if bit else -1, selector: -1},
                b">=", 0 if bit else -1,
            )
        first += 169 + (57 if root["key"][0] == 4 else 0)
    require(first == 2044422 and len(wanted) == 32287,
            "all physical root-unit rows")
    return wanted


def parse_opb_row(raw):
    fields = raw.split()
    require(len(fields) >= 5 and len(fields) % 2 == 1 and fields[-1] == b";",
            "OPB syntax")
    relation = fields[-3]
    require(relation in (b">=", b"="), "OPB relation")
    terms = {}
    for offset in range(0, len(fields) - 3, 2):
        coefficient = int(fields[offset])
        token = fields[offset + 1]
        require(token.startswith(b"x"), "OPB variable")
        variable = int(token[1:])
        require(1 <= variable <= 98758 and variable not in terms,
                "OPB variable range/uniqueness")
        terms[variable] = coefficient
    return terms, relation, int(fields[-2])


def audit_parent(opb, point):
    """Evaluate each inequality at its exact box minimum."""
    wanted = root_unit_rows(point)
    seen = set()
    digest = hashlib.sha256()
    byte_count = 0
    equality_count = 0
    selector_equality_count = 0
    sharp_roots = set()
    minimum_slack = None
    selector_endpoint = 6 * point.D // 13
    require(13 * selector_endpoint == 6 * point.D, "integral selector endpoint")
    with opb.open("rb") as stream:
        header = stream.readline()
        require(header == PARENT_HEADER, "parent header")
        digest.update(header)
        byte_count += len(header)
        for number, raw in enumerate(stream, 1):
            digest.update(raw)
            byte_count += len(raw)
            terms, relation, rhs = parse_opb_row(raw)
            value = -rhs * point.D
            selector_terms = {}
            for variable, coefficient in terms.items():
                if SELECTOR_FIRST <= variable < SELECTOR_FIRST + 389:
                    selector_terms[variable] = coefficient
                else:
                    value += coefficient * point.values[variable]
            if number in wanted:
                require((terms, relation, rhs) == wanted[number],
                        "root unit provenance " + str(number))
                seen.add(number)
            if relation == b"=":
                equality_count += 1
                if selector_terms:
                    expected = {SELECTOR_FIRST + root: 1 for root in range(389)}
                    require(number == 1974690 and terms == expected and rhs == 1,
                            "sole selector equality")
                    selector_equality_count += 1
                else:
                    require(value == 0, "base equality " + str(number))
                continue
            box_minimum = value + sum(
                min(0, coefficient * selector_endpoint)
                for coefficient in selector_terms.values()
            )
            require(box_minimum >= 0, "base box inequality " + str(number))
            minimum_slack = (box_minimum if minimum_slack is None
                             else min(minimum_slack, box_minimum))
            if (terms.get(point.edge_variables[0, 2]) == 1
                    and rhs == 0 and len(selector_terms) == 1
                    and next(iter(selector_terms.values())) == -1):
                sharp_roots.add(next(iter(selector_terms)) - SELECTOR_FIRST)
    require((number, byte_count, equality_count) == (2983003, 511537255, 87),
            "full parent row/byte/equality count")
    require(digest.hexdigest() == PARENT_SHA256, "full parent identity")
    require(seen == set(wanted) and selector_equality_count == 1,
            "root-unit and selector-sum coverage")
    require(sharp_roots == set(range(389)), "common sharp cap guards")
    require(Q(point.values[point.edge_variables[0, 2]], point.D) == Q(6, 13),
            "separating edge value")
    return {
        "base_rows": number,
        "base_bytes": byte_count,
        "base_equalities": equality_count,
        "base_sha256": digest.hexdigest(),
        "physical_root_unit_rows": len(seen),
        "sharp_selector_cap_rows": len(sharp_roots),
        "base_minimum_box_slack": str(Q(minimum_slack, point.D)),
    }


def audit_suffix(point):
    """Check all post-parent constraints directly from their definitions."""
    D = point.D
    V = point.values
    endpoint = 6 * D // 13

    red_codegree_slacks = []
    for pair, variable in point.edge_variables.items():
        triangle_total = sum(
            V[point.triangle_variables[tuple(sorted(pair + (third,)))]]
            for third in range(N) if third not in pair
        )
        red_codegree_slacks.append(13 * V[variable] - triangle_total)
    require(min(red_codegree_slacks) >= 0, "red codegree constraints")

    coupled_count = 0
    facet_count = 0
    coupled_caps = []
    facet_caps = []
    for root in point.roots:
        core, exterior = root["core"], root["exterior"]
        core_size = len(core)
        exterior_pairs = comb(len(exterior), 2)
        for i, j in combinations(core, 2):
            degree_sum = ((20 if i in EXCEPTIONAL else 21)
                          + (20 if j in EXCEPTIONAL else 21))
            K = 64 - core_size - degree_sum
            edge_mass = V[point.edge_variables[tuple(sorted((i, j)))]]
            footprint = sum(
                V[point.footprint_variables[a, b, i, j]]
                for a, b in combinations(exterior, 2)
            )
            core_incidence = sum(
                V[point.edge_variables[tuple(sorted((center, vertex)))]]
                for center in (i, j) for vertex in core if vertex != center
            )
            outside_triangles = sum(
                V[point.triangle_variables[tuple(sorted((i, j, vertex)))]]
                for vertex in exterior
            )
            constant = 45 - core_size - degree_sum
            S = constant * D + core_incidence + outside_triangles
            binomial = comb(K, 2)
            coupled_gap = (binomial * edge_mass
                           + (exterior_pairs - binomial) * (D - endpoint)
                           - footprint)
            require(coupled_gap >= 0, "coupled-column selector box")
            coupled_caps.append(Q(
                binomial * edge_mass + (exterior_pairs - binomial) * D
                - footprint,
                (exterior_pairs - binomial) * D,
            ))
            coupled_count += 1
            for tangent in range(K):
                guard = (tangent * constant - comb(tangent + 1, 2)
                         + tangent * (core_size + 39))
                require(guard >= 0, "lower-facet guard")
                intercept = (footprint - tangent*S + comb(tangent + 1, 2)*D
                             + guard * (2*D - edge_mass))
                require(intercept - guard*endpoint >= 0,
                        "lower moment-hull selector box")
                if guard:
                    facet_caps.append(Q(intercept, guard*D))
                facet_count += 1
            guard = -(K - 1)*constant + 2*exterior_pairs
            require(guard > 0, "upper-facet guard")
            intercept = ((K - 1)*S - 2*footprint
                         + guard*(2*D - edge_mass))
            require(intercept - guard*endpoint >= 0,
                    "upper moment-hull selector box")
            facet_caps.append(Q(intercept, guard*D))
            facet_count += 1
    require((coupled_count, facet_count) == (21762, 264560),
            "complete column/hull suffix")

    blue_triangle_totals = [0] * N
    blue_codegree = Counter()
    atom_rows = 0
    for vertices, triangle_variable in point.triangle_variables.items():
        pairs = tuple(combinations(vertices, 2))
        edge_masses = [V[point.edge_variables[pair]] for pair in pairs]
        wedges = [
            point.all_blue_wedges[
                tuple(vertex for vertex in vertices if vertex != center) + (center,)
            ]
            for center in vertices
        ]
        a, b, c = edge_masses
        joint_ab = wedges[0] + a + b - D
        joint_ac = wedges[1] + a + c - D
        joint_bc = wedges[2] + b + c - D
        red_triangle = V[triangle_variable]
        atoms = (
            D-a-b-c+joint_ab+joint_ac+joint_bc-red_triangle,
            a-joint_ab-joint_ac+red_triangle,
            b-joint_ab-joint_bc+red_triangle,
            joint_ab-red_triangle,
            c-joint_ac-joint_bc+red_triangle,
            joint_ac-red_triangle,
            joint_bc-red_triangle,
            red_triangle,
        )
        require(atoms == point.triples[point.types(vertices)]
                and min(atoms) >= 0 and sum(atoms) == D,
                "triangle atom inversion")
        for pair in pairs:
            blue_codegree[pair] += atoms[0]
        for center in vertices:
            blue_triangle_totals[center] += atoms[0]
        atom_rows += 8
    require(atom_rows == 98728, "triangle atom rows")

    star_equalities = 0
    for center in range(N):
        degree = 20 if center in EXCEPTIONAL else 21
        for first in range(N):
            if first == center:
                continue
            edge_mass = V[point.edge_variables[tuple(sorted((first, center)))]]
            red_sum = 0
            blue_sum = 0
            for second in range(N):
                if second in (center, first):
                    continue
                wedge_mass = point.all_blue_wedges[
                    tuple(sorted((first, second))) + (center,)
                ]
                blue_sum += wedge_mass
                red_sum += (wedge_mass + edge_mass
                            + V[point.edge_variables[tuple(sorted((second, center)))]]
                            - D)
            require(red_sum == (degree - 1) * edge_mass,
                    "red degree-star equality")
            require(blue_sum == (41 - degree) * (D - edge_mass),
                    "blue degree-star equality")
            star_equalities += 1
    require(star_equalities == 1806, "all degree-star equalities")

    blue_slacks = [
        13*(D - V[variable]) - blue_codegree[pair]
        for pair, variable in point.edge_variables.items()
    ]
    require(min(blue_slacks) >= 0, "blue codegree constraints")
    expected_blue = [
        Q(1389, 13) if vertex in EXCEPTIONAL else Q(100)
        for vertex in range(N)
    ]
    require([Q(value, D) for value in blue_triangle_totals] == expected_blue,
            "blue local triangle totals")

    # The five canonical tables cover all physical four-set type patterns.
    by_four = defaultdict(list)
    for key, variable in point.footprint_variables.items():
        by_four[tuple(sorted(key))].append((key, variable))
    four_sets = 0
    marginal_equalities = 0
    footprint_equalities = 0
    census = Counter()
    for vertices in combinations(range(N), 4):
        types = point.types(vertices)
        dist = point.four[types]
        require(sum(dist) == D and min(dist) >= 0, "four-state simplex")
        census[sum(types)] += 1
        for positions in combinations(range(4), 3):
            triple = tuple(vertices[position] for position in positions)
            require(project_to_three(dist, positions)
                    == point.triples[point.types(triple)],
                    "shared triple marginal")
            marginal_equalities += 8
        pairs = tuple(combinations(vertices, 2))
        for (a, b, i, j), variable in by_four[vertices]:
            red_bit = 1 << pairs.index((i, j))
            blue_bits = sum(
                1 << pairs.index(tuple(sorted((outside, inside))))
                for outside in (a, b) for inside in (i, j)
            )
            mass = sum(value for state, value in enumerate(dist)
                       if state & red_bit and not state & blue_bits)
            require(mass == V[variable], "five-edge footprint marginal")
            footprint_equalities += 1
        four_sets += 1
    require((four_sets, marginal_equalities, footprint_equalities)
            == (123410, 3949120, 74513), "complete P4 lift")
    expected_census = [comb(13, q)*comb(30, 4-q) for q in range(5)]
    require([census[q] for q in range(5)] == expected_census,
            "four-set class census")
    return {
        "red_codegree_rows": len(red_codegree_slacks),
        "red_codegree_minimum_slack": str(Q(min(red_codegree_slacks), D)),
        "coupled_column_rows": coupled_count,
        "moment_hull_rows": facet_count,
        "minimum_coupled_selector_cap": str(min(coupled_caps)),
        "minimum_hull_selector_cap": str(min(facet_caps)),
        "triangle_atom_rows": atom_rows,
        "global_star_equalities": star_equalities,
        "blue_codegree_rows": len(blue_slacks),
        "blue_codegree_minimum_slack": str(Q(min(blue_slacks), D)),
        "blue_totals_E": "1389/13",
        "blue_totals_C": "100",
        "four_sets": four_sets,
        "four_nonnegative_rows": 64*four_sets,
        "triangle_marginal_equalities": marginal_equalities,
        "footprint_equalities": footprint_equalities,
        "physical_four_set_census": expected_census,
    }


def audit_links_and_fiber(links_path, point, package):
    require(file_hash(links_path) == LINKS_SHA256, "anchor-link identity")
    retained = [root for root in range(389) if root not in REMOVED]
    require(len(retained) == 380, "retained selector count")
    require(2*Q(6, 13) < 1 <= 3*Q(6, 13), "sharp three-selector threshold")
    require(Q(1, 380) <= Q(6, 13), "post-cut barycenter")
    anchor_pairs = sorted(point.roots[0]["units"])
    require(len(anchor_pairs) == 83, "anchor-edge domain")
    common = set(point.roots[retained[0]]["units"].items())
    for root in retained:
        require(set(point.roots[root]["units"]) == set(anchor_pairs),
                "common anchor domain")
        common &= set(point.roots[root]["units"].items())
    require(len(common) == 53 and ((0, 2), 1) in common,
            "post-cut common anchor units")

    lines = links_path.read_text(encoding="ascii").splitlines()
    require(len(lines) == 83, "anchor-link equation count")
    violations = 0
    for pair, line in zip(anchor_pairs, lines):
        terms, relation, rhs = parse_opb_row(line.encode("ascii"))
        expected = {point.edge_variables[pair]: 1}
        expected.update({
            SELECTOR_FIRST + root: -1
            for root in range(389) if point.roots[root]["units"][pair]
        })
        require((terms, relation, rhs) == (expected, b"=", 0),
                "anchor-link equation")
        physical = Q(point.values[point.edge_variables[pair]], point.D)
        predicted = sum(
            Q(1, 380) for root in retained
            if point.roots[root]["units"][pair]
        )
        violations += physical != predicted
    require(violations == 83, "barycenter violates every anchor link")
    common_violations = sum(
        Q(point.values[point.edge_variables[pair]], point.D) != bit
        for pair, bit in common
    )
    require(common_violations == 53, "all common anchor units separated")

    cg = json.loads((package / "anchor_cg.json").read_text(encoding="ascii"))
    require(cg["edge"] == [0, 2] and cg["physical_variable"] == 2
            and cg["guard_rows"] == 389, "CG premise metadata")
    multiplier = Q(cg["each_guard_multiplier"])
    equality_multiplier = Q(cg["selector_equality_multiplier"])
    require(multiplier == equality_multiplier == Q(1, 389),
            "CG multipliers")
    coefficients = Counter()
    for root in range(389):
        coefficients[2] += multiplier
        coefficients[SELECTOR_FIRST + root] -= multiplier
        coefficients[SELECTOR_FIRST + root] += equality_multiplier
    coefficients = {str(variable): str(value)
                    for variable, value in coefficients.items() if value}
    require(coefficients == cg["pre_round_coefficients"] == {"2": "1"},
            "CG coefficient cancellation")
    require(Q(cg["pre_round_rhs"]) == Q(1, 389)
            and cg["rounded_rhs"] == 1, "CG integer rounding")
    require(1 - Q(point.values[2], point.D) == Q(7, 13),
            "CG family separation gap")
    return {
        "removed_roots": list(REMOVED),
        "retained_selectors": 380,
        "selector_cap": "6/13",
        "uniform_selector": "1/380",
        "minimum_retained_roots_for_this_family": 3,
        "root_unit_link_equations": 83,
        "root_unit_link_cases": 389*83,
        "postcut_common_anchor_units": 53,
        "violated_common_units": common_violations,
        "uniform_anchor_link_violations": violations,
        "separating_edge": [0, 2],
        "separating_edge_value": "6/13",
        "required_common_edge_value": "1",
        "separation_gap": "7/13",
        "cg_guard_premises": 389,
        "cg_pre_round_rhs": "1/389",
        "cg_rounded_rhs": 1,
        "cg_rank": 1,
        "anchor_link_sha256": file_hash(links_path),
        "anchor_link_strengthened_system_status": "UNDECIDED",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--replay", type=Path, required=True)
    args = parser.parse_args()

    package, table, source_result = verify_source(args.source)
    roots = make_roots(table)
    parameters = json.loads((package / "parameters.json").read_text(encoding="ascii"))
    denominator, canonical = load_certificate(package, parameters)
    point = MomentPoint(denominator, canonical, roots)
    parent = audit_parent(args.replay / "m214-3323.opb", point)
    suffix = audit_suffix(point)
    fiber = audit_links_and_fiber(args.replay / "anchor-links.opbpart",
                                  point, package)
    result = {
        "status": "INDEPENDENT_ACCEPTANCE_M214_POSTCUT_SELECTOR_FIBER",
        "source": source_result,
        "certificate_sha256": CERTIFICATE_SHA256,
        "physical_moment_denominator": denominator,
        "postcut_point_denominator": lcm(denominator, 380),
        "four_state_minimum_mass": "226211/60320000",
        "total_variables": 8023409,
        "total_rows_with_nine_cuts": 15416957,
        "total_equalities": 4148936,
        **parent,
        **suffix,
        **fiber,
        "trust_boundary": [
            "upstream reviewed M214/P4 formulation and coordinate semantics",
            "Ramsey interpretation of the nine imported Boolean exclusions",
            "Python exact arithmetic, SHA-256, and ordinary hardware",
        ],
    }
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
