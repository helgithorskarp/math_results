#!/usr/bin/env python3
"""Produce compact rhombus-rank witnesses for the nine G_11 quotients."""
import argparse
import hashlib
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
Q = 11


def norm(v):
    return (v[0] * v[0] + v[1] * v[1]) % Q


def digest(value):
    raw = json.dumps(value, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def source_graph():
    vertices = [(x, y) for x in range(Q) for y in range(Q)]
    edges = []
    for u, v in combinations(range(len(vertices)), 2):
        a, b = vertices[u], vertices[v]
        if norm(((a[0] - b[0]) % Q, (a[1] - b[1]) % Q)) == 1:
            edges.append((u, v))
    return vertices, edges


def orthogonal_matrices():
    matrices = []
    for a in range(Q):
        for b in range(Q):
            for c in range(Q):
                for d in range(Q):
                    if ((a * a + c * c) % Q == 1 and
                            (b * b + d * d) % Q == 1 and
                            (a * b + c * d) % Q == 0):
                        matrices.append((a, b, c, d))
    return matrices


def apply_matrix(matrix, vector):
    a, b, c, d = matrix
    x, y = vector
    return ((a * x + b * y) % Q, (c * x + d * y) % Q)


def quotient(edges, identified):
    old_to_new = []
    roots = []
    labels = {}
    for old in range(Q * Q):
        root = 0 if old == identified else old
        if root not in labels:
            labels[root] = len(labels)
            roots.append(root)
        old_to_new.append(labels[root])
    quotient_edges = sorted({tuple(sorted((old_to_new[u], old_to_new[v])))
                             for u, v in edges})
    assert all(u != v for u, v in quotient_edges)
    return roots, old_to_new, quotient_edges


def cycles_and_basis(vertex_count, edges):
    adjacency = [set() for _ in range(vertex_count)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    # A key is the unordered pair of opposite vertex pairs.  It records one
    # integer equation e_a + e_c - e_b - e_d per four-cycle.
    witnesses = {}
    for a, c in combinations(range(vertex_count), 2):
        for b, d in combinations(sorted(adjacency[a] & adjacency[c]), 2):
            key = tuple(sorted(((a, c), (b, d))))
            witnesses.setdefault(key, (a, b, c, d))

    basis = {}
    selected = []
    for key in sorted(witnesses):
        cycle = witnesses[key]
        row = sum(1 << v for v in cycle)
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                selected.append(cycle)
                break
            row ^= basis[pivot]
    return len(witnesses), selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=HERE / "certificate.json")
    args = parser.parse_args()
    vertices, edges = source_graph()
    matrices = orthogonal_matrices()
    source_colours = json.loads(
        (HERE.parent / "hadwiger_nelson_finite_abelian_lifts" /
         "q11_five_colouring.json").read_text())
    representatives = {}
    for address, vector in enumerate(vertices[1:], 1):
        k = norm(vector)
        if k not in (0, 1):
            representatives.setdefault(k, (address, vector))
    assert sorted(representatives) == list(range(2, 11))

    cases = []
    for k in range(2, 11):
        address, vector = representatives[k]
        roots, old_to_new, quotient_edges = quotient(edges, address)
        equation_count, basis = cycles_and_basis(len(roots), quotient_edges)
        assert len(basis) == len(roots) - 1 == 119
        colour_matrix = next(matrix for matrix in matrices
                             if source_colours[apply_matrix(matrix, vector)[0] * Q +
                                               apply_matrix(matrix, vector)[1]] ==
                             source_colours[0])
        transformed = [source_colours[apply_matrix(colour_matrix, point)[0] * Q +
                                      apply_matrix(colour_matrix, point)[1]]
                       for point in vertices]
        assert transformed[0] == transformed[address]
        quotient_colours = [transformed[root] for root in roots]
        assert all(quotient_colours[old_to_new[u]] != quotient_colours[old_to_new[v]]
                   for u, v in edges)
        cases.append({
            "norm": k,
            "representative": list(vector),
            "identified_source_addresses": [0, address],
            "quotient_vertices": len(roots),
            "quotient_edges": len(quotient_edges),
            "rhombus_equations": equation_count,
            "rank_mod_2": len(basis),
            "basis_cycles": [list(cycle) for cycle in basis],
            "five_colouring_orthogonal_matrix": list(colour_matrix),
            "five_colouring": quotient_colours,
        })

    dependency_dir = HERE.parent / "hadwiger_nelson_finite_abelian_lifts"
    dependencies = {}
    for name in ("q11_four_unsat.drat", "q11_five_colouring.json"):
        dependencies[name] = hashlib.sha256((dependency_dir / name).read_bytes()).hexdigest()
    certificate = {
        "schema": "hn-g11-one-collision-rhombus-v1",
        "field_order": Q,
        "rank_prime": 2,
        "source_vertices": len(vertices),
        "source_edges": len(edges),
        "source_edge_sha256": digest(edges),
        "chromatic_dependency_sha256": dependencies,
        "cases": cases,
    }
    output = args.output
    output.write_text(json.dumps(certificate, indent=2) + "\n")
    print(json.dumps({
        "output": str(output),
        "cases": len(cases),
        "basis_cycles": sum(len(case["basis_cycles"]) for case in cases),
        "certificate_sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
