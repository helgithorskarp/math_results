#!/usr/bin/env python3
"""Exact audit of the exceptional C5 polytope lemma and sharp family."""

from __future__ import annotations

import hashlib
import itertools
import json
from fractions import Fraction


Vector = tuple[Fraction, ...]
Edge = tuple[int, int]


def cycle_edges(step: int) -> tuple[Edge, ...]:
    return tuple(sorted({tuple(sorted((i, (i + step) % 5))) for i in range(5)}))


def solve_square(rows: list[list[Fraction]], rhs: list[Fraction]) -> Vector | None:
    n = len(rows)
    matrix = [row[:] + [value] for row, value in zip(rows, rhs, strict=True)]
    pivot_row = 0
    for column in range(n):
        pivot = next(
            (row for row in range(pivot_row, n) if matrix[row][column]), None
        )
        if pivot is None:
            return None
        matrix[pivot_row], matrix[pivot] = matrix[pivot], matrix[pivot_row]
        scale = matrix[pivot_row][column]
        matrix[pivot_row] = [entry / scale for entry in matrix[pivot_row]]
        for row in range(n):
            if row == pivot_row:
                continue
            factor = matrix[row][column]
            if factor:
                matrix[row] = [
                    x - factor * y
                    for x, y in zip(matrix[row], matrix[pivot_row], strict=True)
                ]
        pivot_row += 1
    return tuple(matrix[i][-1] for i in range(n))


def polytope_vertices(edges: tuple[Edge, ...]) -> tuple[Vector, ...]:
    constraints: list[tuple[list[Fraction], Fraction]] = []
    for i in range(5):
        row = [Fraction(0) for _ in range(5)]
        row[i] = Fraction(1)
        constraints.append((row, Fraction(0)))
    for i, j in edges:
        row = [Fraction(0) for _ in range(5)]
        row[i] = row[j] = Fraction(1)
        constraints.append((row, Fraction(1)))

    vertices: set[Vector] = set()
    for active in itertools.combinations(constraints, 5):
        solution = solve_square([row for row, _ in active], [rhs for _, rhs in active])
        if solution is None or any(value < 0 for value in solution):
            continue
        if any(solution[i] + solution[j] > 1 for i, j in edges):
            continue
        vertices.add(solution)
    return tuple(sorted(vertices))


def stable_incidence_vectors(edges: tuple[Edge, ...]) -> set[Vector]:
    answer = set()
    edge_sets = {frozenset(edge) for edge in edges}
    for mask in range(1 << 5):
        support = {i for i in range(5) if mask & (1 << i)}
        if all(not pair <= support for pair in edge_sets):
            answer.add(tuple(Fraction(int(i in support)) for i in range(5)))
    return answer


def expected_vertices(edges: tuple[Edge, ...]) -> set[Vector]:
    return stable_incidence_vectors(edges) | {(Fraction(1, 2),) * 5}


def support(vector: Vector) -> tuple[int, ...]:
    return tuple(i for i, value in enumerate(vector) if value)


def is_half(vector: Vector) -> bool:
    return vector == (Fraction(1, 2),) * 5


def certify_pair(a: Vector, b: Vector, original_edges: set[Edge]) -> dict[str, object]:
    if is_half(a) and is_half(b):
        return {"category": "half_half", "terms": 5, "base_denominator": 4}

    if is_half(a) or is_half(b):
        integral = b if is_half(a) else a
        if any(value.denominator != 1 or value not in (0, 1) for value in integral):
            raise AssertionError("nonintegral non-half polytope vertex")
        size = len(support(integral))
        if size > 2:
            raise AssertionError("cycle stable-set support exceeds two")
        return {"category": "half_integral", "support_size": size}

    if any(value.denominator != 1 or value not in (0, 1) for value in a + b):
        raise AssertionError("unexpected rational vertex")
    a_support = set(support(a))
    b_support = set(support(b))
    if any(tuple(sorted(pair)) not in original_edges for pair in itertools.combinations(a_support, 2)):
        raise AssertionError("a-support is not a clique of the original C5")
    if any(tuple(sorted(pair)) in original_edges for pair in itertools.combinations(b_support, 2)):
        raise AssertionError("b-support is not stable in the original C5")
    intersection = len(a_support & b_support)
    if intersection > 1:
        raise AssertionError("a clique and stable set intersect more than once")
    return {"category": "integral_integral", "intersection": intersection}


def lexicographic_power_rows(last_k: int = 12) -> list[dict[str, int]]:
    return [
        {
            "k": k,
            "order": 5**k,
            "alpha": 2**k,
            "omega": 2**k,
            "alpha_times_omega": 4**k,
        }
        for k in range(last_k + 1)
    ]


def audit() -> dict[str, object]:
    original = set(cycle_edges(1))
    a_edges = cycle_edges(2)
    b_edges = cycle_edges(1)
    a_vertices = polytope_vertices(a_edges)
    b_vertices = polytope_vertices(b_edges)
    if set(a_vertices) != expected_vertices(a_edges):
        raise AssertionError("P_a vertex classification failed")
    if set(b_vertices) != expected_vertices(b_edges):
        raise AssertionError("P_b vertex classification failed")

    rows = [certify_pair(a, b, original) for a in a_vertices for b in b_vertices]
    category_counts = {
        category: sum(row["category"] == category for row in rows)
        for category in ("integral_integral", "half_integral", "half_half")
    }
    if category_counts != {
        "integral_integral": 121,
        "half_integral": 22,
        "half_half": 1,
    }:
        raise AssertionError("unexpected vertex-pair category counts")

    family = lexicographic_power_rows()
    for row in family:
        if row["alpha_times_omega"] != row["alpha"] * row["omega"]:
            raise AssertionError("product formula failed")
        if row["order"] != 5 ** row["k"] or row["alpha"] != 2 ** row["k"]:
            raise AssertionError("sharp-family recurrence failed")

    payload = {
        "a_vertices": [[str(value) for value in vector] for vector in a_vertices],
        "b_vertices": [[str(value) for value in vector] for vector in b_vertices],
        "pair_certificates": rows,
        "sharp_family": family,
    }
    digest = hashlib.sha256(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    return {
        "a_polytope_vertices": len(a_vertices),
        "b_polytope_vertices": len(b_vertices),
        "vertex_pairs_checked": len(rows),
        "pair_categories": category_counts,
        "sharp_family_k": [family[0]["k"], family[-1]["k"]],
        "last_sharp_order": family[-1]["order"],
        "last_sharp_alpha_omega": family[-1]["alpha_times_omega"],
        "exact_audit_sha256": digest,
        "trust_boundary": (
            "exact C5 polytope audit only; the universal induction and imported "
            "perfect-graph polytope theorem are in THEOREM.md"
        ),
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
