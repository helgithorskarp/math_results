#!/usr/bin/env python3
"""Independently reconstruct and verify the order-eleven obstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path


ORDER = 43
PRIME = 11
CASES = (10, 21, 32)
EXPECTED_COUNTS = {10: (123, 177_074), 21: (273, 208_332), 32: (533, 535_001)}
Clause = tuple[int, ...]


class Dsu:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))

    def find(self, item: int) -> int:
        while self.parent[item] != item:
            self.parent[item] = self.parent[self.parent[item]]
            item = self.parent[item]
        return item

    def join(self, first: int, second: int) -> None:
        first, second = self.find(first), self.find(second)
        if first != second:
            self.parent[second] = first


def permute(vertex: int, fixed: int) -> int:
    if vertex < fixed:
        return vertex
    cycle, position = divmod(vertex - fixed, PRIME)
    return fixed + PRIME * cycle + (position + 1) % PRIME


def construct_orbits(fixed: int) -> tuple[list[list[int]], Counter[int]]:
    raw = [[-1] * ORDER for _ in range(ORDER)]
    edges = []
    for u in range(ORDER):
        for v in range(u + 1, ORDER):
            raw[u][v] = len(edges)
            edges.append((u, v))
    if len(edges) != 903:
        raise AssertionError("wrong edge count")
    dsu = Dsu(len(edges))
    for u, v in edges:
        pu, pv = sorted((permute(u, fixed), permute(v, fixed)))
        dsu.join(raw[u][v], raw[pu][pv])

    least: dict[int, tuple[int, int]] = {}
    sizes: Counter[int] = Counter()
    for u, v in edges:
        root = dsu.find(raw[u][v])
        least[root] = min(least.get(root, (u, v)), (u, v))
        sizes[root] += 1
    representatives = sorted(least.values())
    number = {representative: index + 1 for index, representative in enumerate(representatives)}
    mapping = [[-1] * ORDER for _ in range(ORDER)]
    for u, v in edges:
        mapping[u][v] = number[least[dsu.find(raw[u][v])]]
    histogram = Counter(sizes.values())
    singleton = fixed * (fixed - 1) // 2
    expected = Counter({1: singleton, PRIME: (903 - singleton) // PRIME})
    if histogram != expected:
        raise AssertionError("edge-orbit size histogram mismatch")
    return mapping, histogram


def edge(mapping: list[list[int]], u: int, v: int) -> int:
    if u > v:
        u, v = v, u
    if u == v or mapping[u][v] < 1:
        raise AssertionError("invalid edge lookup")
    return mapping[u][v]


def normalized(raw: list[int] | tuple[int, ...]) -> Clause:
    clause = tuple(sorted(raw))
    if len(set(clause)) != len(clause):
        raise AssertionError("repeated literal in formula clause")
    if any(-literal in clause for literal in clause):
        raise AssertionError("tautological formula clause")
    return clause


def binary(value: int, width: int) -> tuple[int, ...]:
    return tuple((value >> shift) & 1 for shift in reversed(range(width)))


def block(variables: list[int], values: tuple[int, ...]) -> Clause:
    if len(variables) != len(values):
        raise AssertionError("blocking assignment width mismatch")
    return tuple(
        -variable if value else variable
        for variable, value in zip(variables, values, strict=True)
    )


def least_rotation(word: tuple[int, ...]) -> bool:
    return all(word <= word[shift:] + word[:shift] for shift in range(1, len(word)))


def reconstruct(fixed: int) -> tuple[int, list[Clause], Counter[int]]:
    cycles = (ORDER - fixed) // PRIME
    mapping, histogram = construct_orbits(fixed)
    formula: set[Clause] = set()

    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted(
            {edge(mapping, u, v) for u, v in itertools.combinations(vertices, 2)}
        )
        formula.add(normalized(variables))
        formula.add(normalized([-variable for variable in variables]))

    width = (PRIME - 1) // 2
    cycle_profiles = []
    for cycle in range(cycles):
        base = fixed + PRIME * cycle
        cycle_profiles.append(
            [edge(mapping, base, base + distance) for distance in range(1, width + 1)]
        )
    for left, right in zip(cycle_profiles, cycle_profiles[1:]):
        variables = left + right
        for left_value in range(1 << width):
            for right_value in range(1 << width):
                if left_value > right_value:
                    formula.add(block(variables, binary(left_value, width) + binary(right_value, width)))

    fixed_profiles = [
        [edge(mapping, vertex, fixed + PRIME * cycle) for cycle in range(cycles)]
        for vertex in range(fixed)
    ]
    for left, right in zip(fixed_profiles, fixed_profiles[1:]):
        variables = left + right
        for left_value in range(1 << cycles):
            for right_value in range(1 << cycles):
                if left_value > right_value:
                    formula.add(
                        block(
                            variables,
                            binary(left_value, cycles) + binary(right_value, cycles),
                        )
                    )

    anchor = fixed
    for cycle in range(1, cycles):
        base = fixed + PRIME * cycle
        variables = [edge(mapping, anchor, base + offset) for offset in range(PRIME)]
        for value in range(1 << PRIME):
            word = binary(value, PRIME)
            if not least_rotation(word):
                formula.add(block(variables, word))

    if fixed == 32:
        incidence = [edge(mapping, vertex, fixed) for vertex in range(fixed)]
        internal = [edge(mapping, fixed, fixed + distance) for distance in range(1, width + 1)]
        for value in range(1 << width):
            values = binary(value, width)
            selected = sum(values)
            lower, upper = 18 - 2 * selected, 24 - 2 * selected
            formula.add(normalized(list(block(internal, values)) + [incidence[fixed - lower]]))
            formula.add(normalized(list(block(internal, values)) + [-incidence[fixed - upper - 1]]))

    variables = max(max(map(abs, clause), default=0) for clause in formula)
    clauses = sorted(formula, key=lambda clause: (len(clause), clause))
    if (variables, len(clauses)) != EXPECTED_COUNTS[fixed]:
        raise AssertionError("formula census mismatch")
    return variables, clauses, histogram


def cnf_sha256(variables: int, clauses: list[Clause]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {variables} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


@dataclass
class WatchedClause:
    literals: Clause
    first: int
    second: int


class RupChecker:
    def __init__(self, variables: int, initial: list[Clause]) -> None:
        self.variables = variables
        self.clauses: list[WatchedClause] = []
        self.watchers = {
            literal: []
            for variable in range(1, variables + 1)
            for literal in (variable, -variable)
        }
        self.units: list[int] = []
        self.empty_present = False
        for clause in initial:
            self.add_clause(clause)

    @staticmethod
    def normalize(clause: Clause) -> Clause | None:
        seen = set()
        result = []
        for literal in clause:
            if -literal in seen:
                return None
            if literal not in seen:
                seen.add(literal)
                result.append(literal)
        return tuple(result)

    def add_clause(self, raw: Clause) -> None:
        clause = self.normalize(raw)
        if clause is None:
            return
        if any(literal == 0 or abs(literal) > self.variables for literal in clause):
            raise ValueError("proof literal outside declared range")
        if not clause:
            self.empty_present = True
        elif len(clause) == 1:
            self.units.append(clause[0])
        else:
            index = len(self.clauses)
            self.clauses.append(WatchedClause(clause, 0, 1))
            self.watchers[clause[0]].append(index)
            self.watchers[clause[1]].append(index)

    @staticmethod
    def value(literal: int, assignment: list[int]) -> int:
        value = assignment[abs(literal)]
        return value if literal > 0 else -value

    @staticmethod
    def enqueue(literal: int, assignment: list[int], trail: deque[int]) -> bool:
        variable = abs(literal)
        value = 1 if literal > 0 else -1
        if assignment[variable] == -value:
            return False
        if assignment[variable] == 0:
            assignment[variable] = value
            trail.append(literal)
        return True

    def rup(self, raw: Clause) -> bool:
        clause = self.normalize(raw)
        if clause is None:
            return True
        assignment = [0] * (self.variables + 1)
        trail: deque[int] = deque()
        for unit in self.units:
            if not self.enqueue(unit, assignment, trail):
                return True
        for literal in clause:
            if not self.enqueue(-literal, assignment, trail):
                return True
        while trail:
            false_literal = -trail.popleft()
            watched = self.watchers[false_literal]
            position = 0
            while position < len(watched):
                clause_index = watched[position]
                record = self.clauses[clause_index]
                if record.literals[record.first] == false_literal:
                    false_watch, other_watch, replace_first = record.first, record.second, True
                elif record.literals[record.second] == false_literal:
                    false_watch, other_watch, replace_first = record.second, record.first, False
                else:
                    raise AssertionError("inconsistent watcher")
                other = record.literals[other_watch]
                if self.value(other, assignment) == 1:
                    position += 1
                    continue
                replacement = next(
                    (
                        candidate
                        for candidate, literal in enumerate(record.literals)
                        if candidate not in (false_watch, other_watch)
                        and self.value(literal, assignment) != -1
                    ),
                    None,
                )
                if replacement is not None:
                    if replace_first:
                        record.first = replacement
                    else:
                        record.second = replacement
                    watched[position] = watched[-1]
                    watched.pop()
                    self.watchers[record.literals[replacement]].append(clause_index)
                    continue
                if self.value(other, assignment) == -1:
                    return True
                if not self.enqueue(other, assignment, trail):
                    return True
                position += 1
        return self.empty_present


def parse_line(line: str) -> tuple[bool, Clause]:
    fields = line.split()
    deletion = bool(fields and fields[0] == "d")
    if deletion:
        fields = fields[1:]
    if not fields or fields[-1] != "0":
        raise ValueError("proof line is not zero-terminated")
    return deletion, tuple(map(int, fields[:-1]))


def replay(variables: int, clauses: list[Clause], path: Path) -> tuple[int, int]:
    checker = RupChecker(variables, clauses)
    additions = deletions = 0
    derived_empty = False
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"blank proof line {number}")
        deletion, clause = parse_line(line)
        if deletion:
            deletions += 1
            continue
        additions += 1
        if not checker.rup(clause):
            raise AssertionError(f"non-RUP addition at {path}:{number}")
        checker.add_clause(clause)
        derived_empty |= not clause
    if not derived_empty:
        raise AssertionError("proof did not derive the empty clause")
    return additions, deletions


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=here / "result.json")
    args = parser.parse_args()
    document = json.loads(args.result.read_text())
    expected_top = {
        "format": "r55-order11-automorphism-obstruction-v1",
        "order": ORDER,
        "automorphism_order": PRIME,
        "degree_window": [18, 24],
        "single_cycle_degree_case": 32,
        "solver": "PySAT Glucose 4.2",
    }
    for key, value in expected_top.items():
        if document.get(key) != value:
            raise AssertionError(f"manifest mismatch at {key}")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != len(CASES):
        raise AssertionError("manifest case count mismatch")

    total_additions = total_deletions = total_bytes = 0
    for fixed, case in zip(CASES, cases, strict=True):
        variables, clauses, histogram = reconstruct(fixed)
        expected_case = {
            "fixed_points": fixed,
            "eleven_cycles": (ORDER - fixed) // PRIME,
            "variables": variables,
            "clauses": len(clauses),
            "cnf_sha256": cnf_sha256(variables, clauses),
        }
        for key, value in expected_case.items():
            if case.get(key) != value:
                raise AssertionError(f"case f={fixed} mismatch at {key}")
        path = here / case["proof_file"]
        payload = path.read_bytes()
        if len(payload) != case["proof_bytes"]:
            raise AssertionError("proof byte count mismatch")
        if hashlib.sha256(payload).hexdigest() != case["proof_sha256"]:
            raise AssertionError("proof hash mismatch")
        additions, deletions = replay(variables, clauses, path)
        if additions != case["proof_additions"] or deletions != case["proof_deletions"]:
            raise AssertionError("proof line census mismatch")
        if additions + deletions != case["proof_lines"]:
            raise AssertionError("proof total line count mismatch")
        total_additions += additions
        total_deletions += deletions
        total_bytes += len(payload)
        print(
            f"PASS fixed={fixed} eleven_cycles={(ORDER-fixed)//PRIME} "
            f"variables={variables} clauses={len(clauses)} "
            f"orbit_sizes={dict(sorted(histogram.items()))} "
            f"additions={additions} deletions={deletions}",
            flush=True,
        )
    print(
        f"PASS order-eleven obstruction additions={total_additions} "
        f"deletions={total_deletions} proof_bytes={total_bytes}",
        flush=True,
    )


if __name__ == "__main__":
    main()
