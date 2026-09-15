#!/usr/bin/env python3
"""Independent review of the frozen H516-surgery to H632 gate.

This checker imports no executable code from the target or its parents.  It
reconstructs both exact graphs from hash-pinned data, derives the labelled
surgery, and checks a six-vertex odd-wheel certificate which proves the
stronger whole-plane obstruction.
"""

from __future__ import annotations

from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PINS = json.loads((HERE / "SOURCE_PINS.json").read_text())
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)
UNIT_NORM = (96 * 96, 0, 0, 0, 0, 0, 0, 0)


def require(condition: bool, message: object) -> None:
    if not condition:
        raise ValueError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stream_hash(rows) -> str:
    encoded = "".join(",".join(map(str, row)) + "\n" for row in rows).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def pinned_json(relative: str):
    path = REPO / relative
    require(sha256_file(path) == PINS["input_files"][relative], ("input hash", relative))
    return json.loads(path.read_text())


def scaled_axis(axis) -> tuple[int, ...]:
    require(isinstance(axis, list) and len(axis) == 8, "coordinate axis shape")
    answer = []
    for value in axis:
        scaled = 96 * Fraction(value)
        require(scaled.denominator == 1, ("coordinate denominator", value))
        answer.append(int(scaled))
    return tuple(answer)


def scaled_point(row) -> tuple[tuple[int, ...], tuple[int, ...]]:
    require(isinstance(row, list) and len(row) == 2, "coordinate point shape")
    return scaled_axis(row[0]), scaled_axis(row[1])


def source_point(row) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """SOURCE.json already stores integer numerators over 96."""
    require(isinstance(row, list) and len(row) == 2, "source point shape")
    require(all(isinstance(axis, list) and len(axis) == 8 for axis in row), "source axis shape")
    require(all(isinstance(value, int) for axis in row for value in axis), "source numerator")
    return tuple(row[0]), tuple(row[1])


def norm_coefficients(p, q) -> tuple[int, ...]:
    """Squared norm in the three-generator multiquadratic basis.

    Basis index i is the subset mask of (sqrt(3),sqrt(5),sqrt(11)).
    The product of indices i,j has output index i xor j and rational factor
    RADICANDS[i & j].  Ordered convolution automatically includes both cross
    terms and differs from both target implementations.
    """
    output = [0] * 8
    for p_axis, q_axis in zip(p, q):
        delta = [a - b for a, b in zip(p_axis, q_axis)]
        for i, a in enumerate(delta):
            if not a:
                continue
            for j, b in enumerate(delta):
                if b:
                    output[i ^ j] += a * b * RADICANDS[i & j]
    return tuple(output)


def exact_graph(labels, points):
    require(len(labels) == len(points), "label/point count")
    require(len(labels) == len(set(labels)), "distinct labels")
    require(len(points) == len(set(points)), "distinct exact points")
    edges = []
    pair_count = 0
    for i, u in enumerate(labels):
        for j in range(i + 1, len(labels)):
            pair_count += 1
            if norm_coefficients(points[i], points[j]) == UNIT_NORM:
                edges.append((u, labels[j]))
    return sorted(edges), pair_count


def adjacency(vertices, edges):
    result = {v: set() for v in vertices}
    for u, v in edges:
        require(u in result and v in result and u != v, ("edge endpoint", u, v))
        require(v not in result[u], ("duplicate edge", u, v))
        result[u].add(v)
        result[v].add(u)
    return result


def triangles(vertices, adjacent):
    answer = []
    for u in vertices:
        for v in sorted(x for x in adjacent[u] if u < x):
            for w in sorted(x for x in adjacent[u] & adjacent[v] if v < x):
                answer.append((u, v, w))
    return answer


def source_and_surgery():
    source = pinned_json("hadwiger_nelson_h516_degree4_surgeries/SOURCE.json")
    labels = source["labels"]
    require(labels == sorted(labels) and len(labels) == 516, "source labels")
    points = [source_point(row) for row in source["coordinates"]]
    exact_edges, pair_count = exact_graph(labels, points)
    declared_edges = [tuple(edge) for edge in source["edges"]]
    require(declared_edges == sorted(set(declared_edges)), "source edge encoding")
    require(exact_edges == declared_edges, "source is not its complete strict unit graph")
    original = adjacency(labels, declared_edges)

    centres = sorted(v for v in labels if len(original[v]) == 4)
    require(centres == source["degree4"], "degree-four list")
    allowed = {
        centre: [
            pair
            for pair in itertools.combinations(sorted(original[centre]), 2)
            if pair[1] not in original[pair[0]]
        ]
        for centre in centres
    }
    closed_stars = {v: original[v] | {v} for v in centres}
    quadruples = [
        q
        for q in itertools.combinations(centres, 4)
        if all(
            not (closed_stars[u] & closed_stars[v])
            for u, v in itertools.combinations(q, 2)
        )
    ]
    family_count = sum(
        len(allowed[q[0]])
        * len(allowed[q[1]])
        * len(allowed[q[2]])
        * len(allowed[q[3]])
        for q in quadruples
    )
    operations = [(centre, *allowed[centre][0]) for centre in quadruples[0]]
    require(operations == [tuple(row) for row in PINS["selected_operations"]], "selected surgery")

    # Closed stars are disjoint, but use a genuine disjoint-set quotient rather
    # than relying on that fact when constructing the selected graph.
    parent = {v: v for v in labels}

    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    def union(u, v):
        a, b = find(u), find(v)
        parent[max(a, b)] = min(a, b)

    deleted = set()
    for centre, u, v in operations:
        require(len(original[centre]) == 4, ("centre degree", centre))
        require(u in original[centre] and v in original[centre], ("neighbour pair", centre))
        require(v not in original[u], ("pair must be nonadjacent", centre, u, v))
        deleted.add(centre)
        union(u, v)
    require(all(
        not (closed_stars[u] & closed_stars[v])
        for u, v in itertools.combinations((row[0] for row in operations), 2)
    ), "selected closed-star disjointness")

    vertices = sorted({find(v) for v in labels if v not in deleted})
    edge_set = set()
    for u, v in declared_edges:
        if u in deleted or v in deleted:
            continue
        a, b = find(u), find(v)
        require(a != b, ("quotient loop", u, v))
        edge_set.add(tuple(sorted((a, b))))
    edges = sorted(edge_set)
    final_adj = adjacency(vertices, edges)
    source_triangles = triangles(vertices, final_adj)
    anchor = min(
        source_triangles,
        key=lambda row: (-sum(len(final_adj[v]) for v in row), row),
    )
    return {
        "pair_count": pair_count,
        "strict_edges": len(declared_edges),
        "strict_edge_sha256": stream_hash(declared_edges),
        "centres": centres,
        "quadruples": len(quadruples),
        "family_count": family_count,
        "operations": operations,
        "vertices": vertices,
        "edges": edges,
        "adjacency": final_adj,
        "triangles": source_triangles,
        "anchor": anchor,
    }


def target_graph():
    old = pinned_json("hadwiger_nelson_parts509_heule_union_minimum/certificate_H510.json")
    fresh = pinned_json("hadwiger_nelson_heule510_completion_frontier/fresh_candidates.json")
    old_labels = [
        v
        for v in sorted(map(int, old["coordinates"]))
        if "510" in old["provenance"][v]
    ]
    require(len(old_labels) == 510 and len(fresh) == 122, "H632 input partition")
    points = [scaled_point(old["coordinates"][str(v)]) for v in old_labels]
    points.extend(scaled_point(row["coordinates"]) for row in fresh)
    labels = list(range(632))
    edges, pair_count = exact_graph(labels, points)
    target_adj = adjacency(labels, edges)
    target_triangles = triangles(labels, target_adj)
    return points, edges, target_adj, target_triangles, pair_count


def checked_odd_wheel(final_adj):
    hub = 147
    rim = (0, 144, 296, 87, 150)
    require(len({hub, *rim}) == 6, "wheel labels distinct")
    spokes = [tuple(sorted((hub, v))) for v in rim]
    rim_edges = [tuple(sorted((rim[i], rim[(i + 1) % len(rim)]))) for i in range(len(rim))]
    required = spokes + rim_edges
    require(all(v in final_adj[u] for u, v in required), "odd-wheel edge missing")
    internal = sorted(
        (u, v)
        for u, v in itertools.combinations(sorted({hub, *rim}), 2)
        if v in final_adj[u]
    )
    require(internal == sorted(required), "selected wheel unexpectedly has chords")

    # Closing a rim of k unit chords on the unit circle requires a sum of k
    # signs to be 0 modulo 6.  Check the finite parity fact explicitly here.
    sign_sums = {sum(signs) % 6 for signs in itertools.product((-1, 1), repeat=len(rim))}
    require(0 not in sign_sums, "odd rim could close")
    require(any(sum(signs) % 6 == 0 for signs in itertools.product((-1, 1), repeat=6)),
            "even-rim control")
    return hub, rim, sorted(required), internal


def anchored_wheel_join(target_adj, target_triangles):
    """Directly enumerate all anchored maps of the six-vertex wheel only."""
    cases = []
    wheel_maps = 0
    for triangle in target_triangles:
        for a, b, c in itertools.permutations(triangle):
            count = 0
            # Source rim is 0--144--296--87--150--0, hub 147.
            for x296 in target_adj[b] & target_adj[c]:
                for x150 in target_adj[a] & target_adj[c]:
                    count += len(target_adj[c] & target_adj[x296] & target_adj[x150])
            cases.append((a, b, c, count))
            wheel_maps += count
    return cases, wheel_maps


def main() -> None:
    source = source_and_surgery()
    points, target_edges, target_adj, target_triangles, target_pairs = target_graph()
    hub, rim, wheel_edges, internal = checked_odd_wheel(source["adjacency"])
    cases, wheel_maps = anchored_wheel_join(target_adj, target_triangles)

    mutated = {v: set(row) for v, row in source["adjacency"].items()}
    bad_u, bad_v = wheel_edges[0]
    mutated[bad_u].remove(bad_v)
    mutated[bad_v].remove(bad_u)
    missing_edge_rejected = False
    try:
        checked_odd_wheel(mutated)
    except ValueError:
        missing_edge_rejected = True
    require(missing_edge_rejected, "missing-edge control did not reject")

    require(source["pair_count"] == 132870, "source pair census")
    require(source["strict_edges"] == 2538, "source edge count")
    require(source["quadruples"] == 87 and source["family_count"] == 53276, "family census")
    require(len(source["vertices"]) == 508 and len(source["edges"]) == 2520, "quotient size")
    require(stream_hash(source["edges"]) == "05680a50e65c29a7321eeb6bdd8ce494b58455fd3a9d3d9f692168da43f6935b", "quotient edge hash")
    require(len(source["triangles"]) == 1030 and source["anchor"] == (0, 144, 147), "source anchor")
    require(target_pairs == 199396 and len(points) == 632 and len(target_edges) == 3112, "H632 census")
    require(stream_hash(target_edges) == "8dd36c195b3e252ec2be150ea6a029375707293fec70b63da9fc157eed4140f0", "H632 edge hash")
    require(len(target_triangles) == 1266, "H632 triangle count")
    require(stream_hash(target_triangles) == "ea6846e04b4eef58d78ebb22047014ef5603d0127cd5b91a81a107691f53df49", "H632 triangle hash")
    require(len(cases) == 7596 and wheel_maps == 0, "anchored odd-wheel join")

    result = {
        "status": "INDEPENDENT_ACCEPT_AND_STRENGTHEN",
        "source_parent": {
            "accepted_contribution_ref": PINS["accepted_source_contribution_ref"],
            "accepted_review_ref": PINS["accepted_source_review_ref"],
            "all_coordinate_pairs": source["pair_count"],
            "vertices": 516,
            "strict_unit_edges": source["strict_edges"],
            "strict_edge_sha256": source["strict_edge_sha256"],
        },
        "selected_surgery": {
            "compatible_centre_quadruples": source["quadruples"],
            "labelled_family_choices": source["family_count"],
            "operations": [list(row) for row in source["operations"]],
            "vertices": len(source["vertices"]),
            "edges": len(source["edges"]),
            "edge_sha256": stream_hash(source["edges"]),
            "triangles": len(source["triangles"]),
            "anchor": list(source["anchor"]),
        },
        "odd_wheel": {
            "hub": hub,
            "rim": list(rim),
            "required_edges": [list(row) for row in wheel_edges],
            "induced_on_six_vertices": wheel_edges == internal,
            "rim_length": len(rim),
            "odd_sign_closure_residues": sorted({sum(signs) % 6 for signs in itertools.product((-1, 1), repeat=5)}),
            "whole_plane_noninjective_maps": 0,
        },
        "target": {
            "all_coordinate_pairs": target_pairs,
            "vertices": len(points),
            "strict_unit_edges": len(target_edges),
            "edge_sha256": stream_hash(target_edges),
            "triangles": len(target_triangles),
            "triangle_sha256": stream_hash(target_triangles),
        },
        "independent_direct_wheel_join": {
            "oriented_anchor_images": len(cases),
            "wheel_maps": wheel_maps,
            "case_sha256": stream_hash(cases),
        },
        "conclusions": {
            "target_no_homomorphism": True,
            "stronger_fixed_source_no_plane_unit_edge_map": True,
            "abstract_nonfour_uses_accepted_parent": True,
            "physical_graph_constructed": False,
            "record_improvement": False,
            "other_surgeries_excluded": False,
        },
        "controls": {
            "odd_rim_sign_closure_rejected": True,
            "even_six_rim_sign_closure_exists": True,
            "missing_wheel_edge_rejected": missing_edge_rejected,
        },
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
