#!/usr/bin/env python3
"""Independently reconstruct and verify the medium-prime obstruction."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import lzma
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path


ORDER = 43
CASES = {13: (4, 17, 30), 17: (9, 26), 19: (5, 24), 23: (20,)}
CASE_ORDER = tuple((prime, fixed) for prime in CASES for fixed in CASES[prime])
RAT_CASE = (13, 17)
EXPECTED_COUNTS = {
    (13, 4): (75, 164_796),
    (13, 17): (195, 161_936),
    (13, 30): (471, 402_223),
    (17, 9): (87, 262_848),
    (17, 26): (359, 222_839),
    (19, 5): (57, 723_284),
    (19, 24): (309, 165_411),
    (23, 20): (221, 95_213),
}
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


def image(vertex: int, fixed: int, prime: int) -> int:
    if vertex < fixed:
        return vertex
    cycle, position = divmod(vertex - fixed, prime)
    return fixed + prime * cycle + (position + 1) % prime


def construct_orbits(fixed: int, prime: int) -> tuple[list[list[int]], Counter[int]]:
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
        pu, pv = sorted((image(u, fixed, prime), image(v, fixed, prime)))
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
    expected = Counter({1: singleton, prime: (903 - singleton) // prime})
    if not singleton:
        del expected[1]
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


def reconstruct(prime: int, fixed: int) -> tuple[int, list[Clause], Counter[int]]:
    cycles = (ORDER - fixed) // prime
    mapping, histogram = construct_orbits(fixed, prime)
    formula: set[Clause] = set()

    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted(
            {edge(mapping, u, v) for u, v in itertools.combinations(vertices, 2)}
        )
        formula.add(normalized(variables))
        formula.add(normalized([-variable for variable in variables]))

    width = (prime - 1) // 2
    cycle_profiles = []
    for cycle in range(cycles):
        base = fixed + prime * cycle
        cycle_profiles.append(
            [edge(mapping, base, base + distance) for distance in range(1, width + 1)]
        )
    for left, right in zip(cycle_profiles, cycle_profiles[1:]):
        variables = left + right
        for left_value in range(1 << width):
            for right_value in range(1 << width):
                if left_value > right_value:
                    formula.add(
                        block(
                            variables,
                            binary(left_value, width) + binary(right_value, width),
                        )
                    )

    fixed_profiles = [
        [edge(mapping, vertex, fixed + prime * cycle) for cycle in range(cycles)]
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
        base = fixed + prime * cycle
        variables = [edge(mapping, anchor, base + offset) for offset in range(prime)]
        for value in range(1 << prime):
            word = binary(value, prime)
            if not least_rotation(word):
                formula.add(block(variables, word))

    if cycles == 1:
        incidence = [edge(mapping, vertex, fixed) for vertex in range(fixed)]
        internal = [
            edge(mapping, fixed, fixed + distance) for distance in range(1, width + 1)
        ]
        for value in range(1 << width):
            values = binary(value, width)
            selected = sum(values)
            lower, upper = 18 - 2 * selected, 24 - 2 * selected
            blocked = list(block(internal, values))
            if lower > fixed:
                formula.add(normalized(blocked))
            elif lower > 0:
                formula.add(normalized(blocked + [incidence[fixed - lower]]))
            if upper < 0:
                formula.add(normalized(blocked))
            elif upper < fixed:
                formula.add(normalized(blocked + [-incidence[fixed - upper - 1]]))

    variables = max(max(map(abs, clause), default=0) for clause in formula)
    clauses = sorted(formula, key=lambda clause: (len(clause), clause))
    if (variables, len(clauses)) != EXPECTED_COUNTS[(prime, fixed)]:
        raise AssertionError("formula census mismatch")
    return variables, clauses, histogram


def cnf_bytes(variables: int, clauses: list[Clause]) -> bytes:
    lines = [f"p cnf {variables} {len(clauses)}\n"]
    lines.extend(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return "".join(lines).encode("ascii")


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


def replay(variables: int, clauses: list[Clause], payload: bytes) -> tuple[int, int]:
    checker = RupChecker(variables, clauses)
    additions = deletions = 0
    derived_empty = False
    for number, line in enumerate(payload.decode("ascii").splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"blank proof line {number}")
        deletion, clause = parse_line(line)
        if deletion:
            deletions += 1
            continue
        additions += 1
        if not checker.rup(clause):
            raise AssertionError(f"non-RUP addition at proof line {number}")
        checker.add_clause(clause)
        derived_empty |= not clause
    if not derived_empty:
        raise AssertionError("proof did not derive the empty clause")
    return additions, deletions


def check_payload(case: dict, payload: bytes) -> tuple[int, int]:
    if len(payload) != case["proof_bytes"]:
        raise AssertionError("proof byte count mismatch")
    if hashlib.sha256(payload).hexdigest() != case["proof_sha256"]:
        raise AssertionError("proof hash mismatch")
    lines = payload.decode("ascii").splitlines()
    additions = sum(not line.startswith("d ") for line in lines)
    deletions = len(lines) - additions
    if (len(lines), additions, deletions) != (
        case["proof_lines"],
        case["proof_additions"],
        case["proof_deletions"],
    ):
        raise AssertionError("proof line census mismatch")
    return additions, deletions


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=here / "result.json")
    parser.add_argument(
        "--rat-cnf", type=Path, help="write independently reconstructed p13/f17 CNF"
    )
    parser.add_argument(
        "--only-rup-case", help="replay only one RUP case, formatted prime:fixed"
    )
    args = parser.parse_args()
    selected = None
    if args.only_rup_case:
        selected = tuple(map(int, args.only_rup_case.split(":")))
        if selected not in CASE_ORDER or selected == RAT_CASE:
            raise ValueError("--only-rup-case must name one of the seven RUP cases")

    document = json.loads(args.result.read_text())
    expected_top = {
        "format": "r55-medium-prime-automorphism-obstruction-v1",
        "order": ORDER,
        "automorphism_orders": list(CASES),
        "degree_window": [18, 24],
        "single_cycle_degree_cases": [[13, 30], [17, 26], [19, 24], [23, 20]],
        "rat_case": list(RAT_CASE),
    }
    for key, value in expected_top.items():
        if document.get(key) != value:
            raise AssertionError(f"manifest mismatch at {key}")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != len(CASE_ORDER):
        raise AssertionError("manifest case count mismatch")

    totals = Counter()
    for (prime, fixed), case in zip(CASE_ORDER, cases, strict=True):
        variables, clauses, histogram = reconstruct(prime, fixed)
        formula = cnf_bytes(variables, clauses)
        expected_case = {
            "prime": prime,
            "fixed_points": fixed,
            "prime_cycles": (ORDER - fixed) // prime,
            "variables": variables,
            "clauses": len(clauses),
            "cnf_sha256": hashlib.sha256(formula).hexdigest(),
            "proof_kind": "DRAT" if (prime, fixed) == RAT_CASE else "RUP",
        }
        for key, value in expected_case.items():
            if case.get(key) != value:
                raise AssertionError(f"case p={prime}, f={fixed} mismatch at {key}")

        path = here / case["proof_file"]
        stored = path.read_bytes()
        if (prime, fixed) == RAT_CASE:
            if case.get("proof_compression") != "xz":
                raise AssertionError("RAT proof compression mismatch")
            if len(stored) != case["proof_compressed_bytes"]:
                raise AssertionError("compressed proof byte count mismatch")
            if hashlib.sha256(stored).hexdigest() != case["proof_compressed_sha256"]:
                raise AssertionError("compressed proof hash mismatch")
            payload = lzma.decompress(stored)
            additions, deletions = check_payload(case, payload)
            if args.rat_cnf:
                args.rat_cnf.write_bytes(formula)
            label = "hash-checked; external DRAT replay required"
        else:
            payload = stored
            check_payload(case, payload)
            if selected is None or selected == (prime, fixed):
                additions, deletions = replay(variables, clauses, payload)
                label = "RUP-replayed"
            else:
                additions = case["proof_additions"]
                deletions = case["proof_deletions"]
                label = "hash-checked"
        totals["additions"] += additions
        totals["deletions"] += deletions
        totals["bytes"] += len(payload)
        print(
            f"PASS prime={prime} fixed={fixed} cycles={(ORDER-fixed)//prime} "
            f"variables={variables} clauses={len(clauses)} "
            f"orbit_sizes={dict(sorted(histogram.items()))} {label}",
            flush=True,
        )
    if args.rat_cnf and not args.rat_cnf.exists():
        raise AssertionError("failed to write RAT formula")
    print(
        f"PASS medium-prime census additions={totals['additions']} "
        f"deletions={totals['deletions']} proof_bytes={totals['bytes']}",
        flush=True,
    )


if __name__ == "__main__":
    main()
