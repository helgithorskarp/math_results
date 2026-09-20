#!/usr/bin/env python3
"""Optional CP-SAT discovery generator for simultaneous 2/11-growable seeds."""

from __future__ import annotations

import argparse
import json
from ortools.sat.python import cp_model

SUPPORT = (1, 2, 11)


def length(i: int, j: int, n: int) -> int:
    difference = abs(i - j)
    return min(difference, n - difference)


def changes(i: int, j: int, width: int, cut: int, n: int) -> bool:
    ii = i if i <= cut else i + width
    jj = j if j <= cut else j + width
    return length(ii, jj, n + width) > length(i, j, n)


def solve(counts: tuple[int, int, int], seconds: float) -> dict[str, object]:
    n = sum(counts) + 1
    dummy = n
    model = cp_model.CpModel()
    arcs = {}
    edges = {}
    circuit = []
    for i in range(n):
        for j in range(i + 1, n):
            if length(i, j, n) in SUPPORT:
                forward = model.new_bool_var(f"a_{i}_{j}")
                backward = model.new_bool_var(f"a_{j}_{i}")
                used = model.new_bool_var(f"e_{i}_{j}")
                arcs[i, j] = forward
                arcs[j, i] = backward
                edges[i, j] = used
                model.add(used == forward + backward)
                circuit.extend(((i, j, forward), (j, i, backward)))
        to_dummy = model.new_bool_var(f"a_{i}_D")
        from_dummy = model.new_bool_var(f"a_D_{i}")
        arcs[i, dummy] = to_dummy
        arcs[dummy, i] = from_dummy
        circuit.extend(((i, dummy, to_dummy), (dummy, i, from_dummy)))
    model.add_circuit(circuit)
    for edge_length, target in zip(SUPPORT, counts):
        model.add(sum(edge for pair, edge in edges.items() if length(*pair, n) == edge_length) == target)

    choices = {}
    for width in (2, 11):
        width_choices = []
        for cut in range(width - 1, n - width):
            choice = model.new_bool_var(f"g_{width}_{cut}")
            choices[width, cut] = choice
            width_choices.append(choice)
            critical = set(range(cut - width + 1, cut + 1))
            changed = [(i, j, edge) for (i, j), edge in edges.items() if changes(i, j, width, cut, n)]
            for vertex in critical:
                model.add(sum(edge for i, j, edge in changed if vertex in (i, j)) == 1).only_enforce_if(choice)
            for i, j, edge in changed:
                if i not in critical and j not in critical:
                    model.add(edge == 0).only_enforce_if(choice)
        model.add_exactly_one(width_choices)

    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = seconds
    solver.parameters.num_search_workers = 1
    solver.parameters.random_seed = 1
    status = solver.solve(model)
    result: dict[str, object] = {"counts": list(counts), "status": solver.status_name(status)}
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return result
    successor = {i: j for (i, j), arc in arcs.items() if solver.value(arc)}
    path = []
    at = successor[dummy]
    while at != dummy:
        path.append(at)
        at = successor[at]
    result["path"] = path
    result["growth"] = {
        str(width): next(cut for (candidate, cut), choice in choices.items() if candidate == width and solver.value(choice))
        for width in (2, 11)
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--counts", type=int, nargs=3, required=True)
    parser.add_argument("--seconds", type=float, default=300.0)
    args = parser.parse_args()
    print(json.dumps(solve(tuple(args.counts), args.seconds), separators=(",", ":"), sort_keys=True))


if __name__ == "__main__":
    main()
