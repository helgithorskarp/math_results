#!/usr/bin/env python3
"""Exact standard-library verifier for the flexible-fish contact theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_CERTIFICATE = HERE / "geometry_certificate.json"
DEFAULT_RELATION = HERE / "relation_certificate.json"
FIXED = {0: (0, 0), 1: (1, 0)}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def proper(word, edges, colours=4):
    return (len(word) == 23 and set(word) <= set(map(str, range(colours)))
            and all(word[a] != word[b] for a, b in edges))


def three_colour_search(edges):
    """Exhaustive deterministic DSATUR decision; false result proves non-3."""
    adjacency = [set() for _ in range(23)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colour = [-1]*23
    colour[0], colour[1] = 0, 1
    nodes = 0

    def visit(left):
        nonlocal nodes
        nodes += 1
        if not left:
            return True
        vertex = max(left, key=lambda v: (
            len({colour[w] for w in adjacency[v] if colour[w] >= 0}),
            len(adjacency[v]), -v))
        forbidden = {colour[w] for w in adjacency[vertex] if colour[w] >= 0}
        for value in range(3):
            if value not in forbidden:
                colour[vertex] = value
                if visit(left-{vertex}):
                    return True
        colour[vertex] = -1
        return False

    return visit(set(range(2, 23))), nodes


def verify(path=DEFAULT_CERTIFICATE, relation_path=DEFAULT_RELATION):
    path = Path(path)
    relation_path = Path(relation_path)
    certificate = json.loads(path.read_text())
    require(certificate["schema"] == "fish-self-contact-root-v1", "schema")
    source_edges = list(map(tuple, certificate["source_edges"]))
    require(source_edges == sorted(set(source_edges)) and len(source_edges) == 42,
            "source edge list")
    require(source_edges[0] == (0, 1), "fixed source edge")
    target = tuple(certificate["target_contact"])
    require(target == (10, 21) and target not in source_edges, "target contact")
    full_edges = sorted(source_edges+[target])
    equations = [edge for edge in full_edges if edge != (0, 1)]
    free = [vertex for vertex in range(23) if vertex not in FIXED]
    where = {vertex: i for i, vertex in enumerate(free)}
    require(len(equations) == 2*len(free) == 42, "square equation system")

    h = certificate["midpoint_denominator"]
    d = certificate["inverse_denominator"]
    radius_denominator = certificate["radius_denominator"]
    require(all(type(value) is int and value > 0
                for value in (h, d, radius_denominator)), "denominators")
    midpoint = certificate["midpoint_numerators"]
    inverse = certificate["inverse_numerators"]
    require(len(midpoint) == 23 and all(len(row) == 2 for row in midpoint),
            "midpoint dimensions")
    require(len(inverse) == 42 and all(len(row) == 42 for row in inverse),
            "inverse dimensions")
    require(all(type(value) is int for row in midpoint for value in row),
            "midpoint integrality")
    require(all(type(value) is int for row in inverse for value in row),
            "inverse integrality")
    require(certificate["fixed_vertices"] ==
            {str(v): list(point) for v, point in FIXED.items()}, "fixed vertices")
    for vertex, point in FIXED.items():
        require(midpoint[vertex] == [h*x for x in point], "fixed midpoint")

    jacobian = [[0]*42 for _ in range(42)]
    residual = []
    for row, (a, b) in enumerate(equations):
        dx = midpoint[a][0]-midpoint[b][0]
        dy = midpoint[a][1]-midpoint[b][1]
        residual.append(dx*dx+dy*dy-h*h)
        if a in where:
            jacobian[row][2*where[a]] = 2*dx
            jacobian[row][2*where[a]+1] = 2*dy
        if b in where:
            jacobian[row][2*where[b]] = -2*dx
            jacobian[row][2*where[b]+1] = -2*dy

    defect = [
        [int(i == j)*d*h-sum(inverse[i][k]*jacobian[k][j]
                              for k in range(42))
         for j in range(42)]
        for i in range(42)
    ]
    beta = Q(max(sum(abs(value) for value in row) for row in defect), d*h)
    inverse_norm = Q(max(sum(abs(value) for value in row) for row in inverse), d)
    residual_image = Q(max(abs(sum(inverse[i][k]*residual[k]
                                       for k in range(42)))
                           for i in range(42)), d*h*h)
    radius = Q(1, radius_denominator)
    eta = beta+16*radius*inverse_norm
    displacement = residual_image+eta*radius
    require(beta < 1 and eta < 1 and displacement < radius,
            "contraction and ball inclusion")

    points = [tuple(Q(value, h) for value in point) for point in midpoint]
    minimum_separation = None
    minimum_nonedge_gap = None
    for a, b in combinations(range(23), 2):
        dx = points[a][0]-points[b][0]
        dy = points[a][1]-points[b][1]
        distance2 = dx*dx+dy*dy
        error = 4*radius*(abs(dx)+abs(dy))+8*radius*radius
        require(distance2 > error, f"unresolved collision {(a, b)}")
        margin = distance2-error
        minimum_separation = margin if minimum_separation is None else min(
            minimum_separation, margin)
        if (a, b) not in full_edges:
            require(abs(distance2-1) > error, f"unresolved nonedge {(a, b)}")
            margin = abs(distance2-1)-error
            minimum_nonedge_gap = margin if minimum_nonedge_gap is None else min(
                minimum_nonedge_gap, margin)

    blocked = certificate["source_blocked_word"]
    surviving = certificate["surviving_complete_word"]
    three_colourable, search_nodes = three_colour_search(source_edges)
    require(not three_colourable, "source unexpectedly three-colourable")
    require(proper(blocked, source_edges), "blocked source word is improper")
    require(blocked[target[0]] == blocked[target[1]],
            "blocked word does not witness source loss")
    require(not proper(blocked, full_edges), "blocked word survived contact")
    require(proper(surviving, full_edges), "surviving word is improper")

    relation = json.loads(relation_path.read_text())
    require(relation["schema"] == "fish-contact-pair-cover-v1", "relation schema")
    require(relation["fixed_edge_colours"] == {"0": 0, "1": 1},
            "fixed edge colours")
    words = relation["words"]
    require(len(words) == len(set(words)) and words, "relation word set")
    require(all(proper(word, full_edges) for word in words),
            "improper relation word")
    nonedges = [pair for pair in combinations(range(23), 2)
                if pair not in full_edges]
    for pair in nonedges:
        states = {words[index][pair[0]] == words[index][pair[1]]
                  for index in range(len(words))}
        require(states == {False, True}, f"uncovered nonedge {pair}")
    for omitted in range(len(words)):
        require(any(len({words[index][pair[0]] == words[index][pair[1]]
                         for index in range(len(words)) if index != omitted}) < 2
                    for pair in nonedges),
                f"relation word {omitted} is redundant")

    graph_rows = [f"{a} {b}" for a, b in full_edges]
    edge_hash = hashlib.sha256(("\n".join(graph_rows)+"\n").encode()).hexdigest()
    return {
        "status": "EXACT FISH CONTACT SOURCE-LOSS AND PAIR-NEUTRALITY VERIFIED",
        "vertices": 23,
        "source_edges": len(source_edges),
        "complete_unit_edges": len(full_edges),
        "new_contacts": [list(target)],
        "chromatic_number": 4,
        "blocked_complete_source_colourings_at_least": 1,
        "surviving_complete_source_colourings_at_least": 1,
        "complete_physical_colour_words": len(words),
        "nonedges_pair_neutral": len(nonedges),
        "forced_equal_nonedges": 0,
        "forced_different_nonedges": 0,
        "unit_pairs_forced_different": len(full_edges),
        "relation_cover_inclusion_minimal": True,
        "three_colour_search_nodes": search_nodes,
        "radius": str(radius),
        "beta": str(beta),
        "inverse_norm": str(inverse_norm),
        "eta": str(eta),
        "self_map_displacement": str(displacement),
        "squared_separation_lower": str(minimum_separation),
        "nonedge_squared_unit_gap_lower": str(minimum_nonedge_gap),
        "edge_stream_sha256": edge_hash,
        "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "relation_certificate_sha256": hashlib.sha256(
            relation_path.read_bytes()).hexdigest(),
        "colour_word_stream_sha256": hashlib.sha256(
            (("\n".join(words))+"\n").encode()).hexdigest(),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", nargs="?", type=Path,
                        default=DEFAULT_CERTIFICATE)
    parser.add_argument("--relation-certificate", type=Path,
                        default=DEFAULT_RELATION)
    args = parser.parse_args()
    print(json.dumps(verify(args.certificate, args.relation_certificate),
                     indent=2, sort_keys=True))
