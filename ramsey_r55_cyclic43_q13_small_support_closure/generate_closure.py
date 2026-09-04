#!/usr/bin/env python3
"""Generate the exact small-support Cyclic(43) q=13 layer closure.

The starting set is selected from the independently certified q=13 exits of
the 238-state threshold-twelve addition: precisely the exits whose non-unit
cyclic support is {17,21} or {17,17,21}.  We exhaust every one-edge move that
stays at objective thirteen, and record the complete lower boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path
from types import ModuleType


N = 43
M = 903
EXPECTED_BOUNDARY_SHA256 = "af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85"
EXPECTED_Q6_SHA256 = "aea99967a1a3cc41c640c73c471a73b015259186619495ffa5223968cb48d320"
EXPECTED_Q8_SHA256 = "740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a"


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
    """Return the objective and exact objective after each of the 903 flips."""
    red, blue = engine.adjacency(engine.SEED_RED_MASK ^ state)
    objective = engine.clique_count(red, 5) + engine.clique_count(blue, 5)
    moves = []
    for edge, (u, v) in enumerate(engine.EDGES):
        red_extensions = engine.triangle_count(red, red[u] & red[v])
        blue_extensions = engine.triangle_count(blue, blue[u] & blue[v])
        if (red[u] >> v) & 1:
            after = objective - red_extensions + blue_extensions
        else:
            after = objective + red_extensions - blue_extensions
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


def connected_components(states: list[int], graph: dict[int, set[int]], engine: ModuleType) -> list[list[int]]:
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
    move_data: dict[int, list[tuple[int, int, int | None]]],
) -> tuple[dict[str, object], dict[str, list[list[int]]]]:
    state_set = set(states)
    internal_multiplicity: Counter[tuple[int, int]] = Counter()
    graph = {state: set() for state in states}
    all_move_objectives: Counter[int] = Counter()
    minimum_objectives: Counter[int] = Counter()
    sublevel_targets: defaultdict[int, set[int]] = defaultdict(set)
    boundary_objectives: Counter[int] = Counter()

    for source in states:
        moves = move_data[source]
        minimum_objectives[min(after for _, after, _ in moves)] += 1
        for _, after, target in moves:
            all_move_objectives[after] += 1
            if after == 13:
                assert target is not None and target in state_set
                internal_multiplicity[source, target] += 1
                graph[source].add(target)
            else:
                boundary_objectives[after] += 1
                if after <= 12:
                    assert target is not None
                    sublevel_targets[after].add(target)

    if any(source == target for source, target in internal_multiplicity):
        raise AssertionError("unexpected q=13 self-loop in quotient")
    for (source, target), multiplicity in internal_multiplicity.items():
        if internal_multiplicity[target, source] != multiplicity:
            raise AssertionError("directed q=13 quotient multiplicities are not symmetric")
    undirected = {
        (source, target): multiplicity
        for (source, target), multiplicity in internal_multiplicity.items()
        if engine.state_key(source) < engine.state_key(target)
    }
    components = connected_components(states, graph, engine)
    component_index = {
        state: number for number, component in enumerate(components) for state in component
    }

    profiles = []
    for number, component in enumerate(components):
        component_set = set(component)
        edges = sum(
            1
            for source, target in undirected
            if source in component_set and target in component_set
        )
        raw_edges = sum(
            multiplicity
            for (source, target), multiplicity in undirected.items()
            if source in component_set and target in component_set
        )
        boundary = Counter()
        low_distinct: defaultdict[int, set[int]] = defaultdict(set)
        source_minimum = Counter()
        for source in component:
            moves = move_data[source]
            source_minimum[min(after for _, after, _ in moves)] += 1
            for _, after, target in moves:
                if after != 13:
                    boundary[after] += 1
                    if after <= 12:
                        assert target is not None
                        low_distinct[after].add(target)
        profiles.append(
            {
                "component_index": number,
                "representative_state_index": states.index(component[0]),
                "states": len(component),
                "input_seeds": len(component_set & seeds),
                "simple_internal_edges": edges,
                "raw_internal_edges": raw_edges,
                "simple_cycle_rank": edges - len(component) + 1,
                "multigraph_cycle_rank": raw_edges - len(component) + 1,
                "support_signature_histogram": histogram(
                    signature_name(engine, state) for state in component
                ),
                "minimum_neighbor_objective_histogram": histogram(source_minimum),
                "boundary_directed_incidence_by_objective": histogram(boundary),
                "distinct_sublevel_targets_by_objective": {
                    str(objective): len(low_distinct[objective])
                    for objective in sorted(low_distinct)
                },
            }
        )

    reflection_image = {}
    reflection_fixed_states = 0
    for state in states:
        image = reflected_state(engine, state)
        if image not in state_set:
            raise AssertionError("reflection leaves the q=13 closure")
        reflection_image[state] = image
        reflection_fixed_states += image == state
    reflection_pairs = sorted(
        {
            tuple(sorted((component_index[state], component_index[image])))
            for state, image in reflection_image.items()
        }
    )
    if any(a == b for a, b in reflection_pairs):
        raise AssertionError("a q=13 component is fixed by reflection")

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
        "all_flip_objective_histogram": histogram(all_move_objectives),
        "boundary_directed_incidence_by_objective": histogram(boundary_objectives),
        "minimum_neighbor_objective_histogram": histogram(minimum_objectives),
        "internal_directed_incidences": sum(internal_multiplicity.values()),
        "simple_internal_edges": simple_edges,
        "raw_internal_edges": raw_edges,
        "simple_cycle_rank": simple_edges - len(states) + len(components),
        "multigraph_cycle_rank": raw_edges - len(states) + len(components),
        "directed_pair_multiplicity_histogram": histogram(internal_multiplicity.values()),
        "distinct_sublevel_targets_by_objective": {
            str(objective): len(sublevel_targets[objective])
            for objective in sorted(sublevel_targets)
        },
        "reflection_component_pairs": [list(pair) for pair in reflection_pairs],
        "reflection_fixed_state_count": reflection_fixed_states,
        "dihedral_state_orbit_count": sum(
            1
            for state in states
            if engine.state_key(state) <= engine.state_key(reflection_image[state])
        ),
    }
    encoded_sublevel = {
        str(objective): [engine.edges_from_state(state) for state in sorted(targets, key=engine.state_key)]
        for objective, targets in sorted(sublevel_targets.items())
    }
    return claims, encoded_sublevel


def upstream_membership(
    engine: ModuleType,
    sublevel: dict[str, list[list[int]]],
    q6_path: Path,
    q8_path: Path,
) -> dict[str, object]:
    if digest(q6_path) != EXPECTED_Q6_SHA256:
        raise AssertionError("unexpected objective-six certificate hash")
    if digest(q8_path) != EXPECTED_Q8_SHA256:
        raise AssertionError("unexpected objective-eight certificate hash")
    q6_document = json.loads(q6_path.read_text())
    q8_document = json.loads(q8_path.read_text())
    q6_representatives = [
        engine.state_from_edges(item)
        for item in q6_document["objective_six_rotation_representatives"]
    ]
    q8_representatives = [
        engine.state_from_edges(item)
        for item in q8_document["objective_eight_component_rotation_representatives"]
    ]
    indices = {}
    for objective, representatives in (("6", q6_representatives), ("8", q8_representatives)):
        position = {state: number for number, state in enumerate(representatives)}
        endpoints = [engine.state_from_edges(item) for item in sublevel[objective]]
        missing = [state for state in endpoints if state not in position]
        if missing:
            raise AssertionError(f"q={objective} endpoint absent from primary component certificate")
        indices[objective] = [position[state] for state in endpoints]
    return {
        "objective_six_source_sha256": EXPECTED_Q6_SHA256,
        "objective_eight_source_sha256": EXPECTED_Q8_SHA256,
        "endpoint_indices_in_source_order": indices,
        "all_objective_six_endpoints_in_primary_component": True,
        "all_objective_eight_endpoints_in_primary_component": True,
    }


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", type=Path)
    parser.add_argument("primary_q6", type=Path)
    parser.add_argument("primary_q8", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=here / "closure_certificate.json")
    args = parser.parse_args()
    if digest(args.boundary) != EXPECTED_BOUNDARY_SHA256:
        raise AssertionError("unexpected parent boundary certificate hash")

    engine = load_boundary_engine()
    boundary = json.loads(args.boundary.read_text())
    boundary_targets = [engine.state_from_edges(item) for item in boundary["target_states"]]
    seeds = {
        state
        for state in boundary_targets
        if engine.support_signature(state) in {(17, 21), (17, 17, 21)}
    }
    if len(seeds) != 18:
        raise AssertionError(f"expected 18 small-support seeds, found {len(seeds)}")

    reached = set(seeds)
    queue = deque(sorted(seeds, key=engine.state_key))
    move_data: dict[int, list[tuple[int, int, int | None]]] = {}
    while queue:
        source = queue.popleft()
        objective, raw_moves = objective_and_moves(engine, source)
        if objective != 13:
            raise AssertionError("closure source does not have objective thirteen")
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
    if len(states) != 150:
        raise AssertionError(f"expected 150 q=13 states, found {len(states)}")
    claims, sublevel = build_claims(engine, states, seeds, move_data)
    membership = upstream_membership(engine, sublevel, args.primary_q6, args.primary_q8)
    certificate = {
        "format": "cyclic43-q13-small-support-layer-closure-v1",
        "order": N,
        "edge_count": M,
        "canonicalization": "minimum tuple of 15 little-endian 64-bit toggle words over C_43 rotations",
        "scope": "the complete q=13 layer components meeting the 18 {17,21}/{17,17,21} exits of A_12",
        "parent_boundary_sha256": EXPECTED_BOUNDARY_SHA256,
        "seed_states": [engine.edges_from_state(state) for state in sorted(seeds, key=engine.state_key)],
        "q13_states": [engine.edges_from_state(state) for state in states],
        "sublevel_endpoint_states_by_objective": sublevel,
        "primary_anchor_membership": membership,
        "claims": claims,
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print("PASS generated exact small-support q=13 layer closure")
    print(
        f"states={claims['state_count']} components={claims['component_count']} "
        f"edges={claims['simple_internal_edges']} cycle_rank={claims['simple_cycle_rank']}"
    )
    print(f"component_sizes={claims['component_size_histogram']}")
    print(f"sublevel_targets={claims['distinct_sublevel_targets_by_objective']}")
    print(f"certificate_sha256={digest(args.output)}")


if __name__ == "__main__":
    main()
