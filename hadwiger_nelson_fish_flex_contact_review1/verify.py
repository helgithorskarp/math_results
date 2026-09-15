#!/usr/bin/env python3
"""Independent exact review of the flexible-fish self-contact certificate.

The reviewed geometry checker uses a midpoint Jacobian defect plus one
closed-form quadratic error bound.  This checker instead evaluates every
Jacobian entry on the whole rational coordinate box and propagates rational
intervals through I-AJ(X).  It also uses direct interval squared distances
for the complete-pair scan and a static-order colouring search.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET = HERE.parent / "hadwiger_nelson_fish_flex_contact_source_loss"
GEOMETRY = TARGET / "geometry_certificate.json"
RELATION = TARGET / "relation_certificate.json"
EXPECTED = HERE / "EXPECTED.json"
GEOMETRY_SHA256 = "e079c2d86f0b3574e6e24d9fc18a9abc2d8b7d7fe111ba011d5978875d5fc732"
RELATION_SHA256 = "ffc789b63d1818f91d5fedb30bcc17996c26bb4de254602fb414115ab81554ac"
FIXED = {0: (Q(0), Q(0)), 1: (Q(1), Q(0))}
# Reconstructed independently from the operation sequence in the pinned
# Shibuya hodfish_vertices routine: explicit unit translations, the two
# parents of every cu construction, and its four closing equations.
SHIBUYA_CONSTRUCTION_EDGES = sorted([
    (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (1, 5),
    (4, 6), (3, 6), (6, 7), (5, 7), (2, 8), (6, 8),
    (0, 9), (7, 9), (8, 10), (1, 10), (9, 11), (3, 11),
    (4, 12), (10, 12), (2, 13), (6, 14), (13, 14),
    (13, 15), (6, 15), (1, 16), (15, 16), (16, 17), (14, 17),
    (5, 18), (18, 19), (6, 19), (6, 20), (18, 20),
    (20, 21), (0, 21), (19, 22), (21, 22),
    (2, 12), (5, 11), (2, 17), (5, 22),
])


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def iadd(x, y):
    return x[0] + y[0], x[1] + y[1]


def ineg(x):
    return -x[1], -x[0]


def iscale(c, x):
    a, b = c*x[0], c*x[1]
    return (a, b) if a <= b else (b, a)


def imaxabs(x):
    return max(abs(x[0]), abs(x[1]))


def isquare(x):
    lo, hi = x
    top = max(lo*lo, hi*hi)
    return (Q(0), top) if lo <= 0 <= hi else (min(lo*lo, hi*hi), top)


def idifference(x, y):
    return x[0] - y[1], x[1] - y[0]


def proper(word, edges, colours=4):
    return (len(word) == 23 and set(word) <= set(map(str, range(colours)))
            and all(word[a] != word[b] for a, b in edges))


def static_colour(edges, colours, values=None):
    """Complete fixed-order search; unlike the target this is not DSATUR."""
    adjacency = [set() for _ in range(23)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    require(1 in adjacency[0], "normalizing edge absent")
    order = list(range(2, 23))
    palette = list(range(colours)) if values is None else list(values)
    colour = [-1]*23
    colour[0], colour[1] = 0, 1
    nodes = 0

    def visit(index):
        nonlocal nodes
        nodes += 1
        if index == len(order):
            return True
        vertex = order[index]
        forbidden = {colour[w] for w in adjacency[vertex] if colour[w] >= 0}
        for value in palette:
            if value not in forbidden:
                colour[vertex] = value
                if visit(index + 1):
                    return True
        colour[vertex] = -1
        return False

    found = visit(0)
    return found, nodes, "".join(map(str, colour)) if found else None


def components(adjacency, omitted=frozenset()):
    seen = set()
    count = 0
    for start in range(len(adjacency)):
        if start in omitted or start in seen:
            continue
        count += 1
        stack = [start]
        seen.add(start)
        while stack:
            vertex = stack.pop()
            for neighbour in adjacency[vertex] - omitted:
                if neighbour not in seen:
                    seen.add(neighbour)
                    stack.append(neighbour)
    return count


def girth(adjacency):
    answer = len(adjacency) + 1
    for start in range(len(adjacency)):
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


def verify(geometry_path=GEOMETRY, relation_path=RELATION, check_hashes=True):
    geometry_path, relation_path = Path(geometry_path), Path(relation_path)
    if check_hashes:
        require(digest(geometry_path) == GEOMETRY_SHA256,
                "reviewed geometry hash")
        require(digest(relation_path) == RELATION_SHA256,
                "reviewed relation hash")
    certificate = json.loads(geometry_path.read_text())
    relation = json.loads(relation_path.read_text())
    require(certificate["schema"] == "fish-self-contact-root-v1", "schema")
    require(relation["schema"] == "fish-contact-pair-cover-v1",
            "relation schema")

    source_edges = [tuple(edge) for edge in certificate["source_edges"]]
    require(source_edges == sorted(set(source_edges)) and len(source_edges) == 42,
            "source edges")
    require(source_edges == SHIBUYA_CONSTRUCTION_EDGES,
            "source edges differ from reconstructed fish construction")
    contact = tuple(certificate["target_contact"])
    require(contact == (10, 21) and contact not in source_edges, "contact")
    full_edges = sorted(source_edges + [contact])
    edge_set = set(full_edges)
    equations = [edge for edge in full_edges if edge != (0, 1)]
    free_vertices = list(range(2, 23))
    position = {vertex: index for index, vertex in enumerate(free_vertices)}
    require(len(equations) == 42 == 2*len(free_vertices), "square system")

    h = certificate["midpoint_denominator"]
    d = certificate["inverse_denominator"]
    rd = certificate["radius_denominator"]
    require(all(type(x) is int and x > 0 for x in (h, d, rd)),
            "positive integer denominators")
    midpoint_rows = certificate["midpoint_numerators"]
    inverse_rows = certificate["inverse_numerators"]
    require(len(midpoint_rows) == 23
            and all(len(row) == 2 for row in midpoint_rows), "midpoint shape")
    require(len(inverse_rows) == 42
            and all(len(row) == 42 for row in inverse_rows), "inverse shape")
    require(all(type(x) is int for row in midpoint_rows for x in row),
            "midpoint integers")
    require(all(type(x) is int for row in inverse_rows for x in row),
            "inverse integers")
    midpoint = [tuple(Q(x, h) for x in row) for row in midpoint_rows]
    inverse = [[Q(x, d) for x in row] for row in inverse_rows]
    require(midpoint[0] == FIXED[0] and midpoint[1] == FIXED[1],
            "fixed midpoint")
    radius = Q(1, rd)
    coordinate_boxes = [
        ((x, x), (y, y)) if vertex in FIXED else
        ((x-radius, x+radius), (y-radius, y+radius))
        for vertex, (x, y) in enumerate(midpoint)
    ]

    # Exact residual at the box midpoint.
    residual = []
    for a, b in equations:
        dx = midpoint[a][0] - midpoint[b][0]
        dy = midpoint[a][1] - midpoint[b][1]
        residual.append(dx*dx + dy*dy - 1)
    image = [sum(inverse[i][k]*residual[k] for k in range(42))
             for i in range(42)]
    centre_displacement = max(map(abs, image))

    # Entrywise interval Jacobian on the entire box.
    jacobian_rows = []
    for a, b in equations:
        entries = {}
        for coordinate in (0, 1):
            difference = idifference(coordinate_boxes[a][coordinate],
                                     coordinate_boxes[b][coordinate])
            if a in position:
                entries[2*position[a] + coordinate] = iscale(Q(2), difference)
            if b in position:
                entries[2*position[b] + coordinate] = iscale(Q(-2), difference)
        jacobian_rows.append(entries)

    # D encloses I-AJ(X).  Its interval row norm is a Lipschitz constant
    # for T(X)=X-AF(X) on the box.
    contraction = Q(0)
    for i in range(42):
        row = [(Q(int(i == j)), Q(int(i == j))) for j in range(42)]
        for k, entries in enumerate(jacobian_rows):
            coefficient = inverse[i][k]
            if coefficient:
                for j, interval in entries.items():
                    row[j] = iadd(row[j], ineg(iscale(coefficient, interval)))
        contraction = max(contraction, sum(map(imaxabs, row)))
    self_map_bound = centre_displacement + contraction*radius
    require(contraction < 1, "interval contraction")
    require(self_map_bound < radius, "interval self-map")

    # Direct interval distance evaluation for every unordered point pair.
    separation_lower = None
    nonedge_unit_gap_lower = None
    for a, b in combinations(range(23), 2):
        dx = idifference(coordinate_boxes[a][0], coordinate_boxes[b][0])
        dy = idifference(coordinate_boxes[a][1], coordinate_boxes[b][1])
        distance2 = iadd(isquare(dx), isquare(dy))
        require(distance2[0] > 0, f"collision not excluded: {(a, b)}")
        separation_lower = (distance2[0] if separation_lower is None else
                            min(separation_lower, distance2[0]))
        if (a, b) not in edge_set:
            if distance2[1] < 1:
                gap = 1 - distance2[1]
            elif distance2[0] > 1:
                gap = distance2[0] - 1
            else:
                raise ValueError(f"extra unit pair not excluded: {(a, b)}")
            nonedge_unit_gap_lower = (gap if nonedge_unit_gap_lower is None
                                      else min(nonedge_unit_gap_lower, gap))

    # Independent complete graph-colouring checks.
    source_three, source_nodes, _ = static_colour(source_edges, 3)
    require(not source_three, "source is three-colourable")
    complete_three, complete_nodes, _ = static_colour(full_edges, 3)
    require(not complete_three, "complete graph is three-colourable")
    complete_four, four_nodes, fresh_word = static_colour(
        full_edges, 4, values=(3, 2, 1, 0))
    require(complete_four and proper(fresh_word, full_edges),
            "fresh four-colouring")

    blocked = certificate["source_blocked_word"]
    surviving = certificate["surviving_complete_word"]
    require(proper(blocked, source_edges), "blocked source word")
    require(blocked[10] == blocked[21]
            and not proper(blocked, full_edges), "source-loss witness")
    require(proper(surviving, full_edges), "surviving target word")

    require(relation["fixed_edge_colours"] == {"0": 0, "1": 1},
            "relation normalization")
    words = relation["words"]
    require(words and len(words) == len(set(words)), "distinct cover words")
    require(all(proper(word, full_edges) for word in words), "cover properness")
    require(fresh_word not in set(words + [blocked, surviving]),
            "fresh word unexpectedly duplicated")
    nonedges = [pair for pair in combinations(range(23), 2)
                if pair not in edge_set]
    requests = {}
    for pair in nonedges:
        states = {word[pair[0]] == word[pair[1]] for word in words}
        require(states == {False, True}, f"pair state missing: {pair}")
        for state in (False, True):
            requests[pair, state] = [i for i, word in enumerate(words)
                                     if (word[pair[0]] == word[pair[1]]) == state]
    essential_requests = []
    for index in range(len(words)):
        witnesses = sorted((pair, state) for (pair, state), owners in requests.items()
                           if owners == [index])
        require(witnesses, f"cover word {index} is not essential")
        pair, state = witnesses[0]
        essential_requests.append([index, list(pair), "equal" if state else "different"])

    # Structural checks keep the geometric result separate from one-sum and
    # bridge phenomena.  Minimum degree three plus no cut of size <=2 gives
    # exact vertex connectivity three.
    adjacency = [set() for _ in range(23)]
    for a, b in full_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    require(components(adjacency) == 1, "disconnected graph")
    require(all(components(adjacency, frozenset(cut)) == 1
                for size in (1, 2)
                for cut in combinations(range(23), size)), "small vertex cut")
    degree_histogram = Counter(map(len, adjacency))
    require(min(degree_histogram) == 3, "minimum degree")
    graph_girth = girth(adjacency)

    edge_stream = "".join(f"{a} {b}\n" for a, b in full_edges)
    return {
        "status": "ACCEPT_WITH_STRICT_ONE_ROOT_PAIR_NEUTRAL_LIMITATION",
        "reviewed_geometry_sha256": digest(geometry_path),
        "reviewed_relation_sha256": digest(relation_path),
        "vertices": 23,
        "source_edges": len(source_edges),
        "complete_unit_edges": len(full_edges),
        "new_contact": list(contact),
        "chromatic_number_source": 4,
        "chromatic_number_complete": 4,
        "static_source_3colour_nodes": source_nodes,
        "static_complete_3colour_nodes": complete_nodes,
        "fresh_4colour_nodes": four_nodes,
        "fresh_4colour_word": fresh_word,
        "fresh_word_differs_from_all_target_words": True,
        "box_radius": str(radius),
        "interval_contraction_bound": str(contraction),
        "centre_displacement": str(centre_displacement),
        "self_map_bound": str(self_map_bound),
        "squared_separation_lower": str(separation_lower),
        "nonedge_squared_unit_gap_lower": str(nonedge_unit_gap_lower),
        "physical_nonedges": len(nonedges),
        "pair_state_requests_checked": 2*len(nonedges),
        "pair_neutral_nonedges": len(nonedges),
        "relation_cover_words": len(words),
        "relation_cover_inclusion_minimal": True,
        "essential_requests": essential_requests,
        "vertex_connectivity": 3,
        "degree_histogram": {str(k): degree_histogram[k]
                             for k in sorted(degree_histogram)},
        "girth": graph_girth,
        "edge_stream_sha256": hashlib.sha256(edge_stream.encode()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--geometry", type=Path, default=GEOMETRY)
    parser.add_argument("--relation", type=Path, default=RELATION)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    result = verify(args.geometry, args.relation)
    if args.check_expected:
        require(json.loads(EXPECTED.read_text()) == result, "EXPECTED mismatch")
    print(json.dumps(result, indent=2, sort_keys=True))
