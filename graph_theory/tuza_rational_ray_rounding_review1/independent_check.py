#!/usr/bin/env python3
"""Independent exact audit for the rational-ray triangle-packing package.

This checker intentionally imports no code from the reviewed directory.  It
reconstructs all three templates from their mathematical descriptions, treats
the submitted JSON only as untrusted certificate data, and exercises lift
orders not used by the submitted checker.
"""

from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from json import dumps, loads
from math import lcm
from pathlib import Path
import sys


EXPECTED_OPTIMA = {
    "reviewed_nine_vertex_seed": Fraction(11, 2),
    "three_type_boolean_template": Fraction(44, 3),
    "one_clique_type": Fraction(1, 6),
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def q(value):
    return Fraction(value)


def pair_kinds(triple):
    return [tuple(sorted(pair)) for pair in combinations(triple, 2)]


def reconstructed_specs():
    neighborhoods = [(0, 1, 2), (0, 1, 3), (0, 3), (1, 2, 3), (2, 3)]
    seed_edges = set(combinations(range(4), 2))
    seed_edges |= {
        tuple(sorted((vertex, 4 + index)))
        for index, neighborhood in enumerate(neighborhoods)
        for vertex in neighborhood
    }

    boolean_edges = set(combinations(range(8), 2))
    boolean_edges |= {
        (mask, 8 + bit)
        for bit in range(3)
        for mask in range(8)
        if (mask >> bit) & 1
    }
    return {
        "reviewed_nine_vertex_seed": (9, set(), seed_edges),
        "three_type_boolean_template": (11, set(range(8)), boolean_edges),
        "one_clique_type": (1, {0}, set()),
    }


def audit_profile(profile, expected):
    name = profile["name"]
    d, expected_loops, expected_edges = expected
    loops = set(profile["loops"])
    edges_list = [tuple(row) for row in profile["edges"]]
    edges = set(edges_list)
    require(profile["d"] == d, f"{name}: wrong number of types")
    require(loops == expected_loops, f"{name}: wrong loop support")
    require(len(edges) == len(edges_list) and edges == expected_edges,
            f"{name}: wrong or repeated cross-edge support")
    require(all(a < b for a, b in edges), f"{name}: noncanonical cross edge")

    kinds = edges | {(i, i) for i in loops}
    capacities = {edge: Fraction(1, 2) if edge[0] == edge[1] else Fraction(1)
                  for edge in kinds}
    triangles = [
        triple for triple in combinations_with_replacement(range(d), 3)
        if all(edge in kinds for edge in pair_kinds(triple))
    ]

    primal = {}
    for row in profile["primal"]:
        triple = tuple(row["types"])
        require(tuple(sorted(triple)) == triple and triple in triangles,
                f"{name}: invalid primal triangle")
        require(triple not in primal, f"{name}: repeated primal triangle")
        primal[triple] = q(row["weight"])
        require(primal[triple] >= 0, f"{name}: negative primal weight")

    dual = {}
    for row in profile["dual"]:
        edge = tuple(row["types"])
        require(tuple(sorted(edge)) == edge and edge in kinds,
                f"{name}: invalid dual edge")
        require(edge not in dual, f"{name}: repeated dual edge")
        dual[edge] = q(row["weight"])
        require(dual[edge] >= 0, f"{name}: negative dual weight")

    loads = Counter()
    for triple, weight in primal.items():
        for edge in pair_kinds(triple):
            loads[edge] += weight
    require(all(loads[edge] <= capacities[edge] for edge in kinds),
            f"{name}: primal capacity violation")
    require(all(sum(dual.get(edge, Fraction(0)) for edge in pair_kinds(triple)) >= 1
                for triple in triangles), f"{name}: uncovered dual constraint")

    primal_value = sum(primal.values(), Fraction(0))
    dual_value = sum((capacities[edge] * dual.get(edge, Fraction(0))
                      for edge in kinds), Fraction(0))
    expected_value = EXPECTED_OPTIMA[name]
    require(q(profile["optimum"]) == primal_value == dual_value == expected_value,
            f"{name}: primal/dual values do not match")

    # Independently compile only the packet invariants needed by Keevash's
    # lattice conditions.  Every component receives fresh vertices.
    denominator = lcm(*[value.denominator for value in
                        [*capacities.values(), *primal.values()]])
    packet_edge_counts = Counter()
    packet_degree_sums = Counter()
    triangle_components = 0
    spare_components = 0
    for triple, weight in primal.items():
        multiplicity = denominator * weight
        require(multiplicity.denominator == 1, f"{name}: nonintegral packet")
        for _ in range(int(multiplicity)):
            triangle_components += 1
            for edge in pair_kinds(triple):
                packet_edge_counts[edge] += 1
            for vertex_type in triple:
                packet_degree_sums[vertex_type] += 2
    for edge, capacity in capacities.items():
        multiplicity = denominator * (capacity - loads[edge])
        require(multiplicity.denominator == 1 and multiplicity >= 0,
                f"{name}: invalid spare-edge count")
        for _ in range(int(multiplicity)):
            spare_components += 1
            packet_edge_counts[edge] += 1
            packet_degree_sums[edge[0]] += 1
            packet_degree_sums[edge[1]] += 1
    require(all(packet_edge_counts[edge] == denominator * capacities[edge]
                for edge in kinds), f"{name}: packet edge-vector mismatch")
    for vertex_type in range(d):
        expected_degree = denominator * sum(
            capacity * (2 if edge[0] == edge[1] == vertex_type else 1)
            for edge, capacity in capacities.items() if vertex_type in edge
        )
        require(packet_degree_sums[vertex_type] == expected_degree,
                f"{name}: packet degree-vector mismatch")

    return {
        "denominator": denominator,
        "dual_value": str(dual_value),
        "edge_types": len(kinds),
        "packet_components": triangle_components + spare_components,
        "packet_spare_edges": spare_components,
        "primal_value": str(primal_value),
        "triangle_types_checked": len(triangles),
    }


def supported_graph_edges(d, loops, edges, scale, diagonal_deleted):
    kinds = edges | {(i, i) for i in loops}
    result = set()
    for left, right in combinations(range(d * scale), 2):
        kind = tuple(sorted((left // scale, right // scale)))
        if kind in kinds and (not diagonal_deleted or left % scale != right % scale):
            result.add((left, right))
    return result


def triangle_edges(triangle):
    return [tuple(sorted(pair)) for pair in combinations(triangle, 2)]


def check_packing(packing, graph_edges, vertex_count, exact_cover=False):
    used = set()
    for triangle in packing:
        require(len(triangle) == 3 and len(set(triangle)) == 3,
                "invalid literal triangle")
        require(all(type(vertex) is int and 0 <= vertex < vertex_count
                    for vertex in triangle), "literal vertex out of range")
        for edge in triangle_edges(triangle):
            require(edge in graph_edges, "literal triangle uses a nonedge")
            require(edge not in used, "literal packing repeats an edge")
            used.add(edge)
    if exact_cover:
        require(used == graph_edges, "literal decomposition does not cover the host")
    return len(used)


def latin_lift(base_packing, factor):
    return [
        [a * factor + i, b * factor + j, c * factor + ((i + j) % factor)]
        for a, b, c in base_packing
        for i in range(factor)
        for j in range(factor)
    ]


def xor_steiner_blocks(order):
    blocks = [
        triple for triple in combinations(range(order), 3)
        if (triple[0] + 1) ^ (triple[1] + 1) ^ (triple[2] + 1) == 0
    ]
    pairs = [pair for triple in blocks for pair in combinations(triple, 2)]
    require(len(pairs) == len(set(pairs)) == order * (order - 1) // 2,
            "order-63 XOR blocks are not a Steiner triple system")
    return blocks


def label_substitution(base_packing, order, blocks):
    return [
        [(vertex // 3) * order + block[vertex % 3] for vertex in triangle]
        for block in blocks
        for triangle in base_packing
    ]


def audit(path):
    raw = path.read_bytes()
    certificate = loads(raw)
    require(certificate.get("format") == 1, "unexpected certificate format")
    specs = reconstructed_specs()
    profiles = certificate["profiles"]
    require(len(profiles) == 3 and {p["name"] for p in profiles} == set(specs),
            "unexpected profile roster")
    by_name = {p["name"]: p for p in profiles}
    summaries = {name: audit_profile(by_name[name], specs[name]) for name in sorted(specs)}

    seed_d, seed_loops, seed_edges = specs["reviewed_nine_vertex_seed"]
    lift = certificate["independent_lift"]
    require(lift["profile"] == "reviewed_nine_vertex_seed" and lift["scale"] == 2,
            "unexpected seed lift metadata")
    base_seed_edges = supported_graph_edges(seed_d, seed_loops, seed_edges, 2, False)
    base_seed_used = check_packing(lift["packing"], base_seed_edges, 18)
    require(len(lift["packing"]) == 22 and base_seed_used == 66,
            "seed packing has wrong size")

    # Factor 21 gives scale 42, beyond the factors {1,2,3,5,8,15} exercised
    # by the submitted checker.
    factor = 21
    lifted_seed = latin_lift(lift["packing"], factor)
    lifted_scale = 2 * factor
    lifted_seed_edges = supported_graph_edges(
        seed_d, seed_loops, seed_edges, lifted_scale, False
    )
    lifted_seed_used = check_packing(
        lifted_seed, lifted_seed_edges, seed_d * lifted_scale
    )
    require(len(lifted_seed) == lifted_scale * lifted_scale * Fraction(11, 2),
            "scale-42 lift misses the exact fractional bound")

    boolean_d, boolean_loops, boolean_edges = specs["three_type_boolean_template"]
    diagonal = certificate["diagonal_decomposition"]
    require(diagonal["profile"] == "three_type_boolean_template" and
            diagonal["scale"] == 3, "unexpected Boolean decomposition metadata")
    j3_edges = supported_graph_edges(
        boolean_d, boolean_loops, boolean_edges, 3, True
    )
    j3_used = check_packing(diagonal["packing"], j3_edges, 33, exact_cover=True)
    require(len(diagonal["packing"]) == 88 and j3_used == 264,
            "order-three decomposition has wrong size")

    # The submitted checker stopped at order 31.  The projective binary STS
    # on the 63 nonzero vectors of F_2^6 supplies a larger independent test.
    order = 63
    blocks = xor_steiner_blocks(order)
    lifted_boolean = label_substitution(diagonal["packing"], order, blocks)
    j63_edges = supported_graph_edges(
        boolean_d, boolean_loops, boolean_edges, order, True
    )
    j63_used = check_packing(
        lifted_boolean, j63_edges, boolean_d * order, exact_cover=True
    )
    require(len(lifted_boolean) == 44 * order * (order - 1) // 3,
            "order-63 decomposition has wrong triangle count")

    return {
        "certificate_sha256": sha256(raw).hexdigest(),
        "finite_witnesses": {
            "boolean_J3": {
                "edges_covered": j3_used,
                "triangles": len(diagonal["packing"]),
            },
            "boolean_J63_new_test": {
                "edges_covered": j63_used,
                "steiner_blocks": len(blocks),
                "triangles": len(lifted_boolean),
                "vertices": boolean_d * order,
            },
            "seed_F2": {
                "edges_used": base_seed_used,
                "triangles": len(lift["packing"]),
            },
            "seed_F42_new_test": {
                "edges_used": lifted_seed_used,
                "factor": factor,
                "triangles": len(lifted_seed),
                "vertices": seed_d * lifted_scale,
            },
        },
        "profiles": summaries,
        "status": "PASS",
        "trust_boundary": (
            "Exact finite checks only. Keevash generalized partite decomposition, "
            "Kirkman existence at every admissible order, and the written asymptotic "
            "reduction are audited mathematically rather than proved by this program."
        ),
    }


if __name__ == "__main__":
    require(len(sys.argv) == 2, "usage: independent_check.py CERTIFICATES.json")
    print(dumps(audit(Path(sys.argv[1])), indent=2, sort_keys=True))
