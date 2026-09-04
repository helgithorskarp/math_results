#!/usr/bin/env python3
"""Independently rebuild and replay all low-orbit three-cycle certificates."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path


ORDER = 43
ORBIT_CAP = 25


def degree_choices(length: int) -> set[int]:
    # A union of distance classes on a cycle has degree two per selected
    # non-antipodal class, plus an optional antipodal matching when even.
    return set(range(length)) if length % 2 == 0 else set(range(0, length, 2))


def degree_feasible(parts: tuple[int, int, int]) -> bool:
    gcds = {(i, j): math.gcd(parts[i], parts[j]) for i in range(3) for j in range(i + 1, 3)}
    for selected01 in range(gcds[0, 1] + 1):
        for selected02 in range(gcds[0, 2] + 1):
            for selected12 in range(gcds[1, 2] + 1):
                cross = (
                    selected01 * parts[1] // gcds[0, 1]
                    + selected02 * parts[2] // gcds[0, 2],
                    selected01 * parts[0] // gcds[0, 1]
                    + selected12 * parts[2] // gcds[1, 2],
                    selected02 * parts[0] // gcds[0, 2]
                    + selected12 * parts[1] // gcds[1, 2],
                )
                if all(
                    any(18 <= cross[i] + internal <= 24 for internal in degree_choices(parts[i]))
                    for i in range(3)
                ):
                    return True
    return False


def variable_count(parts: tuple[int, int, int]) -> int:
    return sum(length // 2 for length in parts) + sum(
        math.gcd(parts[i], parts[j]) for i in range(3) for j in range(i + 1, 3)
    )


def classified_types() -> tuple[list[tuple[int, int, int]], int, int, int, int]:
    low = []
    infeasible = high = low_infeasible = high_infeasible = 0
    for first in range(1, ORDER // 3 + 1):
        for second in range(first, (ORDER - first) // 2 + 1):
            parts = (first, second, ORDER - first - second)
            if not degree_feasible(parts):
                infeasible += 1
                if variable_count(parts) <= ORBIT_CAP:
                    low_infeasible += 1
                else:
                    high_infeasible += 1
            elif variable_count(parts) <= ORBIT_CAP:
                low.append(parts)
            else:
                high += 1
    if len(low) + infeasible + high != 154:
        raise AssertionError("partition census mismatch")
    return low, infeasible, high, low_infeasible, high_infeasible


def advance(vertex: int, parts: tuple[int, int, int]) -> int:
    start = 0
    for length in parts:
        if vertex < start + length:
            return start + (vertex - start + 1) % length
        start += length
    raise AssertionError("vertex outside cycle partition")


def canonical_edge(edge: tuple[int, int], parts: tuple[int, int, int]) -> tuple[int, int]:
    seed = edge
    images = []
    while not images or edge != seed:
        images.append(edge)
        edge = tuple(sorted((advance(edge[0], parts), advance(edge[1], parts))))
    if len(set(images)) != len(images):
        raise AssertionError("permutation orbit repeated before returning to seed")
    return min(images)


def reconstruct(parts: tuple[int, int, int]) -> tuple[list[tuple[int, int]], set[int], Counter[int]]:
    edges = list(itertools.combinations(range(ORDER), 2))
    representative = {edge: canonical_edge(edge, parts) for edge in edges}
    representatives = sorted(set(representative.values()))
    if len(representatives) != variable_count(parts):
        raise AssertionError("edge-orbit count mismatch")
    index = {edge: i for i, edge in enumerate(representatives)}
    edge_variable = {edge: index[rep] for edge, rep in representative.items()}
    masks = set()
    count = 0
    for vertices in itertools.combinations(range(ORDER), 5):
        mask = 0
        for edge in itertools.combinations(vertices, 2):
            mask |= 1 << edge_variable[edge]
        masks.add(mask)
        count += 1
    if count != 962_598:
        raise AssertionError("five-set count mismatch")
    sizes = Counter(Counter(representative.values()).values())
    return representatives, masks, sizes


def clauses_from_masks(masks: set[int], variables: int) -> list[tuple[int, ...]]:
    clauses = []
    for mask in sorted(masks):
        positive = tuple(i + 1 for i in range(variables) if mask >> i & 1)
        clauses.extend((positive, tuple(-literal for literal in positive)))
    clauses.append((1,))
    return clauses


def cnf_sha256(variables: int, clauses: list[tuple[int, ...]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {variables} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


@dataclass
class WatchedClause:
    literals: tuple[int, ...]
    first: int
    second: int


class RupChecker:
    """A standard-library watched-literal reverse-unit-propagation checker."""

    def __init__(self, variables: int, initial: list[tuple[int, ...]]) -> None:
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
    def normalize(clause: tuple[int, ...]) -> tuple[int, ...] | None:
        seen = set()
        normalized = []
        for literal in clause:
            if -literal in seen:
                return None
            if literal not in seen:
                seen.add(literal)
                normalized.append(literal)
        return tuple(normalized)

    def add_clause(self, raw: tuple[int, ...]) -> None:
        clause = self.normalize(raw)
        if clause is None:
            return
        if any(literal == 0 or abs(literal) > self.variables for literal in clause):
            raise ValueError("literal outside declared range")
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

    def rup(self, raw: tuple[int, ...]) -> bool:
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
                    raise AssertionError("inconsistent watch list")
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


def parse_line(line: str) -> tuple[bool, tuple[int, ...]]:
    fields = line.split()
    deletion = bool(fields and fields[0] == "d")
    if deletion:
        fields = fields[1:]
    if not fields or fields[-1] != "0":
        raise ValueError("proof line is not zero-terminated")
    return deletion, tuple(map(int, fields[:-1]))


def replay(variables: int, clauses: list[tuple[int, ...]], path: Path) -> tuple[int, int]:
    checker = RupChecker(variables, clauses)
    additions = deletions = 0
    derived_empty = False
    for number, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"blank proof line {number}")
        deletion, clause = parse_line(line)
        if deletion:
            # Retaining derived clauses is sound and avoids trusting deletions.
            deletions += 1
            continue
        additions += 1
        if not checker.rup(clause):
            raise AssertionError(f"non-RUP addition at {path}:{number}")
        checker.add_clause(clause)
        derived_empty |= not clause
    if not derived_empty:
        raise AssertionError(f"{path} does not derive the empty clause")
    return additions, deletions


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=here / "proof_manifest.json")
    args = parser.parse_args()
    document = json.loads(args.result.read_text())

    low, infeasible, high, low_infeasible, high_infeasible = classified_types()
    expected_top = {
        "format": "r55-three-cycle-low-orbit-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "total_three_cycle_types": 154,
        "degree_infeasible_types": infeasible,
        "low_orbit_types": low_infeasible + len(low),
        "degree_infeasible_low_orbit_types": low_infeasible,
        "degree_infeasible_high_orbit_types": high_infeasible,
        "exact_low_orbit_types": len(low),
        "edge_orbit_cap": ORBIT_CAP,
        "feasible_high_orbit_types_open": high,
        "five_set_count": 962_598,
    }
    for key, value in expected_top.items():
        if document.get(key) != value:
            raise AssertionError(f"manifest mismatch at {key}")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != len(low):
        raise AssertionError("manifest case count mismatch")

    total_additions = total_deletions = total_bytes = 0
    for parts, case in zip(low, cases, strict=True):
        representatives, masks, orbit_sizes = reconstruct(parts)
        variables = len(representatives)
        clauses = clauses_from_masks(masks, variables)
        proof_path = here / case["proof_file"]
        expected_case = {
            "cycle_type": list(parts),
            "variable_count": variables,
            "edge_orbit_size_histogram": {
                str(size): count for size, count in sorted(orbit_sizes.items())
            },
            "distinct_five_set_masks": len(masks),
            "five_set_mask_size_histogram": {
                str(size): count
                for size, count in sorted(Counter(mask.bit_count() for mask in masks).items())
            },
            "clause_count": len(clauses),
            "color_swap_unit_clause": 1,
            "cnf_sha256": cnf_sha256(variables, clauses),
            "satisfiable": False,
        }
        for key, value in expected_case.items():
            if case.get(key) != value:
                raise AssertionError(f"case {parts} mismatch at {key}")
        if hashlib.sha256(proof_path.read_bytes()).hexdigest() != case["proof_sha256"]:
            raise AssertionError(f"case {parts} proof hash mismatch")
        if proof_path.stat().st_size != case["proof_byte_count"]:
            raise AssertionError(f"case {parts} proof size mismatch")
        additions, deletions = replay(variables, clauses, proof_path)
        if additions + deletions != case["proof_line_count"]:
            raise AssertionError(f"case {parts} proof line count mismatch")
        total_additions += additions
        total_deletions += deletions
        total_bytes += proof_path.stat().st_size
        print(
            f"PASS cycle_type={'+'.join(map(str, parts))} variables={variables} "
            f"clauses={len(clauses)} additions={additions} deletions={deletions}"
        )
    print(
        f"PASS replayed 26 proofs additions={total_additions} "
        f"deletions={total_deletions} proof_bytes={total_bytes}"
    )


if __name__ == "__main__":
    main()
