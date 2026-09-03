#!/usr/bin/env python3
"""Deterministic CP-SAT generator for growable BHR path witnesses."""

from __future__ import annotations

from collections import Counter

from ortools.sat.python import cp_model

from verify import U, bdiff, verify_growth


def solve(
    counts_tuple: tuple[int, int, int],
    required: tuple[int, ...],
    seconds: float = 10.0,
) -> tuple[dict[str, object] | None, str]:
    counts = dict(zip(U, counts_tuple))
    n = sum(counts_tuple) + 1
    dummy = n
    model = cp_model.CpModel()

    # A directed Hamiltonian circuit through the n labels and a dummy node.
    # Removing the dummy and its two incident arcs leaves an oriented path.
    arcs: dict[tuple[int, int], cp_model.IntVar] = {}
    edge_vars: dict[tuple[int, int], cp_model.IntVar] = {}
    circuit = []
    for i in range(n):
        for j in range(i + 1, n):
            if bdiff(i, j, n) in counts:
                aij = model.new_bool_var(f"a_{i}_{j}")
                aji = model.new_bool_var(f"a_{j}_{i}")
                eij = model.new_bool_var(f"e_{i}_{j}")
                arcs[i, j] = aij
                arcs[j, i] = aji
                edge_vars[i, j] = eij
                model.add(eij == aij + aji)
                circuit.extend(((i, j, aij), (j, i, aji)))
        to_dummy = model.new_bool_var(f"a_{i}_D")
        from_dummy = model.new_bool_var(f"a_D_{i}")
        arcs[i, dummy] = to_dummy
        arcs[dummy, i] = from_dummy
        circuit.extend(((i, dummy, to_dummy), (dummy, i, from_dummy)))
    model.add_circuit(circuit)

    for length, target in counts.items():
        model.add(
            sum(e for (i, j), e in edge_vars.items() if bdiff(i, j, n) == length)
            == target
        )

    growth_choice: dict[tuple[int, int], cp_model.IntVar] = {}
    for x in required:
        choices = []
        for m in range(x - 1, n - x):
            g = model.new_bool_var(f"grow_{x}_{m}")
            growth_choice[x, m] = g
            choices.append(g)
            interval = set(range(m - x + 1, m + 1))
            stretched = []
            for (i, j), edge in edge_vars.items():
                old = bdiff(i, j, n)
                ii = i if i <= m else i + x
                jj = j if j <= m else j + x
                if bdiff(ii, jj, n + x) != old:
                    stretched.append((i, j, edge))
            for y in interval:
                model.add(
                    sum(edge for i, j, edge in stretched if y in (i, j)) == 1
                ).only_enforce_if(g)
            for i, j, edge in stretched:
                if i not in interval and j not in interval:
                    model.add(edge == 0).only_enforce_if(g)
        if not choices:
            return None, "INFEASIBLE"
        model.add_exactly_one(choices)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 1
    status = solver.solve(model)
    status_name = solver.status_name(status)
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None, status_name

    successor = {}
    for (i, j), arc in arcs.items():
        if solver.value(arc):
            successor[i] = j
    path = []
    at = successor[dummy]
    while at != dummy:
        path.append(at)
        at = successor[at]
    growth = {
        x: next(
            m
            for (xx, m), choice in growth_choice.items()
            if xx == x and solver.value(choice)
        )
        for x in required
    }

    actual = Counter(bdiff(i, j, n) for i, j in zip(path, path[1:]))
    if actual != Counter(counts):
        raise RuntimeError("internal edge-count decoding failure")
    for x, m in growth.items():
        verify_growth(path, x, m)
    return {"path": path, "growth": growth}, status_name
