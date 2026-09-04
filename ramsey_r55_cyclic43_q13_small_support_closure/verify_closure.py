#!/usr/bin/env python3
"""Independent verifier for the small-support Cyclic(43) q=13 closure.

This file imports neither the generator nor the earlier boundary engine.  It
uses explicit vertex triples for every flip delta and separately implements
the rotation quotient, reflection, graph traversal, and all certificate
summaries.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


N = 43
M = 903
SEED_DISTANCES = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}
EXPECTED_BOUNDARY_SHA256 = "af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85"
EXPECTED_Q6_SHA256 = "aea99967a1a3cc41c640c73c471a73b015259186619495ffa5223968cb48d320"
EXPECTED_Q8_SHA256 = "740c10a6cc72d148ce949749aa8d8f132aa70f9bb0b797ee3e2fbe5ba84fdc1a"
EDGES = list(itertools.combinations(range(N), 2))
EDGE_NUMBER = {pair: number for number, pair in enumerate(EDGES)}
EDGE_DISTANCE = [min(v - u, N - (v - u)) for u, v in EDGES]
FULL_VERTICES = (1 << N) - 1
SEED_RED = sum(1 << edge for edge, distance in enumerate(EDGE_DISTANCE) if distance in SEED_DISTANCES)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pack(edge_list: list[int]) -> int:
    if edge_list != sorted(set(edge_list)) or any(not 0 <= edge < M for edge in edge_list):
        raise AssertionError("malformed edge list")
    return sum(1 << edge for edge in edge_list)


def unpack(state: int) -> list[int]:
    return [edge for edge in range(M) if (state >> edge) & 1]


def words(state: int) -> tuple[int, ...]:
    mask = (1 << 64) - 1
    return tuple((state >> (64 * word)) & mask for word in range(15))


def rotated(state: int, amount: int) -> int:
    answer = 0
    for edge in unpack(state):
        u, v = EDGES[edge]
        u, v = (u + amount) % N, (v + amount) % N
        if u > v:
            u, v = v, u
        answer |= 1 << EDGE_NUMBER[u, v]
    return answer


def canonical(state: int) -> int:
    return min((rotated(state, amount) for amount in range(N)), key=words)


def reflected(state: int) -> int:
    answer = 0
    for edge in unpack(state):
        u, v = EDGES[edge]
        u, v = (-u) % N, (-v) % N
        if u > v:
            u, v = v, u
        answer |= 1 << EDGE_NUMBER[u, v]
    return canonical(answer)


def support(state: int) -> tuple[int, ...]:
    return tuple(sorted(EDGE_DISTANCE[edge] for edge in unpack(state) if EDGE_DISTANCE[edge] != 1))


def signature(state: int) -> str:
    values = support(state)
    return "cycle_only" if not values else ",".join(map(str, values))


def color_rows(state: int) -> tuple[list[int], list[int]]:
    red_mask = SEED_RED ^ state
    red = [0] * N
    for edge in unpack(red_mask):
        u, v = EDGES[edge]
        red[u] |= 1 << v
        red[v] |= 1 << u
    blue = []
    for vertex in range(N):
        blue.append((FULL_VERTICES ^ (1 << vertex)) & ~red[vertex])
    return red, blue


def count_cliques(rows: list[int], size: int) -> int:
    def visit(candidates: list[int], needed: int) -> int:
        if needed == 0:
            return 1
        if len(candidates) < needed:
            return 0
        total = 0
        for position, vertex in enumerate(candidates):
            later = [
                other
                for other in candidates[position + 1 :]
                if (rows[vertex] >> other) & 1
            ]
            total += visit(later, needed - 1)
        return total

    return visit(list(range(N)), size)


def explicit_triangles(rows: list[int], mask: int) -> int:
    vertices = [vertex for vertex in range(N) if (mask >> vertex) & 1]
    answer = 0
    for a, b, c in itertools.combinations(vertices, 3):
        if ((rows[a] >> b) & 1) and ((rows[a] >> c) & 1) and ((rows[b] >> c) & 1):
            answer += 1
    return answer


def histogram(values) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(value): counts[value] for value in sorted(counts, key=str)}


def scan_state(state: int) -> tuple[int, list[tuple[int, int, int | None]]]:
    red, blue = color_rows(state)
    objective = count_cliques(red, 5) + count_cliques(blue, 5)
    moves = []
    for edge, (u, v) in enumerate(EDGES):
        red_extensions = explicit_triangles(red, red[u] & red[v])
        blue_extensions = explicit_triangles(blue, blue[u] & blue[v])
        if (red[u] >> v) & 1:
            after = objective - red_extensions + blue_extensions
        else:
            after = objective + red_extensions - blue_extensions
        target = canonical(state ^ (1 << edge)) if after == 13 or after <= 12 else None
        moves.append((edge, after, target))
    return objective, moves


def components(states: list[int], graph: dict[int, set[int]]) -> list[list[int]]:
    unseen = set(states)
    answer = []
    while unseen:
        start = min(unseen, key=words)
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
        answer.append(sorted(part, key=words))
    answer.sort(key=lambda part: words(part[0]))
    return answer


def summarize(
    states: list[int],
    seeds: set[int],
    move_data: dict[int, list[tuple[int, int, int | None]]],
) -> tuple[dict[str, object], dict[str, list[list[int]]]]:
    state_set = set(states)
    directed: Counter[tuple[int, int]] = Counter()
    graph = {state: set() for state in states}
    all_objectives = Counter()
    boundary = Counter()
    minima = Counter()
    low: defaultdict[int, set[int]] = defaultdict(set)
    for source in states:
        minima[min(after for _, after, _ in move_data[source])] += 1
        for _, after, target in move_data[source]:
            all_objectives[after] += 1
            if after == 13:
                if target not in state_set:
                    raise AssertionError("certificate omits an objective-thirteen neighbour")
                directed[source, target] += 1
                graph[source].add(target)
            else:
                boundary[after] += 1
                if after <= 12:
                    assert target is not None
                    low[after].add(target)
    if any(source == target for source, target in directed):
        raise AssertionError("unexpected self-loop")
    for (source, target), multiplicity in directed.items():
        if directed[target, source] != multiplicity:
            raise AssertionError("asymmetric directed multiplicity")
    undirected = {
        (source, target): multiplicity
        for (source, target), multiplicity in directed.items()
        if words(source) < words(target)
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
        raise AssertionError("listed q=13 states are not exactly the seed closure")
    part_number = {state: number for number, part in enumerate(parts) for state in part}
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
        part_boundary = Counter()
        part_low: defaultdict[int, set[int]] = defaultdict(set)
        part_minima = Counter()
        for source in part:
            part_minima[min(after for _, after, _ in move_data[source])] += 1
            for _, after, target in move_data[source]:
                if after != 13:
                    part_boundary[after] += 1
                    if after <= 12:
                        assert target is not None
                        part_low[after].add(target)
        profiles.append(
            {
                "component_index": number,
                "representative_state_index": states.index(part[0]),
                "states": len(part),
                "input_seeds": len(part_set & seeds),
                "simple_internal_edges": simple_edges,
                "raw_internal_edges": raw_edges,
                "simple_cycle_rank": simple_edges - len(part) + 1,
                "multigraph_cycle_rank": raw_edges - len(part) + 1,
                "support_signature_histogram": histogram(signature(state) for state in part),
                "minimum_neighbor_objective_histogram": histogram(part_minima),
                "boundary_directed_incidence_by_objective": histogram(part_boundary),
                "distinct_sublevel_targets_by_objective": {
                    str(objective): len(part_low[objective]) for objective in sorted(part_low)
                },
            }
        )
    reflection = {state: reflected(state) for state in states}
    if not set(reflection.values()) <= state_set:
        raise AssertionError("reflection leaves the closure")
    reflection_pairs = sorted(
        {tuple(sorted((part_number[state], part_number[target]))) for state, target in reflection.items()}
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
        "support_signature_histogram": histogram(signature(state) for state in states),
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
            str(objective): len(low[objective]) for objective in sorted(low)
        },
        "reflection_component_pairs": [list(pair) for pair in reflection_pairs],
        "reflection_fixed_state_count": sum(state == target for state, target in reflection.items()),
        "dihedral_state_orbit_count": sum(words(state) <= words(target) for state, target in reflection.items()),
    }
    encoded_low = {
        str(objective): [unpack(state) for state in sorted(targets, key=words)]
        for objective, targets in sorted(low.items())
    }
    return claims, encoded_low


def verify_primary_membership(
    certificate: dict[str, object], q6_path: Path, q8_path: Path
) -> None:
    if digest(q6_path) != EXPECTED_Q6_SHA256 or digest(q8_path) != EXPECTED_Q8_SHA256:
        raise AssertionError("unexpected primary-component input hash")
    q6 = json.loads(q6_path.read_text())["objective_six_rotation_representatives"]
    q8 = json.loads(q8_path.read_text())["objective_eight_component_rotation_representatives"]
    primary = {"6": [pack(item) for item in q6], "8": [pack(item) for item in q8]}
    membership = certificate["primary_anchor_membership"]
    expected = {
        "objective_six_source_sha256": EXPECTED_Q6_SHA256,
        "objective_eight_source_sha256": EXPECTED_Q8_SHA256,
        "endpoint_indices_in_source_order": {},
        "all_objective_six_endpoints_in_primary_component": True,
        "all_objective_eight_endpoints_in_primary_component": True,
    }
    for objective in ("6", "8"):
        positions = {state: number for number, state in enumerate(primary[objective])}
        endpoints = [pack(item) for item in certificate["sublevel_endpoint_states_by_objective"][objective]]
        if not set(endpoints) <= set(primary[objective]):
            raise AssertionError(f"q={objective} endpoint is not in the primary certificate")
        expected["endpoint_indices_in_source_order"][objective] = [positions[state] for state in endpoints]
    if membership != expected:
        raise AssertionError("primary anchor membership payload mismatch")


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("boundary", type=Path)
    parser.add_argument("primary_q6", type=Path)
    parser.add_argument("primary_q8", type=Path)
    parser.add_argument("certificate", type=Path, nargs="?", default=here / "closure_certificate.json")
    args = parser.parse_args()
    if digest(args.boundary) != EXPECTED_BOUNDARY_SHA256:
        raise AssertionError("unexpected parent boundary hash")
    document = json.loads(args.certificate.read_text())
    boundary = json.loads(args.boundary.read_text())
    expected_seeds = {
        pack(item)
        for item in boundary["target_states"]
        if support(pack(item)) in {(17, 21), (17, 17, 21)}
    }
    seeds = {pack(item) for item in document["seed_states"]}
    states = [pack(item) for item in document["q13_states"]]
    if seeds != expected_seeds or len(seeds) != 18:
        raise AssertionError("seed set does not match the parent boundary")
    if states != sorted(set(states), key=words) or len(states) != 150:
        raise AssertionError("q=13 state list is not 150 distinct states in canonical order")
    move_data = {}
    for number, state in enumerate(states):
        if canonical(state) != state:
            raise AssertionError(f"state {number} is not canonical")
        if len({rotated(state, amount) for amount in range(N)}) != N:
            raise AssertionError(f"state {number} does not have a free C_43 orbit")
        objective, moves = scan_state(state)
        if objective != 13:
            raise AssertionError(f"state {number} has objective {objective}")
        move_data[state] = moves
    claims, low = summarize(states, seeds, move_data)
    if claims != document["claims"]:
        raise AssertionError("claim payload mismatch")
    if low != document["sublevel_endpoint_states_by_objective"]:
        raise AssertionError("complete sublevel endpoint payload mismatch")
    verify_primary_membership(document, args.primary_q6, args.primary_q8)
    expected_header = {
        "format": "cyclic43-q13-small-support-layer-closure-v1",
        "order": N,
        "edge_count": M,
        "canonicalization": "minimum tuple of 15 little-endian 64-bit toggle words over C_43 rotations",
        "scope": "the complete q=13 layer components meeting the 18 {17,21}/{17,17,21} exits of A_12",
        "parent_boundary_sha256": EXPECTED_BOUNDARY_SHA256,
    }
    for key, value in expected_header.items():
        if document.get(key) != value:
            raise AssertionError(f"header mismatch at {key}")
    print("PASS independently verified the complete small-support q=13 layer closure")
    print(
        f"states={claims['state_count']} components={claims['component_count']} "
        f"edges={claims['simple_internal_edges']} cycle_rank={claims['simple_cycle_rank']}"
    )
    print(f"component_sizes={claims['component_size_histogram']}")
    print(f"sublevel_targets={claims['distinct_sublevel_targets_by_objective']}")
    print(f"certificate_sha256={digest(args.certificate)}")


if __name__ == "__main__":
    main()
