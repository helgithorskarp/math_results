#!/usr/bin/env python3
"""Independent finite audit for the order-54 seven-edge exclusion.

This standard-library checker deliberately does not import the target's SAT
generator.  It reconstructs the arithmetic equality case, the two colored
matching types, their automorphism orbits, and the expected case index.  With
--validation it also checks every CNF and proof hash in a fresh target run.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from itertools import combinations, permutations, product
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_TARGET = HERE.parent / "graph_theory" / "extremal_girth5_order54"


def edge(a: int, b: int) -> tuple[int, int]:
    return (a, b) if a < b else (b, a)


def perfect_matchings(points: tuple[int, ...]):
    if not points:
        yield frozenset()
        return
    first = points[0]
    for i in range(1, len(points)):
        second = points[i]
        rest = points[1:i] + points[i + 1 :]
        for matching in perfect_matchings(rest):
            yield matching | {edge(first, second)}


M = frozenset(edge(2 * i, 2 * i + 1) for i in range(5))


def canonical_k(cycles: tuple[tuple[int, ...], ...]) -> frozenset[tuple[int, int]]:
    return frozenset(
        edge(2 * i + 1, 2 * j)
        for cycle in cycles
        for i, j in zip(cycle, cycle[1:] + cycle[:1])
    )


def component_sizes(graph_edges: frozenset[tuple[int, int]]) -> tuple[int, ...]:
    adjacency = [set() for _ in range(10)]
    for a, b in graph_edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen = set(range(10))
    sizes = []
    while unseen:
        stack = [min(unseen)]
        seen = set(stack)
        while stack:
            v = stack.pop()
            for w in adjacency[v] - seen:
                seen.add(w)
                stack.append(w)
        unseen -= seen
        sizes.append(len(seen))
    return tuple(sorted(sizes))


def m_preserving_permutations():
    for pair_permutation in permutations(range(5)):
        for flips in product((0, 1), repeat=5):
            yield tuple(
                2 * pair_permutation[i] + (bit ^ flips[i])
                for i in range(5)
                for bit in range(2)
            )


def transform_edge_set(edges, permutation):
    return frozenset(edge(permutation[a], permutation[b]) for a, b in edges)


def independent(subset, graph_edges) -> bool:
    return all(edge(a, b) not in graph_edges for a, b in combinations(subset, 2))


def raw_motifs(k_edges):
    graph_edges = M | k_edges
    motifs = set()
    for i_set in combinations(range(10), 3):
        if not independent(i_set, graph_edges):
            continue
        remainder = set(range(10)) - set(i_set) - {x ^ 1 for x in i_set}
        assert len(remainder) == 4
        for x_set in combinations(sorted(remainder), 2):
            y_set = tuple(sorted(remainder - set(x_set)))
            if independent(x_set, graph_edges) and independent(y_set, graph_edges):
                motifs.add((tuple(i_set), tuple(x_set), y_set))
    return motifs


def transform_motif(motif, permutation):
    return tuple(tuple(sorted(permutation[x] for x in part)) for part in motif)


def motif_audit(name: str, cycles: tuple[tuple[int, ...], ...]):
    k_edges = canonical_k(cycles)
    automorphisms = [
        permutation
        for permutation in m_preserving_permutations()
        if transform_edge_set(k_edges, permutation) == k_edges
    ]
    raw = raw_motifs(k_edges)
    unseen = set(raw)
    orbit_sizes = []
    while unseen:
        representative = min(unseen)
        orbit = {transform_motif(representative, p) for p in automorphisms}
        assert orbit <= raw
        unseen -= orbit
        orbit_sizes.append(len(orbit))
    return {
        "automorphisms": len(automorphisms),
        "matching": name,
        "orbits": len(orbit_sizes),
        "orbit_sizes": sorted(orbit_sizes),
        "raw_motifs": len(raw),
    }


def arithmetic_audit():
    feasible = []
    for m in range(14):
        for k in range(14):
            if k >= max(0, 2 * m - 13) and 3 * m + k <= 22:
                feasible.append((m, k))
    assert max(m for m, _ in feasible) == 7
    assert [pair for pair in feasible if pair[0] == 7] == [(7, 1)]

    # Equality in the two binomial lower bounds permits only c=3,4 on V6
    # and c=1,2 on V7.  The incidence sums then force these multiplicities.
    v6_c4 = (39 + 2 * 7) - 3 * 17
    v7_c2 = (65 - 4 * 7) - 1 * 24
    profile = {"6,3": 17 - v6_c4, "6,4": v6_c4,
               "7,1": 24 - v7_c2, "7,2": v7_c2}
    assert profile == {"6,3": 15, "6,4": 2, "7,1": 11, "7,2": 13}
    assert sum(int(key[0]) * count for key, count in profile.items()) == 270
    return {"max_high_edges_before_sat": 7,
            "seven_edge_degree_two_vertices": 1,
            "forced_low_profile": profile}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_audit(target: Path, motif_results):
    manifest = json.loads((target / "seven_edge_expected.json").read_text())
    records = manifest["cases"]
    by_name = {record["case"]: record for record in records}
    assert len(records) == len(by_name) == 50
    orbit_counts = {row["matching"]: row["orbits"] for row in motif_results}
    expected_names = {
        f"{matching}_{motif}_{pattern}"
        for matching in ("46", "10")
        for motif in range(orbit_counts[matching])
        for pattern in ("11", "12")
    }
    assert set(by_name) == expected_names
    for record in records:
        assert record["variables"] == 190190
        assert record["clauses"] == 525414
        for field in ("cnf_sha256", "drup_sha256"):
            assert len(record[field]) == 64
            int(record[field], 16)
    return {"cases": len(records), "clauses_per_case": 525414,
            "manifest_sha256": sha256(target / "seven_edge_expected.json"),
            "variables_per_case": 190190}


def validation_audit(path: Path, target: Path):
    expected = {
        record["case"]: record
        for record in json.loads((target / "seven_edge_expected.json").read_text())["cases"]
    }
    validation = json.loads(path.read_text())
    actual = {record["case"]: record for record in validation["cases"]}
    assert len(actual) == len(validation["cases"]) == 50
    assert set(actual) == set(expected)
    for name, record in actual.items():
        assert record["status"] == "UNSAT"
        assert record["checker_status"] == "VERIFIED"
        assert record["cnf_sha256"] == expected[name]["cnf_sha256"]
        assert record["proof_sha256"] == expected[name]["drup_sha256"]
    assert validation["verified_unsat"] == 50
    return {
        "all_cnf_hashes_match": True,
        "all_proof_hashes_match": True,
        "cases": 50,
        "validation_sha256": sha256(path),
        "verified_unsat": 50,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-dir", type=Path, default=DEFAULT_TARGET)
    parser.add_argument("--validation", type=Path)
    args = parser.parse_args()

    matching_counts = {}
    for matching in perfect_matchings(tuple(range(10))):
        if matching.isdisjoint(M):
            sizes = component_sizes(M | matching)
            matching_counts[sizes] = matching_counts.get(sizes, 0) + 1
    assert matching_counts == {(10,): 384, (4, 6): 160}

    motifs = [
        motif_audit("10", ((0, 1, 2, 3, 4),)),
        motif_audit("46", ((0, 1), (2, 3, 4))),
    ]
    assert [(x["automorphisms"], x["raw_motifs"], x["orbits"]) for x in motifs] == [
        (10, 160, 16), (24, 172, 9)
    ]

    result = {
        "arithmetic": arithmetic_audit(),
        "coverage": {"colored_matchings": {"10": 384, "4+6": 160},
                     "motifs": motifs},
        "manifest": manifest_audit(args.target_dir.resolve(), motifs),
    }
    if args.validation:
        result["fresh_validation"] = validation_audit(
            args.validation.resolve(), args.target_dir.resolve()
        )
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
