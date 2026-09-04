#!/usr/bin/env python3
"""Generate the exact Cyclic(43) objective-13 exit certificate.

The 238 source states are toggles relative to Exoo's cyclic seed.  For each
source and each edge, the flipped objective is computed by counting triangles
in the common red and blue neighbourhoods of the edge endpoints.  This is
algorithmically independent of the upstream NumPy five-set-incidence scan.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict, deque
from pathlib import Path


ORDER = 43
EDGE_COUNT = ORDER * (ORDER - 1) // 2
FIVE_SET_COUNT = 962_598
SEED_DISTANCES = frozenset({1, 2, 7, 10, 12, 13, 14, 16, 18, 20, 21})
MASK64 = (1 << 64) - 1
WORD_COUNT = (EDGE_COUNT + 63) // 64

EDGES = tuple(itertools.combinations(range(ORDER), 2))
EDGE_ID = [[-1] * ORDER for _ in range(ORDER)]
for _edge, (_u, _v) in enumerate(EDGES):
    EDGE_ID[_u][_v] = _edge
    EDGE_ID[_v][_u] = _edge

EDGE_DISTANCE = tuple(min(v - u, ORDER - (v - u)) for u, v in EDGES)
ROTATED_EDGE = tuple(
    tuple(
        EDGE_ID[min((u + shift) % ORDER, (v + shift) % ORDER)]
        [max((u + shift) % ORDER, (v + shift) % ORDER)]
        for u, v in EDGES
    )
    for shift in range(ORDER)
)
SEED_RED_MASK = sum(
    1 << edge for edge, distance in enumerate(EDGE_DISTANCE) if distance in SEED_DISTANCES
)
ALL_VERTICES = (1 << ORDER) - 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def state_from_edges(edges: list[int] | tuple[int, ...]) -> int:
    state = 0
    previous = -1
    for edge in edges:
        if not isinstance(edge, int) or not previous < edge < EDGE_COUNT:
            raise ValueError("state edges must be strictly increasing integers in [0,903)")
        state |= 1 << edge
        previous = edge
    return state


def edges_from_state(state: int) -> list[int]:
    edges: list[int] = []
    while state:
        bit = state & -state
        edges.append(bit.bit_length() - 1)
        state ^= bit
    return edges


def state_key(state: int) -> tuple[int, ...]:
    """The upstream canonical ordering: 15 little-endian 64-bit words."""
    return tuple((state >> (64 * word)) & MASK64 for word in range(WORD_COUNT))


def rotate_state(state: int, shift: int) -> int:
    rotated = 0
    permutation = ROTATED_EDGE[shift]
    while state:
        bit = state & -state
        rotated |= 1 << permutation[bit.bit_length() - 1]
        state ^= bit
    return rotated


def canonical_state(state: int) -> int:
    return min((rotate_state(state, shift) for shift in range(ORDER)), key=state_key)


def support_signature(state: int) -> tuple[int, ...]:
    return tuple(sorted(EDGE_DISTANCE[edge] for edge in edges_from_state(state) if EDGE_DISTANCE[edge] != 1))


def signature_name(signature: tuple[int, ...]) -> str:
    return "cycle_only" if not signature else ",".join(map(str, signature))


def source_family(state: int) -> str:
    signature = support_signature(state)
    names = {
        (): "cycle_only",
        (5, 16, 16): "two_16_one_5",
        (17, 17, 21): "two_17_one_21",
    }
    if signature not in names:
        raise AssertionError(f"unexpected source signature {signature}")
    return names[signature]


def adjacency(red_mask: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    red = [0] * ORDER
    for edge in edges_from_state(red_mask):
        u, v = EDGES[edge]
        red[u] |= 1 << v
        red[v] |= 1 << u
    blue = [0] * ORDER
    for vertex in range(ORDER):
        blue[vertex] = (ALL_VERTICES ^ (1 << vertex)) & ~red[vertex]
    return tuple(red), tuple(blue)


def clique_count(adjacency_rows: tuple[int, ...], size: int) -> int:
    """Count unlabeled cliques exactly by increasing-vertex recursion."""

    def extend(candidates: int, needed: int) -> int:
        if needed == 0:
            return 1
        if candidates.bit_count() < needed:
            return 0
        if needed == 1:
            return candidates.bit_count()
        total = 0
        while candidates.bit_count() >= needed:
            bit = candidates & -candidates
            candidates ^= bit
            vertex = bit.bit_length() - 1
            total += extend(candidates & adjacency_rows[vertex], needed - 1)
        return total

    return extend(ALL_VERTICES, size)


def triangle_count(adjacency_rows: tuple[int, ...], vertices: int) -> int:
    """Count triangles induced by ``vertices`` using bit intersections."""
    total = 0
    remaining = vertices
    while remaining:
        v_bit = remaining & -remaining
        remaining ^= v_bit
        v = v_bit.bit_length() - 1
        neighbours = adjacency_rows[v] & remaining
        while neighbours:
            u_bit = neighbours & -neighbours
            neighbours ^= u_bit
            u = u_bit.bit_length() - 1
            total += (adjacency_rows[u] & neighbours).bit_count()
    return total


def objective_and_exit_edges(state: int) -> tuple[int, list[int]]:
    red, blue = adjacency(SEED_RED_MASK ^ state)
    objective = clique_count(red, 5) + clique_count(blue, 5)
    exits: list[int] = []
    for edge, (u, v) in enumerate(EDGES):
        red_extensions = triangle_count(red, red[u] & red[v])
        blue_extensions = triangle_count(blue, blue[u] & blue[v])
        if (red[u] >> v) & 1:
            flipped = objective - red_extensions + blue_extensions
        else:
            flipped = objective + red_extensions - blue_extensions
        if flipped == 13:
            exits.append(edge)
    return objective, exits


class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def union(self, left: int, right: int) -> None:
        left = self.find(left)
        right = self.find(right)
        if left == right:
            return
        if self.rank[left] < self.rank[right]:
            left, right = right, left
        self.parent[right] = left
        if self.rank[left] == self.rank[right]:
            self.rank[left] += 1


def histogram(values: list[int] | Counter[int]) -> dict[str, int]:
    counts = values if isinstance(values, Counter) else Counter(values)
    return {str(key): counts[key] for key in sorted(counts)}


def build_claims(
    sources: list[int], targets: list[int], pair_counts: Counter[tuple[int, int]]
) -> dict[str, object]:
    source_index = {state: index for index, state in enumerate(sources)}
    target_index = {state: index for index, state in enumerate(targets)}
    source_pairs: defaultdict[int, set[int]] = defaultdict(set)
    source_raw: Counter[int] = Counter()
    target_pairs: defaultdict[int, set[int]] = defaultdict(set)
    target_raw: Counter[int] = Counter()
    family_pairs: defaultdict[str, list[tuple[int, int, int]]] = defaultdict(list)
    for (source, target), multiplicity in pair_counts.items():
        s = source_index[source]
        t = target_index[target]
        source_pairs[s].add(t)
        source_raw[s] += multiplicity
        target_pairs[t].add(s)
        target_raw[t] += multiplicity
        family_pairs[source_family(source)].append((s, t, multiplicity))

    uf = UnionFind(len(sources) + len(targets))
    for source, target in pair_counts:
        uf.union(source_index[source], len(sources) + target_index[target])
    roots = {uf.find(index) for index in range(len(sources) + len(targets))}
    component_count = len(roots)

    component_sources: defaultdict[int, set[int]] = defaultdict(set)
    component_targets: defaultdict[int, set[int]] = defaultdict(set)
    component_pairs: Counter[int] = Counter()
    component_raw: Counter[int] = Counter()
    for s in range(len(sources)):
        component_sources[uf.find(s)].add(s)
    for t in range(len(targets)):
        component_targets[uf.find(len(sources) + t)].add(t)
    for (source, target), multiplicity in pair_counts.items():
        root = uf.find(source_index[source])
        component_pairs[root] += 1
        component_raw[root] += multiplicity

    profiles = []
    mixed_components = 0
    for root in roots:
        source_ids = component_sources[root]
        target_ids = component_targets[root]
        families = Counter(source_family(sources[s]) for s in source_ids)
        if len(families) != 1:
            mixed_components += 1
        vertices = len(source_ids) + len(target_ids)
        profiles.append(
            {
                "sources": len(source_ids),
                "targets": len(target_ids),
                "distinct_pairs": component_pairs[root],
                "raw_incidences": component_raw[root],
                "simple_cycle_rank": component_pairs[root] - vertices + 1,
                "multigraph_cycle_rank": component_raw[root] - vertices + 1,
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
    for family in ("cycle_only", "two_16_one_5", "two_17_one_21"):
        records = family_pairs[family]
        family_source_ids = {s for s, _, _ in records}
        family_target_ids = {t for _, t, _ in records}
        family_roots = {uf.find(s) for s in family_source_ids}
        distinct_pairs = len(records)
        raw_incidences = sum(multiplicity for _, _, multiplicity in records)
        family_summaries[family] = {
            "sources": len(family_source_ids),
            "targets": len(family_target_ids),
            "distinct_pairs": distinct_pairs,
            "raw_incidences": raw_incidences,
            "components": len(family_roots),
            "simple_cycle_rank": distinct_pairs
            - len(family_source_ids)
            - len(family_target_ids)
            + len(family_roots),
            "multigraph_cycle_rank": raw_incidences
            - len(family_source_ids)
            - len(family_target_ids)
            + len(family_roots),
            "target_support_signature_histogram": histogram(
                [signature_name(support_signature(targets[t])) for t in family_target_ids]
            ),
        }

    return {
        "source_count": len(sources),
        "source_support_family_histogram": dict(
            sorted(Counter(source_family(source) for source in sources).items())
        ),
        "raw_incidences": sum(pair_counts.values()),
        "distinct_source_target_pairs": len(pair_counts),
        "distinct_targets": len(targets),
        "pair_multiplicity_histogram": histogram(Counter(pair_counts.values())),
        "source_distinct_target_degree_histogram": histogram(
            [len(source_pairs[index]) for index in range(len(sources))]
        ),
        "source_raw_degree_histogram": histogram(
            [source_raw[index] for index in range(len(sources))]
        ),
        "target_distinct_source_degree_histogram": histogram(
            [len(target_pairs[index]) for index in range(len(targets))]
        ),
        "target_raw_degree_histogram": histogram(
            [target_raw[index] for index in range(len(targets))]
        ),
        "target_support_signature_histogram": histogram(
            [signature_name(support_signature(target)) for target in targets]
        ),
        "bipartite_component_count": component_count,
        "simple_cycle_rank": len(pair_counts) - len(sources) - len(targets) + component_count,
        "multigraph_cycle_rank": sum(pair_counts.values())
        - len(sources)
        - len(targets)
        + component_count,
        "mixed_source_family_component_count": mixed_components,
        "family_summaries": family_summaries,
        "component_profiles": profiles,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    document = json.loads(args.source.read_text())
    raw_sources = document["complete_additional_objective_12_rotation_representatives"]
    sources = [state_from_edges(edges) for edges in raw_sources]
    if len(sources) != 238 or len(set(sources)) != 238:
        raise AssertionError("expected 238 distinct source states")
    if any(canonical_state(source) != source for source in sources):
        raise AssertionError("source file contains a noncanonical state")
    sources.sort(key=state_key)

    pair_counts: Counter[tuple[int, int]] = Counter()
    for position, source in enumerate(sources, 1):
        objective, exits = objective_and_exit_edges(source)
        if objective != 12:
            raise AssertionError(f"source {position - 1} has objective {objective}, not 12")
        for edge in exits:
            target = canonical_state(source ^ (1 << edge))
            pair_counts[source, target] += 1

    targets = sorted({target for _, target in pair_counts}, key=state_key)
    for position, target in enumerate(targets):
        red, blue = adjacency(SEED_RED_MASK ^ target)
        objective = clique_count(red, 5) + clique_count(blue, 5)
        if objective != 13:
            raise AssertionError(f"target {position} has objective {objective}, not 13")
        if canonical_state(target) != target:
            raise AssertionError(f"target {position} is not canonical")
        if len({rotate_state(target, shift) for shift in range(ORDER)}) != ORDER:
            raise AssertionError(f"target {position} is not free under C_43")

    source_index = {state: index for index, state in enumerate(sources)}
    target_index = {state: index for index, state in enumerate(targets)}
    incidences = sorted(
        [source_index[source], target_index[target], multiplicity]
        for (source, target), multiplicity in pair_counts.items()
    )
    claims = build_claims(sources, targets, pair_counts)
    certificate = {
        "format": "cyclic43-q13-boundary-v1",
        "order": ORDER,
        "edge_count": EDGE_COUNT,
        "five_set_count": FIVE_SET_COUNT,
        "seed_red_cyclic_distances": sorted(SEED_DISTANCES),
        "source_file_sha256": sha256(args.source),
        "upstream_source_commit": "02a959f499aa8e3b749a7f7fb3d3fc5f255c3b14",
        "canonicalization": "minimum tuple of 15 little-endian 64-bit toggle words over C_43 rotations",
        "scope": "all objective-13 one-edge exits from the persisted 238-state A_12 list",
        "source_states": [edges_from_state(source) for source in sources],
        "target_states": [edges_from_state(target) for target in targets],
        "incidences": incidences,
        "claims": claims,
    }
    args.output.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")
    print("PASS generated exact Cyclic(43) q=13 boundary certificate")
    print(
        f"sources={len(sources)} raw={sum(pair_counts.values())} "
        f"pairs={len(pair_counts)} targets={len(targets)}"
    )
    print(
        f"components={claims['bipartite_component_count']} "
        f"simple_cycle_rank={claims['simple_cycle_rank']} "
        f"multigraph_cycle_rank={claims['multigraph_cycle_rank']}"
    )
    print(f"certificate_sha256={sha256(args.output)}")


if __name__ == "__main__":
    main()
