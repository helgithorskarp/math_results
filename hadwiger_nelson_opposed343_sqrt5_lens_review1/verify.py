#!/usr/bin/env python3
"""Independent exact review of the opposed-S343 sqrt(5) lens layer.

The target verifier is not imported.  Arithmetic uses the quadratic tower
Q(sqrt(3),sqrt(11)) plus sqrt(5), rather than a flat radicand lookup or
square-class masks.  The reviewed S343 theorem is an explicit dependency.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from itertools import combinations, product
from pathlib import Path


sys.setrecursionlimit(2000)

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TARGET = ROOT / "hadwiger_nelson_opposed343_sqrt5_lens_stop"
B_SOURCE = ROOT / "hadwiger_nelson_nonmono159_214_lowden2/points214.tsv"
PARENT = ROOT / "hadwiger_nelson_golomb_opposed_b214_stop"
PARENT_REVIEW = ROOT / "hadwiger_nelson_golomb_opposed_b214_review1"

PINNED = {
    TARGET / "certificate.json":
        "a412d0e0b18e6113319a645c21d2562db43218a315c907cd2636ff4fc60a179b",
    B_SOURCE:
        "97c9b3a964ed19874ae3fe932eb8c085fd637f618d2481fffaebbd1fbae55c2f",
    PARENT / "certificate.json":
        "3f6a4a13ead37de71ceb3cd1818d21a9036ea0273e151461fc54d9df1a8c2e19",
    PARENT_REVIEW / "EXPECTED.json":
        "4e4724c48f4f673c7e21b7ac4a0dac0c0feaa14d86dd750e085efea9536fce0a",
}

SCALE = 144
E_ZERO = (0, 0, 0, 0)
F_ZERO = (E_ZERO, E_ZERO)
UNIT_SQUARED = ((SCALE * SCALE, 0, 0, 0), E_ZERO)
CENTRE_SQUARED = ((16 * SCALE * SCALE // 9, 0, 0, 0), E_ZERO)

# Canonical seven-vertex Moser-spindle graph.
MOSER_EDGES = {
    (0, 1), (0, 2), (0, 4), (1, 2), (1, 6), (2, 6),
    (3, 4), (3, 5), (3, 6), (4, 5), (5, 6),
}


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def stream_hash(rows) -> str:
    return sha256(("\n".join(rows) + "\n").encode("ascii"))


def e_add(first, second):
    return tuple(a + b for a, b in zip(first, second, strict=True))


def e_neg(value):
    return tuple(-coefficient for coefficient in value)


def e_scale(value, scalar):
    return tuple(scalar * coefficient for coefficient in value)


def e_mul(first, second):
    """Multiply in E=Q(sqrt(3),sqrt(11)), basis 1,r,s,rs."""
    a, b, c, d = first
    A, B, C, D = second
    return (
        a * A + 3 * b * B + 11 * c * C + 33 * d * D,
        a * B + b * A + 11 * (c * D + d * C),
        a * C + c * A + 3 * (b * D + d * B),
        a * D + d * A + b * C + c * B,
    )


def f_add(first, second):
    return e_add(first[0], second[0]), e_add(first[1], second[1])


def f_neg(value):
    return e_neg(value[0]), e_neg(value[1])


def f_sub(first, second):
    return f_add(first, f_neg(second))


def f_mul(first, second):
    """Multiply (u+v sqrt(5))(x+y sqrt(5)) as a quadratic tower."""
    u, v = first
    x, y = second
    return (e_add(e_mul(u, x), e_scale(e_mul(v, y), 5)),
            e_add(e_mul(u, y), e_mul(v, x)))


def f_div_exact(value, divisor):
    need(divisor > 0, "nonpositive divisor")
    flat = value[0] + value[1]
    need(all(coefficient % divisor == 0 for coefficient in flat),
         "nonintegral division")
    return (tuple(coefficient // divisor for coefficient in value[0]),
            tuple(coefficient // divisor for coefficient in value[1]))


def sqrt5_times(value):
    # sqrt(5)(u+v sqrt(5)) = 5v+u sqrt(5).
    return e_scale(value[1], 5), value[0]


def axis_from_flat(flat):
    """Target order: 1,r,root5,r*root5,s,rs,s*root5,rs*root5."""
    need(len(flat) == 8, "axis arity")
    return ((flat[0], flat[1], flat[4], flat[5]),
            (flat[2], flat[3], flat[6], flat[7]))


def axis_to_flat(axis):
    u, v = axis
    return (u[0], u[1], v[0], v[1], u[2], u[3], v[2], v[3])


def squared_distance(first, second):
    dx = f_sub(first[0], second[0])
    dy = f_sub(first[1], second[1])
    return f_add(f_mul(dx, dx), f_mul(dy, dy))


def exact_edges(points):
    return tuple(
        (first, second)
        for first, second in combinations(range(len(points)), 2)
        if squared_distance(points[first], points[second]) == UNIT_SQUARED
    )


def point_hash(points):
    return stream_hash(
        " ".join(map(str, axis_to_flat(x) + axis_to_flat(y)))
        for x, y in points
    )


def edge_hash(edges):
    return stream_hash(f"{first} {second}" for first, second in edges)


def pair_hash(pairs):
    return stream_hash(f"{first} {second}" for first, second in pairs)


def golomb():
    rows = (
        (0, 0, 0, 0), (36, 0, 0, 0), (18, 0, 18, 0),
        (-18, 0, 18, 0), (-36, 0, 0, 0), (-18, 0, -18, 0),
        (18, 0, -18, 0), (6, 0, 0, 6), (-3, -3, 3, -3),
        (-3, 3, -3, -3),
    )
    points = []
    for a, b, c, d in rows:
        x = ((4 * a, 0, 0, 4 * b), E_ZERO)
        y = ((0, 4 * c, 4 * d, 0), E_ZERO)
        points.append((x, y))
    return tuple(points)


def read_b214():
    points = []
    for line in B_SOURCE.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("#"):
            continue
        row = tuple(map(int, line.split()))
        need(len(row) == 16, "B214 coordinate arity")
        need(all(row[index] == 0 for index in range(16)
                 if index not in (0, 5, 9, 12)), "B214 outside E")
        x = axis_from_flat(tuple(12 * coefficient for coefficient in row[:8]))
        y = axis_from_flat(tuple(12 * coefficient for coefficient in row[8:]))
        points.append((x, y))
    need(len(points) == len(set(points)) == 214, "B214 order")
    return tuple(points)


def shift_b214(points, reflected):
    out = []
    shift = ((72 if reflected else -72, 0, 0, 0), E_ZERO)
    for x, y in points:
        xx = f_neg(x) if reflected else x
        out.append((f_add(xx, shift), y))
    return tuple(out)


def merge_blocks(*blocks):
    points = []
    index = {}
    maps = []
    for block in blocks:
        image = []
        for point in block:
            if point not in index:
                index[point] = len(points)
                points.append(point)
            image.append(index[point])
        maps.append(image)
    return tuple(points), maps


def build_source():
    g = golomb()
    b214 = read_b214()
    points, maps = merge_blocks(g, shift_b214(b214, False),
                                shift_b214(b214, True))
    edges = exact_edges(points)
    need((len(points), len(edges)) == (343, 1782), "S343 census")
    need(point_hash(points)
         == "987b1b9a9bc1ca2c16d3cec5a4c77d5b3dc70d0d8bf7acb39155a039564dc269",
         "independent S343 lifted point stream")
    return points, edges, maps


def lens_point(first, second, sign):
    need(sign in (-1, 1), "lens sign")
    midpoint_x = f_div_exact(f_add(first[0], second[0]), 2)
    midpoint_y = f_div_exact(f_add(first[1], second[1]), 2)
    dx = f_sub(second[0], first[0])
    dy = f_sub(second[1], first[1])
    turn_x = f_div_exact(sqrt5_times(dy), 4)
    turn_y = f_div_exact(sqrt5_times(dx), 4)
    if sign == 1:
        return f_sub(midpoint_x, turn_x), f_add(midpoint_y, turn_y)
    return f_add(midpoint_x, turn_x), f_sub(midpoint_y, turn_y)


def build_geometry():
    source, source_edges, _ = build_source()
    centres = tuple(
        (first, second)
        for first, second in combinations(range(343), 2)
        if squared_distance(source[first], source[second]) == CENTRE_SQUARED
    )
    need(len(centres) == 54, "centre-pair count")
    centre_degrees = Counter(vertex for pair in centres for vertex in pair)
    need(len(centre_degrees) == 108 and set(centre_degrees.values()) == {1},
         "centre pairs are not a matching")

    positive = tuple(lens_point(source[first], source[second], 1)
                     for first, second in centres)
    negative = tuple(lens_point(source[first], source[second], -1)
                     for first, second in centres)
    new = positive + negative
    need(len(new) == len(set(new)) == 108, "new-point collision")
    need(not set(new) & set(source), "old/new collision")
    need(all(any(coefficient for axis in point for coefficient in axis[1])
             for point in new), "new point remains in source field")

    for offset, pair in enumerate(centres):
        for vertex in (positive[offset], negative[offset]):
            need(squared_distance(vertex, source[pair[0]]) == UNIT_SQUARED
                 and squared_distance(vertex, source[pair[1]]) == UNIT_SQUARED,
                 "defining lens incidence")

    points = source + new
    edges = exact_edges(points)
    old_edges = tuple(edge for edge in edges if edge[1] < 343)
    cross_edges = tuple(edge for edge in edges if edge[0] < 343 <= edge[1])
    new_edges = tuple(edge for edge in edges if edge[0] >= 343)
    need(old_edges == source_edges, "source is not induced")
    need((len(points), len(edges), len(cross_edges), len(new_edges))
         == (451, 2170, 216, 172), "complete geometry census")

    old_neighbours = {vertex: [] for vertex in range(343, 451)}
    for old, new_vertex in cross_edges:
        old_neighbours[new_vertex].append(old)
    for offset, pair in enumerate(centres):
        need(tuple(sorted(old_neighbours[343 + offset])) == pair,
             "positive old contacts")
        need(tuple(sorted(old_neighbours[397 + offset])) == pair,
             "negative old contacts")

    degrees = [0] * 451
    for first, second in edges:
        degrees[first] += 1
        degrees[second] += 1
    return {
        "points": points,
        "edges": edges,
        "source_edges": source_edges,
        "centres": centres,
        "cross_edges": cross_edges,
        "new_edges": new_edges,
        "old_neighbours": old_neighbours,
        "degrees": tuple(degrees),
    }


def proper(word, vertices, edges):
    return (isinstance(word, str) and len(word) == vertices
            and set(word) <= set("0123")
            and all(word[first] != word[second] for first, second in edges))


def adjacency(vertices, edges):
    result = [set() for _ in range(vertices)]
    for first, second in edges:
        result[first].add(second)
        result[second].add(first)
    return result


def components(vertices, edges, allowed=None):
    adj = adjacency(vertices, edges)
    remaining = set(range(vertices)) if allowed is None else set(allowed)
    result = []
    while remaining:
        start = min(remaining)
        remaining.remove(start)
        seen = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            new = adj[vertex] & remaining
            remaining -= new
            seen |= new
            stack.extend(new)
        result.append(tuple(sorted(seen)))
    return sorted(result, key=lambda row: (len(row), row))


def local_edges(vertices, edges):
    order = {vertex: index for index, vertex in enumerate(vertices)}
    return {(order[first], order[second])
            for first, second in edges if first in order and second in order}


def graph_isomorphic(size, first_edges, second_edges):
    first_adj = adjacency(size, first_edges)
    second_adj = adjacency(size, second_edges)
    first_invariant = [
        (len(first_adj[v]), tuple(sorted(len(first_adj[w]) for w in first_adj[v])))
        for v in range(size)
    ]
    second_invariant = [
        (len(second_adj[v]), tuple(sorted(len(second_adj[w]) for w in second_adj[v])))
        for v in range(size)
    ]
    if sorted(first_invariant) != sorted(second_invariant):
        return False
    candidates = [[w for w in range(size)
                   if second_invariant[w] == first_invariant[v]]
                  for v in range(size)]
    mapping = {}
    used = set()

    def search():
        if len(mapping) == size:
            return True
        vertex = min((v for v in range(size) if v not in mapping),
                     key=lambda v: (len([w for w in candidates[v] if w not in used]),
                                    -len(first_adj[v] & mapping.keys()), v))
        for image in candidates[vertex]:
            if image in used:
                continue
            if all((other in first_adj[vertex])
                   == (mapping[other] in second_adj[image]) for other in mapping):
                mapping[vertex] = image
                used.add(image)
                if search():
                    return True
                used.remove(image)
                del mapping[vertex]
        return False

    return search()


def k_colourable(vertices, edges, colours):
    adj = adjacency(vertices, edges)
    assigned = [-1] * vertices

    def search(remaining):
        if not remaining:
            return True
        vertex = max((v for v in range(vertices) if assigned[v] < 0),
                     key=lambda v: (len({assigned[w] for w in adj[v]
                                        if assigned[w] >= 0}),
                                    len(adj[v]), -v))
        forbidden = {assigned[w] for w in adj[vertex] if assigned[w] >= 0}
        for colour in range(colours):
            if colour in forbidden:
                continue
            assigned[vertex] = colour
            if search(remaining - 1):
                return True
        assigned[vertex] = -1
        return False

    return search(vertices)


def bipartite(vertices, edges):
    adj = adjacency(vertices, edges)
    colours = {}
    for start in range(vertices):
        if start in colours:
            continue
        colours[start] = 0
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour in adj[vertex]:
                if neighbour not in colours:
                    colours[neighbour] = 1 - colours[vertex]
                    stack.append(neighbour)
                elif colours[neighbour] == colours[vertex]:
                    return False
    return True


def layer_structure(geometry):
    new_components = components(451, geometry["new_edges"], range(343, 451))
    need([len(component) for component in new_components] == [6] * 8 + [15] * 4,
         "new-layer component orders")
    component_edges = [local_edges(component, geometry["new_edges"])
                       for component in new_components]
    need([len(edges) for edges in component_edges] == [7] * 8 + [29] * 4,
         "new-layer component edge counts")
    need(all(graph_isomorphic(6, component_edges[0], edges)
             for edges in component_edges[:8]), "six-vertex component types")
    need(all(graph_isomorphic(15, component_edges[8], edges)
             for edges in component_edges[8:]), "fifteen-vertex component types")
    need(all(bipartite(6, edges) for edges in component_edges[:8]),
         "six-vertex component is not bipartite")
    need(all(not k_colourable(15, edges, 3)
             and k_colourable(15, edges, 4)
             for edges in component_edges[8:]),
         "fifteen-vertex component chromatic number")

    spindle_sets = []
    for component, edges in zip(new_components[8:], component_edges[8:], strict=True):
        found = []
        for subset in combinations(range(15), 7):
            chosen = tuple(component[index] for index in subset)
            induced = local_edges(chosen, geometry["new_edges"])
            if len(induced) == 11 and graph_isomorphic(7, induced, MOSER_EDGES):
                found.append(chosen)
        need(len(found) == 1, "Moser spindle count in large component")
        spindle_sets.append(found[0])
    expected_spindles = [
        (343, 370, 401, 415, 426, 429, 435),
        (346, 362, 373, 374, 382, 423, 432),
        (347, 361, 372, 375, 381, 397, 424),
        (369, 378, 400, 416, 427, 428, 436),
    ]
    need(spindle_sets == expected_spindles, "Moser spindle labels")
    need(not k_colourable(7, MOSER_EDGES, 3)
         and k_colourable(7, MOSER_EDGES, 4), "Moser chromatic number")

    old_attachment_sets = [
        frozenset(old for vertex in component
                  for old in geometry["old_neighbours"][vertex])
        for component in new_components
    ]
    attachment_multiplicities = Counter(old_attachment_sets)
    need(len(attachment_multiplicities) == 6
         and set(attachment_multiplicities.values()) == {2},
         "paired attachment modules")
    need(sorted(map(len, attachment_multiplicities)) == [12] * 4 + [30] * 2,
         "attachment-module orders")

    return {
        "components": len(new_components),
        "component_order_histogram": {"6": 8, "15": 4},
        "component_edge_histogram": {"7": 8, "29": 4},
        "component_isomorphism_types": 2,
        "six_vertex_components_bipartite": True,
        "fifteen_vertex_components_four_chromatic": True,
        "disjoint_moser_spindles": [list(vertices) for vertices in spindle_sets],
        "paired_old_attachment_modules": 6,
        "attachment_order_histogram": {"12": 4, "30": 2},
        "layer_chromatic_number": 4,
    }


def cut_vertices_after_pair(adj, removed_first, removed_second):
    vertices = len(adj)
    discovery = [-1] * vertices
    low = [0] * vertices
    parent = [-1] * vertices
    cuts = set()
    clock = 0

    def visit(vertex):
        nonlocal clock
        discovery[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for neighbour in adj[vertex]:
            if neighbour == removed_first or neighbour == removed_second:
                continue
            if discovery[neighbour] < 0:
                parent[neighbour] = vertex
                children += 1
                visit(neighbour)
                low[vertex] = min(low[vertex], low[neighbour])
                if parent[vertex] < 0 and children > 1:
                    cuts.add(vertex)
                elif parent[vertex] >= 0 and low[neighbour] >= discovery[vertex]:
                    cuts.add(vertex)
            elif neighbour != parent[vertex]:
                low[vertex] = min(low[vertex], discovery[neighbour])

    for vertex in range(vertices):
        if vertex not in (removed_first, removed_second) and discovery[vertex] < 0:
            visit(vertex)
    return clock, cuts


def connectivity_census(vertices, edges):
    adj = adjacency(vertices, edges)

    def component_count(removed):
        remaining = set(range(vertices)) - set(removed)
        count = 0
        while remaining:
            start = remaining.pop()
            stack = [start]
            count += 1
            while stack:
                vertex = stack.pop()
                new = adj[vertex] & remaining
                remaining -= new
                stack.extend(new)
        return count

    visited, articulations = cut_vertices_after_pair(adj, -1, -1)
    need(visited == vertices and not articulations, "base connectivity")
    for first, second in combinations(range(vertices), 2):
        visited, cuts = cut_vertices_after_pair(adj, first, second)
        need(visited == vertices - 2, f"pair separator {(first, second)}")
        need(not cuts, f"triple separator above pair {(first, second)}")
    minimum_degree = min(map(len, adj))
    witness_vertex = min(vertex for vertex in range(vertices)
                         if len(adj[vertex]) == minimum_degree)
    witness = sorted(adj[witness_vertex])
    need(minimum_degree == len(witness) == 4, "connectivity upper bound")
    need(component_count(witness) > 1, "four-cut witness")
    return {
        "vertex_connectivity": 4,
        "articulation_vertices": 0,
        "pair_separator_candidates_checked": vertices * (vertices - 1) // 2,
        "pair_separators": 0,
        "triple_separator_candidates_covered":
            vertices * (vertices - 1) * (vertices - 2) // 6,
        "triple_separators": 0,
        "four_cut_witness_vertex": witness_vertex,
        "four_cut_witness": witness,
    }


def verify_relations(geometry):
    parent = json.loads((PARENT / "certificate.json").read_text())
    target = json.loads((TARGET / "certificate.json").read_text())
    need(parent.get("schema") == "golomb-opposed-b214-native-a159-stop-v1",
         "parent schema")
    patterns = parent["surviving_patterns"]
    need(len(patterns) == 66 and patterns == sorted(patterns),
         "parent relation patterns")
    need(set(parent["s343_words"]) == set(patterns), "parent positive keys")
    for pattern in patterns:
        word = parent["s343_words"][pattern]
        need(word[:10] == pattern and proper(word, 343, geometry["source_edges"]),
             f"parent positive word {pattern}")

    need(target.get("schema") == "opposed343-sqrt5-lens-stop-v1",
         "target schema")
    words = target.get("words")
    need(isinstance(words, dict) and sorted(words) == patterns,
         "target relation keys")
    digest = hashlib.sha256()
    for pattern in patterns:
        word = words[pattern]
        need(word[:10] == pattern and proper(word, 451, geometry["edges"]),
             f"target positive word {pattern}")
        digest.update((pattern + " " + word + "\n").encode("ascii"))
    need(target["point_sha256"] == point_hash(geometry["points"]),
         "target point hash")
    need(target["edge_sha256"] == edge_hash(geometry["edges"]),
         "target edge hash")
    need(target["centre_pair_sha256"] == pair_hash(geometry["centres"]),
         "target centre-pair hash")
    return {
        "source_patterns_imported_from_reviewed_parent": len(patterns),
        "positive_extension_words_checked": len(words),
        "final_patterns": len(words),
        "relation_reduction": 0,
        "witness_stream_sha256": digest.hexdigest(),
        "ordinary_chromatic_number": 4,
    }


def run():
    for path, digest in PINNED.items():
        need(sha256(path.read_bytes()) == digest, f"input hash: {path.name}")
    geometry = build_geometry()
    points = geometry["points"]
    edges = geometry["edges"]
    point_digest = point_hash(points)
    edge_digest = edge_hash(edges)
    centre_digest = pair_hash(geometry["centres"])
    need(point_digest
         == "08e1d57663aa5a899dc68a0c2aad6eee6259f57893fb1a4965a383e97b638a42",
         "point stream")
    need(edge_digest
         == "1227a8ac0e8357e7fd2587778b8585eb1e00a3eb6d0ec834984a4e1bb45f521a",
         "edge stream")
    need(centre_digest
         == "e54d4e57082e4c7912296db675033fb1352449552f4d8f691fac56ca8b7df0e4",
         "centre stream")

    layer = layer_structure(geometry)
    relation = verify_relations(geometry)
    connectivity = connectivity_census(451, edges)
    new_degrees = Counter(geometry["degrees"][343:])

    return {
        "status": "ACCEPTED_INDEPENDENT_SQRT5_LENS_STOP_REVIEW",
        "target_commit": "8a98d34290f4ba578a28ae69aa1edb8fe7399d85",
        "coordinate_model": "Q(sqrt3,sqrt11)_plus_sqrt5_quadratic_tower",
        "coordinate_scale": SCALE,
        "source_points": 343,
        "source_edges": len(geometry["source_edges"]),
        "centre_distance_squared": "16/9",
        "centre_pairs": len(geometry["centres"]),
        "centre_pairs_form_matching": True,
        "distinct_centre_vertices": 108,
        "new_points": 108,
        "outside_source_field_points": 108,
        "complete_points": len(points),
        "complete_edges": len(edges),
        "all_pairs": len(points) * (len(points) - 1) // 2,
        "old_new_edges": len(geometry["cross_edges"]),
        "new_new_edges": len(geometry["new_edges"]),
        "new_point_degree_histogram": {
            str(degree): count for degree, count in sorted(new_degrees.items())
        },
        "point_sha256": point_digest,
        "edge_sha256": edge_digest,
        "centre_pair_sha256": centre_digest,
        "relation": relation,
        "new_layer_structure": layer,
        "connectivity": connectivity,
        "record_candidate": False,
        "global_exclusion": False,
        "tested_finishing_class": "both_lens_points_for_all_S343_pairs_at_squared_distance_16/9",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    report = run()
    if args.check_expected:
        need(report == json.loads((HERE / "EXPECTED.json").read_text()),
             "expected output")
    print(json.dumps(report, indent=2, sort_keys=True))
