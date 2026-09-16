#!/usr/bin/env python3
"""Exact verifier for one 15/45-degree interaction of two T721 fragments."""
import argparse
import hashlib
import json
import math
import sys
from collections import Counter, deque
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_t721_weighted_cover"
sys.path.insert(0, str(SOURCE))
import native  # noqa: E402


def need(test, message):
    if not test:
        raise ValueError(message)


def basis(index, value):
    out = [F(0)] * 8
    out[index] = F(value)
    return tuple(out)


def rotate(point, cosine, sine):
    x, y = point[:8], point[8:]
    return native.add(native.mul(cosine, x), native.neg(native.mul(sine, y))) + native.add(
        native.mul(sine, x), native.mul(cosine, y)
    )


def integer_points(points):
    scale = math.lcm(*(x.denominator for point in points for x in point))
    return scale, [tuple(int(x * scale) for x in point) for point in points]


def hash_points(points):
    return hashlib.sha256("".join(" ".join(map(str, p)) + "\n" for p in points).encode()).hexdigest()


def hash_edges(edges):
    return hashlib.sha256("".join(f"{u} {v}\n" for u, v in edges).encode()).hexdigest()


def graph_structure(n, edges):
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    components = []
    seen = set()
    for start in range(n):
        if start in seen:
            continue
        stack = [start]
        seen.add(start)
        component = []
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adjacency[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        components.append(component)

    work = [set(row) for row in adjacency]
    removed = {u for u in range(n) if len(work[u]) < 4}
    queue = deque(removed)
    while queue:
        u = queue.popleft()
        for v in tuple(work[u]):
            work[v].discard(u)
            if v not in removed and len(work[v]) < 4:
                removed.add(v)
                queue.append(v)
    core4 = set(range(n)) - removed

    timer = 0
    discovery = [-1] * n
    low = [0] * n
    parent = [-1] * n
    articulations = set()
    bridges = []

    def dfs(u):
        nonlocal timer
        discovery[u] = low[u] = timer
        timer += 1
        children = 0
        for v in adjacency[u]:
            if discovery[v] < 0:
                parent[v] = u
                children += 1
                dfs(v)
                low[u] = min(low[u], low[v])
                if parent[u] < 0 and children > 1:
                    articulations.add(u)
                if parent[u] >= 0 and low[v] >= discovery[u]:
                    articulations.add(u)
                if low[v] > discovery[u]:
                    bridges.append(tuple(sorted((u, v))))
            elif v != parent[u]:
                low[u] = min(low[u], discovery[v])

    for u in range(n):
        if discovery[u] < 0:
            dfs(u)
    return adjacency, sorted(map(len, components), reverse=True), core4, articulations, sorted(bridges)


def check_word(word, edges, colours):
    need(len(word) > 0 and all(c in colours for c in word), "word alphabet")
    need(all(word[u] != word[v] for u, v in edges), "monochromatic edge")


def three_colour_search(vertices, edges):
    """Definition-level exhaustive search, with only colour-permutation symmetry removed."""
    vertices = sorted(vertices)
    local = {v: i for i, v in enumerate(vertices)}
    adjacency = [set() for _ in vertices]
    for u, v in edges:
        if u in local and v in local:
            a, b = local[u], local[v]
            adjacency[a].add(b)
            adjacency[b].add(a)
    triangles = []
    for a in range(len(vertices)):
        for b in adjacency[a]:
            if a < b:
                for c in adjacency[a] & adjacency[b]:
                    if b < c:
                        triangles.append((a, b, c))
    need(triangles, "nonthree witness has no triangle")
    triangle = min(triangles, key=lambda row: tuple(vertices[x] for x in row))
    colour = [-1] * len(vertices)
    for c, u in enumerate(triangle):
        colour[u] = c
    nodes = 0

    def visit():
        nonlocal nodes
        nodes += 1
        uncoloured = [u for u, c in enumerate(colour) if c < 0]
        if not uncoloured:
            return True
        u = max(
            uncoloured,
            key=lambda x: (len({colour[v] for v in adjacency[x] if colour[v] >= 0}), len(adjacency[x]), -vertices[x]),
        )
        forbidden = {colour[v] for v in adjacency[u] if colour[v] >= 0}
        for c in range(3):
            if c not in forbidden:
                colour[u] = c
                if visit():
                    return True
                colour[u] = -1
        return False

    sat = visit()
    word = None if not sat else "".join(str(c) for c in colour)
    return word, nodes, [vertices[u] for u in triangle]


def verify(input_path, word_path=None, fragment_path=None):
    fragment_path = fragment_path or HERE / "fragment.json"
    word_path = word_path or HERE / "four_word.txt"
    spec = json.loads(Path(fragment_path).read_text())
    need(spec.get("version") == "t721-30deg-fragment-v1", "fragment version")
    raw = Path(input_path).read_bytes()
    need(len(raw) == 40529, "input bytes")
    need(hashlib.sha256(raw).hexdigest() == "a63fa371d7cf42faa8a3b26d56df81b0c25c1f149d6791dd25c7c356abe1b7c6", "input hash")

    half = native.half(input_path)
    source_scale, source_points = integer_points(half)
    source_edges, source_survivors = native.edges(source_points, source_scale)
    need(len(half) == spec["source_vertices"] == 721 and len(source_edges) == 3948, "source graph")
    adjacency = [set() for _ in half]
    for u, v in source_edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    certificate = json.loads((SOURCE / "certificate.json").read_text())
    mandatory = {0, 1} | {row["deleted"] for row in certificate["steps"]}
    need(len(mandatory) == spec["mandatory_vertices"] == 238, "mandatory label count")
    ranking = sorted(
        (-len(adjacency[v] & mandatory), -len(adjacency[v]), v)
        for v in range(len(half))
        if v not in mandatory
    )
    extras = [v for _, _, v in ranking[: spec["enrichment_vertices"]]]
    need(extras == spec["extra_labels"], "enrichment ranking")
    labels = sorted(mandatory | set(extras))
    need(len(labels) == spec["fragment_vertices"] == 254 < len(half), "proper fragment")
    label_index = {v: i for i, v in enumerate(labels)}
    fragment_edges = [(u, v) for u, v in source_edges if u in label_index and v in label_index]
    need(len(fragment_edges) == 670, "fragment edge count")

    cosine15 = native.add(basis(3, F(1, 4)), basis(1, F(1, 4)))
    sine15 = native.add(basis(3, F(1, 4)), basis(1, F(-1, 4)))
    cosine45 = sine45 = basis(1, F(1, 2))
    frame_a = [rotate(half[v], cosine15, sine15) for v in labels]
    frame_b = [rotate(half[v], cosine45, sine45) for v in labels]
    need(len(set(frame_a)) == len(set(frame_b)) == 254, "frame collision")
    native_spindle = set(half) | {native.transform(point) for point in half}
    need(not set(frame_a) <= native_spindle and not set(frame_b) <= native_spindle, "native-host reduction")
    # Rational (-1,0) is fixed by every pointwise Galois automorphism but moves in both frames.
    terminal_position = label_index[0]
    need(frame_a[terminal_position] != half[0] and frame_b[terminal_position] != half[0], "pointwise-Galois reduction")

    full = sorted(set(frame_a) | set(frame_b))
    ids = {point: i for i, point in enumerate(full)}
    map_a = [ids[point] for point in frame_a]
    map_b = [ids[point] for point in frame_b]
    set_a, set_b = set(map_a), set(map_b)
    shared = set_a & set_b
    private_a, private_b = set_a - set_b, set_b - set_a
    scale, points = integer_points(full)
    edges, survivors = native.edges(points, scale)
    edge_set = set(edges)
    internal_a = {
        tuple(sorted((map_a[label_index[u]], map_a[label_index[v]]))) for u, v in fragment_edges
    }
    internal_b = {
        tuple(sorted((map_b[label_index[u]], map_b[label_index[v]]))) for u, v in fragment_edges
    }
    extra_edges = edge_set - internal_a - internal_b
    private_edges = {
        (u, v)
        for u, v in edge_set
        if (u in private_a and v in private_b) or (u in private_b and v in private_a)
    }
    need(extra_edges == private_edges, "extra/private cross-edge classification")

    graph, components, core4, articulations, bridges = graph_structure(len(full), edges)
    word = Path(word_path).read_text().strip()
    need(len(word) == len(full), "four-word length")
    check_word(word, edges, "0123")

    witness = spec["nonthree_vertices"]
    need(len(witness) == len(set(witness)) == 26 and all(0 <= v < len(full) for v in witness), "nonthree labels")
    witness_edges = [(u, v) for u, v in edges if u in witness and v in witness]
    witness_private = [(u, v) for u, v in private_edges if u in witness and v in witness]
    need(len(witness_edges) == 50 and len(witness_private) == 7, "nonthree witness edges")
    witness_word, search_nodes, fixed_triangle = three_colour_search(witness, witness_edges)
    need(witness_word is None, "nonthree witness is three-colourable")
    deletion_nodes = 0
    for deleted in witness:
        deletion_word, nodes, _ = three_colour_search(set(witness) - {deleted}, witness_edges)
        need(deletion_word is not None, "nonthree witness is not vertex-critical")
        deletion_nodes += nodes

    result = {
        "verified": True,
        "record_candidate": False,
        "chromatic_number": 4,
        "vertices": len(full),
        "edges": len(edges),
        "pair_checks": len(full) * (len(full) - 1) // 2,
        "scale": scale,
        "basis": list(native.D),
        "source_vertices": len(half),
        "source_edges": len(source_edges),
        "source_modular_survivors": source_survivors,
        "fragment_vertices_each": len(labels),
        "fragment_edges_each": len(fragment_edges),
        "formal_vertices": 2 * len(labels),
        "collisions": len(shared),
        "private_vertices_a": len(private_a),
        "private_vertices_b": len(private_b),
        "private_cross_edges": len(private_edges),
        "extra_edges_beyond_fragment_edges": len(extra_edges),
        "components": components,
        "articulations": len(articulations),
        "bridges": len(bridges),
        "four_core_vertices": len(core4),
        "four_core_private_a": len(core4 & private_a),
        "four_core_private_b": len(core4 & private_b),
        "four_core_shared": len(core4 & shared),
        "degree_counts": {str(k): v for k, v in sorted(Counter(map(len, graph)).items())},
        "nonthree_witness_vertices": len(witness),
        "nonthree_witness_edges": len(witness_edges),
        "nonthree_witness_private_cross_edges": len(witness_private),
        "nonthree_witness_membership": {
            "private_a": len(set(witness) & private_a),
            "private_b": len(set(witness) & private_b),
            "shared": len(set(witness) & shared),
        },
        "nonthree_fixed_triangle": fixed_triangle,
        "nonthree_search_nodes": search_nodes,
        "nonthree_deletion_search_nodes": deletion_nodes,
        "nonthree_vertex_critical": True,
        "coordinate_sha256": hash_points(points),
        "edge_sha256": hash_edges(edges),
        "four_word_sha256": hashlib.sha256((word + "\n").encode()).hexdigest(),
        "exact_all_pairs": True,
        "native_scope_excluded": True,
        "pointwise_galois_scope_excluded": True,
    }
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--check-expected", action="store_true")
    args = parser.parse_args()
    output = verify(args.input)
    if args.check_expected:
        need(output == json.loads((HERE / "expected.json").read_text()), "expected mismatch")
    print(json.dumps(output, indent=2, sort_keys=True))
