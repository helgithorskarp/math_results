#!/usr/bin/env python3
"""Definition-level verifier for seven order-21 HOP certificates.

This checker does not implement the orbit exact-cover search.  It expands
each retained pair of starters into all 40 meals and checks the seating
definition directly using exact Python sets and counters.
"""

from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


MODULUS = 20
INFINITY = 20
ROOT = Path(__file__).resolve().parent
Person = tuple[int, int]
Edge = tuple[Person, Person]
Factor = tuple[Edge, ...]
EXPECTED_TYPES = {
    (16, 3, 2),
    (15, 4, 2),
    (14, 5, 2),
    (13, 6, 2),
    (12, 7, 2),
    (11, 8, 2),
    (10, 9, 2),
}


def require_plain_int(value: object, name: str) -> int:
    if type(value) is not int:
        raise ValueError(f"{name} is not an integer")
    return value


def canonical_edge(left: Person, right: Person) -> Edge:
    for couple, bit in (left, right):
        if not 0 <= couple <= INFINITY:
            raise ValueError("couple outside 0,...,20")
        if bit not in (0, 1):
            raise ValueError("spouse bit is not zero or one")
    if left[0] == right[0]:
        raise ValueError("external edge joins one couple")
    return tuple(sorted((left, right)))  # type: ignore[return-value]


def parse_endpoint(raw: object) -> Person:
    if not isinstance(raw, list) or len(raw) != 2:
        raise ValueError("malformed endpoint")
    return (
        require_plain_int(raw[0], "couple"),
        require_plain_int(raw[1], "spouse bit"),
    )


def parse_factor(raw: object) -> Factor:
    if not isinstance(raw, list) or len(raw) != 21:
        raise ValueError("a stored starter must contain 21 edges")
    edges = []
    for item in raw:
        if not isinstance(item, list) or len(item) != 2:
            raise ValueError("malformed edge")
        edges.append(canonical_edge(parse_endpoint(item[0]), parse_endpoint(item[1])))
    if len(set(edges)) != 21:
        raise ValueError("a stored starter repeats an edge")
    return tuple(sorted(edges))


def rotate_person(person: Person, shift: int) -> Person:
    couple, bit = person
    return (couple if couple == INFINITY else (couple + shift) % MODULUS, bit)


def rotate_factor(factor: Factor, shift: int) -> Factor:
    return tuple(
        sorted(
            canonical_edge(rotate_person(left, shift), rotate_person(right, shift))
            for left, right in factor
        )
    )


def determined_second_starter(first: Factor) -> Factor:
    second = set(rotate_factor(first, MODULUS // 2))
    same_zero = canonical_edge((0, 0), (10, 0))
    same_one = canonical_edge((0, 1), (10, 1))
    cross_one = canonical_edge((0, 0), (10, 1))
    cross_two = canonical_edge((0, 1), (10, 0))
    if same_zero not in second or same_one not in second:
        raise ValueError("half-turn lacks the prescribed same-bit 2-cycle")
    second.remove(same_zero)
    second.remove(same_one)
    second.add(cross_one)
    second.add(cross_two)
    return tuple(sorted(second))


def person_cycle_lengths(factor: Factor) -> tuple[int, ...]:
    all_people = {(couple, bit) for couple in range(21) for bit in range(2)}
    incidence = Counter(person for edge in factor for person in edge)
    if set(incidence) != all_people or set(incidence.values()) != {1}:
        raise ValueError("external factor is not a perfect matching")

    adjacency: dict[Person, list[Person]] = defaultdict(list)
    for left, right in factor:
        adjacency[left].append(right)
        adjacency[right].append(left)
    for couple in range(21):
        left, right = (couple, 0), (couple, 1)
        adjacency[left].append(right)
        adjacency[right].append(left)
    if any(len(adjacency[person]) != 2 for person in all_people):
        raise AssertionError("meal plus spouse matching is not 2-regular")

    seen: set[Person] = set()
    lengths = []
    for root in sorted(all_people):
        if root in seen:
            continue
        stack = [root]
        component: set[Person] = set()
        while stack:
            person = stack.pop()
            if person in component:
                continue
            component.add(person)
            seen.add(person)
            stack.extend(
                neighbour
                for neighbour in adjacency[person]
                if neighbour not in component
            )
        lengths.append(len(component))
    return tuple(sorted(lengths, reverse=True))


def canonical_schedule_bytes(meals_by_type: dict[tuple[int, ...], list[Factor]]) -> bytes:
    serial = []
    for target in sorted(meals_by_type, reverse=True):
        meals = [
            [[list(left), list(right)] for left, right in factor]
            for factor in meals_by_type[target]
        ]
        serial.append({"type": list(target), "meals": meals})
    return json.dumps(serial, separators=(",", ":"), sort_keys=True).encode()


def verify_records(records: object) -> dict[tuple[int, ...], list[Factor]]:
    if not isinstance(records, list):
        raise ValueError("certificate collection is not a list")
    declared_types = []
    meals_by_type: dict[tuple[int, ...], list[Factor]] = {}
    expected_external_edges = {
        canonical_edge((u, a), (v, b))
        for u in range(21)
        for v in range(u + 1, 21)
        for a in range(2)
        for b in range(2)
    }
    assert len(expected_external_edges) == 840

    for record in records:
        if not isinstance(record, dict):
            raise ValueError("certificate record is not an object")
        if require_plain_int(record.get("n"), "n") != 21:
            raise ValueError("certificate has wrong order")
        raw_type = record.get("type")
        if not isinstance(raw_type, list) or len(raw_type) != 3:
            raise ValueError("certificate has malformed type")
        target = tuple(require_plain_int(value, "type entry") for value in raw_type)
        if target not in EXPECTED_TYPES:
            raise ValueError(f"unexpected type {target}")
        declared_types.append(target)

        first = parse_factor(record.get("F1"))
        third = parse_factor(record.get("F3"))
        required_same_bit = {
            canonical_edge((0, 0), (10, 0)),
            canonical_edge((0, 1), (10, 1)),
        }
        if not required_same_bit <= set(first):
            raise ValueError("F1 lacks the prescribed difference-10 2-cycle")
        second = determined_second_starter(first)
        target_person_lengths = tuple(2 * length for length in target)
        for index, starter in enumerate((first, second, third), start=1):
            actual = person_cycle_lengths(starter)
            if actual != target_person_lengths:
                raise ValueError(
                    f"type {target} starter F{index} has person cycles {actual}"
                )

        meals = [rotate_factor(first, shift) for shift in range(10)]
        meals += [rotate_factor(second, shift) for shift in range(10)]
        meals += [rotate_factor(third, shift) for shift in range(20)]
        if len(meals) != 40 or len(set(meals)) != 40:
            raise ValueError(f"type {target} does not give 40 distinct meals")
        if any(person_cycle_lengths(meal) != target_person_lengths for meal in meals):
            raise ValueError(f"type {target} has a developed meal of wrong type")
        counts = Counter(edge for meal in meals for edge in meal)
        if set(counts) != expected_external_edges or set(counts.values()) != {1}:
            missing = len(expected_external_edges - set(counts))
            repeated = sum(value - 1 for value in counts.values() if value > 1)
            raise ValueError(
                f"type {target} has inexact coverage: "
                f"missing={missing}, repeated={repeated}"
            )
        meals_by_type[target] = meals

    if len(declared_types) != len(set(declared_types)):
        raise ValueError("certificate collection repeats a type")
    if set(declared_types) != EXPECTED_TYPES:
        raise ValueError("certificate collection does not contain exactly seven types")
    return meals_by_type


def load_records() -> tuple[bytes, list[dict[str, Any]]]:
    raw = (ROOT / "certificates.jsonl").read_bytes()
    lines = [line for line in raw.splitlines() if line.strip()]
    return raw, [json.loads(line) for line in lines]


def mutation_tests(records: list[dict[str, Any]]) -> int:
    mutations: list[list[dict[str, Any]]] = []

    missing_type = copy.deepcopy(records)
    missing_type.pop()
    mutations.append(missing_type)

    repeated_edge = copy.deepcopy(records)
    repeated_edge[0]["F3"][0] = copy.deepcopy(repeated_edge[0]["F3"][1])
    mutations.append(repeated_edge)

    wrong_type = copy.deepcopy(records)
    wrong_type[1]["type"] = [16, 3, 2]
    mutations.append(wrong_type)

    changed_endpoint = copy.deepcopy(records)
    changed_endpoint[2]["F3"][0][0][1] ^= 1
    mutations.append(changed_endpoint)

    for index, mutation in enumerate(mutations, start=1):
        try:
            verify_records(mutation)
        except (AssertionError, KeyError, TypeError, ValueError):
            continue
        raise AssertionError(f"mutation {index} was not rejected")
    return len(mutations)


def main() -> None:
    raw, records = load_records()
    meals_by_type = verify_records(records)
    rejected = mutation_tests(records)
    print("order=21 mixed_three_table_types=7")
    for target in sorted(meals_by_type, reverse=True):
        table_sizes = tuple(2 * length for length in target)
        print(
            f"type={target} tables={table_sizes} meals=40 "
            "external_edges=840 coverage_multiplicity=1"
        )
    print(f"mutation_tests_rejected={rejected}")
    print(f"certificates_sha256={hashlib.sha256(raw).hexdigest()}")
    print(
        "developed_schedules_sha256="
        f"{hashlib.sha256(canonical_schedule_bytes(meals_by_type)).hexdigest()}"
    )
    print("VERIFIED all mixed order-21 three-table HOP types with one 4-table")


if __name__ == "__main__":
    main()
