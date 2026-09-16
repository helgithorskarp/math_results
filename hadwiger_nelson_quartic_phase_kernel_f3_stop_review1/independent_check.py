#!/usr/bin/env python3
"""Independent Cartesian/modular review of the quartic F3 completion."""

import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path


HERE = Path(__file__).resolve().parent
DENOMINATOR = 8
SIEVES = ((157, 12), (193, 75))


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


def add(left, right):
    return tuple(x + y for x, y in zip(left, right))


def neg(value):
    return tuple(-x for x in value)


def sub(left, right):
    return add(left, neg(right))


def polynomial_multiply(left, right):
    """Multiply integer coefficient rows modulo T^4-12."""
    unreduced = [0] * 7
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            unreduced[i + j] += x * y
    for exponent in range(6, 3, -1):
        unreduced[exponent - 4] += 12 * unreduced[exponent]
    return tuple(unreduced[:4])


def squared_distance_polynomial(left, right):
    delta = sub(left, right)
    x, y = delta[:4], delta[4:]
    result = add(polynomial_multiply(x, x), polynomial_multiply(y, y))
    return (result[0] - DENOMINATOR * DENOMINATOR,) + result[1:]


def validate_sieve(prime, root):
    is_prime = prime >= 2 and all(prime % divisor for divisor in range(2, int(prime ** 0.5) + 1))
    need(is_prime and prime > DENOMINATOR and pow(root, 4, prime) == 12 % prime,
         "invalid finite-field specialization")


def modular_unit_test(left, right, prime, root):
    delta = sub(left, right)

    def evaluate(coefficients):
        result = 0
        for coefficient in reversed(coefficients):
            result = (result * root + coefficient) % prime
        return result

    x = evaluate(delta[:4])
    y = evaluate(delta[4:])
    return (x * x + y * y - DENOMINATOR * DENOMINATOR) % prime == 0


def exact_unit_test(left, right):
    return squared_distance_polynomial(left, right) == (0, 0, 0, 0)


def complete_edges(points):
    for sieve in SIEVES:
        validate_sieve(*sieve)
    candidate_counts = [0, 0]
    joint_candidates = []
    for left, right in itertools.combinations(range(len(points)), 2):
        passed = [modular_unit_test(points[left], points[right], *sieve) for sieve in SIEVES]
        for index, value in enumerate(passed):
            candidate_counts[index] += value
        if all(passed):
            joint_candidates.append((left, right))
    edges = [edge for edge in joint_candidates if exact_unit_test(points[edge[0]], points[edge[1]])]
    return edges, candidate_counts, len(joint_candidates)


def square_root_three_times(coefficients):
    # sqrt(3)=T^2/2 and T^4=12.
    a, b, c, d = coefficients
    return (Fraction(6 * c), Fraction(6 * d), Fraction(a, 2), Fraction(b, 2))


def rotate_sixty(point):
    x = tuple(map(Fraction, point[:4]))
    y = tuple(map(Fraction, point[4:]))
    sy = square_root_three_times(y)
    sx = square_root_three_times(x)
    new_x = tuple((a - b) / 2 for a, b in zip(x, sy))
    new_y = tuple((a + b) / 2 for a, b in zip(sx, y))
    need(all(value.denominator == 1 for value in new_x + new_y),
         "rotation escaped the scaled lattice")
    return tuple(int(value) for value in new_x + new_y)


def rotations(point):
    result = []
    current = point
    for _ in range(6):
        result.append(current)
        current = rotate_sixty(current)
    need(current == point and len(set(result)) == 6, "sixfold rotation orbit")
    return result


def source_points():
    zero = (0,) * 8
    one = (8, 0, 0, 0, 0, 0, 0, 0)
    zeta = (-4, 0, 0, 0, 0, 0, 2, 0)
    a1 = (-4, 0, 0, 0, 0, 0, -2, 0)
    # These are the Cartesian expansions displayed in the parent proof.
    y = (-6, 2, 1, 0, -2, 0, 1, 1)
    z = (-6, -2, 1, 0, -2, 0, 1, -1)
    centres = [zero, a1, sub(neg(one), y), add(neg(zeta), z)]
    tips = [neg(one), neg(zeta)]
    cross_pairs = ((0, 2), (0, 3), (1, 2), (1, 3))
    roots = []
    for left, right in cross_pairs:
        tip = tips[right - 2]
        roots.append(sorted((tip, sub(add(centres[left], centres[right]), tip))))
    direction_sets = [set(), set()]
    for group in range(2):
        seeds = [sub(centres[2 * group + 1], centres[2 * group])]
        for (left, right), root_pair in zip(cross_pairs, roots):
            owner = centres[left if group == 0 else right]
            seeds.extend(sub(root, owner) for root in root_pair)
        for seed in seeds:
            direction_sets[group].update(rotations(seed))
    need(list(map(len, direction_sets)) == [18, 24], "source direction census")
    points = sorted({
        add(centre, direction)
        for index, centre in enumerate(centres)
        for direction in direction_sets[index // 2]
    })
    need(len(points) == 74, "source point census")
    return points


def encoded_axis(axis):
    return [[Fraction(value, DENOMINATOR).numerator,
             Fraction(value, DENOMINATOR).denominator] for value in axis]


def encode_point(point):
    return [encoded_axis(point[:4]), encoded_axis(point[4:])]


def digest(value):
    blob = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
    return hashlib.sha256(blob).hexdigest()


def construct():
    source = source_points()
    source_edges, source_sieve_counts, source_joint = complete_edges(source)
    need(len(source_edges) == 198, "source edge census")
    source_adjacency = [set() for _ in source]
    for left, right in source_edges:
        source_adjacency[left].add(right)
        source_adjacency[right].add(left)
    candidates = set()
    routes = 0
    for middle in range(len(source)):
        for left, right in itertools.combinations(sorted(source_adjacency[middle]), 2):
            candidate = sub(add(source[left], source[right]), source[middle])
            need(exact_unit_test(candidate, source[left]) and exact_unit_test(candidate, source[right]),
                 "opposite rhombus corner")
            routes += 1
            if candidate not in set(source):
                candidates.add(candidate)
    need(routes == 1442, "unit two-path census")
    histogram = {}
    contacts = {}
    for candidate in sorted(candidates):
        count = sum(exact_unit_test(candidate, old) for old in source)
        histogram[count] = histogram.get(count, 0) + 1
        contacts[candidate] = count
    selected = [candidate for candidate in sorted(candidates) if contacts[candidate] >= 3]
    points = sorted(source + selected)
    source_set = set(source)
    source_indices = [index for index, point in enumerate(points) if point in source_set]
    edges, final_sieve_counts, final_joint = complete_edges(points)
    selected_indices = set(range(len(points))) - set(source_indices)
    old_new = sum((left in selected_indices) != (right in selected_indices) for left, right in edges)
    new_new = sum(left in selected_indices and right in selected_indices for left, right in edges)
    return {
        "source": source,
        "source_edges": source_edges,
        "source_sieve_counts": source_sieve_counts,
        "source_joint": source_joint,
        "routes": routes,
        "candidates": candidates,
        "histogram": histogram,
        "contacts": contacts,
        "selected": selected,
        "points": points,
        "source_indices": source_indices,
        "edges": edges,
        "final_sieve_counts": final_sieve_counts,
        "final_joint": final_joint,
        "old_new_edges": old_new,
        "new_new_edges": new_new,
    }


def adjacency(order, edges):
    result = [set() for _ in range(order)]
    for left, right in edges:
        result[left].add(right)
        result[right].add(left)
    return result


def fresh_three_colouring(order, edges):
    graph = adjacency(order, edges)
    colours = [-1] * order
    masks = [0] * order
    degrees = list(map(len, graph))
    start = max(range(order), key=lambda vertex: (degrees[vertex], vertex))
    colours[start] = 0
    for other in graph[start]:
        masks[other] |= 1
    nodes = 0
    backtracks = 0

    def search(done, maximum):
        nonlocal nodes, backtracks
        nodes += 1
        if done == order:
            return True
        vertex = max(
            (item for item in range(order) if colours[item] < 0),
            key=lambda item: (masks[item].bit_count(), degrees[item], item),
        )
        available = [colour for colour in range(min(2, maximum + 1) + 1)
                     if not masks[vertex] & (1 << colour)]
        for colour in reversed(available):
            bit = 1 << colour
            colours[vertex] = colour
            changed = []
            conflict = False
            for other in graph[vertex]:
                if colours[other] < 0 and not masks[other] & bit:
                    masks[other] |= bit
                    changed.append(other)
                    if masks[other] == 0b111:
                        conflict = True
            if not conflict and search(done + 1, max(maximum, colour)):
                return True
            for other in changed:
                masks[other] ^= bit
            colours[vertex] = -1
            backtracks += 1
        return False

    need(search(1, 0), "fresh three-colour search failed")
    need(max(colours) == 2, "fresh word does not use three colours")
    word = "".join(map(str, colours))
    validate_word(word, order, edges)
    return word, nodes, backtracks


def validate_word(word, order, edges):
    need(isinstance(word, str) and len(word) == order, "colour word length")
    need(set(word) <= set("012"), "colour word alphabet")
    need(all(word[left] != word[right] for left, right in edges), "monochromatic edge")


def graph_structure(order, edges):
    graph = adjacency(order, edges)
    discovery = [-1] * order
    low = [0] * order
    parent = [-1] * order
    articulations = set()
    bridges = set()
    clock = 0

    def visit(vertex):
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for other in graph[vertex]:
            if discovery[other] < 0:
                parent[other] = vertex
                children += 1
                visit(other)
                low[vertex] = min(low[vertex], low[other])
                if parent[vertex] < 0 and children > 1:
                    articulations.add(vertex)
                if parent[vertex] >= 0 and low[other] >= discovery[vertex]:
                    articulations.add(vertex)
                if low[other] > discovery[vertex]:
                    bridges.add(tuple(sorted((vertex, other))))
            elif other != parent[vertex]:
                low[vertex] = min(low[vertex], discovery[other])

    visit(0)
    need(all(value >= 0 for value in discovery), "graph disconnected")
    degrees = [len(row) for row in graph]
    return sorted(articulations), sorted(bridges), degrees


def connectivity_audit(order, edges):
    """Determine vertex/edge connectivity through three, with witnesses."""
    base_graph = adjacency(order, edges)
    degrees = list(map(len, base_graph))
    need(min(degrees) == 3, "connectivity audit expects minimum degree three")

    def reduced_structure(deleted_vertex=None, deleted_edge=None):
        graph = [[] for _ in range(order)]
        for edge_index, (left, right) in enumerate(edges):
            if edge_index == deleted_edge or left == deleted_vertex or right == deleted_vertex:
                continue
            graph[left].append((right, edge_index))
            graph[right].append((left, edge_index))
        discovery = [-1] * order
        low = [0] * order
        parent = [-1] * order
        articulations = set()
        bridges = set()
        clock = 0

        def visit(vertex):
            nonlocal clock
            discovery[vertex] = low[vertex] = clock
            clock += 1
            children = 0
            for other, edge_index in graph[vertex]:
                if discovery[other] < 0:
                    parent[other] = vertex
                    children += 1
                    visit(other)
                    low[vertex] = min(low[vertex], low[other])
                    if parent[vertex] < 0 and children > 1:
                        articulations.add(vertex)
                    if parent[vertex] >= 0 and low[other] >= discovery[vertex]:
                        articulations.add(vertex)
                    if low[other] > discovery[vertex]:
                        bridges.add(edge_index)
                elif other != parent[vertex]:
                    low[vertex] = min(low[vertex], discovery[other])

        start = next(vertex for vertex in range(order) if vertex != deleted_vertex)
        visit(start)
        connected = sum(value >= 0 for value in discovery) == order - (deleted_vertex is not None)
        return connected, articulations, bridges

    vertex_cut = None
    for deleted in range(order):
        connected, articulations, _ = reduced_structure(deleted_vertex=deleted)
        need(connected, "base graph had an articulation")
        if articulations:
            vertex_cut = [deleted, min(articulations)]
            break
    if vertex_cut is None:
        vertex_connectivity = 3
        witness_vertex = next(vertex for vertex, degree in enumerate(degrees) if degree == 3)
        vertex_cut = sorted(base_graph[witness_vertex])
    else:
        vertex_connectivity = 2

    edge_cut = None
    for deleted, first_edge in enumerate(edges):
        connected, _, bridges = reduced_structure(deleted_edge=deleted)
        need(connected, "base graph had a bridge")
        if bridges:
            edge_cut = [list(first_edge), list(edges[min(bridges)])]
            break
    if edge_cut is None:
        edge_connectivity = 3
        witness_vertex = next(vertex for vertex, degree in enumerate(degrees) if degree == 3)
        edge_cut = [list(sorted((witness_vertex, other))) for other in sorted(base_graph[witness_vertex])]
    else:
        edge_connectivity = 2
    return vertex_connectivity, vertex_cut, edge_connectivity, edge_cut


def review_result():
    built = construct()
    points = built["points"]
    edges = built["edges"]
    order = len(points)
    word, nodes, backtracks = fresh_three_colouring(order, edges)
    certificate = json.loads((HERE / "certificate.json").read_text())
    need(set(certificate) == {"label_order", "three_word"}, "certificate keys")
    need(certificate["label_order"] == "lexicographic scaled Cartesian coefficient rows",
         "certificate label order")
    validate_word(certificate["three_word"], order, edges)
    need(certificate["three_word"] == word, "stored and freshly found words differ")
    edge_set = set(edges)
    source_index_set = set(built["source_indices"])
    triangle = next(
        triple for triple in itertools.combinations(built["source_indices"], 3)
        if all(tuple(sorted(pair)) in edge_set for pair in itertools.combinations(triple, 2))
    )
    source_word = "".join(word[index] for index in built["source_indices"])
    source_edges_in_final_order = [
        (built["source_indices"][left], built["source_indices"][right])
        for left, right in built["source_edges"]
    ]
    validate_word(source_word, 74, built["source_edges"])
    final_articulations, final_bridges, final_degrees = graph_structure(order, edges)
    source_articulations, source_bridges, source_degrees = graph_structure(74, built["source_edges"])
    source_vertex_connectivity, source_vertex_cut, source_edge_connectivity, source_edge_cut = connectivity_audit(74, built["source_edges"])
    completion_vertex_connectivity, completion_vertex_cut, completion_edge_connectivity, completion_edge_cut = connectivity_audit(order, edges)
    need(all(index in source_index_set for index in triangle), "triangle outside source")
    need(len(source_edges_in_final_order) == 198, "source embedding")
    point_hash = digest([encode_point(point) for point in points])
    edge_hash = digest(edges)
    source_hash = digest([encode_point(point) for point in built["source"]])
    source_edge_hash = digest(built["source_edges"])
    return {
        "status": "ACCEPT_AND_STRENGTHEN_EXACT_THREE",
        "source_vertices": 74,
        "source_edges": len(built["source_edges"]),
        "source_point_sha256": source_hash,
        "source_edge_sha256": source_edge_hash,
        "source_sieve_candidate_counts": built["source_sieve_counts"],
        "source_joint_sieve_candidates": built["source_joint"],
        "unit_two_paths": built["routes"],
        "all_new_candidates": len(built["candidates"]),
        "candidate_contact_histogram": [[key, built["histogram"][key]] for key in sorted(built["histogram"])],
        "selected_new_points": len(built["selected"]),
        "vertices": order,
        "edges": len(edges),
        "source_source_edges": len(built["source_edges"]),
        "source_new_edges": built["old_new_edges"],
        "new_new_edges": built["new_new_edges"],
        "all_final_pairs_checked": order * (order - 1) // 2,
        "final_sieve_candidate_counts": built["final_sieve_counts"],
        "final_joint_sieve_candidates": built["final_joint"],
        "point_sha256": point_hash,
        "edge_sha256": edge_hash,
        "source_triangle": list(triangle),
        "source_three_word_sha256": hashlib.sha256(source_word.encode()).hexdigest(),
        "fresh_three_word_sha256": hashlib.sha256(word.encode()).hexdigest(),
        "fresh_three_search_nodes": nodes,
        "fresh_three_search_backtracks": backtracks,
        "source_chromatic_number": 3,
        "completion_chromatic_number": 3,
        "source_connected": True,
        "source_articulation_vertices": source_articulations,
        "source_bridges": [list(edge) for edge in source_bridges],
        "source_minimum_degree": min(source_degrees),
        "source_vertex_connectivity": source_vertex_connectivity,
        "source_vertex_cut_witness": source_vertex_cut,
        "source_edge_connectivity": source_edge_connectivity,
        "source_edge_cut_witness": source_edge_cut,
        "completion_connected": True,
        "completion_articulation_vertices": final_articulations,
        "completion_bridges": [list(edge) for edge in final_bridges],
        "completion_minimum_degree": min(final_degrees),
        "completion_maximum_degree": max(final_degrees),
        "completion_vertex_connectivity": completion_vertex_connectivity,
        "completion_vertex_cut_witness": completion_vertex_cut,
        "completion_edge_connectivity": completion_edge_connectivity,
        "completion_edge_cut_witness": completion_edge_cut,
        "record_candidate": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = review_result()
    if arguments.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
