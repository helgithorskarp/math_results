#!/usr/bin/env python3
"""Clean-room checker for the Cyclic(43) small-support q=13 closure.

Unlike the reviewed generator and verifier, this checker enumerates all
five-vertex subsets and tracks their ten red-edge counts directly.  A flip
destroys a monochromatic K5 exactly when its count is 0 or 10, and creates
one exactly when its count is 1 or 9 and the minority edge is flipped.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import platform
import resource
import time
from array import array
from collections import Counter, defaultdict, deque
from pathlib import Path


N = 43
M = math.comb(N, 2)
Q = 13
SEED_DISTANCES = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}
EXPECTED_CLOSURE_SHA256 = "85e271af8ebbd55c8bf8e6ad033122911f750a13dc95f638d74681f8c03e4d1e"
EXPECTED_BOUNDARY_SHA256 = "af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85"
EXPECTED_Q6_SHA256 = "aea99967a1a3cc41c640c73c471a73b015259186619495ffa5223968cb48d320"
EXPECTED_Q8_SHA256 = "740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a"

EDGES = list(itertools.combinations(range(N), 2))
EDGE_ID = {edge: number for number, edge in enumerate(EDGES)}
EDGE_DISTANCE = [min(v - u, N - (v - u)) for u, v in EDGES]
SEED_RED = sum(
    1 << edge for edge, distance in enumerate(EDGE_DISTANCE) if distance in SEED_DISTANCES
)
SEED_EDGE_RED = tuple(bool((SEED_RED >> edge) & 1) for edge in range(M))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise AssertionError(f"{label} hash {actual}, expected {expected}")


def pack(edges: list[int]) -> int:
    if edges != sorted(set(edges)) or any(not 0 <= edge < M for edge in edges):
        raise AssertionError("malformed toggle-edge list")
    return sum(1 << edge for edge in edges)


def unpack(state: int) -> list[int]:
    answer: list[int] = []
    while state:
        bit = state & -state
        answer.append(bit.bit_length() - 1)
        state ^= bit
    return answer


def word_key(state: int) -> tuple[int, ...]:
    mask = (1 << 64) - 1
    return tuple((state >> (64 * index)) & mask for index in range(15))


def edge_permutation(vertex_map) -> tuple[int, ...]:
    image = []
    for u, v in EDGES:
        a, b = vertex_map(u), vertex_map(v)
        if a > b:
            a, b = b, a
        image.append(EDGE_ID[a, b])
    if sorted(image) != list(range(M)):
        raise AssertionError("edge image is not a permutation")
    return tuple(image)


ROTATIONS = tuple(
    edge_permutation(lambda vertex, shift=shift: (vertex + shift) % N)
    for shift in range(N)
)
REFLECTION = edge_permutation(lambda vertex: (-vertex) % N)


def permute(state: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    while state:
        bit = state & -state
        answer |= 1 << permutation[bit.bit_length() - 1]
        state ^= bit
    return answer


def canonical(state: int) -> int:
    return min((permute(state, rotation) for rotation in ROTATIONS), key=word_key)


def reflected(state: int) -> int:
    return canonical(permute(state, REFLECTION))


def support_signature(state: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            EDGE_DISTANCE[edge]
            for edge in unpack(state)
            if EDGE_DISTANCE[edge] != 1
        )
    )


def signature_name(state: int) -> str:
    values = support_signature(state)
    return "cycle_only" if not values else ",".join(map(str, values))


def histogram(values) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(value): counts[value] for value in sorted(counts, key=str)}


def build_five_sets() -> tuple[bytearray, array, list[array]]:
    """Return seed red counts, flat edge IDs, and edge-to-K5 incidence."""
    seed_counts = bytearray()
    flat_edges = array("H")
    incidence = [array("I") for _ in range(M)]
    for vertices in itertools.combinations(range(N), 5):
        clique_edges = [EDGE_ID[edge] for edge in itertools.combinations(vertices, 2)]
        clique_number = len(seed_counts)
        seed_counts.append(sum(SEED_EDGE_RED[edge] for edge in clique_edges))
        flat_edges.extend(clique_edges)
        for edge in clique_edges:
            incidence[edge].append(clique_number)
    if len(seed_counts) != math.comb(N, 5) or len(flat_edges) != 10 * len(seed_counts):
        raise AssertionError("incomplete five-set table")
    expected_incidence = math.comb(N - 2, 3)
    if any(len(entries) != expected_incidence for entries in incidence):
        raise AssertionError("incorrect edge-to-five-set incidence")
    return seed_counts, flat_edges, incidence


def add_pattern_effect(
    red_count: int,
    offset: int,
    flat_edges: array,
    red_mask: int,
    deltas: list[int],
) -> int:
    """Apply one K5's flip effects; return 1 iff it is monochromatic."""
    if red_count in (0, 10):
        for position in range(offset, offset + 10):
            deltas[flat_edges[position]] -= 1
        return 1
    if red_count in (1, 9):
        seek_red = red_count == 1
        minority = -1
        for position in range(offset, offset + 10):
            edge = flat_edges[position]
            if bool((red_mask >> edge) & 1) == seek_red:
                if minority != -1:
                    raise AssertionError("non-unique minority edge")
                minority = edge
        if minority == -1:
            raise AssertionError("missing minority edge")
        deltas[minority] += 1
    return 0


def self_test(flat_edges: array) -> None:
    local_edges = array("H", range(10))
    for count, red_mask, expected_q, expected_delta in (
        (0, 0, 1, [-1] * 10),
        (10, (1 << 10) - 1, 1, [-1] * 10),
        (1, 1 << 3, 0, [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]),
        (9, ((1 << 10) - 1) ^ (1 << 7), 0, [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]),
        (5, sum(1 << edge for edge in range(5)), 0, [0] * 10),
    ):
        deltas = [0] * 10
        q = add_pattern_effect(count, 0, local_edges, red_mask, deltas)
        if q != expected_q or deltas != expected_delta:
            raise AssertionError("local K5 flip identity failed")
    state = (1 << 0) | (1 << 137) | (1 << 902)
    images = {permute(state, rotation) for rotation in ROTATIONS}
    if len(images) != N or {canonical(image) for image in images} != {canonical(state)}:
        raise AssertionError("rotation canonicalization self-test failed")
    if reflected(reflected(state)) != canonical(state):
        raise AssertionError("reflection self-test failed")
    if flat_edges.typecode != "H":
        raise AssertionError("unexpected packed edge type")


def positions(data: bytearray, value: int):
    needle = bytes((value,))
    position = data.find(needle)
    while position != -1:
        yield position
        position = data.find(needle, position + 1)


def scan_state(
    state: int,
    seed_counts: bytearray,
    flat_edges: array,
    incidence: list[array],
) -> tuple[int, bytearray]:
    counts = seed_counts.copy()
    for edge in unpack(state):
        step = -1 if SEED_EDGE_RED[edge] else 1
        for clique_number in incidence[edge]:
            counts[clique_number] += step
    red_mask = SEED_RED ^ state
    deltas = [0] * M
    objective = 0
    for red_count in (0, 1, 9, 10):
        for clique_number in positions(counts, red_count):
            objective += add_pattern_effect(
                red_count, 10 * clique_number, flat_edges, red_mask, deltas
            )
    after = bytearray(objective + delta for delta in deltas)
    return objective, after


def components(states: list[int], graph: dict[int, set[int]]) -> list[list[int]]:
    unseen = set(states)
    answer: list[list[int]] = []
    while unseen:
        start = min(unseen, key=word_key)
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
        answer.append(sorted(component, key=word_key))
    return sorted(answer, key=lambda component: word_key(component[0]))


def summarize(
    states: list[int],
    seeds: set[int],
    objectives: dict[int, bytearray],
    targets: dict[tuple[int, int], int],
) -> tuple[dict[str, object], dict[str, list[list[int]]]]:
    state_set = set(states)
    directed: Counter[tuple[int, int]] = Counter()
    graph = {state: set() for state in states}
    all_objectives = Counter()
    boundary = Counter()
    minima = Counter()
    low: defaultdict[int, set[int]] = defaultdict(set)
    for source in states:
        minima[min(objectives[source])] += 1
        for edge, after in enumerate(objectives[source]):
            all_objectives[after] += 1
            if after == Q:
                target = targets[source, edge]
                if target not in state_set:
                    raise AssertionError("certificate omits a q=13 neighbor")
                directed[source, target] += 1
                graph[source].add(target)
            else:
                boundary[after] += 1
                if after < Q:
                    low[after].add(targets[source, edge])
    if any(source == target for source, target in directed):
        raise AssertionError("unexpected quotient self-loop")
    for (source, target), multiplicity in directed.items():
        if directed[target, source] != multiplicity:
            raise AssertionError("asymmetric directed multiplicity")
    undirected = {
        (source, target): multiplicity
        for (source, target), multiplicity in directed.items()
        if word_key(source) < word_key(target)
    }
    parts = components(states, graph)
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
    part_index = {state: number for number, part in enumerate(parts) for state in part}
    state_position = {state: number for number, state in enumerate(states)}
    profiles = []
    for number, part in enumerate(parts):
        part_set = set(part)
        simple_edges = sum(
            source in part_set and target in part_set for source, target in undirected
        )
        raw_edges = sum(
            multiplicity
            for (source, target), multiplicity in undirected.items()
            if source in part_set and target in part_set
        )
        part_boundary = Counter()
        part_low: defaultdict[int, set[int]] = defaultdict(set)
        part_minima = Counter()
        for source in part:
            part_minima[min(objectives[source])] += 1
            for edge, after in enumerate(objectives[source]):
                if after != Q:
                    part_boundary[after] += 1
                    if after < Q:
                        part_low[after].add(targets[source, edge])
        profiles.append(
            {
                "component_index": number,
                "representative_state_index": state_position[part[0]],
                "states": len(part),
                "input_seeds": len(part_set & seeds),
                "simple_internal_edges": simple_edges,
                "raw_internal_edges": raw_edges,
                "simple_cycle_rank": simple_edges - len(part) + 1,
                "multigraph_cycle_rank": raw_edges - len(part) + 1,
                "support_signature_histogram": histogram(signature_name(state) for state in part),
                "minimum_neighbor_objective_histogram": histogram(part_minima),
                "boundary_directed_incidence_by_objective": histogram(part_boundary),
                "distinct_sublevel_targets_by_objective": {
                    str(value): len(part_low[value]) for value in sorted(part_low)
                },
            }
        )
    reflection = {state: reflected(state) for state in states}
    if not set(reflection.values()) <= state_set:
        raise AssertionError("reflection leaves the closure")
    reflection_pairs = sorted(
        {
            tuple(sorted((part_index[state], part_index[target])))
            for state, target in reflection.items()
        }
    )
    if any(left == right for left, right in reflection_pairs):
        raise AssertionError("reflection unexpectedly fixes a component")
    simple_edges = len(undirected)
    raw_edges = sum(undirected.values())
    claims = {
        "input_seed_count": len(seeds),
        "state_count": len(states),
        "component_count": len(parts),
        "component_size_histogram": histogram(len(part) for part in parts),
        "component_profiles": profiles,
        "support_signature_histogram": histogram(signature_name(state) for state in states),
        "all_flip_objective_histogram": histogram(all_objectives),
        "boundary_directed_incidence_by_objective": histogram(boundary),
        "minimum_neighbor_objective_histogram": histogram(minima),
        "internal_directed_incidences": sum(directed.values()),
        "simple_internal_edges": simple_edges,
        "raw_internal_edges": raw_edges,
        "simple_cycle_rank": simple_edges - len(states) + len(parts),
        "multigraph_cycle_rank": raw_edges - len(states) + len(parts),
        "directed_pair_multiplicity_histogram": histogram(directed.values()),
        "distinct_sublevel_targets_by_objective": {
            str(value): len(low[value]) for value in sorted(low)
        },
        "reflection_component_pairs": [list(pair) for pair in reflection_pairs],
        "reflection_fixed_state_count": sum(
            state == target for state, target in reflection.items()
        ),
        "dihedral_state_orbit_count": sum(
            word_key(state) <= word_key(target) for state, target in reflection.items()
        ),
    }
    encoded_low = {
        str(value): [unpack(state) for state in sorted(low[value], key=word_key)]
        for value in sorted(low)
    }
    return claims, encoded_low


def verify_primary_membership(document: dict, q6_path: Path, q8_path: Path) -> None:
    checked_hash(q6_path, EXPECTED_Q6_SHA256, "q=6 input")
    checked_hash(q8_path, EXPECTED_Q8_SHA256, "q=8 input")
    q6 = json.loads(q6_path.read_text())["objective_six_rotation_representatives"]
    q8 = json.loads(q8_path.read_text())["objective_eight_component_rotation_representatives"]
    membership = document["primary_anchor_membership"]
    expected = {
        "objective_six_source_sha256": EXPECTED_Q6_SHA256,
        "objective_eight_source_sha256": EXPECTED_Q8_SHA256,
        "endpoint_indices_in_source_order": {},
        "all_objective_six_endpoints_in_primary_component": True,
        "all_objective_eight_endpoints_in_primary_component": True,
    }
    for value, source in (("6", q6), ("8", q8)):
        source_states = [pack(edges) for edges in source]
        positions_by_state = {state: index for index, state in enumerate(source_states)}
        endpoints = [
            pack(edges) for edges in document["sublevel_endpoint_states_by_objective"][value]
        ]
        if not set(endpoints) <= set(source_states):
            raise AssertionError(f"q={value} endpoint absent from pinned primary array")
        expected["endpoint_indices_in_source_order"][value] = [
            positions_by_state[state] for state in endpoints
        ]
    if membership != expected:
        raise AssertionError("primary membership payload mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("closure", type=Path)
    parser.add_argument("boundary", type=Path)
    parser.add_argument("primary_q6", type=Path)
    parser.add_argument("primary_q8", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    checked_hash(args.closure, EXPECTED_CLOSURE_SHA256, "closure certificate")
    checked_hash(args.boundary, EXPECTED_BOUNDARY_SHA256, "parent boundary")
    document = json.loads(args.closure.read_text())
    boundary = json.loads(args.boundary.read_text())
    seed_counts, flat_edges, incidence = build_five_sets()
    self_test(flat_edges)
    seeds = {pack(edges) for edges in document["seed_states"]}
    expected_seeds = {
        pack(edges)
        for edges in boundary["target_states"]
        if support_signature(pack(edges)) in {(17, 21), (17, 17, 21)}
    }
    if seeds != expected_seeds or len(seeds) != 18:
        raise AssertionError("seed set differs from the selected parent-boundary states")
    states = [pack(edges) for edges in document["q13_states"]]
    if states != sorted(set(states), key=word_key) or len(states) != 150:
        raise AssertionError("state list is not 150 distinct canonical-order states")
    objectives: dict[int, bytearray] = {}
    targets: dict[tuple[int, int], int] = {}
    for state in states:
        if canonical(state) != state:
            raise AssertionError("noncanonical listed state")
        if len({permute(state, rotation) for rotation in ROTATIONS}) != N:
            raise AssertionError("non-free listed C_43 orbit")
        objective, after = scan_state(state, seed_counts, flat_edges, incidence)
        if objective != Q:
            raise AssertionError(f"listed state has objective {objective}")
        objectives[state] = after
        for edge, target_objective in enumerate(after):
            if target_objective <= Q:
                targets[state, edge] = canonical(state ^ (1 << edge))
    claims, low = summarize(states, seeds, objectives, targets)
    if claims != document["claims"]:
        raise AssertionError("reconstructed claim dictionary differs from certificate")
    if low != document["sublevel_endpoint_states_by_objective"]:
        raise AssertionError("reconstructed sublevel payload differs entry-by-entry")
    verify_primary_membership(document, args.primary_q6, args.primary_q8)
    elapsed = time.monotonic() - started
    print("PASS clean-room five-subset verification of small-support q=13 closure")
    print(f"python={platform.python_version()} five_sets={len(seed_counts)} cpu_processes=1")
    print(
        f"states={claims['state_count']} components={claims['component_count']} "
        f"edges={claims['simple_internal_edges']} cycle_rank={claims['simple_cycle_rank']}"
    )
    print(f"component_sizes={claims['component_size_histogram']}")
    print(f"sublevel_targets={claims['distinct_sublevel_targets_by_objective']}")
    print(f"closure_sha256={sha256(args.closure)}")
    print(f"peak_rss_kib={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
    print(f"elapsed_seconds={elapsed:.3f}")


if __name__ == "__main__":
    main()
