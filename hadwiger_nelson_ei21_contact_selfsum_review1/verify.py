#!/usr/bin/env python3
"""Independent exact review of the EI21 contact and commutative self-sum.

The target uses aggregate midpoint error formulas.  This checker propagates
axis-aligned rational intervals through the full Jacobian and evaluates every
source and self-sum distance by interval endpoint arithmetic.  It imports no
target code and uses no external solver.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_ei21_contact_selfsum_fourcolour_stop"
GEOMETRY = TARGET / "geometry_certificate.json"
SELFSUM = TARGET / "selfsum_certificate.json"
EXPECTED = HERE / "EXPECTED.json"
GEOMETRY_SHA256 = "4e94704ca1f96743f1bb950393ff4fadd6377d8a33697f0debb484722d8cd162"
SELFSUM_SHA256 = "983e7f2da0ef236d2c9fd2e26cda93649c8873c04940183877e62cbded0e88a8"
FIXED = {0: (Q(0), Q(0)), 1: (Q(0), Q(-1))}

# Reconstructed from the operation sequence of ei21_vertices at pinned
# Shibuya commit 218097c9971db2b60ab94a0b8dae20d76741cc43.  Each cu call
# contributes its two parent edges; the fixed A--B edge and the three closure
# conditions contribute the remaining four edges.
SHIBUYA_SOURCE_EDGES = sorted([
    (0, 1),
    (0, 3), (2, 3), (0, 4), (2, 4),
    (1, 5), (2, 5), (1, 6), (2, 6),
    (6, 7), (3, 7), (4, 8), (5, 8), (7, 8),
    (1, 9), (7, 9), (6, 10),
    (9, 11), (10, 11), (10, 12), (9, 12),
    (6, 13), (11, 13), (12, 14), (13, 14), (4, 14),
    (8, 15), (1, 15), (5, 16),
    (16, 17), (15, 17), (15, 18), (16, 18),
    (17, 19), (5, 19), (19, 20), (18, 20), (3, 20),
])
CONTACT = (0, 14)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def iadd(left, right):
    return left[0] + right[0], left[1] + right[1]


def ineg(interval):
    return -interval[1], -interval[0]


def isub(left, right):
    return left[0] - right[1], left[1] - right[0]


def iscale(coefficient, interval):
    values = coefficient * interval[0], coefficient * interval[1]
    return min(values), max(values)


def isquare(interval):
    lo, hi = interval
    top = max(lo * lo, hi * hi)
    return (Q(0), top) if lo <= 0 <= hi else (min(lo * lo, hi * hi), top)


def imaxabs(interval):
    return max(abs(interval[0]), abs(interval[1]))


def overlaps(left, right):
    return not (left[1] < right[0] or right[1] < left[0])


def proper(word, order, edges, colours=4):
    return (len(word) == order
            and set(word) <= set(map(str, range(colours)))
            and all(word[left] != word[right] for left, right in edges))


def static_colour(order, edges, colours, values=None):
    """Complete fixed-label search, independent of the target's DSATUR."""
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    require(1 in adjacency[0], "normalizing edge absent")
    assignment = [-1] * order
    assignment[0], assignment[1] = 0, 1
    palette = tuple(range(colours)) if values is None else tuple(values)
    nodes = 0

    def visit(vertex):
        nonlocal nodes
        nodes += 1
        if vertex == order:
            return True
        forbidden = {assignment[n] for n in adjacency[vertex]
                     if assignment[n] >= 0}
        for colour in palette:
            if colour not in forbidden:
                assignment[vertex] = colour
                if visit(vertex + 1):
                    return True
        assignment[vertex] = -1
        return False

    found = visit(2)
    word = "".join(map(str, assignment)) if found else None
    return found, nodes, word


def component_count(order, edges, omitted=frozenset()):
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        if left not in omitted and right not in omitted:
            adjacency[left].add(right)
            adjacency[right].add(left)
    seen = set()
    answer = 0
    for start in range(order):
        if start in omitted or start in seen:
            continue
        answer += 1
        seen.add(start)
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex] - seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return answer


def vertex_connectivity(order, edges):
    require(component_count(order, edges) == 1, "disconnected graph")
    for size in range(1, order):
        cuts = [cut for cut in combinations(range(order), size)
                if component_count(order, edges, frozenset(cut)) > 1]
        if cuts:
            return size, cuts
    return order - 1, []


def girth(order, edges):
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        adjacency[left].add(right)
        adjacency[right].add(left)
    answer = order + 1
    for start in range(order):
        distance = {start: 0}
        parent = {start: -1}
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbour in adjacency[vertex]:
                if neighbour not in distance:
                    distance[neighbour] = distance[vertex] + 1
                    parent[neighbour] = vertex
                    queue.append(neighbour)
                elif parent[vertex] != neighbour:
                    answer = min(answer, distance[vertex]
                                 + distance[neighbour] + 1)
    return answer


def union_components(order, edges):
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


def source_review(geometry):
    require(geometry["schema"] == "ei21-contact-root-v1", "geometry schema")
    source_edges = sorted(map(tuple, geometry["source_edges"]))
    require(source_edges == SHIBUYA_SOURCE_EDGES, "source reconstruction")
    require(tuple(geometry["target_contact"]) == CONTACT, "target contact")
    complete_edges = sorted(source_edges + [CONTACT])
    equations = [edge for edge in complete_edges if edge != (0, 1)]
    free = list(range(2, 21))
    position = {vertex: index for index, vertex in enumerate(free)}
    require(len(equations) == 38 == 2 * len(free), "square system")

    h = geometry["midpoint_denominator"]
    d = geometry["inverse_denominator"]
    rd = geometry["radius_denominator"]
    require(all(type(value) is int and value > 0 for value in (h, d, rd)),
            "positive denominators")
    midpoint_rows = geometry["midpoint_numerators"]
    inverse_rows = geometry["inverse_numerators"]
    require(len(midpoint_rows) == 21
            and all(len(row) == 2 for row in midpoint_rows), "midpoint shape")
    require(len(inverse_rows) == 38
            and all(len(row) == 38 for row in inverse_rows), "inverse shape")
    require(all(type(value) is int for row in midpoint_rows for value in row),
            "midpoint integrality")
    require(all(type(value) is int for row in inverse_rows for value in row),
            "inverse integrality")
    midpoint = [tuple(Q(value, h) for value in row) for row in midpoint_rows]
    inverse = [[Q(value, d) for value in row] for row in inverse_rows]
    require(midpoint[0] == FIXED[0] and midpoint[1] == FIXED[1],
            "fixed anchors")
    radius = Q(1, rd)
    point_boxes = [
        ((x, x), (y, y)) if vertex in FIXED else
        ((x - radius, x + radius), (y - radius, y + radius))
        for vertex, (x, y) in enumerate(midpoint)
    ]

    residual = []
    jacobian_rows = []
    for left, right in equations:
        dx = midpoint[left][0] - midpoint[right][0]
        dy = midpoint[left][1] - midpoint[right][1]
        residual.append(dx * dx + dy * dy - 1)
        entries = {}
        for coordinate in (0, 1):
            difference = isub(point_boxes[left][coordinate],
                               point_boxes[right][coordinate])
            if left in position:
                entries[2 * position[left] + coordinate] = iscale(Q(2), difference)
            if right in position:
                entries[2 * position[right] + coordinate] = iscale(Q(-2), difference)
        jacobian_rows.append(entries)
    image = [sum(inverse[row][k] * residual[k] for k in range(38))
             for row in range(38)]
    centre_displacement = max(map(abs, image))

    contraction = Q(0)
    for row_index in range(38):
        row = [(Q(int(row_index == column)), Q(int(row_index == column)))
               for column in range(38)]
        for equation, entries in enumerate(jacobian_rows):
            coefficient = inverse[row_index][equation]
            if coefficient:
                for column, interval in entries.items():
                    row[column] = iadd(row[column],
                                       ineg(iscale(coefficient, interval)))
        contraction = max(contraction, sum(map(imaxabs, row)))
    self_map_bound = centre_displacement + contraction * radius
    require(contraction < Q(1, 10**22), "interval contraction")
    require(self_map_bound < Q(1, 10**47), "interval self-map")

    separation_lower = None
    nonedge_gap_lower = None
    edge_set = set(complete_edges)
    for left, right in combinations(range(21), 2):
        dx = isub(point_boxes[left][0], point_boxes[right][0])
        dy = isub(point_boxes[left][1], point_boxes[right][1])
        distance = iadd(isquare(dx), isquare(dy))
        require(distance[0] > 0, f"source collision unresolved: {(left, right)}")
        separation_lower = (distance[0] if separation_lower is None else
                            min(separation_lower, distance[0]))
        if (left, right) not in edge_set:
            if distance[1] < 1:
                gap = 1 - distance[1]
            elif distance[0] > 1:
                gap = distance[0] - 1
            else:
                raise ValueError(f"source nonedge unresolved: {(left, right)}")
            nonedge_gap_lower = (gap if nonedge_gap_lower is None else
                                 min(nonedge_gap_lower, gap))
    require(separation_lower > Q(38, 1000), "source separation margin")
    require(nonedge_gap_lower > Q(9, 1000), "source unit-gap margin")

    source_three, source_nodes, _ = static_colour(21, source_edges, 3)
    complete_three, complete_nodes, _ = static_colour(21, complete_edges, 3)
    require(not source_three and not complete_three, "three-colouring found")
    fresh_four, fresh_nodes, fresh_word = static_colour(
        21, complete_edges, 4, values=(3, 2, 1, 0))
    require(fresh_four and proper(fresh_word, 21, complete_edges),
            "fresh four-colouring absent")
    blocked = geometry["source_blocked_word"]
    surviving = geometry["surviving_complete_word"]
    require(proper(blocked, 21, source_edges), "blocked source word")
    require(blocked[0] == blocked[14]
            and not proper(blocked, 21, complete_edges), "source-loss witness")
    require(proper(surviving, 21, complete_edges), "surviving word")
    require(fresh_word not in (blocked, surviving), "fresh word duplicated")

    connectivity, cuts = vertex_connectivity(21, complete_edges)
    require(connectivity == 3 and len(cuts) == 12, "vertex connectivity")
    require(all(component_count(21, [edge for edge in complete_edges
                                     if edge != omitted]) == 1
                for omitted in complete_edges), "source bridge")
    degree_histogram = Counter()
    for vertex in range(21):
        degree_histogram[sum(vertex in edge for edge in complete_edges)] += 1
    edge_stream = "".join(f"{left} {right}\n" for left, right in complete_edges)
    return point_boxes, complete_edges, {
        "vertices": 21,
        "source_edges": 38,
        "complete_unit_edges": 39,
        "new_contact": [0, 14],
        "source_chromatic_number": 4,
        "contact_chromatic_number": 4,
        "source_static_three_colour_nodes": source_nodes,
        "complete_static_three_colour_nodes": complete_nodes,
        "fresh_four_colour_nodes": fresh_nodes,
        "fresh_four_colour_word": fresh_word,
        "vertex_connectivity": connectivity,
        "minimum_vertex_cuts": len(cuts),
        "first_minimum_cut": list(cuts[0]),
        "degree_histogram": {str(degree): degree_histogram[degree]
                             for degree in sorted(degree_histogram)},
        "girth": girth(21, complete_edges),
        "interval_contraction_bound_lt": "1/10^22",
        "interval_self_map_bound_lt": "1/10^47",
        "squared_separation_gt": "38/1000",
        "nonedge_squared_unit_gap_gt": "9/1000",
        "edge_stream_sha256": hashlib.sha256(edge_stream.encode()).hexdigest(),
    }


def selfsum_review(point_boxes, source_edges, certificate):
    require(certificate["schema"] ==
            "ei21-contact-commutative-selfsum-fourcolour-stop-v1",
            "self-sum schema")
    addresses = list(combinations_with_replacement(range(21), 2))
    address_index = {address: index for index, address in enumerate(addresses)}
    boxes = [
        (iadd(point_boxes[left][0], point_boxes[right][0]),
         iadd(point_boxes[left][1], point_boxes[right][1]))
        for left, right in addresses
    ]
    possible_equal = []
    for left, right in combinations(range(len(addresses)), 2):
        if (overlaps(boxes[left][0], boxes[right][0])
                and overlaps(boxes[left][1], boxes[right][1])):
            possible_equal.append((left, right))
    clusters = union_components(len(addresses), possible_equal)
    cluster_of = {address: cluster for cluster, members in enumerate(clusters)
                  for address in members}

    possible_edges = set()
    within_upper = Q(0)
    separation_lower = None
    excluded_gap = None
    pair_checks = 0
    for left, right in combinations(range(len(addresses)), 2):
        dx = isub(boxes[left][0], boxes[right][0])
        dy = isub(boxes[left][1], boxes[right][1])
        distance = iadd(isquare(dx), isquare(dy))
        pair_checks += 1
        if cluster_of[left] == cluster_of[right]:
            require(distance[1] < 1, "possible internal self-sum unit edge")
            within_upper = max(within_upper, distance[1])
            continue
        require(distance[0] > 0, "possible collision crosses clusters")
        separation_lower = (distance[0] if separation_lower is None else
                            min(separation_lower, distance[0]))
        if distance[0] <= 1 <= distance[1]:
            possible_edges.add(tuple(sorted((cluster_of[left], cluster_of[right]))))
        else:
            gap = 1 - distance[1] if distance[1] < 1 else distance[0] - 1
            excluded_gap = gap if excluded_gap is None else min(excluded_gap, gap)
    edges = sorted(possible_edges)
    require(len(clusters) == 210 and len(edges) == 731, "self-sum census")
    require(within_upper < Q(1, 10**48), "self-sum internal margin")
    require(separation_lower > Q(36, 10**6), "self-sum separation margin")
    require(excluded_gap > Q(167, 10**6), "self-sum unit-gap margin")

    stream = json.dumps({"clusters": clusters, "edges": edges},
                        separators=(",", ":")) + "\n"
    graph_hash = hashlib.sha256(stream.encode()).hexdigest()
    require(graph_hash == certificate["conservative_graph_sha256"],
            "self-sum graph hash")
    word = certificate["four_colour_word"]
    require(proper(word, len(clusters), edges), "self-sum four-colour word")

    edge_set = set(edges)
    fibre_clusters = []
    for fixed in range(21):
        formal = [address_index[tuple(sorted((moving, fixed)))]
                  for moving in range(21)]
        fibre = [cluster_of[address] for address in formal]
        require(len(set(fibre)) == 21, "collapsed translated source fibre")
        require(all(tuple(sorted((fibre[left], fibre[right]))) in edge_set
                    for left, right in source_edges),
                "translated source edge missing")
        fibre_clusters.append(set(fibre))
    require(all(fibre_clusters[left] & fibre_clusters[right]
                for left, right in combinations(range(21), 2)),
            "translated source fibres fail to intersect")

    cluster_sizes = Counter(map(len, clusters))
    colour_histogram = Counter(word)
    return {
        "formal_addresses": 231,
        "formal_address_pair_checks": pair_checks,
        "possible_equality_pairs": len(possible_equal),
        "possible_equality_clusters": len(clusters),
        "cluster_size_histogram": {str(size): cluster_sizes[size]
                                   for size in sorted(cluster_sizes)},
        "possible_unit_cluster_edges": len(edges),
        "conservative_graph_sha256": graph_hash,
        "colour_histogram": {colour: colour_histogram[colour]
                             for colour in sorted(colour_histogram)},
        "proper_four_colouring": True,
        "translated_source_fibres": 21,
        "all_fibre_pairs_intersect": True,
        "actual_chromatic_number": 4,
        "actual_support_order_interval": [210, 231],
        "actual_unit_graph_connected": True,
        "actual_unit_graph_bridgeless": True,
        "within_cluster_squared_distance_upper_lt": "1/10^48",
        "different_cluster_squared_separation_gt": "36/1000000",
        "excluded_squared_unit_gap_gt": "167/1000000",
    }


def verify(geometry_path=GEOMETRY, selfsum_path=SELFSUM,
           check_hashes=True, check_expected=False):
    geometry_path, selfsum_path = Path(geometry_path), Path(selfsum_path)
    if check_hashes:
        require(digest(geometry_path) == GEOMETRY_SHA256,
                "reviewed geometry hash")
        require(digest(selfsum_path) == SELFSUM_SHA256,
                "reviewed self-sum hash")
    geometry = json.loads(geometry_path.read_text())
    certificate = json.loads(selfsum_path.read_text())
    require(certificate["geometry_sha256"] == digest(geometry_path),
            "self-sum geometry binding")
    point_boxes, source_edges, source = source_review(geometry)
    selfsum = selfsum_review(point_boxes, source_edges, certificate)
    result = {
        "status": "ACCEPT_WITH_ONE_ROOT_AND_ONE_OPERATION_LIMITATION",
        "reviewed_geometry_sha256": digest(geometry_path),
        "reviewed_selfsum_sha256": digest(selfsum_path),
        "source": source,
        "selfsum": selfsum,
        "record_candidate": False,
    }
    if check_expected:
        require(json.loads(EXPECTED.read_text()) == result, "EXPECTED mismatch")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", type=Path, default=GEOMETRY)
    parser.add_argument("--selfsum", type=Path, default=SELFSUM)
    parser.add_argument("--no-hashes", action="store_true")
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    print(json.dumps(verify(arguments.geometry, arguments.selfsum,
                            not arguments.no_hashes, arguments.check_expected),
                     indent=2, sort_keys=True))
