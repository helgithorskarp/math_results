#!/usr/bin/env python3
"""Generate the exact q=13 closure of the {5,16}/{5,16,16} exit family."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from collections import Counter, defaultdict, deque
from pathlib import Path
from types import ModuleType


N = 43
M = 903
EXPECTED_BOUNDARY_SHA256 = "af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85"
SEED_SIGNATURES = {(5, 16), (5, 16, 16)}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_boundary_engine() -> ModuleType:
    source = (
        Path(__file__).resolve().parents[1]
        / "ramsey_r55_cyclic43_q13_boundary_certificate"
        / "generate_boundary.py"
    )
    spec = importlib.util.spec_from_file_location("cyclic43_boundary_engine", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def histogram(values) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(value): counts[value] for value in sorted(counts, key=str)}


def signature_name(engine: ModuleType, state: int) -> str:
    values = engine.support_signature(state)
    return "cycle_only" if not values else ",".join(map(str, values))


def objective_and_moves(engine: ModuleType, state: int) -> tuple[int, list[tuple[int, int]]]:
    red, blue = engine.adjacency(engine.SEED_RED_MASK ^ state)
    objective = engine.clique_count(red, 5) + engine.clique_count(blue, 5)
    moves = []
    for edge, (u, v) in enumerate(engine.EDGES):
        red_extensions = engine.triangle_count(red, red[u] & red[v])
        blue_extensions = engine.triangle_count(blue, blue[u] & blue[v])
        after = (
            objective - red_extensions + blue_extensions
            if (red[u] >> v) & 1
            else objective + red_extensions - blue_extensions
        )
        moves.append((edge, after))
    return objective, moves


def reflected_state(engine: ModuleType, state: int) -> int:
    answer = 0
    for edge in engine.edges_from_state(state):
        u, v = engine.EDGES[edge]
        u, v = (-u) % N, (-v) % N
        if u > v:
            u, v = v, u
        answer |= 1 << engine.EDGE_ID[u][v]
    return engine.canonical_state(answer)


def find_components(
    states: list[int], graph: dict[int, set[int]], engine: ModuleType
) -> list[list[int]]:
    unseen = set(states)
    components = []
    while unseen:
        start = min(unseen, key=engine.state_key)
        unseen.remove(start)
        queue = deque([start])
        component = []
        while queue:
            state = queue.popleft()
            component.append(state)
            for target in graph[state]:
                if target in unseen:
                    unseen.remove(target)
                    queue.append(target)
        components.append(sorted(component, key=engine.state_key))
    components.sort(key=lambda component: engine.state_key(component[0]))
    return components


def build_claims(
    engine: ModuleType,
    states: list[int],
    seeds: set[int],
    internal: dict[int, Counter[int]],
    objective_counts: dict[int, Counter[int]],
    low_targets: dict[int, dict[int, set[int]]],
) -> tuple[dict[str, object], dict[str, list[list[int]]]]:
    state_set = set(states)
    graph = {state: set(internal[state]) for state in states}
    for source in states:
        for target, multiplicity in internal[source].items():
            if target not in state_set:
                raise AssertionError("q=13 closure is not closed")
            if source == target:
                raise AssertionError("unexpected self-loop")
            if internal[target][source] != multiplicity:
                raise AssertionError("directed quotient multiplicities are asymmetric")
    undirected = {
        (source, target): multiplicity
        for source in states
        for target, multiplicity in internal[source].items()
        if engine.state_key(source) < engine.state_key(target)
    }
    components = find_components(states, graph, engine)
    component_index = {
        state: number for number, component in enumerate(components) for state in component
    }
    state_index = {state: number for number, state in enumerate(states)}

    profiles = []
    for number, component in enumerate(components):
        component_set = set(component)
        simple_edges = sum(
            1 for source, target in undirected if source in component_set and target in component_set
        )
        raw_edges = sum(
            multiplicity
            for (source, target), multiplicity in undirected.items()
            if source in component_set and target in component_set
        )
        boundary = Counter()
        minima = Counter()
        distinct_low: defaultdict[int, set[int]] = defaultdict(set)
        for source in component:
            counts = objective_counts[source]
            minima[min(counts)] += 1
            boundary.update({objective: count for objective, count in counts.items() if objective != 13})
            for objective, targets in low_targets[source].items():
                distinct_low[objective].update(targets)
        profiles.append(
            {
                "component_index": number,
                "representative_state_index": state_index[component[0]],
                "states": len(component),
                "input_seeds": len(component_set & seeds),
                "simple_internal_edges": simple_edges,
                "raw_internal_edges": raw_edges,
                "simple_cycle_rank": simple_edges - len(component) + 1,
                "multigraph_cycle_rank": raw_edges - len(component) + 1,
                "support_signature_histogram": histogram(
                    signature_name(engine, state) for state in component
                ),
                "minimum_neighbor_objective_histogram": histogram(minima),
                "boundary_directed_incidence_by_objective": histogram(boundary),
                "distinct_sublevel_targets_by_objective": {
                    str(objective): len(distinct_low[objective])
                    for objective in sorted(distinct_low)
                },
            }
        )

    all_moves = Counter()
    boundary = Counter()
    minima = Counter()
    global_low: defaultdict[int, set[int]] = defaultdict(set)
    for state in states:
        all_moves.update(objective_counts[state])
        minima[min(objective_counts[state])] += 1
        boundary.update(
            {objective: count for objective, count in objective_counts[state].items() if objective != 13}
        )
        for objective, targets in low_targets[state].items():
            global_low[objective].update(targets)

    reflection = {state: reflected_state(engine, state) for state in states}
    if not set(reflection.values()) <= state_set:
        raise AssertionError("reflection leaves the closure")
    reflection_pairs = sorted(
        {
            tuple(sorted((component_index[state], component_index[target])))
            for state, target in reflection.items()
        }
    )
    simple_edges = len(undirected)
    raw_edges = sum(undirected.values())
    claims = {
        "input_seed_count": len(seeds),
        "state_count": len(states),
        "component_count": len(components),
        "component_size_histogram": histogram(len(component) for component in components),
        "component_profiles": profiles,
        "support_signature_histogram": histogram(
            signature_name(engine, state) for state in states
        ),
        "all_flip_objective_histogram": histogram(all_moves),
        "boundary_directed_incidence_by_objective": histogram(boundary),
        "minimum_neighbor_objective_histogram": histogram(minima),
        "internal_directed_incidences": sum(sum(counts.values()) for counts in internal.values()),
        "simple_internal_edges": simple_edges,
        "raw_internal_edges": raw_edges,
        "simple_cycle_rank": simple_edges - len(states) + len(components),
        "multigraph_cycle_rank": raw_edges - len(states) + len(components),
        "directed_pair_multiplicity_histogram": histogram(
            multiplicity for counts in internal.values() for multiplicity in counts.values()
        ),
        "distinct_sublevel_targets_by_objective": {
            str(objective): len(global_low[objective]) for objective in sorted(global_low)
        },
        "reflection_component_pairs": [list(pair) for pair in reflection_pairs],
        "reflection_fixed_state_count": sum(state == target for state, target in reflection.items()),
        "reflection_fixed_component_count": sum(left == right for left, right in reflection_pairs),
        "dihedral_state_orbit_count": sum(
            engine.state_key(state) <= engine.state_key(target)
            for state, target in reflection.items()
        ),
    }
    encoded_low = {
        str(objective): [
            engine.edges_from_state(state)
            for state in sorted(targets, key=engine.state_key)
        ]
        for objective, targets in sorted(global_low.items())
    }
    return claims, encoded_low


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=here / "closure_certificate.json")
    args = parser.parse_args()
    if digest(args.boundary) != EXPECTED_BOUNDARY_SHA256:
        raise AssertionError("unexpected parent boundary certificate hash")
    engine = load_boundary_engine()
    parent = json.loads(args.boundary.read_text())
    seeds = {
        engine.state_from_edges(item)
        for item in parent["target_states"]
        if engine.support_signature(engine.state_from_edges(item)) in SEED_SIGNATURES
    }
    if len(seeds) != 386:
        raise AssertionError(f"expected 386 medium-support seeds, found {len(seeds)}")

    reached = set(seeds)
    queue = deque(sorted(seeds, key=engine.state_key))
    internal: dict[int, Counter[int]] = {}
    objective_counts: dict[int, Counter[int]] = {}
    low_targets: dict[int, dict[int, set[int]]] = {}
    started = time.monotonic()
    processed = 0
    while queue:
        source = queue.popleft()
        objective, moves = objective_and_moves(engine, source)
        if objective != 13:
            raise AssertionError("closure source does not have objective thirteen")
        source_internal = Counter()
        source_objectives = Counter()
        source_low: defaultdict[int, set[int]] = defaultdict(set)
        for edge, after in moves:
            source_objectives[after] += 1
            if after == 13 or after <= 12:
                target = engine.canonical_state(source ^ (1 << edge))
                if after == 13:
                    source_internal[target] += 1
                    if target not in reached:
                        reached.add(target)
                        queue.append(target)
                else:
                    source_low[after].add(target)
        internal[source] = source_internal
        objective_counts[source] = source_objectives
        low_targets[source] = dict(source_low)
        processed += 1
        if processed % 500 == 0:
            print(
                f"processed={processed} reached={len(reached)} queue={len(queue)} "
                f"elapsed={time.monotonic() - started:.1f}s",
                flush=True,
            )
    states = sorted(reached, key=engine.state_key)
    if len(states) != 6279:
        raise AssertionError(f"expected 6279 q=13 states, found {len(states)}")
    claims, sublevel = build_claims(
        engine, states, seeds, internal, objective_counts, low_targets
    )
    certificate = {
        "format": "cyclic43-q13-medium-support-layer-closure-v1",
        "order": N,
        "edge_count": M,
        "canonicalization": "minimum tuple of 15 little-endian 64-bit toggle words over C_43 rotations",
        "scope": "complete q=13 layer components meeting the 386 {5,16}/{5,16,16} exits of A_12",
        "parent_boundary_sha256": EXPECTED_BOUNDARY_SHA256,
        "seed_states": [
            engine.edges_from_state(state) for state in sorted(seeds, key=engine.state_key)
        ],
        "q13_states": [engine.edges_from_state(state) for state in states],
        "sublevel_endpoint_states_by_objective": sublevel,
        "claims": claims,
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print("PASS generated exact medium-support q=13 layer closure")
    print(
        f"states={claims['state_count']} components={claims['component_count']} "
        f"edges={claims['simple_internal_edges']} cycle_rank={claims['simple_cycle_rank']}"
    )
    print(f"component_sizes={claims['component_size_histogram']}")
    print(f"sublevel_targets={claims['distinct_sublevel_targets_by_objective']}")
    print(f"certificate_sha256={digest(args.output)}")


if __name__ == "__main__":
    main()
