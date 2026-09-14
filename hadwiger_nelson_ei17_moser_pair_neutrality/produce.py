"""Deterministically construct positive two-terminal relation witnesses."""

from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path

from model import DEPENDENCIES, build, need


def solve(order, edges, colours_count, pins=()):
    adjacency = [set() for _ in range(order)]
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    colours = [-1] * order
    for vertex, colour in pins:
        if colours[vertex] not in (-1, colour):
            return None
        colours[vertex] = colour
    if any(colours[a] == colours[b] != -1 for a, b in edges):
        return None

    def visit():
        best = None
        for vertex in range(order):
            if colours[vertex] >= 0:
                continue
            forbidden = {colours[w] for w in adjacency[vertex] if colours[w] >= 0}
            allowed = tuple(c for c in range(colours_count) if c not in forbidden)
            if not allowed:
                return False
            key = (len(forbidden), len(adjacency[vertex]), -vertex)
            if best is None or key > best[0]:
                best = key, vertex, allowed
        if best is None:
            return True
        _, vertex, allowed = best
        for colour in allowed:
            colours[vertex] = colour
            if visit():
                return True
        colours[vertex] = -1
        return False

    return tuple(colours) if visit() else None


def generate():
    graph = build()
    edges = graph["edges"]
    edge_set = set(edges)
    order = len(graph["classes"])
    first = solve(order, edges, 4)
    need(first is not None, "source is not four-colourable; requires separate certificate")
    words = [first]

    while True:
        by_signature = {}
        for vertex in range(order):
            by_signature.setdefault(tuple(word[vertex] for word in words), []).append(vertex)
        block = next((vertices for vertices in by_signature.values() if len(vertices) > 1), None)
        if block is None:
            break
        a, b = block[:2]
        word = solve(order, edges, 4, ((a, 0), (b, 1)))
        need(word is not None, f"forced equal pair requires separate certificate: {a},{b}")
        words.append(word)

    for a, b in combinations(range(order), 2):
        if (a, b) in edge_set or any(word[a] == word[b] for word in words):
            continue
        word = solve(order, edges, 4, ((a, 0), (b, 0)))
        need(word is not None, f"forced different nonedge requires separate certificate: {a},{b}")
        words.append(word)

    collision_classes = [list(group) for group in graph["classes"] if len(group) > 1]
    return {
        "schema": "ei17-moser-pair-neutrality-v1",
        "dependency_sha256": DEPENDENCIES,
        "formal_addresses": 119,
        "physical_points": order,
        "unit_edges": len(edges),
        "collision_classes": collision_classes,
        "graph_sha256": graph["graph_sha256"],
        "words": ["".join(map(str, word)) for word in words],
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    need(not args.out.exists(), "output path already exists")
    certificate = generate()
    args.out.write_text(json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n")
    print(json.dumps({
        "output": str(args.out),
        "physical_points": certificate["physical_points"],
        "unit_edges": certificate["unit_edges"],
        "colour_words": len(certificate["words"]),
    }, sort_keys=True))
