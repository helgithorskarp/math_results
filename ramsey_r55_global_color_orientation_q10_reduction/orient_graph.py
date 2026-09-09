#!/usr/bin/env python3
"""Orient a 43-vertex red edge list by color complement and check good43."""
from itertools import combinations
from pathlib import Path
import json
import sys


def need(condition, message):
    if not condition:
        raise ValueError(message)


def has_k5(red, want_red):
    for vertices in combinations(range(43), 5):
        colors = [tuple(sorted(edge)) in red
                  for edge in combinations(vertices, 2)]
        if (all(colors) if want_red else not any(colors)):
            return True
    return False


def read_graph(path):
    value = json.loads(Path(path).read_text())
    need(value.get("order") == 43, "order must be 43")
    red = set()
    for item in value.get("red_edges", []):
        need(isinstance(item, list) and len(item) == 2, "edge format")
        u, v = item
        need(isinstance(u, int) and isinstance(v, int), "integer endpoints")
        need(0 <= u < v < 43, "canonical endpoint range")
        need((u, v) not in red, "duplicate edge")
        red.add((u, v))
    return red


def orient(red):
    complete = set(combinations(range(43), 2))
    original_edges = len(red)
    original_good = not has_k5(red, True) and not has_k5(red, False)
    complemented = original_edges > 451
    oriented = complete - red if complemented else red
    oriented_good = not has_k5(oriented, True) and not has_k5(oriented, False)
    need(original_good == oriented_good, "good43 complement invariance")
    return {
        "complemented": complemented,
        "good43": oriented_good,
        "order": 43,
        "original_red_edge_count": original_edges,
        "red_edge_count": len(oriented),
        "red_edges": [list(edge) for edge in sorted(oriented)],
    }


if __name__ == "__main__":
    need(len(sys.argv) == 2, "usage: orient_graph.py GRAPH.json")
    print(json.dumps(orient(read_graph(sys.argv[1])), separators=(",", ":")))
