#!/usr/bin/env python3
"""Independent audit of the G14 augmentation four-colouring CNF bridge.

This standard-library checker imports none of the target's Python modules.  It
reconstructs the 510-vertex local graph from the canonical Parts edge list and
the two committed completion-point records, decides their mutual distance in
Q(sqrt(3),sqrt(5),sqrt(11)), and requires the CNF to be byte-semantically the
exact weak four-colouring encoding plus three sound triangle pins.
"""
from __future__ import annotations

import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


N = 509
DROP = 350
QIDS = (523, 619)
RADICANDS = (3, 5, 11)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_sha(edges: list[tuple[int, int]]) -> str:
    return hashlib.sha256("".join(f"{a} {b}\n" for a, b in edges).encode()).hexdigest()


def multiply(x: tuple[Fraction, ...], y: tuple[Fraction, ...]) -> tuple[Fraction, ...]:
    out = [Fraction(0)] * 8
    for i, a in enumerate(x):
        if not a:
            continue
        for j, b in enumerate(y):
            if not b:
                continue
            factor = 1
            for bit, radicand in enumerate(RADICANDS):
                if (i & j) & (1 << bit):
                    factor *= radicand
            out[i ^ j] += a * b * factor
    return tuple(out)


def q_unit(a: dict, b: dict) -> bool:
    ax, ay = (tuple(Fraction(c) for c in a[key]) for key in ("x", "y"))
    bx, by = (tuple(Fraction(c) for c in b[key]) for key in ("x", "y"))
    dx = tuple(x - y for x, y in zip(ax, bx))
    dy = tuple(x - y for x, y in zip(ay, by))
    sx, sy = multiply(dx, dx), multiply(dy, dy)
    return tuple(x + y for x, y in zip(sx, sy)) == (Fraction(1),) + (Fraction(0),) * 7


def read_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = declared_clauses = None
    clauses = []
    for line in path.read_text().splitlines():
        if not line or line.startswith("c"):
            continue
        fields = line.split()
        if fields[0] == "p":
            if variables is not None or fields[1] != "cnf" or len(fields) != 4:
                raise ValueError("bad or repeated DIMACS header")
            variables, declared_clauses = map(int, fields[2:])
            continue
        values = tuple(map(int, fields))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise ValueError("malformed DIMACS clause")
        clauses.append(values[:-1])
    if variables is None or len(clauses) != declared_clauses:
        raise ValueError("DIMACS count mismatch")
    return variables, clauses


def main() -> None:
    if len(sys.argv) not in (3, 4):
        raise SystemExit("usage: verify_cnf_bridge.py MATH_RESULTS CNF [DRAT]")
    root, cnf_path = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    proof_path = Path(sys.argv[3]).resolve() if len(sys.argv) == 4 else None
    target_dir = root / "hadwiger_nelson_parts509_g14_augmentation"
    base_dir = root / "hadwiger_nelson_parts509_criticality"
    completion_dir = root / "hadwiger_nelson_parts509_swap_closure"
    ambient_dir = root / "hadwiger_nelson_parts509_pair_closure"

    cert_path = target_dir / "certificate.json"
    manifest_path = target_dir / "proof_manifest.json"
    base_path = base_dir / "certificate.json"
    completion_path = completion_dir / "completion_points.json"
    cert = json.loads(cert_path.read_text())
    manifest = json.loads(manifest_path.read_text())
    base = json.loads(base_path.read_text())
    completion = json.loads(completion_path.read_text())
    ambient = json.loads((ambient_dir / "ambient_w3_edges.json").read_text())

    if sha256(base_dir / "parts509.vtx") != cert["parts_coordinate_sha256"]:
        raise ValueError("coordinate digest mismatch")
    if sha256(completion_path) != cert["completion_points_sha256"]:
        raise ValueError("completion-point digest mismatch")
    all_edges = [tuple(edge) for edge in ambient["edges"]]
    if all_edges != sorted(set(all_edges)):
        raise ValueError("ambient edge list is not canonical")
    base_edges = [(a, b) for a, b in all_edges if b < N]
    if edge_sha(base_edges) != base["edge_sha256"]:
        raise ValueError("Parts base-edge digest mismatch")

    labels = [("V", v) for v in range(N) if v != DROP] + [("Q3", q) for q in QIDS]
    if cert["A_pair"]["local_vertex_order"] != [[kind, index] for kind, index in labels]:
        raise ValueError("certificate local order mismatch")
    local = {label: i for i, label in enumerate(labels)}
    edges = []
    for a, b in base_edges:
        if DROP not in (a, b):
            edges.append(tuple(sorted((local[("V", a)], local[("V", b)]))))
    for q in QIDS:
        record = completion["points"][q]
        neighbors = record["neighbors"]
        if neighbors != sorted(set(neighbors)) or len(neighbors) < 3:
            raise ValueError("malformed completion neighborhood")
        for v in neighbors:
            if v != DROP:
                edges.append(tuple(sorted((local[("V", v)], local[("Q3", q)]))))
    q_records = [completion["points"][q] for q in QIDS]
    if q_unit(*q_records):
        edges.append((local[("Q3", QIDS[0])], local[("Q3", QIDS[1])]))
    edges = sorted(edges)
    if len(edges) != cert["A_pair"]["strict_edges"] or edge_sha(edges) != cert["A_pair"]["strict_edge_sha256"]:
        raise ValueError("independently assembled local graph mismatch")

    variables, clauses = read_cnf(cnf_path)
    expected = [tuple(4 * v + c + 1 for c in range(4)) for v in range(len(labels))]
    expected.extend((-4 * a - c - 1, -4 * b - c - 1) for a, b in edges for c in range(4))
    triangle = tuple(manifest["cnf"]["pinned_triangle"])
    edge_set = set(edges)
    if any(tuple(sorted(pair)) not in edge_set for pair in ((triangle[0], triangle[1]), (triangle[0], triangle[2]), (triangle[1], triangle[2]))):
        raise ValueError("pins do not lie on a triangle")
    expected.extend((4 * vertex + color + 1,) for color, vertex in enumerate(triangle))
    if variables != 4 * len(labels) or clauses != expected:
        raise ValueError("CNF is not the exact intended weak four-colouring encoding")
    if sha256(cnf_path) != manifest["cnf"]["sha256"] or cnf_path.stat().st_size != manifest["cnf"]["bytes"]:
        raise ValueError("CNF bytes differ from proof manifest")

    proof_checked = False
    if proof_path is not None:
        if sha256(proof_path) != manifest["proof"]["sha256"] or proof_path.stat().st_size != manifest["proof"]["bytes"]:
            raise ValueError("DRAT bytes differ from proof manifest")
        proof_checked = True

    print(json.dumps({
        "all_checks": True,
        "vertices": len(labels),
        "strict_edges": len(edges),
        "q3_pair_is_unit": q_unit(*q_records),
        "variables": variables,
        "clauses": len(clauses),
        "triangle": triangle,
        "cnf_sha256": sha256(cnf_path),
        "proof_bytes_match_manifest": proof_checked,
        "proof_sha256": sha256(proof_path) if proof_path else None,
        "certificate_sha256": sha256(cert_path),
    }, indent=2))


if __name__ == "__main__":
    main()
