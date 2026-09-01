#!/usr/bin/env python3
"""Classify the eleven exceptional Parts-509 one-point swap graphs.

The checker uses only graph invariants and the Python standard library.  It
does not solve graph isomorphism.  For a graph G and vertex v define

    profile_G(v) = (deg(v), sorted(deg(w) for w in N(v))).

Both the degree histogram and the multiset of vertex profiles are preserved by
isomorphism.  The certificate succeeds only if one of these two exact
invariants separates every pair among the base graph and the eleven swaps.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


EXPECTED_EDGE_SHA256 = (
    "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
)
EXPECTED_SWAP_CERTIFICATE_SHA256 = (
    "a36a11bf3e63d3ec887b0f4507d51623773b968842a964a314e364713ac46ca3"
)
BASE_VERTEX_COUNT = 509
ADDED_VERTEX = 509


Profile = tuple[int, tuple[int, ...]]


@dataclass(frozen=True)
class GraphData:
    name: str
    deleted_vertex: int | None
    added_degree: int | None
    adjacency: dict[int, frozenset[int]]

    @property
    def edge_count(self) -> int:
        return sum(map(len, self.adjacency.values())) // 2

    @property
    def degree_histogram(self) -> Counter[int]:
        return Counter(map(len, self.adjacency.values()))

    @property
    def profile_histogram(self) -> Counter[Profile]:
        degrees = {v: len(nbrs) for v, nbrs in self.adjacency.items()}
        return Counter(
            (degrees[v], tuple(sorted(degrees[w] for w in nbrs)))
            for v, nbrs in self.adjacency.items()
        )


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_edge_sha256(edges: Iterable[tuple[int, int]]) -> str:
    digest = hashlib.sha256()
    for u, v in sorted(edges):
        digest.update(f"{u} {v}\n".encode("ascii"))
    return digest.hexdigest()


def load_base_edges(path: Path) -> list[tuple[int, int]]:
    raw = json.loads(path.read_text())
    if not isinstance(raw, list):
        raise ValueError("edge input is not a JSON list")
    edges = [tuple(map(int, edge)) for edge in raw]
    if len(edges) != 2442 or len(set(edges)) != len(edges):
        raise ValueError("expected 2,442 distinct base edges")
    if any(not (0 <= u < v < BASE_VERTEX_COUNT) for u, v in edges):
        raise ValueError("base edge outside 0 <= u < v < 509")
    actual_hash = canonical_edge_sha256(edges)
    if actual_hash != EXPECTED_EDGE_SHA256:
        raise ValueError(f"base-edge hash mismatch: {actual_hash}")
    return edges


def adjacency(vertices: Iterable[int], edges: Iterable[tuple[int, int]]) -> dict[int, frozenset[int]]:
    mutable = {v: set() for v in vertices}
    for u, v in edges:
        if u not in mutable or v not in mutable:
            raise ValueError(f"edge {(u, v)} has an absent endpoint")
        if u == v:
            raise ValueError("loop in a simple graph")
        mutable[u].add(v)
        mutable[v].add(u)
    frozen = {v: frozenset(nbrs) for v, nbrs in mutable.items()}
    if any(v not in frozen[w] for v, nbrs in frozen.items() for w in nbrs):
        raise AssertionError("asymmetric adjacency")
    return frozen


def load_graphs(edge_path: Path, swap_path: Path) -> tuple[list[GraphData], dict[str, str]]:
    edges = load_base_edges(edge_path)
    swap_hash = file_sha256(swap_path)
    if swap_hash != EXPECTED_SWAP_CERTIFICATE_SHA256:
        raise ValueError(f"swap-certificate hash mismatch: {swap_hash}")
    document = json.loads(swap_path.read_text())
    swaps = document.get("swaps")
    if not isinstance(swaps, list) or len(swaps) != 11:
        raise ValueError("expected exactly eleven declared swaps")

    graphs = [
        GraphData(
            name="G",
            deleted_vertex=None,
            added_degree=None,
            adjacency=adjacency(range(BASE_VERTEX_COUNT), edges),
        )
    ]
    for index, swap in enumerate(swaps):
        deleted = int(swap["u"])
        neighbors = tuple(map(int, swap["q_neighbors"]))
        if not (0 <= deleted < BASE_VERTEX_COUNT):
            raise ValueError(f"swap {index}: bad deleted vertex")
        if len(neighbors) != len(set(neighbors)):
            raise ValueError(f"swap {index}: repeated added-point neighbor")
        if any(not (0 <= v < BASE_VERTEX_COUNT) for v in neighbors):
            raise ValueError(f"swap {index}: bad added-point neighbor")

        vertices = (set(range(BASE_VERTEX_COUNT)) - {deleted}) | {ADDED_VERTEX}
        swapped_edges = [edge for edge in edges if deleted not in edge]
        swapped_edges.extend(
            (min(ADDED_VERTEX, v), max(ADDED_VERTEX, v))
            for v in neighbors
            if v != deleted
        )
        graphs.append(
            GraphData(
                name=f"S{index}",
                deleted_vertex=deleted,
                added_degree=sum(v != deleted for v in neighbors),
                adjacency=adjacency(vertices, swapped_edges),
            )
        )

    return graphs, {
        "canonical_base_edge_sha256": EXPECTED_EDGE_SHA256,
        "swap_certificate_sha256": swap_hash,
    }


def profile_to_json(profile: Profile) -> dict[str, object]:
    degree, neighbor_degrees = profile
    return {"degree": degree, "neighbor_degrees": list(neighbor_degrees)}


def counter_digest(counter: Counter[Profile]) -> str:
    rows = [
        [profile[0], list(profile[1]), count]
        for profile, count in sorted(counter.items())
    ]
    encoded = json.dumps(rows, separators=(",", ":")).encode("ascii")
    return hashlib.sha256(encoded).hexdigest()


def certify(graphs: list[GraphData], input_hashes: dict[str, str]) -> dict[str, object]:
    summaries: list[dict[str, object]] = []
    degree_histograms = {graph.name: graph.degree_histogram for graph in graphs}
    profile_histograms = {graph.name: graph.profile_histogram for graph in graphs}

    for graph in graphs:
        summaries.append(
            {
                "name": graph.name,
                "vertices": len(graph.adjacency),
                "edges": graph.edge_count,
                "deleted_vertex": graph.deleted_vertex,
                "added_degree": graph.added_degree,
                "degree_histogram": {
                    str(degree): count
                    for degree, count in sorted(degree_histograms[graph.name].items())
                },
                "degree_profile_multiset_sha256": counter_digest(
                    profile_histograms[graph.name]
                ),
            }
        )

    separations: list[dict[str, object]] = []
    histogram_separations = 0
    profile_separations = 0
    for left_index, left in enumerate(graphs):
        for right in graphs[left_index + 1 :]:
            left_degrees = degree_histograms[left.name]
            right_degrees = degree_histograms[right.name]
            if left_degrees != right_degrees:
                witness_degree = min(
                    degree
                    for degree in set(left_degrees) | set(right_degrees)
                    if left_degrees[degree] != right_degrees[degree]
                )
                separations.append(
                    {
                        "left": left.name,
                        "right": right.name,
                        "invariant": "degree_histogram",
                        "witness_degree": witness_degree,
                        "left_count": left_degrees[witness_degree],
                        "right_count": right_degrees[witness_degree],
                    }
                )
                histogram_separations += 1
                continue

            left_profiles = profile_histograms[left.name]
            right_profiles = profile_histograms[right.name]
            if left_profiles == right_profiles:
                raise AssertionError(
                    f"the selected invariants do not separate {left.name} and {right.name}"
                )
            witness_profile = min(
                profile
                for profile in set(left_profiles) | set(right_profiles)
                if left_profiles[profile] != right_profiles[profile]
            )
            separations.append(
                {
                    "left": left.name,
                    "right": right.name,
                    "invariant": "degree_profile_multiset",
                    "witness_profile": profile_to_json(witness_profile),
                    "left_count": left_profiles[witness_profile],
                    "right_count": right_profiles[witness_profile],
                }
            )
            profile_separations += 1

    expected_pairs = len(graphs) * (len(graphs) - 1) // 2
    if len(separations) != expected_pairs:
        raise AssertionError("pair count mismatch")
    if any(summary["vertices"] != BASE_VERTEX_COUNT for summary in summaries):
        raise AssertionError("a classified graph does not have 509 vertices")

    return {
        "claim": (
            "The Parts graph G and its eleven declared non-4-colourable "
            "one-point swaps S0,...,S10 are pairwise nonisomorphic."
        ),
        "proof_method": (
            "Every pair is separated by its degree histogram or, when those "
            "agree, by the multiset over vertices of (degree, sorted neighbor degrees)."
        ),
        "input_hashes": input_hashes,
        "graphs": summaries,
        "pairwise_comparisons": expected_pairs,
        "degree_histogram_separations": histogram_separations,
        "degree_profile_separations": profile_separations,
        "all_pairwise_separated": True,
        "separations": separations,
    }


def build_parser() -> argparse.ArgumentParser:
    here = Path(__file__).resolve().parent
    root = here.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--edges",
        type=Path,
        default=root / "hadwiger_nelson_parts509_degree10_replacements" / "edges.json",
    )
    parser.add_argument(
        "--swaps",
        type=Path,
        default=root / "hadwiger_nelson_parts509_swap_closure" / "swap_certificate.json",
    )
    parser.add_argument(
        "--expect",
        type=Path,
        help="compare the exact generated JSON with a committed certificate",
    )
    return parser


def main() -> None:
    arguments = build_parser().parse_args()
    graphs, input_hashes = load_graphs(arguments.edges, arguments.swaps)
    certificate = certify(graphs, input_hashes)
    canonical = json.dumps(certificate, indent=2, sort_keys=True) + "\n"
    if arguments.expect is not None:
        expected = arguments.expect.read_text()
        if canonical != expected:
            raise SystemExit(f"certificate mismatch: {arguments.expect}")
    print(canonical, end="")


if __name__ == "__main__":
    main()
