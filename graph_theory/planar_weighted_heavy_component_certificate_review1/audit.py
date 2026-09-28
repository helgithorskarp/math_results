#!/usr/bin/env python3
"""Independent audit of the 50-vertex geodesic-pair certificate."""

from __future__ import annotations

import hashlib
import heapq
import itertools
import json
from pathlib import Path


SOURCE = Path(__file__).resolve().parents[1] / "planar_weighted_heavy_component_certificate"
N = 50


def graph() -> tuple[list[dict[int, int]], set[tuple[int, int]]]:
    def vertex(i: int, j: int) -> int:
        return 1 + 7 * i + j

    edges: set[tuple[int, int]] = set()
    for i, j in itertools.product(range(7), repeat=2):
        a = vertex(i, j)
        if i + 1 < 7:
            edges.add(tuple(sorted((a, vertex(i + 1, j)))))
        if j + 1 < 7:
            edges.add(tuple(sorted((a, vertex(i, j + 1)))))
        if i + 1 < 7 and j + 1 < 7:
            edges.add(tuple(sorted((a, vertex(i + 1, j + 1)))))
        if i in (0, 6) or j in (0, 6):
            edges.add((0, a))
    assert len(edges) == 144
    adjacency = [{} for _ in range(N)]
    for a, b in edges:
        data = hashlib.sha256(f"1:{a}:{b}".encode("ascii")).digest()
        length = 1 + int.from_bytes(data[:4], "big") % 19
        adjacency[a][b] = length
        adjacency[b][a] = length
    return adjacency, edges


def all_distances(adjacency: list[dict[int, int]]) -> list[list[int]]:
    result = []
    for start in range(N):
        distances = [10**9] * N
        distances[start] = 0
        heap = [(0, start)]
        while heap:
            distance, vertex = heapq.heappop(heap)
            if distance != distances[vertex]:
                continue
            for neighbor, length in adjacency[vertex].items():
                candidate = distance + length
                if candidate < distances[neighbor]:
                    distances[neighbor] = candidate
                    heapq.heappush(heap, (candidate, neighbor))
        assert max(distances) < 10**9
        result.append(distances)
    return result


def components(
    adjacency: list[dict[int, int]], edges: set[tuple[int, int]], removed: set[int]
) -> list[frozenset[int]]:
    parent = list(range(N))

    def root(v: int) -> int:
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v

    for a, b in edges:
        if a not in removed and b not in removed:
            parent[root(a)] = root(b)
    groups: dict[int, set[int]] = {}
    for v in range(N):
        if v not in removed:
            groups.setdefault(root(v), set()).add(v)
    return [frozenset(group) for group in groups.values()]


def longest_order(adjacency: list[dict[int, int]], distances: list[list[int]]) -> int:
    answer = 0
    for source in range(N):
        best = [0] * N
        best[source] = 1
        for vertex in sorted(range(N), key=lambda v: distances[source][v]):
            for neighbor, length in adjacency[vertex].items():
                if distances[source][vertex] + length == distances[source][neighbor]:
                    best[neighbor] = max(best[neighbor], best[vertex] + 1)
        answer = max(answer, max(best))
    return answer


def main() -> None:
    certificate = json.loads((SOURCE / "certificate.json").read_text())
    assert certificate["schema"] == "heavy-component-chain-v1"
    assert certificate["metric_seed"] == 1
    assert len(certificate["cuts"]) == 14
    adjacency, edges = graph()
    distances = all_distances(adjacency)
    distance_hash = hashlib.sha256(
        json.dumps(distances, separators=(",", ":")).encode()
    ).hexdigest()
    assert distance_hash == "d8f716eae373104373a6c7af4ab7f81623ef039bc7d1683394ae92a893e77f09"

    # Enumerate all pairwise-intersecting choices, without the author's
    # forced-component rule or component traversal.
    compatible: list[tuple[frozenset[int], ...]] = [()]
    counts = []
    final_blockers = []
    paths = set()
    component_families = []
    for cut in certificate["cuts"]:
        assert 1 <= len(cut["paths"]) <= 2
        removed: set[int] = set()
        for path in cut["paths"]:
            assert path and len(set(path)) == len(path)
            assert all(isinstance(v, int) and 0 <= v < N for v in path)
            cost = 0
            for a, b in zip(path, path[1:]):
                assert b in adjacency[a]
                cost += adjacency[a][b]
            assert cost == distances[path[0]][path[-1]]
            removed.update(path)
            sequence = tuple(path)
            paths.add(min(sequence, sequence[::-1]))
        parts = components(adjacency, edges, removed)
        component_families.append(parts)
        if len(compatible) == 1 and compatible[0]:
            final_blockers = [
                next((i for i, earlier in enumerate(compatible[0]) if not part & earlier), None)
                for part in parts
            ]
        compatible = [
            chosen + (part,)
            for chosen in compatible
            for part in parts
            if all(part & earlier for earlier in chosen)
        ]
        counts.append(len(compatible))

    assert counts == [1] * 13 + [0], counts
    assert all(blocker is not None for blocker in final_blockers)
    assert len(paths) == 22
    assert longest_order(adjacency, distances) == 11

    def compatible_count(families: list[list[frozenset[int]]]) -> int:
        choices: list[tuple[frozenset[int], ...]] = [()]
        for family in families:
            choices = [
                chosen + (part,)
                for chosen in choices
                for part in family
                if all(part & earlier for earlier in chosen)
            ]
        return len(choices)

    omission_counts = [
        compatible_count(component_families[:i] + component_families[i + 1 :])
        for i in range(len(component_families))
    ]
    assert omission_counts == [1, 1, 1, 1, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1]
    print(json.dumps({
        "vertices": N,
        "edges": len(edges),
        "cuts": len(certificate["cuts"]),
        "distinct_paths": len(paths),
        "compatible_prefix_counts": counts,
        "last_cut_blocked_by_earlier_cuts": final_blockers,
        "one_cut_omission_compatible_counts": omission_counts,
        "maximum_geodesic_order": 11,
        "distance_matrix_sha256": distance_hash,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
