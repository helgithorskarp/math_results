#!/usr/bin/env python3
"""Try every L deletion from the exact 574-point pool obstruction.

SAT answers are decoded and checked directly before being saved. An UNSAT
answer is only a construction-search signal until separately proof-checked.
"""
from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import time
from pathlib import Path

from pysat.solvers import Solver

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PARENT = REPO / "hadwiger_nelson_parts509_pool_obstruction574"
GEOMETRY = (REPO /
    "hadwiger_nelson_parts509_pool_shape6_review1/independent_check.py")


def pack(word: str) -> str:
    raw = bytearray((len(word) + 3) // 4)
    for i, character in enumerate(word):
        colour = ord(character) - ord("0")
        if colour not in range(4):
            raise ValueError("colour outside 0,...,3")
        raw[i // 4] |= colour << (2 * (i % 4))
    return base64.b64encode(raw).decode()


def write_json(path: Path, value) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)


def load_graph():
    certificate = json.loads((PARENT / "certificate.json").read_text())
    spec = importlib.util.spec_from_file_location("exact_geometry", GEOMETRY)
    geometry = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(geometry)
    _, points, _, _, all_edges = geometry.read_geometry()
    labels = list(range(374)) + certificate["pool_labels"]
    selected = set(labels)
    if len(labels) != 574 or len({points[v] for v in labels}) != 574:
        raise ValueError("parent graph labels or exact points changed")
    edges = [(a, b) for a, b in all_edges
             if a in selected and b in selected]
    if len(edges) != 2707:
        raise ValueError("parent graph edge count changed")
    return labels, edges


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    labels, label_edges = load_graph()
    position = {v: i for i, v in enumerate(labels)}
    edges = [(position[a], position[b]) for a, b in label_edges]
    n = len(labels)
    act = lambda i: i + 1
    colour = lambda i, c: n + 4 * i + c + 1
    clauses = [[-act(i)] + [colour(i, c) for c in range(4)]
               for i in range(n)]
    clauses += [[-act(a), -act(b), -colour(a, c), -colour(b, c)]
                for a, b in edges for c in range(4)]
    for label, c in ((0, 0), (149, 1), (152, 2)):
        clauses.append([colour(position[label], c)])

    result = {
        "schema": "parts574-L-indispensability-search-v1",
        "parent_vertices": 574,
        "parent_edges": 2707,
        "tested_deletion_domain": list(range(374)),
        "colourings": [],
        "provisional_nonfour_deletions": [],
        "status": "searching",
    }
    started = time.time()
    with Solver(name="cadical195", bootstrap_with=clauses,
                use_timer=True) as solver:
        for removed in range(374):
            assumptions = [act(i) for i, label in enumerate(labels)
                           if label != removed]
            solve_started = time.time()
            answer = solver.solve(assumptions=assumptions)
            elapsed = time.time() - solve_started
            if answer is False:
                result["provisional_nonfour_deletions"].append({
                    "removed": removed,
                    "wall_seconds": elapsed,
                    "note": "UNSAT search signal; independent proof required",
                })
                result["status"] = "provisional_smaller_seed_found"
                write_json(args.output, result)
                print(json.dumps(result["provisional_nonfour_deletions"][-1]),
                      flush=True)
                return
            if answer is not True:
                result["status"] = "unknown"
                write_json(args.output, result)
                return
            positive = {literal for literal in solver.get_model()
                        if literal > 0}
            active_labels = [label for label in labels if label != removed]
            word = []
            decoded = {}
            for label in active_labels:
                i = position[label]
                hits = [c for c in range(4) if colour(i, c) in positive]
                if not hits:
                    raise ValueError("model did not supply a colour")
                # The standard colouring CNF needs at least one colour rather
                # than exactly one. Adjacent colour sets are disjoint, so
                # choosing the least true colour preserves propriety.
                decoded[label] = min(hits)
                word.append(str(decoded[label]))
            if not all(decoded[a] != decoded[b] for a, b in label_edges
                       if removed not in (a, b)):
                raise ValueError("decoded colouring failed an exact edge")
            result["colourings"].append({
                "removed": removed,
                "colouring_2bit": pack("".join(word)),
                "wall_seconds": elapsed,
            })
            result["elapsed_seconds"] = time.time() - started
            result["native_solver_seconds"] = solver.time_accum()
            if removed % 25 == 24:
                write_json(args.output, result)
                print(json.dumps({
                    "removed_through": removed,
                    "colourings": len(result["colourings"]),
                    "elapsed_seconds": result["elapsed_seconds"],
                    "native_solver_seconds": result["native_solver_seconds"],
                }), flush=True)
    result["status"] = "all_L_single_deletions_four_colourable"
    write_json(args.output, result)
    print(json.dumps({
        "status": result["status"],
        "colourings": len(result["colourings"]),
        "elapsed_seconds": result["elapsed_seconds"],
        "native_solver_seconds": result["native_solver_seconds"],
    }), flush=True)


if __name__ == "__main__":
    main()
