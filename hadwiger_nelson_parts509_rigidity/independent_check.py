#!/usr/bin/env python3
"""Independent SymPy sparse-matrix check of the Parts-509 rigidity claim.

This checker does not import rigidity_certificate.py or the sibling exact-field
implementation.  It parses the coordinate expressions directly, specializes
them modulo 131, and uses SymPy DomainMatrix rather than FLINT matrices.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter
from pathlib import Path

import sympy
from sympy.polys.domains import GF
from sympy.polys.matrices import DomainMatrix


P = 131
ROOTS = {3: 38, 5: 23, 11: 50}
N = 509
EXPECTED_COORDINATE_SHA256 = (
    "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5"
)
EXPECTED_RAW_EDGE_SHA256 = (
    "2308fe8a798113e1c3bee9b571ed21875c44997a9916712bd76b6983f24861c8"
)
EXPECTED_EDGE_SHA256 = (
    "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_int_lines(values: list[int] | tuple[int, ...]) -> str:
    return hashlib.sha256("".join(f"{value}\n" for value in values).encode()).hexdigest()


def sha256_coordinate_lines(coords: list[tuple[int, int]]) -> str:
    return hashlib.sha256(
        "".join(f"{x} {y}\n" for x, y in coords).encode()
    ).hexdigest()


def canonical_edge_sha256(edges: list[tuple[int, int]]) -> str:
    return hashlib.sha256(
        "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode()
    ).hexdigest()


def split_pair(body: str) -> tuple[str, str]:
    text = body.replace("Sqrt[", "sqrt(").replace("]", ")")
    depth = 0
    for index, character in enumerate(text):
        if character == "(":
            depth += 1
        elif character == ")":
            depth -= 1
        elif character == "," and depth == 0:
            return text[:index], text[index + 1 :]
    raise ValueError(f"cannot split coordinate pair {body!r}")


def sqrt_value(node: sympy.Expr) -> sympy.Integer:
    value = int(node.base)
    result = 1
    for prime, exponent in sympy.factorint(value).items():
        result *= prime ** (exponent // 2)
        if exponent % 2:
            if prime not in ROOTS:
                raise ValueError(f"unexpected sqrt({prime})")
            result *= ROOTS[prime]
    return sympy.Integer(result)


def is_integer_sqrt(node: sympy.Expr) -> bool:
    return bool(
        node.is_Pow
        and node.exp == sympy.Rational(1, 2)
        and node.base.is_Integer
        and node.base > 0
    )


def expression_mod(text: str) -> int:
    expression = sympy.sympify(text)
    expression = sympy.sqrtdenest(expression).expand(power_base=True, force=True)
    rational = sympy.cancel(expression.replace(is_integer_sqrt, sqrt_value))
    if not rational.is_Rational:
        raise ValueError(f"modular evaluation left a non-rational expression: {rational}")
    numerator, denominator = map(int, sympy.fraction(rational))
    if denominator % P == 0:
        raise ValueError("coordinate denominator vanishes modulo 131")
    return numerator % P * pow(denominator % P, -1, P) % P


def load_coordinates(path: Path) -> list[tuple[int, int]]:
    coords: list[tuple[int, int]] = []
    for line_number, raw in enumerate(path.read_text().splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        if not (line.startswith("{") and line.endswith("}")):
            raise ValueError(f"line {line_number}: malformed coordinate")
        x_text, y_text = split_pair(line[1:-1])
        coords.append((expression_mod(x_text), expression_mod(y_text)))
    if len(coords) != N:
        raise ValueError(f"expected {N} points, found {len(coords)}")
    return coords


def load_edges(path: Path) -> list[tuple[int, int]]:
    if sha256_file(path) != EXPECTED_RAW_EDGE_SHA256:
        raise ValueError("unexpected raw edge input")
    raw = json.loads(path.read_text())
    edges = [tuple(map(int, edge)) for edge in raw]
    if len(edges) != 2442 or len(set(edges)) != 2442:
        raise ValueError("expected 2,442 distinct edges")
    if any(not (0 <= u < v < N) for u, v in edges):
        raise ValueError("edge is not canonical or is out of range")
    if canonical_edge_sha256(edges) != EXPECTED_EDGE_SHA256:
        raise ValueError("unexpected canonical edge list")
    return sorted(edges)


def build_matrix(
    coords: list[tuple[int, int]], edges: list[tuple[int, int]]
) -> DomainMatrix:
    entries: dict[int, dict[int, int]] = {}
    for row, (u, v) in enumerate(edges):
        dx = (coords[u][0] - coords[v][0]) % P
        dy = (coords[u][1] - coords[v][1]) % P
        if (dx * dx + dy * dy) % P != 1:
            raise ValueError(f"edge {(u, v)} is not unit after specialization")
        row_entries = {
            2 * u: dx,
            2 * u + 1: dy,
            2 * v: (-dx) % P,
            2 * v + 1: (-dy) % P,
        }
        entries[row] = {column: value for column, value in row_entries.items() if value}
    return DomainMatrix.from_dict_sympy(len(edges), 2 * N, entries).convert_to(GF(P))


def compute(coordinate_path: Path, edge_path: Path) -> dict[str, object]:
    started = time.monotonic()
    if sha256_file(coordinate_path) != EXPECTED_COORDINATE_SHA256:
        raise ValueError("unexpected coordinate input")
    if any(root * root % P != radicand for radicand, root in ROOTS.items()):
        raise AssertionError("invalid square-root specialization")
    coords = load_coordinates(coordinate_path)
    edges = load_edges(edge_path)
    matrix = build_matrix(coords, edges)
    rank = matrix.rank()
    maximum_rank = 2 * N - 3
    if rank != maximum_rank:
        raise ValueError(f"rigidity rank is {rank}, expected {maximum_rank}")

    _, basis_edges = matrix.transpose().rref()
    if len(basis_edges) != rank:
        raise ValueError("wrong row-basis size")
    basis = matrix.extract(list(basis_edges), list(range(matrix.shape[1])))
    _, coordinate_pivots = basis.rref()
    if len(coordinate_pivots) != rank:
        raise ValueError("wrong coordinate-pivot count")
    omitted_columns = sorted(set(range(matrix.shape[1])) - set(coordinate_pivots))
    minor = basis.extract(list(range(rank)), list(coordinate_pivots))
    inverse = minor.inv()
    basis_set = set(basis_edges)
    nonbasis_edges = [i for i in range(matrix.shape[0]) if i not in basis_set]
    coefficients = matrix.extract(nonbasis_edges, list(coordinate_pivots)) * inverse
    coefficient_rows = coefficients.to_list()

    supports: list[int] = []
    normalized_columns: list[tuple[int, ...]] = []
    normalized_digest = hashlib.sha256()
    for column in range(rank):
        values = tuple(
            int(coefficient_rows[row][column]) % P for row in range(len(nonbasis_edges))
        )
        support = sum(value != 0 for value in values)
        if support == 0:
            raise ValueError("zero coefficient column")
        scale = pow(next(value for value in values if value), -1, P)
        normalized = tuple(value * scale % P for value in values)
        supports.append(support)
        normalized_columns.append(normalized)
        for value in normalized:
            normalized_digest.update(value.to_bytes(4, "little"))
    if min(supports) < 2 or len(set(normalized_columns)) != rank:
        raise ValueError("two-edge redundancy checks failed")

    incident: list[list[int]] = [[] for _ in range(N)]
    for edge_index, (u, v) in enumerate(edges):
        incident[u].append(edge_index)
        incident[v].append(edge_index)
    basis_position = {edge_index: i for i, edge_index in enumerate(basis_edges)}
    nonbasis_position = {edge_index: i for i, edge_index in enumerate(nonbasis_edges)}
    vertex_deletion_ranks: list[int] = []
    for vertex in range(N):
        removed = set(incident[vertex])
        missing_basis = [basis_position[i] for i in removed if i in basis_position]
        retained_nonbasis = [
            nonbasis_position[i] for i in nonbasis_edges if i not in removed
        ]
        entries: dict[int, dict[int, int]] = {}
        for row_index, coefficient_row in enumerate(retained_nonbasis):
            values = {
                column_index: int(coefficient_rows[coefficient_row][basis_column]) % P
                for column_index, basis_column in enumerate(missing_basis)
            }
            values = {column: value for column, value in values.items() if value}
            if values:
                entries[row_index] = values
        projected = DomainMatrix.from_dict_sympy(
            len(retained_nonbasis), len(missing_basis), entries
        ).convert_to(GF(P))
        vertex_deletion_ranks.append(rank - len(missing_basis) + projected.rank())
    if set(vertex_deletion_ranks) != {2 * (N - 1) - 3}:
        raise ValueError("not every vertex deletion is rigid")

    sharp_vertex = 310
    sharp_deleted = incident[sharp_vertex][:3]
    sharp_deleted_set = set(sharp_deleted)
    retained_rows = [
        row for row in range(matrix.shape[0]) if row not in sharp_deleted_set
    ]
    sharp_rank = matrix.extract(retained_rows, list(range(matrix.shape[1]))).rank()
    if sharp_rank != maximum_rank - 1:
        raise ValueError("sharp deletion has unexpected rank")

    return {
        "prime": P,
        "square_roots_of_3_5_11": [ROOTS[p] for p in (3, 5, 11)],
        "modular_coordinates_sha256": sha256_coordinate_lines(coords),
        "rigidity_matrix_rows": len(edges),
        "rigidity_matrix_columns": 2 * N,
        "rank": rank,
        "maximum_rank": maximum_rank,
        "row_basis_size": len(basis_edges),
        "row_basis_edge_indices_sha256": sha256_int_lines(basis_edges),
        "row_basis_first": list(basis_edges[:8]),
        "row_basis_last": list(basis_edges[-8:]),
        "omitted_coordinate_columns": omitted_columns,
        "nonbasis_rows": len(nonbasis_edges),
        "coefficient_column_support_min": min(supports),
        "coefficient_column_support_max": max(supports),
        "distinct_projective_coefficient_columns": len(set(normalized_columns)),
        "normalized_coefficient_columns_sha256": normalized_digest.hexdigest(),
        "vertex_deletion_rank_histogram": {
            str(key): value for key, value in sorted(Counter(vertex_deletion_ranks).items())
        },
        "sharp_vertex": sharp_vertex,
        "sharp_incident_edge_indices": incident[sharp_vertex],
        "sharp_deleted_edge_indices": sharp_deleted,
        "rank_after_sharp_three_edge_deletion": sharp_rank,
        "all_checks": True,
        "elapsed_seconds_informational": round(time.monotonic() - started, 3),
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    root = here.parent
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("summary", "verify"), nargs="?", default="verify")
    parser.add_argument("--certificate", type=Path, default=here / "certificate.json")
    parser.add_argument(
        "--coordinates",
        type=Path,
        default=root / "hadwiger_nelson_parts509_criticality" / "parts509.vtx",
    )
    parser.add_argument(
        "--edges",
        type=Path,
        default=root / "hadwiger_nelson_parts509_degree10_replacements" / "edges.json",
    )
    args = parser.parse_args()
    summary = compute(args.coordinates, args.edges)
    elapsed = summary.pop("elapsed_seconds_informational")
    if args.mode == "verify":
        certificate = json.loads(args.certificate.read_text())
        if certificate.get("independent") != summary:
            raise ValueError("independent summary differs from certificate.json")
        print("independent_certificate_verified=true")
    else:
        print(json.dumps(summary, indent=2, sort_keys=True))
    print(
        f"all_checks=true rank={summary['rank']} edge_deletion_tolerance=2 "
        f"vertex_deletions_rigid=509 sharp_three_edge_rank="
        f"{summary['rank_after_sharp_three_edge_deletion']} elapsed_seconds={elapsed}"
    )


if __name__ == "__main__":
    main()
