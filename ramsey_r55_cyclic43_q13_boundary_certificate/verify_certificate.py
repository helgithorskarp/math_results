#!/usr/bin/env python3
"""Independently verify every entry of the Cyclic(43) q=13 certificate.

Unlike ``generate_boundary.py``, this checker counts common-neighbour
triangles by explicit triples and finds bipartite components by breadth-first
search.  It shares no project code with the generator or upstream NumPy scan.
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
EDGES = list(itertools.combinations(range(N), 2))
EDGE_NUMBER = {pair: number for number, pair in enumerate(EDGES)}
EDGE_DISTANCE = [min(v - u, N - (v - u)) for u, v in EDGES]
FULL_VERTEX_SET = (1 << N) - 1
SEED_RED = sum(1 << e for e, d in enumerate(EDGE_DISTANCE) if d in SEED_DISTANCES)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pack(edge_list: list[int]) -> int:
    if edge_list != sorted(set(edge_list)) or any(not 0 <= e < M for e in edge_list):
        raise AssertionError("malformed edge list")
    return sum(1 << e for e in edge_list)


def unpack(state: int) -> list[int]:
    answer = []
    for edge in range(M):
        if (state >> edge) & 1:
            answer.append(edge)
    return answer


def words(state: int) -> tuple[int, ...]:
    mask = (1 << 64) - 1
    return tuple((state >> (64 * j)) & mask for j in range(15))


def rotated(state: int, amount: int) -> int:
    answer = 0
    for edge in unpack(state):
        u, v = EDGES[edge]
        u = (u + amount) % N
        v = (v + amount) % N
        if u > v:
            u, v = v, u
        answer |= 1 << EDGE_NUMBER[u, v]
    return answer


def canonical(state: int) -> int:
    candidates = [rotated(state, amount) for amount in range(N)]
    return min(candidates, key=words)


def color_rows(toggle_state: int) -> tuple[list[int], list[int]]:
    red_edges = SEED_RED ^ toggle_state
    red = [0] * N
    for edge in unpack(red_edges):
        u, v = EDGES[edge]
        red[u] |= 1 << v
        red[v] |= 1 << u
    blue = []
    for vertex in range(N):
        possible = FULL_VERTEX_SET & ~(1 << vertex)
        blue.append(possible & ~red[vertex])
    return red, blue


def number_of_k_cliques(rows: list[int], k: int) -> int:
    """Independent ordered backtracking count."""

    def visit(prefix_last: int, candidates: list[int], still_needed: int) -> int:
        del prefix_last  # documents that candidates already enforce increasing order
        if still_needed == 0:
            return 1
        if len(candidates) < still_needed:
            return 0
        total = 0
        for position, vertex in enumerate(candidates):
            later_neighbours = [
                other
                for other in candidates[position + 1 :]
                if (rows[vertex] >> other) & 1
            ]
            total += visit(vertex, later_neighbours, still_needed - 1)
        return total

    return visit(-1, list(range(N)), k)


def explicit_triangle_count(rows: list[int], vertex_mask: int) -> int:
    vertices = [v for v in range(N) if (vertex_mask >> v) & 1]
    total = 0
    for a, b, c in itertools.combinations(vertices, 3):
        if ((rows[a] >> b) & 1) and ((rows[a] >> c) & 1) and ((rows[b] >> c) & 1):
            total += 1
    return total


def support(state: int) -> tuple[int, ...]:
    return tuple(sorted(EDGE_DISTANCE[e] for e in unpack(state) if EDGE_DISTANCE[e] != 1))


def family(state: int) -> str:
    return {
        (): "cycle_only",
        (5, 16, 16): "two_16_one_5",
        (17, 17, 21): "two_17_one_21",
    }[support(state)]


def signature(state: int) -> str:
    values = support(state)
    return "cycle_only" if not values else ",".join(str(value) for value in values)


def histogram(values: list[int] | list[str] | Counter[int]) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(value): counts[value] for value in sorted(counts)}


def regenerate(source_lists: list[list[int]]) -> tuple[list[int], list[int], Counter[tuple[int, int]]]:
    sources = sorted((pack(item) for item in source_lists), key=words)
    if len(sources) != 238 or len(set(sources)) != 238:
        raise AssertionError("source list is not 238 distinct states")
    pairs: Counter[tuple[int, int]] = Counter()
    for source_number, source in enumerate(sources):
        if canonical(source) != source:
            raise AssertionError(f"source {source_number} is not canonical")
        red, blue = color_rows(source)
        objective = number_of_k_cliques(red, 5) + number_of_k_cliques(blue, 5)
        if objective != 12:
            raise AssertionError(f"source {source_number} has objective {objective}")
        for edge, (u, v) in enumerate(EDGES):
            r = explicit_triangle_count(red, red[u] & red[v])
            b = explicit_triangle_count(blue, blue[u] & blue[v])
            after = objective - r + b if ((red[u] >> v) & 1) else objective + r - b
            if after == 13:
                target = canonical(source ^ (1 << edge))
                pairs[source, target] += 1
    targets = sorted({target for _, target in pairs}, key=words)
    for target_number, target in enumerate(targets):
        if canonical(target) != target:
            raise AssertionError(f"target {target_number} is not canonical")
        if len({rotated(target, amount) for amount in range(N)}) != N:
            raise AssertionError(f"target {target_number} has a nonfree C_43 orbit")
    return sources, targets, pairs


def summarize(
    sources: list[int], targets: list[int], pairs: Counter[tuple[int, int]]
) -> dict[str, object]:
    si = {state: number for number, state in enumerate(sources)}
    ti = {state: number for number, state in enumerate(targets)}
    left_neighbours: defaultdict[int, set[int]] = defaultdict(set)
    right_neighbours: defaultdict[int, set[int]] = defaultdict(set)
    left_raw: Counter[int] = Counter()
    right_raw: Counter[int] = Counter()
    graph: defaultdict[tuple[str, int], set[tuple[str, int]]] = defaultdict(set)
    for (source, target), multiplicity in pairs.items():
        s, t = si[source], ti[target]
        left_neighbours[s].add(t)
        right_neighbours[t].add(s)
        left_raw[s] += multiplicity
        right_raw[t] += multiplicity
        graph["s", s].add(("t", t))
        graph["t", t].add(("s", s))

    unseen = {("s", s) for s in range(len(sources))} | {
        ("t", t) for t in range(len(targets))
    }
    profiles = []
    vertex_component: dict[tuple[str, int], int] = {}
    while unseen:
        start = min(unseen)
        queue = deque([start])
        unseen.remove(start)
        vertices = []
        while queue:
            vertex = queue.popleft()
            vertices.append(vertex)
            for neighbour in graph[vertex]:
                if neighbour in unseen:
                    unseen.remove(neighbour)
                    queue.append(neighbour)
        number = len(profiles)
        for vertex in vertices:
            vertex_component[vertex] = number
        source_ids = {i for side, i in vertices if side == "s"}
        target_ids = {i for side, i in vertices if side == "t"}
        distinct = sum(len(left_neighbours[s]) for s in source_ids)
        raw = sum(left_raw[s] for s in source_ids)
        families = Counter(family(sources[s]) for s in source_ids)
        profiles.append(
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
    profiles.sort(
        key=lambda item: (
            -item["targets"],
            -item["sources"],
            -item["distinct_pairs"],
            sorted(item["source_families"].items()),
        )
    )

    family_summaries: dict[str, object] = {}
    for name in ("cycle_only", "two_16_one_5", "two_17_one_21"):
        source_ids = {s for s, source in enumerate(sources) if family(source) == name}
        target_ids = set().union(*(left_neighbours[s] for s in source_ids))
        distinct = sum(len(left_neighbours[s]) for s in source_ids)
        raw = sum(left_raw[s] for s in source_ids)
        components = {vertex_component["s", s] for s in source_ids}
        family_summaries[name] = {
            "sources": len(source_ids),
            "targets": len(target_ids),
            "distinct_pairs": distinct,
            "raw_incidences": raw,
            "components": len(components),
            "simple_cycle_rank": distinct - len(source_ids) - len(target_ids) + len(components),
            "multigraph_cycle_rank": raw - len(source_ids) - len(target_ids) + len(components),
            "target_support_signature_histogram": histogram(
                [signature(targets[t]) for t in target_ids]
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
            [len(left_neighbours[s]) for s in range(len(sources))]
        ),
        "source_raw_degree_histogram": histogram(
            [left_raw[s] for s in range(len(sources))]
        ),
        "target_distinct_source_degree_histogram": histogram(
            [len(right_neighbours[t]) for t in range(len(targets))]
        ),
        "target_raw_degree_histogram": histogram(
            [right_raw[t] for t in range(len(targets))]
        ),
        "target_support_signature_histogram": histogram(
            [signature(target) for target in targets]
        ),
        "bipartite_component_count": len(profiles),
        "simple_cycle_rank": len(pairs) - len(sources) - len(targets) + len(profiles),
        "multigraph_cycle_rank": sum(pairs.values())
        - len(sources)
        - len(targets)
        + len(profiles),
        "mixed_source_family_component_count": sum(
            len(profile["source_families"]) != 1 for profile in profiles
        ),
        "family_summaries": family_summaries,
        "component_profiles": profiles,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    source_doc = json.loads(args.source.read_text())
    certificate = json.loads(args.certificate.read_text())

    if certificate["format"] != "cyclic43-q13-boundary-v1":
        raise AssertionError("wrong certificate format")
    if certificate["source_file_sha256"] != digest(args.source):
        raise AssertionError("source hash mismatch")
    source_lists = source_doc["complete_additional_objective_12_rotation_representatives"]
    sources, targets, pairs = regenerate(source_lists)

    expected_sources = [unpack(source) for source in sources]
    expected_targets = [unpack(target) for target in targets]
    si = {source: number for number, source in enumerate(sources)}
    ti = {target: number for number, target in enumerate(targets)}
    expected_incidences = sorted(
        [si[source], ti[target], multiplicity]
        for (source, target), multiplicity in pairs.items()
    )
    if certificate["source_states"] != expected_sources:
        raise AssertionError("source-state table mismatch")
    if certificate["target_states"] != expected_targets:
        raise AssertionError("target-state table mismatch")
    if certificate["incidences"] != expected_incidences:
        raise AssertionError("incidence table mismatch")
    claims = summarize(sources, targets, pairs)
    if certificate["claims"] != claims:
        raise AssertionError("summary-claim mismatch")

    print("PASS independently verified every Cyclic(43) q=13 certificate entry")
    print(
        f"sources={len(sources)} raw={sum(pairs.values())} "
        f"pairs={len(pairs)} targets={len(targets)}"
    )
    print(
        f"components={claims['bipartite_component_count']} "
        f"simple_cycle_rank={claims['simple_cycle_rank']} "
        f"multigraph_cycle_rank={claims['multigraph_cycle_rank']}"
    )
    print(f"certificate_sha256={digest(args.certificate)}")


if __name__ == "__main__":
    main()
