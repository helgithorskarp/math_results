#!/usr/bin/env python3
"""Clean-room audit of the C5^2 Ramsey(5,5;43) obstruction.

This checker does not import the submitted implementation and does not call a
SAT solver or drat-trim.  It constructs the action from two generators,
rebuilds the invariant Ramsey CNF, and checks every addition in the retained
trace by reverse unit propagation (RUP).
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import lzma
from pathlib import Path


N = 43
EXPECTED_CNF_SHA256 = (
    "ffb03c6ae916ee712a94a66f5cbbfc85d86ae08e19e4476a6e8c504e2505561f"
)
EXPECTED_PROOF_SHA256 = (
    "f440cfb407bd02866aad61a02686d56441cfaf4389099e00b8074e2c9c56a8a3"
)


def action(vertex: int, u: int, v: int) -> int:
    """The forced F_5^2 action, expressed through its four orbit types."""
    if vertex < 3:
        return vertex
    if vertex < 8:
        return 3 + (vertex - 3 + u) % 5
    if vertex < 13:
        return 8 + (vertex - 8 + v) % 5
    if vertex < 18:
        return 13 + (vertex - 13 + v - u) % 5
    x, y = divmod(vertex - 18, 5)
    return 18 + 5 * ((x + u) % 5) + (y + v) % 5


def forced_set_classification() -> None:
    """Enumerate all orbit-count solutions and projective-line triples."""
    solutions = []
    for fixed in range(N + 1):
        choices = [b for b in range(9) if fixed + 5 * b in (3, 8)]
        for counts in itertools.product(choices, repeat=6):
            for regular in range(2):
                if fixed + 5 * sum(counts) + 25 * regular == N:
                    solutions.append((fixed, counts, regular))
    expected = {
        (3, counts, 1)
        for counts in itertools.product((0, 1), repeat=6)
        if sum(counts) == 3
    }
    assert set(solutions) == expected and len(solutions) == 20

    # Lines are normalized nonzero vectors: infinity plus slopes 0,...,4.
    reps = [(0, 1)] + [(1, slope) for slope in range(5)]
    index = {rep: i for i, rep in enumerate(reps)}

    def normalize(x: int, y: int) -> tuple[int, int]:
        if x % 5 == 0:
            return (0, 1)
        inverse = pow(x % 5, -1, 5)
        return (1, y * inverse % 5)

    images = set()
    for a, b, c, d in itertools.product(range(5), repeat=4):
        if (a * d - b * c) % 5 == 0:
            continue
        permutation = tuple(
            index[normalize(a * x + b * y, c * x + d * y)]
            for x, y in reps
        )
        images.add(tuple(sorted(permutation[i] for i in (0, 1, 2))))
    assert len(images) == 20

    # A 25-cycle becomes exactly five 5-cycles under the fifth power;
    # any original 5-cycles become fixed.
    fifth_power_counts = []
    for old_five_cycles in range(4):
        fixed = N - 25 - 5 * old_five_cycles
        assert fixed in (18, 13, 8, 3)
        fifth_power_counts.append(5)
    assert set(fifth_power_counts).isdisjoint({7, 8})


def edge_orbits() -> tuple[dict[tuple[int, int], int], dict[int, int]]:
    """Find edge components using only the two F_5^2 generators."""
    pairs = [(a, b) for a in range(N) for b in range(a + 1, N)]
    unseen = set(pairs)
    components: list[list[tuple[int, int]]] = []
    while unseen:
        seed = min(unseen)
        component = {seed}
        frontier = [seed]
        while frontier:
            left, right = frontier.pop()
            for u, v in ((1, 0), (0, 1)):
                image = tuple(sorted((action(left, u, v), action(right, u, v))))
                if image not in component:
                    component.add(image)
                    frontier.append(image)
        unseen.difference_update(component)
        components.append(sorted(component))
    components.sort(key=lambda part: part[0])
    mapping = {
        edge: variable
        for variable, component in enumerate(components, 1)
        for edge in component
    }
    distribution: dict[int, int] = {}
    for component in components:
        distribution[len(component)] = distribution.get(len(component), 0) + 1
    assert len(mapping) == N * (N - 1) // 2
    assert len(components) == 51
    assert distribution == {1: 3, 5: 15, 25: 33}
    return mapping, distribution


def formula() -> tuple[list[tuple[int, ...]], str]:
    mapping, _ = edge_orbits()
    clauses: set[tuple[int, ...]] = set()
    for vertices in itertools.combinations(range(N), 5):
        variables = sorted(
            {
                mapping[(left, right)]
                for left, right in itertools.combinations(vertices, 2)
            }
        )
        positive = tuple(variables)
        negative = tuple(-variable for variable in reversed(variables))
        clauses.add(positive)
        clauses.add(negative)
    ordered = sorted(clauses, key=lambda clause: (len(clause), clause))
    digest = hashlib.sha256()
    digest.update(f"p cnf 51 {len(ordered)}\n".encode("ascii"))
    for clause in ordered:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    hexdigest = digest.hexdigest()
    assert len(ordered) == 52362
    assert hexdigest == EXPECTED_CNF_SHA256
    return ordered, hexdigest


class RUPDatabase:
    """Small proof database with a direct watched-occurrence RUP check."""

    def __init__(self, original: list[tuple[int, ...]]) -> None:
        self.clauses = list(original)
        self.active = bytearray([1]) * len(original)
        self.occurrences = {literal: [] for literal in range(-51, 52) if literal}
        self.by_clause: dict[tuple[int, ...], list[int]] = {}
        for identifier, clause in enumerate(original):
            self._index(identifier, clause)

    def _index(self, identifier: int, clause: tuple[int, ...]) -> None:
        assert len(set(clause)) == len(clause)
        assert not any(-literal in clause for literal in clause)
        for literal in clause:
            self.occurrences[literal].append(identifier)
        self.by_clause.setdefault(clause, []).append(identifier)

    def rup_conflict(self, proposed: tuple[int, ...]) -> bool:
        count = len(self.clauses)
        remaining = [len(clause) for clause in self.clauses]
        satisfied = bytearray(count)
        value = [0] * 52
        queue = [-literal for literal in proposed]
        for identifier, clause in enumerate(self.clauses):
            if not self.active[identifier]:
                continue
            if not clause:
                return True
            if len(clause) == 1:
                queue.append(clause[0])

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
                    satisfied[identifier] = 1
            for identifier in self.occurrences[-literal]:
                if not self.active[identifier] or satisfied[identifier]:
                    continue
                remaining[identifier] -= 1
                if remaining[identifier] == 0:
                    return True
                if remaining[identifier] == 1:
                    unit = next(
                        item
                        for item in self.clauses[identifier]
                        if value[abs(item)] == 0
                    )
                    queue.append(unit)
        return False

    def add_rup(self, clause: tuple[int, ...]) -> None:
        assert self.rup_conflict(clause), ("non-RUP addition", clause)
        identifier = len(self.clauses)
        self.clauses.append(clause)
        self.active.append(1)
        self._index(identifier, clause)

    def delete(self, clause: tuple[int, ...]) -> None:
        identifiers = self.by_clause.get(clause, [])
        for identifier in reversed(identifiers):
            if self.active[identifier]:
                self.active[identifier] = 0
                return
        raise AssertionError(("deletion of absent clause", clause))


def rup_self_test() -> None:
    database = RUPDatabase([(1,)])
    assert database.rup_conflict((1,))
    assert not database.rup_conflict((2,))
    database.delete((1,))
    assert not database.rup_conflict((1,))

    unit_chain = RUPDatabase([(1, 2), (-1, 2), (-2,)])
    assert unit_chain.rup_conflict(())


def check_proof(original: list[tuple[int, ...]], proof_path: Path) -> tuple[int, int]:
    compressed = proof_path.read_bytes()
    proof = lzma.decompress(compressed)
    assert hashlib.sha256(proof).hexdigest() == EXPECTED_PROOF_SHA256
    database = RUPDatabase(original)
    additions = deletions = 0
    last_added: tuple[int, ...] | None = None
    for number, raw in enumerate(proof.decode("ascii").splitlines(), 1):
        fields = raw.split()
        deletion = fields[0] == "d"
        if deletion:
            fields = fields[1:]
        assert fields and fields[-1] == "0", (number, raw)
        # DRAT treats a clause as a set; literal order in deletion lines need
        # not match either the original DIMACS order or an addition line.
        clause = tuple(sorted(map(int, fields[:-1])))
        assert all(1 <= abs(literal) <= 51 for literal in clause)
        if deletion:
            database.delete(clause)
            deletions += 1
        else:
            database.add_rup(clause)
            additions += 1
            last_added = clause
    assert last_added == ()
    assert (additions, deletions) == (172, 232)
    return additions, deletions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("proof", type=Path)
    args = parser.parse_args()
    rup_self_test()
    forced_set_classification()
    clauses, digest = formula()
    additions, deletions = check_proof(clauses, args.proof)
    print(
        "PASS solutions=20 line_triples=1 edge_orbits=51 "
        f"clauses={len(clauses)} cnf_sha256={digest} "
        f"rup_additions={additions} deletions={deletions} final_empty=true"
    )


if __name__ == "__main__":
    main()
