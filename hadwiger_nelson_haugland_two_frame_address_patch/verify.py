#!/usr/bin/env python3
"""Standard-library exact checker for the frozen two-frame support."""

from __future__ import annotations

import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import model as M


EXPECTED_CROSS = [(56, 461), (83, 461), (123, 461), (193, 461), (197, 461)]


def check_word(word, order, edges):
    M.require(type(word) is str and len(word) == order, "four-word length")
    M.require(set(word) <= set("0123"), "four-word alphabet")
    colours = list(map(int, word))
    M.require(all(colours[u] != colours[v] for u, v in edges), "monochromatic unit edge")


def not_three_colourable(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    colours = {v: -1 for v in vertices}
    nodes = 0

    def visit():
        nonlocal nodes
        nodes += 1
        uncoloured = [v for v in vertices if colours[v] < 0]
        if not uncoloured:
            return True
        v = max(uncoloured, key=lambda x: (len({colours[y] for y in adjacency[x] if colours[y] >= 0}), len(adjacency[x]), -x))
        forbidden = {colours[y] for y in adjacency[v] if colours[y] >= 0}
        for colour in range(3):
            if colour not in forbidden:
                colours[v] = colour
                if visit():
                    return True
        colours[v] = -1
        return False

    return not visit(), nodes


def scope_check(points):
    source = M.HERE.parent / "hadwiger_nelson_haugland2131_strict_edges/independent_check.py"
    graph = M.HERE.parent / "hadwiger_nelson_haugland2131_exact_reproduction/graph.json"
    M.require(sha256(source.read_bytes()).hexdigest() == "5e7f356bb66237a7f8f46ac01ca4a29a3bc23fc382296ec476fd09d6cdde8916", "pinned parent geometry")
    M.require(sha256(graph.read_bytes()).hexdigest() == "201196679760fc329fff548346b843a821646ce5ffc326a91cc24598effc299d", "pinned parent paths")
    spec = importlib.util.spec_from_file_location("hn_parent_geometry_two_frame_scope", source)
    G = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(G)
    payload = json.loads(graph.read_text())
    sqrt3, vectors = G.field_constants()
    g1 = G.build_g1(payload["paths"], sqrt3, vectors)
    g2 = G.build_g2(g1, sqrt3)
    parent = set(G.build_g3(g2, sqrt3))
    M.require((len(g1), len(g2), len(parent)) == (740, 1066, 2131), "parent counts")

    def lift(value):
        out = G.ZERO
        for exponent, coefficient in enumerate(value):
            out = G.add(out, G.scale(G.power(G.ZETA, 2 * exponent), coefficient))
        return out

    def cartesian(value):
        z, zbar = lift(value), lift(M.F.conj(value))
        x = G.scale(G.add(z, zbar), M.Q(1, 2))
        y = G.scale(G.multiply(G.sub(z, zbar), G.neg(G.power(G.ZETA, 21))), M.Q(1, 2))
        return x, y

    converted = []
    for a, b in points:
        xa, ya = cartesian(a)
        xb, yb = cartesian(b)
        converted.append(((xa, xb), (ya, yb)))
    frame_a_hits = sum(point in parent for point in converted[:231])
    frame_b_hits = sum(point in parent for point in converted[231:])
    M.require((frame_a_hits, frame_b_hits) == (7, 0), "parent intersection counts")
    return {"frame_a_points_in_parent": frame_a_hits, "frame_b_points_in_parent": frame_b_hits,
            "support_not_parent_subset": True}


def verify(certificate, with_scope=False):
    M.require(certificate["version"] == 1, "certificate version")
    M.require(certificate["anchors"] == [197, 230], "frozen anchor labels")
    normalized, patch, translation, points = M.construction()
    M.require(M.enorm(M.ALPHA) == M.EONE, "second-frame multiplier is not a rotation")
    edges, survivors, exact_rejects = M.complete_edges(points)
    M.require(edges == sorted(set(edges)), "edge ordering")
    cross = [(u, v) for u, v in edges if u < 231 <= v]
    M.require(cross == EXPECTED_CROSS, "cross-frame contacts")
    M.require(len(edges) == 1853 and survivors == 1867 and exact_rejects == 14, "complete scan counts")
    M.require(M.coordinate_hash(points) == certificate["coordinate_sha256"], "coordinate hash")
    M.require(M.edge_hash(edges) == certificate["edge_sha256"], "edge hash")
    check_word(certificate["four_word"], len(points), edges)

    patch_index = {point: i for i, point in enumerate(patch)}
    source_vertices = [patch_index[point] for point in normalized]
    source_edges = [(source_vertices[u], source_vertices[v]) for u, v in M.F.edges(normalized, 1)]
    M.require(len(source_vertices) == 21 and len(source_edges) == 42, "embedded source")
    no_three, nodes = not_three_colourable(source_vertices, source_edges)
    M.require(no_three, "embedded source unexpectedly three-colourable")
    M.require(len(M.components(range(462), edges)) == 1, "whole graph connectivity")
    separated = M.components(range(462), edges, {461})
    M.require(len(separated) == 2 and sorted(map(len, separated)) == [230, 231], "contact bottleneck")

    result = {
        "status": "EXACT_TWO_FRAME_SUPPORT_FOUR_CHROMATIC",
        "vertices": 462,
        "unit_edges": 1853,
        "patch_vertices_each": 231,
        "patch_unit_edges_each": 924,
        "cross_edges": [list(edge) for edge in cross],
        "cross_edges_all_incident_to_global_vertex": 461,
        "components_after_contact_vertex_deletion": list(map(len, separated)),
        "modular_survivors": survivors,
        "exact_rejects": exact_rejects,
        "proper_four_word_checked": True,
        "embedded_21_point_source_not_three_colourable": True,
        "three_colour_search_nodes": nodes,
        "coordinate_sha256": certificate["coordinate_sha256"],
        "edge_sha256": certificate["edge_sha256"],
        "record_candidate": False,
    }
    if with_scope:
        result["scope"] = scope_check(points)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", action="store_true")
    args = parser.parse_args()
    certificate = json.loads((M.HERE / "certificate.json").read_text())
    print(json.dumps(verify(certificate, args.scope), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
