#!/usr/bin/env python3
"""Independent exact audit of the M=214 order-three symmetry restriction.

No reviewed module is imported.  The checker exhausts the fixed-vertex cases
from the theorem, validates both counting identities on every labeled graph
through order six, and reads the sharpness fixture directly from its edge list.
"""

from __future__ import annotations

import hashlib
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "ramsey_r55_m214_symmetry_audit" / "degree_incidence43.edges"
FIXTURE_SHA256 = "e01e328dd8da11eafe59940c3db23e998abebb52ce2316bf18c3b588f7a792ba"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def fixed_vertex_obstruction() -> None:
    scanned = congruent = survivors = 0
    case_counts = []
    for moving_cycles in (14, 13):
        fixed = 43 - 3 * moving_cycles
        for fixed_exceptional in range(fixed + 1):
            fixed_central = fixed - fixed_exceptional
            if (13 - fixed_exceptional) < 0 or (13 - fixed_exceptional) % 3:
                continue
            if (30 - fixed_central) < 0 or (30 - fixed_central) % 3:
                continue
            pairs = list(combinations(range(fixed), 2))
            local_scanned = local_congruent = local_survivors = 0
            residue_sums = Counter()
            for mask in range(1 << len(pairs)):
                local_scanned += 1
                degree = [0] * fixed
                exceptional_neighbors = [0] * fixed
                for bit, (u, v) in enumerate(pairs):
                    if not (mask >> bit) & 1:
                        continue
                    degree[u] += 1
                    degree[v] += 1
                    exceptional_neighbors[u] += v < fixed_exceptional
                    exceptional_neighbors[v] += u < fixed_exceptional
                if any(degree[v] % 3 != (2 if v < fixed_exceptional else 0)
                       for v in range(fixed)):
                    continue
                local_congruent += 1
                # Since every nonnegative orbit excess is at most two, its
                # value is the least residue of the fixed E-neighbor count.
                excess = [value % 3 for value in exceptional_neighbors]
                residue_sums[sum(excess)] += 1
                local_survivors += sum(excess) == 2
            scanned += local_scanned
            congruent += local_congruent
            survivors += local_survivors
            case_counts.append((moving_cycles, fixed_exceptional, local_scanned,
                                local_congruent, dict(residue_sums), local_survivors))
    require(scanned == 129, "fixed-graph scan total")
    require(congruent == 3 and survivors == 0, "fixed-graph obstruction")
    require(case_counts == [
        (14, 1, 1, 0, {}, 0),
        (13, 1, 64, 0, {}, 0),
        (13, 4, 64, 3, {8: 3}, 0),
    ], "fixed-case classification")
    print("PASS fixed vertices: 129 labeled graphs, 3 degree-congruent cases, 0 residue-budget survivors")


def all_graph_identity_audit(order: int = 6) -> None:
    pairs = list(combinations(range(order), 2))
    instances = 0
    for mask in range(1 << len(pairs)):
        adjacency = [set() for _ in range(order)]
        edges = set()
        for bit, edge in enumerate(pairs):
            if (mask >> bit) & 1:
                u, v = edge
                adjacency[u].add(v)
                adjacency[v].add(u)
                edges.add(edge)
        degrees = [len(neighbors) for neighbors in adjacency]
        red_triangles = sum(all(tuple(sorted(edge)) in edges for edge in combinations(triple, 2))
                            for triple in combinations(range(order), 3))
        blue_triangles = sum(all(tuple(sorted(edge)) not in edges for edge in combinations(triple, 2))
                             for triple in combinations(range(order), 3))
        goodman = comb(order, 3) - sum(d * (order - 1 - d) for d in degrees) // 2
        require(red_triangles + blue_triangles == goodman, "Goodman identity")
        for vertex in range(order):
            neighbors = adjacency[vertex]
            nonneighbors = set(range(order)) - neighbors - {vertex}
            red_local = sum(tuple(sorted(edge)) in edges for edge in combinations(neighbors, 2))
            blue_local = sum(tuple(sorted(edge)) not in edges for edge in combinations(nonneighbors, 2))
            rhs = (comb(order - 1 - degrees[vertex], 2) - len(edges)
                   + sum(degrees[w] for w in neighbors))
            require(red_local + blue_local == rhs, "neighborhood identity")
            instances += 1
    require(instances == 196608, "identity instance total")
    print("PASS identities: all 32768 labeled order-6 graphs and 196608 rooted instances")


def fixture_audit() -> None:
    require(hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA256,
            "fixture hash")
    lines = [tuple(map(int, line.split())) for line in FIXTURE.read_text().splitlines()]
    require(lines[0] == (43, 445), "fixture header")
    edges = set(lines[1:])
    require(len(edges) == len(lines) - 1 == 445, "fixture edges")
    require(all(0 <= u < v < 43 for u, v in edges), "fixture edge range")
    adjacency = [set() for _ in range(43)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    degrees = [len(row) for row in adjacency]
    require(Counter(degrees) == {20: 13, 21: 30}, "fixture degree profile")
    exceptional = {v for v, degree in enumerate(degrees) if degree == 20}
    incidence = [len(row & exceptional) for row in adjacency]
    require(min(incidence) == 6 and sum(value - 6 for value in incidence) == 2,
            "fixture incidence budget")
    sigma = [3 * (v // 3) + (v + 1) % 3 if v < 36 else v for v in range(43)]
    require(len(set(sigma)) == 43 and all(sigma[sigma[sigma[v]]] == v for v in range(43)),
            "fixture permutation")
    image = {tuple(sorted((sigma[u], sigma[v]))) for u, v in edges}
    require(image == edges, "fixture automorphism")
    blue_five = (0, 1, 2, 40, 41)
    require(all(tuple(sorted(edge)) not in edges for edge in combinations(blue_five, 2)),
            "fixture independent five-set")
    red_local = [sum(tuple(sorted(edge)) in edges for edge in combinations(row, 2))
                 for row in adjacency]
    failures = [v for v in range(43)
                if red_local[v] != (93 if v in exceptional else 100)]
    require(failures == list(range(43)), "fixture local-equality failures")
    require(sum(sigma[v] != v for v in range(43)) == 36, "fixture moving vertices")
    print("PASS fixture: 43 vertices, 445 edges, degree profile 20^13 21^30, twelve moving cycles, explicit blue K5")


def branch_arithmetic() -> None:
    red_edges = (13 * 20 + 30 * 21) // 2
    mono = comb(43, 3) - (13 * 20 * 22 + 30 * 21 * 21) // 2
    red_cap_sum = 13 * 93 + 30 * 100
    blue_cap_sum = 13 * 107 + 30 * 100
    total_excess = red_cap_sum + blue_cap_sum - 3 * mono
    require((red_edges, mono, red_cap_sum, blue_cap_sum, total_excess)
            == (445, 2866, 4209, 4391, 2), "branch totals")
    require([value for value in range(total_excess + 1)
             if (red_cap_sum - value) % 3 == 0] == [0], "red exactness")
    for degree, red_cap, blue_cap in ((20, 93, 107), (21, 100, 100)):
        for a in range(14):
            local_total = comb(42 - degree, 2) - red_edges + 21 * degree - a
            require(local_total == 206 - a, "specialized neighborhood identity")
            require(blue_cap - (local_total - red_cap) == a - 6,
                    "blue-deficiency identity")
    require(13 * 20 - 43 * 6 == 2, "incidence excess")
    require(445 - 21 - 100 - 110 == 214, "anchor cut")

    patterns = []
    for moving in (10, 11, 12):
        for exceptional_moving in range(5):
            fixed_exceptional = 13 - 3 * exceptional_moving
            fixed_central = 30 - 3 * (moving - exceptional_moving)
            if fixed_exceptional >= 0 and fixed_central >= 3:
                patterns.append((moving, exceptional_moving, fixed_exceptional, fixed_central))
    require(patterns == [
        (10, 1, 10, 3), (10, 2, 7, 6), (10, 3, 4, 9), (10, 4, 1, 12),
        (11, 2, 7, 3), (11, 3, 4, 6), (11, 4, 1, 9),
        (12, 3, 4, 3), (12, 4, 1, 6),
    ], "degree-class patterns")

    variables = comb(43, 2) + comb(43, 3)
    constraints = 2 * comb(43, 5) + 4 * comb(43, 3) + 4 * 43 - 1
    equalities = 43 + 43 + 42
    require((variables, constraints, equalities) == (13244, 1974731, 128),
            "OPB dimensions")
    print("PASS M=214 arithmetic: m=445 mono=2866 red/blue=1403/1463 excess=2 anchor_cut=214")
    print("PASS conditional range: moving_cycles=10..12 across 9 necessary degree-class patterns")
    print("PASS OPB dimensions: variables=13244 constraints=1974731 equalities=128 (no solver verdict)")


def main() -> None:
    fixed_vertex_obstruction()
    all_graph_identity_audit()
    fixture_audit()
    branch_arithmetic()
    print("PASS: independently verified the standalone symmetry lemma and conditional M=214 corollary")
    print("SCOPE: upstream hard-branch classification and minimum-ten theorem are imported; no M=214 SAT/UNSAT result is claimed")


if __name__ == "__main__":
    main()
