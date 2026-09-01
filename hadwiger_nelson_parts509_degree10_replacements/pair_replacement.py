#!/usr/bin/env python3
"""Exact two-delete/one-add search around four Parts-509 completion points.

The verifier is solver-free.  Generation requires python-sat and writes only a
compact coloring-witness certificate, never a solver trace or proof log.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import struct
import sys
from collections import defaultdict
from pathlib import Path

import sympy


HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "hadwiger_nelson_parts509_criticality"
VERTICES = BASE / "parts509.vtx"
BASE_CERTIFICATE = BASE / "certificate.json"
MAGIC = b"HN509RP1"
N = 509
K = 4
X = N
ROW_BYTES = (N + 1 + 3) // 4
HEADER = struct.Struct("<8sHHI")
RECORD_PREFIX = struct.Struct("<HH")
EXPECTED_NEIGHBORS = (
    (6, 19, 36, 56, 78, 143, 217, 261, 262, 333),
    (28, 51, 68, 133, 135, 173, 197, 298, 339, 348),
    (7, 18, 31, 66, 85, 136, 220, 256, 273, 328),
    (39, 40, 54, 128, 144, 182, 188, 303, 334, 355),
)


def load_parts_module():
    path = BASE / "parts509.py"
    spec = importlib.util.spec_from_file_location("parts509_base", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def candidate_expressions():
    r3 = sympy.sqrt(3)
    r11 = sympy.sqrt(11)
    return (
        (-sympy.Rational(1, 6), (-r3 + 2 * r11) / 6),
        (-sympy.Rational(1, 6), (r3 + 2 * r11) / 6),
        (sympy.Rational(1, 6), (-r3 + 2 * r11) / 6),
        (sympy.Rational(1, 6), (r3 + 2 * r11) / 6),
    )


def exact_candidates(parts):
    return [(parts.to_field(x), parts.to_field(y)) for x, y in candidate_expressions()]


def load_base_data():
    parts = load_parts_module()
    points, edges = parts.load_graph(VERTICES)
    if len(points) != N or len(edges) != 2442:
        raise ValueError("unexpected base graph")
    base_certificate = json.loads(BASE_CERTIFICATE.read_text())
    packed = base64.b64decode(
        base_certificate["deletion_colorings_base64"], validate=True
    )
    if hashlib.sha256(packed).hexdigest() != base_certificate[
        "packed_deletion_colorings_sha256"
    ]:
        raise ValueError("base deletion certificate hash mismatch")
    rows = parts.unpack_deletion_rows(packed, N)
    for deleted, row in enumerate(rows):
        parts.validate_coloring(N, edges, row, K, deleted)

    candidates = exact_candidates(parts)
    if len(set(candidates)) != len(candidates):
        raise ValueError("completion points are not distinct")
    if any(candidate in points for candidate in candidates):
        raise ValueError("a completion point duplicates a Parts vertex")
    neighbors = tuple(
        tuple(
            vertex
            for vertex, point in enumerate(points)
            if parts.squared_distance(candidate, point) == parts.ONE
        )
        for candidate in candidates
    )
    if neighbors != EXPECTED_NEIGHBORS:
        raise ValueError(f"exact candidate neighborhoods differ: {neighbors}")
    manifest_edges = [tuple(edge) for edge in json.loads((HERE / "edges.json").read_text())]
    manifest_neighbors = tuple(
        tuple(row) for row in json.loads((HERE / "candidate_neighbors.json").read_text())
    )
    if manifest_edges != edges:
        raise ValueError("committed edge manifest differs from exact reconstruction")
    if manifest_neighbors != neighbors:
        raise ValueError("committed neighbor manifest differs from exact reconstruction")
    return parts, points, edges, rows, neighbors


def row_extends(rows, neighbors, row_deleted, additionally_deleted):
    used = {
        rows[row_deleted][vertex]
        for vertex in neighbors
        if vertex not in (row_deleted, additionally_deleted)
    }
    return used != set(range(K))


def residual_instances(rows, neighbor_sets):
    residual = set()
    precovered = 0
    for candidate, neighbors in enumerate(neighbor_sets):
        for u in range(N):
            for v in range(u + 1, N):
                if row_extends(rows, neighbors, u, v) or row_extends(rows, neighbors, v, u):
                    precovered += 1
                else:
                    residual.add((candidate, u, v))
    return residual, precovered


def unpack_colors(raw):
    if len(raw) != ROW_BYTES:
        raise ValueError("wrong packed coloring length")
    if raw[-1] & 0xF0:
        raise ValueError("nonzero unused bits in packed coloring")
    return tuple((raw[index // 4] >> (2 * (index % 4))) & 3 for index in range(N + 1))


def pack_colors(colors, deleted):
    values = [3 if index in deleted else color for index, color in enumerate(colors)]
    raw = bytearray(ROW_BYTES)
    for index, color in enumerate(values):
        if not 0 <= color < K:
            raise ValueError(f"invalid color {color} at {index}")
        raw[index // 4] |= color << (2 * (index % 4))
    return bytes(raw)


def read_certificate(path):
    data = path.read_bytes()
    if len(data) < HEADER.size:
        raise ValueError("truncated certificate")
    magic, vertices, candidates, count = HEADER.unpack_from(data)
    if (magic, vertices, candidates) != (MAGIC, N, len(EXPECTED_NEIGHBORS)):
        raise ValueError("certificate header mismatch")
    expected_size = HEADER.size + count * (RECORD_PREFIX.size + ROW_BYTES)
    if len(data) != expected_size:
        raise ValueError(f"certificate size mismatch: expected {expected_size}, got {len(data)}")
    records = []
    offset = HEADER.size
    for _ in range(count):
        u, v = RECORD_PREFIX.unpack_from(data, offset)
        offset += RECORD_PREFIX.size
        raw = data[offset : offset + ROW_BYTES]
        offset += ROW_BYTES
        if not 0 <= u < v < N:
            raise ValueError(f"invalid deleted pair {(u, v)}")
        records.append((u, v, raw))
    return records


def write_certificate(path, records):
    # Preserve generation order within a deleted pair: later witnesses were
    # generated only for candidates not covered by earlier witnesses.  Sorting
    # the bytes within a pair could make a later record redundant on replay.
    canonical = list(dict.fromkeys(records))
    canonical.sort(key=lambda record: (record[0], record[1]))
    with path.open("wb") as output:
        output.write(HEADER.pack(MAGIC, N, len(EXPECTED_NEIGHBORS), len(canonical)))
        for u, v, raw in canonical:
            output.write(RECORD_PREFIX.pack(u, v))
            output.write(raw)


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def verify_witness(colors, pair, edges):
    deleted = set(pair)
    for vertex, color in enumerate(colors):
        if vertex not in deleted and not 0 <= color < K:
            raise ValueError(f"invalid active color at vertex {vertex}")
    for u, v in edges:
        if u not in deleted and v not in deleted and colors[u] == colors[v]:
            raise ValueError(f"monochromatic retained edge {(u, v)} for deletion {pair}")


def command_verify(certificate_path):
    parts, points, edges, rows, neighbor_sets = load_base_data()
    del parts, points
    residual, precovered = residual_instances(rows, neighbor_sets)
    initial_residual = len(residual)
    records = read_certificate(certificate_path)
    retained_edge_checks = 0
    useful_records = 0
    for u, v, raw in records:
        colors = unpack_colors(raw)
        verify_witness(colors, (u, v), edges)
        retained_edge_checks += sum(a not in (u, v) and b not in (u, v) for a, b in edges)
        newly_covered = 0
        for candidate, neighbors in enumerate(neighbor_sets):
            if all(vertex in (u, v) or colors[vertex] != colors[X] for vertex in neighbors):
                instance = (candidate, u, v)
                if instance in residual:
                    residual.remove(instance)
                    newly_covered += 1
        if newly_covered:
            useful_records += 1
    if residual:
        sample = sorted(residual)[:10]
        raise ValueError(f"certificate leaves {len(residual)} instances uncovered, e.g. {sample}")
    if useful_records != len(records):
        raise ValueError(f"certificate contains {len(records) - useful_records} redundant records")
    summary = {
        "all_checks": True,
        "base_vertices": N,
        "base_edges": len(edges),
        "candidate_points": len(neighbor_sets),
        "exact_unit_neighbors_per_candidate": [len(row) for row in neighbor_sets],
        "two_deletion_instances": len(neighbor_sets) * N * (N - 1) // 2,
        "instances_covered_by_prior_deletion_rows": precovered,
        "residual_instances": initial_residual,
        "certificate_records": len(records),
        "useful_certificate_records": useful_records,
        "retained_edge_inequality_checks": retained_edge_checks,
        "certificate_sha256": file_sha256(certificate_path),
        "conclusion": "every certified two-delete/one-add graph is 4-colorable",
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


def color_var(vertex, color):
    return vertex * K + color + 1


DELETE_BASE = (N + 1) * K + 1
SELECTOR_BASE = DELETE_BASE + N


def delete_var(vertex):
    return DELETE_BASE + vertex


def selector_var(candidate):
    return SELECTOR_BASE + candidate


def make_solver(edges, neighbor_sets, solver_name):
    from pysat.solvers import Solver

    solver = Solver(name=solver_name)
    for vertex in range(N):
        solver.add_clause([delete_var(vertex)] + [color_var(vertex, color) for color in range(K)])
    solver.add_clause([color_var(X, color) for color in range(K)])
    for u, v in edges:
        for color in range(K):
            solver.add_clause(
                [delete_var(u), delete_var(v), -color_var(u, color), -color_var(v, color)]
            )
    for candidate, neighbors in enumerate(neighbor_sets):
        for vertex in neighbors:
            for color in range(K):
                solver.add_clause(
                    [
                        -selector_var(candidate),
                        delete_var(vertex),
                        -color_var(X, color),
                        -color_var(vertex, color),
                    ]
                )
    for color, vertex in enumerate((0, 149, 152)):
        solver.add_clause([delete_var(vertex), color_var(vertex, color)])
    return solver


def solve_assumptions(pair, candidate):
    deleted = set(pair)
    return [delete_var(v) if v in deleted else -delete_var(v) for v in range(N)] + [
        selector_var(candidate)
    ]


def model_colors(model, pair):
    positive = {literal for literal in model if literal > 0}
    deleted = set(pair)
    colors = []
    for vertex in range(N + 1):
        if vertex in deleted:
            colors.append(-1)
            continue
        selected = [color for color in range(K) if color_var(vertex, color) in positive]
        if not selected:
            raise ValueError(f"model gives active vertex {vertex} no color")
        colors.append(selected[0])
    return colors


def command_generate(output_path, solver_name):
    _, _, edges, rows, neighbor_sets = load_base_data()
    residual, _ = residual_instances(rows, neighbor_sets)
    by_pair = defaultdict(set)
    for candidate, u, v in residual:
        by_pair[(u, v)].add(candidate)
    records = []
    with make_solver(edges, neighbor_sets, solver_name) as solver:
        for pair_number, pair in enumerate(sorted(by_pair), 1):
            uncovered = by_pair[pair]
            while uncovered:
                target = min(uncovered)
                if not solver.solve(solve_assumptions(pair, target)):
                    raise RuntimeError(
                        f"found a non-4-colorable 508-vertex candidate: point {target}, deletion {pair}"
                    )
                colors = model_colors(solver.get_model(), pair)
                verify_witness(colors, pair, edges)
                covered = {
                    candidate
                    for candidate in uncovered
                    if all(
                        vertex in pair or colors[vertex] != colors[X]
                        for vertex in neighbor_sets[candidate]
                    )
                }
                if target not in covered:
                    raise AssertionError("target not covered by its own SAT model")
                uncovered.difference_update(covered)
                records.append((*pair, pack_colors(colors, set(pair))))
            if pair_number % 1000 == 0:
                print(f"pairs={pair_number}/{len(by_pair)} records={len(records)}", flush=True)
    write_certificate(output_path, records)
    command_verify(output_path)


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    verify = subparsers.add_parser("verify", help="solver-free exact replay")
    verify.add_argument("certificate", type=Path)
    generate = subparsers.add_parser("generate", help="regenerate SAT coloring witnesses")
    generate.add_argument("output", type=Path)
    generate.add_argument("--solver", default="minisat22")
    return parser


def main():
    args = build_parser().parse_args()
    if args.command == "verify":
        command_verify(args.certificate)
    else:
        command_generate(args.output, args.solver)


if __name__ == "__main__":
    main()
