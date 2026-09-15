#!/usr/bin/env python3
"""Exact conservative four-colour proof for the EI17 difference body."""

from __future__ import annotations

import hashlib
import importlib
import json
import sys
from fractions import Fraction
from itertools import combinations
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_ei17_common_pair"
DEPENDENCIES = {
    "intervals.py": "0fb646ef2fccf68334e6c0d80d1b2f7210a73a1f0135030a15ccf02c1d5b3ce7",
    "seed.py": "9ec359a35d352b1947d87516df918135eb83658a2125ccfc6515dcbff907e833",
    "seed_edges.json": "b77a3a242467f2c1ed3f047914492e70a0da9cbe6ca8234941c8dd008e25e450",
    "seed_midpoint.json": "fb712ad09168fa51814556641f31280acc8ad1e71a17a9878d1cfd55eeb96565",
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(value):
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(payload).hexdigest()


def overlaps(a, b):
    return a.lo <= b.hi and b.lo <= a.hi


def load_source():
    for name, expected in DEPENDENCIES.items():
        actual = hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
        require(actual == expected, f"changed source dependency: {name}")
    sys.path.insert(0, str(SOURCE))
    try:
        intervals = importlib.import_module("intervals")
        seed = importlib.import_module("seed")
    finally:
        sys.path.pop(0)
    return intervals, seed


def reconstruct():
    intervals, seed = load_source()
    source_points, root = seed.certify()
    source_edges = [tuple(edge) for edge in
                    json.loads((SOURCE / "seed_edges.json").read_text())]
    require(len(source_points) == 17 and len(source_edges) == 31,
            "wrong EI17 inventory")

    addresses = [(i, j) for i in range(17) for j in range(17)]
    boxes = [tuple(source_points[i][k] - source_points[j][k] for k in range(2))
             for i, j in addresses]
    parent = list(range(289))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        a, b = find(a), find(b)
        if a != b:
            parent[max(a, b)] = min(a, b)

    possible_collision_pairs = 0
    for a, b in combinations(range(289), 2):
        if overlaps(boxes[a][0], boxes[b][0]) and overlaps(boxes[a][1], boxes[b][1]):
            possible_collision_pairs += 1
            union(a, b)
    grouped = {}
    for address in range(289):
        grouped.setdefault(find(address), []).append(address)
    classes = [grouped[key] for key in sorted(grouped)]
    class_of = {address: c for c, group in enumerate(classes) for address in group}

    edges = set()
    unit_gap = None
    separation = None
    for a, b in combinations(range(289), 2):
        d2 = intervals.squared_distance(boxes[a], boxes[b])
        ca, cb = class_of[a], class_of[b]
        if ca == cb:
            require(not d2.contains(1), "possible unit edge inside one colour group")
            gap = min(abs(d2.lo - intervals.Q), abs(d2.hi - intervals.Q))
            unit_gap = gap if unit_gap is None else min(unit_gap, gap)
        elif d2.contains(1):
            edges.add(tuple(sorted((ca, cb))))
        else:
            gap = min(abs(d2.lo - intervals.Q), abs(d2.hi - intervals.Q))
            unit_gap = gap if unit_gap is None else min(unit_gap, gap)
        if ca != cb:
            gaps = []
            for k in range(2):
                if boxes[a][k].hi < boxes[b][k].lo:
                    gaps.append(boxes[b][k].lo - boxes[a][k].hi)
                elif boxes[b][k].hi < boxes[a][k].lo:
                    gaps.append(boxes[a][k].lo - boxes[b][k].hi)
            require(gaps, "different colour groups can still collide")
            local = max(gaps)
            separation = local if separation is None else min(separation, local)
    edges = sorted(edges)

    embedded = [class_of[17 * i + 16] for i in range(17)]
    require(len(set(embedded)) == 17, "embedded EI17 copy collapsed")
    edge_set = set(edges)
    require(all(tuple(sorted((embedded[u], embedded[v]))) in edge_set
                for u, v in source_edges), "source edge absent from supergraph")
    return {
        "intervals": intervals,
        "root": root,
        "classes": classes,
        "class_of": class_of,
        "edges": edges,
        "embedded": embedded,
        "possible_collision_pairs": possible_collision_pairs,
        "unit_gap": unit_gap,
        "separation": separation,
    }


def verify(certificate):
    graph = reconstruct()
    word = certificate.get("four_colour_word")
    require(certificate.get("schema") == 1 and type(word) is str,
            "malformed certificate")
    require(len(word) == len(graph["classes"]) and set(word) <= set("0123"),
            "malformed colour word")
    require(all(word[u] != word[v] for u, v in graph["edges"]),
            "improper conservative-supergraph colouring")

    intervals = graph["intervals"]
    histogram = {
        str(size): sum(len(group) == size for group in graph["classes"])
        for size in sorted({len(group) for group in graph["classes"]})
    }
    return {
        "verified": True,
        "formal_difference_addresses": 289,
        "physical_point_upper_bound": 273,
        "possible_collision_pairs": graph["possible_collision_pairs"],
        "possible_equality_colour_groups": len(graph["classes"]),
        "class_size_histogram": histogram,
        "conservative_possible_unit_edges": len(graph["edges"]),
        "conservative_graph_sha256": digest({
            "classes": graph["classes"], "edges": graph["edges"]
        }),
        "coordinate_separation_lower": str(Fraction(graph["separation"], intervals.Q)),
        "squared_unit_exclusion_gap_lower": str(Fraction(graph["unit_gap"], intervals.Q)),
        "embedded_EI17_vertices": len(graph["embedded"]),
        "embedded_EI17_edges": 31,
        "physical_graph_chromatic_number": 4,
        "record_candidate": False,
    }


def malformed_control(certificate):
    bad = dict(certificate)
    word = certificate["four_colour_word"]
    graph = reconstruct()
    u, v = graph["edges"][0]
    replacement = list(word)
    replacement[v] = replacement[u]
    bad["four_colour_word"] = "".join(replacement)
    try:
        verify(bad)
    except ValueError:
        return 1
    raise RuntimeError("corrupted colouring accepted")


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    result = verify(certificate)
    result["malformed_controls_rejected"] = malformed_control(certificate)
    expected = json.loads((HERE / "expected.json").read_text())
    require(result == expected, "expected result mismatch")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("EXACT EI17 DIFFERENCE-BODY FOUR-COLOUR STOP VERIFIED")


if __name__ == "__main__":
    main()
