#!/usr/bin/env python3
"""Solver-free exact check of the five nonidentity T375 D3 self-gluings."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "hadwiger_nelson_small_triangle_forcer375"
DEPENDENCIES = {
    "geometry.py": "921fa358c620ed86bd11c6fc9f97ae03ddb491da94612f086cd165a94ffc77bd",
    "appendix.json": "dd74c3ef0bb3e9cc1c9c32f7ecc703c1d85cacaca6fca97834d162e8c05997fa",
    "certificate.json": "282fd209157b0c327e02451c32a3d2f2dbb40c4ec31e6531bdd3b8316854b28e",
    "colour_check.py": "c5ffcb2c0a0ff93a6ee06364e307648933274b6df4cbcc6f990e5ddc35294e1a",
}
PATTERNS = ("001", "010", "011", "012")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest_bytes(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reflect(p):
    a, b, c, d = p
    return (-a, -b, c, d)


def transform(geometry, p, rotation, reflected):
    q = reflect(p) if reflected else p
    for _ in range(rotation):
        q = geometry.rotate(q)
    return q


def build_case(geometry, source_points, source_edges, rotation, reflected):
    moved = [transform(geometry, p, rotation, reflected) for p in source_points]
    points = list(source_points)
    index = {p: i for i, p in enumerate(points)}
    moved_indices = []
    for p in moved:
        if p not in index:
            index[p] = len(points)
            points.append(p)
        moved_indices.append(index[p])
    require(set(index[p] for p in geometry.TERMINALS) == {0, 1, 2},
            "marked triangle was not preserved")
    inherited = {tuple(edge) for edge in source_edges}
    inherited |= {
        tuple(sorted((moved_indices[u], moved_indices[v])))
        for u, v in source_edges
    }
    edges = geometry.edges(points)
    return points, edges, inherited


def check_word(word, pattern, order, edges):
    require(type(word) is str and len(word) == order and set(word) <= set("0123"),
            "malformed colour word")
    require(word[:3] == pattern, "wrong canonical terminal pattern")
    require(all(word[u] != word[v] for u, v in edges), "improper colour word")


def verify(certificate):
    require(certificate.get("schema") == 1, "wrong schema")
    for name, expected_hash in DEPENDENCIES.items():
        require(digest_bytes(SOURCE / name) == expected_hash, f"changed dependency {name}")
    geometry = load_module("t375_d3_geometry", SOURCE / "geometry.py")
    colour_check = load_module("t375_d3_colour_check", SOURCE / "colour_check.py")
    source_points, source_edges = geometry.graph()
    require(len(source_points) == 375 and len(source_edges) == 1661,
            "changed T375 source inventory")
    answer, forcing_stats = colour_check.solve(
        375, source_edges, [(0, 0), (1, 0), (2, 0)]
    )
    require(answer is None, "T375 no longer forbids a monochromatic marked triangle")
    require(forcing_stats == {"nodes": 735, "conflicts": 367},
            "changed T375 exhaustive replay")

    expected_actions = [(1, False), (2, False), (0, True), (1, True), (2, True)]
    cases = certificate.get("cases")
    require(type(cases) is list and len(cases) == 5, "wrong case count")
    summaries = []
    for case, (rotation, reflected) in zip(cases, expected_actions):
        require(case.get("rotation_steps_120") == rotation and
                case.get("reflected_in_y_axis_first") is reflected,
                "wrong or reordered D3 action")
        points, edges, inherited = build_case(
            geometry, source_points, source_edges, rotation, reflected
        )
        require(len(points) == case.get("points") and len(points) <= 508,
                "wrong point count or cap failure")
        require(750 - len(points) == case.get("collisions_between_copies"),
                "wrong collision count")
        require(len(edges) == case.get("edges") and
                len(inherited) == case.get("inherited_edge_union"),
                "wrong edge inventory")
        require(geometry.digest(points) == case.get("point_sha256") and
                geometry.digest(edges) == case.get("edge_sha256"),
                "wrong geometry hash")
        require(inherited <= {tuple(edge) for edge in edges},
                "inherited edge absent from complete physical graph")
        words = case.get("terminal_witnesses")
        require(type(words) is dict and tuple(sorted(words)) == PATTERNS,
                "wrong witness patterns")
        for pattern in PATTERNS:
            check_word(words[pattern], pattern, len(points), edges)
        summaries.append({
            "rotation_steps_120": rotation,
            "reflected_in_y_axis_first": reflected,
            "points": len(points),
            "collisions_between_copies": 750 - len(points),
            "complete_unit_edges": len(edges),
            "inherited_unit_edges": len(inherited),
            "incidental_cross_contacts": len(edges) - len(inherited),
            "all_four_nonmonochromatic_patterns_extend": True,
            "four_colourable": True,
        })
    return {
        "verified": True,
        "source": {"points": 375, "edges": 1661,
                   "monochromatic_terminal_query": forcing_stats},
        "cases": summaries,
        "all_cases_at_most_508": True,
        "all_relations_unchanged": True,
        "record_candidate": False,
    }


def malformed_controls(certificate):
    bad = json.loads(json.dumps(certificate))
    bad["cases"][0]["terminal_witnesses"]["001"] = (
        "1" + bad["cases"][0]["terminal_witnesses"]["001"][1:]
    )
    try:
        verify(bad)
    except ValueError:
        return 1
    raise RuntimeError("malformed colour certificate accepted")


def main():
    certificate = json.loads((HERE / "certificate.json").read_text())
    result = verify(certificate)
    result["malformed_controls_rejected"] = malformed_controls(certificate)
    expected = json.loads((HERE / "expected.json").read_text())
    require(result == expected, "expected result mismatch")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    print("EXACT T375 D3 SELF-GLUING CLOSURE VERIFIED")


if __name__ == "__main__":
    main()
