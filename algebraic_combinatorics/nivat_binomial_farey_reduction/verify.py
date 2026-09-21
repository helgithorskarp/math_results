#!/usr/bin/env python3
"""Exact audits for the binary-binomial Farey-triangle reduction."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from itertools import combinations


Vector = tuple[int, int]


def det(u: Vector, v: Vector) -> int:
    return u[0] * v[1] - u[1] * v[0]


def primitive_direction(u: Vector) -> Vector:
    if u == (0, 0):
        raise ValueError("zero vector has no direction")
    g = math.gcd(abs(u[0]), abs(u[1]))
    v = (u[0] // g, u[1] // g)
    if v[0] < 0 or (v[0] == 0 and v[1] < 0):
        v = (-v[0], -v[1])
    return v


def multiply_mod2(left: set[Vector], right: set[Vector]) -> set[Vector]:
    result: set[Vector] = set()
    for a in left:
        for b in right:
            exponent = (a[0] + b[0], a[1] + b[1])
            if exponent in result:
                result.remove(exponent)
            else:
                result.add(exponent)
    return result


def product_support(directions: list[Vector]) -> set[Vector]:
    result = {(0, 0)}
    for u in directions:
        result = multiply_mod2(result, {(0, 0), u})
    return result


def rref(rows: list[int], columns: int) -> tuple[list[int], list[int]]:
    work = [row for row in rows if row]
    pivots: list[int] = []
    rank = 0
    for column in range(columns):
        pivot = next(
            (index for index in range(rank, len(work))
             if (work[index] >> column) & 1),
            None,
        )
        if pivot is None:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        for index in range(len(work)):
            if index != rank and ((work[index] >> column) & 1):
                work[index] ^= work[rank]
        pivots.append(column)
        rank += 1
        if rank == len(work):
            break
    return work[:rank], pivots


def nullspace(rows: list[int], columns: int) -> list[int]:
    reduced, pivots = rref(rows, columns)
    pivot_set = set(pivots)
    basis: list[int] = []
    for free in (c for c in range(columns) if c not in pivot_set):
        vector = 1 << free
        for row, pivot in reversed(list(zip(reduced, pivots))):
            if (row & vector).bit_count() & 1:
                vector |= 1 << pivot
        basis.append(vector)
    return basis


def convolution_rows(size: int, support: set[Vector]) -> list[int]:
    rows: list[int] = []
    for i in range(size):
        for j in range(size):
            row = 0
            for a, b in support:
                column = ((i + a) % size) * size + (j + b) % size
                row ^= 1 << column
            rows.append(row)
    return rows


def torus_record(size: int) -> dict[str, object]:
    if size < 3 or size % 2 == 0:
        raise ValueError("torus sizes must be odd integers at least three")
    factors = [
        {(0, 0), (1, 0)},
        {(0, 0), (0, 1)},
        {(0, 0), (1, 1)},
    ]
    triangle = {(0, 0)}
    for factor in factors:
        triangle = multiply_mod2(triangle, factor)
    factor_kernels = [
        nullspace(convolution_rows(size, factor), size * size)
        for factor in factors
    ]
    triangle_kernel = nullspace(
        convolution_rows(size, triangle), size * size
    )
    sum_dimension = len(rref(sum(factor_kernels, []), size * size)[1])
    assert sum_dimension == len(triangle_kernel) == 3 * size - 2
    return {
        "size": size,
        "direction_kernel_dimensions": [len(k) for k in factor_kernels],
        "direction_sum_dimension": sum_dimension,
        "triangle_kernel_dimension": len(triangle_kernel),
    }


def direction_record(bound: int) -> dict[str, object]:
    if bound < 1:
        raise ValueError("bound must be positive")
    directions = sorted({
        primitive_direction((a, b))
        for a in range(-bound, bound + 1)
        for b in range(-bound, bound + 1)
        if (a, b) != (0, 0)
    })
    edges = [pair for pair in combinations(directions, 2)
             if abs(det(*pair)) == 1]
    triangles = [triple for triple in combinations(directions, 3)
                 if all(abs(det(u, v)) == 1
                        for u, v in combinations(triple, 2))]
    four_cliques = [quad for quad in combinations(directions, 4)
                    if all(abs(det(u, v)) == 1
                           for u, v in combinations(quad, 2))]
    normalized = set()
    for triple in triangles:
        u, v, w = triple
        if det(u, v) == -1:
            v = (-v[0], -v[1])
        assert det(u, v) == 1
        a = det(w, v)
        b = det(u, w)
        assert abs(a) == abs(b) == 1
        left = (a * u[0] + b * v[0], a * u[1] + b * v[1])
        assert left == w or left == (-w[0], -w[1])
        normalized.add(((1, 0), (0, 1), (1, 1)))
    assert not four_cliques
    assert len(normalized) == (1 if triangles else 0)
    digest_payload = [list(vector) for vector in directions]
    digest = hashlib.sha256(
        json.dumps(digest_payload, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "bound": bound,
        "primitive_unoriented_directions": len(directions),
        "determinant_one_edges": len(edges),
        "determinant_one_triangles": len(triangles),
        "determinant_one_four_cliques": len(four_cliques),
        "triangle_normal_forms": len(normalized),
        "direction_digest": digest,
    }


def build_record(bound: int, torus_sizes: list[int]) -> dict[str, object]:
    triangle_support = sorted(product_support([(1, 0), (0, 1), (1, 1)]))
    expected_support = sorted({
        (0, 0), (1, 0), (0, 1), (2, 1), (1, 2), (2, 2)
    })
    assert triangle_support == expected_support
    return {
        "schema": "nivat-binomial-farey-reduction-v1",
        "direction_audit": direction_record(bound),
        "triangle_support": [list(vector) for vector in triangle_support],
        "triangle_support_generates_z2": (
            (1, 0) in triangle_support and (0, 1) in triangle_support
        ),
        "odd_torus_audits": [torus_record(size) for size in torus_sizes],
        "trust_boundary": (
            "Finite audits corroborate the normal form and decomposition; "
            "the universal theorem uses the written proof and cited results."
        ),
    }


def parse_sizes(value: str) -> list[int]:
    try:
        sizes = [int(item) for item in value.split(",") if item]
    except ValueError as error:
        raise argparse.ArgumentTypeError("sizes must be comma-separated integers") from error
    if not sizes or any(size < 3 or size % 2 == 0 for size in sizes):
        raise argparse.ArgumentTypeError("sizes must be odd integers at least three")
    return sizes


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, default=6)
    parser.add_argument("--torus-sizes", type=parse_sizes, default=[3, 5, 7])
    arguments = parser.parse_args()
    print(json.dumps(
        build_record(arguments.bound, arguments.torus_sizes),
        indent=2,
        sort_keys=True,
    ))


if __name__ == "__main__":
    main()
