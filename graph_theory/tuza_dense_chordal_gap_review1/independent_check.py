#!/usr/bin/env python3
"""Independent exact checks for the dense-chordal Tuza gap.

This checker imports no target source or output.  It exhausts every labelled
graph through six vertices, recognizes chordality from induced cycles, checks
an independently constructed maximum-cardinality elimination order, solves
the fractional triangle-packing LP over the rationals, computes the exact
triangle cover by exhaustive surviving-edge sets, and tests the zero/unit
structural inequality for every possible zero-edge set.

Requires CPython 3.11+ and only the standard library.
"""

from __future__ import annotations

from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from math import isqrt
import json
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def edge_pairs(n: int) -> list[tuple[int, int]]:
    return list(combinations(range(n), 2))


def triangle_masks(n: int, edges: list[tuple[int, int]]) -> list[int]:
    edge_id = {edge: index for index, edge in enumerate(edges)}
    result = []
    for vertices in combinations(range(n), 3):
        pairs = list(combinations(vertices, 2))
        if all(pair in edge_id for pair in pairs):
            result.append(sum(1 << edge_id[pair] for pair in pairs))
    return result


def has_induced_cycle(n: int, edges: list[tuple[int, int]]) -> bool:
    """Definition-level chordality test, independent of elimination."""
    edge_set = set(edges)
    for size in range(4, n + 1):
        for vertices in combinations(range(n), size):
            degrees = {v: 0 for v in vertices}
            adjacency = {v: [] for v in vertices}
            for a, b in combinations(vertices, 2):
                if (a, b) in edge_set:
                    degrees[a] += 1
                    degrees[b] += 1
                    adjacency[a].append(b)
                    adjacency[b].append(a)
            if not all(degrees[v] == 2 for v in vertices):
                continue
            seen = {vertices[0]}
            stack = [vertices[0]]
            while stack:
                for neighbor in adjacency[stack.pop()]:
                    if neighbor not in seen:
                        seen.add(neighbor)
                        stack.append(neighbor)
            if len(seen) == size:
                return True
    return False


def mcs_peo(n: int, edges: list[tuple[int, int]]) -> tuple[int, ...]:
    """Maximum-cardinality search; return the reverse selection order."""
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    weights = [0] * n
    remaining = set(range(n))
    selected = []
    while remaining:
        vertex = max(remaining, key=lambda v: (weights[v], v))
        selected.append(vertex)
        remaining.remove(vertex)
        for neighbor in adjacency[vertex] & remaining:
            weights[neighbor] += 1
    order = tuple(reversed(selected))
    rank = {vertex: index for index, vertex in enumerate(order)}
    for vertex in order:
        later = [w for w in adjacency[vertex] if rank[w] > rank[vertex]]
        require(
            all(b in adjacency[a] for a, b in combinations(later, 2)),
            "MCS failed to produce an elimination order",
        )
    return order


def fractional_packing(
    edge_count: int, triangles: list[int]
) -> tuple[Fraction, list[Fraction]]:
    """Exact primal simplex with a slack basis and a largest-gain pivot rule."""
    triangle_count = len(triangles)
    width = triangle_count + edge_count
    rows = []
    for edge in range(edge_count):
        row = [Fraction(bool(mask >> edge & 1)) for mask in triangles]
        row += [Fraction(index == edge) for index in range(edge_count)]
        row.append(Fraction(1))
        rows.append(row)
    objective = [Fraction(-1)] * triangle_count
    objective += [Fraction(0)] * edge_count + [Fraction(0)]
    basis = list(range(triangle_count, width))

    while True:
        improving = [index for index, value in enumerate(objective[:-1]) if value < 0]
        if not improving:
            break
        entering = min(improving, key=lambda j: (objective[j], j))
        candidates = [row for row in range(edge_count) if rows[row][entering] > 0]
        require(bool(candidates), "packing LP became unbounded")
        leaving = min(
            candidates,
            key=lambda row: (rows[row][-1] / rows[row][entering], basis[row]),
        )
        pivot = rows[leaving][entering]
        rows[leaving] = [value / pivot for value in rows[leaving]]
        for row in range(edge_count):
            if row == leaving or rows[row][entering] == 0:
                continue
            multiplier = rows[row][entering]
            rows[row] = [
                value - multiplier * pivot_value
                for value, pivot_value in zip(rows[row], rows[leaving])
            ]
        multiplier = objective[entering]
        objective = [
            value - multiplier * pivot_value
            for value, pivot_value in zip(objective, rows[leaving])
        ]
        basis[leaving] = entering

    primal = [Fraction(0)] * triangle_count
    for row, variable in enumerate(basis):
        if variable < triangle_count:
            primal[variable] = rows[row][-1]
    dual = objective[triangle_count:width]
    loads = [
        sum((primal[index] for index, mask in enumerate(triangles) if mask >> edge & 1), Fraction(0))
        for edge in range(edge_count)
    ]
    require(all(weight >= 0 for weight in primal), "negative primal weight")
    require(all(load <= 1 for load in loads), "infeasible primal packing")
    require(all(0 <= weight <= 1 for weight in dual), "bad dual edge weight")
    require(
        all(
            sum((dual[edge] for edge in range(edge_count) if mask >> edge & 1), Fraction(0)) >= 1
            for mask in triangles
        ),
        "infeasible dual cover",
    )
    value = sum(primal, Fraction(0))
    require(value == sum(dual, Fraction(0)) == objective[-1], "duality failure")
    return value, dual


def graph_audit(n: int) -> tuple[dict[str, int], bytes]:
    complete = edge_pairs(n)
    chordal = lp_cases = zero_cases = positive_bounds = 0
    digest_records = []
    for graph_mask in range(1 << len(complete)):
        edges = [edge for index, edge in enumerate(complete) if graph_mask >> index & 1]
        if has_induced_cycle(n, edges):
            continue
        chordal += 1
        order = mcs_peo(n, edges)
        rank = {vertex: index for index, vertex in enumerate(order)}
        triangles = triangle_masks(n, edges)
        edge_count = len(edges)
        maximum_surviving = 0
        for zero_mask in range(1 << edge_count):
            if any(zero_mask & triangle == triangle for triangle in triangles):
                continue
            zero_cases += 1
            maximum_surviving = max(maximum_surviving, zero_mask.bit_count())
            forced = 0
            for triangle in triangles:
                if (zero_mask & triangle).bit_count() == 2:
                    forced |= triangle & ~zero_mask
            forced_count = forced.bit_count()
            zero_degrees = [0] * n
            for edge_index, (a, b) in enumerate(edges):
                if zero_mask >> edge_index & 1:
                    earlier = a if rank[a] < rank[b] else b
                    zero_degrees[earlier] += 1
            require(sum(zero_degrees) == zero_mask.bit_count(), "zero-edge orientation drift")
            require(
                all(degree * (degree - 1) // 2 <= forced_count for degree in zero_degrees),
                "forced-unit clique bound failed",
            )
            z = zero_mask.bit_count()
            require(
                z <= n or (z - n) ** 2 <= 2 * forced_count * n * n,
                "elimination zero/unit inequality failed",
            )

        tau = edge_count - maximum_surviving
        fractional, dual = fractional_packing(edge_count, triangles)
        z = sum(weight == 0 for weight in dual)
        h = sum(weight == 1 for weight in dual)
        gap = 2 * fractional - tau
        require(gap >= h, "unit-edge deletion bound failed")
        require(gap >= Fraction(edge_count, 6) - Fraction(2 * z, 3), "zero-edge gap failed")
        if n:
            claimed = Fraction(edge_count * edge_count, 50 * n * n) - Fraction(2 * n, 3)
            require(gap >= claimed, "finite fractional theorem failed")
            positive_bounds += claimed > 0
        digest_records.append((graph_mask, str(fractional), tau, z, h, str(gap)))
        lp_cases += 1
    data = repr(digest_records).encode()
    return {
        "chordal_graphs": chordal,
        "exact_fractional_pairs": lp_cases,
        "zero_edge_sets": zero_cases,
        "positive_theorem_bounds": positive_bounds,
    }, data


def scalar_checks() -> dict[str, int]:
    density_cases = type_cases = complete_cases = positive_complete = 0
    for numerator in range(1, 50):
        beta = Fraction(numerator, 100)
        eta = beta * beta / 400
        require(2 * eta == beta * beta / 200, "density rounding budget")
        density_cases += 1
    for r in range(1, 101):
        a = 8 * r + 11
        eta = Fraction(1, 64 * a * (r + 1) ** 2)
        require(2 * eta * (r + 1) ** 2 == Fraction(1, 32 * a), "type rounding budget")
        threshold = 1
        while threshold * threshold < 8 * threshold + 128 * (r + 1):
            threshold += 1
        root_argument = 16 + 128 * (r + 1)
        root_floor = isqrt(root_argument)
        published = 4 + root_floor + int(root_floor * root_floor < root_argument)
        require(threshold == published, "threshold drift")
        require(Fraction(3, 32 * a) - Fraction(1, 32 * a) == Fraction(1, 16 * a), "margin algebra")
        type_cases += 1
    # Nonvacuous all-order controls.  For K_n, uniform triangle weight
    # 1/(n-2) gives nu*=binom(n,2)/3 and Mantel's theorem gives
    # tau=binom(n,2)-floor(n^2/4).
    for n in range(3, 1001):
        edges = n * (n - 1) // 2
        fractional = Fraction(edges, 3)
        tau = edges - n * n // 4
        gap = 2 * fractional - tau
        claimed = Fraction(edges * edges, 50 * n * n) - Fraction(2 * n, 3)
        require(gap >= claimed, "complete-graph fractional bound")
        complete_cases += 1
        positive_complete += claimed > 0
    return {
        "density_scalar_cases": density_cases,
        "type_scalar_cases": type_cases,
        "complete_graph_controls": complete_cases,
        "positive_complete_graph_bounds": positive_complete,
    }


def main() -> None:
    require(len(sys.argv) == 1, "usage: python3 independent_check.py")
    require(sys.version_info >= (3, 11), "CPython 3.11+ required")
    expected_counts = [1, 1, 2, 8, 61, 822, 18154]
    totals = {
        "chordal_graphs": 0,
        "exact_fractional_pairs": 0,
        "zero_edge_sets": 0,
        "positive_theorem_bounds": 0,
    }
    record_hash = sha256()
    per_order = []
    for n in range(7):
        counts, records = graph_audit(n)
        require(counts["chordal_graphs"] == expected_counts[n], f"order-{n} census drift")
        per_order.append(counts["chordal_graphs"])
        for key in totals:
            totals[key] += counts[key]
        record_hash.update(records)
    output = {
        "status": "VERIFIED",
        "arithmetic": "exact Python int and Fraction",
        "chordal_graph_counts": per_order,
        "exact_record_sha256": record_hash.hexdigest(),
        **totals,
        **scalar_checks(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
