#!/usr/bin/env python3
"""Generate symmetry-reduced prime-order Ramsey(5,5;43) formulas."""

from __future__ import annotations

import argparse
import hashlib
import itertools
from pathlib import Path


ORDER = 43
CASES = {13: (4, 17, 30), 17: (9, 26), 19: (5, 24), 23: (20,)}


def single_cycle_degree_clauses(
    fixed: int, incidence: list[int], internal: list[int]
) -> set[tuple[int, ...]]:
    """Encode 18 <= T+2S <= 24 for a sorted incidence threshold word."""
    if len(incidence) != fixed:
        raise AssertionError("incidence width mismatch")
    clauses: set[tuple[int, ...]] = set()
    for values in itertools.product((0, 1), repeat=len(internal)):
        selected = sum(values)
        lower, upper = 18 - 2 * selected, 24 - 2 * selected
        blocked = [
            -variable if value else variable
            for variable, value in zip(internal, values, strict=True)
        ]
        if lower > fixed:
            clauses.add(tuple(sorted(blocked)))
        elif lower > 0:
            clauses.add(tuple(sorted(blocked + [incidence[fixed - lower]])))
        if upper < 0:
            clauses.add(tuple(sorted(blocked)))
        elif upper < fixed:
            clauses.add(tuple(sorted(blocked + [-incidence[fixed - upper - 1]])))
    return clauses


def build(prime: int, fixed: int) -> tuple[int, list[tuple[int, ...]]]:
    if prime not in CASES or fixed not in CASES[prime]:
        raise ValueError("unsupported prime/fixed-point pair")
    cycles = (ORDER - fixed) // prime

    def image(vertex: int, power: int = 1) -> int:
        if vertex < fixed:
            return vertex
        cycle, position = divmod(vertex - fixed, prime)
        return fixed + prime * cycle + (position + power) % prime

    def edge_key(u: int, v: int) -> tuple[int, int]:
        return min(
            tuple(sorted((image(u, power), image(v, power))))
            for power in range(prime)
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

    width = (prime - 1) // 2
    internal_patterns = list(itertools.product((0, 1), repeat=width))
    cycle_profiles = []
    for cycle in range(cycles):
        base = fixed + prime * cycle
        cycle_profiles.append(
            [mapping[(base, base + distance)] for distance in range(1, width + 1)]
        )
    for left, right in zip(cycle_profiles, cycle_profiles[1:]):
        for left_bits in internal_patterns:
            for right_bits in internal_patterns:
                if left_bits > right_bits:
                    clauses.add(block(left + right, left_bits + right_bits))

    fixed_patterns = list(itertools.product((0, 1), repeat=cycles))
    fixed_profiles = [
        [mapping[(vertex, fixed + prime * cycle)] for cycle in range(cycles)]
        for vertex in range(fixed)
    ]
    for left, right in zip(fixed_profiles, fixed_profiles[1:]):
        for left_bits in fixed_patterns:
            for right_bits in fixed_patterns:
                if left_bits > right_bits:
                    clauses.add(block(left + right, left_bits + right_bits))

    anchor = fixed
    for cycle in range(1, cycles):
        base = fixed + prime * cycle
        variables = [mapping[(anchor, base + offset)] for offset in range(prime)]
        for word in itertools.product((0, 1), repeat=prime):
            rotations = [word[shift:] + word[:shift] for shift in range(prime)]
            if word != min(rotations):
                clauses.add(block(variables, word))

    if cycles == 1:
        incidence = [mapping[(vertex, fixed)] for vertex in range(fixed)]
        internal = [
            mapping[(fixed, fixed + distance)] for distance in range(1, width + 1)
        ]
        clauses.update(single_cycle_degree_clauses(fixed, incidence, internal))

    expected_variables = (
        fixed * (fixed - 1) // 2
        + fixed * cycles
        + width * cycles
        + prime * cycles * (cycles - 1) // 2
    )
    if len(representatives) != expected_variables:
        raise AssertionError("edge-orbit count mismatch")
    return len(representatives), sorted(clauses, key=lambda clause: (len(clause), clause))


def write_formula(prime: int, fixed: int, output: Path) -> tuple[int, int, str]:
    variables, clauses = build(prime, fixed)
    with output.open("w", encoding="ascii", newline="\n") as stream:
        stream.write(f"p cnf {variables} {len(clauses)}\n")
        for clause in clauses:
            stream.write(" ".join(map(str, clause)) + " 0\n")
    return variables, len(clauses), hashlib.sha256(output.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--prime", required=True, type=int, choices=CASES)
    parser.add_argument("--fixed", required=True, type=int)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    variables, clauses, digest = write_formula(args.prime, args.fixed, args.output)
    print(
        f"prime={args.prime} fixed={args.fixed} "
        f"cycles={(ORDER-args.fixed)//args.prime} variables={variables} "
        f"clauses={clauses} sha256={digest}",
        flush=True,
    )


if __name__ == "__main__":
    main()
