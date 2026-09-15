#!/usr/bin/env python3
"""Produce the finite H516-surgery to H632 homomorphism certificate."""

from __future__ import annotations

import argparse
from collections import Counter, deque
import hashlib
import itertools
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO / "hadwiger_nelson_heule632_pair_pilot"))
import build as host_build  # type: ignore  # noqa: E402


def need(ok, why):
    if not ok:
        raise ValueError(why)


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask -= low


def edge_hash(edges):
    raw = "".join(f"{u},{v}\n" for u, v in sorted(edges)).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def triangle_hash(triangles):
    raw = "".join(f"{u},{v},{w}\n" for u, v, w in triangles).encode("ascii")
    return hashlib.sha256(raw).hexdigest()


def source_graph(plan):
    path = REPO / "hadwiger_nelson_h516_degree4_surgeries/SOURCE.json"
    raw = path.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == plan["input_files"][str(path.relative_to(REPO))], "source input identity")
    data = json.loads(raw)
    old = {v: set() for v in data["labels"]}
    for u, v in data["edges"]:
        old[u].add(v)
        old[v].add(u)
    centres = sorted(v for v in old if len(old[v]) == 4)
    options = {
        v: [pair for pair in itertools.combinations(sorted(old[v]), 2) if pair[1] not in old[pair[0]]]
        for v in centres
    }
    stars = {v: old[v] | {v} for v in centres}
    quadruples = [
        q
        for q in itertools.combinations(centres, 4)
        if all(not (stars[u] & stars[v]) for u, v in itertools.combinations(q, 2))
    ]
    need(len(quadruples) == 87, "compatible quadruple count")
    labelled_choices = sum(
        len(options[q[0]]) * len(options[q[1]]) * len(options[q[2]]) * len(options[q[3]])
        for q in quadruples
    )
    need(labelled_choices == 53276, "labelled surgery family count")
    quadruple = quadruples[0]
    operations = [(c, *options[c][0]) for c in quadruple]
    deleted = {c for c, _, _ in operations}
    representative = {v: v for v in old}
    for _, u, v in operations:
        representative[v] = u
    vertices = sorted({representative[v] for v in old if v not in deleted})
    edges = set()
    for u, v in data["edges"]:
        if u in deleted or v in deleted:
            continue
        a, b = representative[u], representative[v]
        need(a != b, "loop after surgery")
        edges.add(tuple(sorted((a, b))))
    adjacency = {v: set() for v in vertices}
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
    triangles = [
        (u, v, w)
        for u, v in sorted(edges)
        for w in sorted(adjacency[u] & adjacency[v])
        if v < w
    ]
    anchor = min(triangles, key=lambda t: (-sum(len(adjacency[v]) for v in t), t))
    return vertices, sorted(edges), adjacency, centres, quadruples, labelled_choices, operations, triangles, anchor


def target_graph(plan):
    for name, digest in plan["input_files"].items():
        need(hashlib.sha256((REPO / name).read_bytes()).hexdigest() == digest, ("input identity", name))
    points, edges, _ = host_build.geometry()
    adjacency_sets = [set() for _ in points]
    adjacency_bits = [0 for _ in points]
    for u, v in edges:
        adjacency_sets[u].add(v)
        adjacency_sets[v].add(u)
        adjacency_bits[u] |= 1 << v
        adjacency_bits[v] |= 1 << u
    triangles = [
        (u, v, w)
        for u, v in edges
        for w in sorted(adjacency_sets[u] & adjacency_sets[v])
        if v < w
    ]
    return edges, adjacency_bits, triangles


def propagate(vertices, adjacency, target, pins):
    all_values = (1 << len(target)) - 1
    domains = {v: all_values for v in vertices}
    for v, x in pins.items():
        domains[v] = 1 << x
    queue = deque()
    queued = set()
    for w in pins:
        for v in adjacency[w]:
            queue.append((v, w))
            queued.add((v, w))
    unions = {}
    revisions = strict = 0
    while queue:
        v, w = queue.popleft()
        queued.remove((v, w))
        revisions += 1
        other = domains[w]
        possible = unions.get(other)
        if possible is None:
            possible = 0
            for x in bits(other):
                possible |= target[x]
            unions[other] = possible
        new = domains[v] & possible
        if new == domains[v]:
            continue
        domains[v] = new
        strict += 1
        if not new:
            return domains, revisions, strict
        for u in adjacency[v]:
            if (u, v) not in queued:
                queue.append((u, v))
                queued.add((u, v))
    return domains, revisions, strict


def build_certificate():
    plan = json.loads((HERE / "plan.json").read_text())
    vertices, source_edges, source_adj, centres, quadruples, choices, operations, source_triangles, anchor = source_graph(plan)
    target_edges, target_adj, target_triangles = target_graph(plan)
    zero_vertices = Counter()
    revisions = strict = empty = nonempty = 0
    for tri in target_triangles:
        for image in itertools.permutations(tri):
            domains, r, s = propagate(vertices, source_adj, target_adj, dict(zip(anchor, image)))
            revisions += r
            strict += s
            zeros = [v for v in vertices if not domains[v]]
            if zeros:
                empty += 1
                zero_vertices[zeros[0]] += 1
            else:
                nonempty += 1
    need(nonempty == 0, "unexpected surviving anchor image")
    return {
        "claim": plan["claim"],
        "source": {
            "vertices": len(vertices),
            "edges": len(source_edges),
            "edge_sha256": edge_hash(source_edges),
            "degree_four_centres": centres,
            "compatible_centre_quadruples": len(quadruples),
            "labelled_family_choices": choices,
            "selected_choice_index": 0,
            "selected_operations": [list(x) for x in operations],
            "triangles": len(source_triangles),
            "anchor": list(anchor),
            "anchor_degrees": [len(source_adj[v]) for v in anchor],
        },
        "target": {
            "vertices": len(target_adj),
            "edges": len(target_edges),
            "edge_sha256": edge_hash(target_edges),
            "triangles": len(target_triangles),
            "triangle_sha256": triangle_hash(target_triangles),
        },
        "complete_anchor_census": {
            "oriented_images": 6 * len(target_triangles),
            "empty_after_arc_consistency": empty,
            "nonempty_fixed_points": nonempty,
            "first_zero_vertex_histogram": {str(k): v for k, v in sorted(zero_vertices.items())},
            "producer_arc_revisions": revisions,
            "producer_strict_domain_revisions": strict,
        },
        "conclusion": {
            "homomorphisms": 0,
            "physical_candidate_found": False,
            "record_improvement": False,
            "source_host_pair_retired": True
        },
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    certificate = build_certificate()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print(json.dumps(certificate["complete_anchor_census"], sort_keys=True))


if __name__ == "__main__":
    main()
