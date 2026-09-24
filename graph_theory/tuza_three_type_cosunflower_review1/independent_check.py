#!/usr/bin/env python3
"""Independent exact checks for the three-type co-sunflower theorem.

This checker imports no target code, report, or certificate.  It constructs
the small graphs directly from disjoint complement cells, computes their
packing and covering numbers by generic branching, and evaluates the claimed
analytic bounds using rational arithmetic and literal bipartition searches.
It also recounts the complete finite domain in neighborhood-size coordinates.

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


def clique_packing(k: int) -> int:
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
    p: tuple[int, int, int]
    c: int
    d: int
    m: tuple[int, int, int]

    @property
    def u(self) -> int:
        return sum(self.p) + self.c

    @property
    def k(self) -> int:
        return self.u + self.d

    @property
    def neighborhoods(self) -> tuple[frozenset[int], ...]:
        result = []
        start = 0
        universe = frozenset(range(self.u))
        for size in self.p:
            result.append(universe - frozenset(range(start, start + size)))
            start += size
        return tuple(result)


def graph_data(instance: Instance) -> tuple[list[tuple[int, int]], list[tuple[int, int, int]]]:
    """Construct the actual graph and list every triangle by edge indices."""
    edges = {tuple(edge) for edge in combinations(range(instance.k), 2)}
    center = instance.k
    for neighborhood, copies in zip(instance.neighborhoods, instance.m):
        for _ in range(copies):
            edges.update((vertex, center) for vertex in neighborhood)
            center += 1
    ordered_edges = sorted(edges)
    edge_id = {edge: index for index, edge in enumerate(ordered_edges)}
    triangles = []
    for vertices in combinations(range(center), 3):
        pairs = [tuple(pair) for pair in combinations(vertices, 2)]
        if all(pair in edge_id for pair in pairs):
            triangles.append(tuple(sorted(edge_id[pair] for pair in pairs)))
    return ordered_edges, triangles


def exact_triangle_cover(edge_count: int, triangles: list[tuple[int, int, int]]) -> int:
    """Minimum hitting set by generic branch-and-bound."""
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

    def greedy_cover(remaining: int) -> int:
        used = 0
        while remaining:
            edge = max(
                range(edge_count),
                key=lambda e: (remaining & edge_to_triangles[e]).bit_count(),
            )
            remaining &= ~edge_to_triangles[edge]
            used += 1
        return used

    def greedy_packing(remaining: int) -> int:
        used = 0
        while remaining:
            candidates = []
            scan = remaining
            while scan:
                low = scan & -scan
                index = low.bit_length() - 1
                candidates.append(index)
                scan ^= low
            index = min(candidates, key=lambda i: (remaining & conflicts[i]).bit_count())
            remaining &= ~conflicts[index]
            used += 1
        return used

    full = (1 << len(triangles)) - 1
    incumbent = greedy_cover(full)
    seen_depth: dict[int, int] = {}

    def search(remaining: int, depth: int) -> None:
        nonlocal incumbent
        if not remaining:
            incumbent = min(incumbent, depth)
            return
        if depth >= incumbent or depth + greedy_packing(remaining) >= incumbent:
            return
        previous = seen_depth.get(remaining)
        if previous is not None and previous <= depth:
            return
        seen_depth[remaining] = depth
        incumbent = min(incumbent, depth + greedy_cover(remaining))

        candidates = []
        scan = remaining
        while scan:
            low = scan & -scan
            index = low.bit_length() - 1
            score = sum(
                (remaining & edge_to_triangles[edge]).bit_count()
                for edge in triangles[index]
            )
            candidates.append((score, index))
            scan ^= low
        triangle_index = max(candidates)[1]
        incidences = [remaining & edge_to_triangles[e] for e in triangles[triangle_index]]
        branches = []
        for position, incidence in enumerate(incidences):
            dominated = any(
                position != other
                and incidence | incidences[other] == incidences[other]
                and (incidence != incidences[other] or other < position)
                for other in range(3)
            )
            if not dominated:
                branches.append(incidence)
        for incidence in sorted(branches, key=int.bit_count, reverse=True):
            search(remaining & ~incidence, depth + 1)

    search(full, 0)
    return incumbent


def exact_triangle_packing(edge_count: int, triangles: list[tuple[int, int, int]]) -> int:
    """Maximum edge-disjoint family by generic include/exclude branching."""
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
        edge = max(
            range(edge_count),
            key=lambda e: (remaining & edge_to_triangles[e]).bit_count(),
        )
        incident = remaining & edge_to_triangles[edge]
        require(incident != 0, "triangle state has no represented edge")
        best = solve(remaining & ~incident)
        scan = incident
        while scan:
            low = scan & -scan
            index = low.bit_length() - 1
            best = max(best, 1 + solve(remaining & ~conflicts[index]))
            scan ^= low
        return best

    return solve((1 << len(triangles)) - 1)


def literal_cut_cover(instance: Instance, edges: list[tuple[int, int]]) -> int:
    """Enumerate every clique bipartition and all center-type placements."""
    answer = len(edges)
    starts = [instance.k]
    for copies in instance.m[:-1]:
        starts.append(starts[-1] + copies)

    def center_type(vertex: int) -> int:
        for index in range(2, -1, -1):
            if vertex >= starts[index]:
                return index
        raise RuntimeError("not a center")

    for clique_mask in range(1 << instance.k):
        for type_mask in range(8):
            def side(vertex: int) -> int:
                if vertex < instance.k:
                    return (clique_mask >> vertex) & 1
                return (type_mask >> center_type(vertex)) & 1

            deleted = sum(side(a) == side(b) for a, b in edges)
            answer = min(answer, deleted)
    return answer


def claimed_lower_bound(instance: Instance) -> tuple[int, int]:
    """Compute B and h with Fractions and exhaustive shared-palette allocation."""
    sizes = tuple(len(s) for s in instance.neighborhoods)
    colors = tuple(palette_count(s) for s in sizes)
    h1 = sum(
        Fraction(instance.m[i] * choose2(sizes[i]), colors[i]) for i in range(3)
    )
    for i, j in combinations(range(3), 2):
        intersection = len(instance.neighborhoods[i] & instance.neighborhoods[j])
        h1 -= Fraction(
            instance.m[i] * instance.m[j] * choose2(intersection),
            colors[i] * colors[j],
        )
    common = len(set.intersection(*(set(s) for s in instance.neighborhoods)))
    h1 += Fraction(
        instance.m[0] * instance.m[1] * instance.m[2] * choose2(common),
        colors[0] * colors[1] * colors[2],
    )
    h2 = max(
        Fraction(sum(a[i] * choose2(sizes[i]) for i in range(3)), palette_count(instance.u))
        for a0 in range(instance.m[0] + 1)
        for a1 in range(instance.m[1] + 1)
        for a2 in range(instance.m[2] + 1)
        for a in [(a0, a1, a2)]
        if sum(a) <= palette_count(instance.u)
    )
    h = ceil_fraction(max(h1, h2))
    q = choose2(instance.k)
    p = clique_packing(instance.k)
    residual = Fraction(
        p * (q - h) * (4 * (q - h) - instance.k * instance.k),
        3 * instance.k * choose3(instance.k),
    )
    return max(p, h, ceil_fraction(Fraction(h) + residual)), h


def canonical_instances(last_k: int):
    for k in range(3, last_k + 1):
        for u in range(3, k + 1):
            d = k - u
            for p0 in range(u // 3 + 1):
                for p1 in range(max(1, p0), u + 1):
                    for p2 in range(p1, u + 1):
                        if p0 + p1 + p2 > u or u - p2 < 2:
                            continue
                        c = u - p0 - p1 - p2
                        sizes = (u - p0, u - p1, u - p2)
                        for m0 in range(1, sizes[0]):
                            for m1 in range(1, sizes[1]):
                                for m2 in range(1, sizes[2]):
                                    yield Instance((p0, p1, p2), c, d, (m0, m1, m2))


def full_domain(last: int) -> tuple[int, int, int]:
    """Count shapes and tuples using ordered neighborhood sizes, not p-cells."""
    shapes = tuples = analytic = 0
    for u in range(3, last + 1):
        for s0 in range(2, u + 1):
            for s1 in range(2, min(s0, u - 1) + 1):
                lower = max(2, 2 * u - s0 - s1)
                for s2 in range(lower, s1 + 1):
                    multiplicities = (s0 - 1) * (s1 - 1) * (s2 - 1)
                    outside_values = last - u + 1
                    finite_max = min(last - u, max(2, 54 - u))
                    skipped = last - u - finite_max
                    shapes += 1
                    tuples += multiplicities * outside_values
                    analytic += multiplicities * skipped
    return shapes, tuples, analytic


def quartic_certificate() -> dict[str, str]:
    coefficients = [
        Fraction(1, 12), Fraction(-1, 2), Fraction(11, 12),
        Fraction(-4, 9), Fraction(2, 27),
    ]
    a = Fraction(9, 25)
    value = sum(coefficient * a**power for power, coefficient in enumerate(coefficients))
    derivative = sum(
        power * coefficient * a ** (power - 1)
        for power, coefficient in enumerate(coefficients) if power
    )
    lower = value - 9 * derivative * derivative
    require(value == Fraction(6191, 2343750), "quartic value mismatch")
    require(derivative == Fraction(16, 15625), "quartic derivative mismatch")
    require(lower == Fraction(3855551, 1464843750) > Fraction(1, 400), "quartic gap")
    at_199 = Fraction(199 * 199, 400) - Fraction(199, 2) - Fraction(1, 4)
    outside_55 = Fraction(31 * 55 * 55, 3456) - Fraction(55, 2) - Fraction(1, 4)
    require(-1 < at_199 < 0, "order-199 integrality bridge")
    require(-1 < outside_55 < 0, "outside-tail integrality bridge")
    return {
        "gap": str(lower),
        "order_199_margin": str(at_199),
        "outside_55_margin": str(outside_55),
    }


def main() -> None:
    require(len(sys.argv) == 1, "usage: python3 independent_check.py")
    require(sys.version_info >= (3, 11), "CPython 3.11+ required")
    # Solver controls use only abstract triangle-edge incidences.  They catch
    # a vacuous or off-by-one optimization routine before graph instances are
    # considered.
    controls = [
        (3, [(0, 1, 2)], 1, 1),
        (6, [(0, 1, 2), (3, 4, 5)], 2, 2),
        (5, [(0, 1, 2), (0, 3, 4)], 1, 1),
    ]
    for edge_count, triangles, expected_nu, expected_tau in controls:
        require(
            exact_triangle_packing(edge_count, triangles) == expected_nu,
            "packing solver control failed",
        )
        require(
            exact_triangle_cover(edge_count, triangles) == expected_tau,
            "cover solver control failed",
        )
    records = []
    cases = equality = lower_tight = cover_tight = 0
    minimum_slack = None
    for instance in canonical_instances(5):
        edges, triangles = graph_data(instance)
        nu = exact_triangle_packing(len(edges), triangles)
        tau = exact_triangle_cover(len(edges), triangles)
        lower, h = claimed_lower_bound(instance)
        upper = literal_cut_cover(instance, edges)
        label = (*instance.p, instance.c, instance.d, *instance.m)
        require(lower <= nu, f"packing bound exceeds optimum at {label}")
        require(tau <= upper, f"cut bound below optimum at {label}")
        require(tau <= 2 * nu, f"Tuza inequality fails at {label}")
        slack = 2 * nu - tau
        minimum_slack = slack if minimum_slack is None else min(minimum_slack, slack)
        equality += int(slack == 0)
        lower_tight += int(lower == nu)
        cover_tight += int(upper == tau)
        records.append((*label, len(edges), len(triangles), nu, tau, lower, upper, h))
        cases += 1

    require(cases == 237, "small-instance domain drift")
    shapes, tuples, analytic = full_domain(198)
    require((shapes, tuples, analytic) == (11539903, 497893855660344, 441165614683344), "full-domain mismatch")
    output = {
        "status": "VERIFIED",
        "exact_small_instances": cases,
        "exact_record_sha256": sha256(repr(records).encode()).hexdigest(),
        "tuza_equality_instances": equality,
        "minimum_exact_slack": minimum_slack,
        "packing_bound_tight_instances": lower_tight,
        "cut_bound_tight_instances": cover_tight,
        "full_shapes": shapes,
        "full_parameter_tuples": tuples,
        "analytically_certified_tuples": analytic,
        "quartic_certificate": quartic_certificate(),
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
