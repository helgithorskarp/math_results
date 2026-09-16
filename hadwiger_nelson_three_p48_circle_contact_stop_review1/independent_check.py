#!/usr/bin/env python3
"""Independent rational-Gram review of the frozen triple-P48 support."""

import argparse
import hashlib
import itertools
import json
import math
from fractions import Fraction as F
from pathlib import Path


HERE = Path(__file__).resolve().parent
TARGET_NAME = "hadwiger_nelson_three_p48_circle_contact_stop"


class ReviewFailure(RuntimeError):
    pass


def need(condition, message):
    if not condition:
        raise ReviewFailure(message)


# The real biquadratic field Q(sqrt(33),sqrt(105)) in the basis
# 1, sqrt(33), sqrt(105), sqrt(385), with sqrt(33)sqrt(105)=3sqrt(385).
def bf(*values):
    values = values or (0,)
    return tuple(F(values[index] if index < len(values) else 0) for index in range(4))


def badd(left, right):
    return tuple(x + y for x, y in zip(left, right))


def bscale(value, scalar):
    scalar = F(scalar)
    return tuple(scalar * x for x in value)


def bmul(left, right):
    # Products of basis elements, encoded as (rational multiplier, basis index).
    table = (
        ((1, 0), (1, 1), (1, 2), (1, 3)),
        ((1, 1), (33, 0), (3, 3), (11, 2)),
        ((1, 2), (3, 3), (105, 0), (35, 1)),
        ((1, 3), (11, 2), (35, 1), (385, 0)),
    )
    result = [F(0) for _ in range(4)]
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            multiplier, target = table[i][j]
            result[target] += x * y * multiplier
    return tuple(result)


def gram_matrix():
    """Gram matrix for 1, omega, r, r*omega, v, v*omega."""
    one = bf(1)
    root33 = bf(0, 1)
    # For a unit q=x+i*y, store x and t=sqrt(3)*y.  The cross Gram block
    # between (u,u*omega) and (u*q,u*q*omega) is determined by x,t.
    r_x = bf(F(5, 6))
    r_t = bscale(root33, F(1, 6))
    v_x = bscale(bf(-35, -7, 1, -5), F(1, 168))
    v_t = bscale(bf(-21, 35, -5, -3), F(1, 168))
    rv_x = badd(bscale(v_x, F(5, 6)), bscale(bmul(root33, v_t), F(1, 18)))
    rv_t = badd(bscale(v_t, F(5, 6)), bscale(bmul(root33, v_x), F(-1, 6)))

    def unit_norm(x, t):
        return badd(bmul(x, x), bscale(bmul(t, t), F(1, 3)))

    need(unit_norm(r_x, r_t) == one, "r Gram data are not unit")
    need(unit_norm(v_x, v_t) == one, "v Gram data are not unit")
    need(unit_norm(rv_x, rv_t) == one, "relative rotation Gram data are not unit")

    zero = bf()
    matrix = [[zero for _ in range(6)] for _ in range(6)]
    for base in (0, 2, 4):
        matrix[base][base] = one
        matrix[base + 1][base + 1] = one
        matrix[base][base + 1] = matrix[base + 1][base] = bf(F(1, 2))

    def block(left, right, x, t):
        values = ((x, bscale(badd(x, bscale(t, -1)), F(1, 2))),
                  (bscale(badd(x, t), F(1, 2)), x))
        for a in range(2):
            for b in range(2):
                matrix[left + a][right + b] = values[a][b]
                matrix[right + b][left + a] = values[a][b]

    block(0, 2, r_x, r_t)
    block(0, 4, v_x, v_t)
    block(2, 4, rv_x, rv_t)
    denominators = [entry.denominator for row in matrix for value in row for entry in value]
    scale = math.lcm(*denominators)
    integer_matrix = [
        [tuple(int(scale * entry) for entry in value) for value in row]
        for row in matrix
    ]
    return scale, integer_matrix


def quadratic(vector, matrix):
    result = [0, 0, 0, 0]
    for i, left in enumerate(vector):
        if not left:
            continue
        for j in range(i, len(vector)):
            right = vector[j]
            if not right:
                continue
            multiplier = left * right * (1 if i == j else 2)
            for k, coefficient in enumerate(matrix[i][j]):
                result[k] += multiplier * coefficient
    return tuple(result)


def vector_sub(left, right):
    return tuple(x - y for x, y in zip(left, right))


def addresses():
    result = [
        (a, b)
        for a in range(-8, 9)
        for b in range(-8, 9)
        if a * a + a * b + b * b <= 48
    ]
    need(len(result) == 169, "P48 address census")
    return result


def raw_support():
    result = []
    for layer in range(3):
        for a, b in addresses():
            if layer == 0:
                vector = (a, b, 0, 0, 0, 0)
            elif layer == 1:
                vector = (0, 0, a, b, 0, 0)
            else:
                vector = (2, 1, 0, 0, a, b)
            result.append({"layer": layer, "address": (a, b), "vector": vector})
    return result


class UnionFind:
    def __init__(self, order):
        self.parent = list(range(order))

    def find(self, item):
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left, right):
        left, right = self.find(left), self.find(right)
        if left != right:
            self.parent[max(left, right)] = min(left, right)


def reconstruct():
    scale, gram = gram_matrix()
    raw = raw_support()
    zero = (0, 0, 0, 0)
    one = (scale, 0, 0, 0)
    union = UnionFind(len(raw))
    raw_collisions = []
    for left, right in itertools.combinations(range(len(raw)), 2):
        difference = vector_sub(raw[left]["vector"], raw[right]["vector"])
        if quadratic(difference, gram) == zero:
            union.union(left, right)
            raw_collisions.append((left, right))
    roots = sorted({union.find(index) for index in range(len(raw))})
    need(len(roots) == 505, "physical support order")
    root_to_vertex = {root: index for index, root in enumerate(roots)}
    raw_vertex = [root_to_vertex[union.find(index)] for index in range(len(raw))]
    roles = [[] for _ in roots]
    for item, vertex in zip(raw, raw_vertex):
        roles[vertex].append((item["layer"], *item["address"]))
    representatives = [raw[root]["vector"] for root in roots]
    edges = []
    for left, right in itertools.combinations(range(len(representatives)), 2):
        difference = vector_sub(representatives[left], representatives[right])
        if quadratic(difference, gram) == one:
            edges.append((left, right))
    edge_set = set(edges)
    layer_sets = []
    for layer in range(3):
        layer_sets.append({raw_vertex[index] for index, item in enumerate(raw) if item["layer"] == layer})
    internal_sets = [
        {edge for edge in edge_set if edge[0] in vertices and edge[1] in vertices}
        for vertices in layer_sets
    ]
    inherited = set().union(*internal_sets)
    extra = sorted(edge_set - inherited)
    overlap = [
        [left, right, len(layer_sets[left] & layer_sets[right])]
        for left, right in itertools.combinations(range(3), 2)
    ]
    cross = {}
    for left, right in itertools.combinations(range(3), 2):
        cross[f"{left}-{right}"] = sum(
            (a in layer_sets[left] and b in layer_sets[right])
            or (b in layer_sets[left] and a in layer_sets[right])
            for a, b in extra
        )
    role_lookup = {
        role: vertex
        for vertex, entries in enumerate(roles)
        for role in entries
    }
    moser_roles = (
        (0, 0, 0), (0, 1, 0), (0, 0, 1), (0, 1, 1),
        (1, 1, 0), (1, 0, 1), (1, 1, 1),
    )
    moser = [role_lookup[role] for role in moser_roles]
    moser_edges = [
        (i, j)
        for i, j in itertools.combinations(range(7), 2)
        if tuple(sorted((moser[i], moser[j]))) in edge_set
    ]
    need(len(moser_edges) == 11, "embedded Moser edge census")
    three_words = sum(
        all(word[i] != word[j] for i, j in moser_edges)
        for word in itertools.product(range(3), repeat=7)
    )
    need(three_words == 0, "embedded Moser spindle is three-colourable")
    point_stream = "".join(
        "|".join(f"{layer}:{a},{b}" for layer, a, b in entries) + "\n"
        for entries in roles
    ).encode()
    edge_stream = "".join(f"{left},{right}\n" for left, right in edges).encode()
    return {
        "scale": scale,
        "gram": gram,
        "raw": raw,
        "raw_vertex": raw_vertex,
        "roles": roles,
        "representatives": representatives,
        "edges": edges,
        "edge_set": edge_set,
        "layer_sets": layer_sets,
        "internal_sets": internal_sets,
        "extra": extra,
        "overlap": overlap,
        "cross": cross,
        "moser": moser,
        "moser_edges": moser_edges,
        "raw_collisions": raw_collisions,
        "point_role_sha256": hashlib.sha256(point_stream).hexdigest(),
        "edge_sha256": hashlib.sha256(edge_stream).hexdigest(),
    }


def adjacency(order, edges):
    result = [set() for _ in range(order)]
    for left, right in edges:
        result[left].add(right)
        result[right].add(left)
    return result


def reached_vertices(order, edges, deleted_vertices=(), deleted_edges=()):
    graph = adjacency(order, set(edges) - {tuple(sorted(edge)) for edge in deleted_edges})
    deleted = set(deleted_vertices)
    start = next(vertex for vertex in range(order) if vertex not in deleted)
    seen = {start}
    stack = [start]
    while stack:
        vertex = stack.pop()
        for other in graph[vertex]:
            if other not in deleted and other not in seen:
                seen.add(other)
                stack.append(other)
    return seen


def fresh_four_colouring(order, edges):
    """Deterministic DSATUR search; no submitted colour word is read."""
    graph = adjacency(order, edges)
    colours = [-1] * order

    def choose():
        candidates = (vertex for vertex, colour in enumerate(colours) if colour < 0)
        return max(candidates, key=lambda vertex: (
            len({colours[n] for n in graph[vertex] if colours[n] >= 0}),
            len(graph[vertex]),
            -vertex,
        ))

    nodes = 0

    def search(coloured, maximum):
        nonlocal nodes
        nodes += 1
        if coloured == order:
            return True
        vertex = choose()
        forbidden = {colours[n] for n in graph[vertex] if colours[n] >= 0}
        existing = list(range(maximum + 1))
        available = [colour for colour in existing if colour not in forbidden]
        if maximum < 3 and maximum + 1 not in forbidden:
            available.append(maximum + 1)
        for colour in available:
            colours[vertex] = colour
            if search(coloured + 1, max(maximum, colour)):
                return True
        colours[vertex] = -1
        return False

    colours[0] = 0
    need(search(1, 0), "fresh four-colour search failed")
    need(max(colours) == 3, "fresh word unexpectedly uses fewer than four colours")
    need(all(colours[left] != colours[right] for left, right in edges), "fresh word is improper")
    word = "".join(map(str, colours))
    return word, nodes


def validate_word(word, order, edges):
    need(isinstance(word, str) and len(word) == order, "review word length")
    need(set(word) <= set("0123"), "review word alphabet")
    need(all(word[left] != word[right] for left, right in edges), "review word is improper")


def connectivity(order, edges):
    graph = adjacency(order, edges)
    discovery = [-1] * order
    low = [0] * order
    parent = [-1] * order
    articulations = set()
    bridges = []
    time = 0

    def visit(vertex):
        nonlocal time
        discovery[vertex] = low[vertex] = time
        time += 1
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
                    bridges.append(tuple(sorted((vertex, other))))
            elif other != parent[vertex]:
                low[vertex] = min(low[vertex], discovery[other])

    visit(0)
    need(all(value >= 0 for value in discovery), "support graph is disconnected")
    degrees = [len(neighbours) for neighbours in graph]
    return sorted(articulations), sorted(set(bridges)), degrees


def role_edge(graph, edge):
    return [
        [list(role) for role in graph["roles"][vertex]]
        for vertex in edge
    ]


def review_result():
    graph = reconstruct()
    order = len(graph["roles"])
    word, nodes = fresh_four_colouring(order, graph["edges"])
    certificate = json.loads((HERE / "certificate.json").read_text())
    need(set(certificate) == {"label_order", "four_word"}, "review certificate keys")
    need(certificate["label_order"] == "canonical raw-role classes", "review label order")
    validate_word(certificate["four_word"], order, graph["edges"])
    need(certificate["four_word"] == word, "stored and freshly found words differ")
    articulations, bridges, degrees = connectivity(order, graph["edges"])
    need(not articulations, "unexpected articulation")
    need(not bridges, "unexpected bridge")
    need(min(degrees) == 2, "minimum degree mismatch")
    # A connected graph with no cut vertex/bridge is at least 2-connected in
    # both senses.  A degree-two vertex supplies matching upper bounds.
    degree_two = [vertex for vertex, degree in enumerate(degrees) if degree == 2]
    need(degree_two, "missing connectivity upper-bound witness")
    graph_adjacency = adjacency(order, graph["edges"])
    witness_vertex = degree_two[0]
    witness_neighbours = sorted(graph_adjacency[witness_vertex])
    witness_edges = [tuple(sorted((witness_vertex, other))) for other in witness_neighbours]
    need(len(reached_vertices(order, graph["edges"], witness_neighbours)) < order - 2,
         "degree-two neighbours do not witness a vertex cut")
    need(len(reached_vertices(order, graph["edges"], deleted_edges=witness_edges)) < order,
         "degree-two incident edges do not witness an edge cut")

    total = [sum(vector[index] for vector in graph["representatives"]) for index in range(6)]
    expected_total = (336, 168, 0, 0, 0, 0)  # 168*A in the six-vector coordinates.
    difference = vector_sub(total, expected_total)
    need(quadratic(difference, graph["gram"]) == (0, 0, 0, 0), "centroid identity")
    centroid_hits = []
    for vertex, point in enumerate(graph["representatives"]):
        scaled_point = tuple(order * entry for entry in point)
        if quadratic(vector_sub(scaled_point, total), graph["gram"]) == (0, 0, 0, 0):
            centroid_hits.append(vertex)
    need(not centroid_hits, "odd support contains its centroid")

    return {
        "status": "ACCEPT_AND_STRENGTHEN_FIXED_SUPPORT",
        "vertices": order,
        "edges": len(graph["edges"]),
        "all_physical_pairs_checked": order * (order - 1) // 2,
        "raw_addresses": len(graph["raw"]),
        "raw_collision_pairs": len(graph["raw_collisions"]),
        "overlaps": graph["overlap"],
        "internal_edges": [len(edges) for edges in graph["internal_sets"]],
        "extra_edges": len(graph["extra"]),
        "extra_edges_by_pair": graph["cross"],
        "complete_extra_edges_by_roles": [role_edge(graph, edge) for edge in graph["extra"]],
        "point_role_sha256": graph["point_role_sha256"],
        "edge_sha256": graph["edge_sha256"],
        "gram_denominator": graph["scale"],
        "moser_vertices": graph["moser"],
        "moser_edges": len(graph["moser_edges"]),
        "moser_three_colour_assignments_exhausted": 3 ** 7,
        "fresh_four_word_sha256": hashlib.sha256(word.encode()).hexdigest(),
        "fresh_four_search_nodes": nodes,
        "connected": True,
        "articulation_vertices": articulations,
        "bridges": bridges,
        "minimum_degree": min(degrees),
        "degree_two_vertices": degree_two,
        "vertex_connectivity": 2,
        "edge_connectivity": 2,
        "connectivity_witness": {
            "degree_two_vertex": witness_vertex,
            "neighbours": witness_neighbours,
            "incident_edges": [list(edge) for edge in witness_edges],
        },
        "centrally_symmetric": False,
        "chromatic_number": 4,
        "record_candidate": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-expected", action="store_true")
    arguments = parser.parse_args()
    result = review_result()
    if arguments.check_expected:
        expected = json.loads((HERE / "EXPECTED.json").read_text())
        need(result == expected, "review result differs from EXPECTED.json")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
