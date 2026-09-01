#!/usr/bin/env python3
"""Independent exact replay of the pair-replacement classification.

This checker imports none of ``parts509.py``, ``kfield.py``, or the primary
classifier.  It parses the published coordinates into SymPy's AlgebraicField,
reconstructs every relevant strict unit-distance graph, rebuilds each CNF byte
for byte, and directly checks the three positive colouring witnesses.  When a
proof directory is supplied it also hashes every omitted DRAT file against the
compact certificate.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path

import sympy
from sympy import QQ, Rational, sqrt, sympify


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "hadwiger_nelson_parts509_criticality"
SWAP = ROOT / "hadwiger_nelson_parts509_swap_closure"
PAIR = ROOT / "hadwiger_nelson_parts509_pair_closure"
N = 509
K = 4
RADICALS = [
    sympy.Integer(1),
    sqrt(3),
    sqrt(5),
    sqrt(15),
    sqrt(11),
    sqrt(33),
    sqrt(55),
    sqrt(165),
]


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def split_pair(body: str):
    expression = body.replace("Sqrt[", "sqrt(").replace("]", ")")
    depth = 0
    for index, character in enumerate(expression):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            return expression[:index], expression[index + 1 :]
    raise ValueError(body)


def color_var(vertex: int, color: int) -> int:
    return K * vertex + color + 1


def triangle(edges):
    adjacency = [set() for _ in range(N)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    for a, b in edges:
        common = adjacency[a] & adjacency[b]
        if common:
            return a, b, min(common)
    raise ValueError("no triangle")


def dimacs_bytes(edges):
    clauses = []
    for vertex in range(N):
        clauses.append([color_var(vertex, color) for color in range(K)])
        for color, other in itertools.combinations(range(K), 2):
            clauses.append([-color_var(vertex, color), -color_var(vertex, other)])
    for a, b in edges:
        for color in range(K):
            clauses.append([-color_var(a, color), -color_var(b, color)])
    for color, vertex in enumerate(triangle(edges)):
        clauses.append([color_var(vertex, color)])
    output = [f"p cnf {N * K} {len(clauses)}\n"]
    output.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(output).encode("ascii")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--proof-dir", type=Path)
    args = parser.parse_args()

    field = QQ.algebraic_field(sqrt(3), sqrt(5), sqrt(11))
    expressions = []
    for line in (BASE / "parts509.vtx").read_text().splitlines():
        stripped = line.strip()
        if stripped:
            x, y = split_pair(stripped[1:-1])
            expressions.append((sympify(x), sympify(y)))
    points = [
        (field.from_sympy(sympy.sqrtdenest(x)), field.from_sympy(sympy.sqrtdenest(y)))
        for x, y in expressions
    ]
    if len(points) != N or len(set(points)) != N:
        raise ValueError("base-point count or distinctness failure")
    one = field.one

    def unit(p, q):
        dx = p[0] - q[0]
        dy = p[1] - q[1]
        return dx * dx + dy * dy == one

    base_edges = [(a, b) for a in range(N) for b in range(a + 1, N) if unit(points[a], points[b])]
    base_edge_hash = sha256_bytes("".join(f"{a} {b}\n" for a, b in base_edges).encode("ascii"))
    if len(base_edges) != 2442:
        raise ValueError(f"expected 2442 base unit pairs, found {len(base_edges)}")

    completion = json.loads((SWAP / "completion_points.json").read_text())

    def from_coefficients(strings):
        expression = sum(
            Rational(Fraction(value).numerator, Fraction(value).denominator) * radical
            for value, radical in zip(strings, RADICALS)
        )
        return field.from_sympy(expression)

    qpoints = [
        (from_coefficients(row["x"]), from_coefficients(row["y"]))
        for row in completion["points"]
    ]
    pair_certificate = json.loads((PAIR / "pair_certificate.json").read_text())
    candidates = pair_certificate["pairs_with_U_eq2"]
    used_q = sorted({q for row in candidates for q in row["A"]})
    qneighbors = {}
    for q in used_q:
        if qpoints[q] in points:
            raise ValueError(f"q={q} duplicates a base point")
        neighbors = tuple(v for v, point in enumerate(points) if unit(qpoints[q], point))
        if neighbors != tuple(completion["points"][q]["neighbors"]):
            raise ValueError(f"q={q} exact-neighbour mismatch")
        qneighbors[q] = neighbors

    certificate = json.loads(args.certificate.read_text())
    expected_hashes = {
        "base_coordinate_sha256": sha256_file(BASE / "parts509.vtx"),
        "completion_points_sha256": sha256_file(SWAP / "completion_points.json"),
        "pair_certificate_sha256": sha256_file(PAIR / "pair_certificate.json"),
        "base_edge_sha256": base_edge_hash,
    }
    for key, expected in expected_hashes.items():
        if certificate.get(key) != expected:
            raise ValueError(f"{key} mismatch")
    if len(candidates) != 63 or len(certificate.get("records", [])) != 63:
        raise ValueError("candidate count mismatch")

    colorable = certified = edge_checks = proof_bytes = 0
    for index, (candidate, record) in enumerate(zip(candidates, certificate["records"])):
        if record["index"] != index or record["A"] != candidate["A"] or record["U"] != candidate["U"]:
            raise ValueError(f"candidate metadata mismatch at {index}")
        q1, q2 = candidate["A"]
        deleted = set(candidate["U"])
        retained = [vertex for vertex in range(N) if vertex not in deleted]
        renumber = {vertex: new for new, vertex in enumerate(retained)}
        edges = [
            (renumber[a], renumber[b])
            for a, b in base_edges
            if a in renumber and b in renumber
        ]
        for offset, q in enumerate((q1, q2)):
            new_q = len(retained) + offset
            edges.extend((renumber[v], new_q) for v in qneighbors[q] if v in renumber)
        qq_edge = unit(qpoints[q1], qpoints[q2])
        if qq_edge:
            edges.append((len(retained), len(retained) + 1))
        edges = sorted((min(a, b), max(a, b)) for a, b in edges)
        if len(edges) != len(set(edges)) or len(edges) != record["edges"] or qq_edge != record["qq_edge"]:
            raise ValueError(f"candidate {index} edge reconstruction mismatch")
        if sha256_bytes(dimacs_bytes(edges)) != record["cnf_sha256"]:
            raise ValueError(f"candidate {index} CNF mismatch")

        if record["status"] == "4-colorable":
            coloring = [int(character) for character in record["coloring"]]
            if len(coloring) != N or any(coloring[a] == coloring[b] for a, b in edges):
                raise ValueError(f"candidate {index} invalid coloring")
            colorable += 1
            edge_checks += len(edges)
        elif record["status"] == "certified-not-4-colorable":
            certified += 1
            if args.proof_dir is not None:
                proof = args.proof_dir / f"candidate_{index:02d}.drat"
                if sha256_file(proof) != record["drat_proof_sha256"]:
                    raise ValueError(f"candidate {index} proof hash mismatch")
                if proof.stat().st_size != record["drat_proof_bytes"]:
                    raise ValueError(f"candidate {index} proof size mismatch")
                proof_bytes += proof.stat().st_size
        else:
            raise ValueError(f"candidate {index} unexpected status")

    if (colorable, certified) != (3, 60):
        raise ValueError("classification totals mismatch")
    if args.proof_dir is not None and proof_bytes != certificate["proof_summary"]["total_proof_bytes"]:
        raise ValueError("aggregate proof-byte count mismatch")
    print(
        f"all_checks=true base_unit_pairs={len(base_edges)} used_completion_points={len(used_q)} "
        f"candidates=63 colorable=3 certified_not_4_colorable=60"
    )
    print(
        f"coloring_edge_checks={edge_checks} proof_bytes_hashed={proof_bytes} "
        f"certificate_sha256={sha256_file(args.certificate)}"
    )


if __name__ == "__main__":
    main()
