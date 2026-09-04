#!/usr/bin/env python3
"""Independent definition-level audit of the two residual order-nine CNFs.

This checker does not import contributor code.  It constructs unordered-edge
orbits by walking the permutation, rather than by the contributor's
least-image implementation or C++ disjoint-set implementation, and compares
the complete normalized clause sets of supplied DIMACS files.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
from collections import Counter
from pathlib import Path


ORDER = 43
CASES = ((3, 5, 1), (4, 2, 1))
EARLIER = {
    (3, 0, 16), (3, 1, 13), (3, 2, 10), (3, 3, 7),
    (3, 4, 4), (4, 0, 7), (4, 1, 4),
}


def norm_pair(u: int, v: int) -> tuple[int, int]:
    return (u, v) if u < v else (v, u)


def vertex_cycles(case: tuple[int, int, int]) -> list[tuple[int, ...]]:
    result: list[tuple[int, ...]] = []
    start = 0
    for length, count in zip((9, 3, 1), case, strict=True):
        for _ in range(count):
            result.append(tuple(range(start, start + length)))
            start += length
    assert start == ORDER
    return result


def successor_and_orbits(case: tuple[int, int, int]):
    cycles = vertex_cycles(case)
    successor = list(range(ORDER))
    for cycle in cycles:
        for index, vertex in enumerate(cycle):
            successor[vertex] = cycle[(index + 1) % len(cycle)]

    # The first unassigned edge is the lexicographically least edge in its
    # orbit, so this also fixes variable numbering without a least-image map.
    mapping: dict[tuple[int, int], int] = {}
    orbit_sizes: list[int] = []
    for seed in itertools.combinations(range(ORDER), 2):
        if seed in mapping:
            continue
        orbit: set[tuple[int, int]] = set()
        edge = seed
        for _ in range(9):
            orbit.add(edge)
            edge = norm_pair(successor[edge[0]], successor[edge[1]])
        assert edge == seed
        variable = len(orbit_sizes) + 1
        assert all(item not in mapping for item in orbit)
        for item in orbit:
            mapping[item] = variable
        orbit_sizes.append(len(orbit))
    assert len(mapping) == ORDER * (ORDER - 1) // 2
    return cycles, successor, mapping, Counter(orbit_sizes)


def bits(number: int, width: int) -> tuple[int, ...]:
    return tuple((number >> shift) & 1 for shift in range(width - 1, -1, -1))


def blocking_clause(variables, values) -> tuple[int, ...]:
    return tuple(sorted(-variable if value else variable
                        for variable, value in zip(variables, values, strict=True)))


def build_expected(case: tuple[int, int, int]):
    cycles, successor, mapping, distribution = successor_and_orbits(case)
    clauses: set[tuple[int, ...]] = set()
    for five in itertools.combinations(range(ORDER), 5):
        variables = {mapping[pair] for pair in itertools.combinations(five, 2)}
        clauses.add(tuple(sorted(variables)))
        clauses.add(tuple(sorted(-variable for variable in variables)))
    base_count = len(clauses)

    nines = [cycle for cycle in cycles if len(cycle) == 9]
    threes = [cycle for cycle in cycles if len(cycle) == 3]
    for group, width in ((nines, 4), (threes, 1)):
        profiles = [tuple(mapping[norm_pair(cycle[0], cycle[d])]
                          for d in range(1, width + 1))
                    for cycle in group]
        for left_vars, right_vars in zip(profiles, profiles[1:]):
            for left in range(1 << width):
                for right in range(left):
                    clauses.add(blocking_clause(
                        left_vars + right_vars, bits(left, width) + bits(right, width)))

    anchor = nines[0][0]
    cross_sets = []
    for cycle in nines[1:] + threes:
        variables = tuple(mapping[norm_pair(anchor, vertex)] for vertex in cycle)
        assert len(set(variables)) == len(cycle)
        cross_sets.append(set(variables))
        width = len(cycle)
        for number in range(1 << width):
            word = bits(number, width)
            if min(word[shift:] + word[:shift] for shift in range(width)) < word:
                clauses.add(blocking_clause(variables, word))
    assert all(left.isdisjoint(right)
               for index, left in enumerate(cross_sets)
               for right in cross_sets[index + 1:])

    audit_centralizer(cycles, successor, mapping)
    return len(set(mapping.values())), clauses, base_count, distribution


def audit_centralizer(cycles, successor, mapping) -> None:
    def require_commuting(permutation):
        assert sorted(permutation) == list(range(ORDER))
        assert all(permutation[successor[v]] == successor[permutation[v]]
                   for v in range(ORDER))

    # Equal-length cycle swaps generate all profile-sorting permutations.
    for length in (9, 3):
        group = [cycle for cycle in cycles if len(cycle) == length]
        for left, right in zip(group, group[1:]):
            permutation = list(range(ORDER))
            for u, v in zip(left, right, strict=True):
                permutation[u], permutation[v] = v, u
            require_commuting(permutation)

    # Individual rotations commute with g, preserve internal profiles, and
    # cyclically rotate only the relevant anchor cross word.
    anchor = next(cycle for cycle in cycles if len(cycle) == 9)[0]
    moving = [cycle for cycle in cycles if len(cycle) > 1]
    for cycle in moving:
        profile_width = (len(cycle) - 1) // 2
        original_profile = tuple(mapping[norm_pair(cycle[0], cycle[d])]
                                 for d in range(1, profile_width + 1))
        for shift in range(len(cycle)):
            permutation = list(range(ORDER))
            for index, vertex in enumerate(cycle):
                permutation[vertex] = cycle[(index + shift) % len(cycle)]
            require_commuting(permutation)
            rotated_profile = tuple(
                mapping[norm_pair(permutation[cycle[0]], permutation[cycle[d]])]
                for d in range(1, profile_width + 1))
            assert rotated_profile == original_profile
            if cycle[0] != anchor:
                original = tuple(mapping[norm_pair(anchor, vertex)] for vertex in cycle)
                transformed = tuple(
                    mapping[norm_pair(permutation[anchor], permutation[vertex])]
                    for vertex in cycle)
                assert transformed == original[shift:] + original[:shift]


def read_dimacs(path: Path):
    variables = clauses_declared = None
    clauses: set[tuple[int, ...]] = set()
    parsed = 0
    with path.open(encoding="ascii") as stream:
        for raw in stream:
            line = raw.strip()
            if not line or line.startswith("c"):
                continue
            fields = line.split()
            if fields[0] == "p":
                assert variables is None and fields[1] == "cnf" and len(fields) == 4
                variables, clauses_declared = map(int, fields[2:])
                continue
            assert variables is not None and fields[-1] == "0"
            literals = list(map(int, fields[:-1]))
            assert literals and all(0 < abs(literal) <= variables for literal in literals)
            assert len(literals) == len(set(literals))
            assert not any(-literal in literals for literal in literals)
            clause = tuple(sorted(literals))
            assert clause not in clauses
            clauses.add(clause)
            parsed += 1
    assert variables is not None and parsed == clauses_declared == len(clauses)
    return variables, clauses


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("case0", type=Path)
    parser.add_argument("case1", type=Path)
    args = parser.parse_args()

    survivors = {(a, b, ORDER - 9 * a - 3 * b)
                 for a in range(1, ORDER // 9 + 1)
                 for b in range(ORDER // 3 + 1)
                 if ORDER - 9 * a - 3 * b >= 0 and 3 * a >= 7}
    assert survivors == EARLIER | set(CASES)
    print("PASS type_reduction survivors=9 earlier=7 residual=2")

    for index, (case, path) in enumerate(zip(CASES, (args.case0, args.case1), strict=True)):
        expected_variables, expected, base_count, distribution = build_expected(case)
        actual_variables, actual = read_dimacs(path)
        missing, extra = expected - actual, actual - expected
        assert actual_variables == expected_variables
        assert not missing and not extra, (
            f"case {index} differs: missing={next(iter(missing), None)} "
            f"extra={next(iter(extra), None)}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"PASS case={case} variables={actual_variables} clauses={len(actual)} "
              f"base={base_count} symmetry={len(actual)-base_count} "
              f"orbit_sizes={dict(sorted(distribution.items()))} sha256={digest} "
              "complete_clause_equality=true centralizer_generators=true")


if __name__ == "__main__":
    main()
