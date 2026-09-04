#!/usr/bin/env python3
"""Independently verify the minimum-degree cycle-only q=13 components."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter
from pathlib import Path
from types import ModuleType


EXPECTED_BOUNDARY_SHA256 = "af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_independent_tools() -> tuple[ModuleType, ModuleType]:
    directory = Path(__file__).resolve().parents[1]
    source = directory / "ramsey_r55_cyclic43_q13_medium_support_closure" / "verify_closure.py"
    spec = importlib.util.spec_from_file_location("medium_closure_verifier", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {source}")
    tools = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tools)
    return tools, tools.load_independent_engine()


def q13_degree(tools: ModuleType, engine: ModuleType, state: int) -> tuple[int, int]:
    red, blue = engine.color_rows(state)
    objective = engine.count_cliques(red, 5) + engine.count_cliques(blue, 5)
    degree = 0
    for u, v in engine.EDGES:
        r = tools.edge_common_triangle_count(red, red[u] & red[v])
        b = tools.edge_common_triangle_count(blue, blue[u] & blue[v])
        after = objective - r + b if (red[u] >> v) & 1 else objective + r - b
        degree += after == 13
    return objective, degree


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", type=Path)
    parser.add_argument("certificate", type=Path, nargs="?", default=here / "closure_certificate.json")
    args = parser.parse_args()
    if digest(args.boundary) != EXPECTED_BOUNDARY_SHA256:
        raise AssertionError("unexpected parent boundary hash")
    tools, engine = load_independent_tools()
    parent = json.loads(args.boundary.read_text())
    document = json.loads(args.certificate.read_text())
    cycle_seeds = sorted(
        {
            engine.pack(item)
            for item in parent["target_states"]
            if engine.support(engine.pack(item)) == ()
        },
        key=engine.words,
    )
    if len(cycle_seeds) != 1381:
        raise AssertionError("parent does not contain 1381 cycle-only exits")
    degrees = {}
    started = time.monotonic()
    for number, state in enumerate(cycle_seeds, start=1):
        objective, degree = q13_degree(tools, engine, state)
        if objective != 13:
            raise AssertionError("parent cycle-only exit is not q=13")
        degrees[state] = degree
        if number % 250 == 0:
            print(
                f"verified_seed_degrees={number}/{len(cycle_seeds)} "
                f"elapsed={time.monotonic() - started:.1f}s",
                flush=True,
            )
    selected = {state for state in cycle_seeds if degrees[state] <= 2}
    stored_seeds = {engine.pack(item) for item in document["seed_states"]}
    if selected != stored_seeds or Counter(degrees[state] for state in selected) != Counter({1: 2, 2: 2}):
        raise AssertionError("certificate seed set does not match the exact degree criterion")

    states = [engine.pack(item) for item in document["q13_states"]]
    if states != sorted(set(states), key=engine.words) or len(states) != 36:
        raise AssertionError("q=13 state list is malformed")
    internal = {}
    objective_counts = {}
    low_targets = {}
    for number, state in enumerate(states):
        if tools.canonical_state(engine, state) != state:
            raise AssertionError(f"state {number} is not canonical")
        edges = tools.set_edges(state)
        if len({tools.rotate_edge_list(engine, edges, amount) for amount in range(43)}) != 43:
            raise AssertionError(f"state {number} has a nonfree orbit")
        objective, counts, inside, low = tools.scan_state(engine, state)
        if objective != 13:
            raise AssertionError(f"state {number} has objective {objective}")
        internal[state] = inside
        objective_counts[state] = counts
        low_targets[state] = low
    claims, sublevel = tools.summarize(
        engine, states, selected, internal, objective_counts, low_targets
    )
    parent_in_closure = set(cycle_seeds) & set(states)
    claims.update(
        {
            "parent_cycle_seed_count": len(cycle_seeds),
            "parent_cycle_seed_q13_degree_histogram": tools.histogram(degrees.values()),
            "selected_seed_q13_degree_histogram": tools.histogram(
                degrees[state] for state in selected
            ),
            "parent_cycle_seeds_in_closure": len(parent_in_closure),
            "closure_parent_seed_q13_degree_histogram": tools.histogram(
                degrees[state] for state in parent_in_closure
            ),
        }
    )
    if claims != document["claims"]:
        raise AssertionError("claim payload mismatch")
    if sublevel != document["sublevel_endpoint_states_by_objective"]:
        raise AssertionError("sublevel endpoint payload mismatch")
    expected_header = {
        "format": "cyclic43-q13-cycle-minimum-degree-layer-closure-v1",
        "order": 43,
        "edge_count": 903,
        "canonicalization": "minimum tuple of 15 little-endian 64-bit toggle words over C_43 rotations",
        "scope": "complete q=13 layer components meeting all cycle-only A_12 exits of q13 degree at most two",
        "selection_rule": "among all 1381 cycle-only parent exits, retain exactly those with one or two q=13 flips",
        "parent_boundary_sha256": EXPECTED_BOUNDARY_SHA256,
    }
    for key, value in expected_header.items():
        if document.get(key) != value:
            raise AssertionError(f"header mismatch at {key}")
    print("PASS independently verified all minimum-degree cycle-only q=13 components")
    print(
        f"parent_seeds={len(cycle_seeds)} selected={len(selected)} "
        f"states={claims['state_count']} components={claims['component_count']}"
    )
    print(
        f"edges={claims['simple_internal_edges']} cycle_rank={claims['simple_cycle_rank']} "
        f"component_sizes={claims['component_size_histogram']}"
    )
    print(f"sublevel_targets={claims['distinct_sublevel_targets_by_objective']}")
    print(f"certificate_sha256={digest(args.certificate)}")


if __name__ == "__main__":
    main()
