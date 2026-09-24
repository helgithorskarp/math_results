#!/usr/bin/env python3
"""Independent exact checks for centered-triangle rounding.

This program imports no target source, output, or certificate.  It builds the
centered LP from the graph definition, solves it over the rationals, computes
the integer centered optimum by a separate matching-mask dynamic program, and
checks the proof's extreme-point counts.  It also exhausts the residual
triangle inequality on every graph through six vertices and evaluates exact
small split-graph packing and cover optima.

Requires CPython 3.11+ and only the standard library.
"""

from __future__ import annotations

from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
import json


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def rank(matrix: list[list[int | F]]) -> int:
    rows = [[F(value) for value in row] for row in matrix]
    if not rows:
        return 0
    pivot_row = 0
    for column in range(len(rows[0])):
        pivot = next((i for i in range(pivot_row, len(rows)) if rows[i][column]), None)
        if pivot is None:
            continue
        rows[pivot_row], rows[pivot] = rows[pivot], rows[pivot_row]
        scale = rows[pivot_row][column]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for i in range(len(rows)):
            if i == pivot_row or not rows[i][column]:
                continue
            scale = rows[i][column]
            rows[i] = [a - scale * b for a, b in zip(rows[i], rows[pivot_row])]
        pivot_row += 1
        if pivot_row == len(rows):
            break
    return pivot_row


def lp_system(
    k: int,
    neighborhoods: tuple[tuple[int, ...], ...],
    multiplicities: tuple[int, ...],
    base_edges: tuple[tuple[int, int], ...],
) -> tuple[list[list[int]], list[int], tuple[tuple[int, int, int], ...], int]:
    edge_index = {edge: i for i, edge in enumerate(base_edges)}
    spoke_rows = tuple((i, v) for i, s in enumerate(neighborhoods) for v in s)
    spoke_index = {item: len(base_edges) + j for j, item in enumerate(spoke_rows)}
    variables = tuple(
        (i, u, v)
        for i, s in enumerate(neighborhoods)
        for u, v in combinations(s, 2)
        if (u, v) in edge_index
    )
    row_count = len(base_edges) + len(spoke_rows)
    matrix = [[0] * len(variables) for _ in range(row_count)]
    for j, (i, u, v) in enumerate(variables):
        matrix[edge_index[u, v]][j] = 1
        matrix[spoke_index[i, u]][j] = 1
        matrix[spoke_index[i, v]][j] = 1
    rhs = [1] * len(base_edges) + [multiplicities[i] for i, _ in spoke_rows]
    return matrix, rhs, variables, len(base_edges)


def rational_packing_lp(
    matrix: list[list[int]], rhs: list[int]
) -> tuple[F, list[F], list[F]]:
    """Exact slack-basis simplex with a largest-improvement pivot rule."""
    row_count = len(matrix)
    variable_count = len(matrix[0]) if matrix else 0
    if not variable_count:
        return F(0), [], [F(0)] * row_count
    width = variable_count + row_count
    rows = []
    for i, source in enumerate(matrix):
        rows.append(
            [F(value) for value in source]
            + [F(i == j) for j in range(row_count)]
            + [F(rhs[i])]
        )
    objective = [-F(1)] * variable_count + [F(0)] * row_count + [F(0)]
    basis = list(range(variable_count, width))
    pivots = 0
    while True:
        improving = [j for j, value in enumerate(objective[:-1]) if value < 0]
        if not improving:
            break
        entering = min(improving, key=lambda j: (objective[j], j))
        candidates = [i for i in range(row_count) if rows[i][entering] > 0]
        require(bool(candidates), "unbounded packing LP")
        leaving = min(
            candidates,
            key=lambda i: (rows[i][-1] / rows[i][entering], basis[i]),
        )
        pivot = rows[leaving][entering]
        rows[leaving] = [value / pivot for value in rows[leaving]]
        for i in range(row_count):
            if i == leaving or not rows[i][entering]:
                continue
            scale = rows[i][entering]
            rows[i] = [a - scale * b for a, b in zip(rows[i], rows[leaving])]
        scale = objective[entering]
        objective = [a - scale * b for a, b in zip(objective, rows[leaving])]
        basis[leaving] = entering
        pivots += 1
        require(pivots < 10000, "simplex pivot limit")

    primal = [F(0)] * variable_count
    for i, variable in enumerate(basis):
        if variable < variable_count:
            primal[variable] = rows[i][-1]
    dual = objective[variable_count:width]
    loads = [sum((F(a) * x for a, x in zip(row, primal)), F(0)) for row in matrix]
    require(all(x >= 0 for x in primal + dual), "negative LP coordinate")
    require(all(load <= bound for load, bound in zip(loads, rhs)), "primal infeasible")
    require(
        all(sum((dual[i] * matrix[i][j] for i in range(row_count)), F(0)) >= 1
            for j in range(variable_count)),
        "dual infeasible",
    )
    value = sum(primal, F(0))
    require(value == sum((y * b for y, b in zip(dual, rhs)), F(0)), "duality gap")
    support = [j for j, x in enumerate(primal) if x]
    active = [i for i, (load, bound) in enumerate(zip(loads, rhs)) if load == bound]
    require(
        rank([[matrix[i][j] for j in support] for i in active]) == len(support),
        "returned optimum is not an extreme point",
    )
    return value, primal, dual


def all_matching_masks(k: int, allowed_mask: int, base_edges: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    result = []
    for mask in range(1 << len(base_edges)):
        if mask & ~allowed_mask:
            continue
        used_vertices = 0
        valid = True
        for j, (u, v) in enumerate(base_edges):
            if not (mask >> j) & 1:
                continue
            bits = (1 << u) | (1 << v)
            if used_vertices & bits:
                valid = False
                break
            used_vertices |= bits
        if valid:
            result.append(mask)
    return tuple(result)


def allocate_centers(
    k: int,
    neighborhoods: tuple[tuple[int, ...], ...],
    multiplicities: tuple[int, ...],
    base_edges: tuple[tuple[int, int], ...],
    available_mask: int | None = None,
) -> int:
    """Definition-level integer optimum via one matching choice per center."""
    if available_mask is None:
        available_mask = (1 << len(base_edges)) - 1
    edge_index = {edge: i for i, edge in enumerate(base_edges)}
    reachable = {0}
    for s, multiplicity in zip(neighborhoods, multiplicities):
        vertices = set(s)
        allowed = sum(
            1 << edge_index[edge]
            for edge in base_edges
            if set(edge) <= vertices and (available_mask >> edge_index[edge]) & 1
        )
        choices = all_matching_masks(k, allowed, base_edges)
        for _ in range(multiplicity):
            reachable = {
                used | choice
                for used in reachable
                for choice in choices
                if not used & choice
            }
    return max((mask.bit_count() for mask in reachable), default=0)


def local_saturation(
    k: int,
    neighborhoods: tuple[tuple[int, ...], ...],
    multiplicities: tuple[int, ...],
) -> bool:
    for u, v in combinations(range(k), 2):
        load = sum(
            (F(m, len(s) - 1) for s, m in zip(neighborhoods, multiplicities)
             if u in s and v in s),
            F(0),
        )
        if load > 1:
            return False
    return True


def instance_audit() -> tuple[dict[str, object], bytes]:
    cases = saturated = local_certificates = nonintegral = 0
    worst_gap = F(0)
    worst_ratio = F(0)
    worst_record: tuple[object, ...] = ()
    digest = sha256()
    full_split_samples: list[tuple[int, tuple[tuple[int, ...], ...], tuple[int, ...]]] = []

    for k in range(2, 5):
        complete_edges = tuple(combinations(range(k), 2))
        subsets = tuple(
            subset
            for size in range(2, k + 1)
            for subset in combinations(range(k), size)
        )
        type_lists = []
        for subset in subsets:
            for m in range(1, min(3, len(subset)) + 1):
                type_lists.append(((subset,), (m,)))
        for first, second in combinations(subsets, 2):
            for m1 in (1, 2):
                for m2 in (1, 2):
                    type_lists.append(((first, second), (m1, m2)))

        for base_mask in range(1 << len(complete_edges)):
            base_edges = tuple(
                edge for j, edge in enumerate(complete_edges) if (base_mask >> j) & 1
            )
            for neighborhoods, multiplicities in type_lists:
                matrix, rhs, variables, base_rows = lp_system(
                    k, neighborhoods, multiplicities, base_edges
                )
                value, primal, _ = rational_packing_lp(matrix, rhs)
                integer = allocate_centers(k, neighborhoods, multiplicities, base_edges)
                D = sum(map(len, neighborhoods))
                gap = value - integer
                require(gap <= F(3 * D, 2), "centered rounding theorem failed")

                loads = [sum((F(a) * x for a, x in zip(row, primal)), F(0)) for row in matrix]
                support = [j for j, x in enumerate(primal) if x]
                tight_base = sum(loads[i] == 1 for i in range(base_rows))
                require(len(support) <= tight_base + D, "support count failed")
                unit_variables = [j for j, x in enumerate(primal) if x == 1]
                fractional_edges = {
                    tuple(sorted((u, v)))
                    for j, (i, u, v) in enumerate(variables)
                    if primal[j] not in (0, 1)
                }
                require(len(fractional_edges) <= D, "fractional-edge count failed")
                require(value - len(unit_variables) <= D, "floor loss failed")

                unit_by_type = []
                edge_index = {edge: i for i, edge in enumerate(base_edges)}
                for type_index in range(len(neighborhoods)):
                    mask = sum(
                        1 << edge_index[u, v]
                        for j, (i, u, v) in enumerate(variables)
                        if i == type_index and primal[j] == 1
                    )
                    unit_by_type.append(mask)
                kept = 0
                for i, mask in enumerate(unit_by_type):
                    kept += allocate_centers(
                        k,
                        (neighborhoods[i],),
                        (multiplicities[i],),
                        base_edges,
                        mask,
                    )
                require(len(unit_variables) - kept <= F(D, 2), "coloring loss failed")
                require(kept >= value - F(3 * D, 2), "constructed rounding failed")

                if gap:
                    nonintegral += 1
                ratio = gap / D if D else F(0)
                if ratio > worst_ratio or (ratio == worst_ratio and gap > worst_gap):
                    worst_gap, worst_ratio = gap, ratio
                    worst_record = (k, base_mask, neighborhoods, multiplicities, str(value), integer)

                if base_mask == (1 << len(complete_edges)) - 1:
                    E = sum(len(s) * m for s, m in zip(neighborhoods, multiplicities))
                    if 2 * value == E:
                        saturated += 1
                        if len(full_split_samples) < 160:
                            full_split_samples.append((k, neighborhoods, multiplicities))
                    if local_saturation(k, neighborhoods, multiplicities):
                        require(2 * value == E, "local certificate did not saturate")
                        local_certificates += 1

                digest.update(repr((k, base_mask, neighborhoods, multiplicities, str(value), integer)).encode())
                cases += 1

    return ({
        "exact_lp_integer_pairs": cases,
        "nonintegral_instances": nonintegral,
        "spoke_saturated_complete_base_instances": saturated,
        "local_saturation_certificates": local_certificates,
        "worst_observed_gap": str(worst_gap),
        "worst_observed_gap_over_D": str(worst_ratio),
        "worst_record": repr(worst_record),
        "deterministic_records_sha256": digest.hexdigest(),
        "full_split_samples": full_split_samples,
    }, digest.digest())


def residual_graph_audit() -> dict[str, int]:
    graphs = triangles = 0
    for k in range(1, 7):
        edges = tuple(combinations(range(k), 2))
        for mask in range(1 << len(edges)):
            chosen = {edge for j, edge in enumerate(edges) if (mask >> j) & 1}
            tris = [
                triple for triple in combinations(range(k), 3)
                if set(combinations(triple, 2)) <= chosen
            ]
            e = len(chosen)
            require(F(len(tris)) >= F(e * (4 * e - k * k), 3 * k),
                    "degree-sum triangle bound failed")
            classes = [[] for _ in range(k)]
            for triple in tris:
                classes[sum(triple) % k].append(triple)
            require(max(map(len, classes), default=0) >= F(len(tris), k),
                    "modular averaging failed")
            for family in classes:
                used = set()
                for triple in family:
                    triangle_edges = set(combinations(triple, 2))
                    require(not used & triangle_edges, "modular class is not a packing")
                    used |= triangle_edges
            graphs += 1
            triangles += len(tris)
    return {"graphs_through_order_six": graphs, "triangles_seen": triangles}


def full_split_optima(
    k: int,
    neighborhoods: tuple[tuple[int, ...], ...],
    multiplicities: tuple[int, ...],
) -> tuple[int, int]:
    edges: list[tuple[int, int]] = list(combinations(range(k), 2))
    centers: list[tuple[int, tuple[int, ...]]] = []
    next_vertex = k
    for s, m in zip(neighborhoods, multiplicities):
        for _ in range(m):
            centers.append((next_vertex, s))
            edges.extend((min(next_vertex, v), max(next_vertex, v)) for v in s)
            next_vertex += 1
    edge_index = {edge: i for i, edge in enumerate(edges)}
    triangle_masks = []
    for triple in combinations(range(k), 3):
        triangle_masks.append(sum(1 << edge_index[e] for e in combinations(triple, 2)))
    for center, s in centers:
        for u, v in combinations(s, 2):
            triangle_edges = ((u, v), (u, center), (v, center))
            triangle_masks.append(
                sum(1 << edge_index[min(a, b), max(a, b)] for a, b in triangle_edges)
            )
    triangle_masks = tuple(sorted(set(triangle_masks)))
    count = len(triangle_masks)
    conflict = [0] * count
    incident = [0] * len(edges)
    for i, first in enumerate(triangle_masks):
        for j, second in enumerate(triangle_masks):
            if first & second:
                conflict[i] |= 1 << j
        for edge in range(len(edges)):
            if (first >> edge) & 1:
                incident[edge] |= 1 << i

    @lru_cache(None)
    def packing(remaining: int) -> int:
        if not remaining:
            return 0
        indices = [i for i in range(count) if (remaining >> i) & 1]
        chosen = max(indices, key=lambda i: (remaining & conflict[i]).bit_count())
        without = remaining & ~(1 << chosen)
        return max(packing(without), 1 + packing(remaining & ~conflict[chosen]))

    @lru_cache(None)
    def cover(remaining: int) -> int:
        if not remaining:
            return 0
        chosen = (remaining & -remaining).bit_length() - 1
        return 1 + min(
            cover(remaining & ~incident[edge])
            for edge in range(len(edges))
            if (triangle_masks[chosen] >> edge) & 1
        )

    all_triangles = (1 << count) - 1
    return packing(all_triangles), cover(all_triangles)


def corollary_audit(samples: list[tuple[int, tuple[tuple[int, ...], ...], tuple[int, ...]]]) -> dict[str, object]:
    exact_graphs = 0
    minimum_gap: int | None = None
    for k, neighborhoods, multiplicities in samples:
        nu, tau = full_split_optima(k, neighborhoods, multiplicities)
        r = len(neighborhoods)
        bound = (F(k * k, 66) - (F(1, 2) + F(12 * r, 11)) * k
                 + F(5, 12) - 4 * r - F(48 * r * r, 11))
        require(2 * nu - tau >= bound, "conditional Tuza inequality failed")
        gap = 2 * nu - tau
        minimum_gap = gap if minimum_gap is None else min(minimum_gap, gap)
        exact_graphs += 1

    identities = thresholds = tangent_cases = 0
    for r in range(1, 51):
        for u in range(21):
            k = 80 * r + 40 + u
            claimed = (F(k * k, 66) - (F(1, 2) + F(12 * r, 11)) * k
                       + F(5, 12) - 4 * r - F(48 * r * r, 11))
            expanded = (F(u * u, 66) + (F(4 * r, 3) + F(47, 66)) * u
                        + F(16 * r * r, 3) + F(28 * r, 3) + F(205, 44))
            require(claimed == expanded > 0, "explicit threshold identity failed")
            thresholds += 1
        for k in (2, 3, 7, 31, 280):
            for numerator in range(41):
                t = F(numerator, 40)
                raw = k * k * (F(1, 12) - t / 2 + F(11, 12) * t * t) - 4 * r * k * t
                low = F(k * k, 66) - F(12 * r * k, 11) - F(48 * r * r, 11)
                center = F(3, 11) + F(24 * r, 11 * k)
                require(raw - low == F(11 * k * k, 12) * (t - center) ** 2,
                        "square completion failed")
                identities += 1
    for k in range(2, 101):
        q = F(k * (k - 1), 2)
        for H_num in range(0, 21):
            H = q * H_num / 20
            derivative = F(4, 3 * k) + F(8 * H, 3 * k * k)
            value_H = F(k * k, 6) - F(k, 2) + F(1, 3) + F(4 * H, 3 * k) + F(4 * H * H, 3 * k * k)
            for D in range(0, 2 * k + 1):
                h = max(F(0), H - F(3 * D, 2))
                value_h = F(k * k, 6) - F(k, 2) + F(1, 3) + F(4 * h, 3 * k) + F(4 * h * h, 3 * k * k)
                require(value_h >= value_H - F(3 * D, 2) * derivative,
                        "convex tangent step failed")
                tangent_cases += 1
    return {
        "exact_saturated_split_optima": exact_graphs,
        "minimum_exact_2nu_minus_tau": minimum_gap,
        "square_completion_cases": identities,
        "threshold_cases": thresholds,
        "convex_tangent_cases": tangent_cases,
    }


def sharpness_audit() -> dict[str, int]:
    cases = 0
    for k in range(3, 32, 2):
        edges = tuple(combinations(range(k), 2))
        color_classes: dict[int, list[tuple[int, int]]] = {color: [] for color in range(k)}
        for edge in edges:
            color_classes[sum(edge) % k].append(edge)
        for family in color_classes.values():
            require(len(family) == (k - 1) // 2, "round-robin class size")
            require(len({v for edge in family for v in edge}) == k - 1, "class is not a matching")
        packed = sum(len(color_classes[color]) for color in range(k - 1))
        require(F(len(edges) - packed) == F(k - 1, 2), "sharpness gap failed")
        cases += 1
    return {"odd_complete_split_families": cases, "largest_clique": 31}


def main() -> None:
    instance_stats, record_digest = instance_audit()
    samples = instance_stats.pop("full_split_samples")
    output = {
        "status": "INDEPENDENT_CENTERED_ROUNDING_REVIEW_PASSED",
        "instances": instance_stats,
        "residual_graphs": residual_graph_audit(),
        "conditional_corollary": corollary_audit(samples),
        "sharpness": sharpness_audit(),
        "method": (
            "independent exact rational LP; matching-mask integer optimization; "
            "definition-level split packing/cover recursion; exhaustive residual graphs"
        ),
        "record_digest_redundancy": record_digest.hex(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
