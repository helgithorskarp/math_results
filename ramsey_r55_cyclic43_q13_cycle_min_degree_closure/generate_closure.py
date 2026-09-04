#!/usr/bin/env python3
"""Close the minimum-q13-degree cycle-only boundary seeds exactly."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter, deque
from pathlib import Path
from types import ModuleType


EXPECTED_BOUNDARY_SHA256 = "af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_fast_engine() -> tuple[ModuleType, ModuleType]:
    directory = Path(__file__).resolve().parents[1]
    closure_source = directory / "ramsey_r55_cyclic43_q13_small_support_closure" / "generate_closure.py"
    spec = importlib.util.spec_from_file_location("small_closure_generator", closure_source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {closure_source}")
    closure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(closure)
    return closure, closure.load_boundary_engine()


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=here / "closure_certificate.json")
    args = parser.parse_args()
    if digest(args.boundary) != EXPECTED_BOUNDARY_SHA256:
        raise AssertionError("unexpected parent boundary certificate hash")
    closure, engine = load_fast_engine()
    parent = json.loads(args.boundary.read_text())
    cycle_seeds = sorted(
        {
            engine.state_from_edges(item)
            for item in parent["target_states"]
            if engine.support_signature(engine.state_from_edges(item)) == ()
        },
        key=engine.state_key,
    )
    if len(cycle_seeds) != 1381:
        raise AssertionError(f"expected 1381 cycle-only seeds, found {len(cycle_seeds)}")

    degrees = {}
    started = time.monotonic()
    for number, state in enumerate(cycle_seeds, start=1):
        objective, moves = closure.objective_and_moves(engine, state)
        if objective != 13:
            raise AssertionError("cycle-only parent seed is not q=13")
        degrees[state] = sum(after == 13 for _, after in moves)
        if number % 250 == 0:
            print(
                f"seed_degrees={number}/{len(cycle_seeds)} "
                f"elapsed={time.monotonic() - started:.1f}s",
                flush=True,
            )
    seeds = {state for state in cycle_seeds if degrees[state] <= 2}
    if len(seeds) != 4 or Counter(degrees[state] for state in seeds) != Counter({1: 2, 2: 2}):
        raise AssertionError("unexpected minimum-degree seed set")

    reached = set(seeds)
    queue = deque(sorted(seeds, key=engine.state_key))
    move_data = {}
    while queue:
        source = queue.popleft()
        objective, raw_moves = closure.objective_and_moves(engine, source)
        if objective != 13:
            raise AssertionError("closure source is not q=13")
        moves = []
        for edge, after in raw_moves:
            target = None
            if after == 13 or after <= 12:
                target = engine.canonical_state(source ^ (1 << edge))
            moves.append((edge, after, target))
            if after == 13 and target not in reached:
                reached.add(target)
                queue.append(target)
        move_data[source] = moves
    states = sorted(reached, key=engine.state_key)
    if len(states) != 36:
        raise AssertionError(f"expected 36 q=13 states, found {len(states)}")
    claims, sublevel = closure.build_claims(engine, states, seeds, move_data)
    parent_in_closure = set(cycle_seeds) & set(states)
    claims.update(
        {
            "parent_cycle_seed_count": len(cycle_seeds),
            "parent_cycle_seed_q13_degree_histogram": closure.histogram(degrees.values()),
            "selected_seed_q13_degree_histogram": closure.histogram(
                degrees[state] for state in seeds
            ),
            "parent_cycle_seeds_in_closure": len(parent_in_closure),
            "closure_parent_seed_q13_degree_histogram": closure.histogram(
                degrees[state] for state in parent_in_closure
            ),
            "reflection_fixed_component_count": sum(
                left == right for left, right in claims["reflection_component_pairs"]
            ),
        }
    )
    certificate = {
        "format": "cyclic43-q13-cycle-minimum-degree-layer-closure-v1",
        "order": 43,
        "edge_count": 903,
        "canonicalization": "minimum tuple of 15 little-endian 64-bit toggle words over C_43 rotations",
        "scope": "complete q=13 layer components meeting all cycle-only A_12 exits of q13 degree at most two",
        "selection_rule": "among all 1381 cycle-only parent exits, retain exactly those with one or two q=13 flips",
        "parent_boundary_sha256": EXPECTED_BOUNDARY_SHA256,
        "seed_states": [engine.edges_from_state(state) for state in sorted(seeds, key=engine.state_key)],
        "q13_states": [engine.edges_from_state(state) for state in states],
        "sublevel_endpoint_states_by_objective": sublevel,
        "claims": claims,
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print("PASS generated exact minimum-degree cycle-only q=13 closure")
    print(
        f"parent_seeds={len(cycle_seeds)} selected={len(seeds)} "
        f"states={claims['state_count']} components={claims['component_count']}"
    )
    print(
        f"edges={claims['simple_internal_edges']} cycle_rank={claims['simple_cycle_rank']} "
        f"component_sizes={claims['component_size_histogram']}"
    )
    print(f"sublevel_targets={claims['distinct_sublevel_targets_by_objective']}")
    print(f"certificate_sha256={digest(args.output)}")


if __name__ == "__main__":
    main()
