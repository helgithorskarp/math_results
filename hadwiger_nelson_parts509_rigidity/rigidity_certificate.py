#!/usr/bin/env python3
"""Exact modular certificate for rigidity of the Parts-509 framework.

The characteristic-zero rigidity matrix has entries in
Q(sqrt(3), sqrt(5), sqrt(11)).  A nonzero minor after a valid finite-field
specialization is therefore a certificate that the corresponding exact minor
is nonzero.  This program uses python-flint for the finite-field linear algebra.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

from flint import nmod_mat


P = 1_000_081
ROOTS = (35_512, 183_365, 29_480)
RADICANDS = (3, 5, 11)
N = 509
EXPECTED_COORDINATE_SHA256 = (
    "770a585a6c1e1222355322707479cb826e9ada560279da904ef89c15c99ff0b5"
)
EXPECTED_EDGE_SHA256 = (
    "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha256_int_lines(values: list[int]) -> str:
    return hashlib.sha256("".join(f"{value}\n" for value in values).encode()).hexdigest()


def sha256_coordinate_lines(coords: list[tuple[int, int]]) -> str:
    return hashlib.sha256(
        "".join(f"{x} {y}\n" for x, y in coords).encode()
    ).hexdigest()


def load_parts_module(source_dir: Path):
    spec = importlib.util.spec_from_file_location("parts509", source_dir / "parts509.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load the sibling exact-geometry checker")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fraction_mod(value: Fraction) -> int:
    denominator = value.denominator % P
    if denominator == 0:
        raise ValueError("coordinate denominator vanishes modulo the certificate prime")
    return value.numerator % P * pow(denominator, -1, P) % P


RADICAL_POWERS = tuple(
    __import__("math").prod(ROOTS[bit] for bit in range(3) if mask & (1 << bit)) % P
    for mask in range(8)
)


def field_mod(value: tuple[Fraction, ...]) -> int:
    if len(value) != 8:
        raise ValueError("expected the eight-element multiquadratic basis")
    return sum(
        fraction_mod(coefficient) * RADICAL_POWERS[mask]
        for mask, coefficient in enumerate(value)
    ) % P


def pivot_columns(matrix: nmod_mat, rank: int) -> list[int]:
    reduced, observed_rank = matrix.rref()
    if observed_rank != rank:
        raise ValueError(f"unexpected rank {observed_rank}, expected {rank}")
    pivots: list[int] = []
    next_column = 0
    for row in range(rank):
        while next_column < matrix.ncols() and int(reduced[row, next_column]) == 0:
            next_column += 1
        if next_column == matrix.ncols():
            raise ValueError("rref ended before the advertised rank")
        pivots.append(next_column)
        next_column += 1
    return pivots


def build_rigidity_matrix(
    coords: list[tuple[int, int]], edges: list[tuple[int, int]]
) -> nmod_mat:
    flat: list[int] = []
    for u, v in edges:
        dx = (coords[u][0] - coords[v][0]) % P
        dy = (coords[u][1] - coords[v][1]) % P
        row = [0] * (2 * len(coords))
        row[2 * u] = dx
        row[2 * u + 1] = dy
        row[2 * v] = (-dx) % P
        row[2 * v + 1] = (-dy) % P
        flat.extend(row)
    return nmod_mat(len(edges), 2 * len(coords), flat, P)


def compute(source_dir: Path) -> dict[str, object]:
    started = time.monotonic()
    parts = load_parts_module(source_dir)
    coordinate_path = source_dir / "parts509.vtx"
    if sha256_file(coordinate_path) != EXPECTED_COORDINATE_SHA256:
        raise ValueError("unexpected coordinate input")
    points, edges = parts.load_graph(coordinate_path)
    if len(points) != N or len(edges) != 2442:
        raise ValueError("unexpected strict graph order or size")
    if parts.edge_sha256(edges) != EXPECTED_EDGE_SHA256:
        raise ValueError("unexpected exact unit-distance edge list")
    if any(root * root % P != value for root, value in zip(ROOTS, RADICANDS)):
        raise AssertionError("invalid square-root specialization")

    coords = [(field_mod(x), field_mod(y)) for x, y in points]
    matrix = build_rigidity_matrix(coords, edges)
    maximum_rank = 2 * N - 3
    rank = matrix.rank()
    if rank != maximum_rank:
        raise ValueError(f"rigidity rank is {rank}, expected {maximum_rank}")

    # Pivot columns of R^T are a deterministic row basis of R.
    basis_edges = pivot_columns(matrix.transpose(), rank)
    basis_set = set(basis_edges)
    basis_flat = [
        int(matrix[edge_index, column])
        for edge_index in basis_edges
        for column in range(matrix.ncols())
    ]
    basis_matrix = nmod_mat(rank, matrix.ncols(), basis_flat, P)
    coordinate_pivots = pivot_columns(basis_matrix, rank)
    omitted_columns = sorted(set(range(matrix.ncols())) - set(coordinate_pivots))

    minor = nmod_mat(
        rank,
        rank,
        [
            int(basis_matrix[row, column])
            for row in range(rank)
            for column in coordinate_pivots
        ],
        P,
    )
    inverse = minor.inv()
    nonbasis_edges = [i for i in range(len(edges)) if i not in basis_set]
    restricted = nmod_mat(
        len(nonbasis_edges),
        rank,
        [
            int(matrix[edge_index, column])
            for edge_index in nonbasis_edges
            for column in coordinate_pivots
        ],
        P,
    )
    coefficients = restricted * inverse

    # In the row representation [I; A], a basis row i can be replaced by a
    # nonbasis row f exactly when A[f,i] is nonzero.  Two basis rows i,j can be
    # replaced simultaneously exactly when columns i,j of A are independent.
    supports: list[int] = []
    normalized_columns: list[tuple[int, ...]] = []
    normalized_digest = hashlib.sha256()
    for column in range(rank):
        values = tuple(int(coefficients[row, column]) for row in range(len(nonbasis_edges)))
        support = sum(value != 0 for value in values)
        if support == 0:
            raise ValueError(f"basis row {column} has no replacement")
        scale = pow(next(value for value in values if value), -1, P)
        normalized = tuple(value * scale % P for value in values)
        supports.append(support)
        normalized_columns.append(normalized)
        for value in normalized:
            normalized_digest.update(value.to_bytes(4, "little"))
    if min(supports) < 2:
        raise ValueError("a basis row does not survive deletion with one nonbasis row")
    if len(set(normalized_columns)) != rank:
        raise ValueError("two basis coefficient columns are projectively equal")

    # Delete all edges incident with v.  In [I; A], only the removed basis
    # coordinates need to be recovered by the retained nonbasis rows.
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
        projected = nmod_mat(
            len(retained_nonbasis),
            len(missing_basis),
            [
                int(coefficients[row, column])
                for row in retained_nonbasis
                for column in missing_basis
            ],
            P,
        )
        deletion_rank = rank - len(missing_basis) + projected.rank()
        vertex_deletion_ranks.append(deletion_rank)
    if set(vertex_deletion_ranks) != {2 * (N - 1) - 3}:
        raise ValueError("not every one-vertex deletion is infinitesimally rigid")

    # Sharpness: vertex 310 has degree four.  Removing three incident edges
    # leaves it with one constraint, so characteristic-zero rank is at most
    # 1014.  The modular rank below proves equality.
    sharp_vertex = 310
    sharp_deleted = incident[sharp_vertex][:3]
    sharp_deleted_set = set(sharp_deleted)
    sharp_flat = [
        int(matrix[row, column])
        for row in range(matrix.nrows())
        if row not in sharp_deleted_set
        for column in range(matrix.ncols())
    ]
    sharp_matrix = nmod_mat(matrix.nrows() - 3, matrix.ncols(), sharp_flat, P)
    sharp_rank = sharp_matrix.rank()
    if sharp_rank != maximum_rank - 1:
        raise ValueError("the advertised sharp three-edge deletion has unexpected rank")

    return {
        "prime": P,
        "square_roots_of_3_5_11": list(ROOTS),
        "modular_coordinates_sha256": sha256_coordinate_lines(coords),
        "rigidity_matrix_rows": len(edges),
        "rigidity_matrix_columns": 2 * N,
        "rank": rank,
        "maximum_rank": maximum_rank,
        "row_basis_size": len(basis_edges),
        "row_basis_edge_indices_sha256": sha256_int_lines(basis_edges),
        "row_basis_first": basis_edges[:8],
        "row_basis_last": basis_edges[-8:],
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
        "--source-dir",
        type=Path,
        default=root / "hadwiger_nelson_parts509_criticality",
    )
    args = parser.parse_args()
    summary = compute(args.source_dir)
    elapsed = summary.pop("elapsed_seconds_informational")
    if args.mode == "verify":
        certificate = json.loads(args.certificate.read_text())
        if certificate.get("primary") != summary:
            raise ValueError("primary summary differs from certificate.json")
        print("primary_certificate_verified=true")
    else:
        print(json.dumps(summary, indent=2, sort_keys=True))
    print(
        f"all_checks=true rank={summary['rank']} edge_deletion_tolerance=2 "
        f"vertex_deletions_rigid=509 sharp_three_edge_rank="
        f"{summary['rank_after_sharp_three_edge_deletion']} elapsed_seconds={elapsed}"
    )


if __name__ == "__main__":
    main()
