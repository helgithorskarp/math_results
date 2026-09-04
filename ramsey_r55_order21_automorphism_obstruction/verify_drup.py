#!/usr/bin/env python3
"""Rebuild the order-21 Ramsey CNF and independently replay its DRUP proof."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from dataclasses import dataclass
from pathlib import Path


ORDER = 43
GENERATOR = 9
GROUP_ORDER = 21
VARIABLE_COUNT = 43


def canonical_edge(edge: tuple[int, int]) -> tuple[int, int]:
    images = []
    multiplier = 1
    for _ in range(GROUP_ORDER):
        images.append(
            tuple(sorted((multiplier * edge[0] % ORDER, multiplier * edge[1] % ORDER)))
        )
        multiplier = multiplier * GENERATOR % ORDER
    if multiplier != 1 or len(set(images)) != GROUP_ORDER:
        raise AssertionError("9 does not generate the required order-21 action")
    return min(images)


def reconstruct_masks() -> tuple[list[tuple[int, int]], set[int], list[int]]:
    representatives = sorted({canonical_edge(edge) for edge in itertools.combinations(range(ORDER), 2)})
    if len(representatives) != VARIABLE_COUNT:
        raise AssertionError("expected 43 edge orbits")
    representative_to_variable = {
        representative: index for index, representative in enumerate(representatives)
    }
    edge_to_variable = {
        edge: representative_to_variable[canonical_edge(edge)]
        for edge in itertools.combinations(range(ORDER), 2)
    }
    masks = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        mask = 0
        for edge in itertools.combinations(vertices, 2):
            mask |= 1 << edge_to_variable[edge]
        masks.add(mask)
    if len(masks) != 43_655:
        raise AssertionError("unexpected full mask count")

    minimal = []
    mask_set = set(masks)
    for mask in sorted(mask_set, key=lambda value: (value.bit_count(), value)):
        submask = (mask - 1) & mask
        while submask and submask not in mask_set:
            submask = (submask - 1) & mask
        if not submask:
            minimal.append(mask)
    if len(minimal) != 32_126:
        raise AssertionError("unexpected minimal mask count")

    # Explicitly check that each discarded five-set constraint contains an
    # included constraint, which proves the subsumption reduction sound.
    minimal_set = set(minimal)
    for mask in masks:
        submask = mask
        while submask and submask not in minimal_set:
            submask = (submask - 1) & mask
        if not submask:
            raise AssertionError("minimal masks do not cover every five-set mask")
    return representatives, masks, minimal


def clauses_from_masks(masks: list[int]) -> list[tuple[int, ...]]:
    clauses = []
    for mask in masks:
        variables = tuple(index + 1 for index in range(VARIABLE_COUNT) if mask >> index & 1)
        clauses.append(variables)
        clauses.append(tuple(-variable for variable in variables))
    clauses.append((1,))
    return clauses


def dimacs_sha256(clauses: list[tuple[int, ...]]) -> str:
    digest = hashlib.sha256()
    digest.update(f"p cnf {VARIABLE_COUNT} {len(clauses)}\n".encode())
    for clause in clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode())
    return digest.hexdigest()


@dataclass
class WatchedClause:
    literals: tuple[int, ...]
    first: int
    second: int


class RupChecker:
    """A small watched-literal reverse-unit-propagation checker."""

    def __init__(self, variable_count: int, initial: list[tuple[int, ...]]) -> None:
        self.variable_count = variable_count
        self.clauses: list[WatchedClause] = []
        self.watchers = {literal: [] for variable in range(1, variable_count + 1) for literal in (variable, -variable)}
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

    def add_clause(self, raw_clause: tuple[int, ...]) -> None:
        clause = self.normalize(raw_clause)
        if clause is None:
            return
        if any(literal == 0 or abs(literal) > self.variable_count for literal in clause):
            raise ValueError("proof literal outside the declared variable range")
        if not clause:
            self.empty_present = True
            return
        if len(clause) == 1:
            self.units.append(clause[0])
            return
        index = len(self.clauses)
        self.clauses.append(WatchedClause(clause, 0, 1))
        self.watchers[clause[0]].append(index)
        self.watchers[clause[1]].append(index)

    @staticmethod
    def literal_value(literal: int, assignment: list[int]) -> int:
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

    def rup(self, raw_clause: tuple[int, ...]) -> bool:
        clause = self.normalize(raw_clause)
        if clause is None:
            return True
        assignment = [0] * (self.variable_count + 1)
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
                    false_watch = record.first
                    other_watch = record.second
                    replace_first = True
                elif record.literals[record.second] == false_literal:
                    false_watch = record.second
                    other_watch = record.first
                    replace_first = False
                else:
                    raise AssertionError("watch list is inconsistent")

                other_literal = record.literals[other_watch]
                if self.literal_value(other_literal, assignment) == 1:
                    position += 1
                    continue

                replacement = None
                for candidate_index, candidate in enumerate(record.literals):
                    if candidate_index in (false_watch, other_watch):
                        continue
                    if self.literal_value(candidate, assignment) != -1:
                        replacement = candidate_index
                        break
                if replacement is not None:
                    if replace_first:
                        record.first = replacement
                    else:
                        record.second = replacement
                    watched[position] = watched[-1]
                    watched.pop()
                    self.watchers[record.literals[replacement]].append(clause_index)
                    continue

                other_value = self.literal_value(other_literal, assignment)
                if other_value == -1:
                    return True
                if not self.enqueue(other_literal, assignment, trail):
                    return True
                position += 1
        return self.empty_present


def parse_proof_line(line: str) -> tuple[bool, tuple[int, ...]]:
    fields = line.split()
    deletion = bool(fields and fields[0] == "d")
    if deletion:
        fields = fields[1:]
    if not fields or fields[-1] != "0":
        raise ValueError("proof line is not zero-terminated")
    return deletion, tuple(map(int, fields[:-1]))


def verify_proof(clauses: list[tuple[int, ...]], proof_path: Path) -> tuple[int, int]:
    checker = RupChecker(VARIABLE_COUNT, clauses)
    additions = deletions = 0
    derived_empty = False
    for number, line in enumerate(proof_path.read_text().splitlines(), start=1):
        if not line.strip():
            raise ValueError(f"blank proof line {number}")
        deletion, clause = parse_proof_line(line)
        if deletion:
            # Retaining already proved clauses is sound and avoids trusting
            # deletion bookkeeping: every retained clause remains a logical
            # consequence of the original formula.
            deletions += 1
            continue
        additions += 1
        if not checker.rup(clause):
            raise AssertionError(f"proof addition {number} is not RUP")
        checker.add_clause(clause)
        if not clause:
            derived_empty = True
    if not derived_empty:
        raise AssertionError("proof did not derive the empty clause")
    return additions, deletions


def main() -> None:
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--proof", type=Path, default=here / "obstruction.drup")
    parser.add_argument("--result", type=Path, default=here / "result.json")
    arguments = parser.parse_args()

    document = json.loads(arguments.result.read_text())
    representatives, masks, minimal = reconstruct_masks()
    clauses = clauses_from_masks(minimal)
    expected = {
        "format": "r55-order21-automorphism-obstruction-v1",
        "order": ORDER,
        "vertex_orbit_sizes": [1, 21, 21],
        "edge_orbit_count": len(representatives),
        "edge_orbit_size_histogram": {"21": 43},
        "five_set_count": 962_598,
        "distinct_five_set_masks": len(masks),
        "five_set_mask_size_histogram": {
            str(key): value for key, value in sorted(Counter(x.bit_count() for x in masks).items())
        },
        "inclusion_minimal_mask_count": len(minimal),
        "minimal_mask_size_histogram": {
            str(key): value for key, value in sorted(Counter(x.bit_count() for x in minimal).items())
        },
        "variable_count": VARIABLE_COUNT,
        "clause_count": len(clauses),
        "color_swap_unit_clause": 1,
        "cnf_sha256": dimacs_sha256(clauses),
        "satisfiable": False,
    }
    for key, value in expected.items():
        if document.get(key) != value:
            raise AssertionError(f"result metadata mismatch at {key}")
    if hashlib.sha256(arguments.proof.read_bytes()).hexdigest() != document["proof_sha256"]:
        raise AssertionError("proof hash mismatch")
    if arguments.proof.stat().st_size != document["proof_byte_count"]:
        raise AssertionError("proof byte count mismatch")

    additions, deletions = verify_proof(clauses, arguments.proof)
    if additions + deletions != document["proof_line_count"]:
        raise AssertionError("proof line count mismatch")
    print("PASS independently rebuilt CNF and replayed DRUP proof")
    print(
        f"variables={VARIABLE_COUNT} clauses={len(clauses)} "
        f"five_set_masks={len(masks)} minimal_masks={len(minimal)}"
    )
    print(
        f"proof_lines={additions + deletions} additions={additions} deletions={deletions} "
        f"proof_sha256={document['proof_sha256']}"
    )


if __name__ == "__main__":
    main()
