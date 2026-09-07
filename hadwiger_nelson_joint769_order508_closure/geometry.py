#!/usr/bin/env python3
"""Reconstruct the exact 769-point fresh-triangle host."""

from fractions import Fraction
from itertools import combinations
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CYCLIC = REPO / "hadwiger_nelson_cyclic_batch_probe"
SEED = REPO / "hadwiger_nelson_neutral_mutation_candidate"
RADICANDS = (1, 3, 5, 15, 11, 33, 55, 165)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run_source(script, arguments):
    optimize = "-" + "O" * sys.flags.optimize if sys.flags.optimize else None
    command = [sys.executable]
    if optimize:
        command.append(optimize)
    command.extend([str(script), *map(str, arguments)])
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    run = subprocess.run(command, capture_output=True, text=True, env=environment)
    require(run.returncode == 0, f"source reconstruction failed: {script.name}\n{run.stdout}{run.stderr}")
    return run.stdout


def square(row):
    result = [Fraction(0) for _ in range(8)]
    for left in range(8):
        for right in range(left, 8):
            result[left ^ right] += (
                (1 if left == right else 2)
                * row[left]
                * row[right]
                * RADICANDS[left & right]
            )
    return tuple(result)


def squared_distance(left, right):
    difference = [
        tuple(a - b for a, b in zip(left[axis], right[axis]))
        for axis in range(2)
    ]
    return tuple(a + b for a, b in zip(square(difference[0]), square(difference[1])))


def decode_point(raw):
    require(
        isinstance(raw, list)
        and len(raw) == 2
        and all(isinstance(axis, list) and len(axis) == 8 for axis in raw),
        "malformed field point",
    )
    return tuple(tuple(Fraction(value) for value in axis) for axis in raw)


def generate(output, certificate):
    output.mkdir(parents=True, exist_ok=True)
    gate_output = output / "source_gate"
    seed_output = output / "source_seed"
    run_source(CYCLIC / "gate_geometry.py", ["--output", gate_output])
    run_source(SEED / "verify.py", ["--output", seed_output])

    gate = json.loads((gate_output / "gate_geometry.json").read_text())
    seed_graph = json.loads((seed_output / "graph.json").read_text())
    require(len(seed_graph["coordinates"]) == 509 and seed_graph["scale"] == 96, "seed geometry")
    seed_points = [
        (
            tuple(Fraction(value, 96) for value in row[:8]),
            tuple(Fraction(value, 96) for value in row[8:]),
        )
        for row in seed_graph["coordinates"]
    ]
    require(all(len(row) == 16 for row in seed_graph["coordinates"]), "seed coordinate width")

    triangles = gate["K_triangles"]
    require(len(triangles) == 126, "fresh triangle count")
    used = sorted({point for triangle in triangles for point in triangle})
    require(len(used) == certificate["added_vertices"] == 260, "triangle-union support")
    records = gate["K_points"]
    require(used and used[-1] < len(records), "triangle point outside catalogue")
    added_points = [decode_point(records[source]["point"]) for source in used]
    require(
        len(set(seed_points + added_points)) == certificate["host_vertices"] == 769,
        "coincident host points",
    )

    one = (Fraction(1),) + (Fraction(0),) * 7
    seed_added = []
    for seed_vertex, seed_point in enumerate(seed_points):
        for added_vertex, added_point in enumerate(added_points):
            if squared_distance(seed_point, added_point) == one:
                seed_added.append((seed_vertex, 509 + added_vertex))
    source_to_added = {source: index for index, source in enumerate(used)}
    declared_seed_added = sorted(
        (seed_vertex, 509 + source_to_added[source])
        for source in used
        for seed_vertex in records[source]["neighbours"]
    )
    require(seed_added == declared_seed_added, "seed-added unit-edge census")

    added_edges = []
    for left, right in combinations(range(260), 2):
        if squared_distance(added_points[left], added_points[right]) == one:
            added_edges.append((509 + left, 509 + right))
    added_edge_set = set(added_edges)
    require(
        all(
            (min(509 + source_to_added[a], 509 + source_to_added[b]),
             max(509 + source_to_added[a], 509 + source_to_added[b])) in added_edge_set
            for triangle in triangles
            for a, b in combinations(triangle, 2)
        ),
        "non-unit declared triangle",
    )

    seed_edges = [tuple(edge) for edge in seed_graph["edges"]]
    require(
        seed_edges == sorted(set(seed_edges))
        and len(seed_edges) == 2447
        and all(0 <= left < right < 509 for left, right in seed_edges),
        "seed edge census",
    )
    edges = sorted(seed_edges + seed_added + added_edges)
    edge_data = json.dumps(edges, separators=(",", ":")).encode()
    require(
        len(edges) == certificate["host_edges"] == 3560
        and digest(edge_data) == certificate["host_edges_sha256"],
        "host edge census",
    )
    host = {
        "vertices": len(seed_points) + len(added_points),
        "edges": edges,
        "seed_vertices": len(seed_points),
        "added_source_ids": used,
    }
    (output / "host.json").write_text(json.dumps(host, separators=(",", ":")) + "\n")
    result = {
        "vertices": len(seed_points) + len(added_points),
        "edges": len(edges),
        "seed_edges": len(seed_edges),
        "seed_added_edges": len(seed_added),
        "added_edges": len(added_edges),
        "fresh_triangles": len(triangles),
        "added_points": len(added_points),
        "pair_checks": 769 * 768 // 2,
        "host_edges_sha256": digest(edge_data),
    }
    return result, edges
