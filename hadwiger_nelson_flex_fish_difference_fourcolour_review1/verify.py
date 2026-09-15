#!/usr/bin/env python3
"""Independent exact review of the flexible-fish difference-body stop.

The target bounds squared distances by expanding around rational midpoints.
This checker instead builds an exact axis-aligned rational interval for every
coordinate, subtracts those intervals definitionally, and evaluates squared
distance intervals by endpoint arithmetic.  It does not import target code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_fish_flex_contact_source_loss"
TARGET = HERE.parent / "hadwiger_nelson_flex_fish_difference_fourcolour_stop"
GEOMETRY = SOURCE / "geometry_certificate.json"
CERTIFICATE = TARGET / "certificate.json"
EXPECTED = HERE / "EXPECTED.json"
GEOMETRY_SHA256 = "e079c2d86f0b3574e6e24d9fc18a9abc2d8b7d7fe111ba011d5978875d5fc732"
CERTIFICATE_SHA256 = "15c578fd0830897d39699972acf992648a18b6896957fd00490c3e9810e12ac1"

# Independently reconstructed in the accepted source review from the pinned
# Shibuya hodfish_vertices operation sequence.
FISH_EDGES = sorted([
    (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (1, 5),
    (4, 6), (3, 6), (6, 7), (5, 7), (2, 8), (6, 8),
    (0, 9), (7, 9), (8, 10), (1, 10), (9, 11), (3, 11),
    (4, 12), (10, 12), (2, 13), (6, 14), (13, 14),
    (13, 15), (6, 15), (1, 16), (15, 16), (16, 17), (14, 17),
    (5, 18), (18, 19), (6, 19), (6, 20), (18, 20),
    (20, 21), (0, 21), (19, 22), (21, 22),
    (2, 12), (5, 11), (2, 17), (5, 22),
])
CONTACT = (10, 21)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def iadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def isub(left, right):
    return left[0] - right[1], left[1] - right[0]


def isquare(interval):
    lo, hi = interval
    top = max(lo * lo, hi * hi)
    return (Q(0), top) if lo <= 0 <= hi else (min(lo * lo, hi * hi), top)


def overlaps(left, right):
    return not (left[1] < right[0] or right[1] < left[0])


def components(order, edges):
    parent = list(range(order))

    def find(vertex):
        while parent[vertex] != vertex:
            parent[vertex] = parent[parent[vertex]]
            vertex = parent[vertex]
        return vertex

    for left, right in edges:
        left, right = find(left), find(right)
        if left != right:
            parent[right] = left
    groups = {}
    for vertex in range(order):
        groups.setdefault(find(vertex), []).append(vertex)
    return sorted(groups.values(), key=lambda group: group[0])


def connected(order, edges):
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex] - seen:
            seen.add(neighbour)
            stack.append(neighbour)
    return len(seen) == order


def k_colourable(order, edges, colours):
    """Complete fixed-label search, independent of target SAT production."""
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    require(1 in adjacency[0], "normalizing edge absent")
    assignment = [-1] * order
    assignment[0], assignment[1] = 0, 1
    nodes = 0

    def visit(vertex):
        nonlocal nodes
        nodes += 1
        if vertex == order:
            return True
        forbidden = {assignment[n] for n in adjacency[vertex]
                     if assignment[n] >= 0}
        for colour in range(colours):
            if colour not in forbidden:
                assignment[vertex] = colour
                if visit(vertex + 1):
                    return True
        assignment[vertex] = -1
        return False

    return visit(2), nodes


def conservative_graph(geometry):
    h = geometry["midpoint_denominator"]
    radius = Q(1, geometry["radius_denominator"])
    require(type(h) is int and h > 0, "midpoint denominator")
    require(type(geometry["radius_denominator"]) is int
            and geometry["radius_denominator"] > 0, "radius denominator")
    midpoint_rows = geometry["midpoint_numerators"]
    require(len(midpoint_rows) == 23
            and all(len(row) == 2 for row in midpoint_rows), "midpoint shape")
    require(all(type(value) is int for row in midpoint_rows for value in row),
            "midpoint integrality")

    point_boxes = []
    for vertex, (x_num, y_num) in enumerate(midpoint_rows):
        x, y = Q(x_num, h), Q(y_num, h)
        error = Q(0) if vertex in (0, 1) else radius
        point_boxes.append(((x - error, x + error),
                            (y - error, y + error)))
    require(point_boxes[0] == ((Q(0), Q(0)), (Q(0), Q(0))),
            "first fixed anchor")
    require(point_boxes[1] == ((Q(1), Q(1)), (Q(0), Q(0))),
            "second fixed anchor")

    addresses = [(i, j) for i in range(23) for j in range(23)]
    boxes = [
        (isub(point_boxes[i][0], point_boxes[j][0]),
         isub(point_boxes[i][1], point_boxes[j][1]))
        for i, j in addresses
    ]
    possible_equal = []
    for left, right in combinations(range(len(addresses)), 2):
        if (overlaps(boxes[left][0], boxes[right][0])
                and overlaps(boxes[left][1], boxes[right][1])):
            possible_equal.append((left, right))
    clusters = components(len(addresses), possible_equal)
    cluster_of = {address: index for index, group in enumerate(clusters)
                  for address in group}

    possible_edges = set()
    within_upper = Q(0)
    separation_lower = None
    excluded_unit_gap = None
    pair_checks = 0
    for left, right in combinations(range(len(addresses)), 2):
        dx = isub(boxes[left][0], boxes[right][0])
        dy = isub(boxes[left][1], boxes[right][1])
        squared = iadd(isquare(dx), isquare(dy))
        pair_checks += 1
        if cluster_of[left] == cluster_of[right]:
            require(squared[1] < 1, "possible internal unit edge")
            within_upper = max(within_upper, squared[1])
            continue
        require(squared[0] > 0, "possible equality crosses clusters")
        separation_lower = (squared[0] if separation_lower is None else
                            min(separation_lower, squared[0]))
        if squared[0] <= 1 <= squared[1]:
            possible_edges.add(tuple(sorted(
                (cluster_of[left], cluster_of[right]))))
        else:
            gap = 1 - squared[1] if squared[1] < 1 else squared[0] - 1
            excluded_unit_gap = (gap if excluded_unit_gap is None else
                                 min(excluded_unit_gap, gap))
    return {
        "addresses": addresses,
        "clusters": clusters,
        "cluster_of": cluster_of,
        "edges": sorted(possible_edges),
        "possible_equal_pairs": len(possible_equal),
        "pair_checks": pair_checks,
        "within_upper": within_upper,
        "separation_lower": separation_lower,
        "excluded_unit_gap": excluded_unit_gap,
    }


def check_word(word, order, edges):
    require(type(word) is str and len(word) == order, "four-colour word length")
    require(set(word) <= set("0123"), "four-colour alphabet")
    require(all(word[left] != word[right] for left, right in edges),
            "improper four-colour word")


def verify(geometry_path=GEOMETRY, certificate_path=CERTIFICATE,
           check_hashes=True, check_expected=False):
    geometry_path, certificate_path = Path(geometry_path), Path(certificate_path)
    if check_hashes:
        require(digest(geometry_path) == GEOMETRY_SHA256,
                "reviewed source geometry hash")
        require(digest(certificate_path) == CERTIFICATE_SHA256,
                "reviewed target certificate hash")
    geometry = json.loads(geometry_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    require(geometry["schema"] == "fish-self-contact-root-v1", "source schema")
    require(certificate["schema"] ==
            "flex-fish-ordered-difference-fourcolour-stop-v1", "target schema")
    source_edges = sorted(map(tuple, geometry["source_edges"]))
    require(source_edges == FISH_EDGES, "source edge reconstruction")
    require(tuple(geometry["target_contact"]) == CONTACT, "source contact")
    complete_source_edges = sorted(source_edges + [CONTACT])
    require(connected(23, complete_source_edges), "source disconnected")
    require(all(connected(23, [edge for edge in complete_source_edges
                              if edge != omitted])
                for omitted in complete_source_edges), "source has a bridge")
    source_three_colourable, source_search_nodes = k_colourable(
        23, complete_source_edges, 3)
    require(not source_three_colourable, "source unexpectedly three-colourable")

    graph = conservative_graph(geometry)
    clusters, edges = graph["clusters"], graph["edges"]
    order = len(clusters)
    require(order == 433, "conservative cluster count")
    require(len(edges) == 1646, "conservative edge count")
    require(graph["within_upper"] < Q(1, 10**48), "internal margin")
    require(graph["separation_lower"] > Q(399, 10**6), "separation margin")
    require(graph["excluded_unit_gap"] > Q(17, 10**6), "unit-gap margin")

    stream = json.dumps({"clusters": clusters, "edges": edges},
                        separators=(",", ":")) + "\n"
    graph_hash = hashlib.sha256(stream.encode()).hexdigest()
    require(graph_hash == certificate["conservative_graph_sha256"],
            "conservative graph hash")
    word = certificate["four_colour_word"]
    check_word(word, order, edges)

    # Each fixed-j fibre is a translated copy of the exact source and is
    # injective.  Every fibre contains address (j,j), the common zero point.
    for j in range(23):
        fibre = [graph["cluster_of"][23 * i + j] for i in range(23)]
        require(len(set(fibre)) == 23, "collapsed translated source fibre")
        require(graph["cluster_of"][23 * j + j] in fibre,
                "zero absent from fibre")
        require(all(tuple(sorted((fibre[left], fibre[right]))) in set(edges)
                    for left, right in complete_source_edges),
                "translated source edge absent from supergraph")
    diagonal_clusters = {graph["cluster_of"][23 * i + i] for i in range(23)}
    require(len(diagonal_clusters) == 1, "diagonal addresses not grouped")

    cluster_sizes = Counter(map(len, clusters))
    colour_histogram = Counter(word)
    result = {
        "status": "ACCEPT_WITH_EXACT_SOURCE_AND_OPERATION_LIMITATION",
        "reviewed_source_geometry_sha256": digest(geometry_path),
        "reviewed_target_certificate_sha256": digest(certificate_path),
        "formal_addresses": 529,
        "formal_address_pair_checks": graph["pair_checks"],
        "possible_equality_pairs": graph["possible_equal_pairs"],
        "possible_equality_clusters": order,
        "cluster_size_histogram": {str(size): cluster_sizes[size]
                                    for size in sorted(cluster_sizes)},
        "possible_unit_cluster_edges": len(edges),
        "conservative_graph_sha256": graph_hash,
        "colour_histogram": {colour: colour_histogram[colour]
                              for colour in sorted(colour_histogram)},
        "proper_four_colouring": True,
        "translated_source_fibres": 23,
        "source_static_three_colour_nodes": source_search_nodes,
        "source_chromatic_lower_bound": 4,
        "actual_chromatic_number": 4,
        "actual_support_order_interval": [433, 507],
        "actual_unit_graph_connected": True,
        "actual_unit_graph_bridgeless": True,
        "within_cluster_squared_distance_upper_lt": "1/10^48",
        "different_cluster_squared_separation_gt": "399/1000000",
        "excluded_squared_unit_gap_gt": "17/1000000",
        "record_candidate": False,
    }
    if check_expected:
        require(json.loads(EXPECTED.read_text()) == result, "EXPECTED mismatch")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", type=Path, default=GEOMETRY)
    parser.add_argument("--certificate", type=Path, default=CERTIFICATE)
    parser.add_argument("--no-hashes", action="store_true")
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    print(json.dumps(verify(arguments.geometry, arguments.certificate,
                            not arguments.no_hashes, arguments.check_expected),
                     indent=2, sort_keys=True))
