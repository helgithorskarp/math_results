#!/usr/bin/env python3
"""Generate the compact positive-colouring certificate (SAT is discovery only)."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pysat.solvers import Solver

from common import (
    CRITICALITY_CERTIFICATE,
    FORMAT,
    GRAPH_CERTIFICATE,
    N,
    POINTS,
    ROTATION_CERTIFICATE,
    coloring_ok,
    edge_size_histogram,
    enumerate_line_classes,
    file_sha256,
    internal_edges,
    line_digest,
    normalized_line,
    pack_coloring,
    parse_points,
    unpack_coloring,
)


def clauses(edges):
    result = [[4 * vertex + color + 1 for color in range(4)] for vertex in range(N)]
    result.extend(
        [-4 * u - color - 1, -4 * v - color - 1]
        for u, v in edges
        for color in range(4)
    )
    # A fixed triangle in L removes only global colour permutation.
    result.extend([[4 * vertex + color + 1] for color, vertex in enumerate((0, 149, 152))])
    return result


def decode_model(model):
    positive = {literal for literal in model if literal > 0}
    return [
        next(color for color in range(4) if 4 * vertex + color + 1 in positive)
        for vertex in range(N)
    ]


def generate(output: Path) -> None:
    points = parse_points(POINTS)
    classes, _discriminants, invariant, stats, radii = enumerate_line_classes(points)
    rotation = json.loads(ROTATION_CERTIFICATE.read_text())
    if rotation.get("format") != "parts509-k-rational-rotation-scan-v1":
        raise ValueError("sibling rotation certificate format mismatch")

    k_lines = set()
    for event in rotation["events"]:
        for u, v in event["event_cross_edges"]:
            key = normalized_line(points, radii, u, v)
            if (u, v) not in classes[key]:
                raise ValueError("sibling event edge is absent from the exact line census")
            k_lines.add(key)
    if not k_lines.issubset(classes):
        raise AssertionError("unknown K-event line")
    nonk = {key: classes[key] for key in classes.keys() - k_lines}

    base = internal_edges(points) + invariant
    witnesses = [unpack_coloring(rotation["generic_four_coloring"])]
    if not coloring_ok(witnesses[0], base):
        raise ValueError("sibling generic witness fails on the common base")

    # Harder (larger) cross-edge classes first produces a small deterministic library.
    search_order = sorted(nonk, key=lambda key: (-len(nonk[key]), key))
    solver_calls = 0
    for position, key in enumerate(search_order, 1):
        event_edges = nonk[key]
        if any(coloring_ok(colors, event_edges) for colors in witnesses):
            continue
        solver_calls += 1
        with Solver(name="cadical195", bootstrap_with=clauses(base + event_edges)) as solver:
            if not solver.solve():
                raise RuntimeError(f"non-K line class at search position {position} is not 4-colourable")
            colors = decode_model(solver.get_model())
        if not coloring_ok(colors, base + event_edges):
            raise AssertionError("solver returned an invalid model")
        witnesses.append(colors)

    ordered = sorted(nonk)
    assignments = []
    for key in ordered:
        assignment = next(
            index
            for index, colors in enumerate(witnesses)
            if coloring_ok(colors, nonk[key])
        )
        assignments.append(assignment)

    certificate = {
        "format": FORMAT,
        "scope": "all non-K real origin-fixing rotations of the fixed Parts-509 L/S gadgets",
        "source_sha256": {
            "parts509.vtx": file_sha256(POINTS),
            "parts509_certificate.json": file_sha256(GRAPH_CERTIFICATE),
            "rotation_certificate.json": file_sha256(ROTATION_CERTIFICATE),
            "criticality_certificate.json": file_sha256(CRITICALITY_CERTIFICATE),
        },
        "counts": {
            **stats,
            "L_edges": sum(v < 374 for _u, v in base),
            "S_edges": sum(u >= 374 for u, _v in base),
            "k_intersection_line_classes": len(k_lines),
            "nonk_line_classes": len(nonk),
            "nonk_event_rotations": 2 * len(nonk),
            "all_real_event_rotations": rotation["counts"]["event_rotations"] + 2 * len(nonk),
            "nonk_cross_edge_histogram": edge_size_histogram(nonk),
            "witnesses": len(witnesses),
            "generator_solver_calls": solver_calls,
        },
        "nonk_line_key_sha256": line_digest(nonk),
        "witnesses": [pack_coloring(colors) for colors in witnesses],
        "assignments": assignments,
    }
    output.write_text(json.dumps(certificate, separators=(",", ":")) + "\n")
    print(json.dumps(certificate["counts"], indent=2, sort_keys=True))
    print(f"nonk_line_key_sha256={certificate['nonk_line_key_sha256']}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", nargs="?", type=Path, default=Path("certificate.json"))
    args = parser.parse_args()
    generate(args.output)


if __name__ == "__main__":
    main()
