#!/usr/bin/env python3
"""Independent exact geometry and witness replay in SymPy's AlgebraicField.

This checker imports neither the primary verifier nor either sibling exact-field
implementation.  It reparses all coordinates, rebuilds every strict unit edge,
and independently decodes and checks every proper-colouring witness.
"""
from __future__ import annotations

import base64
import hashlib
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import sympy
from sympy import QQ, Rational, sqrt, sympify

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "hadwiger_nelson_parts509_criticality"
SWAP = ROOT / "hadwiger_nelson_parts509_swap_closure"
RADICALS = [sympy.Integer(1), sqrt(3), sqrt(5), sqrt(15), sqrt(11), sqrt(33), sqrt(55), sqrt(165)]
A_Q = (470, 523, 653, 619)
B_Q = (411, 750, 454, 417)
PAIR_Q = (523, 619)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def split_pair(body):
    expression = body.replace("Sqrt[", "sqrt(").replace("]", ")")
    depth = 0
    for i, character in enumerate(expression):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            return expression[:i], expression[i + 1 :]
    raise ValueError(body)


def main():
    cert = json.loads((HERE / "certificate.json").read_text())
    if cert["format"] != "parts509-g14-augmentation-v1":
        raise ValueError("unexpected certificate format")
    if sha256((BASE / "parts509.vtx").read_bytes()) != cert["parts_coordinate_sha256"]:
        raise ValueError("Parts coordinate hash mismatch")
    if sha256((SWAP / "completion_points.json").read_bytes()) != cert["completion_points_sha256"]:
        raise ValueError("completion list hash mismatch")

    field = QQ.algebraic_field(sqrt(3), sqrt(5), sqrt(11))
    basis = [field.from_sympy(radical) for radical in RADICALS]

    def expression_to_field(text):
        expression = sympy.expand(sympy.sqrtdenest(sympify(text)))
        result = field.zero
        for term, coefficient in expression.as_coefficients_dict().items():
            if term not in RADICALS or not coefficient.is_Rational:
                raise ValueError(f"unexpected denested term {term}: {coefficient}")
            result += field.from_sympy(Rational(coefficient)) * basis[RADICALS.index(term)]
        return result

    vertices = []
    for line in (BASE / "parts509.vtx").read_text().splitlines():
        if line.strip():
            x, y = split_pair(line.strip()[1:-1])
            vertices.append((expression_to_field(x), expression_to_field(y)))
    if len(vertices) != 509 or len(set(vertices)) != 509:
        raise ValueError("bad Parts coordinate set")

    completion_doc = json.loads((SWAP / "completion_points.json").read_text())

    def from_coefficients(values):
        result = field.zero
        for value, generator in zip(values, basis):
            rational = Fraction(value)
            result += field.from_sympy(Rational(rational.numerator, rational.denominator)) * generator
        return result

    qpoints = {}
    for qid in set(A_Q + B_Q):
        row = completion_doc["points"][qid]
        qpoints[qid] = from_coefficients(row["x"]), from_coefficients(row["y"])
    one = field.one

    def d2(a, b):
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

    def build(qids, drop=None):
        labels = [["V", v] for v in range(509) if v != drop] + [["Q3", q] for q in qids]
        points = [vertices[index] if kind == "V" else qpoints[index] for kind, index in labels]
        edges = [(u, v) for u in range(len(points)) for v in range(u + 1, len(points)) if d2(points[u], points[v]) == one]
        return labels, edges

    def edge_sha256(edges):
        return sha256("".join(f"{u} {v}\n" for u, v in edges).encode())

    def decode(record):
        raw = base64.b64decode(record["base64"], validate=True)
        if sha256(raw) != record["sha256"]:
            raise ValueError("payload hash mismatch")
        count = record["values_per_row"]
        width = (2 * count + 7) // 8
        if len(raw) != width * record["rows"]:
            raise ValueError("payload length mismatch")
        rows = []
        for r in range(record["rows"]):
            block = raw[r * width : (r + 1) * width]
            values = [(block[(2 * i) // 8] >> ((2 * i) % 8)) & 3 for i in range(count)]
            if (2 * count) % 8 and block[-1] >> ((2 * count) % 8):
                raise ValueError("nonzero padding")
            rows.append(values)
        return rows

    retained_checks = 0

    def check(name, qids, drop, deletion_key):
        nonlocal retained_checks
        record = cert[name]
        labels, edges = build(qids, drop)
        if (record["vertices"] != len(labels) or record["strict_edges"] != len(edges)
                or record["strict_edge_sha256"] != edge_sha256(edges)):
            raise ValueError(f"{name} graph mismatch")
        deletions = record[deletion_key]
        rows = decode(record["deletion_colorings"])
        if len(rows) != len(deletions):
            raise ValueError(f"{name} row mismatch")
        for deleted, row in zip(deletions, rows):
            color = []
            source = iter(row)
            for v in range(len(labels)):
                color.append(-1 if v == deleted else next(source))
            for u, v in edges:
                if deleted not in (u, v):
                    retained_checks += 1
                    if color[u] == color[v]:
                        raise ValueError(f"bad {name} witness at {deleted}")
        return len(labels), len(edges), len(rows)

    a_pair = check("A_pair", PAIR_Q, 350, "deletions")
    b_full = check("B_full", B_Q, None, "base_vertex_deletions_with_witnesses")

    # Independently replay the twelve colourable nodes in the four-point subset lattice.
    _, a_full_edges = build(A_Q)
    if cert["A_subset_profile"]["full_augmentation_edge_sha256"] != edge_sha256(a_full_edges):
        raise ValueError("A-full edge hash mismatch")
    subset_rows = cert["A_subset_profile"]["four_colorable_subsets"]
    seen_subsets = set()
    for row in subset_rows:
        subset = tuple(row["slots"])
        seen_subsets.add(subset)
        active = set(range(509)) - {350}
        active.update(509 + slot for slot in subset)
        colors = row["coloring_on_A_full_order"]
        if len(colors) != 513 or any((colors[v] == "-") != (v not in active) for v in range(513)):
            raise ValueError("bad A-subset activity mask")
        for u, v in a_full_edges:
            if u in active and v in active:
                retained_checks += 1
                if colors[u] == colors[v]:
                    raise ValueError("bad A-subset witness")
    expected_subsets = {subset for size in range(5) for subset in combinations(range(4), size)
                        if not (1 in subset and 3 in subset)}
    if seen_subsets != expected_subsets:
        raise ValueError("incomplete A-subset profile")
    for qid, point in sorted(qpoints.items()):
        fresh = [v for v, candidate in enumerate(vertices) if d2(point, candidate) == one]
        if fresh != completion_doc["points"][qid]["neighbors"]:
            raise ValueError(f"neighborhood mismatch at Q3[{qid}]")

    print(json.dumps({
        "independent_sympy_check": True,
        "A_pair": {"vertices": a_pair[0], "strict_edges": a_pair[1], "rows": a_pair[2]},
        "A_four_colorable_subsets": len(seen_subsets),
        "B_full": {"vertices": b_full[0], "strict_edges": b_full[1], "rows": b_full[2]},
        "retained_edge_checks": retained_checks,
        "completion_neighborhood_rescans": len(qpoints),
        "field": "SymPy AlgebraicField QQ(sqrt(3),sqrt(5),sqrt(11))",
    }, indent=2))


if __name__ == "__main__":
    main()
