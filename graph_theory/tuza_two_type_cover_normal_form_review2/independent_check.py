#!/usr/bin/env python3
"""Independent exact audit of the two-neighborhood split-graph normal form.

The exact oracles below use only definitions:

* enumerate triangle-free clique cores and their independence numbers;
* solve maximum triangle-free subgraph by branching on a surviving triangle;
* enumerate all cuts directly.

Only the values under review are loaded from the sibling ``cover.py``.  None
of its host formula, feasibility logic, or certificate reconstruction is used
by the oracles.
"""

from functools import lru_cache
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import combinations, product
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tuza_two_type_cover_normal_form" / "cover.py"
SPEC = spec_from_file_location("candidate_cover", TARGET)
assert SPEC is not None and SPEC.loader is not None
CANDIDATE = module_from_spec(SPEC)
SPEC.loader.exec_module(CANDIDATE)


def edge_system(order):
    edges = tuple(combinations(range(order), 2))
    edge_index = {edge: i for i, edge in enumerate(edges)}
    triangles = tuple(
        sum(1 << edge_index[edge] for edge in combinations(vertices, 2))
        for vertices in combinations(range(order), 3)
    )
    return edges, triangles


@lru_cache(None)
def triangle_free_cores(order):
    """All triangle-free labelled clique cores, with all-set alpha tables."""
    edges, triangles = edge_system(order)
    records = []
    for mask in range(1 << len(edges)):
        if any(mask & triangle == triangle for triangle in triangles):
            continue
        adjacent = [0] * order
        for bit, (u, v) in enumerate(edges):
            if mask >> bit & 1:
                adjacent[u] |= 1 << v
                adjacent[v] |= 1 << u
        alpha = [0] * (1 << order)
        for vertices in range(1, 1 << order):
            low = vertices & -vertices
            vertex = low.bit_length() - 1
            rest = vertices ^ low
            alpha[vertices] = max(
                alpha[rest], 1 + alpha[rest & ~adjacent[vertex]]
            )
        records.append((mask.bit_count(), tuple(alpha)))
    return tuple(records)


def exact_two_type_tau(a, b, c, d, multiplicity_s, multiplicity_t):
    """Definition-level split-cover optimum via all triangle-free cores."""
    order = a + b + c + d
    all_clique_edges = order * (order - 1) // 2
    set_s = (1 << (c + a)) - 1
    set_t = ((1 << c) - 1) | (((1 << b) - 1) << (c + a))
    size_s, size_t = a + c, b + c
    return min(
        all_clique_edges
        - core_edges
        + multiplicity_s * (size_s - alpha[set_s])
        + multiplicity_t * (size_t - alpha[set_t])
        for core_edges, alpha in triangle_free_cores(order)
    )


def protected_host(x, y, z, w):
    """Edges of K_W join (K_{Y,Z} disjoint union I_X)."""
    start_y = x
    start_z = x + y
    start_w = x + y + z
    class_y = set(range(start_y, start_z))
    class_z = set(range(start_z, start_w))
    class_w = set(range(start_w, start_w + w))
    edges = []
    for u, v in combinations(range(x + y + z + w), 2):
        if u in class_w or v in class_w:
            edges.append((u, v))
        elif (u in class_y and v in class_z) or (u in class_z and v in class_y):
            edges.append((u, v))
    return tuple(edges)


def maximum_triangle_free_edges(order, host_edges):
    """Exact optimum by minimum-deletion branching on present triangles."""
    all_edges, all_triangles = edge_system(order)
    global_index = {edge: bit for bit, edge in enumerate(all_edges)}
    host_mask = sum(1 << global_index[edge] for edge in host_edges)

    @lru_cache(None)
    def deletions(mask):
        triangle = next(
            (triangle for triangle in all_triangles if mask & triangle == triangle),
            None,
        )
        if triangle is None:
            return 0
        choices = [bit for bit in range(len(all_edges)) if triangle >> bit & 1]
        return 1 + min(deletions(mask ^ (1 << bit)) for bit in choices)

    return len(host_edges) - deletions(host_mask)


def maximum_cut(order, edges):
    """Exact cut enumeration with vertex zero fixed on one side."""
    if order == 0:
        return 0
    return max(
        sum(((side >> u) ^ (side >> v)) & 1 for u, v in edges)
        for side in range(1 << (order - 1))
    )


def obstruction_host(t):
    """The three-type allowed clique host from the sharpness construction."""
    order = 2 * t + 3
    vertex_v, vertex_c, vertex_d = 0, 1, 2
    class_p = set(range(3, t + 3))
    class_q = set(range(t + 3, order))
    neighborhoods = (
        class_p | {vertex_d},
        class_p | class_q,
        {vertex_c} | class_q,
    )
    return order, tuple(
        edge
        for edge in combinations(range(order), 2)
        if not any(set(edge) <= neighborhood for neighborhood in neighborhoods)
    )


def check_two_type_values():
    digest = sha256()
    cases = 0
    by_order = {}
    multiplicities = (0, 1, 2, 5)
    for order in range(7):
        order_cases = 0
        for a in range(order + 1):
            for b in range(order - a + 1):
                for c in range(order - a - b + 1):
                    d = order - a - b - c
                    for multiplicity_s, multiplicity_t in product(
                        multiplicities, repeat=2
                    ):
                        parameters = (
                            a,
                            b,
                            c,
                            d,
                            multiplicity_s,
                            multiplicity_t,
                        )
                        exact = exact_two_type_tau(*parameters)
                        claimed = CANDIDATE.solve(*parameters)["tau"]
                        assert exact == claimed, (parameters, exact, claimed)
                        digest.update(
                            (json.dumps([parameters, exact]) + "\n").encode()
                        )
                        cases += 1
                        order_cases += 1
        by_order[str(order)] = order_cases
    return {
        "cases": cases,
        "cases_by_clique_order": by_order,
        "record_sha256": digest.hexdigest(),
    }


def check_protected_hosts():
    digest = sha256()
    cases = 0
    by_order = {}
    for order in range(8):
        order_cases = 0
        for x in range(order + 1):
            for y in range(order - x + 1):
                for z in range(order - x - y + 1):
                    w = order - x - y - z
                    host_edges = protected_host(x, y, z, w)
                    triangle_free = maximum_triangle_free_edges(order, host_edges)
                    cut = maximum_cut(order, host_edges)
                    claimed = CANDIDATE.host_optimum(x, y, z, w)["value"]
                    assert triangle_free == cut == claimed, (
                        (x, y, z, w),
                        triangle_free,
                        cut,
                        claimed,
                    )
                    digest.update(
                        (
                            json.dumps([[x, y, z, w], triangle_free, cut])
                            + "\n"
                        ).encode()
                    )
                    cases += 1
                    order_cases += 1
        by_order[str(order)] = order_cases
    return {
        "cases": cases,
        "cases_by_order": by_order,
        "record_sha256": digest.hexdigest(),
    }


def check_three_type_boundary():
    records = []
    for t in range(2, 9):
        order, edges = obstruction_host(t)
        triangle_free = maximum_triangle_free_edges(order, edges)
        cut = maximum_cut(order, edges)
        assert len(edges) == 4 * t + 3
        assert triangle_free == 4 * t + 1
        assert cut == 4 * t
        records.append(
            {
                "t": t,
                "host_edges": len(edges),
                "triangle_free": triangle_free,
                "maximum_cut": cut,
            }
        )
    return records


def main():
    result = {
        "target": str(TARGET.relative_to(ROOT)),
        "two_type_exact_oracle": check_two_type_values(),
        "protected_host_exact_oracle": check_protected_hosts(),
        "three_type_boundary": check_three_type_boundary(),
    }
    canonical = json.dumps(result, indent=2, sort_keys=True) + "\n"
    result["summary_sha256_before_self_field"] = sha256(canonical.encode()).hexdigest()
    expected_path = Path(__file__).with_name("EXPECTED_OUTPUT.json")
    if expected_path.exists():
        expected = json.loads(expected_path.read_text())
        assert result == expected, ("unexpected output", result)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
