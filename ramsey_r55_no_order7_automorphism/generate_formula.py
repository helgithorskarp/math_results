#!/usr/bin/env python3
"""Generate the four remaining order-seven Ramsey(5,5;43) formulas."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path

N = 43
CASES = (15, 22, 29, 36)


def single_cycle_degree_clauses(
    incidence: list[int], internal: list[int]
) -> set[tuple[int, ...]]:
    """Encode 18 <= T+2S <= 24 for a nondecreasing incidence word."""
    fixed = len(incidence)
    assert fixed == 36 and len(internal) == 3
    clauses: set[tuple[int, ...]] = set()
    for values in itertools.product((0, 1), repeat=3):
        selected = sum(values)
        lower, upper = 18 - 2 * selected, 24 - 2 * selected
        blocked = [
            -variable if value else variable
            for variable, value in zip(internal, values)
        ]
        clauses.add(tuple(sorted(blocked + [incidence[fixed - lower]])))
        clauses.add(tuple(sorted(blocked + [-incidence[fixed - upper - 1]])))
    return clauses


def build(fixed: int) -> tuple[int, list[tuple[int, ...]]]:
    assert fixed in CASES
    cycles = (N - fixed) // 7

    def image(vertex: int, power: int = 1) -> int:
        if vertex < fixed:
            return vertex
        cycle, position = divmod(vertex - fixed, 7)
        return fixed + 7 * cycle + (position + power) % 7

    def edge_key(u: int, v: int) -> tuple[int, int]:
        return min(
            tuple(sorted((image(u, power), image(v, power))))
            for power in range(7)
        )

    representatives = sorted(
        {edge_key(u, v) for u in range(N) for v in range(u + 1, N)}
    )
    index = {edge: i + 1 for i, edge in enumerate(representatives)}
    mapping = {
        (u, v): index[edge_key(u, v)]
        for u in range(N)
        for v in range(u + 1, N)
    }

    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(N), 5):
        variables = sorted(
            {mapping[(u, v)] for u, v in itertools.combinations(vertices, 2)}
        )
        clauses.add(tuple(variables))
        clauses.add(tuple(-variable for variable in reversed(variables)))

    def block(variables: list[int], values: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(
            -variable if value else variable
            for variable, value in zip(variables, values)
        )

    patterns3 = list(itertools.product((0, 1), repeat=3))
    cycle_profiles = []
    for cycle in range(cycles):
        base = fixed + 7 * cycle
        cycle_profiles.append(
            [mapping[(base, base + distance)] for distance in (1, 2, 3)]
        )
    for left, right in zip(cycle_profiles, cycle_profiles[1:]):
        for left_bits in patterns3:
            for right_bits in patterns3:
                if left_bits > right_bits:
                    clauses.add(block(left + right, left_bits + right_bits))

    fixed_patterns = list(itertools.product((0, 1), repeat=cycles))
    fixed_profiles = [
        [mapping[(vertex, fixed + 7 * cycle)] for cycle in range(cycles)]
        for vertex in range(fixed)
    ]
    for left, right in zip(fixed_profiles, fixed_profiles[1:]):
        for left_bits in fixed_patterns:
            for right_bits in fixed_patterns:
                if left_bits > right_bits:
                    clauses.add(block(left + right, left_bits + right_bits))

    anchor = fixed
    for cycle in range(1, cycles):
        base = fixed + 7 * cycle
        variables = [mapping[(anchor, base + offset)] for offset in range(7)]
        for word in itertools.product((0, 1), repeat=7):
            rotations = [word[shift:] + word[:shift] for shift in range(7)]
            if word != min(rotations):
                clauses.add(block(variables, word))

    if fixed == 36:
        # The sorted fixed-to-cycle bits have threshold form.  If T is their
        # number of ones and S the number of selected internal distances, a
        # moving vertex has degree T+2S.  These two conditional boundary
        # literals per internal pattern say 18 <= T+2S <= 24.
        incidence = [mapping[(vertex, fixed)] for vertex in range(fixed)]
        internal = [mapping[(fixed, fixed + distance)] for distance in (1, 2, 3)]
        clauses.update(single_cycle_degree_clauses(incidence, internal))

    return len(representatives), sorted(clauses, key=lambda clause: (len(clause), clause))


def write_formula(fixed: int, output: Path) -> tuple[int, int, str]:
    variables, clauses = build(fixed)
    with output.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    return variables, len(clauses), hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixed", required=True, type=int, choices=CASES)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    variables, clauses, digest = write_formula(args.fixed, args.output)
    print(
        f"fixed={args.fixed} cycles={(N-args.fixed)//7} "
        f"variables={variables} clauses={clauses} sha256={digest}"
    )


if __name__ == "__main__":
    main()
