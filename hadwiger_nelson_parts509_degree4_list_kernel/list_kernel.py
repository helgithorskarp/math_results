#!/usr/bin/env python3
"""Verify and regenerate proof inputs for the Parts-509 degree-4 list kernel.

The compact certificate contains positive colorings for all allowed list states
and counterexample colorings defining a finite hitting-set lower bound.  This
program verifies those witnesses directly and regenerates the two CNFs whose
UNSAT proof traces stay under /scratch.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
from typing import Iterable, Sequence


N = 509
K = 4
DEGREE_FOUR = (310, 313, 316, 319, 322, 325)
PINNED_TRIANGLE = (0, 149, 152)
STRICT_EDGE_SHA256 = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
REDUCED_EDGE_SHA256 = "93f5ff096936613b61fcbdba3bca27addd5d59868c10561385c4ada7606d2305"
FORMAT = "parts509-degree4-list-kernel-v1"
AVAIL_OFFSET = N * K


def color_var(vertex: int, color: int) -> int:
    return K * vertex + color + 1


def avail_var(index: int, color: int) -> int:
    return AVAIL_OFFSET + K * index + color + 1


def canonical_edge_bytes(edges: Iterable[tuple[int, int]]) -> bytes:
    return "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode("ascii")


def edge_hash(edges: Iterable[tuple[int, int]]) -> str:
    return hashlib.sha256(canonical_edge_bytes(edges)).hexdigest()


def load_edges(path: Path) -> list[tuple[int, int]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    edges = sorted(tuple(sorted(map(int, edge))) for edge in raw)
    assert len(edges) == len(set(edges)) == 2442
    assert edge_hash(edges) == STRICT_EDGE_SHA256
    assert all(0 <= u < v < N for u, v in edges)
    return edges


def adjacency(edges: Sequence[tuple[int, int]]) -> list[set[int]]:
    adj = [set() for _ in range(N)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def permute_mask(mask: int, permutation: tuple[int, ...]) -> int:
    return sum(1 << permutation[c] for c in range(K) if mask & (1 << c))


def orbit(state: tuple[int, ...]) -> set[tuple[int, ...]]:
    return {
        tuple(permute_mask(mask, permutation) for mask in state)
        for permutation in itertools.permutations(range(K))
    }


def decode_core_coloring(text: str) -> list[int]:
    core = [v for v in range(N) if v not in set(DEGREE_FOUR)]
    assert len(text) == len(core)
    assert set(text) <= set("0123")
    colors = [-1] * N
    for vertex, symbol in zip(core, text, strict=True):
        colors[vertex] = int(symbol)
    return colors


def available_state(colors: Sequence[int], adj: Sequence[set[int]]) -> tuple[int, ...]:
    return tuple(
        sum(1 << c for c in range(K) if c not in {colors[u] for u in adj[v]})
        for v in DEGREE_FOUR
    )


def proper(colors: Sequence[int], edges: Iterable[tuple[int, int]]) -> bool:
    return all(colors[u] != colors[v] for u, v in edges)


def remove_dominated(hyperedges: Iterable[int]) -> tuple[int, ...]:
    minimal: list[int] = []
    for edge in sorted(set(hyperedges), key=lambda value: (value.bit_count(), value)):
        if not any(old & edge == old for old in minimal):
            minimal.append(edge)
    return tuple(minimal)


def hitting_number(hyperedges: Iterable[Iterable[int]], universe_size: int) -> tuple[int, int]:
    """Exact solver-free branch-and-bound; return optimum and searched nodes."""
    masks = remove_dominated(
        sum(1 << element for element in edge) for edge in hyperedges
    )
    forced = 0
    while True:
        remaining = tuple(edge for edge in masks if not edge & forced)
        singletons = [edge for edge in remaining if edge.bit_count() == 1]
        if not singletons:
            masks = remaining
            break
        for edge in singletons:
            forced |= edge

    memo: dict[tuple[tuple[int, ...], int], bool] = {}
    nodes = 0

    def feasible(edges: tuple[int, ...], budget: int) -> bool:
        nonlocal nodes
        nodes += 1
        if not edges:
            return True
        if budget <= 0:
            return False
        key = (edges, budget)
        if key in memo:
            return memo[key]
        used = 0
        packing = 0
        for edge in sorted(edges, key=int.bit_count):
            if not edge & used:
                used |= edge
                packing += 1
        if packing > budget:
            memo[key] = False
            return False
        pivot = min(edges, key=int.bit_count)
        choices = [1 << i for i in range(universe_size) if pivot & (1 << i)]
        choices.sort(key=lambda bit: -sum(bool(edge & bit) for edge in edges))
        for bit in choices:
            residual = tuple(edge for edge in edges if not edge & bit)
            if feasible(residual, budget - 1):
                memo[key] = True
                return True
        memo[key] = False
        return False

    forced_count = forced.bit_count()
    for extra in range(universe_size - forced_count + 1):
        if feasible(masks, extra):
            return forced_count + extra, nodes
    raise AssertionError("finite hitting instance has no hitting set")


def verify_certificate(edge_path: Path, certificate_path: Path) -> dict[str, int]:
    strict_edges = load_edges(edge_path)
    strict_set = set(strict_edges)
    adj = adjacency(strict_edges)
    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    assert cert["format"] == FORMAT
    assert tuple(cert["degree_four_vertices"]) == DEGREE_FOUR
    assert tuple(v for v in range(N) if len(adj[v]) == 4) == DEGREE_FOUR
    assert all(not (adj[v] & set(DEGREE_FOUR)) for v in DEGREE_FOUR)
    assert {
        str(v): sorted(adj[v]) for v in DEGREE_FOUR
    } == cert["terminal_neighborhoods"]

    base_internal = [tuple(edge) for edge in cert["base_internal_edges"]]
    extras = [tuple(edge) for edge in cert["extra_edges"]]
    selected_indices = tuple(cert["selected_extra_indices"])
    selected = [extras[i] for i in selected_indices]
    incident = sorted(edge for edge in strict_edges if set(edge) & set(DEGREE_FOUR))
    internal_strict = set(strict_edges) - set(incident)
    assert len(incident) == 24
    assert len(base_internal) == len(set(base_internal)) == 2235
    assert len(extras) == len(set(extras)) == 183
    assert set(base_internal) | set(extras) == internal_strict
    assert not (set(base_internal) & set(extras))
    reduced = sorted(set(base_internal) | set(incident))
    assert len(reduced) == 2259
    assert edge_hash(reduced) == REDUCED_EDGE_SHA256
    assert len(selected_indices) == len(set(selected_indices)) == 14
    assert selected == [tuple(edge) for edge in cert["selected_extra_edges"]]

    representatives: set[tuple[int, ...]] = set()
    for row in cert["states"]:
        state = tuple(row["available_masks"])
        assert state == min(orbit(state))
        assert len(orbit(state)) == 24
        assert tuple(row["available_sizes"]) == tuple(mask.bit_count() for mask in state)
        colors = decode_core_coloring(row["core_coloring"])
        assert proper(colors, internal_strict)
        assert available_state(colors, adj) == state
        representatives.add(state)
    assert len(representatives) == cert["states_mod_color_permutation"] == 22
    allowed = set().union(*(orbit(state) for state in representatives))
    assert len(allowed) == cert["labeled_states"] == 528
    availability_distribution = Counter(sum(mask.bit_count() for mask in state) for state in representatives)
    assert availability_distribution == Counter({6: 4, 7: 6, 8: 12})

    hyperedges = []
    for row in cert["constraints"]:
        colors = decode_core_coloring(row["core_coloring"])
        assert proper(colors, base_internal)
        state = available_state(colors, adj)
        assert state == tuple(row["available_masks"])
        assert state not in allowed
        violated = tuple(i for i, (u, v) in enumerate(extras) if colors[u] == colors[v])
        assert violated == tuple(row["violated_extra_indices"])
        assert violated
        hyperedges.append(violated)
    assert len(hyperedges) == cert["hitting_constraints"] == 144
    assert all(set(edge) & set(selected_indices) for edge in hyperedges)
    optimum, nodes = hitting_number(hyperedges, len(extras))
    assert optimum == cert["minimum_extra_edges"] == 14

    print("strict_unit_edge_manifest_verified=true")
    print("reduced_2259_edge_core_verified=true")
    print("allowed_states_verified=22_mod_S4_528_labeled")
    print("counterexample_coloring_constraints_verified=144")
    print(f"solver_free_hitting_number={optimum}")
    print(f"solver_free_branch_nodes={nodes}")
    print("selected_interface_edges=14")
    print("all_checks=true")
    return {"optimum": optimum, "nodes": nodes}


def graph_coloring_clauses(
    vertices: Iterable[int], edges: Iterable[tuple[int, int]]
) -> list[list[int]]:
    clauses: list[list[int]] = []
    for vertex in vertices:
        clauses.append([color_var(vertex, c) for c in range(K)])
        for c, d in itertools.combinations(range(K), 2):
            clauses.append([-color_var(vertex, c), -color_var(vertex, d)])
    for u, v in edges:
        for c in range(K):
            clauses.append([-color_var(u, c), -color_var(v, c)])
    return clauses


def list_reification_clauses(adj: Sequence[set[int]]) -> list[list[int]]:
    clauses: list[list[int]] = []
    for i, vertex in enumerate(DEGREE_FOUR):
        for color in range(K):
            available = avail_var(i, color)
            for neighbor in sorted(adj[vertex]):
                clauses.append([-available, -color_var(neighbor, color)])
            clauses.append(
                [available] + [color_var(neighbor, color) for neighbor in sorted(adj[vertex])]
            )
    return clauses


def state_block(state: tuple[int, ...]) -> list[int]:
    return [
        -avail_var(i, c) if state[i] & (1 << c) else avail_var(i, c)
        for i in range(len(DEGREE_FOUR))
        for c in range(K)
    ]


def exact_at_most(
    variables: Sequence[int], bound: int, start_variable: int
) -> list[list[int]]:
    """Tseitin encode exact recurrence z[i,j] = [sum(x[:i]) >= j]."""
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
            # current iff above OR (diagonal AND variable).
            clauses.extend(
                [
                    [-current, above, diagonal],
                    [-current, above, variable],
                    [-above, current],
                    [-diagonal, -variable, current],
                ]
            )
    clauses.append([-threshold(len(variables), bound + 1)])
    return clauses


def write_dimacs(path: Path, clauses: Sequence[Sequence[int]]) -> tuple[int, int, str]:
    variables = max(abs(literal) for clause in clauses for literal in clause)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii") as handle:
        handle.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            handle.write(" ".join(map(str, clause)) + " 0\n")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return variables, len(clauses), digest


def generate_cnfs(edge_path: Path, certificate_path: Path, scratch: Path) -> None:
    strict_edges = load_edges(edge_path)
    adj = adjacency(strict_edges)
    cert = json.loads(certificate_path.read_text(encoding="utf-8"))
    base_internal = [tuple(edge) for edge in cert["base_internal_edges"]]
    extras = [tuple(edge) for edge in cert["extra_edges"]]
    selected = [extras[i] for i in cert["selected_extra_indices"]]
    representatives = {tuple(row["available_masks"]) for row in cert["states"]}
    allowed = set().union(*(orbit(state) for state in representatives))
    core = [v for v in range(N) if v not in set(DEGREE_FOUR)]
    interface = graph_coloring_clauses(core, base_internal + selected)
    interface.extend([[color_var(v, c)] for c, v in enumerate(PINNED_TRIANGLE)])
    interface.extend(list_reification_clauses(adj))
    interface.extend(state_block(state) for state in sorted(allowed))
    interface_path = scratch / "kernel_interface.cnf"
    interface_summary = write_dimacs(interface_path, interface)

    hyperedges = [row["violated_extra_indices"] for row in cert["constraints"]]
    lower = [[index + 1 for index in edge] for edge in hyperedges]
    lower.extend(exact_at_most(list(range(1, len(extras) + 1)), 13, len(extras) + 1))
    lower_path = scratch / "kernel_lower13.cnf"
    lower_summary = write_dimacs(lower_path, lower)
    assert interface_summary == (
        cert["interface_cnf"]["variables"],
        cert["interface_cnf"]["clauses"],
        cert["interface_cnf"]["sha256"],
    )
    assert lower_summary == (
        cert["lower13_cnf"]["variables"],
        cert["lower13_cnf"]["clauses"],
        cert["lower13_cnf"]["sha256"],
    )
    print(f"interface_cnf_variables={interface_summary[0]}")
    print(f"interface_cnf_clauses={interface_summary[1]}")
    print(f"interface_cnf_sha256={interface_summary[2]}")
    print(f"lower13_cnf_variables={lower_summary[0]}")
    print(f"lower13_cnf_clauses={lower_summary[1]}")
    print(f"lower13_cnf_sha256={lower_summary[2]}")
    print("cnf_regeneration_verified=true")


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--edges",
        type=Path,
        default=here.parent / "hadwiger_nelson_parts509_degree10_replacements" / "edges.json",
    )
    parser.add_argument("--certificate", type=Path, default=here / "certificate.json")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("verify")
    generate = subparsers.add_parser("generate-cnfs")
    generate.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()
    verify_certificate(args.edges, args.certificate)
    if args.command == "generate-cnfs":
        generate_cnfs(args.edges, args.certificate, args.scratch)


if __name__ == "__main__":
    main()
