#!/usr/bin/env python3
"""Exact consistency/provenance audit for the hand proof in README.md.

No SAT solver, catalog enumeration, or claimed 43-vertex Ramsey witness.
Graph edges are lexicographically ordered unordered pairs on 0,...,n-1.
"""

from hashlib import sha256
from itertools import combinations
from math import comb
from pathlib import Path


U = dict(zip(range(18, 25), (85, 92, 100, 107, 114, 122, 132)))
IMPORTED = {
    "BACKBONE_ESCAPE_PROFILES.txt": "48f6310b77c7e3e2439f4fa780275dce660fdfd4d8fc030fc2bebf25b310db26",
    "verify_anchor_propagation.py": "05543d5552a373ddc457c463db6f19850535987bf7b4cb2c31d4494821cb67fb",
    "EXPECTED_OUTPUT.txt": "dafc86e61e8d6d803cfe30f5c7868c7d286fa46e888c798d7c09d6941b74edc7",
    "singleton_sat.py": "022db19e2d3fc8d8738ce49a904bedc3068ece6cfd3f37d3576f86d947cce0d5",
    "EXPECTED_SINGLETON_SAT.txt": "e86185dc04ff5d5c1548b0e4f32098c641fa95ae3e848f652c851a45c09e390b",
    "EXPECTED_SINGLETON_LOCAL_SAT.txt": "b74a0f83cd67965c7ba05c80a2ae59652b1401877f0dacc758b97c3d689dcd07",
    "SINGLETON_TYPED_BRANCHES.tsv": "e4ba765ae7bad943ea132d8a1ad37824840aea7e7ea3da29ec98c8521617cab2",
    "SINGLETON_TYPED_STABILIZED_BRANCHES.tsv": "ddf8c30014e35fbf005381078d1804089283d3cbddad5ef2c1cb1b36d91315cf",
}


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise AssertionError(detail)


def literal_counts(n: int, edges: set[tuple[int, int]]):
    """Direct induced-edge definition, separate from the degree identity."""
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        require(0 <= a < b < n, (n, a, b))
        adjacency[a].add(b)
        adjacency[b].add(a)
    degrees = [len(neighbors) for neighbors in adjacency]
    pairs = []
    vertices = set(range(n))
    for v in range(n):
        red = adjacency[v]
        blue = vertices - red - {v}
        t_r = sum((a, b) in edges for a, b in combinations(sorted(red), 2))
        t_b = sum((a, b) not in edges for a, b in combinations(sorted(blue), 2))
        pairs.append((t_r, t_b))
    return adjacency, degrees, pairs


def check_graph(n: int, edges: set[tuple[int, int]]):
    adjacency, degrees, pairs = literal_counts(n, edges)
    for v, (t_r, t_b) in enumerate(pairs):
        expected = comb(n - 1 - degrees[v], 2) - len(edges)
        expected += sum(degrees[w] for w in adjacency[v])
        require(t_r + t_b == expected, (n, sorted(edges), v, pairs[v], expected))
    return adjacency, degrees, pairs


def partitions(total: int, minimum: int = 1):
    if total == 0:
        yield ()
    for first in range(minimum, total + 1):
        for rest in partitions(total - first, first):
            yield (first,) + rest


def component_caps(budget: int, order_caps: dict[int, int]):
    rows = []
    for total in range(2, budget + 1):
        for partition in partitions(total):
            if len(partition) >= 2:
                rows.append((partition, sum(order_caps[a] for a in partition)))
    return rows


def local_pairs(total: int, red_cap: int, blue_cap: int):
    return [(red, total - red) for red in range(red_cap + 1)
            if 0 <= total - red <= blue_cap]


def main() -> None:
    graphs = vertex_checks = 0
    for n in range(7):
        edge_order = tuple(combinations(range(n), 2))
        for mask in range(1 << len(edge_order)):
            edges = {edge for i, edge in enumerate(edge_order) if (mask >> i) & 1}
            check_graph(n, edges)
            graphs += 1
            vertex_checks += n
    require((graphs, vertex_checks) == (33868, 202013), (graphs, vertex_checks))
    print("PASS identity on every labeled graph n=0..6: graphs=33868 vertices=202013")

    # A 20-regular circulant plus 21 disjoint nonedges; vertex 42 is unmatched.
    n, z = 43, 42
    edges = {(a, b) for a, b in combinations(range(n), 2)
             if min(b - a, n - (b - a)) <= 10}
    matching = {(i, i + 21) for i in range(21)}
    require(not (edges & matching), "fixture matching must consist of nonedges")
    edges |= matching
    adjacency, degrees, pairs = check_graph(n, edges)
    require(degrees == [21] * 42 + [20] and len(edges) == 451, degrees)
    for v in range(n):
        require(sum(pairs[v]) == (200 if v == z else 200 - int(z in adjacency[v])),
                (v, pairs[v]))
    require(all(edge in edges for edge in combinations(range(5), 2)), "fixture K5")
    print("PASS non-Ramsey n=43 fixture: m=451 degrees=20^1,21^42; explicit red K5")

    require(local_pairs(200, 100, 100) == [(100, 100)], "blue to z")
    require(local_pairs(199, 100, 100) == [(99, 100), (100, 99)], "red to z")
    require(local_pairs(200, U[20] - 7, U[22] - 7) == [(93, 107)], "vertex z")
    require(comb(22, 2) - 107 == 124, "red edges on D")
    print("PASS forced local pairs: blue-to-z=(100,100); red-to-z=(99,100)/(100,99)")
    print("PASS z=(93,107); D=N_B(z) has order 22 and red/blue edges 124/107")

    blue_rows = component_caps(4, {1: 3, 2: 8, 3: 17})
    red_rows = component_caps(3, {1: 4, 2: 13})
    require(blue_rows == [((1, 1), 6), ((1, 1, 1), 9), ((1, 2), 11),
                          ((1, 1, 1, 1), 12), ((1, 1, 2), 14),
                          ((1, 3), 20), ((2, 2), 16)], blue_rows)
    require(red_rows == [((1, 1), 8), ((1, 1, 1), 12), ((1, 2), 17)], red_rows)
    require(22 - max(cap for _, cap in blue_rows) == 2, blue_rows)
    require(22 - max(cap for _, cap in red_rows) == 5, red_rows)
    print("PASS disconnected order caps: (4,5)<=20, (5,4)<=17; kappa blue>=2 red>=5")
    require(21 - 17 == 4 and 21 - 13 == 8, "internal degree intervals")
    print("PASS internal degree intervals on D: blue=4..13 red=8..17")

    red_d_forced = comb(22, 2) - 107
    red_d_base = 100 + 21
    require((red_d_forced, red_d_base) == (124, 121), "singleton contradiction")
    require(red_d_forced - 21 == 103 != 100, "anchor contradiction")
    print("PASS singleton local-profile contradiction: e_R(D)=124 and 121; 103!=100")

    offsets = [comb(42 - d, 2) + 21*d - U[d] - U[42 - d] + 14 - 231
               for d in range(18, 25)]
    require(offsets == [220, 221, 220, 220, 221, 223, 223], offsets)
    print("PASS degree-neighborhood offsets b(18..24)=220,221,220,220,221,223,223")

    prior = Path(__file__).resolve().parent.parent / "ramsey_r55_doubly_exact_anchor_propagation"
    for name, digest in IMPORTED.items():
        actual = sha256((prior / name).read_bytes()).hexdigest()
        require(actual == digest, (name, actual, digest))
    rows = [line for line in (prior / "BACKBONE_ESCAPE_PROFILES.txt").read_text().splitlines()
            if line and not line.startswith("#")]
    require(rows == ["220 3 22 0,0,0,21,0,0,0 0,0,1,20,0,0,0"], rows)
    require(348 + len(rows) == 349, "inherited profile count")
    print("PASS eight inherited source/profile/manifest hashes; sole historical escape=M220-W3")
    print("SCOPE hand-proof corollary closes all 349 profiles; inherited 348-profile proof not rerun")
    print("SCOPE local-profile/typed/stabilized formulas analytically inconsistent; base formula unresolved")


if __name__ == "__main__":
    main()
