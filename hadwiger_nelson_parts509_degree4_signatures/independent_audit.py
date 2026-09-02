#!/usr/bin/env python3
"""Independent exact-geometry, witness, and DIMACS audit."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import sys


N = 509
K = 4
D = (310, 313, 316, 319, 322, 325)
ALLOWED = (1, 2, 4, 8, 9, 16, 18, 32, 36)
PIN = (0, 149, 152)
EDGE_DIGEST = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"


def x(v: int, c: int) -> int:
    return 4 * v + c + 1


def b(i: int) -> int:
    return 2037 + i


def edge_digest(edges: list[tuple[int, int]]) -> str:
    data = "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode("ascii")
    return hashlib.sha256(data).hexdigest()


def parse_dimacs(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    variables = clauses_declared = None
    clauses = []
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        fields = line.split()
        if fields[0] == "p":
            assert fields[:2] == ["p", "cnf"] and len(fields) == 4
            variables, clauses_declared = map(int, fields[2:])
            continue
        values = tuple(map(int, fields))
        assert values[-1] == 0 and all(v != 0 for v in values[:-1])
        clauses.append(values[:-1])
    assert variables is not None and clauses_declared == len(clauses)
    return variables, clauses


def independently_expected_cnf(
    edges: list[tuple[int, int]], adj: list[set[int]]
) -> list[tuple[int, ...]]:
    removed = set(D)
    expected: list[tuple[int, ...]] = []
    for v in range(N):
        if v in removed:
            continue
        expected.append(tuple(x(v, c) for c in range(K)))
        for pair in itertools.combinations(range(K), 2):
            expected.append(tuple(-x(v, c) for c in pair))
    for u, v in edges:
        if u in removed or v in removed:
            continue
        for c in range(K):
            expected.append((-x(u, c), -x(v, c)))
    expected.extend((x(v, c),) for c, v in enumerate(PIN))
    for i, v in enumerate(D):
        neighbors = sorted(adj[v])
        for colors in itertools.product(range(K), repeat=K):
            antecedent = tuple(-x(neighbors[j], colors[j]) for j in range(K))
            conclusion = b(i) if len(set(colors)) == K else -b(i)
            expected.append(antecedent + (conclusion,))
    for mask in ALLOWED:
        expected.append(
            tuple(-b(i) if mask & (1 << i) else b(i) for i in range(len(D)))
        )
    return expected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--criticality-dir", type=Path, required=True)
    parser.add_argument("--edge-manifest", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    args = parser.parse_args()

    sys.path.insert(0, str(args.criticality_dir))
    from parts509 import load_graph  # type: ignore

    points, exact_edges_raw = load_graph(args.criticality_dir / "parts509.vtx")
    exact_edges = sorted(tuple(e) for e in exact_edges_raw)
    manifest_edges = sorted(
        tuple(e) for e in json.loads(args.edge_manifest.read_text(encoding="utf-8"))
    )
    assert len(points) == N
    assert exact_edges == manifest_edges
    assert edge_digest(exact_edges) == EDGE_DIGEST

    adj = [set() for _ in range(N)]
    for u, v in exact_edges:
        adj[u].add(v)
        adj[v].add(u)
    degree_four = tuple(i for i, neighbors in enumerate(adj) if len(neighbors) == 4)
    assert degree_four == D
    assert all(not (adj[v] & set(D)) for v in D)

    # The six shared neighbors form the canonical 6-cycle; each low-degree
    # vertex is the apex of one consecutive edge and has two private neighbors.
    shared = sorted(
        x for x in set().union(*(adj[v] for v in D))
        if sum(x in adj[v] for v in D) == 2
    )
    assert shared == [150, 153, 158, 161, 166, 169]
    shared_cycle_edges = {
        tuple(sorted((shared[i], shared[(i + 1) % len(shared)])))
        for i in range(len(shared))
    }
    actual_shared_edges = {
        (u, v) for u, v in itertools.combinations(shared, 2) if v in adj[u]
    }
    assert actual_shared_edges == shared_cycle_edges
    assert all(len(adj[v] & set(shared)) == 2 for v in D)
    assert all(
        sum(y in adj[x] for x, y in itertools.combinations(adj[v], 2)) == 1
        for v in D
    )

    cert = json.loads(args.certificate.read_text(encoding="utf-8"))
    assert tuple(cert["degree_four_vertices"]) == D
    assert tuple(cert["allowed_masks"]) == ALLOWED
    core = [v for v in range(N) if v not in set(D)]
    assert len(core) == 503
    for mask_text, encoded in cert["core_colorings"].items():
        mask = int(mask_text)
        assert mask in ALLOWED and len(encoded) == len(core)
        colors = [-1] * N
        for v, symbol in zip(core, encoded, strict=True):
            assert symbol in "0123"
            colors[v] = int(symbol)
        assert all(
            colors[u] != colors[v]
            for u, v in exact_edges
            if u not in D and v not in D
        )
        observed = sum(
            1 << i
            for i, v in enumerate(D)
            if len({colors[nbr] for nbr in adj[v]}) == 4
        )
        assert observed == mask
    assert set(map(int, cert["core_colorings"])) == set(ALLOWED)

    variables, actual_cnf = parse_dimacs(args.cnf)
    expected_cnf = independently_expected_cnf(exact_edges, adj)
    assert variables == 2042
    assert Counter(actual_cnf) == Counter(expected_cnf)
    assert len(actual_cnf) == len(expected_cnf) == 14741
    assert hashlib.sha256(args.cnf.read_bytes()).hexdigest() == cert["cnf_sha256"]

    print("exact_geometry_reconstructed=true")
    print("strict_edges=2442")
    print("degree_four_vertices=310,313,316,319,322,325")
    print("degree_four_vertices_independent=true")
    print("shared_neighbor_cycle=150,153,158,161,166,169")
    print("sat_witnesses_verified=9")
    print("classification_cnf_semantics_verified=true")
    print("classification_cnf_variables=2042")
    print("classification_cnf_clauses=14741")


if __name__ == "__main__":
    main()
