#!/usr/bin/env python3
"""Independently verify all one-pair collision quotients of G_11.

Only exact Python integer arithmetic is used.  The producer is not imported.
"""
import argparse
import hashlib
import json
from itertools import combinations, product
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE_DIR = HERE.parent / "hadwiger_nelson_finite_abelian_lifts"
CERTIFICATE = HERE / "certificate.json"
EXPECTED = HERE / "EXPECTED.json"
Q = 11


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value):
    raw = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def quadratic_norm(v):
    x, y = v
    return (x * x + y * y) % Q


def reconstruct_source():
    vertices = [(x, y) for x in range(Q) for y in range(Q)]
    edges = []
    for u in range(len(vertices)):
        x, y = vertices[u]
        for v in range(u + 1, len(vertices)):
            X, Y = vertices[v]
            if ((x - X) ** 2 + (y - Y) ** 2) % Q == 1:
                edges.append((u, v))
    return vertices, edges


def orthogonal_matrices():
    matrices = []
    for a, b, c, d in product(range(Q), repeat=4):
        if ((a * a + c * c) % Q == 1 and
                (b * b + d * d) % Q == 1 and
                (a * b + c * d) % Q == 0):
            matrices.append((a, b, c, d))
    return matrices


def apply_matrix(matrix, vector):
    a, b, c, d = matrix
    x, y = vector
    return ((a * x + b * y) % Q, (c * x + d * y) % Q)


def make_quotient(source_edges, identified):
    classes = []
    class_index = {}
    mapping = []
    for vertex in range(Q * Q):
        canonical = 0 if vertex == identified else vertex
        if canonical not in class_index:
            class_index[canonical] = len(classes)
            classes.append(canonical)
        mapping.append(class_index[canonical])
    edges = set()
    for u, v in source_edges:
        a, b = mapping[u], mapping[v]
        require(a != b, "an adjacent pair was identified")
        edges.add((min(a, b), max(a, b)))
    edges = sorted(edges)
    # This is the quotient-map homomorphism check used by the chromatic bridge.
    require(all((min(mapping[u], mapping[v]), max(mapping[u], mapping[v])) in edges
                for u, v in source_edges), "quotient is not a graph homomorphic image")
    return classes, mapping, edges


def enumerate_rhombus_equations(vertex_count, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for u, v in edges:
        require(0 <= u < v < vertex_count, "bad quotient edge")
        adjacency[u].add(v)
        adjacency[v].add(u)
    equations = set()
    for a, c in combinations(range(vertex_count), 2):
        common = adjacency[a].intersection(adjacency[c])
        for b, d in combinations(common, 2):
            equations.add(tuple(sorted(((a, c), tuple(sorted((b, d)))))))
    return equations, adjacency


def rank_mod_2(rows):
    basis = {}
    for original in rows:
        require(type(original) is int and original >= 0, "bad binary row")
        row = original
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def check_case(case, expected_norm, vertices, source_edges, matrices):
    require(set(case) == {"norm", "representative", "identified_source_addresses",
                          "quotient_vertices", "quotient_edges", "rhombus_equations",
                          "rank_mod_2", "basis_cycles",
                          "five_colouring_orthogonal_matrix", "five_colouring"},
            "case fields")
    require(case["norm"] == expected_norm, "case order or norm")
    representative = case["representative"]
    require(isinstance(representative, list) and len(representative) == 2 and
            all(type(x) is int and 0 <= x < Q for x in representative),
            "representative format")
    representative = tuple(representative)
    require(quadratic_norm(representative) == expected_norm,
            "representative norm")
    address = representative[0] * Q + representative[1]
    require(case["identified_source_addresses"] == [0, address],
            "identified addresses")

    target_shell = {v for v in vertices if quadratic_norm(v) == expected_norm}
    orbit = {apply_matrix(matrix, representative) for matrix in matrices}
    require(orbit == target_shell and len(orbit) == 12,
            "orthogonal orbit does not cover norm shell")

    classes, mapping, quotient_edges = make_quotient(source_edges, address)
    require(len(classes) == case["quotient_vertices"] == 120, "quotient order")
    require(len(quotient_edges) == case["quotient_edges"], "quotient size")
    equations, adjacency = enumerate_rhombus_equations(len(classes), quotient_edges)
    require(len(equations) == case["rhombus_equations"], "rhombus equation count")

    cycles = case["basis_cycles"]
    require(isinstance(cycles, list) and len(cycles) == 119, "basis length")
    rows = []
    for cycle in cycles:
        require(isinstance(cycle, list) and len(cycle) == 4 and
                all(type(v) is int and 0 <= v < len(classes) for v in cycle) and
                len(set(cycle)) == 4, "cycle format")
        a, b, c, d = cycle
        require(b in adjacency[a] and c in adjacency[b] and
                d in adjacency[c] and a in adjacency[d], "claimed cycle is absent")
        require(tuple(sorted(((min(a, c), max(a, c)),
                              (min(b, d), max(b, d))))) in equations,
                "cycle equation is absent")
        rows.append(sum(1 << v for v in cycle))
    rank = rank_mod_2(rows)
    require(rank == case["rank_mod_2"] == len(classes) - 1,
            "rank witness")
    colour_matrix = case["five_colouring_orthogonal_matrix"]
    require(isinstance(colour_matrix, list) and len(colour_matrix) == 4 and
            tuple(colour_matrix) in matrices, "colouring matrix")
    colours = case["five_colouring"]
    require(isinstance(colours, list) and len(colours) == len(classes) and
            all(type(c) is int and 0 <= c < 5 for c in colours) and
            set(colours) == set(range(5)), "five-colouring format")
    require(all(colours[u] != colours[v] for u, v in quotient_edges),
            "improper quotient five-colouring")
    source_colours = json.loads((SOURCE_DIR / "q11_five_colouring.json").read_text())
    inherited = []
    for root in classes:
        image = apply_matrix(tuple(colour_matrix), vertices[root])
        inherited.append(source_colours[image[0] * Q + image[1]])
    require(colours == inherited and
            source_colours[0] == source_colours[
                apply_matrix(tuple(colour_matrix), representative)[0] * Q +
                apply_matrix(tuple(colour_matrix), representative)[1]],
            "five-colouring inheritance")
    return {
        "norm": expected_norm,
        "quotient_vertices": len(classes),
        "quotient_edges": len(quotient_edges),
        "rhombus_equations": len(equations),
        "basis_rank_mod_2": rank,
        "colours_used": len(set(colours)),
        "source_edges_mapped": len(source_edges),
    }


def run(certificate):
    require(set(certificate) == {"schema", "field_order", "rank_prime",
                                  "source_vertices", "source_edges",
                                  "source_edge_sha256", "chromatic_dependency_sha256",
                                  "cases"}, "certificate fields")
    require(certificate["schema"] == "hn-g11-one-collision-rhombus-v1",
            "schema")
    require(certificate["field_order"] == Q and certificate["rank_prime"] == 2,
            "field or rank prime")
    vertices, source_edges = reconstruct_source()
    require(len(vertices) == certificate["source_vertices"] == 121,
            "source order")
    require(len(source_edges) == certificate["source_edges"] == 726,
            "source size")
    require(digest(source_edges) == certificate["source_edge_sha256"],
            "source edge hash")

    dependencies = certificate["chromatic_dependency_sha256"]
    require(set(dependencies) == {"q11_four_unsat.drat", "q11_five_colouring.json"},
            "dependency fields")
    for name, expected in dependencies.items():
        require(type(expected) is str and len(expected) == 64 and
                sha256(SOURCE_DIR / name) == expected, "chromatic dependency hash")
    source_colours = json.loads((SOURCE_DIR / "q11_five_colouring.json").read_text())
    require(isinstance(source_colours, list) and len(source_colours) == 121 and
            all(type(c) is int and 0 <= c < 5 for c in source_colours) and
            set(source_colours) == set(range(5)) and
            all(source_colours[u] != source_colours[v] for u, v in source_edges),
            "imported source five-colouring")

    # Because -1 is not a square mod 11, x^2+y^2=0 only at zero.
    require({v for v in vertices if quadratic_norm(v) == 0} == {(0, 0)},
            "anisotropy")
    norm_sizes = {k: sum(quadratic_norm(v) == k for v in vertices)
                  for k in range(Q)}
    require(norm_sizes == {0: 1, 1: 12, 2: 12, 3: 12, 4: 12, 5: 12,
                           6: 12, 7: 12, 8: 12, 9: 12, 10: 12},
            "norm shell census")
    matrices = orthogonal_matrices()
    require(len(matrices) == 24, "orthogonal group order")
    for matrix in matrices:
        require(all(quadratic_norm(apply_matrix(matrix, v)) == quadratic_norm(v)
                    for v in vertices), "matrix is not norm preserving")

    cases = certificate["cases"]
    require(isinstance(cases, list) and len(cases) == 9, "case count")
    summaries = [check_case(case, k, vertices, source_edges, matrices)
                 for k, case in zip(range(2, 11), cases)]
    # The source has only norm-one edges; anisotropy and the nine transitive
    # nonzero norm shells therefore exhaust all allowed unordered collisions.
    result = {
        "verified": True,
        "source_graph": "G_11=Cay(F_11^2,{d:d.x^2+d.y^2=1})",
        "source_vertices": len(vertices),
        "source_edges": len(source_edges),
        "orthogonal_matrices": len(matrices),
        "nonadjacent_pair_orbits": len(summaries),
        "quotients_checked": len(summaries),
        "basis_cycles_checked": sum(x["basis_rank_mod_2"] for x in summaries),
        "all_rhombus_ranks": [x["basis_rank_mod_2"] for x in summaries],
        "quotient_edge_counts": [x["quotient_edges"] for x in summaries],
        "rhombus_equation_counts": [x["rhombus_equations"] for x in summaries],
        "injective_unit_distance_quotient_exists": False,
        "one_collision_family_excluded": True,
        "chromatic_lower_bound_imported_from_pinned_dependency": True,
        "all_quotients_have_verified_five_colourings": True,
        "all_quotient_chromatic_numbers": [5] * len(summaries),
        "record_improvement": False,
    }
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text())
    result = run(certificate)
    if args.check_expected:
        require(result == json.loads(EXPECTED.read_text()), "expected result mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
