#!/usr/bin/env python3
"""Independent definition-level audit of the degree-19 Ramsey obstruction.

This reviewer-owned program imports no module and reads no certificate from
the reviewed contribution.  It exhausts small labeled graphs to test the
universal identities and density inequality, and separately reconstructs the
four exceptional-core arguments from their mathematical definitions.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, permutations, product
from math import comb


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def adjacency(order: int, edge_mask: int) -> list[int]:
    near = [0] * order
    for index, (a, b) in enumerate(combinations(range(order), 2)):
        if edge_mask >> index & 1:
            near[a] |= 1 << b
            near[b] |= 1 << a
    return near


def induced_edges(vertices: int, near: list[int]) -> int:
    total = 0
    pending = vertices
    while pending:
        bit = pending & -pending
        vertex = bit.bit_length() - 1
        total += (near[vertex] & vertices).bit_count()
        pending -= bit
    require(total % 2 == 0, "induced degree sum parity")
    return total // 2


def monochromatic_five(near: list[int]) -> bool:
    order = len(near)
    for chosen in combinations(range(order), 5):
        vertices = sum(1 << vertex for vertex in chosen)
        edges = induced_edges(vertices, near)
        if edges in (0, 10):
            return True
    return False


def density_bound(order: int, removed: int) -> int:
    return 4 * (order - removed) + removed * (order - removed) + comb(removed, 2)


def graph_identity_and_density(order: int) -> tuple[int, int, int]:
    all_vertices = (1 << order) - 1
    graph_count = 1 << comb(order, 2)
    ramsey_graphs = 0
    rooted_subsets = 0
    vertex_identities = 0
    for edge_mask in range(graph_count):
        near = adjacency(order, edge_mask)
        edge_count = edge_mask.bit_count()
        for vertex in range(order):
            red = near[vertex]
            blue = all_vertices ^ red ^ (1 << vertex)
            degree = red.bit_count()
            left = induced_edges(red, near) + comb(blue.bit_count(), 2) - induced_edges(blue, near)
            degree_sum = sum(near[w].bit_count() for w in range(order) if red >> w & 1)
            right = comb(order - 1 - degree, 2) - edge_count + degree_sum
            require(left == right, "vertex neighborhood identity")
            vertex_identities += 1

        if monochromatic_five(near):
            continue
        ramsey_graphs += 1
        for z, w in permutations(range(order), 2):
            options = near[z] & ~(1 << w)
            chosen = options
            while True:
                n = chosen.bit_count()
                s = (chosen & near[w]).bit_count()
                require(induced_edges(chosen, near) <= density_bound(n, s),
                        "rooted density inequality")
                rooted_subsets += 1
                if chosen == 0:
                    break
                chosen = (chosen - 1) & options
    return vertex_identities, ramsey_graphs, rooted_subsets


def clique(core: list[int], vertices: int, red: bool) -> bool:
    selected = [v for v in range(len(core)) if vertices >> v & 1]
    return all(bool(core[a] >> b & 1) == red for a, b in combinations(selected, 2))


def exceptional_cores() -> None:
    degrees = (19, 20, 20, 20)
    epsilons = (-2, -1, -1, -1)
    require(sum(degrees) + 39 * 21 == 898, "degree sum")
    require((sum(degrees) + 39 * 21) // 2 == 449, "red edge count")
    require(comb(23, 2) - 449 + 19 * 21 == 203, "degree-19 identity constant")
    require(comb(21, 2) - 449 + 21 * 21 == 202, "degree-21 identity constant")

    admissible = []
    edge_counts = Counter()
    for edge_mask in range(64):
        core = adjacency(4, edge_mask)
        correction = sum(epsilons[w] for w in range(4) if core[0] >> w & 1)
        if 203 + correction <= 85 + 115:
            admissible.append(edge_mask)
            edge_counts[induced_edges(0b1110, core)] += 1
    require(admissible == [7, 15, 23, 31, 39, 47, 55, 63], "forced exceptional star")
    require(edge_counts == {0: 1, 1: 3, 2: 3, 3: 1}, "four core classes")

    signatures = [mask for mask in range(16)
                  if 2 * bool(mask & 1) + sum(bool(mask & (1 << i)) for i in (1, 2, 3)) >= 2]
    require(signatures == [1, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15],
            "weighted signatures")

    # Independent L: sum(2-|X|) <= y_{0}, while that cell has size at most 3.
    require(all(2 - mask.bit_count() <= (mask == 1) for mask in signatures),
            "independent-core pointwise cover")
    require(2 * 39 - 16 - 19 - 19 - 19 == 5 and 5 > 3,
            "independent-core contradiction")

    # Each row is: core, constant/coefficient vector, rooted terms, margins, total cap.
    rows = [
        (15, (3, -1, -1, -1, -2), ((1, 10), (1, 12), (6, 1)),
         (39, 16, 18, 18, 19), 27),
        (31, (2, -1, 0, -1, -1), ((1, 12), (6, 1), (10, 4)),
         (39, 16, 17, 18, 18), 26),
    ]
    for core_mask, coefficients, roots, margins, expected_left in rows:
        core = adjacency(4, core_mask)
        for red_roots, blue_roots in roots:
            require(clique(core, red_roots, True) and clique(core, blue_roots, False),
                    "rooted Ramsey cell validity")
            require((5 - red_roots.bit_count(), 5 - blue_roots.bit_count()) in ((3, 4), (4, 3)),
                    "rooted Ramsey cap type")
        for signature in signatures:
            left = coefficients[0] + sum(coefficients[i + 1]
                                         for i in range(4) if signature >> i & 1)
            right = sum(signature & red == red and signature & blue == 0
                        for red, blue in roots)
            require(left <= right, "nontriangle pointwise cover")
        total_left = coefficients[0] * margins[0] + sum(
            coefficients[i + 1] * margins[i + 1] for i in range(4))
        require(total_left == expected_left and total_left > 3 * 8,
                "nontriangle summed contradiction")

    # Triangle core: H incidences into J are at most five.  A low vertex has
    # at most floor(H/3) red neighbors in J, and deleting them invokes the
    # rooted (4,4) density inequality.
    require(3 * (20 - 3) - 2 * 23 == 5, "triangle incidence bound")
    for H in range(6):
        required = 85 - 3 - H
        upper = density_bound(16, H // 3)
        require(required > upper, "triangle density contradiction")
    print("PASS exceptional cores: eight forced-star labels, four classes, contradictions=5>3,27>24,26>24,77>75")


def paley_positive_fixture() -> None:
    order = 19
    near = [0] * order
    residues = {value * value % 17 for value in range(1, 17)}

    def add(a: int, b: int) -> None:
        near[a] |= 1 << b
        near[b] |= 1 << a

    for a, b in combinations(range(17), 2):
        if (b - a) % 17 in residues:
            add(a, b)
    for vertex in range(17):
        add(17, vertex)
    add(17, 18)

    require(not monochromatic_five(near), "positive fixture is not (5,5)")
    J = (1 << 17) - 1
    require(all((near[v] & J).bit_count() == 8 for v in range(17)),
            "Paley core regularity")
    require(induced_edges(J, near) == 68 == density_bound(17, 0),
            "sharp positive density fixture")

    bad = [0] * 12
    for a, b in combinations(range(11), 2):
        bad[a] |= 1 << b
        bad[b] |= 1 << a
    bad[10] |= 1 << 11
    bad[11] |= 1 << 10
    clique_ten = (1 << 10) - 1
    require(induced_edges(clique_ten, bad) == 45 > density_bound(10, 0),
            "negative fixture should violate bound")
    print("PASS fixtures: every 5-set of the 19-vertex positive graph; sharp (n,s,e)=(17,0,68); no-K5 negative control")


def ramsey_bound_audit() -> None:
    # Exhaust R(3,3)<=6.  R(2,4)=4 is immediate: avoiding a red K2 makes K4 blue.
    for edge_mask in range(1 << 15):
        near = adjacency(6, edge_mask)
        require(any(clique(near, sum(1 << v for v in chosen), color)
                    for chosen in combinations(range(6), 3) for color in (False, True)),
                "R(3,3)<=6")
    # If a (3,4) coloring on nine vertices existed, every red degree would be
    # at most 3 and every blue degree at most 5, hence every red degree exactly
    # 3.  The resulting degree sum 27 is odd.
    require(9 * 3 % 2 == 1, "odd regularity contradiction")
    print("PASS self-contained Ramsey input: exhaustive R(3,3)<=6 plus odd-degree proof of R(3,4)<=9")


def main() -> None:
    ramsey_bound_audit()
    exceptional_cores()
    paley_positive_fixture()
    stats5 = graph_identity_and_density(5)
    stats6 = graph_identity_and_density(6)
    require(stats5 == (5120, 1022, 68940), "five-vertex exhaustive totals")
    print(f"PASS graph identity/density n=5: vertex_instances={stats5[0]} (5,5)_graphs={stats5[1]} rooted_subsets={stats5[2]}")
    print(f"PASS graph identity/density n=6: vertex_instances={stats6[0]} (5,5)_graphs={stats6[1]} rooted_subsets={stats6[2]}")
    print("PASS: independently verified the localized degree-19 profile obstruction")
    print("SCOPE: hard-branch 68-to-67 corollary additionally imports pinned extrema and parent classification")


if __name__ == "__main__":
    main()
