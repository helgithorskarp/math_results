#!/usr/bin/env python3
"""Independent exact checks for the iterated line-graph sphere review.

CPython 3.11+, standard library only.  This program imports no target code,
fixtures, or output.  Finite checks corroborate the proof; they do not prove
its universal homotopy assertions.
"""

import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def make_graph(n, edges):
    normalized = tuple(sorted(tuple(sorted(edge)) for edge in edges))
    require(len(set(normalized)) == len(normalized), "duplicate edge")
    require(all(len(edge) == 2 and 0 <= edge[0] < edge[1] < n
                for edge in normalized), "graph is not finite and simple")
    return n, normalized


def degrees(graph):
    n, edges = graph
    result = [0] * n
    for u, v in edges:
        result[u] += 1
        result[v] += 1
    return result


def connected(graph):
    n, edges = graph
    if n == 0:
        return False
    adjacency = [[] for _ in range(n)]
    for u, v in edges:
        adjacency[u].append(v)
        adjacency[v].append(u)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adjacency[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return len(seen) == n


def line_graph(graph):
    edges = graph[1]
    line_edges = []
    for i, j in combinations(range(len(edges)), 2):
        if set(edges[i]).intersection(edges[j]):
            line_edges.append((i, j))
    return make_graph(len(edges), line_edges)


def sphere_count(graph):
    return sum(comb(degree - 1, 3) for degree in degrees(graph)
               if degree >= 4)


def triangle_count(graph):
    n, edges = graph
    edge_set = set(edges)
    return sum(((a, b) in edge_set and (a, c) in edge_set
                and (b, c) in edge_set)
               for a, b, c in combinations(range(n), 3))


def line_clique_euler(graph):
    """Euler characteristic of Cl(L(graph)), from stars and triangles."""
    value = len(graph[1]) + triangle_count(graph)
    for degree in degrees(graph):
        for size in range(2, degree + 1):
            value += (-1) ** (size - 1) * comb(degree, size)
    return value


def maximal_cliques_of_line_graph(graph):
    """Bron--Kerbosch, used only to audit the star/triangle reduction."""
    edges = graph[1]
    order = len(edges)
    adjacency = [0] * order
    for i, j in combinations(range(order), 2):
        if set(edges[i]).intersection(edges[j]):
            adjacency[i] |= 1 << j
            adjacency[j] |= 1 << i
    answer = []

    def visit(chosen, candidates, excluded):
        if not candidates and not excluded:
            answer.append(chosen)
            return
        union = candidates | excluded
        if union:
            pivot_bit = union & -union
            pivot = pivot_bit.bit_length() - 1
            branch = candidates & ~adjacency[pivot]
        else:
            branch = candidates
        while branch:
            bit = branch & -branch
            branch ^= bit
            vertex = bit.bit_length() - 1
            visit(chosen | bit, candidates & adjacency[vertex],
                  excluded & adjacency[vertex])
            candidates ^= bit
            excluded |= bit

    visit(0, (1 << order) - 1, 0)
    return answer


def audit_clique_classification(graph):
    edges = graph[1]
    relevant = 0
    for mask in maximal_cliques_of_line_graph(graph):
        indices = [i for i in range(len(edges)) if mask & (1 << i)]
        if len(indices) < 3:
            continue
        relevant += 1
        common = set(edges[indices[0]])
        for index in indices[1:]:
            common.intersection_update(edges[index])
        if common:
            continue
        chosen = {edges[index] for index in indices}
        vertices = set().union(*(set(edge) for edge in chosen))
        require(len(indices) == 3 and len(vertices) == 3
                and chosen == {tuple(sorted(edge))
                               for edge in combinations(sorted(vertices), 2)},
                "pairwise-intersecting family is neither a star nor triangle")
    return relevant


def exceptional(graph):
    profile = sorted(degrees(graph))
    return max(profile, default=0) <= 2 or profile == [1, 1, 1, 3]


def degree_four_time(graph):
    require(not exceptional(graph), "hitting time requested for an exception")
    current = graph
    for step in range(4):
        if max(degrees(current), default=0) >= 4:
            return step
        current = line_graph(current)
    raise ValueError("degree four was not reached by the third line graph")


def adjacency_lists(graph):
    result = [[] for _ in range(graph[0])]
    for u, v in graph[1]:
        result[u].append(v)
        result[v].append(u)
    return result


def path_distance(graph, source, target):
    adjacency = adjacency_lists(graph)
    distance = {source: 0}
    stack = [source]
    for u in stack:
        if u == target:
            return distance[u]
        for v in adjacency[u]:
            if v not in distance:
                distance[v] = distance[u] + 1
                stack.append(v)
    raise ValueError("vertices lie in different components")


def is_late_family(graph):
    """Recognize the two tree families whose degree-four time is three."""
    n, edges = graph
    if not connected(graph) or len(edges) != n - 1:
        return False
    profile = degrees(graph)
    if max(profile, default=0) != 3:
        return False
    adjacency = adjacency_lists(graph)
    cubic = [v for v, degree in enumerate(profile) if degree == 3]
    if len(cubic) == 1:
        neighbor_degrees = sorted(profile[u] for u in adjacency[cubic[0]])
        return neighbor_degrees == [1, 1, 2]
    if len(cubic) == 2:
        local = all(sorted(profile[u] for u in adjacency[v]) == [1, 1, 2]
                    for v in cubic)
        return local and path_distance(graph, cubic[0], cubic[1]) >= 3
    return False


def remove_free_pair(faces, lower, upper):
    require(lower in faces and upper in faces, "collapse pair is absent")
    require(lower & upper == lower
            and upper.bit_count() == lower.bit_count() + 1,
            "collapse pair has wrong codimension")
    cofaces = {face for face in faces
               if face != lower and face & lower == lower}
    require(cofaces == {upper}, "lower face is not free")
    faces.remove(lower)
    faces.remove(upper)


def oriented_boundary(simplex):
    result = Counter()
    for index in range(len(simplex)):
        face = simplex[:index] + simplex[index + 1:]
        result[face] += (-1) ** index
    return Counter({face: coefficient for face, coefficient in result.items()
                    if coefficient})


def add_chain(target, coefficient, simplex):
    for face, value in oriented_boundary(simplex).items():
        target[face] += coefficient * value
        if target[face] == 0:
            del target[face]


def audit_star_template(degree):
    """Replay the universal local collapse and check cone disks over Z."""
    faces = set(range(1, 1 << degree))
    apex = degree - 1
    apex_bit = 1 << apex
    rest = range(degree - 1)
    pairs = 0
    for size in range(degree - 1, 2, -1):
        for subset in combinations(rest, size):
            lower = sum(1 << vertex for vertex in subset)
            remove_free_pair(faces, lower, lower | apex_bit)
            pairs += 1
    expected = {face for face in range(1, 1 << degree)
                if face.bit_count() <= 2
                or (face.bit_count() == 3 and face & apex_bit)}
    require(faces == expected, "star did not collapse to the stated cone")
    disks = 0
    for a, b, c in combinations(rest, 3):
        chain = Counter()
        add_chain(chain, 1, (b, c, apex))
        add_chain(chain, -1, (a, c, apex))
        add_chain(chain, 1, (a, b, apex))
        require(chain == oriented_boundary((a, b, c)),
                "integral cone disk has wrong oriented boundary")
        disks += 1
    require(disks == comb(max(degree - 1, 0), 3),
            "wrong number of omitted star triangles")
    return pairs, disks


def type_a(subdivisions):
    require(subdivisions >= 1, "type-A arm must be subdivided")
    edges = [(0, 1), (0, 2)]
    previous = 0
    for offset in range(subdivisions):
        vertex = 3 + offset
        edges.append((previous, vertex))
        previous = vertex
    edges.append((previous, 3 + subdivisions))
    return make_graph(4 + subdivisions, edges)


def double_star(middle_subdivisions):
    require(middle_subdivisions >= 0, "negative subdivision count")
    edges = [(0, 2), (0, 3), (1, 4), (1, 5)]
    previous = 0
    for offset in range(middle_subdivisions):
        vertex = 6 + offset
        edges.append((previous, vertex))
        previous = vertex
    edges.append((previous, 1))
    return make_graph(6 + middle_subdivisions, edges)


def enumerate_connected_graphs():
    counts = Counter()
    hitting = Counter()
    recurrence_checks = 0
    classified_cliques = 0
    late_checks = 0
    for n in range(1, 7):
        possible = list(combinations(range(n), 2))
        for bits in range(1 << len(possible)):
            graph = make_graph(n, [edge for index, edge in enumerate(possible)
                                   if bits & (1 << index)])
            if not connected(graph):
                continue
            counts[n] += 1
            classified_cliques += audit_clique_classification(graph)
            if not exceptional(graph):
                time = degree_four_time(graph)
                hitting[time] += 1
                require((time == 3) == is_late_family(graph),
                        "late-family classification failed")
                late_checks += 1
            if len(graph[1]) >= 2:
                difference = (line_clique_euler(line_graph(graph))
                              - line_clique_euler(graph))
                require(difference == sphere_count(graph),
                        "Euler characteristic recurrence failed")
                recurrence_checks += 1
    return counts, hitting, recurrence_checks, classified_cliques, late_checks


def run():
    (counts, hitting, recurrence_checks,
     classified_cliques, late_checks) = enumerate_connected_graphs()
    require(dict(counts) == {1: 1, 2: 1, 3: 4, 4: 38, 5: 728, 6: 26704},
            "connected labelled graph census is incomplete")

    template_pairs = template_disks = 0
    for degree in range(1, 11):
        pairs, disks = audit_star_template(degree)
        template_pairs += pairs
        template_disks += disks

    type_a_times = []
    for subdivisions in range(1, 9):
        graph = type_a(subdivisions)
        require(is_late_family(graph), "type-A fixture not recognized")
        type_a_times.append(degree_four_time(graph))

    double_times = []
    for subdivisions in range(9):
        graph = double_star(subdivisions)
        time = degree_four_time(graph)
        require(is_late_family(graph) == (subdivisions >= 2),
                "double-star boundary classification failed")
        double_times.append(time)

    claw = make_graph(4, [(0, 1), (0, 2), (0, 3)])
    four_star = make_graph(5, [(0, i) for i in range(1, 5)])
    triangle_leaf = make_graph(4, [(0, 1), (1, 2), (0, 2), (0, 3)])
    require(exceptional(claw), "claw boundary control failed")
    require(degree_four_time(four_star) == 0, "four-star control failed")
    require(degree_four_time(triangle_leaf) == 2,
            "triangle-with-leaf control failed")

    return {
        "status": "VERIFIED",
        "connected_labelled_graphs_by_order": dict(sorted(counts.items())),
        "euler_recurrences_checked": recurrence_checks,
        "maximal_star_or_triangle_cliques_checked": classified_cliques,
        "nonexceptional_graphs_classified": late_checks,
        "degree_four_hitting_time_histogram": dict(sorted(hitting.items())),
        "local_star_degrees_checked": [1, 10],
        "local_collapse_pairs_replayed": template_pairs,
        "integral_cone_disks_checked": template_disks,
        "adversarial_boundary_fixtures": {
            "claw": "exception",
            "four_leaf_star": 0,
            "triangle_with_leaf": 2,
            "type_A_subdivisions_1_to_8": type_a_times,
            "double_star_middle_subdivisions_0_to_8": double_times,
        },
        "trust_boundary": (
            "finite corroboration only; universal homotopy and extremal "
            "classification arguments are audited in REVIEW.md"
        ),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--emit", action="store_true",
                        help="emit result without checking expected.json")
    arguments = parser.parse_args()
    result = run()
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if not arguments.emit:
        expected = json.loads(Path(__file__).with_name("expected.json").read_text())
        require(json.loads(encoded) == expected, "expected result mismatch")
    print(encoded, end="")


if __name__ == "__main__":
    main()
