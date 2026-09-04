#!/usr/bin/env python3
"""Definition-level checks of centralizer relabeling on arbitrary colorings.

The general existence proof is in README.md. These deterministic tests
exercise its constructive relabeling without assuming the Ramsey property.
"""
from __future__ import annotations

import itertools
import random

from generate_formula import BASE, CASES, symmetry_clauses


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def audit_case(case):
    mapping, _ = BASE.edge_mapping(case)
    cycles = BASE.vertex_cycles(case)
    successor = list(range(43))
    for cycle in cycles:
        for i, vertex in enumerate(cycle):
            successor[vertex] = cycle[(i + 1) % len(cycle)]
    variables = max(mapping.values())
    clauses = symmetry_clauses(case)
    rng = random.Random(90543)
    assignments = [[0] * (variables + 1), [1] * (variables + 1)]
    assignments += [[0] + [rng.randrange(2) for _ in range(variables)]
                    for _ in range(100)]
    for values in assignments:
        def edge(u, v):
            return values[mapping[min(u, v), max(u, v)]]

        def profile(cycle):
            return tuple(edge(cycle[0], cycle[d])
                         for d in range(1, (len(cycle) + 1) // 2))

        # p maps new labels to old labels. Only equal-length cycles are moved.
        p = list(range(43))
        for length in (9, 3):
            slots = [cycle for cycle in cycles if len(cycle) == length]
            ordered = sorted(slots, key=profile)
            for slot, old in zip(slots, ordered, strict=True):
                for v, w in zip(slot, old, strict=True):
                    p[v] = w
        for cycle in cycles:
            if cycle[0] == 0 or len(cycle) == 1:
                continue
            old = [p[v] for v in cycle]
            shift = min(range(len(cycle)), key=lambda s: tuple(
                edge(p[0], old[(j + s) % len(cycle)]) for j in range(len(cycle))))
            for j, v in enumerate(cycle):
                p[v] = old[(j + shift) % len(cycle)]
        require(sorted(p) == list(range(43)), "not a permutation")
        require(all(p[successor[v]] == successor[p[v]] for v in range(43)),
                "relabeling does not centralize the generator")
        new_values = {}
        for (u, v), variable in mapping.items():
            value = edge(p[u], p[v])
            require(variable not in new_values or new_values[variable] == value,
                    "relabeling broke pair-orbit invariance")
            new_values[variable] = value
        require(all(any(new_values[abs(lit)] == int(lit > 0) for lit in clause)
                    for clause in clauses), "normalization fails a clause")
        # The entire relabeled graph, not merely its counts, has been checked.
        require(all(new_values[var] == edge(p[u], p[v])
                    for (u, v), var in mapping.items()), "edge mismatch")
    print(f"PASS case={case} arbitrary_colorings={len(assignments)} "
          "permutation_and_all_903_edges_verified=true")


def main():
    # Burnside counts supply a separate check on the local word census.
    for length, expected in ((3, 4), (9, 60)):
        representatives = set()
        for word in itertools.product((0, 1), repeat=length):
            representatives.add(min(word[s:] + word[:s] for s in range(length)))
        require(len(representatives) == expected, "necklace count differs")
        print(f"PASS binary_necklaces length={length} count={expected}")
    for case in CASES:
        audit_case(case)
    # Recompute the full power filter, independently of the earlier CASES list.
    survivors = {(a, b, 43 - 9*a - 3*b) for a in range(1, 5) for b in range(15)
                 if 9*a + 3*b <= 43 and 3*a >= 7}
    earlier = {(3, b, 16 - 3*b) for b in range(5)} | {(4, 0, 7), (4, 1, 4)}
    require(survivors == earlier | set(CASES), "full type coverage differs")
    require(not earlier.intersection(CASES), "residual cases overlap")
    print("PASS power_survivors=9 earlier_exclusions=7 residual_exclusions=2 open_types=0")


if __name__ == "__main__":
    main()
