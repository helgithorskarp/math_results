#!/usr/bin/env python3
"""Independent verifier for the 6,279-state medium-support q=13 closure.

The graph/color/rotation engine comes from the previously published standalone
explicit checker, not from the generator.  Here triangle counts use a second
identity: sum, over induced edges, the number of common induced neighbours and
divide by three.  The verifier streams the 5.67 million flips into compact
per-source summaries before independently rebuilding every certificate claim.
"""

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


def load_independent_engine() -> ModuleType:
    source = (
        Path(__file__).resolve().parents[1]
        / "ramsey_r55_cyclic43_q13_small_support_closure"
        / "verify_closure.py"
    )
    spec = importlib.util.spec_from_file_location("cyclic43_independent_engine", source)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import {source}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def histogram(values) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(value): counts[value] for value in sorted(counts, key=str)}


def set_edges(state: int) -> list[int]:
    edges = []
    remaining = state
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        edges.append(bit.bit_length() - 1)
    return edges


def rotate_edge_list(engine: ModuleType, edges: list[int], amount: int) -> int:
    answer = 0
    for edge in edges:
        u, v = engine.EDGES[edge]
        u, v = (u + amount) % N, (v + amount) % N
        if u > v:
            u, v = v, u
        answer |= 1 << engine.EDGE_NUMBER[u, v]
    return answer


def canonical_state(engine: ModuleType, state: int) -> int:
    edges = set_edges(state)
    return min(
        (rotate_edge_list(engine, edges, amount) for amount in range(N)),
        key=engine.words,
    )


def reflected_state(engine: ModuleType, state: int) -> int:
    answer = 0
    for edge in set_edges(state):
        u, v = engine.EDGES[edge]
        u, v = (-u) % N, (-v) % N
        if u > v:
            u, v = v, u
        answer |= 1 << engine.EDGE_NUMBER[u, v]
    return canonical_state(engine, answer)


def edge_common_triangle_count(rows: list[int], mask: int) -> int:
    """Count triangles as one third of edge/common-neighbour incidences."""
    total = 0
    remaining = mask
    while remaining:
        bit = remaining & -remaining
        remaining ^= bit
        a = bit.bit_length() - 1
        later_neighbours = rows[a] & remaining
        while later_neighbours:
            b_bit = later_neighbours & -later_neighbours
            later_neighbours ^= b_bit
            b = b_bit.bit_length() - 1
            total += (rows[a] & rows[b] & mask).bit_count()
    if total % 3:
        raise AssertionError("triangle incidence count is not divisible by three")
    return total // 3


def scan_state(engine: ModuleType, state: int) -> tuple[int, Counter[int], Counter[int], dict[int, set[int]]]:
    red, blue = engine.color_rows(state)
    objective = engine.count_cliques(red, 5) + engine.count_cliques(blue, 5)
    objective_counts = Counter()
    internal = Counter()
    low: defaultdict[int, set[int]] = defaultdict(set)
    for edge, (u, v) in enumerate(engine.EDGES):
        red_extensions = edge_common_triangle_count(red, red[u] & red[v])
        blue_extensions = edge_common_triangle_count(blue, blue[u] & blue[v])
        after = (
            objective - red_extensions + blue_extensions
            if (red[u] >> v) & 1
            else objective + red_extensions - blue_extensions
        )
        objective_counts[after] += 1
        if after == 13 or after <= 12:
            target = canonical_state(engine, state ^ (1 << edge))
            if after == 13:
                internal[target] += 1
            else:
                low[after].add(target)
    return objective, objective_counts, internal, dict(low)


def find_components(
    states: list[int], graph: dict[int, set[int]], engine: ModuleType
) -> list[list[int]]:
    unseen = set(states)
    parts = []
    while unseen:
        start = min(unseen, key=engine.words)
        unseen.remove(start)
        queue = deque([start])
        part = []
        while queue:
            state = queue.popleft()
            part.append(state)
            for target in graph[state]:
                if target in unseen:
                    unseen.remove(target)
                    queue.append(target)
        parts.append(sorted(part, key=engine.words))
    parts.sort(key=lambda part: engine.words(part[0]))
    return parts


def summarize(
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
                raise AssertionError("certificate omits an objective-thirteen neighbour")
            if source == target:
                raise AssertionError("unexpected self-loop")
            if internal[target][source] != multiplicity:
                raise AssertionError("asymmetric quotient multiplicity")
    reached = set(seeds)
    queue = deque(seeds)
    while queue:
        source = queue.popleft()
        for target in graph[source]:
            if target not in reached:
                reached.add(target)
                queue.append(target)
    if reached != state_set:
        raise AssertionError("listed states are not exactly the q=13 seed closure")
    undirected = {
        (source, target): multiplicity
        for source in states
        for target, multiplicity in internal[source].items()
        if engine.words(source) < engine.words(target)
    }
    parts = find_components(states, graph, engine)
    part_number = {state: number for number, part in enumerate(parts) for state in part}
    state_number = {state: number for number, state in enumerate(states)}
    profiles = []
    for number, part in enumerate(parts):
        part_set = set(part)
        simple_edges = sum(
            1 for source, target in undirected if source in part_set and target in part_set
        )
        raw_edges = sum(
            multiplicity
            for (source, target), multiplicity in undirected.items()
            if source in part_set and target in part_set
        )
        boundary = Counter()
        minima = Counter()
        distinct_low: defaultdict[int, set[int]] = defaultdict(set)
        for source in part:
            counts = objective_counts[source]
            minima[min(counts)] += 1
            boundary.update({objective: count for objective, count in counts.items() if objective != 13})
            for objective, targets in low_targets[source].items():
                distinct_low[objective].update(targets)
        profiles.append(
            {
                "component_index": number,
                "representative_state_index": state_number[part[0]],
                "states": len(part),
                "input_seeds": len(part_set & seeds),
                "simple_internal_edges": simple_edges,
                "raw_internal_edges": raw_edges,
                "simple_cycle_rank": simple_edges - len(part) + 1,
                "multigraph_cycle_rank": raw_edges - len(part) + 1,
                "support_signature_histogram": histogram(engine.signature(state) for state in part),
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
    pairs = sorted(
        {tuple(sorted((part_number[state], part_number[target]))) for state, target in reflection.items()}
    )
    simple_edges = len(undirected)
    raw_edges = sum(undirected.values())
    claims = {
        "input_seed_count": len(seeds),
        "state_count": len(states),
        "component_count": len(parts),
        "component_size_histogram": histogram(len(part) for part in parts),
        "component_profiles": profiles,
        "support_signature_histogram": histogram(engine.signature(state) for state in states),
        "all_flip_objective_histogram": histogram(all_moves),
        "boundary_directed_incidence_by_objective": histogram(boundary),
        "minimum_neighbor_objective_histogram": histogram(minima),
        "internal_directed_incidences": sum(sum(counts.values()) for counts in internal.values()),
        "simple_internal_edges": simple_edges,
        "raw_internal_edges": raw_edges,
        "simple_cycle_rank": simple_edges - len(states) + len(parts),
        "multigraph_cycle_rank": raw_edges - len(states) + len(parts),
        "directed_pair_multiplicity_histogram": histogram(
            multiplicity for counts in internal.values() for multiplicity in counts.values()
        ),
        "distinct_sublevel_targets_by_objective": {
            str(objective): len(global_low[objective]) for objective in sorted(global_low)
        },
        "reflection_component_pairs": [list(pair) for pair in pairs],
        "reflection_fixed_state_count": sum(state == target for state, target in reflection.items()),
        "reflection_fixed_component_count": sum(left == right for left, right in pairs),
        "dihedral_state_orbit_count": sum(
            engine.words(state) <= engine.words(target) for state, target in reflection.items()
        ),
    }
    encoded_low = {
        str(objective): [engine.unpack(state) for state in sorted(targets, key=engine.words)]
        for objective, targets in sorted(global_low.items())
    }
    return claims, encoded_low


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", type=Path)
    parser.add_argument("certificate", type=Path, nargs="?", default=here / "closure_certificate.json")
    args = parser.parse_args()
    if digest(args.boundary) != EXPECTED_BOUNDARY_SHA256:
        raise AssertionError("unexpected parent boundary hash")
    engine = load_independent_engine()
    parent = json.loads(args.boundary.read_text())
    document = json.loads(args.certificate.read_text())
    expected_seeds = {
        engine.pack(item)
        for item in parent["target_states"]
        if engine.support(engine.pack(item)) in SEED_SIGNATURES
    }
    seeds = {engine.pack(item) for item in document["seed_states"]}
    states = [engine.pack(item) for item in document["q13_states"]]
    if seeds != expected_seeds or len(seeds) != 386:
        raise AssertionError("seed set does not match the parent boundary")
    if states != sorted(set(states), key=engine.words) or len(states) != 6279:
        raise AssertionError("q=13 state list is malformed")
    state_set = set(states)
    if not seeds <= state_set:
        raise AssertionError("seed is absent from state list")
    internal = {}
    objective_counts = {}
    low_targets = {}
    started = time.monotonic()
    for number, state in enumerate(states, start=1):
        if canonical_state(engine, state) != state:
            raise AssertionError(f"state {number - 1} is not canonical")
        edges = set_edges(state)
        if len({rotate_edge_list(engine, edges, amount) for amount in range(N)}) != N:
            raise AssertionError(f"state {number - 1} has a nonfree orbit")
        objective, counts, inside, low = scan_state(engine, state)
        if objective != 13:
            raise AssertionError(f"state {number - 1} has objective {objective}")
        internal[state] = inside
        objective_counts[state] = counts
        low_targets[state] = low
        if number % 250 == 0:
            print(
                f"verified={number}/{len(states)} elapsed={time.monotonic() - started:.1f}s",
                flush=True,
            )
    claims, sublevel = summarize(
        engine, states, seeds, internal, objective_counts, low_targets
    )
    if claims != document["claims"]:
        raise AssertionError("claim payload mismatch")
    if sublevel != document["sublevel_endpoint_states_by_objective"]:
        raise AssertionError("complete sublevel endpoint payload mismatch")
    expected_header = {
        "format": "cyclic43-q13-medium-support-layer-closure-v1",
        "order": N,
        "edge_count": M,
        "canonicalization": "minimum tuple of 15 little-endian 64-bit toggle words over C_43 rotations",
        "scope": "complete q=13 layer components meeting the 386 {5,16}/{5,16,16} exits of A_12",
        "parent_boundary_sha256": EXPECTED_BOUNDARY_SHA256,
    }
    for key, value in expected_header.items():
        if document.get(key) != value:
            raise AssertionError(f"header mismatch at {key}")
    print("PASS independently verified the complete medium-support q=13 layer closure")
    print(
        f"states={claims['state_count']} components={claims['component_count']} "
        f"edges={claims['simple_internal_edges']} cycle_rank={claims['simple_cycle_rank']}"
    )
    print(f"component_sizes={claims['component_size_histogram']}")
    print(f"sublevel_targets={claims['distinct_sublevel_targets_by_objective']}")
    print(f"certificate_sha256={digest(args.certificate)}")


if __name__ == "__main__":
    main()
