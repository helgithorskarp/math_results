#!/usr/bin/env python3
"""Solver-free checker for the unique Parts-509 degree-four interface kernel."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable


N = 509
K = 4
D = (310, 313, 316, 319, 322, 325)
OPTIMUM = 14
STRICT_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def edge_hash(edges: Iterable[tuple[int, int]]) -> str:
    payload = "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode("ascii")
    return hashlib.sha256(payload).hexdigest()


def exact_at_most(variables: list[int], bound: int, start_variable: int) -> list[list[int]]:
    width = bound + 2

    def threshold(i: int, j: int) -> int:
        return start_variable + i * width + j

    clauses = [[threshold(0, 0)]]
    clauses.extend([[-threshold(0, j)] for j in range(1, width)])
    for i, variable in enumerate(variables, 1):
        current = threshold(i, 0)
        above = threshold(i - 1, 0)
        clauses.extend([[-current, above], [-above, current]])
        for j in range(1, width):
            current = threshold(i, j)
            above = threshold(i - 1, j)
            diagonal = threshold(i - 1, j - 1)
            clauses.extend([
                [-current, above, diagonal],
                [-current, above, variable],
                [-above, current],
                [-diagonal, -variable, current],
            ])
    clauses.append([-threshold(len(variables), bound + 1)])
    return clauses


def verify_threshold_gate() -> None:
    """Truth-table check the local Tseitin gate c iff a or (d and x)."""
    clauses = [
        [-4, 1, 2],
        [-4, 1, 3],
        [-1, 4],
        [-2, -3, 4],
    ]
    for values in itertools.product((False, True), repeat=4):
        relation = values[3] == (values[0] or (values[1] and values[2]))
        satisfies = all(
            any(values[abs(lit) - 1] == (lit > 0) for lit in clause)
            for clause in clauses
        )
        assert satisfies == relation


def dimacs_bytes(clauses: list[list[int]]) -> tuple[bytes, int]:
    variables = max(abs(lit) for clause in clauses for lit in clause)
    lines = [f"p cnf {variables} {len(clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in clauses)
    return ("\n".join(lines) + "\n").encode("ascii"), variables


def minimal_masks(edges: Iterable[int]) -> tuple[int, ...]:
    answer: list[int] = []
    for edge in sorted(set(edges), key=lambda value: (value.bit_count(), value)):
        if not any(old & edge == old for old in answer):
            answer.append(edge)
    return tuple(answer)


def enumerate_transversals(hyperedges: list[tuple[int, ...]]) -> tuple[set[tuple[int, ...]], int]:
    """Exhaustively partition all hitting sets of cardinality at most OPTIMUM."""
    initial = minimal_masks(sum(1 << i for i in edge) for edge in hyperedges)
    solutions: set[tuple[int, ...]] = set()
    nodes = 0

    def propagate(
        edges: tuple[int, ...], chosen: int, forbidden: int
    ) -> tuple[tuple[int, ...], int] | None:
        while True:
            available = [edge & ~forbidden for edge in edges if not edge & chosen]
            if any(edge == 0 for edge in available):
                return None
            available = list(minimal_masks(available))
            units = 0
            for edge in available:
                if edge.bit_count() == 1:
                    units |= edge
            new_units = units & ~chosen
            if not new_units:
                return tuple(available), chosen
            chosen |= new_units
            if chosen.bit_count() > OPTIMUM:
                return None

    def search(edges: tuple[int, ...], chosen: int, forbidden: int) -> None:
        nonlocal nodes
        nodes += 1
        reduced = propagate(edges, chosen, forbidden)
        if reduced is None:
            return
        edges, chosen = reduced
        budget = OPTIMUM - chosen.bit_count()
        if not edges:
            if budget != 0:
                raise AssertionError("source instance has a transversal below the stated optimum")
            solution = tuple(i for i in range(183) if chosen & (1 << i))
            assert solution not in solutions
            solutions.add(solution)
            return
        used = 0
        packing = 0
        for edge in sorted(edges, key=int.bit_count):
            if not edge & used:
                used |= edge
                packing += 1
        if packing > budget:
            return
        pivot = min(edges, key=lambda edge: (edge.bit_count(), edge))
        choices = [1 << i for i in range(183) if pivot & (1 << i)]
        choices.sort(key=lambda bit: (-sum(bool(edge & bit) for edge in edges), bit))
        earlier = 0
        for bit in choices:
            search(edges, chosen | bit, forbidden | earlier)
            earlier |= bit

    search(initial, 0, 0)
    return solutions, nodes


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(1 << permutation[c] for c in range(K) if mask & (1 << c))


def orbit(state: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        tuple(permute_mask(mask, permutation) for mask in state)
        for permutation in itertools.permutations(range(K))
    }


def decode_core_coloring(text: str) -> list[int]:
    core = [v for v in range(N) if v not in set(D)]
    assert len(text) == len(core) == 503 and set(text) <= set("0123")
    colors = [-1] * N
    for vertex, symbol in zip(core, text, strict=True):
        colors[vertex] = int(symbol)
    return colors


def available_state(colors: list[int], neighborhoods: dict[int, list[int]]) -> tuple[int, ...]:
    return tuple(
        sum(1 << c for c in range(K) if c not in {colors[u] for u in neighborhoods[v]})
        for v in D
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--completeness-cnf", type=Path)
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    source_dir = here.parent / "hadwiger_nelson_parts509_degree4_list_kernel"
    edge_path = here.parent / "hadwiger_nelson_parts509_degree10_replacements" / "edges.json"
    certificate_path = here / "certificate.json"
    source_path = source_dir / "certificate.json"
    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    source = json.loads(source_path.read_text(encoding="utf-8"))
    assert cert["format"] == "parts509-degree4-unique-kernel-v1"
    assert sha256(source_path) == cert["source_certificate_sha256"]

    strict_edges = sorted(tuple(map(int, edge)) for edge in json.loads(edge_path.read_text()))
    assert len(strict_edges) == len(set(strict_edges)) == 2442
    assert edge_hash(strict_edges) == STRICT_EDGE_SHA256
    base = [tuple(edge) for edge in source["base_internal_edges"]]
    extras = [tuple(edge) for edge in source["extra_edges"]]
    assert len(base) == 2235 and len(extras) == 183
    hyperedges = [tuple(row["violated_extra_indices"]) for row in source["constraints"]]
    assert len(hyperedges) == 144

    declared = {tuple(row) for row in cert["minimum_transversals"]}
    assert len(declared) == cert["minimum_transversal_count"] == 42
    assert all(len(row) == len(set(row)) == OPTIMUM for row in declared)
    assert all(all(set(row) & set(edge) for edge in hyperedges) for row in declared)
    computed, nodes = enumerate_transversals(hyperedges)
    assert computed == declared

    completeness_clauses = [[i + 1 for i in edge] for edge in hyperedges]
    completeness_clauses.extend(
        exact_at_most(list(range(1, 184)), OPTIMUM, 184)
    )
    completeness_clauses.extend(
        [[-(i + 1) for i in model] for model in sorted(declared)]
    )
    cnf_bytes, cnf_variables = dimacs_bytes(completeness_clauses)
    expected_cnf = cert["completeness_cnf"]
    assert cnf_variables == expected_cnf["variables"] == 3127
    assert len(completeness_clauses) == expected_cnf["clauses"] == 11549
    assert hashlib.sha256(cnf_bytes).hexdigest() == expected_cnf["sha256"]
    verify_threshold_gate()
    if args.completeness_cnf is not None:
        assert args.completeness_cnf.read_bytes() == cnf_bytes

    winner = tuple(cert["unique_full_interface_kernel"])
    assert winner == tuple(source["selected_extra_indices"])
    assert winner in declared
    losers = declared - {winner}
    representatives = {tuple(row["available_masks"]) for row in source["states"]}
    allowed = set().union(*(orbit(state) for state in representatives))
    neighborhoods = {
        int(v): list(map(int, ns))
        for v, ns in source["terminal_neighborhoods"].items()
    }
    strict_set = set(strict_edges)
    assert set(base) | set(extras) == strict_set - {
        edge for edge in strict_set if set(edge) & set(D)
    }

    covered: set[tuple[int, ...]] = set()
    for witness in cert["failure_witnesses"]:
        colors = decode_core_coloring(witness["core_coloring"])
        state = available_state(colors, neighborhoods)
        assert state == tuple(witness["forbidden_state"])
        assert state not in allowed
        failures = {tuple(row) for row in witness["failed_transversals"]}
        assert failures <= losers and not failures & covered
        for indices in failures:
            candidate_edges = base + [extras[i] for i in indices]
            assert all(colors[u] != colors[v] for u, v in candidate_edges)
        covered |= failures
    assert covered == losers

    print(f"source_hyperedges_verified={len(hyperedges)}")
    print(f"solver_free_search_nodes={nodes}")
    print(f"minimum_transversals_verified={len(computed)}")
    print(f"completeness_cnf_sha256={expected_cnf['sha256']}")
    print("threshold_gate_truth_table_verified=true")
    print(f"failed_transversals_verified={len(covered)}")
    print("unique_full_interface_kernel_verified=true")
    print("PASSED")


if __name__ == "__main__":
    main()
