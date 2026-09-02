#!/usr/bin/env python3
"""Generate and verify the two G14 completion augmentations of Parts-509.

The public verifier is solver-free.  The ``generate`` command uses PySAT only
to produce compact proper-colouring witnesses.  The ``cnf`` command writes the
pinned four-colouring instance for the 510-vertex A-pair; keep that instance
and its proof log under /scratch.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import sys
import time
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BASE = ROOT / "hadwiger_nelson_parts509_criticality"
SWAP = ROOT / "hadwiger_nelson_parts509_swap_closure"
sys.path.insert(0, str(SWAP))
import kfield

A_Q = (470, 523, 653, 619)
B_Q = (411, 750, 454, 417)
PAIR_Q = (523, 619)
A_DROP = 350
K = 4


def load_parts_module():
    spec = importlib.util.spec_from_file_location("parts509_g14_augmentation", BASE / "parts509.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def load_geometry():
    parts = load_parts_module()
    vertices = parts.parse_points(BASE / "parts509.vtx")
    completion_doc = json.loads((SWAP / "completion_points.json").read_text())

    def qpoint(index):
        row = completion_doc["points"][index]
        return kfield.from_strings(row["x"]), kfield.from_strings(row["y"])

    def graph(qids, drop=None):
        labels = [["V", v] for v in range(509) if v != drop] + [["Q3", q] for q in qids]
        points = [vertices[index] if kind == "V" else qpoint(index) for kind, index in labels]
        if len(set(points)) != len(points):
            raise ValueError("augmentation repeats a point")
        return labels, points, parts.build_edges(points)

    return parts, completion_doc, graph


def pack(values):
    if any(not 0 <= value < 4 for value in values):
        raise ValueError("only two-bit colours may be packed")
    out = bytearray((2 * len(values) + 7) // 8)
    for i, value in enumerate(values):
        out[(2 * i) // 8] |= value << ((2 * i) % 8)
    return bytes(out)


def unpack(raw, count):
    if len(raw) != (2 * count + 7) // 8:
        raise ValueError("packed row has the wrong length")
    values = [(raw[(2 * i) // 8] >> ((2 * i) % 8)) & 3 for i in range(count)]
    used_bits = (2 * count) % 8
    if used_bits and raw[-1] >> used_bits:
        raise ValueError("nonzero unused bits in packed row")
    return values


def packed_rows(rows):
    raw = b"".join(pack(row) for row in rows)
    return {
        "rows": len(rows),
        "values_per_row": len(rows[0]) if rows else 0,
        "sha256": sha256_bytes(raw),
        "base64": base64.b64encode(raw).decode("ascii"),
    }


def decode_rows(record):
    raw = base64.b64decode(record["base64"], validate=True)
    if sha256_bytes(raw) != record["sha256"]:
        raise ValueError("packed witness hash mismatch")
    width = (2 * record["values_per_row"] + 7) // 8
    if len(raw) != record["rows"] * width:
        raise ValueError("packed witness payload length mismatch")
    return [unpack(raw[i * width : (i + 1) * width], record["values_per_row"])
            for i in range(record["rows"])]


def validate_row(n, edges, row, deleted):
    if len(row) != n - 1:
        raise ValueError("deletion row length mismatch")
    colors = []
    source = iter(row)
    for vertex in range(n):
        colors.append(-1 if vertex == deleted else next(source))
    if any(colors[u] == colors[v] for u, v in edges if u != deleted and v != deleted):
        raise ValueError(f"invalid deletion colouring at local vertex {deleted}")


def generate_rows(n, edges, deletions, solver_name):
    from pysat.solvers import Solver

    active_offset = n * K
    var = lambda v, c: v * K + c + 1
    active = lambda v: active_offset + v + 1
    clauses = [[-active(v)] + [var(v, c) for c in range(K)] for v in range(n)]
    clauses.extend([-active(u), -active(v), -var(u, c), -var(v, c)]
                   for u, v in edges for c in range(K))
    adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)

    def triangle_avoiding(deleted):
        for u, v in edges:
            if deleted in (u, v):
                continue
            common = adjacency[u] & adjacency[v]
            for w in sorted(common):
                if w != deleted:
                    return u, v, w
        raise ValueError("no surviving triangle")

    rows = []
    started = time.time()
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        for position, deleted in enumerate(deletions, 1):
            assumptions = [active(v) if v != deleted else -active(v) for v in range(n)]
            assumptions.extend(var(v, c) for c, v in enumerate(triangle_avoiding(deleted)))
            if not solver.solve(assumptions=assumptions):
                raise ValueError(f"expected deletion {deleted} to be 4-colourable")
            positive = {literal for literal in solver.get_model() if literal > 0}
            colors = [next(c for c in range(K) if var(v, c) in positive)
                      for v in range(n) if v != deleted]
            validate_row(n, edges, colors, deleted)
            rows.append(colors)
            if position % 50 == 0 or position == len(deletions):
                print(f"generated {position}/{len(deletions)} deletion rows in {time.time()-started:.1f}s", flush=True)
    return rows


def generate_subset_witnesses(edges, solver_name):
    """Color all A-subsets not containing both slots 1 and 3."""
    from pysat.solvers import Solver

    n = 513
    active_offset = n * K
    var = lambda v, c: v * K + c + 1
    active = lambda v: active_offset + v + 1
    clauses = [[-active(v)] + [var(v, c) for c in range(K)] for v in range(n)]
    clauses.extend([-active(u), -active(v), -var(u, c), -var(v, c)] for u, v in edges for c in range(K))
    parts = load_parts_module()
    triangle = parts.find_triangle(509, [(u, v) for u, v in edges if v < 509])
    clauses.extend([[var(v, c)] for c, v in enumerate(triangle)])
    records = []
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        for size in range(5):
            for subset in combinations(range(4), size):
                if 1 in subset and 3 in subset:
                    continue
                selected = set(subset)
                active_vertices = set(range(509)) - {A_DROP}
                active_vertices.update(509 + slot for slot in subset)
                assumptions = [active(v) if v in active_vertices else -active(v) for v in range(n)]
                if not solver.solve(assumptions=assumptions):
                    raise ValueError(f"expected A-subset {subset} to be 4-colourable")
                positive = {literal for literal in solver.get_model() if literal > 0}
                coloring = ["-"] * n
                for v in sorted(active_vertices):
                    coloring[v] = str(next(c for c in range(K) if var(v, c) in positive))
                if any(coloring[u] == coloring[v] for u, v in edges if u in active_vertices and v in active_vertices):
                    raise ValueError("invalid A-subset witness")
                records.append({"slots": list(subset), "q3_indices": [A_Q[i] for i in subset],
                                "coloring_on_A_full_order": "".join(coloring)})
    return records


def command_generate(output, solver_name):
    parts, _, graph = load_geometry()
    a_full_labels, _, a_full_edges = graph(A_Q)
    a_pair_labels, _, a_pair_edges = graph(PAIR_Q, A_DROP)
    b_full_labels, _, b_full_edges = graph(B_Q)
    assert len(a_full_edges) == 2459
    assert len(a_pair_edges) == 2445
    assert len(b_full_edges) == 2458

    print("A-pair: colouring all single-vertex deletions", flush=True)
    a_pair_rows = generate_rows(510, a_pair_edges, list(range(510)), solver_name)
    print("A-subsets: colouring every subset not containing the critical pair", flush=True)
    a_subset_rows = generate_subset_witnesses(a_full_edges, solver_name)
    print("B-full: colouring every base deletion", flush=True)
    b_full_rows = generate_rows(513, b_full_edges, list(range(509)), solver_name)

    certificate = {
        "format": "parts509-g14-augmentation-v1",
        "parts_coordinate_sha256": sha256_file(BASE / "parts509.vtx"),
        "completion_points_sha256": sha256_file(SWAP / "completion_points.json"),
        "packing": "two-bit colours, low bits first; rows concatenate in declared deletion order",
        "A_subset_profile": {
            "q3_indices": list(A_Q),
            "dropped_base_vertices": [A_DROP],
            "full_augmentation_vertices": len(a_full_labels),
            "full_augmentation_strict_edges": len(a_full_edges),
            "full_augmentation_edge_sha256": parts.edge_sha256(a_full_edges),
            "minimal_non_four_colorable_slots": [1, 3],
            "minimal_non_four_colorable_q3_indices": list(PAIR_Q),
            "four_colorable_subsets": a_subset_rows,
            "non_four_colorable_subsets": [[1, 3], [0, 1, 3], [1, 2, 3], [0, 1, 2, 3]],
        },
        "A_pair": {
            "q3_indices": list(PAIR_Q),
            "dropped_base_vertices": [A_DROP],
            "vertices": len(a_pair_labels),
            "strict_edges": len(a_pair_edges),
            "strict_edge_sha256": parts.edge_sha256(a_pair_edges),
            "local_vertex_order": a_pair_labels,
            "deletions": list(range(510)),
            "deletion_colorings": packed_rows(a_pair_rows),
        },
        "B_full": {
            "q3_indices": list(B_Q),
            "vertices": len(b_full_labels),
            "strict_edges": len(b_full_edges),
            "strict_edge_sha256": parts.edge_sha256(b_full_edges),
            "base_vertex_deletions_with_witnesses": list(range(509)),
            "repaired_base_vertices": [],
            "deletion_colorings": packed_rows(b_full_rows),
        },
    }
    output.write_text(json.dumps(certificate, sort_keys=True) + "\n")
    print(json.dumps({
        "certificate": str(output),
        "certificate_sha256": sha256_file(output),
        "A_pair_payload": certificate["A_pair"]["deletion_colorings"]["sha256"],
        "B_full_payload": certificate["B_full"]["deletion_colorings"]["sha256"],
    }, indent=2))


def verify_profile(name, record, labels, edges, deletions):
    parts = load_parts_module()
    if (record["vertices"] != len(labels) or record["strict_edges"] != len(edges)
            or record["strict_edge_sha256"] != parts.edge_sha256(edges)):
        raise ValueError(f"{name} size mismatch")
    rows = decode_rows(record["deletion_colorings"])
    if len(rows) != len(deletions):
        raise ValueError(f"{name} row count mismatch")
    for deleted, row in zip(deletions, rows):
        validate_row(len(labels), edges, row, deleted)
    return len(rows), sum(len(edges) - sum(deleted in edge for edge in edges) for deleted in deletions)


def command_verify(certificate_path):
    cert = json.loads(certificate_path.read_text())
    if cert.get("format") != "parts509-g14-augmentation-v1":
        raise ValueError("unexpected certificate format")
    if cert["parts_coordinate_sha256"] != sha256_file(BASE / "parts509.vtx"):
        raise ValueError("Parts coordinate hash mismatch")
    if cert["completion_points_sha256"] != sha256_file(SWAP / "completion_points.json"):
        raise ValueError("completion list hash mismatch")
    parts, completion, graph = load_geometry()
    a_full_labels, _, a_full_edges = graph(A_Q)
    a_pair_labels, _, a_pair_edges = graph(PAIR_Q, A_DROP)
    b_full_labels, _, b_full_edges = graph(B_Q)
    if cert["A_pair"]["local_vertex_order"] != a_pair_labels:
        raise ValueError("A-pair vertex order mismatch")
    if cert["B_full"]["repaired_base_vertices"]:
        raise ValueError("B repair declaration mismatch")

    a_pair_del = cert["A_pair"]["deletions"]
    b_full_del = cert["B_full"]["base_vertex_deletions_with_witnesses"]
    a_pair_checks = verify_profile("A_pair", cert["A_pair"], a_pair_labels, a_pair_edges, a_pair_del)
    b_full_checks = verify_profile("B_full", cert["B_full"], b_full_labels, b_full_edges, b_full_del)

    profile = cert["A_subset_profile"]
    if profile["minimal_non_four_colorable_q3_indices"] != list(PAIR_Q):
        raise ValueError("A minimal pair mismatch")
    if (profile["full_augmentation_vertices"] != len(a_full_labels)
            or profile["full_augmentation_strict_edges"] != len(a_full_edges)
            or profile["full_augmentation_edge_sha256"] != parts.edge_sha256(a_full_edges)):
        raise ValueError("A full augmentation mismatch")
    expected_sat = {subset for size in range(5) for subset in combinations(range(4), size)
                    if not (1 in subset and 3 in subset)}
    seen_sat = set()
    for row in profile["four_colorable_subsets"]:
        subset = tuple(row["slots"])
        if subset not in expected_sat or subset in seen_sat:
            raise ValueError("bad or repeated A-subset witness")
        seen_sat.add(subset)
        colors = row["coloring_on_A_full_order"]
        active = set(range(509)) - {A_DROP}
        active.update(509 + slot for slot in subset)
        if len(colors) != 513 or any((colors[v] == "-") != (v not in active) for v in range(513)):
            raise ValueError("A-subset activity mask mismatch")
        if any(colors[u] == colors[v] for u, v in a_full_edges if u in active and v in active):
            raise ValueError("invalid A-subset colouring")
    if seen_sat != expected_sat:
        raise ValueError("incomplete A-subset witnesses")
    expected_unsat = {subset for size in range(5) for subset in combinations(range(4), size)
                      if 1 in subset and 3 in subset}
    if {tuple(row) for row in profile["non_four_colorable_subsets"]} != expected_unsat:
        raise ValueError("A non-four-colourable subset declaration mismatch")

    # The Q3 indices and their full neighborhoods are checked from first principles.
    vpoints = parts.parse_points(BASE / "parts509.vtx")
    q_neighbors = {}
    for qid in sorted(set(A_Q + B_Q)):
        row = completion["points"][qid]
        point = kfield.from_strings(row["x"]), kfield.from_strings(row["y"])
        fresh = [v for v, candidate in enumerate(vpoints) if parts.squared_distance(point, candidate) == parts.ONE]
        if fresh != row["neighbors"]:
            raise ValueError(f"Q3 neighborhood mismatch at {qid}")
        q_neighbors[str(qid)] = fresh

    print(json.dumps({
        "all_checks": True,
        "A_subset_profile": {"four_colorable_subsets": len(seen_sat), "non_four_colorable_subsets": len(expected_unsat),
                             "minimal_non_four_colorable_q3_indices": list(PAIR_Q)},
        "A_pair": {"vertices": 510, "strict_edges": len(a_pair_edges), "deletion_colorings": a_pair_checks[0],
                   "retained_edge_checks": a_pair_checks[1], "vertex_criticality_upper_half": True},
        "B_full": {"vertices": 513, "strict_edges": len(b_full_edges), "base_deletion_colorings": b_full_checks[0],
                   "retained_edge_checks": b_full_checks[1], "repaired_base_vertices": []},
        "completion_neighborhoods": q_neighbors,
        "exact_distance_decisions": True,
    }, indent=2))


def command_cnf(output):
    if not str(output.resolve()).startswith("/scratch/"):
        raise ValueError("CNF output must be under /scratch")
    parts, _, graph = load_geometry()
    labels, _, edges = graph(PAIR_Q, A_DROP)
    clauses, triangle = parts.pinned_four_color_cnf(len(labels), edges)
    parts.write_dimacs(output, len(labels) * 4, clauses)
    print(json.dumps({"path": str(output), "vertices": len(labels), "edges": len(edges),
                      "variables": len(labels) * 4, "clauses": len(clauses),
                      "pinned_triangle": triangle, "sha256": sha256_file(output)}, indent=2))


def command_subsets(solver_name):
    """Discovery pass over all subsets of the four A-completion points."""
    from pysat.solvers import Solver

    parts, _, graph = load_geometry()
    labels, _, edges = graph(A_Q)
    n = len(labels)
    active_offset = n * K
    var = lambda v, c: v * K + c + 1
    active = lambda v: active_offset + v + 1
    clauses = [[-active(v)] + [var(v, c) for c in range(K)] for v in range(n)]
    clauses.extend([-active(u), -active(v), -var(u, c), -var(v, c)] for u, v in edges for c in range(K))
    triangle = parts.find_triangle(509, [(u, v) for u, v in edges if v < 509])
    clauses.extend([[var(v, c)] for c, v in enumerate(triangle)])
    results = []
    with Solver(name=solver_name, bootstrap_with=clauses) as solver:
        for size in range(5):
            for subset in combinations(range(4), size):
                selected = set(subset)
                assumptions = [-active(A_DROP)]
                assumptions.extend(active(v) for v in range(509) if v != A_DROP)
                assumptions.extend(active(509 + slot) if slot in selected else -active(509 + slot) for slot in range(4))
                started = time.time()
                sat = solver.solve(assumptions=assumptions)
                elapsed = time.time() - started
                if sat:
                    positive = {literal for literal in solver.get_model() if literal > 0}
                    active_vertices = [v for v in range(509) if v != A_DROP] + [509 + slot for slot in subset]
                    colors = {v: next(c for c in range(K) if var(v, c) in positive) for v in active_vertices}
                    if any(colors[u] == colors[v] for u, v in edges if u in colors and v in colors):
                        raise ValueError("solver returned an invalid subset colouring")
                row = {"slots": list(subset), "q3_indices": [A_Q[i] for i in subset],
                       "vertices": 508 + size, "four_colorable": sat, "seconds": round(elapsed, 3)}
                results.append(row)
                print(json.dumps(row), flush=True)
    print(json.dumps({"profile_complete": True, "results": results}, indent=2))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    generate = sub.add_parser("generate")
    generate.add_argument("output", type=Path)
    generate.add_argument("--solver", default="cadical195")
    verify = sub.add_parser("verify")
    verify.add_argument("certificate", type=Path, nargs="?", default=HERE / "certificate.json")
    cnf = sub.add_parser("cnf")
    cnf.add_argument("output", type=Path)
    subsets = sub.add_parser("subsets")
    subsets.add_argument("--solver", default="cadical195")
    args = parser.parse_args()
    if args.command == "generate":
        command_generate(args.output, args.solver)
    elif args.command == "verify":
        command_verify(args.certificate)
    elif args.command == "cnf":
        command_cnf(args.output)
    else:
        command_subsets(args.solver)


if __name__ == "__main__":
    main()
