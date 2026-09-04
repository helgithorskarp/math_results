#!/usr/bin/env python3
"""Generate symmetry-reduced order-eleven Ramsey(5,5;43) formulas.

The centralizer normalizations follow the order-seven construction in the
sibling ramsey_r55_no_order7_automorphism artifact, with profile width and
phase length changed from seven to eleven.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


ORDER = 43
PRIME = 11
CASES = (10, 21, 32)


def single_cycle_degree_clauses(
    incidence: list[int], internal: list[int]
) -> set[tuple[int, ...]]:
    """Encode 18 <= T+2S <= 24 for a nondecreasing incidence word."""
    fixed = len(incidence)
    if fixed != 32 or len(internal) != 5:
        raise AssertionError("unexpected order-eleven single-cycle profile")
    clauses: set[tuple[int, ...]] = set()
    for values in itertools.product((0, 1), repeat=len(internal)):
        selected = sum(values)
        lower, upper = 18 - 2 * selected, 24 - 2 * selected
        blocked = [
            -variable if value else variable
            for variable, value in zip(internal, values, strict=True)
        ]
        clauses.add(tuple(sorted(blocked + [incidence[fixed - lower]])))
        clauses.add(tuple(sorted(blocked + [-incidence[fixed - upper - 1]])))
    return clauses


def build(fixed: int) -> tuple[int, list[tuple[int, ...]]]:
    if fixed not in CASES:
        raise ValueError(f"fixed must be one of {CASES}")
    cycles = (ORDER - fixed) // PRIME

    def image(vertex: int, power: int = 1) -> int:
        if vertex < fixed:
            return vertex
        cycle, position = divmod(vertex - fixed, PRIME)
        return fixed + PRIME * cycle + (position + power) % PRIME

    def edge_key(u: int, v: int) -> tuple[int, int]:
        return min(
            tuple(sorted((image(u, power), image(v, power))))
            for power in range(PRIME)
        )

    representatives = sorted(
        {edge_key(u, v) for u in range(ORDER) for v in range(u + 1, ORDER)}
    )
    index = {edge: position + 1 for position, edge in enumerate(representatives)}
    mapping = {
        (u, v): index[edge_key(u, v)]
        for u in range(ORDER)
        for v in range(u + 1, ORDER)
    }

    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted(
            {mapping[(u, v)] for u, v in itertools.combinations(vertices, 2)}
        )
        clauses.add(tuple(variables))
        clauses.add(tuple(-variable for variable in reversed(variables)))

    def block(variables: list[int], values: tuple[int, ...]) -> tuple[int, ...]:
        return tuple(
            -variable if value else variable
            for variable, value in zip(variables, values, strict=True)
        )

    internal_width = (PRIME - 1) // 2
    internal_patterns = list(itertools.product((0, 1), repeat=internal_width))
    cycle_profiles = []
    for cycle in range(cycles):
        base = fixed + PRIME * cycle
        cycle_profiles.append(
            [mapping[(base, base + distance)] for distance in range(1, internal_width + 1)]
        )
    for left, right in zip(cycle_profiles, cycle_profiles[1:]):
        for left_bits in internal_patterns:
            for right_bits in internal_patterns:
                if left_bits > right_bits:
                    clauses.add(block(left + right, left_bits + right_bits))

    fixed_patterns = list(itertools.product((0, 1), repeat=cycles))
    fixed_profiles = [
        [mapping[(vertex, fixed + PRIME * cycle)] for cycle in range(cycles)]
        for vertex in range(fixed)
    ]
    for left, right in zip(fixed_profiles, fixed_profiles[1:]):
        for left_bits in fixed_patterns:
            for right_bits in fixed_patterns:
                if left_bits > right_bits:
                    clauses.add(block(left + right, left_bits + right_bits))

    anchor = fixed
    for cycle in range(1, cycles):
        base = fixed + PRIME * cycle
        variables = [mapping[(anchor, base + offset)] for offset in range(PRIME)]
        for word in itertools.product((0, 1), repeat=PRIME):
            rotations = [word[shift:] + word[:shift] for shift in range(PRIME)]
            if word != min(rotations):
                clauses.add(block(variables, word))

    if fixed == 32:
        incidence = [mapping[(vertex, fixed)] for vertex in range(fixed)]
        internal = [
            mapping[(fixed, fixed + distance)]
            for distance in range(1, internal_width + 1)
        ]
        clauses.update(single_cycle_degree_clauses(incidence, internal))

    expected_variables = (
        fixed * (fixed - 1) // 2
        + fixed * cycles
        + internal_width * cycles
        + PRIME * cycles * (cycles - 1) // 2
    )
    if len(representatives) != expected_variables:
        raise AssertionError("edge-orbit count mismatch")
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
        f"fixed={args.fixed} cycles={(ORDER - args.fixed) // PRIME} "
        f"variables={variables} clauses={clauses} sha256={digest}",
        flush=True,
    )


if __name__ == "__main__":
    main()
