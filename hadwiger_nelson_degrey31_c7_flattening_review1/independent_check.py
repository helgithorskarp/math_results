#!/usr/bin/env python3
"""Independent exact review of the D31 C7-equivariant planar-map gate.

This module imports no code or data from the reviewed package.  Its D31 edge
list is the literal one-based list extracted from the pinned Wolfram notebook.
"""

from collections import Counter
from hashlib import sha256
import json


SOURCE_EDGE_TEXT = """
1-2 1-7 1-9 1-14 1-17 1-22 1-24 1-29
2-3 2-8 2-10 2-16 2-18 2-23 2-25
3-4 3-9 3-11 3-17 3-19 3-24 3-26
4-5 4-10 4-12 4-18 4-20 4-25 4-27
5-6 5-11 5-13 5-19 5-21 5-26 5-28
6-7 6-12 6-14 6-20 6-22 6-27 6-29
7-8 7-13 7-16 7-21 7-23 7-28
8-15 8-17 8-22 8-30
9-15 9-16 9-18 9-30
10-15 10-17 10-19 10-30
11-15 11-18 11-20 11-30
12-15 12-19 12-21 12-30
13-15 13-20 13-22 13-30
14-15 14-16 14-21 14-30
15-23 15-24 15-25 15-26 15-27 15-28 15-29
16-31 17-31 18-31 19-31 20-31 21-31 22-31
23-31 24-31 25-31 26-31 27-31 28-31 29-31
"""

SOURCE_EDGE_SHA256 = "9691aadee6776f4e65e3dc2f3a5ff586b6d86b94c25bfc67e4dfaf819602b671"
SPINDLE_EDGE_SHA256 = "94b13354045197763850f16beebcfc0ccf22e74084fcb910fc981be6867bfb22"
OBSTRUCTION_EDGE_SHA256 = "d7b347593826292b12195070a61a7e4e3b58005bdb24d7d873b541a17dc75c90"


class CheckError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise CheckError(message)


def parse_edge_text(text, vertices=31):
    edges = set()
    tokens = text.split()
    for token in tokens:
        fields = token.split("-")
        require(len(fields) == 2 and all(field.isdigit() for field in fields),
                f"malformed edge token: {token!r}")
        left, right = (int(field) - 1 for field in fields)
        require(0 <= left < vertices and 0 <= right < vertices,
                f"endpoint outside 1..{vertices}: {token}")
        require(left != right, f"loop: {token}")
        edge = tuple(sorted((left, right)))
        require(edge not in edges, f"duplicate edge: {token}")
        edges.add(edge)
    return tuple(sorted(edges))


def edge_digest(edges):
    payload = "".join(f"{left + 1} {right + 1}\n" for left, right in edges)
    return sha256(payload.encode("ascii")).hexdigest()


def adjacency(vertices, edges):
    rows = [set() for _ in range(vertices)]
    for left, right in edges:
        require(0 <= left < vertices and 0 <= right < vertices and left != right,
                "invalid graph edge")
        rows[left].add(right)
        rows[right].add(left)
    return rows


def triangle_count(vertices, edges):
    rows = adjacency(vertices, edges)
    return sum(len(rows[left] & rows[right]) for left, right in edges) // 3


def sigma_image(vertex):
    for start in (0, 7, 15, 22):
        if start <= vertex < start + 7:
            return start + (vertex - start + 1) % 7
    return vertex


def verify_static_source(edges):
    require(len(edges) == 98, "D31 edge count changed")
    require(edge_digest(edges) == SOURCE_EDGE_SHA256, "D31 edge hash changed")
    require(triangle_count(31, edges) == 0, "D31 is not triangle-free")
    moved = tuple(sorted(tuple(sorted((sigma_image(a), sigma_image(b))))
                         for a, b in edges))
    require(moved == edges, "claimed C7 permutation is not an automorphism")
    return adjacency(31, edges)


def canonical_colouring_census(vertices, edges, colour_count, tracked=()):
    """Enumerate colourings modulo colour names by domain propagation.

    Colour names are introduced in restricted-growth order.  The next vertex
    is selected by current domain size, then static degree and index.  Those
    choices are invariant under permutation of already introduced colours, so
    every global colour-name orbit has exactly one leaf.
    """
    rows = adjacency(vertices, edges)
    domains = [(1 << colour_count) - 1] * vertices
    assigned = [-1] * vertices
    nodes = 0
    leaves = 0
    dead_ends = 0
    patterns = Counter()
    first_word = None

    def visit(done, maximum_colour):
        nonlocal nodes, leaves, dead_ends, first_word
        nodes += 1
        if done == vertices:
            leaves += 1
            if first_word is None:
                first_word = "".join(map(str, assigned))
            if tracked:
                patterns["".join(str(assigned[v]) for v in tracked)] += 1
            return

        vertex = min(
            (v for v in range(vertices) if assigned[v] < 0),
            key=lambda v: (domains[v].bit_count(), -len(rows[v]), v),
        )
        introduced_mask = (1 << min(colour_count, maximum_colour + 2)) - 1
        available = domains[vertex] & introduced_mask
        if not available:
            dead_ends += 1
            return

        while available:
            bit = available & -available
            available -= bit
            colour = bit.bit_length() - 1
            old_vertex_domain = domains[vertex]
            domains[vertex] = bit
            assigned[vertex] = colour
            trail = []
            viable = True
            for neighbour in rows[vertex]:
                if assigned[neighbour] < 0 and domains[neighbour] & bit:
                    trail.append((neighbour, domains[neighbour]))
                    domains[neighbour] &= ~bit
                    if not domains[neighbour]:
                        viable = False
                        break
            if viable:
                visit(done + 1, max(maximum_colour, colour))
            else:
                dead_ends += 1
            for neighbour, old_domain in reversed(trail):
                domains[neighbour] = old_domain
            assigned[vertex] = -1
            domains[vertex] = old_vertex_domain

    visit(0, -1)
    return {
        "nodes": nodes,
        "leaves": leaves,
        "dead_ends": dead_ends,
        "patterns": dict(sorted(patterns.items())),
        "first_word": first_word,
    }


def find_colouring(vertices, edges, colour_count):
    rows = adjacency(vertices, edges)
    domains = [(1 << colour_count) - 1] * vertices
    assigned = [-1] * vertices
    nodes = 0

    def visit(done, maximum_colour):
        nonlocal nodes
        nodes += 1
        if done == vertices:
            return True
        vertex = min(
            (v for v in range(vertices) if assigned[v] < 0),
            key=lambda v: (domains[v].bit_count(), -len(rows[v]), v),
        )
        available = domains[vertex] & ((1 << min(colour_count, maximum_colour + 2)) - 1)
        while available:
            bit = available & -available
            available -= bit
            colour = bit.bit_length() - 1
            old_vertex_domain = domains[vertex]
            domains[vertex] = bit
            assigned[vertex] = colour
            trail = []
            viable = True
            for neighbour in rows[vertex]:
                if assigned[neighbour] < 0 and domains[neighbour] & bit:
                    trail.append((neighbour, domains[neighbour]))
                    domains[neighbour] &= ~bit
                    if not domains[neighbour]:
                        viable = False
                        break
            if viable and visit(done + 1, max(maximum_colour, colour)):
                return True
            for neighbour, old_domain in reversed(trail):
                domains[neighbour] = old_domain
            assigned[vertex] = -1
            domains[vertex] = old_vertex_domain
        return False

    exists = visit(0, -1)
    word = "".join(map(str, assigned)) if exists else None
    return word, nodes


def build_spindle(edges31):
    shared = 30                 # source vertex 31, zero based
    joined = 29                 # source vertex 30, zero based
    second = {shared: shared}
    next_vertex = 31
    for vertex in range(31):
        if vertex != shared:
            second[vertex] = next_vertex
            next_vertex += 1
    require(next_vertex == 61, "bad spindle relabelling")
    edges = set(edges31)
    edges.update(tuple(sorted((second[a], second[b]))) for a, b in edges31)
    bridge = tuple(sorted((joined, second[joined])))
    require(bridge not in edges, "spindle bridge already present")
    edges.add(bridge)
    return tuple(sorted(edges)), second, bridge


def obstruction_edges(edges31):
    wanted = set()
    for j in range(7):
        wanted.add(tuple(sorted((j, (j + 1) % 7))))
        wanted.add(tuple(sorted((7 + j, 14))))
        wanted.add(tuple(sorted((j, 7 + (j - 1) % 7))))
        wanted.add(tuple(sorted((j, 7 + (j + 1) % 7))))
    require(wanted <= set(edges31), "28-edge obstruction is not a source subgraph")
    return tuple(sorted(wanted))


def poly_add(left, right):
    answer = [0] * max(len(left), len(right))
    for index, value in enumerate(left):
        answer[index] += value
    for index, value in enumerate(right):
        answer[index] += value
    while len(answer) > 1 and answer[-1] == 0:
        answer.pop()
    return answer


def poly_multiply(left, right):
    answer = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            answer[i + j] += a * b
    return answer


def main():
    edges31 = parse_edge_text(SOURCE_EDGE_TEXT)
    rows31 = verify_static_source(edges31)
    degree_histogram = dict(sorted(Counter(map(len, rows31)).items()))

    obstruction = obstruction_edges(edges31)
    require(len({v for edge in obstruction for v in edge}) == 15,
            "obstruction carrier should have 15 vertices")
    require(len(obstruction) == 28 and edge_digest(obstruction) == OBSTRUCTION_EDGE_SHA256,
            "obstruction subgraph changed")

    three = canonical_colouring_census(31, edges31, 3, tracked=(14, 29, 30))
    four = canonical_colouring_census(31, edges31, 4, tracked=(14, 29, 30))
    require(three["leaves"] == 0, "D31 unexpectedly has a three-colouring")
    require(four["leaves"] == 1668352, "four-colouring census changed")
    require(four["patterns"] == {"000": 1668352}, "axis ports are not forced equal")

    edges61, second, bridge = build_spindle(edges31)
    require(len(edges61) == 197 and edge_digest(edges61) == SPINDLE_EDGE_SHA256,
            "D61 spindle changed")
    require(triangle_count(61, edges61) == 0, "D61 is not triangle-free")
    five_word, five_nodes = find_colouring(61, edges61, 5)
    require(five_word is not None, "D61 lacks a five-colouring")
    # In every four-colouring, each D31 copy equates its three ports.  The two
    # copies share port 31, so the endpoints of the added bridge must be equal.
    require(second[30] == 30 and bridge == (29, 60), "spindle interface changed")

    # Let f=x^3-2x^2+1 and g=x^3+x^2-2x-1.  The explicit identity below
    # proves gcd(f,g)=1 without a CAS or Euclidean-algorithm implementation.
    f = [1, 0, -2, 1]
    g = [-1, -2, 1, 1]
    bezout_f = [1, -3, -2]
    bezout_g = [0, -3, 2]
    bezout = poly_add(poly_multiply(bezout_f, f), poly_multiply(bezout_g, g))
    require(bezout == [1], "Bezout identity failed")
    require(poly_multiply([-1, 1], [-1, -1, 1]) == f, "factorization of f failed")
    # t_n=z^n+z^-n obeys t_(n+1)=x t_n-t_(n-1), x=z+z^-1.
    t0, t1 = [2], [0, 1]
    t2 = poly_add(poly_multiply([0, 1], t1), [-value for value in t0])
    t3 = poly_add(poly_multiply([0, 1], t2), [-value for value in t1])
    seventh_trace = poly_add(poly_add(poly_add(t3, t2), t1), [1])
    require(seventh_trace == g, "seventh-root trace polynomial derivation failed")
    geometric_equation = poly_add(poly_multiply([0, 0, 1], [2, -1]), [-1])
    require(geometric_equation == [-value for value in f], "geometric polynomial changed")

    output = {
        "verdict": "ACCEPT_EXACT_C7_EQUIVARIANT_GATE",
        "source_vertices": 31,
        "source_edges": len(edges31),
        "source_edge_sha256_one_based": edge_digest(edges31),
        "source_degree_histogram": degree_histogram,
        "source_triangles": triangle_count(31, edges31),
        "sigma_is_automorphism": True,
        "source_chromatic_number": 4,
        "canonical_three_colourings": three["leaves"],
        "three_colour_search_nodes": three["nodes"],
        "canonical_four_colourings": four["leaves"],
        "labelled_four_colourings": 24 * four["leaves"],
        "four_colour_search_nodes": four["nodes"],
        "four_colour_dead_ends": four["dead_ends"],
        "axis_roles_one_based": [15, 30, 31],
        "axis_patterns_in_all_canonical_four_colourings": four["patterns"],
        "obstruction_vertices": 15,
        "obstruction_edges": len(obstruction),
        "obstruction_edge_sha256_one_based": edge_digest(obstruction),
        "spindle_vertices": 61,
        "spindle_edges": len(edges61),
        "spindle_edge_sha256_one_based": edge_digest(edges61),
        "spindle_triangles": triangle_count(61, edges61),
        "spindle_chromatic_number": 5,
        "spindle_five_colour_search_nodes": five_nodes,
        "spindle_proper_five_word": five_word,
        "bezout_f_multiplier_ascending": bezout_f,
        "bezout_g_multiplier_ascending": bezout_g,
        "bezout_result": bezout,
        "seventh_trace_polynomial_ascending": g,
        "geometric_necessity_polynomial_ascending": f,
        "plane_realization_claim": False,
        "arbitrary_plane_map_exclusion": False,
        "record_improvement": False,
    }
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
