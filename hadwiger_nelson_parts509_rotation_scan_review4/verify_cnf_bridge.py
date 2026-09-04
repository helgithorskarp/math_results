#!/usr/bin/env python3
"""Independently audit the two Parts-509 rotation four-colour CNF bridges."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
POINT_DIR = ROOT / "hadwiger_nelson_parts509_criticality"
TARGET_DIR = ROOT / "hadwiger_nelson_parts509_rotation_scan"
sys.path.insert(0, str(POINT_DIR))

from parts509 import build_edges, f_add, f_mul, f_sub, parse_points  # noqa: E402


N = 509
L_SIZE = 374
EXPECTED = {
    108: "b59275f43657f668d21b5fe9ca02488d57b2283d940c454fbdb4aa5617eff426",
    109: "e03f90aa72ae88cd03c85f7cf8db57aaa99ecd7c8df32caff4ef22326ae302fa",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(coefficients):
    return tuple(Fraction(text) for text in coefficients)


def rotate(point, c, s):
    x, y = point
    return (
        f_sub(f_mul(c, x), f_mul(s, y)),
        f_add(f_mul(s, x), f_mul(c, y)),
    )


def parse_dimacs(path: Path):
    header = None
    clauses = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            if header is not None:
                raise ValueError("duplicate DIMACS header")
            fields = line.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise ValueError("bad DIMACS header")
            header = int(fields[2]), int(fields[3])
            continue
        values = [int(text) for text in line.split()]
        if not values or values[-1] != 0 or any(value == 0 for value in values[:-1]):
            raise ValueError("bad DIMACS clause")
        clauses.append(values[:-1])
    if header is None or header[1] != len(clauses):
        raise ValueError("DIMACS clause count mismatch")
    if any(abs(literal) > header[0] for clause in clauses for literal in clause):
        raise ValueError("DIMACS literal exceeds declared variable range")
    return header, clauses


def audit(event_index: int, cnf_path: Path, points, strict, scan):
    record = scan["events"][event_index]
    edges = [(u, v) for u, v in strict if v < L_SIZE or u >= L_SIZE]
    edges += [tuple(edge) for edge in scan["invariant_cross_edges"]]
    edges += [tuple(edge) for edge in record["event_cross_edges"]]
    edges = sorted(edges)
    if len(edges) != 2442 or len(set(edges)) != 2442:
        raise ValueError(f"event {event_index} does not have 2442 distinct labeled edges")

    c, s = decode(record["cos"]), decode(record["sin"])
    union = set(points[:L_SIZE]) | {rotate(point, c, s) for point in points[L_SIZE:]}
    if len(union) != N or record["distinct_points"] != N:
        raise ValueError(f"event {event_index} does not have 509 distinct points")

    header, clauses = parse_dimacs(cnf_path)
    if header != (4 * N, N + 4 * len(edges) + 3):
        raise ValueError(f"event {event_index} has wrong DIMACS dimensions")
    vertex_clauses = [
        [4 * vertex + color + 1 for color in range(4)] for vertex in range(N)
    ]
    edge_clauses = [
        [-4 * u - color - 1, -4 * v - color - 1]
        for u, v in edges
        for color in range(4)
    ]
    if clauses[:N] != vertex_clauses:
        raise ValueError(f"event {event_index} vertex clauses differ")
    if clauses[N : N + 4 * len(edges)] != edge_clauses:
        raise ValueError(f"event {event_index} edge clauses differ")

    pins = clauses[-3:]
    if any(len(clause) != 1 or clause[0] <= 0 for clause in pins):
        raise ValueError(f"event {event_index} symmetry pins are not positive units")
    pin_data = [((clause[0] - 1) // 4, (clause[0] - 1) % 4) for clause in pins]
    vertices = [vertex for vertex, _color in pin_data]
    colors = [color for _vertex, color in pin_data]
    edge_set = set(edges)
    if colors != [0, 1, 2] or len(set(vertices)) != 3:
        raise ValueError(f"event {event_index} symmetry pins have the wrong colors")
    if any(
        (min(vertices[i], vertices[j]), max(vertices[i], vertices[j])) not in edge_set
        for i in range(3)
        for j in range(i + 1, 3)
    ):
        raise ValueError(f"event {event_index} symmetry pins do not lie on a triangle")
    digest = sha256(cnf_path)
    if digest != EXPECTED[event_index]:
        raise ValueError(f"event {event_index} CNF digest differs")
    return vertices, digest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("cnf108", type=Path)
    parser.add_argument("cnf109", type=Path)
    args = parser.parse_args()
    points = parse_points(POINT_DIR / "parts509.vtx")
    strict = build_edges(points)
    scan = json.loads((TARGET_DIR / "rotation_certificate.json").read_text())
    for event_index, path in ((108, args.cnf108), (109, args.cnf109)):
        triangle, digest = audit(event_index, path, points, strict, scan)
        print(
            f"event={event_index} vertices=509 edges=2442 distinct_points=509 "
            f"cnf_variables=2036 clauses=10280 triangle={triangle} sha256={digest}"
        )
    print("cnf_bridge_exact=true symmetry_breaking_sound=true")


if __name__ == "__main__":
    main()
