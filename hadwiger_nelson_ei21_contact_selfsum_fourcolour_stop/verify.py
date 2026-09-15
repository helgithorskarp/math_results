#!/usr/bin/env python3
"""Exact standard-library verifier for the EI21 contact and its self-sum.

No floating-point arithmetic or external solver is used.  The first half
checks a rational contraction certificate for one 21-point strict unit graph.
The second half constructs a conservative supergraph for all 231 unordered
sums.  A supplied four-colour word on that supergraph colours every possible
complete exact physical graph represented by the certified coordinate boxes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement
from pathlib import Path


HERE = Path(__file__).resolve().parent
GEOMETRY = HERE / "geometry_certificate.json"
SELFSUM = HERE / "selfsum_certificate.json"
EXPECTED = HERE / "EXPECTED.json"
FIXED = {0: (0, 0), 1: (0, -1)}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def proper(word, n, edges, colours=4):
    return (len(word) == n and set(word) <= set(map(str, range(colours)))
            and all(word[a] != word[b] for a, b in edges))


def k_colour_search(n, edges, k):
    """Deterministic exhaustive DSATUR; a false result proves impossibility."""
    adjacency = [set() for _ in range(n)]
    for a, b in edges:
        adjacency[a].add(b); adjacency[b].add(a)
    colour = [-1]*n
    colour[0] = 0
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
        for value in range(k):
            if value not in forbidden:
                colour[vertex] = value
                if visit(left-{vertex}):
                    return True
        colour[vertex] = -1
        return False

    return visit(set(range(1, n))), nodes


def connected_without(n, edges, removed_vertex=None, removed_edge=None):
    adjacency = [set() for _ in range(n)]
    for edge in edges:
        if edge == removed_edge:
            continue
        a, b = edge
        if a == removed_vertex or b == removed_vertex:
            continue
        adjacency[a].add(b); adjacency[b].add(a)
    vertices = [v for v in range(n) if v != removed_vertex]
    seen = {vertices[0]}; stack = [vertices[0]]
    while stack:
        v = stack.pop()
        for w in adjacency[v]-seen:
            seen.add(w); stack.append(w)
    return len(seen) == len(vertices)


def source_replay(path):
    path = Path(path)
    certificate = json.loads(path.read_text())
    need(certificate["schema"] == "ei21-contact-root-v1", "geometry schema")
    source = list(map(tuple, certificate["source_edges"]))
    need(source == sorted(set(source)) and len(source) == 38, "source edges")
    need(source[0] == (0, 1), "fixed source edge")
    target = tuple(certificate["target_contact"])
    need(target == (0, 14) and target not in source, "target contact")
    full = sorted(source+[target])
    equations = [edge for edge in full if edge != (0, 1)]
    free = [v for v in range(21) if v not in FIXED]
    where = {v: i for i, v in enumerate(free)}
    need(len(equations) == 2*len(free) == 38, "square system")

    h = certificate["midpoint_denominator"]
    d = certificate["inverse_denominator"]
    radius_denominator = certificate["radius_denominator"]
    need(all(type(x) is int and x > 0 for x in (h, d, radius_denominator)),
         "denominators")
    midpoint = certificate["midpoint_numerators"]
    inverse = certificate["inverse_numerators"]
    need(len(midpoint) == 21 and all(len(row) == 2 for row in midpoint),
         "midpoint dimensions")
    need(len(inverse) == 38 and all(len(row) == 38 for row in inverse),
         "inverse dimensions")
    need(all(type(x) is int for row in midpoint for x in row),
         "midpoint integrality")
    need(all(type(x) is int for row in inverse for x in row),
         "inverse integrality")
    need(certificate["fixed_vertices"] ==
         {str(v): list(p) for v, p in FIXED.items()}, "fixed vertices")
    for vertex, point in FIXED.items():
        need(midpoint[vertex] == [h*x for x in point], "fixed midpoint")

    jacobian = [[0]*38 for _ in range(38)]
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
    defect = [[int(i == j)*d*h-sum(inverse[i][k]*jacobian[k][j]
               for k in range(38)) for j in range(38)] for i in range(38)]
    beta = Q(max(sum(abs(x) for x in row) for row in defect), d*h)
    inverse_norm = Q(max(sum(abs(x) for x in row) for row in inverse), d)
    residual_image = Q(max(abs(sum(inverse[i][k]*residual[k]
                                       for k in range(38)))
                           for i in range(38)), d*h*h)
    radius = Q(1, radius_denominator)
    eta = beta+16*radius*inverse_norm
    displacement = residual_image+eta*radius
    need(beta < 1 and eta < 1 and displacement < radius,
         "contraction and ball inclusion")

    points = [tuple(Q(x, h) for x in p) for p in midpoint]
    minimum_separation = None; minimum_nonedge_gap = None
    for a, b in combinations(range(21), 2):
        dx = points[a][0]-points[b][0]
        dy = points[a][1]-points[b][1]
        distance2 = dx*dx+dy*dy
        error = 4*radius*(abs(dx)+abs(dy))+8*radius*radius
        need(distance2 > error, f"unresolved collision {(a, b)}")
        margin = distance2-error
        minimum_separation = margin if minimum_separation is None else min(
            minimum_separation, margin)
        if (a, b) not in full:
            need(abs(distance2-1) > error, f"unresolved nonedge {(a, b)}")
            margin = abs(distance2-1)-error
            minimum_nonedge_gap = margin if minimum_nonedge_gap is None else min(
                minimum_nonedge_gap, margin)

    blocked = certificate["source_blocked_word"]
    surviving = certificate["surviving_complete_word"]
    three_colourable, search_nodes = k_colour_search(21, source, 3)
    need(not three_colourable, "source unexpectedly three-colourable")
    need(proper(blocked, 21, source), "blocked source word")
    need(blocked[target[0]] == blocked[target[1]], "blocked equality")
    need(not proper(blocked, 21, full), "blocked word survived")
    need(proper(surviving, 21, full), "surviving contact word")
    need(connected_without(21, full), "disconnected contact graph")
    articulations = [v for v in range(21)
                     if not connected_without(21, full, removed_vertex=v)]
    bridges = [edge for edge in full
               if not connected_without(21, full, removed_edge=edge)]
    need(not articulations and not bridges, "separable contact graph")
    edge_stream = "".join(f"{a} {b}\n" for a, b in full)
    summary = {
        "vertices": 21,
        "source_edges": 38,
        "complete_unit_edges": 39,
        "new_contact": list(target),
        "source_chromatic_number": 4,
        "contact_graph_chromatic_number": 4,
        "blocked_complete_source_colourings_at_least": 1,
        "surviving_complete_source_colourings_at_least": 1,
        "articulation_vertices": articulations,
        "bridges": [list(edge) for edge in bridges],
        "three_colour_search_nodes": search_nodes,
        "radius": str(radius),
        "beta": str(beta),
        "eta": str(eta),
        "self_map_displacement": str(displacement),
        "squared_separation_lower": str(minimum_separation),
        "nonedge_squared_unit_gap_lower": str(minimum_nonedge_gap),
        "edge_stream_sha256": hashlib.sha256(edge_stream.encode()).hexdigest(),
        "geometry_certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }
    return points, radius, full, summary


def components(n, edges):
    parent = list(range(n))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in edges:
        a, b = find(a), find(b)
        if a != b:
            parent[b] = a
    out = {}
    for v in range(n):
        out.setdefault(find(v), []).append(v)
    return sorted(out.values(), key=lambda c: c[0])


def squared_error(dx, dy, coordinate_error):
    return (2*coordinate_error*(abs(dx)+abs(dy))
            + 2*coordinate_error*coordinate_error)


def selfsum_replay(path, geometry_path, points, radius, source_edges):
    path = Path(path); certificate = json.loads(path.read_text())
    need(certificate["schema"] ==
         "ei21-contact-commutative-selfsum-fourcolour-stop-v1",
         "self-sum schema")
    geometry_hash = hashlib.sha256(Path(geometry_path).read_bytes()).hexdigest()
    need(certificate["geometry_sha256"] == geometry_hash, "geometry hash")
    addresses = list(combinations_with_replacement(range(21), 2))
    need(len(addresses) == certificate["formal_address_count"] == 231,
         "address count")
    mids = [(points[i][0]+points[j][0], points[i][1]+points[j][1])
            for i, j in addresses]
    address_error = 2*radius
    possible_equal = []
    for a, b in combinations(range(231), 2):
        if all(abs(mids[a][d]-mids[b][d]) <= 2*address_error
               for d in range(2)):
            possible_equal.append((a, b))
    clusters = components(231, possible_equal)
    need(len(clusters) == certificate["possible_equality_cluster_count"] == 210,
         "cluster count")
    cluster_of = {a: c for c, members in enumerate(clusters) for a in members}
    pair_error = 2*address_error
    possible_edges = set(); within_upper = Q(0)
    separation_lower = None; excluded_gap = None
    pair_checks = 0
    for a, b in combinations(range(231), 2):
        dx = mids[a][0]-mids[b][0]
        dy = mids[a][1]-mids[b][1]
        distance2 = dx*dx+dy*dy
        error = squared_error(dx, dy, pair_error)
        pair_checks += 1
        if cluster_of[a] == cluster_of[b]:
            upper = distance2+error
            need(upper < 1, "possible within-cluster unit pair")
            within_upper = max(within_upper, upper)
            continue
        need(distance2 > error, "possible equality crosses clusters")
        gap = distance2-error
        separation_lower = gap if separation_lower is None else min(
            separation_lower, gap)
        if abs(distance2-1) <= error:
            possible_edges.add(tuple(sorted((cluster_of[a], cluster_of[b]))))
        else:
            gap = abs(distance2-1)-error
            excluded_gap = gap if excluded_gap is None else min(excluded_gap, gap)
    edges = sorted(possible_edges)
    need(len(edges) == certificate["possible_unit_cluster_edge_count"] == 731,
         "possible edge count")
    graph_stream = json.dumps({"clusters": clusters, "edges": edges},
                              separators=(",", ":"))+"\n"
    graph_hash = hashlib.sha256(graph_stream.encode()).hexdigest()
    need(graph_hash == certificate["conservative_graph_sha256"], "graph hash")
    word = certificate["four_colour_word"]
    need(proper(word, 210, edges), "self-sum four-colour word")

    # The addresses (0,i) form the exact translated fibre p_0+P.  The source
    # replay proves it is a four-chromatic subgraph, so the actual self-sum is
    # at least four-chromatic; the conservative word proves the upper bound.
    fibre = [addresses.index((0, i)) for i in range(21)]
    need(len({cluster_of[a] for a in fibre}) == 21, "fibre collision")
    need(all(tuple(sorted((cluster_of[fibre[a]], cluster_of[fibre[b]]))) in possible_edges
             for a, b in source_edges), "source fibre edge missing")
    return {
        "formal_address_count": 231,
        "distinct_physical_point_lower_bound": 210,
        "distinct_physical_point_upper_bound": 231,
        "possible_equality_cluster_count": 210,
        "formal_address_pair_checks": pair_checks,
        "possible_unit_cluster_edge_count": 731,
        "within_cluster_squared_distance_upper": str(within_upper),
        "different_cluster_squared_separation_lower": str(separation_lower),
        "excluded_squared_unit_gap_lower": str(excluded_gap),
        "conservative_graph_sha256": graph_hash,
        "actual_chromatic_number": 4,
        "proper_four_colouring": True,
        "selfsum_certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def verify(geometry_path=GEOMETRY, selfsum_path=SELFSUM, check_expected=True):
    points, radius, full_edges, source = source_replay(geometry_path)
    selfsum = selfsum_replay(selfsum_path, geometry_path, points, radius, full_edges)
    summary = {
        "status": "EXACT EI21 CONTACT AND SELF-SUM FOUR-COLOUR STOP VERIFIED",
        "scope": "one frozen EI21 self-contact and its complete commutative self-sum",
        "source": source,
        "selfsum": selfsum,
        "record_candidate": False,
    }
    if check_expected:
        need(summary == json.loads(EXPECTED.read_text()), "expected summary")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("geometry", nargs="?", type=Path, default=GEOMETRY)
    parser.add_argument("--selfsum", type=Path, default=SELFSUM)
    parser.add_argument("--no-expected", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.geometry, args.selfsum, not args.no_expected),
                     indent=2, sort_keys=True))
