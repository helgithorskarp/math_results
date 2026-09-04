#!/usr/bin/env python3
"""Clean-room audit of the six cyclic order-15 Ramsey obstructions.

No submitted source is imported and no SAT solver or external proof checker
is called.  Pair orbits are classified by cycle positions and gcd invariants;
the retained traces are checked directly for RUP or RAT.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import lzma
import math
from pathlib import Path


ORDER = 43
CASES = (
    (1, 4, 2, 2),
    (2, 1, 0, 8),
    (2, 1, 1, 5),
    (2, 1, 2, 2),
    (2, 2, 0, 3),
    (2, 2, 1, 0),
)

EXPECTED = {
    (1, 4, 2, 2): {
        "variables": 99,
        "clauses": 120666,
        "cnf": "7bc3cd5254f45248274c3767c5dd822e510d9ceb07caa5acfbd2f93dd5e2921a",
        "proof": "d28640f1405838d96e2c28ebc5531a8960dcb0f0ed614d23022fdd3b0d60a954",
        "compressed": "695eb3cf070c10772b850472a723cb0a31bfab7d54703fb620723c3e327b04ee",
        "additions": 2098,
        "deletions": 3585,
    },
    (2, 1, 0, 8): {
        "variables": 93,
        "clauses": 121030,
        "cnf": "527f12749c74e49eb2efe961610a4a4ad5afb218e1db37967212be9bb3abb7ed",
        "proof": "8af30bdd51c327d0c7e3d2b3ede92a5d1d0eb823c867539ebf68be529d551c0a",
        "compressed": "a8582da4362384e38de38d08232e214f5479f3cc9c19ad11f3aca2f5dd08c8d5",
        "additions": 185,
        "deletions": 389,
    },
    (2, 1, 1, 5): {
        "variables": 79,
        "clauses": 119598,
        "cnf": "0892d64707c95c11c74f92688eea708a92232adcb91cc1061ee89cde57b46e97",
        "proof": "a5209a3216b933c7dd28534bb6752c57603c2454d3ade7180bcc0f2f78ce55f7",
        "compressed": "2b876a0974312edbb4c677805111f0a2f89d4592206b7e70f880fd8814a184d0",
        "additions": 173,
        "deletions": 379,
    },
    (2, 1, 2, 2): {
        "variables": 71,
        "clauses": 118788,
        "cnf": "673bce285ad3d5b5cfc9ff9b8747ebb04d6d9325664a6f19d184c3c185c3911e",
        "proof": "53a74375260eea66e182fb780a0c550dd4833222d07085cd06def2a772eb1ad0",
        "compressed": "6ddd1a6818dd8f923528c9374a9388a8a33ce0b1158a96a57728985b49ac1634",
        "additions": 2289,
        "deletions": 4330,
    },
    (2, 2, 0, 3): {
        "variables": 73,
        "clauses": 120846,
        "cnf": "4aa4041d0d9a2e708e6450615d35a57d15c6d693c2b78eaac16cdc7bb166f164",
        "proof": "77bab201fc165fa2519675e056a59bab46b44e7c51cf7d27c84910f3ea477f61",
        "compressed": "608e93370921d90b43c24ed0a4f3fcb4dc74b10436cf6dde821b277f8611fede",
        "additions": 568,
        "deletions": 940,
    },
    (2, 2, 1, 0): {
        "variables": 67,
        "clauses": 119446,
        "cnf": "68efaa8fc89e69959c25ad08a9601af8ca889f5aef19f09f3a7e68f3aa6bfd7e",
        "proof": "8730642076f0811b2f93f94e3f358bbae9766b2d50340b8c5023ac824d3d8b4f",
        "compressed": "ab33f6dbc34242d0519f478ded5bbdb5261ba3ae97c31e5e9e36624828a6c238",
        "additions": 2208,
        "deletions": 3452,
    },
}


def proof_name(case: tuple[int, int, int, int]) -> str:
    return "proof_a" + "_".join(map(str, case)) + ".drat.xz"


def power_filter() -> None:
    survivors = []
    for a in range(ORDER // 15 + 1):
        for b in range(ORDER // 5 + 1):
            for c in range(ORDER // 3 + 1):
                fixed = ORDER - 15 * a - 5 * b - 3 * c
                if fixed < 0:
                    continue
                lengths = [15] * a + [5] * b + [3] * c + [1] * fixed
                if math.lcm(*lengths) != 15:
                    continue
                if 3 * a + b in (7, 8) and 5 * a + c >= 7:
                    survivors.append((a, b, c, fixed))
    assert tuple(survivors) == CASES

    # The order-three dependency follows from degree >=18 and the bound
    # degree <= 2k+4 around a monochromatic moving triple.
    assert all(2 * cycles + 4 < 18 for cycles in range(1, 7))
    assert 2 * 7 + 4 == 18


def labeled_vertices(
    case: tuple[int, int, int, int]
) -> list[tuple[int, int, int]]:
    """Return (cycle identifier, cycle length, position) for each vertex."""
    result = []
    cycle_id = 0
    for length, count in zip((15, 5, 3, 1), case, strict=True):
        for _ in range(count):
            result.extend((cycle_id, length, position) for position in range(length))
            cycle_id += 1
    assert len(result) == ORDER
    return result


def edge_mapping(
    case: tuple[int, int, int, int]
) -> tuple[dict[tuple[int, int], int], dict[int, int]]:
    """Classify cyclic pair orbits by a CRT-complete signature.

    Within one odd cycle the unsigned cyclic difference is complete. Between
    cycles of lengths m,n, q-p modulo gcd(m,n) is complete because the two
    position congruences have a common shift precisely under that condition.
    """
    labels = labeled_vertices(case)
    classes: dict[tuple[object, ...], list[tuple[int, int]]] = {}
    for left in range(ORDER):
        left_cycle, left_length, left_position = labels[left]
        for right in range(left + 1, ORDER):
            right_cycle, right_length, right_position = labels[right]
            if left_cycle == right_cycle:
                difference = (right_position - left_position) % left_length
                difference = min(difference, left_length - difference)
                signature: tuple[object, ...] = (
                    "within",
                    left_cycle,
                    difference,
                )
                expected_size = left_length
            else:
                divisor = math.gcd(left_length, right_length)
                signature = (
                    "between",
                    left_cycle,
                    right_cycle,
                    (right_position - left_position) % divisor,
                )
                expected_size = math.lcm(left_length, right_length)
            classes.setdefault(signature, []).append((left, right))
            assert len(classes[signature]) <= expected_size

    for signature, edges in classes.items():
        if signature[0] == "within":
            cycle = int(signature[1])
            expected = labels[next(i for i, item in enumerate(labels) if item[0] == cycle)][1]
        else:
            first_cycle, second_cycle = int(signature[1]), int(signature[2])
            first_length = labels[next(i for i, item in enumerate(labels) if item[0] == first_cycle)][1]
            second_length = labels[next(i for i, item in enumerate(labels) if item[0] == second_cycle)][1]
            expected = math.lcm(first_length, second_length)
        assert len(edges) == expected

    ordered = sorted(classes.values(), key=min)
    mapping = {
        edge: variable
        for variable, edges in enumerate(ordered, 1)
        for edge in edges
    }
    distribution: dict[int, int] = {}
    for edges in ordered:
        distribution[len(edges)] = distribution.get(len(edges), 0) + 1
    assert len(mapping) == ORDER * (ORDER - 1) // 2
    return mapping, distribution


def build_formula(
    case: tuple[int, int, int, int]
) -> tuple[list[tuple[int, ...]], str]:
    mapping, _ = edge_mapping(case)
    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted(
            mapping[pair] for pair in itertools.combinations(vertices, 2)
        )
        distinct = tuple(sorted(set(variables)))
        clauses.add(distinct)
        clauses.add(tuple(-variable for variable in reversed(distinct)))
    ordered = sorted(clauses, key=lambda clause: (len(clause), clause))
    variables = max(mapping.values())
    digest = hashlib.sha256()
    digest.update(f"p cnf {variables} {len(ordered)}\n".encode("ascii"))
    for clause in ordered:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return ordered, digest.hexdigest()


class DRATDatabase:
    """Direct deletion, RUP, and RAT verifier for a small-variable formula."""

    def __init__(self, clauses: list[tuple[int, ...]], variables: int) -> None:
        self.variables = variables
        self.clauses = list(clauses)
        self.active = bytearray([1]) * len(clauses)
        self.occurrences = {
            literal: []
            for literal in range(-variables, variables + 1)
            if literal
        }
        self.by_clause: dict[tuple[int, ...], list[int]] = {}
        self.units: list[int] = []
        self.empties: list[int] = []
        for identifier, clause in enumerate(clauses):
            self._index(identifier, clause)

    def _index(self, identifier: int, clause: tuple[int, ...]) -> None:
        assert len(set(clause)) == len(clause)
        assert not any(-literal in clause for literal in clause)
        self.by_clause.setdefault(clause, []).append(identifier)
        if len(clause) == 0:
            self.empties.append(identifier)
        elif len(clause) == 1:
            self.units.append(identifier)
        for literal in clause:
            self.occurrences[literal].append(identifier)

    def rup(self, clause: tuple[int, ...]) -> bool:
        if any(self.active[identifier] for identifier in self.empties):
            return True
        value = [0] * (self.variables + 1)
        queue = [-literal for literal in clause]
        queue.extend(
            self.clauses[identifier][0]
            for identifier in self.units
            if self.active[identifier]
        )
        remaining: dict[int, int] = {}
        satisfied: set[int] = set()
        cursor = 0
        while cursor < len(queue):
            literal = queue[cursor]
            cursor += 1
            variable = abs(literal)
            sign = 1 if literal > 0 else -1
            if value[variable] == sign:
                continue
            if value[variable] == -sign:
                return True
            value[variable] = sign
            for identifier in self.occurrences[literal]:
                if self.active[identifier]:
                    satisfied.add(identifier)
            for identifier in self.occurrences[-literal]:
                if not self.active[identifier] or identifier in satisfied:
                    continue
                count = remaining.get(identifier, len(self.clauses[identifier])) - 1
                remaining[identifier] = count
                if count == 0:
                    return True
                if count == 1:
                    unit = next(
                        item
                        for item in self.clauses[identifier]
                        if value[abs(item)] == 0
                    )
                    queue.append(unit)
        return False

    def add(self, raw_clause: tuple[int, ...]) -> str:
        assert len(set(raw_clause)) == len(raw_clause)
        assert not any(-literal in raw_clause for literal in raw_clause)
        canonical = tuple(sorted(raw_clause))
        kind = "rup"
        if not self.rup(canonical):
            assert raw_clause, "empty clause is neither RUP nor RAT"
            kind = "rat"
            pivot = raw_clause[0]
            tail = set(raw_clause)
            tail.remove(pivot)
            for identifier in self.occurrences[-pivot]:
                if not self.active[identifier]:
                    continue
                resolvent = tail | (set(self.clauses[identifier]) - {-pivot})
                if any(-literal in resolvent for literal in resolvent):
                    continue
                ordered = tuple(sorted(resolvent))
                assert self.rup(ordered), (
                    "failed RAT resolvent",
                    raw_clause,
                    self.clauses[identifier],
                )

        identifier = len(self.clauses)
        self.clauses.append(canonical)
        self.active.append(1)
        self._index(identifier, canonical)
        return kind

    def delete(self, raw_clause: tuple[int, ...]) -> None:
        canonical = tuple(sorted(raw_clause))
        for identifier in reversed(self.by_clause.get(canonical, [])):
            if self.active[identifier]:
                self.active[identifier] = 0
                return
        raise AssertionError(("deletion of absent clause", raw_clause))


def checker_self_test() -> None:
    unit = DRATDatabase([(1,)], 2)
    assert unit.rup((1,)) and not unit.rup((2,))
    assert unit.add((2,)) == "rat"  # vacuous pivot: no clause contains -2

    nonvacuous = DRATDatabase([(-2, 1)], 2)
    assert not nonvacuous.rup((-1, 2))
    assert nonvacuous.add((2, -1)) == "rat"  # tautological pivot resolvent

    invalid = DRATDatabase([(-2, 1)], 2)
    try:
        invalid.add((2,))
    except AssertionError:
        pass
    else:
        raise AssertionError("invalid RAT addition was accepted")

    chain = DRATDatabase([(1, 2), (-1, 2), (-2,)], 2)
    assert chain.rup(())


def check_proof(
    clauses: list[tuple[int, ...]],
    variables: int,
    path: Path,
    expected: dict[str, object],
) -> tuple[int, int, int, int, int]:
    compressed = path.read_bytes()
    assert hashlib.sha256(compressed).hexdigest() == expected["compressed"]
    proof = lzma.decompress(compressed)
    assert hashlib.sha256(proof).hexdigest() == expected["proof"]
    records: list[tuple[bool, tuple[int, ...]]] = []
    proof_variables = variables
    for number, line in enumerate(proof.decode("ascii").splitlines(), 1):
        fields = line.split()
        deletion = fields[0] == "d"
        if deletion:
            fields = fields[1:]
        assert fields and fields[-1] == "0", (number, line)
        raw_clause = tuple(map(int, fields[:-1]))
        if raw_clause:
            proof_variables = max(proof_variables, *(abs(item) for item in raw_clause))
        records.append((deletion, raw_clause))

    # DRAT may introduce fresh variables.  They have no original occurrences
    # and are admitted only through checked RUP/RAT additions.
    database = DRATDatabase(clauses, proof_variables)
    additions = deletions = rup = rat = 0
    last_added: tuple[int, ...] | None = None
    for deletion, raw_clause in records:
        if deletion:
            database.delete(raw_clause)
            deletions += 1
        else:
            kind = database.add(raw_clause)
            rup += kind == "rup"
            rat += kind == "rat"
            additions += 1
            last_added = raw_clause
    assert last_added == ()
    assert additions == expected["additions"]
    assert deletions == expected["deletions"]
    assert rup + rat == additions
    return additions, deletions, rup, rat, proof_variables


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("proof_directory", type=Path)
    args = parser.parse_args()
    checker_self_test()
    power_filter()
    total_rup = total_rat = 0
    for case in CASES:
        expected = EXPECTED[case]
        clauses, digest = build_formula(case)
        mapping, distribution = edge_mapping(case)
        variables = max(mapping.values())
        assert variables == expected["variables"]
        assert len(clauses) == expected["clauses"]
        assert digest == expected["cnf"]
        additions, deletions, rup, rat, proof_variables = check_proof(
            clauses,
            variables,
            args.proof_directory / proof_name(case),
            expected,
        )
        total_rup += rup
        total_rat += rat
        print(
            f"PASS case={case} variables={variables} clauses={len(clauses)} "
            f"orbit_sizes={distribution} cnf_sha256={digest} "
            f"proof_variables={proof_variables} additions={additions} "
            f"deletions={deletions} rup={rup} rat={rat}"
        )
    print(
        f"PASS all_cases=6 final_empty=6 total_rup={total_rup} "
        f"total_rat={total_rat}"
    )


if __name__ == "__main__":
    main()
