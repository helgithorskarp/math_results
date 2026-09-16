#!/usr/bin/env python3
"""Producer model for the frozen two-step four-contact reflection support."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_moser_all_terminal_contacts/certificate.json"
ONE = (144, 0, 0, 0)


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, b):
    out = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            common = i & j
            factor = (3 if common & 1 else 1) * (11 if common & 2 else 1)
            out[i ^ j] += a[i] * b[j] * factor
    return tuple(out)


def norm2(p, q):
    dx = sub(p[0], q[0])
    dy = sub(p[1], q[1])
    return add(mul(dx, dx), mul(dy, dy))


def strict_edges(points):
    return tuple(
        (i, j)
        for i, j in combinations(range(len(points)), 2)
        if norm2(points[i], points[j]) == ONE
    )


def reflection_candidates(points):
    edges = strict_edges(points)
    neighbors = [[] for _ in points]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    existing = set(points)
    candidates = set()
    route_count = 0
    for r, ns in enumerate(neighbors):
        for p, q in combinations(ns, 2):
            route_count += 1
            z = (
                sub(add(points[p][0], points[q][0]), points[r][0]),
                sub(add(points[p][1], points[q][1]), points[r][1]),
            )
            if z not in existing:
                candidates.add(z)
    return edges, candidates, route_count


def f4(points):
    edges, candidates, route_count = reflection_candidates(points)
    old_degrees = {
        z: sum(norm2(z, point) == ONE for point in points)
        for z in candidates
    }
    kept = tuple(sorted(z for z in candidates if old_degrees[z] >= 4))
    output = tuple(points) + kept
    return output, {
        "input_points": len(points),
        "input_edges": len(edges),
        "unit_two_path_routes": route_count,
        "distinct_new_candidates": len(candidates),
        "old_degree_histogram": {
            str(k): v for k, v in sorted(Counter(old_degrees.values()).items())
        },
        "kept_points": len(kept),
        "output_points": len(output),
    }


def full_closure(points):
    _, candidates, _ = reflection_candidates(points)
    return tuple(points) + tuple(sorted(candidates))


def accepted_closure(points):
    """The accepted source package's route-order simultaneous closure."""
    edges = strict_edges(points)
    neighbors = [[] for _ in points]
    for a, b in edges:
        neighbors[a].append(b)
        neighbors[b].append(a)
    output = list(points)
    index = {point: i for i, point in enumerate(output)}
    for r, ns in enumerate(neighbors):
        for p, q in combinations(ns, 2):
            z = (
                sub(add(points[p][0], points[q][0]), points[r][0]),
                sub(add(points[p][1], points[q][1]), points[r][1]),
            )
            if z not in index:
                index[z] = len(output)
                output.append(z)
    return tuple(output)


def load_source():
    raw_bytes = SOURCE.read_bytes()
    raw = json.loads(raw_bytes)
    if raw["scale"] != 12 or raw["basis"] != ["1", "sqrt3", "sqrt11", "sqrt33"]:
        raise ValueError("unexpected source coordinate model")
    s0 = tuple((tuple(x), tuple(y)) for x, y in raw["C"])
    s1 = accepted_closure(s0)
    return raw_bytes, raw, s0, s1


def build():
    source_bytes, source, s0, a0 = load_source()
    a1, first = f4(a0)
    a2, second = f4(a1)
    full_s2 = accepted_closure(a0)
    return source_bytes, source, s0, a0, a1, a2, full_s2, first, second


def stream_hash(rows):
    text = "".join(",".join(map(str, row)) + "\n" for row in rows)
    return hashlib.sha256(text.encode()).hexdigest()


def point_hash(points):
    return stream_hash([p[0] + p[1] for p in points])


def proper(word, vertex_count, edges, colors=4):
    return (
        len(word) == vertex_count
        and set(word) <= set("0123456789"[:colors])
        and all(word[a] != word[b] for a, b in edges)
    )


def find_coloring(vertex_count, edges, color_count, pins=None):
    adj = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colors = [-1] * vertex_count
    if pins:
        for vertex, color in pins.items():
            colors[vertex] = color

    def visit(left):
        if left == 0:
            return True
        vertex = max(
            (v for v in range(vertex_count) if colors[v] < 0),
            key=lambda v: (
                len({colors[w] for w in adj[v] if colors[w] >= 0}),
                len(adj[v]),
                -v,
            ),
        )
        forbidden = {colors[w] for w in adj[vertex] if colors[w] >= 0}
        for color in range(color_count):
            if color not in forbidden:
                colors[vertex] = color
                if visit(left - 1):
                    return True
        colors[vertex] = -1
        return False

    return tuple(colors) if visit(sum(c < 0 for c in colors)) else None


def cut_structure(vertex_count, edges):
    adj = [set() for _ in range(vertex_count)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    discovered = [-1] * vertex_count
    low = [0] * vertex_count
    parent = [-1] * vertex_count
    clock = 0
    articulations = set()
    bridges = set()

    def visit(vertex):
        nonlocal clock
        discovered[vertex] = low[vertex] = clock
        clock += 1
        children = 0
        for neighbor in adj[vertex]:
            if discovered[neighbor] < 0:
                parent[neighbor] = vertex
                children += 1
                visit(neighbor)
                low[vertex] = min(low[vertex], low[neighbor])
                if parent[vertex] < 0 and children > 1:
                    articulations.add(vertex)
                if parent[vertex] >= 0 and low[neighbor] >= discovered[vertex]:
                    articulations.add(vertex)
                if low[neighbor] > discovered[vertex]:
                    bridges.add(tuple(sorted((vertex, neighbor))))
            elif neighbor != parent[vertex]:
                low[vertex] = min(low[vertex], discovered[neighbor])

    components = 0
    for vertex in range(vertex_count):
        if discovered[vertex] < 0:
            components += 1
            visit(vertex)
    return components, tuple(sorted(articulations)), tuple(sorted(bridges))


def degree_histogram(vertex_count, edges):
    degrees = [0] * vertex_count
    for a, b in edges:
        degrees[a] += 1
        degrees[b] += 1
    return {str(k): v for k, v in sorted(Counter(degrees).items())}
