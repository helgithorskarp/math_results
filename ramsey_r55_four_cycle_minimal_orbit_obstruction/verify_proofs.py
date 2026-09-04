#!/usr/bin/env python3
"""Independently reconstruct and replay the minimal-orbit four-cycle family."""

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
VARIABLES = 26


def orbit_count(parts: tuple[int, ...]) -> int:
    return sum(length // 2 for length in parts) + sum(
        math.gcd(parts[i], parts[j])
        for i in range(4)
        for j in range(i + 1, 4)
    )


def degree_feasible(parts: tuple[int, ...]) -> bool:
    pairs = [(i, j, math.gcd(parts[i], parts[j])) for i in range(4) for j in range(i + 1, 4)]
    internal = [
        set(range(length)) if length % 2 == 0 else set(range(0, length, 2))
        for length in parts
    ]
    for selected in itertools.product(*(range(divisor + 1) for _, _, divisor in pairs)):
        cross = [0, 0, 0, 0]
        for (i, j, divisor), count in zip(pairs, selected, strict=True):
            cross[i] += count * parts[j] // divisor
            cross[j] += count * parts[i] // divisor
        if all(any(18 <= cross[i] + d <= 24 for d in internal[i]) for i in range(4)):
            return True
    return False


def cycle_types() -> tuple[list[tuple[int, ...]], int]:
    partitions = []
    for first in range(1, ORDER // 4 + 1):
        for second in range(first, ORDER + 1):
            for third in range(second, ORDER + 1):
                fourth = ORDER - first - second - third
                if fourth < third:
                    continue
                partitions.append((first, second, third, fourth))
    minimum = min(map(orbit_count, partitions))
    minimal = [parts for parts in partitions if orbit_count(parts) == minimum]
    feasible = [parts for parts in minimal if degree_feasible(parts)]
    if (len(partitions), minimum, len(minimal), len(feasible)) != (588, 26, 131, 75):
        raise AssertionError("unexpected independent census")
    return feasible, len(minimal) - len(feasible)


def advance(vertex: int, parts: tuple[int, ...]) -> int:
    start = 0
    for length in parts:
        if vertex < start + length:
            return start + (vertex - start + 1) % length
        start += length
    raise AssertionError("vertex outside partition")


def canonical_edge(edge: tuple[int, int], parts: tuple[int, ...]) -> tuple[int, int]:
    seed = edge
    images = []
    while not images or edge != seed:
        images.append(edge)
        edge = tuple(sorted((advance(edge[0], parts), advance(edge[1], parts))))
    if len(set(images)) != len(images):
        raise AssertionError("edge orbit repeats early")
    return min(images)


def reconstruct(parts: tuple[int, ...]) -> tuple[set[int], Counter[int]]:
    edges = list(itertools.combinations(range(ORDER), 2))
    representatives = {edge: canonical_edge(edge, parts) for edge in edges}
    ordered = sorted(set(representatives.values()))
    if len(ordered) != VARIABLES:
        raise AssertionError("edge-orbit count mismatch")
    index = {representative: variable for variable, representative in enumerate(ordered)}
    edge_variable = {edge: index[representative] for edge, representative in representatives.items()}
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
    orbit_sizes = Counter(Counter(representatives.values()).values())
    return masks, orbit_sizes


def clauses_from_masks(masks: set[int]) -> list[tuple[int, ...]]:
    clauses = []
    for mask in sorted(masks):
        positive = tuple(i + 1 for i in range(VARIABLES) if mask >> i & 1)
        clauses.extend((positive, tuple(-literal for literal in positive)))
    clauses.append((1,))
    return clauses


def cnf_sha256(clauses: list[tuple[int, ...]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {VARIABLES} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


@dataclass
class WatchedClause:
    literals: tuple[int, ...]
    first: int
    second: int


class RupChecker:
    def __init__(self, initial: list[tuple[int, ...]]) -> None:
        self.clauses: list[WatchedClause] = []
        self.watchers = {
            literal: []
            for variable in range(1, VARIABLES + 1)
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
        if any(literal == 0 or abs(literal) > VARIABLES for literal in clause):
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
        assignment = [0] * (VARIABLES + 1)
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


def parse_line(line: str) -> tuple[bool, tuple[int, ...]]:
    fields = line.split()
    deletion = bool(fields and fields[0] == "d")
    if deletion:
        fields = fields[1:]
    if not fields or fields[-1] != "0":
        raise ValueError("proof line is not zero-terminated")
    return deletion, tuple(map(int, fields[:-1]))


def replay(clauses: list[tuple[int, ...]], path: Path) -> tuple[int, int]:
    checker = RupChecker(clauses)
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
        raise AssertionError("proof did not derive empty clause")
    return additions, deletions


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path, default=here / "proof_manifest.json")
    args = parser.parse_args()
    document = json.loads(args.result.read_text())
    types, infeasible = cycle_types()
    expected_top = {
        "format": "r55-four-cycle-minimal-orbit-obstruction-v1",
        "order": ORDER,
        "degree_window": [18, 24],
        "total_four_cycle_types": 588,
        "minimum_edge_orbit_count": VARIABLES,
        "minimum_orbit_types": 131,
        "degree_infeasible_minimum_orbit_types": infeasible,
        "certified_minimum_orbit_types": len(types),
        "five_set_count": 962_598,
    }
    for key, value in expected_top.items():
        if document.get(key) != value:
            raise AssertionError(f"manifest mismatch at {key}")
    cases = document.get("cases")
    if not isinstance(cases, list) or len(cases) != len(types):
        raise AssertionError("manifest case count mismatch")

    additions = deletions = proof_bytes = 0
    for index, (parts, case) in enumerate(zip(types, cases, strict=True), start=1):
        masks, orbit_sizes = reconstruct(parts)
        clauses = clauses_from_masks(masks)
        expected_case = {
            "cycle_type": list(parts),
            "variable_count": VARIABLES,
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
            "cnf_sha256": cnf_sha256(clauses),
            "satisfiable": False,
        }
        for key, value in expected_case.items():
            if case.get(key) != value:
                raise AssertionError(f"case {parts} mismatch at {key}")
        path = here / case["proof_file"]
        if hashlib.sha256(path.read_bytes()).hexdigest() != case["proof_sha256"]:
            raise AssertionError(f"case {parts} proof hash mismatch")
        if path.stat().st_size != case["proof_byte_count"]:
            raise AssertionError(f"case {parts} proof size mismatch")
        added, deleted = replay(clauses, path)
        if added + deleted != case["proof_line_count"]:
            raise AssertionError(f"case {parts} proof line count mismatch")
        additions += added
        deletions += deleted
        proof_bytes += path.stat().st_size
        print(
            f"PASS case={index}/75 cycle_type={'+'.join(map(str, parts))} "
            f"clauses={len(clauses)} additions={added} deletions={deleted}",
            flush=True,
        )
    print(
        f"PASS replayed 75 proofs additions={additions} "
        f"deletions={deletions} proof_bytes={proof_bytes}",
        flush=True,
    )


if __name__ == "__main__":
    main()
