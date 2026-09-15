#!/usr/bin/env python3
"""Independent exact checker for the H516-surgery/H632 homomorphism gate."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def check(ok, why):
    if not ok:
        raise ValueError(why)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    check(spec is not None and spec.loader is not None, ("module", path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def stream_hash(rows):
    raw = "".join(",".join(map(str, row)) + "\n" for row in rows).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def reconstruct_source(plan):
    path = REPO / "hadwiger_nelson_h516_degree4_surgeries/SOURCE.json"
    raw = path.read_bytes()
    check(hashlib.sha256(raw).hexdigest() == plan["input_files"][str(path.relative_to(REPO))], "source identity")
    source = json.loads(raw)
    labels = sorted(source["labels"])
    adjacency = {v: set() for v in labels}
    for edge in source["edges"]:
        check(len(edge) == 2 and edge[0] < edge[1], "source edge order")
        u, v = edge
        check(u in adjacency and v in adjacency and v not in adjacency[u], "source simple edge")
        adjacency[u].add(v)
        adjacency[v].add(u)
    centres = [v for v in labels if len(adjacency[v]) == 4]
    allowed = {}
    for centre in centres:
        neighbours = sorted(adjacency[centre])
        allowed[centre] = [
            (u, v)
            for u, v in itertools.combinations(neighbours, 2)
            if v not in adjacency[u]
        ]
    quadruples = []
    for q in itertools.combinations(centres, 4):
        closed = [{v} | adjacency[v] for v in q]
        if all(not (closed[i] & closed[j]) for i in range(4) for j in range(i + 1, 4)):
            quadruples.append(q)
    family_count = sum(
        len(allowed[q[0]]) * len(allowed[q[1]]) * len(allowed[q[2]]) * len(allowed[q[3]])
        for q in quadruples
    )
    check(len(quadruples) == 87 and family_count == 53276, "frozen family")
    operations = [(c, *min(allowed[c])) for c in quadruples[0]]

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
        deleted.add(centre)
        union(u, v)
    vertices = sorted({find(v) for v in labels if v not in deleted})
    edges = set()
    for u, v in source["edges"]:
        if u in deleted or v in deleted:
            continue
        a, b = find(u), find(v)
        check(a != b, "quotient loop")
        edges.add((min(a, b), max(a, b)))
    final_adj = {v: set() for v in vertices}
    for u, v in edges:
        final_adj[u].add(v)
        final_adj[v].add(u)

    triangle_set = set()
    for u in vertices:
        for v, w in itertools.combinations(sorted(final_adj[u]), 2):
            if w in final_adj[v]:
                triangle_set.add(tuple(sorted((u, v, w))))
    triangles = sorted(triangle_set)
    anchor = min(triangles, key=lambda t: (-sum(len(final_adj[v]) for v in t), t))
    return vertices, sorted(edges), final_adj, centres, quadruples, family_count, operations, triangles, anchor


def reconstruct_target(plan):
    for name, digest in plan["input_files"].items():
        check(hashlib.sha256((REPO / name).read_bytes()).hexdigest() == digest, ("input identity", name))
    independent = load_module(
        "h632_independent_geometry",
        REPO / "hadwiger_nelson_heule632_pair_pilot/independent.py",
    )
    points, edges, _ = independent.geometry()
    adjacency = [set() for _ in points]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangles = []
    for u in range(len(points)):
        for v, w in itertools.combinations(sorted(adjacency[u]), 2):
            if u < v < w and w in adjacency[v]:
                triangles.append((u, v, w))
    return edges, adjacency, sorted(triangles)


def neighbour_union(mask, target_bits):
    answer = 0
    while mask:
        low = mask & -mask
        answer |= target_bits[low.bit_length() - 1]
        mask -= low
    return answer


def synchronous_arc_consistency(vertices, source_adj, target_bits, pins):
    full = (1 << len(target_bits)) - 1
    domains = {v: full for v in vertices}
    for v, image in pins.items():
        domains[v] = 1 << image
    rounds = 0
    while True:
        rounds += 1
        unions = {}
        next_domains = {}
        for v in vertices:
            domain = domains[v]
            for w in source_adj[v]:
                other = domains[w]
                possible = unions.get(other)
                if possible is None:
                    possible = neighbour_union(other, target_bits)
                    unions[other] = possible
                domain &= possible
                if not domain:
                    break
            next_domains[v] = domain
        if any(not next_domains[v] for v in vertices):
            return next_domains, rounds
        if all(next_domains[v] == domains[v] for v in vertices):
            return next_domains, rounds
        domains = next_domains


def tiny_controls():
    pairs = [(0, 1), (0, 2), (1, 2)]
    cases = valid_maps = 0
    for source_mask in range(8):
        source_adj = {v: set() for v in range(3)}
        source_edges = []
        for i, (u, v) in enumerate(pairs):
            if source_mask >> i & 1:
                source_adj[u].add(v)
                source_adj[v].add(u)
                source_edges.append((u, v))
        for target_mask in range(8):
            target_bits = [0, 0, 0]
            target_edges = set()
            for i, (u, v) in enumerate(pairs):
                if target_mask >> i & 1:
                    target_bits[u] |= 1 << v
                    target_bits[v] |= 1 << u
                    target_edges.add((u, v))
            for pin_mask in range(8):
                pin_vertices = [v for v in range(3) if pin_mask >> v & 1]
                for images in itertools.product(range(3), repeat=len(pin_vertices)):
                    pins = dict(zip(pin_vertices, images))
                    domains, _ = synchronous_arc_consistency(range(3), source_adj, target_bits, pins)
                    actual = []
                    for word in itertools.product(range(3), repeat=3):
                        if any(word[v] != x for v, x in pins.items()):
                            continue
                        if all(tuple(sorted((word[u], word[v]))) in target_edges for u, v in source_edges):
                            actual.append(word)
                    for word in actual:
                        check(all(domains[v] >> word[v] & 1 for v in range(3)), "control map removed")
                    if any(not domains[v] for v in range(3)):
                        check(not actual, "control false exclusion")
                    valid_maps += len(actual)
                    cases += 1
    return {"tiny_cases": cases, "valid_map_instances": valid_maps}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--controls", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    plan = json.loads((HERE / "plan.json").read_text())
    certificate = json.loads((HERE / "certificate.json").read_text())

    vertices, source_edges, source_adj, centres, quadruples, choices, operations, source_triangles, anchor = reconstruct_source(plan)
    target_edges, target_adj, target_triangles = reconstruct_target(plan)
    target_bits = [sum(1 << v for v in row) for row in target_adj]

    source_expected = {
        "vertices": len(vertices),
        "edges": len(source_edges),
        "edge_sha256": stream_hash(source_edges),
        "degree_four_centres": centres,
        "compatible_centre_quadruples": len(quadruples),
        "labelled_family_choices": choices,
        "selected_choice_index": 0,
        "selected_operations": [list(x) for x in operations],
        "triangles": len(source_triangles),
        "anchor": list(anchor),
        "anchor_degrees": [len(source_adj[v]) for v in anchor],
    }
    target_expected = {
        "vertices": len(target_adj),
        "edges": len(target_edges),
        "edge_sha256": stream_hash(target_edges),
        "triangles": len(target_triangles),
        "triangle_sha256": stream_hash(target_triangles),
    }
    check(certificate["claim"] == plan["claim"], "claim")
    check(certificate["source"] == source_expected, "source metadata")
    check(certificate["target"] == target_expected, "target metadata")

    empty = nonempty = 0
    round_histogram = Counter()
    for triangle in target_triangles:
        for image in itertools.permutations(triangle):
            domains, rounds = synchronous_arc_consistency(
                vertices,
                source_adj,
                target_bits,
                dict(zip(anchor, image)),
            )
            round_histogram[rounds] += 1
            if any(not domains[v] for v in vertices):
                empty += 1
            else:
                nonempty += 1
    census = certificate["complete_anchor_census"]
    check(census["oriented_images"] == 6 * len(target_triangles) == 7596, "complete anchor count")
    check(census["empty_after_arc_consistency"] == empty == 7596, "all anchored cases empty")
    check(census["nonempty_fixed_points"] == nonempty == 0, "no surviving fixed point")
    check(sum(census["first_zero_vertex_histogram"].values()) == empty, "producer zero histogram total")
    check(census["producer_arc_revisions"] > 0 and census["producer_strict_domain_revisions"] > 0, "producer schedule counts")
    check(certificate["conclusion"] == {
        "homomorphisms": 0,
        "physical_candidate_found": False,
        "record_improvement": False,
        "source_host_pair_retired": True,
    }, "conclusion")

    result = {
        "verified": True,
        "source_vertices": len(vertices),
        "source_edges": len(source_edges),
        "target_vertices": len(target_adj),
        "target_edges": len(target_edges),
        "source_anchor": list(anchor),
        "target_triangles": len(target_triangles),
        "oriented_anchor_images": empty + nonempty,
        "empty_after_independent_synchronous_arc_consistency": empty,
        "nonempty_fixed_points": nonempty,
        "synchronous_round_histogram": {str(k): v for k, v in sorted(round_histogram.items())},
        "homomorphisms": 0,
        "record_improvement": False,
    }
    if args.controls:
        result["controls"] = tiny_controls()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
