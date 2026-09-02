#!/usr/bin/env python3
"""Independent exact-geometry, witness, hitting-set, and CNF audit.

This file imports no code from list_kernel.py.  It reconstructs the strict
unit-distance graph through the older sibling exact-arithmetic implementation
and uses set-valued color lists and a separate hitting-set recursion.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path


N = 509
D = (310, 313, 316, 319, 322, 325)
TRIANGLE = (0, 149, 152)
STRICT_SHA = "5a95127767cb370f25f5865f057cab9b4a7ee9a72e2f73ad126ae390d71d487c"
REDUCED_SHA = "93f5ff096936613b61fcbdba3bca27addd5d59868c10561385c4ada7606d2305"


def load_exact_edges(criticality_dir: Path):
    module_path = criticality_dir / "parts509.py"
    spec = importlib.util.spec_from_file_location("older_exact_parts509", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    points, edges = module.load_graph(criticality_dir / "parts509.vtx")
    assert len(points) == N and len(set(points)) == N
    edges = sorted(edges)
    return edges


def digest(edges):
    data = "".join(f"{u} {v}\n" for u, v in sorted(edges)).encode("ascii")
    return hashlib.sha256(data).hexdigest()


def adjacencies(edges):
    adj = [set() for _ in range(N)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def decode(text):
    assert len(text) == N - len(D) and set(text) <= set("0123")
    colors = {}
    for vertex, symbol in zip((v for v in range(N) if v not in D), text, strict=True):
        colors[vertex] = int(symbol)
    return colors


def state(colors, adj):
    return tuple(
        frozenset(range(4)) - {colors[u] for u in adj[v]}
        for v in D
    )


def state_from_masks(masks):
    return tuple(frozenset(c for c in range(4) if mask & (1 << c)) for mask in masks)


def relabel(interface, permutation):
    return tuple(frozenset(permutation[c] for c in colors) for colors in interface)


def proper(colors, edges):
    return all(colors[u] != colors[v] for u, v in edges)


def independent_hitting_minimum(hyperedges, universe):
    edges = {frozenset(edge) for edge in hyperedges}
    edges = {edge for edge in edges if not any(other < edge for other in edges)}
    forced = set()
    while True:
        remaining = {edge for edge in edges if edge.isdisjoint(forced)}
        singleton_union = set().union(*(edge for edge in remaining if len(edge) == 1))
        if not singleton_union:
            edges = remaining
            break
        forced.update(singleton_union)

    seen = set()
    nodes = 0

    def search(remaining, budget):
        nonlocal nodes
        nodes += 1
        if not remaining:
            return frozenset()
        if budget == 0:
            return None
        key = (frozenset(remaining), budget)
        if key in seen:
            return None
        packing = []
        for edge in sorted(remaining, key=len):
            if all(edge.isdisjoint(old) for old in packing):
                packing.append(edge)
        if len(packing) > budget:
            seen.add(key)
            return None
        pivot = min(remaining, key=len)
        candidates = sorted(
            pivot,
            key=lambda vertex: -sum(vertex in edge for edge in remaining),
        )
        for vertex in candidates:
            residual = {edge for edge in remaining if vertex not in edge}
            answer = search(residual, budget - 1)
            if answer is not None:
                return answer | {vertex}
        seen.add(key)
        return None

    for extra in range(len(universe) - len(forced) + 1):
        result = search(edges, extra)
        if result is not None:
            return len(forced) + len(result), nodes
    raise AssertionError("no finite hitting set found")


def parse_dimacs(path):
    clauses = []
    header = None
    for line in path.read_text(encoding="ascii").splitlines():
        if not line or line.startswith("c"):
            continue
        if line.startswith("p "):
            _, kind, variables, count = line.split()
            assert kind == "cnf"
            header = (int(variables), int(count))
        else:
            values = [int(x) for x in line.split()]
            assert values[-1] == 0 and 0 not in values[:-1]
            clauses.append(tuple(values[:-1]))
    assert header is not None and header[1] == len(clauses)
    assert max(abs(x) for clause in clauses for x in clause) <= header[0]
    return header, Counter(tuple(sorted(clause)) for clause in clauses)


def audit_interface_cnf(path, cert, adj):
    header, actual = parse_dimacs(path)
    clauses = []
    cv = lambda v, c: 4 * v + c + 1
    av = lambda i, c: N * 4 + 4 * i + c + 1
    core = [v for v in range(N) if v not in D]
    edges = [tuple(e) for e in cert["base_internal_edges"]]
    edges += [tuple(e) for e in cert["selected_extra_edges"]]
    for v in core:
        clauses.append(tuple(cv(v, c) for c in range(4)))
        clauses.extend((-cv(v, c), -cv(v, d)) for c, d in itertools.combinations(range(4), 2))
    for u, v in edges:
        clauses.extend((-cv(u, c), -cv(v, c)) for c in range(4))
    clauses.extend((cv(v, c),) for c, v in enumerate(TRIANGLE))
    for i, v in enumerate(D):
        for color in range(4):
            clauses.extend((-av(i, color), -cv(u, color)) for u in sorted(adj[v]))
            clauses.append(tuple([av(i, color)] + [cv(u, color) for u in sorted(adj[v])]))
    representatives = [state_from_masks(row["available_masks"]) for row in cert["states"]]
    allowed = {
        relabel(interface, permutation)
        for interface in representatives
        for permutation in itertools.permutations(range(4))
    }
    for interface in sorted(allowed, key=lambda row: tuple(tuple(sorted(x)) for x in row)):
        clauses.append(
            tuple(
                -av(i, color) if color in interface[i] else av(i, color)
                for i in range(6)
                for color in range(4)
            )
        )
    expected = Counter(tuple(sorted(clause)) for clause in clauses)
    assert actual == expected
    assert header == (cert["interface_cnf"]["variables"], cert["interface_cnf"]["clauses"])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == cert["interface_cnf"]["sha256"]


def audit_lower_cnf(path, cert):
    header, actual = parse_dimacs(path)
    clauses = [tuple(index + 1 for index in row["violated_extra_indices"]) for row in cert["constraints"]]
    n, bound = len(cert["extra_edges"]), 13
    width = bound + 2
    z = lambda i, j: n + 1 + i * width + j
    clauses.append((z(0, 0),))
    clauses.extend((-z(0, j),) for j in range(1, width))
    for i, variable in enumerate(range(1, n + 1), 1):
        clauses.extend(((-z(i, 0), z(i - 1, 0)), (-z(i - 1, 0), z(i, 0))))
        for j in range(1, width):
            current, above, diagonal = z(i, j), z(i - 1, j), z(i - 1, j - 1)
            clauses.extend(
                (
                    (-current, above, diagonal),
                    (-current, above, variable),
                    (-above, current),
                    (-diagonal, -variable, current),
                )
            )
    clauses.append((-z(n, bound + 1),))
    expected = Counter(tuple(sorted(clause)) for clause in clauses)
    assert actual == expected
    assert header == (cert["lower13_cnf"]["variables"], cert["lower13_cnf"]["clauses"])
    assert hashlib.sha256(path.read_bytes()).hexdigest() == cert["lower13_cnf"]["sha256"]
    # Exhaust the four Boolean variables in the recurrence's local gate.
    for current, above, diagonal, variable in itertools.product((False, True), repeat=4):
        gate_clauses = (
            (not current or above or diagonal),
            (not current or above or variable),
            (not above or current),
            (not diagonal or not variable or current),
        )
        assert all(gate_clauses) == (current == (above or (diagonal and variable)))


def main():
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--certificate", type=Path, default=here / "certificate.json")
    ap.add_argument(
        "--criticality-dir",
        type=Path,
        default=here.parent / "hadwiger_nelson_parts509_criticality",
    )
    ap.add_argument("--interface-cnf", type=Path)
    ap.add_argument("--lower-cnf", type=Path)
    args = ap.parse_args()
    cert = json.loads(args.certificate.read_text())
    edges = load_exact_edges(args.criticality_dir)
    assert len(edges) == 2442 and digest(edges) == STRICT_SHA
    adj = adjacencies(edges)
    assert tuple(v for v in range(N) if len(adj[v]) == 4) == D
    base = [tuple(e) for e in cert["base_internal_edges"]]
    extras = [tuple(e) for e in cert["extra_edges"]]
    incident = [edge for edge in edges if set(edge) & set(D)]
    assert len(base) == 2235 and len(extras) == 183 and len(incident) == 24
    assert digest(base + incident) == REDUCED_SHA
    assert set(base).isdisjoint(extras)
    assert set(base) | set(extras) | set(incident) == set(edges)

    representatives = set()
    for row in cert["states"]:
        colors = decode(row["core_coloring"])
        expected = state_from_masks(row["available_masks"])
        assert proper(colors, set(edges) - set(incident))
        assert state(colors, adj) == expected
        representatives.add(expected)
    assert len(representatives) == 22
    allowed = {
        relabel(interface, permutation)
        for interface in representatives
        for permutation in itertools.permutations(range(4))
    }
    assert len(allowed) == 528

    hyperedges = []
    for row in cert["constraints"]:
        colors = decode(row["core_coloring"])
        assert proper(colors, base)
        actual_state = state(colors, adj)
        assert actual_state == state_from_masks(row["available_masks"])
        assert actual_state not in allowed
        violations = tuple(i for i, (u, v) in enumerate(extras) if colors[u] == colors[v])
        assert violations == tuple(row["violated_extra_indices"])
        hyperedges.append(violations)
    chosen = set(cert["selected_extra_indices"])
    assert len(chosen) == 14 and all(chosen.intersection(edge) for edge in hyperedges)
    optimum, nodes = independent_hitting_minimum(hyperedges, range(len(extras)))
    assert optimum == 14

    if args.interface_cnf:
        audit_interface_cnf(args.interface_cnf, cert, adj)
    if args.lower_cnf:
        audit_lower_cnf(args.lower_cnf, cert)
    print("exact_unit_edges=2442")
    print("reduced_core_edges=2259")
    print("states_mod_S4=22")
    print("labeled_states=528")
    print("hitting_constraints=144")
    print(f"independent_hitting_number={optimum}")
    print(f"independent_branch_nodes={nodes}")
    print(f"interface_cnf_audited={bool(args.interface_cnf)}")
    print(f"lower13_cnf_audited={bool(args.lower_cnf)}")
    print("PASSED")


if __name__ == "__main__":
    main()
