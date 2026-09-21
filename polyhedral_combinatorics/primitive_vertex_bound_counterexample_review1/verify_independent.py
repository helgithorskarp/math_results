#!/usr/bin/env python3
"""Independent exact checks for the primitive-polytope counterexample.

CPython 3.11+, standard library only.  This imports no target code or target
output.  The strict refutation is checked from 4,352 explicit full-rank
vertex witnesses; small cases are separately enumerated from every active
facet basis to audit completeness and zero-interval handling.
"""

import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inequalities(k):
    """Rows (a,b) representing a.x <= b; valid also at boundary k=1."""
    require(type(k) is int and k >= 1, "k must be a positive integer")
    dimension = k + 2
    rows = []
    for coordinate in range(dimension):
        normal = [0] * dimension
        normal[coordinate] = -1
        rows.append((tuple(normal), 0))
    for index in range(k):
        normal = [2 * index + 1, 1] + [0] * k
        normal[index + 2] = 1
        rows.append((tuple(normal), k * k + index * (index + 1)))
    return tuple(rows)


def inner(left, right):
    return sum(a * b for a, b in zip(left, right))


def determinant_bareiss(matrix):
    """Exact determinant using fraction-free Bareiss elimination."""
    size = len(matrix)
    require(size and all(len(row) == size for row in matrix),
            "square matrix required")
    work = [list(row) for row in matrix]
    sign = 1
    previous = 1
    for column in range(size - 1):
        pivot_row = next((row for row in range(column, size)
                          if work[row][column]), None)
        if pivot_row is None:
            return 0
        if pivot_row != column:
            work[column], work[pivot_row] = work[pivot_row], work[column]
            sign = -sign
        pivot = work[column][column]
        for row in range(column + 1, size):
            for col in range(column + 1, size):
                numerator = (work[row][col] * pivot
                             - work[row][column] * work[column][col])
                require(numerator % previous == 0,
                        "Bareiss exact division failed")
                work[row][col] = numerator // previous
            work[row][column] = 0
        previous = pivot
    return sign * work[-1][-1]


def solve_square(normals, offsets):
    """Generic rational RREF, used only by the small complete census."""
    size = len(normals)
    matrix = [[Fraction(value) for value in row] + [Fraction(offset)]
              for row, offset in zip(normals, offsets)]
    for column in range(size):
        pivot = next((row for row in range(column, size)
                      if matrix[row][column]), None)
        if pivot is None:
            return None
        matrix[column], matrix[pivot] = matrix[pivot], matrix[column]
        scale = matrix[column][column]
        matrix[column] = [value / scale for value in matrix[column]]
        for row in range(size):
            if row == column or not matrix[row][column]:
                continue
            scale = matrix[row][column]
            matrix[row] = [left - scale * right
                           for left, right in zip(matrix[row], matrix[column])]
    return tuple(row[-1] for row in matrix)


def base_vertices(k):
    yield "origin", (0, 0)
    for index in range(k + 1):
        yield f"q{index}", (index, k * k - index * index)


def endpoint_witnesses(k):
    """Generate interval endpoints without using the target implementation."""
    for label, (y_value, z_value) in base_vertices(k):
        endpoints = []
        for index in range(k):
            slack = (k * k + index * (index + 1)
                     - (2 * index + 1) * y_value - z_value)
            require(slack >= 0, ("negative fiber", k, label, index))
            endpoints.append((0,) if slack == 0 else (0, slack))
        for private in product(*endpoints):
            yield label, (y_value, z_value) + private


def active_rows(rows, point):
    slacks = tuple(offset - inner(normal, point)
                   for normal, offset in rows)
    require(all(slack >= 0 for slack in slacks),
            ("infeasible witness", point))
    return tuple(index for index, slack in enumerate(slacks) if slack == 0)


def witness_audit(k):
    rows = inequalities(k)
    dimension = k + 2
    seen = set()
    label_counts = {}
    determinant_counts = {}
    digest = sha256()
    for label, point in endpoint_witnesses(k):
        require(point not in seen, ("duplicate witness", k, point))
        seen.add(point)
        active = active_rows(rows, point)
        require(len(active) == dimension,
                ("unexpected active-facet count", k, point, active))
        determinant = abs(determinant_bareiss([rows[index][0]
                                               for index in active]))
        require(determinant > 0,
                ("active normals are singular", k, point, active))
        label_counts[label] = label_counts.get(label, 0) + 1
        determinant_counts[determinant] = determinant_counts.get(
            determinant, 0) + 1
        digest.update(json.dumps([point, active], separators=(",", ":"))
                      .encode("ascii") + b"\n")
    return {
        "k": k,
        "dimension": dimension,
        "facets": len(rows),
        "witnesses": len(seen),
        "cube_vertices": 1 << dimension,
        "base_fiber_counts": label_counts,
        "absolute_active_determinants": {
            str(key): value for key, value in sorted(determinant_counts.items())
        },
        "witness_sha256": digest.hexdigest(),
    }, seen


def facet_and_primitive_audit(k):
    """Use different relative-interior witnesses from the target package."""
    rows = inequalities(k)
    dimension = k + 2
    interior = [Fraction(1, 3)] * dimension
    require(all(inner(normal, interior) < offset
                for normal, offset in rows), "interior witness failed")
    facet_digest = sha256()
    for removed, (normal, offset) in enumerate(rows):
        point = interior[:]
        direction = [0] * dimension
        if removed < dimension:
            point[removed] = 0
            direction[removed] = -1
        else:
            index = removed - dimension
            point[index + 2] = (Fraction(k * k + index * (index + 1))
                                - Fraction(2 * index + 2, 3))
            direction[index + 2] = 1
        slacks = [bound - inner(row, point) for row, bound in rows]
        require(slacks[removed] == 0 and
                all(slack > 0 for index, slack in enumerate(slacks)
                    if index != removed),
                ("inequality lacks a relative-interior facet point", removed))
        derivatives = [inner(row, direction) for row, _ in rows]
        require(derivatives[removed] > 0 and
                all(value <= 0 for index, value in enumerate(derivatives)
                    if index != removed),
                ("facet-deletion direction is not a recession ray", removed))
        facet_digest.update(json.dumps(
            [[str(value) for value in point], direction],
            separators=(",", ":")).encode("ascii") + b"\n")
    return {
        "strict_interior": [str(value) for value in interior],
        "facet_points": len(rows),
        "deletion_rays": len(rows),
        "facet_ray_sha256": facet_digest.hexdigest(),
        "coordinate_upper_bounds": [k, k * k] + [
            k * k + index * (index + 1) for index in range(k)
        ],
    }


def enumerate_vertices_from_bases(k):
    rows = inequalities(k)
    dimension = k + 2
    vertices = set()
    nonsingular = 0
    tested = 0
    for chosen in combinations(range(len(rows)), dimension):
        tested += 1
        point = solve_square([rows[index][0] for index in chosen],
                             [rows[index][1] for index in chosen])
        if point is None:
            continue
        nonsingular += 1
        if all(inner(normal, point) <= offset
               for normal, offset in rows):
            vertices.add(point)
    return vertices, tested, nonsingular


def small_completeness_audit(maximum_k):
    records = []
    total_bases = 0
    for k in range(1, maximum_k + 1):
        witness_record, witnesses = witness_audit(k)
        vertices, tested, nonsingular = enumerate_vertices_from_bases(k)
        rational_witnesses = {
            tuple(Fraction(value) for value in point) for point in witnesses
        }
        require(vertices == rational_witnesses,
                ("complete census differs entrywise", k))
        records.append({
            "k": k,
            "dimension": k + 2,
            "bases_tested": tested,
            "nonsingular_bases": nonsingular,
            "vertices": len(vertices),
        })
        total_bases += tested
    return records, total_bases


def run():
    small_records, total_bases = small_completeness_audit(7)
    equality, _ = witness_audit(9)
    strict, _ = witness_audit(10)
    geometry = facet_and_primitive_audit(10)

    require(strict["witnesses"] == 4352 > strict["cube_vertices"] == 4096,
            "strict numerical counterexample failed")
    require(equality["witnesses"] == equality["cube_vertices"] == 2048,
            "equality count failed")
    require(equality["facets"] == 20 != 2 * equality["dimension"],
            "non-cube facet count failed")
    require(strict["witnesses"] == (1 << (10 - 2)) * (10 + 7),
            "closed count failed")
    require(small_records[0]["vertices"] == 4,
            "k=1 boundary extension failed")

    return {
        "schema": 1,
        "status": "PASS",
        "strict_counterexample": strict,
        "equality_counterexample": equality,
        "k10_defining_conditions": geometry,
        "complete_basis_census_through_k": 7,
        "small_complete_records": small_records,
        "small_bases_tested": total_bases,
        "boundary_extension": (
            "The same inequalities also give a primitive 3-simplex at k=1; "
            "the target starts at k=2 to match the conjecture domain d>=4."),
        "trust_boundary": (
            "The 4,352 direct feasible full-rank witnesses alone refute the "
            "numerical bound. Exact universal equality and the unbounded ratio "
            "also use the reviewed human affine-box completeness proof."),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true")
    arguments = parser.parse_args()
    result = run()
    if arguments.emit:
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    expected_path = Path(__file__).with_name("expected.json")
    expected = json.loads(expected_path.read_text())
    require(result == expected, "frozen expected output mismatch")
    print(json.dumps({
        "status": result["status"],
        "strict_witnesses": result["strict_counterexample"]["witnesses"],
        "small_bases_tested": result["small_bases_tested"],
        "expected_sha256": sha256(expected_path.read_bytes()).hexdigest(),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
