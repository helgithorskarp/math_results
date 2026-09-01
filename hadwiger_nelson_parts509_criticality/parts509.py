#!/usr/bin/env python3
"""Exact geometry and coloring certificates for the Parts 509-vertex graph.

The geometry checker uses rational arithmetic in Q(sqrt(3), sqrt(5), sqrt(11)).
SymPy is used only while parsing and denesting the coordinate expressions.  Once
the coordinates are converted to the eight-element field basis, every equality
test is a comparison of tuples of fractions.

Commands:

  python parts509.py stats parts509.vtx
  python parts509.py generate parts509.vtx certificate.json
  python parts509.py verify parts509.vtx certificate.json
  python parts509.py cnf parts509.vtx /scratch/parts509-4col.cnf
  python parts509.py audit-cnf parts509.vtx reduced.json reduced.cnf

The ``generate`` command additionally needs python-sat.  ``cnf`` writes a DIMACS
encoding for 4-colorability with a sound triangle color-symmetry pin.  Solver
proofs and traces intentionally belong under /scratch, not in this repository.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

import sympy


PRIMES = (3, 5, 11)
PRIME_TO_BIT = {p: i for i, p in enumerate(PRIMES)}
ZERO = (Fraction(0),) * (1 << len(PRIMES))
ONE = (Fraction(1),) + (Fraction(0),) * ((1 << len(PRIMES)) - 1)
CERTIFICATE_FORMAT = "parts509-vertex-criticality-v1"
MAGIC_PACKING = "four 2-bit colors, low bits first, vertices in increasing order with the deleted vertex omitted"

FieldElement = tuple[Fraction, ...]
Point = tuple[FieldElement, FieldElement]
Edge = tuple[int, int]


def f_sub(x: FieldElement, y: FieldElement) -> FieldElement:
    return tuple(a - b for a, b in zip(x, y))


def f_mul(x: FieldElement, y: FieldElement) -> FieldElement:
    out = [Fraction(0)] * len(ZERO)
    for sx, a in enumerate(x):
        if not a:
            continue
        for sy, b in enumerate(y):
            if not b:
                continue
            common = sx & sy
            coefficient = a * b
            for bit, prime in enumerate(PRIMES):
                if common & (1 << bit):
                    coefficient *= prime
            out[sx ^ sy] += coefficient
    return tuple(out)


def f_sq(x: FieldElement) -> FieldElement:
    return f_mul(x, x)


def f_add(x: FieldElement, y: FieldElement) -> FieldElement:
    return tuple(a + b for a, b in zip(x, y))


def denest(expr: sympy.Expr) -> sympy.Expr:
    """Denest the only apparent nested radicals and expand radical products.

    In particular, SymPy turns

      sqrt((35 +/- 5*sqrt(33))/2) / 8

    into (sqrt(55) +/- sqrt(15)) / 16.  Thus all 509 coordinates lie in
    Q(sqrt(3), sqrt(5), sqrt(11)); no numerical root isolation is needed.
    """

    return sympy.sqrtdenest(expr).expand(power_base=True, force=True)


def to_field(expr: sympy.Expr) -> FieldElement:
    expr = sympy.expand(denest(expr))
    symbols = {p: sympy.Symbol(f"_r{p}") for p in PRIMES}

    def is_positive_integer_sqrt(node: sympy.Expr) -> bool:
        return bool(
            node.is_Pow
            and node.exp == sympy.Rational(1, 2)
            and node.base.is_Integer
            and node.base > 0
        )

    def split_sqrt(node: sympy.Expr) -> sympy.Expr:
        value = int(node.base)
        result = sympy.Integer(1)
        for prime, exponent in sympy.factorint(value).items():
            result *= sympy.Integer(prime) ** (exponent // 2)
            if exponent % 2:
                if prime not in symbols:
                    raise ValueError(f"coordinate uses unexpected sqrt({prime})")
                result *= symbols[prime]
        return result

    polynomial_expr = sympy.expand(expr.replace(is_positive_integer_sqrt, split_sqrt))
    polynomial = sympy.Poly(polynomial_expr, *(symbols[p] for p in PRIMES))
    out = [Fraction(0)] * len(ZERO)
    for monomial, coefficient in polynomial.terms():
        mask = 0
        for bit, exponent in enumerate(monomial):
            if exponent not in (0, 1):
                raise ValueError(f"unreduced radical power in {expr}: {monomial}")
            if exponent:
                mask |= 1 << bit
        rational = sympy.Rational(coefficient)
        out[mask] += Fraction(int(rational.p), int(rational.q))
    return tuple(out)


def split_coordinate_pair(body: str) -> tuple[str, str]:
    expression = body.replace("Sqrt[", "sqrt(").replace("]", ")")
    depth = 0
    for index, character in enumerate(expression):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            return expression[:index], expression[index + 1 :]
    raise ValueError(f"cannot split coordinate pair: {body}")


def parse_points(path: Path) -> list[Point]:
    points: list[Point] = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        if not (stripped.startswith("{") and stripped.endswith("}")):
            raise ValueError(f"line {line_number}: expected one Mathematica point")
        x_text, y_text = split_coordinate_pair(stripped[1:-1])
        x_expr = sympy.sympify(x_text)
        y_expr = sympy.sympify(y_text)
        points.append((to_field(x_expr), to_field(y_expr)))
    if len(set(points)) != len(points):
        raise ValueError("coordinate list contains duplicate points")
    return points


def squared_distance(a: Point, b: Point) -> FieldElement:
    dx = f_sub(a[0], b[0])
    dy = f_sub(a[1], b[1])
    return f_add(f_sq(dx), f_sq(dy))


def build_edges(points: Sequence[Point]) -> list[Edge]:
    return [
        (u, v)
        for u in range(len(points))
        for v in range(u + 1, len(points))
        if squared_distance(points[u], points[v]) == ONE
    ]


def edge_sha256(edges: Iterable[Edge]) -> str:
    digest = hashlib.sha256()
    for u, v in edges:
        digest.update(f"{u} {v}\n".encode())
    return digest.hexdigest()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def degrees(n: int, edges: Sequence[Edge]) -> list[int]:
    result = [0] * n
    for u, v in edges:
        result[u] += 1
        result[v] += 1
    return result


def adjacency(n: int, edges: Sequence[Edge]) -> list[set[int]]:
    result = [set() for _ in range(n)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def find_triangle(n: int, edges: Sequence[Edge]) -> tuple[int, int, int]:
    neighbors = adjacency(n, edges)
    for u, v in edges:
        common = neighbors[u] & neighbors[v]
        if common:
            return u, v, min(common)
    raise ValueError("graph has no triangle for color-symmetry breaking")


def triangle_avoiding(n: int, edges: Sequence[Edge], deleted: int) -> tuple[int, int, int]:
    neighbors = adjacency(n, edges)
    for u, v in edges:
        if u == deleted or v == deleted:
            continue
        common = neighbors[u] & neighbors[v]
        for w in sorted(common):
            if w != deleted:
                return u, v, w
    raise ValueError(f"G - {deleted} has no triangle for color-symmetry breaking")


def color_var(vertex: int, color: int, k: int) -> int:
    return vertex * k + color + 1


def coloring_clauses(n: int, edges: Sequence[Edge], k: int) -> list[list[int]]:
    """Equisatisfiable coloring CNF without redundant at-most-one clauses.

    Each vertex selects at least one color, and adjacent vertices have disjoint
    selected-color sets.  Choosing any selected color at each vertex yields an
    ordinary proper coloring, so the encoding is equivalent to k-colorability.
    """

    clauses = [[color_var(v, c, k) for c in range(k)] for v in range(n)]
    clauses.extend(
        [-color_var(u, c, k), -color_var(v, c, k)]
        for u, v in edges
        for c in range(k)
    )
    return clauses


def pinned_four_color_cnf(n: int, edges: Sequence[Edge]) -> tuple[list[list[int]], tuple[int, int, int]]:
    clauses = coloring_clauses(n, edges, 4)
    triangle = find_triangle(n, edges)
    for color, vertex in enumerate(triangle):
        clauses.append([color_var(vertex, color, 4)])
    return clauses, triangle


def write_dimacs(path: Path, variable_count: int, clauses: Sequence[Sequence[int]]) -> None:
    with path.open("w") as output:
        output.write(f"p cnf {variable_count} {len(clauses)}\n")
        for clause in clauses:
            output.write(" ".join(map(str, clause)))
            output.write(" 0\n")


def read_dimacs(path: Path) -> tuple[int, int, list[list[int]]]:
    variable_count = clause_count = None
    clauses: list[list[int]] = []
    pending: list[int] = []
    for line_number, line in enumerate(path.read_text().splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("c"):
            continue
        if stripped.startswith("p"):
            fields = stripped.split()
            if len(fields) != 4 or fields[:2] != ["p", "cnf"]:
                raise ValueError(f"line {line_number}: invalid DIMACS header")
            variable_count, clause_count = map(int, fields[2:])
            continue
        for field in stripped.split():
            literal = int(field)
            if literal:
                pending.append(literal)
            else:
                clauses.append(pending)
                pending = []
    if pending:
        raise ValueError("unterminated final DIMACS clause")
    if variable_count is None or clause_count is None:
        raise ValueError("missing DIMACS header")
    if clause_count != len(clauses):
        raise ValueError(f"DIMACS declares {clause_count} clauses but contains {len(clauses)}")
    if any(abs(literal) > variable_count for clause in clauses for literal in clause):
        raise ValueError("DIMACS literal exceeds declared variable count")
    return variable_count, clause_count, clauses


def validate_coloring(n: int, edges: Sequence[Edge], colors: Sequence[int], k: int, deleted: int | None = None) -> None:
    if len(colors) != n:
        raise ValueError(f"expected {n} colors, got {len(colors)}")
    for vertex, color in enumerate(colors):
        if vertex == deleted:
            if color != -1:
                raise ValueError(f"deleted vertex {deleted} is not marked -1")
        elif not 0 <= color < k:
            raise ValueError(f"vertex {vertex} has invalid color {color}")
    for u, v in edges:
        if u != deleted and v != deleted and colors[u] == colors[v]:
            raise ValueError(f"monochromatic edge {(u, v)} in deletion {deleted}")


def model_to_coloring(model: Sequence[int], n: int, k: int, deleted: int | None = None) -> list[int]:
    positive = {literal for literal in model if literal > 0}
    colors = []
    for vertex in range(n):
        if vertex == deleted:
            colors.append(-1)
            continue
        selected = [color for color in range(k) if color_var(vertex, color, k) in positive]
        if not selected:
            raise ValueError(f"solver model assigns no color to vertex {vertex}")
        colors.append(selected[0])
    return colors


def solve_coloring(
    n: int,
    edges: Sequence[Edge],
    k: int,
    solver_name: str,
    symmetry_pin: bool = False,
) -> list[int] | None:
    from pysat.solvers import Solver

    clauses = coloring_clauses(n, edges, k)
    if symmetry_pin:
        for color, vertex in enumerate(find_triangle(n, edges)):
            clauses.append([color_var(vertex, color, k)])
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        if not solver.solve():
            return None
        colors = model_to_coloring(solver.get_model(), n, k)
    validate_coloring(n, edges, colors, k)
    return colors


def deletion_colorings(n: int, edges: Sequence[Edge], solver_name: str) -> list[list[int]]:
    """Solve every one-vertex deletion through one activation-variable CNF."""

    from pysat.solvers import Solver

    k = 4
    active_offset = n * k

    def active(vertex: int) -> int:
        return active_offset + vertex + 1

    clauses: list[list[int]] = []
    for vertex in range(n):
        clauses.append([-active(vertex)] + [color_var(vertex, c, k) for c in range(k)])
    for u, v in edges:
        for color in range(k):
            clauses.append(
                [
                    -active(u),
                    -active(v),
                    -color_var(u, color, k),
                    -color_var(v, color, k),
                ]
            )

    rows: list[list[int]] = []
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        for deleted in range(n):
            assumptions = [active(v) if v != deleted else -active(v) for v in range(n)]
            for color, vertex in enumerate(triangle_avoiding(n, edges, deleted)):
                assumptions.append(color_var(vertex, color, k))
            if not solver.solve(assumptions=assumptions):
                raise RuntimeError(f"G - {deleted} is not 4-colorable")
            colors = model_to_coloring(solver.get_model(), n, k, deleted)
            validate_coloring(n, edges, colors, k, deleted)
            rows.append(colors)
    return rows


def pack_deletion_rows(rows: Sequence[Sequence[int]]) -> bytes:
    output = bytearray()
    for deleted, row in enumerate(rows):
        values = [color for vertex, color in enumerate(row) if vertex != deleted]
        if any(not 0 <= color < 4 for color in values):
            raise ValueError(f"invalid row {deleted}")
        if len(values) % 4:
            raise ValueError("packing format requires the retained order to be divisible by four")
        for start in range(0, len(values), 4):
            output.append(sum(values[start + shift] << (2 * shift) for shift in range(4)))
    return bytes(output)


def unpack_deletion_rows(data: bytes, n: int) -> list[list[int]]:
    retained = n - 1
    if retained % 4:
        raise ValueError("packing format requires n-1 divisible by four")
    row_bytes = retained // 4
    if len(data) != n * row_bytes:
        raise ValueError(f"packed witness has {len(data)} bytes, expected {n * row_bytes}")
    rows = []
    for deleted in range(n):
        block = data[deleted * row_bytes : (deleted + 1) * row_bytes]
        values = [(byte >> shift) & 3 for byte in block for shift in (0, 2, 4, 6)]
        row = []
        iterator = iter(values)
        for vertex in range(n):
            row.append(-1 if vertex == deleted else next(iterator))
        rows.append(row)
    return rows


def graph_summary(n: int, edges: Sequence[Edge]) -> dict[str, object]:
    degree_values = degrees(n, edges)
    histogram = {str(k): v for k, v in sorted(Counter(degree_values).items())}
    return {
        "vertices": n,
        "edges": len(edges),
        "edge_sha256": edge_sha256(edges),
        "minimum_degree": min(degree_values),
        "maximum_degree": max(degree_values),
        "degree_histogram": histogram,
        "triangle_pin": list(find_triangle(n, edges)),
    }


def load_graph(vtx_path: Path) -> tuple[list[Point], list[Edge]]:
    points = parse_points(vtx_path)
    edges = build_edges(points)
    return points, edges


def command_stats(vtx_path: Path) -> None:
    points, edges = load_graph(vtx_path)
    summary = graph_summary(len(points), edges)
    summary["coordinate_sha256"] = file_sha256(vtx_path)
    summary["exact_field"] = "Q(sqrt(3), sqrt(5), sqrt(11))"
    print(json.dumps(summary, indent=2, sort_keys=True))


def command_cnf(vtx_path: Path, cnf_path: Path) -> None:
    points, edges = load_graph(vtx_path)
    clauses, triangle = pinned_four_color_cnf(len(points), edges)
    write_dimacs(cnf_path, 4 * len(points), clauses)
    print(
        json.dumps(
            {
                "cnf": str(cnf_path),
                "variables": 4 * len(points),
                "clauses": len(clauses),
                "triangle_pin": list(triangle),
                "cnf_sha256": file_sha256(cnf_path),
                **graph_summary(len(points), edges),
            },
            indent=2,
            sort_keys=True,
        )
    )


def command_audit_cnf(vtx_path: Path, edge_json_path: Path, cnf_path: Path) -> None:
    """Audit an externally supplied reduced-graph coloring CNF.

    This is the bridge needed before a DRAT check: every reduced edge must be an
    exact unit pair from the coordinates, and every non-pin clause must be exactly
    the standard at-least-one/binary-edge 4-coloring encoding.  The three unit
    clauses must pin distinct colors on a triangle, which preserves satisfiability.
    """

    points, full_edges = load_graph(vtx_path)
    n = len(points)
    document = json.loads(edge_json_path.read_text())
    reduced_edges = [tuple(map(int, edge)) for edge in document["edges"]]
    if len(set(reduced_edges)) != len(reduced_edges):
        raise ValueError("reduced edge list contains duplicates")
    if any(not (0 <= u < v < n) for u, v in reduced_edges):
        raise ValueError("reduced edge list contains a malformed edge")
    if not set(reduced_edges) <= set(full_edges):
        raise ValueError("reduced graph contains a non-unit edge")

    variable_count, clause_count, clauses = read_dimacs(cnf_path)
    if variable_count != 4 * n:
        raise ValueError(f"expected {4 * n} DIMACS variables, got {variable_count}")
    unit_clauses = [clause for clause in clauses if len(clause) == 1]
    nonunit_clauses = [clause for clause in clauses if len(clause) != 1]
    if len(unit_clauses) != 3 or any(clause[0] <= 0 for clause in unit_clauses):
        raise ValueError("expected exactly three positive unit pin clauses")

    pins = []
    for (literal,) in unit_clauses:
        zero_based = literal - 1
        pins.append((zero_based // 4, zero_based % 4))
    pin_vertices = [vertex for vertex, _ in pins]
    pin_colors = [color for _, color in pins]
    reduced_set = set(reduced_edges)
    if len(set(pin_vertices)) != 3 or len(set(pin_colors)) != 3:
        raise ValueError("pin clauses do not use three distinct vertices and colors")
    if any(
        tuple(sorted((pin_vertices[i], pin_vertices[j]))) not in reduced_set
        for i in range(3)
        for j in range(i + 1, 3)
    ):
        raise ValueError("pin vertices do not form a triangle in the reduced graph")

    expected = coloring_clauses(n, reduced_edges, 4)
    normalize = lambda clause: tuple(sorted(clause))
    if Counter(map(normalize, nonunit_clauses)) != Counter(map(normalize, expected)):
        raise ValueError("non-pin DIMACS clauses do not exactly match the reduced graph")

    print(
        json.dumps(
            {
                "all_checks": True,
                "coordinate_sha256": file_sha256(vtx_path),
                "full_unit_edges": len(full_edges),
                "full_edge_sha256": edge_sha256(full_edges),
                "reduced_edges": len(reduced_edges),
                "reduced_edge_sha256": edge_sha256(reduced_edges),
                "cnf_variables": variable_count,
                "cnf_clauses": clause_count,
                "cnf_sha256": file_sha256(cnf_path),
                "sound_triangle_pins": pins,
                "next_step": "Run a proof checker such as drat-trim on this audited CNF and its DRAT file.",
            },
            indent=2,
            sort_keys=True,
        )
    )


def command_generate(vtx_path: Path, certificate_path: Path, solver_name: str) -> None:
    points, edges = load_graph(vtx_path)
    n = len(points)
    four = solve_coloring(n, edges, 4, solver_name, symmetry_pin=True)
    if four is not None:
        raise RuntimeError("the full graph is 4-colorable")
    five = solve_coloring(n, edges, 5, solver_name)
    if five is None:
        raise RuntimeError("the full graph is not 5-colorable")
    rows = deletion_colorings(n, edges, solver_name)
    neighbors = adjacency(n, edges)
    missing_neighbor_colors = [
        deleted
        for deleted, row in enumerate(rows)
        if {row[vertex] for vertex in neighbors[deleted]} != {0, 1, 2, 3}
    ]
    if missing_neighbor_colors:
        raise RuntimeError(
            "a deletion witness can extend to the full graph: "
            f"{missing_neighbor_colors[:5]}"
        )
    packed = pack_deletion_rows(rows)
    certificate = {
        "format": CERTIFICATE_FORMAT,
        "coordinate_sha256": file_sha256(vtx_path),
        "exact_field": "Q(sqrt(3), sqrt(5), sqrt(11))",
        **graph_summary(n, edges),
        "claim": "The strict unit-distance graph is 5-chromatic and deleting any one vertex makes it 4-colorable.",
        "full_graph_four_color_solver_result": "UNSAT",
        "solver_used_only_to_generate_witnesses": solver_name,
        "five_coloring": "".join(map(str, five)),
        "deletion_row_packing": MAGIC_PACKING,
        "deletion_colorings_base64": base64.b64encode(packed).decode("ascii"),
        "packed_deletion_colorings_sha256": hashlib.sha256(packed).hexdigest(),
    }
    certificate_path.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(
        json.dumps(
            {
                "certificate": str(certificate_path),
                "certificate_sha256": file_sha256(certificate_path),
                "packed_bytes": len(packed),
                "deletion_witnesses": len(rows),
                "neighbor_color_surjectivity_checks": n,
                **graph_summary(n, edges),
            },
            indent=2,
            sort_keys=True,
        )
    )


def command_verify(vtx_path: Path, certificate_path: Path) -> None:
    points, edges = load_graph(vtx_path)
    n = len(points)
    certificate = json.loads(certificate_path.read_text())
    expected = graph_summary(n, edges)
    if certificate.get("format") != CERTIFICATE_FORMAT:
        raise ValueError("unknown certificate format")
    if certificate.get("coordinate_sha256") != file_sha256(vtx_path):
        raise ValueError("coordinate file hash mismatch")
    for key, value in expected.items():
        if certificate.get(key) != value:
            raise ValueError(f"certificate {key} mismatch")

    five = [int(value) for value in certificate["five_coloring"]]
    validate_coloring(n, edges, five, 5)
    packed = base64.b64decode(certificate["deletion_colorings_base64"], validate=True)
    if hashlib.sha256(packed).hexdigest() != certificate["packed_deletion_colorings_sha256"]:
        raise ValueError("packed deletion witness hash mismatch")
    rows = unpack_deletion_rows(packed, n)
    neighbors = adjacency(n, edges)
    for deleted, row in enumerate(rows):
        validate_coloring(n, edges, row, 4, deleted)
        if {row[vertex] for vertex in neighbors[deleted]} != {0, 1, 2, 3}:
            raise ValueError(f"neighbors of deleted vertex {deleted} do not use all colors")

    print(
        json.dumps(
            {
                "all_checks": True,
                "certificate_sha256": file_sha256(certificate_path),
                "coordinate_sha256": file_sha256(vtx_path),
                "exact_unit_distance_pairs": len(edges),
                "edge_sha256": edge_sha256(edges),
                "five_coloring_verified": True,
                "deletion_colorings_verified": len(rows),
                "neighbor_color_surjectivity_checks": n,
                "trust_boundary": "This command verifies geometry and SAT witnesses exactly; full-graph non-4-colorability requires the separately checked UNSAT proof or a trusted SAT solve.",
            },
            indent=2,
            sort_keys=True,
        )
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    stats = subparsers.add_parser("stats")
    stats.add_argument("vtx", type=Path)

    generate = subparsers.add_parser("generate")
    generate.add_argument("vtx", type=Path)
    generate.add_argument("certificate", type=Path)
    generate.add_argument("--solver", default="cadical195")

    verify = subparsers.add_parser("verify")
    verify.add_argument("vtx", type=Path)
    verify.add_argument("certificate", type=Path)

    cnf = subparsers.add_parser("cnf")
    cnf.add_argument("vtx", type=Path)
    cnf.add_argument("output", type=Path)

    audit_cnf = subparsers.add_parser("audit-cnf")
    audit_cnf.add_argument("vtx", type=Path)
    audit_cnf.add_argument("edge_json", type=Path)
    audit_cnf.add_argument("cnf", type=Path)
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    if arguments.command == "stats":
        command_stats(arguments.vtx)
    elif arguments.command == "generate":
        command_generate(arguments.vtx, arguments.certificate, arguments.solver)
    elif arguments.command == "verify":
        command_verify(arguments.vtx, arguments.certificate)
    elif arguments.command == "cnf":
        command_cnf(arguments.vtx, arguments.output)
    elif arguments.command == "audit-cnf":
        command_audit_cnf(arguments.vtx, arguments.edge_json, arguments.cnf)
    else:
        raise AssertionError(arguments.command)


if __name__ == "__main__":
    main()
