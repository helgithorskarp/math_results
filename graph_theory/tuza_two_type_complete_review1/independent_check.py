#!/usr/bin/env python3
"""Independent exact checks for the two-neighborhood split-graph proof.

This program imports no target code or generated output.  It reconstructs
the labelled graphs from the four Venn-cell sizes, computes exact triangle
packing and covering numbers for every capped tuple with 3 <= k <= 5, and
checks the paper's lower and upper bounds against those exact optima.  It
also recounts the complete finite domain in independent (s,t,c) coordinates.

Requires CPython 3.11+ and only the standard library.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import cache
from hashlib import sha256
from itertools import combinations
import json
import sys


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def choose2(x: int) -> int:
    return x * (x - 1) // 2


def choose3(x: int) -> int:
    return x * (x - 1) * (x - 2) // 6


def ceil_fraction(x: Fraction) -> int:
    return -(-x.numerator // x.denominator)


def palette_count(x: int) -> int:
    if x < 2:
        return 1
    return x if x % 2 else x - 1


def clique_packing_formula(k: int) -> int:
    if k < 3:
        return 0
    residue = k % 6
    if residue in (1, 3):
        leave = 0
    elif residue == 5:
        leave = 4
    else:
        leave = k // 2 + int(residue == 4)
    return (choose2(k) - leave) // 3


@dataclass(frozen=True)
class Instance:
    a: int
    b: int
    c: int
    d: int
    m: int
    n: int

    @property
    def k(self) -> int:
        return self.a + self.b + self.c + self.d

    @property
    def s_vertices(self) -> frozenset[int]:
        # A=S\T, B=T\S, X=S intersection T, D=outside.
        return frozenset(range(self.a)) | frozenset(
            range(self.a + self.b, self.a + self.b + self.c)
        )

    @property
    def t_vertices(self) -> frozenset[int]:
        return frozenset(range(self.a, self.a + self.b)) | frozenset(
            range(self.a + self.b, self.a + self.b + self.c)
        )


def graph_data(instance: Instance) -> tuple[list[tuple[int, int]], list[tuple[int, int, int]]]:
    """Return actual graph edges and triangles as triples of edge indices."""
    k = instance.k
    edges = {tuple(edge) for edge in combinations(range(k), 2)}
    for center in range(k, k + instance.m):
        edges.update((vertex, center) for vertex in instance.s_vertices)
    for center in range(k + instance.m, k + instance.m + instance.n):
        edges.update((vertex, center) for vertex in instance.t_vertices)
    ordered_edges = sorted(edges)
    edge_id = {edge: index for index, edge in enumerate(ordered_edges)}

    triangles: list[tuple[int, int, int]] = []
    order = k + instance.m + instance.n
    for vertices in combinations(range(order), 3):
        pairs = [tuple(pair) for pair in combinations(vertices, 2)]
        if all(pair in edge_id for pair in pairs):
            triangles.append(tuple(sorted(edge_id[pair] for pair in pairs)))
    return ordered_edges, triangles


def exact_triangle_cover(edge_count: int, triangles: list[tuple[int, int, int]]) -> int:
    """Minimum hitting set by generic branch-and-bound.

    A greedy cover supplies an incumbent.  A greedy family of pairwise
    edge-disjoint remaining triangles supplies a rigorous lower bound.
    Neither routine uses the split-graph structure or the claimed cut form.
    """
    edge_to_triangles = [0] * edge_count
    for triangle_index, triangle in enumerate(triangles):
        bit = 1 << triangle_index
        for edge in triangle:
            edge_to_triangles[edge] |= bit

    conflicts = [0] * len(triangles)
    for index, triangle in enumerate(triangles):
        conflicts[index] = (
            edge_to_triangles[triangle[0]]
            | edge_to_triangles[triangle[1]]
            | edge_to_triangles[triangle[2]]
        )

    def greedy_cover_size(remaining: int) -> int:
        chosen = 0
        while remaining:
            edge = max(
                range(edge_count),
                key=lambda e: (remaining & edge_to_triangles[e]).bit_count(),
            )
            remaining &= ~edge_to_triangles[edge]
            chosen += 1
        return chosen

    def packing_lower_bound(remaining: int) -> int:
        chosen = 0
        while remaining:
            indices = []
            scan = remaining
            while scan:
                low = scan & -scan
                index = low.bit_length() - 1
                indices.append(index)
                scan ^= low
            index = min(indices, key=lambda i: (remaining & conflicts[i]).bit_count())
            remaining &= ~conflicts[index]
            chosen += 1
        return chosen

    full = (1 << len(triangles)) - 1
    incumbent = greedy_cover_size(full)
    seen_depth: dict[int, int] = {}

    def search(remaining: int, depth: int) -> None:
        nonlocal incumbent
        if not remaining:
            incumbent = min(incumbent, depth)
            return
        if depth >= incumbent:
            return
        previous = seen_depth.get(remaining)
        if previous is not None and previous <= depth:
            return
        seen_depth[remaining] = depth

        incumbent = min(incumbent, depth + greedy_cover_size(remaining))
        if depth + packing_lower_bound(remaining) >= incumbent:
            return

        # Branch on the triangle whose three possible cover edges have the
        # largest total current incidence.  Remove a locally dominated edge
        # choice whenever another edge of the same triangle covers a superset.
        candidate_indices = []
        scan = remaining
        while scan:
            low = scan & -scan
            index = low.bit_length() - 1
            score = sum(
                (remaining & edge_to_triangles[e]).bit_count() for e in triangles[index]
            )
            candidate_indices.append((score, index))
            scan ^= low
        _, triangle_index = max(candidate_indices)
        incidences = [remaining & edge_to_triangles[e] for e in triangles[triangle_index]]
        branches = []
        for position, incidence in enumerate(incidences):
            if any(
                position != other
                and incidence | incidences[other] == incidences[other]
                and (incidence != incidences[other] or other < position)
                for other in range(3)
            ):
                continue
            branches.append(incidence)
        for incidence in sorted(branches, key=int.bit_count, reverse=True):
            search(remaining & ~incidence, depth + 1)

    search(full, 0)
    return incumbent


def exact_triangle_packing(edge_count: int, triangles: list[tuple[int, int, int]]) -> int:
    """Maximum edge-disjoint family by exhaustive include/exclude branching.

    Choosing a graph edge partitions all packings into those using no
    triangle on that edge and those using one specified triangle on it.
    """
    triangle_masks = [sum(1 << edge for edge in triangle) for triangle in triangles]
    edge_to_triangles = [0] * edge_count
    conflicts = [0] * len(triangles)
    for index, triangle in enumerate(triangles):
        for edge in triangle:
            edge_to_triangles[edge] |= 1 << index
    for index, triangle in enumerate(triangles):
        conflicts[index] = (
            edge_to_triangles[triangle[0]]
            | edge_to_triangles[triangle[1]]
            | edge_to_triangles[triangle[2]]
        )

    @cache
    def solve(remaining: int) -> int:
        if not remaining:
            return 0
        active_edges = [
            (remaining & incident).bit_count() for incident in edge_to_triangles
        ]
        edge = max(range(edge_count), key=active_edges.__getitem__)
        incident = remaining & edge_to_triangles[edge]
        require(incident != 0, "remaining triangle has no represented edge")
        best = solve(remaining & ~incident)
        scan = incident
        while scan:
            low = scan & -scan
            index = low.bit_length() - 1
            best = max(best, 1 + solve(remaining & ~conflicts[index]))
            scan ^= low
        return best

    # Each selected object below is a three-edge triangle; this assertion
    # catches representation drift before the recurrence is trusted.
    require(all(mask.bit_count() == 3 for mask in triangle_masks), "bad triangle mask")
    return solve((1 << len(triangles)) - 1)


def cut_cover(instance: Instance, edges: list[tuple[int, int]]) -> int:
    """Definition-level minimum over all clique cuts and type placements."""
    k = instance.k
    answer = len(edges)
    for clique_mask in range(1 << k):
        for s_side in (0, 1):
            for t_side in (0, 1):
                def side(vertex: int) -> int:
                    if vertex < k:
                        return (clique_mask >> vertex) & 1
                    if vertex < k + instance.m:
                        return s_side
                    return t_side

                deleted = sum(side(u) == side(v) for u, v in edges)
                answer = min(answer, deleted)
    return answer


def claimed_lower_bound(instance: Instance) -> tuple[int, int]:
    """Evaluate B and h using Fractions and brute-force palette allocation."""
    s = instance.a + instance.c
    t = instance.b + instance.c
    u = instance.a + instance.b + instance.c
    rs, rt, ru = palette_count(s), palette_count(t), palette_count(u)
    first = (
        Fraction(instance.m * choose2(s), rs)
        + Fraction(instance.n * choose2(t), rt)
        - Fraction(instance.m * instance.n * choose2(instance.c), rs * rt)
    )
    second = max(
        Fraction(i * choose2(s) + j * choose2(t), ru)
        for i in range(instance.m + 1)
        for j in range(instance.n + 1)
        if i + j <= ru
    )
    h = ceil_fraction(max(first, second))
    q = choose2(instance.k)
    p = clique_packing_formula(instance.k)
    residual = Fraction(
        p * (q - h) * (4 * (q - h) - instance.k * instance.k),
        3 * instance.k * choose3(instance.k),
    )
    bound = max(p, h, ceil_fraction(Fraction(h) + residual))
    return bound, h


def canonical_instances(last_k: int):
    for k in range(3, last_k + 1):
        for a in range(k + 1):
            for b in range(min(a, k - a) + 1):
                for c in range(k - a - b + 1):
                    d = k - a - b - c
                    s, t = a + c, b + c
                    for m in range(max(1, s)):
                        for n in range(max(1, t)):
                            yield Instance(a, b, c, d, m, n)


def full_domain_count(last_k: int) -> tuple[int, int]:
    """Count in (s,t,c), not in the target checkers' (a,b,c,d) order."""
    shapes = tuples = 0
    for k in range(3, last_k + 1):
        for s in range(k + 1):
            for t in range(s + 1):
                for _c in range(max(0, s + t - k), t + 1):
                    shapes += 1
                    tuples += max(1, s) * max(1, t)
    return shapes, tuples


def main() -> None:
    require(len(sys.argv) == 1, "usage: python3 independent_check.py")
    require(sys.version_info >= (3, 11), "CPython 3.11+ required")
    control = Instance(0, 0, 0, 3, 0, 0)
    control_edges, control_triangles = graph_data(control)
    require(
        exact_triangle_packing(len(control_edges), control_triangles) == 1
        and exact_triangle_cover(len(control_edges), control_triangles) == 1,
        "K3 control failed",
    )
    records = []
    equality_cases = 0
    minimum_slack = None
    bound_tight = 0
    cover_tight = 0
    cases = 0
    for instance in canonical_instances(5):
        edges, triangles = graph_data(instance)
        nu = exact_triangle_packing(len(edges), triangles)
        tau = exact_triangle_cover(len(edges), triangles)
        lower, h = claimed_lower_bound(instance)
        upper = cut_cover(instance, edges)
        label = (instance.a, instance.b, instance.c, instance.d, instance.m, instance.n)
        require(lower <= nu, f"packing lower bound failed at {label}")
        require(tau <= upper, f"cover upper bound failed at {label}")
        require(tau <= 2 * nu, f"Tuza inequality failed at {label}")
        if instance.m == 0 and instance.n == 0:
            require(
                nu == clique_packing_formula(instance.k),
                f"complete-clique formula failed at {label}",
            )
        slack = 2 * nu - tau
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        equality_cases += int(slack == 0)
        bound_tight += int(lower == nu)
        cover_tight += int(upper == tau)
        records.append((*label, len(edges), len(triangles), nu, tau, lower, upper, h))
        cases += 1

    shapes, tuples = full_domain_count(112)
    require((shapes, tuples) == (3_642_650, 7_636_614_579), "full domain mismatch")
    threshold_gap = Fraction(113 * 113, 228) - Fraction(113, 2) - Fraction(1, 4)
    require(threshold_gap == Fraction(-85, 114), "threshold arithmetic mismatch")
    require(threshold_gap > -1 and Fraction(113, 114) - Fraction(1, 2) > 0,
            "large-order integrality threshold failed")

    encoded = "\n".join(" ".join(map(str, record)) for record in records).encode()
    report = {
        "status": "VERIFIED",
        "exact_cases_k3_to_k5": cases,
        "exact_tuza_equality_cases": equality_cases,
        "minimum_exact_slack_2nu_minus_tau": minimum_slack,
        "packing_bound_tight_cases": bound_tight,
        "cut_cover_tight_cases": cover_tight,
        "full_shapes_k3_to_k112": shapes,
        "full_parameter_tuples_k3_to_k112": tuples,
        "large_order_gap_at_k113": str(threshold_gap),
        "exact_record_sha256": sha256(encoded).hexdigest(),
    }
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
