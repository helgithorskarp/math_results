#!/usr/bin/env python3
"""Clean-room all-five-subsets check of the Cyclic(43) q=13 boundary.

The reviewed programs count triangles in common-color neighborhoods.  This
checker instead enumerates all 962,598 five-vertex sets and tracks their ten
edge colors directly.  It reconstructs every certified source, target,
incidence multiplicity, component profile, and aggregate claim.
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
FIVE_SET_COUNT = math.comb(N, 5)
SEED_DISTANCES = {1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21}
EXPECTED_SOURCE_SHA256 = "4803b2e40dba06c0f82c3d23cbd5ae0a9127da0db24e5655971fff179fb68ec3"
EXPECTED_CERTIFICATE_SHA256 = "af8b6892049ace5610e2d7cea4c8642f39f53634287474127990aca0abbe2b85"

EDGES = list(itertools.combinations(range(N), 2))
EDGE_ID = {edge: number for number, edge in enumerate(EDGES)}
EDGE_DISTANCE = [min(v - u, N - (v - u)) for u, v in EDGES]
SEED_RED = sum(
    1 << edge for edge, distance in enumerate(EDGE_DISTANCE)
    if distance in SEED_DISTANCES
)
SEED_EDGE_RED = tuple(bool((SEED_RED >> edge) & 1) for edge in range(M))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def edge_permutation(shift: int) -> tuple[int, ...]:
    image = []
    for u, v in EDGES:
        a, b = (u + shift) % N, (v + shift) % N
        if a > b:
            a, b = b, a
        image.append(EDGE_ID[a, b])
    if sorted(image) != list(range(M)):
        raise AssertionError("rotation is not an edge permutation")
    return tuple(image)


ROTATIONS = tuple(edge_permutation(shift) for shift in range(N))


def permute(state: int, permutation: tuple[int, ...]) -> int:
    answer = 0
    while state:
        bit = state & -state
        answer |= 1 << permutation[bit.bit_length() - 1]
        state ^= bit
    return answer


def canonical(state: int) -> int:
    return min((permute(state, rotation) for rotation in ROTATIONS), key=word_key)


def support(state: int) -> tuple[int, ...]:
    return tuple(
        sorted(
            EDGE_DISTANCE[edge]
            for edge in unpack(state)
            if EDGE_DISTANCE[edge] != 1
        )
    )


def signature(state: int) -> str:
    values = support(state)
    return "cycle_only" if not values else ",".join(map(str, values))


def family(state: int) -> str:
    return {
        (): "cycle_only",
        (5, 16, 16): "two_16_one_5",
        (17, 17, 21): "two_17_one_21",
    }[support(state)]


def histogram(values) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(value): counts[value] for value in sorted(counts)}


def build_five_set_table() -> tuple[bytearray, array, list[array]]:
    seed_counts = bytearray()
    flat_edges = array("H")
    incidence = [array("I") for _ in range(M)]
    for vertices in itertools.combinations(range(N), 5):
        clique_edges = [EDGE_ID[edge] for edge in itertools.combinations(vertices, 2)]
        clique = len(seed_counts)
        seed_counts.append(sum(SEED_EDGE_RED[edge] for edge in clique_edges))
        flat_edges.extend(clique_edges)
        for edge in clique_edges:
            incidence[edge].append(clique)
    if len(seed_counts) != FIVE_SET_COUNT or len(flat_edges) != 10 * FIVE_SET_COUNT:
        raise AssertionError("incomplete five-set table")
    expected = math.comb(N - 2, 3)
    if any(len(cliques) != expected for cliques in incidence):
        raise AssertionError("incorrect edge-to-five-set incidence")
    return seed_counts, flat_edges, incidence


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
        for clique in incidence[edge]:
            counts[clique] += step
    red_mask = SEED_RED ^ state
    delta = [0] * M
    objective = 0
    for red_count in (0, 10):
        for clique in positions(counts, red_count):
            objective += 1
            offset = 10 * clique
            for index in range(offset, offset + 10):
                delta[flat_edges[index]] -= 1
    for red_count in (1, 9):
        seek_red = red_count == 1
        for clique in positions(counts, red_count):
            offset = 10 * clique
            minority = -1
            for index in range(offset, offset + 10):
                edge = flat_edges[index]
                if bool((red_mask >> edge) & 1) == seek_red:
                    if minority != -1:
                        raise AssertionError("non-unique minority edge")
                    minority = edge
            if minority == -1:
                raise AssertionError("missing minority edge")
            delta[minority] += 1
    return objective, bytearray(objective + change for change in delta)


def reconstruct(
    source_rows: list[list[int]],
    seed_counts: bytearray,
    flat_edges: array,
    incidence: list[array],
) -> tuple[
    list[int],
    list[int],
    Counter[tuple[int, int]],
    dict[tuple[int, int], list[int]],
]:
    sources = sorted((pack(row) for row in source_rows), key=word_key)
    if len(sources) != 238 or len(set(sources)) != 238:
        raise AssertionError("source list is not 238 distinct states")
    pairs: Counter[tuple[int, int]] = Counter()
    pair_flip_edges: defaultdict[tuple[int, int], list[int]] = defaultdict(list)
    for source_number, source in enumerate(sources):
        if canonical(source) != source:
            raise AssertionError(f"source {source_number} is not canonical")
        objective, after = scan_state(source, seed_counts, flat_edges, incidence)
        if objective != 12:
            raise AssertionError(f"source {source_number} has objective {objective}")
        for edge, target_objective in enumerate(after):
            if target_objective == 13:
                pair = source, canonical(source ^ (1 << edge))
                pairs[pair] += 1
                pair_flip_edges[pair].append(edge)
    targets = sorted({target for _, target in pairs}, key=word_key)
    for target_number, target in enumerate(targets):
        images = {permute(target, rotation) for rotation in ROTATIONS}
        if canonical(target) != target or len(images) != N:
            raise AssertionError(f"target {target_number} is noncanonical or nonfree")
    return sources, targets, pairs, dict(pair_flip_edges)


def summarize(
    sources: list[int], targets: list[int], pairs: Counter[tuple[int, int]]
) -> dict[str, object]:
    source_index = {state: index for index, state in enumerate(sources)}
    target_index = {state: index for index, state in enumerate(targets)}
    left: defaultdict[int, set[int]] = defaultdict(set)
    right: defaultdict[int, set[int]] = defaultdict(set)
    left_raw: Counter[int] = Counter()
    right_raw: Counter[int] = Counter()
    graph: defaultdict[tuple[str, int], set[tuple[str, int]]] = defaultdict(set)
    for (source, target), multiplicity in pairs.items():
        s, t = source_index[source], target_index[target]
        left[s].add(t)
        right[t].add(s)
        left_raw[s] += multiplicity
        right_raw[t] += multiplicity
        graph["s", s].add(("t", t))
        graph["t", t].add(("s", s))

    unseen = {("s", s) for s in range(len(sources))} | {
        ("t", t) for t in range(len(targets))
    }
    component_data = []
    component_of: dict[tuple[str, int], int] = {}
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        queue = deque([start])
        vertices = []
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for neighbor in graph[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    queue.append(neighbor)
        number = len(component_data)
        for vertex in vertices:
            component_of[vertex] = number
        source_ids = {number for side, number in vertices if side == "s"}
        target_ids = {number for side, number in vertices if side == "t"}
        distinct = sum(len(left[s]) for s in source_ids)
        raw = sum(left_raw[s] for s in source_ids)
        families = Counter(family(sources[s]) for s in source_ids)
        component_data.append(
            {
                "sources": len(source_ids),
                "targets": len(target_ids),
                "distinct_pairs": distinct,
                "raw_incidences": raw,
                "simple_cycle_rank": distinct - len(vertices) + 1,
                "multigraph_cycle_rank": raw - len(vertices) + 1,
                "source_families": dict(sorted(families.items())),
            }
        )
    component_profiles = sorted(
        component_data,
        key=lambda item: (
            -item["targets"],
            -item["sources"],
            -item["distinct_pairs"],
            sorted(item["source_families"].items()),
        ),
    )

    family_summaries = {}
    for name in ("cycle_only", "two_16_one_5", "two_17_one_21"):
        source_ids = {s for s, source in enumerate(sources) if family(source) == name}
        target_ids = set().union(*(left[s] for s in source_ids))
        distinct = sum(len(left[s]) for s in source_ids)
        raw = sum(left_raw[s] for s in source_ids)
        components = {component_of["s", s] for s in source_ids}
        family_summaries[name] = {
            "sources": len(source_ids),
            "targets": len(target_ids),
            "distinct_pairs": distinct,
            "raw_incidences": raw,
            "components": len(components),
            "simple_cycle_rank": distinct - len(source_ids) - len(target_ids) + len(components),
            "multigraph_cycle_rank": raw - len(source_ids) - len(target_ids) + len(components),
            "target_support_signature_histogram": histogram(
                signature(targets[t]) for t in target_ids
            ),
        }

    return {
        "source_count": len(sources),
        "source_support_family_histogram": dict(
            sorted(Counter(family(source) for source in sources).items())
        ),
        "raw_incidences": sum(pairs.values()),
        "distinct_source_target_pairs": len(pairs),
        "distinct_targets": len(targets),
        "pair_multiplicity_histogram": histogram(Counter(pairs.values())),
        "source_distinct_target_degree_histogram": histogram(
            len(left[s]) for s in range(len(sources))
        ),
        "source_raw_degree_histogram": histogram(
            left_raw[s] for s in range(len(sources))
        ),
        "target_distinct_source_degree_histogram": histogram(
            len(right[t]) for t in range(len(targets))
        ),
        "target_raw_degree_histogram": histogram(
            right_raw[t] for t in range(len(targets))
        ),
        "target_support_signature_histogram": histogram(
            signature(target) for target in targets
        ),
        "bipartite_component_count": len(component_data),
        "simple_cycle_rank": len(pairs) - len(sources) - len(targets) + len(component_data),
        "multigraph_cycle_rank": sum(pairs.values())
        - len(sources)
        - len(targets)
        + len(component_data),
        "mixed_source_family_component_count": sum(
            len(profile["source_families"]) != 1 for profile in component_data
        ),
        "family_summaries": family_summaries,
        "component_profiles": component_profiles,
    }


def self_test() -> None:
    state = (1 << 0) | (1 << 137) | (1 << 902)
    images = {permute(state, rotation) for rotation in ROTATIONS}
    if len(images) != N or {canonical(image) for image in images} != {canonical(state)}:
        raise AssertionError("rotation/canonicalization self-test failed")
    all_red = (1 << 10) - 1
    for red_mask in (0, 1 << 3, all_red ^ (1 << 7), all_red, 0b1010101010):
        red_count = red_mask.bit_count()
        before = int(red_count in (0, 10))
        for edge in range(10):
            after_count = (red_mask ^ (1 << edge)).bit_count()
            direct_delta = int(after_count in (0, 10)) - before
            formula_delta = -1 if red_count in (0, 10) else 0
            if red_count == 1 and (red_mask >> edge) & 1:
                formula_delta = 1
            if red_count == 9 and not ((red_mask >> edge) & 1):
                formula_delta = 1
            if direct_delta != formula_delta:
                raise AssertionError("five-set flip identity self-test failed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    started = time.monotonic()
    if digest(args.source) != EXPECTED_SOURCE_SHA256:
        raise AssertionError("source-file hash mismatch")
    if digest(args.certificate) != EXPECTED_CERTIFICATE_SHA256:
        raise AssertionError("certificate hash mismatch")
    source_document = json.loads(args.source.read_text())
    certificate = json.loads(args.certificate.read_text())
    expected_metadata = {
        "format": "cyclic43-q13-boundary-v1",
        "order": N,
        "edge_count": M,
        "five_set_count": FIVE_SET_COUNT,
        "seed_red_cyclic_distances": sorted(SEED_DISTANCES),
        "source_file_sha256": EXPECTED_SOURCE_SHA256,
    }
    for key, value in expected_metadata.items():
        if certificate.get(key) != value:
            raise AssertionError(f"certificate metadata mismatch: {key}")
    self_test()
    seed_counts, flat_edges, incidence = build_five_set_table()
    source_rows = source_document["complete_additional_objective_12_rotation_representatives"]
    sources, targets, pairs, pair_flip_edges = reconstruct(
        source_rows, seed_counts, flat_edges, incidence
    )
    expected_sources = [unpack(state) for state in sources]
    expected_targets = [unpack(state) for state in targets]
    source_index = {state: number for number, state in enumerate(sources)}
    target_index = {state: number for number, state in enumerate(targets)}
    expected_incidences = sorted(
        [source_index[source], target_index[target], multiplicity]
        for (source, target), multiplicity in pairs.items()
    )
    if certificate["source_states"] != expected_sources:
        raise AssertionError("source table differs entry-by-entry")
    if certificate["target_states"] != expected_targets:
        raise AssertionError("target table differs entry-by-entry")
    if certificate["incidences"] != expected_incidences:
        raise AssertionError("incidence table differs entry-by-entry")
    claims = summarize(sources, targets, pairs)
    if certificate["claims"] != claims:
        raise AssertionError("claim dictionary differs entry-by-entry")
    parallel_pairs = [pair for pair, multiplicity in pairs.items() if multiplicity > 1]
    if len(parallel_pairs) != 1 or pairs[parallel_pairs[0]] != 2:
        raise AssertionError("expected exactly one double-incidence pair")
    parallel_source, parallel_target = parallel_pairs[0]
    parallel_flips = pair_flip_edges[parallel_pairs[0]]
    parallel_description = [
        (edge, EDGES[edge], EDGE_DISTANCE[edge]) for edge in parallel_flips
    ]
    elapsed = time.monotonic() - started
    print("PASS clean-room all-five-subsets verification of Cyclic(43) q=13 boundary")
    print(f"python={platform.python_version()} five_sets={FIVE_SET_COUNT} cpu_processes=1")
    print(
        f"sources={len(sources)} raw={sum(pairs.values())} "
        f"pairs={len(pairs)} targets={len(targets)}"
    )
    print(
        f"components={claims['bipartite_component_count']} "
        f"simple_cycle_rank={claims['simple_cycle_rank']} "
        f"multigraph_cycle_rank={claims['multigraph_cycle_rank']}"
    )
    print(
        f"parallel_pair=source[{source_index[parallel_source]}]"
        f"->target[{target_index[parallel_target]}] flips={parallel_description}"
    )
    print(f"families={claims['source_support_family_histogram']}")
    print(f"certificate_sha256={digest(args.certificate)}")
    print(f"peak_rss_kib={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")
    print(f"elapsed_seconds={elapsed:.3f}")


if __name__ == "__main__":
    main()
