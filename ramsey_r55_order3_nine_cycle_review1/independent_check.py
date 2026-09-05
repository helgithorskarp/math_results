#!/usr/bin/env python3
"""Reviewer-owned semantic audit for the order-three nine-cycle obstruction.

This program imports no code from the reviewed package.  It constructs the
order-three edge orbits directly, projects every 5-subset, and compares the
resulting primary-variable clauses (including the proved normalizations) with
the regenerated full formulas.  It also independently checks the local
arithmetic and the 27-vertex positive fixture.  With --drat-trim it replays
each general DRAT certificate against the formula whose semantics were audited.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import re
import struct
import subprocess
from pathlib import Path


PRIMARY_VARIABLES = 372
CASES = {
    0: (8490, 609409, 545784, 24631263,
        "19a93bc6f17d64cdd5e2c84a9180d3b8c704cd4ea48ce8b7214b3aeb5db44163",
        12162845, "b5c87eeb263154427baa35afbaaea2ccd04d95e4b5b48c876abbee5030c9524a"),
    1: (8514, 612097, 548280, 24774713,
        "fa3c17c653379ac46b576230bff4b8ecf3bd9bd106fd10edb60c7b49b41bdd9b",
        15794263, "307c4dcca2cd912629957e9489a5650997d45bd6f5bd829c60a65636f0e16e84"),
    2: (8532, 614113, 550152, 24899652,
        "a6e33c756d24824f5d10263fc4fe811f5f54e97f2152cfcd91fc805097a64a4a",
        17349019, "d519f421acdeea76aca8542f4634a83b9b00891437770b2f9ef967b84330aed7"),
    3: (8544, 615457, 551400, 25003667,
        "fe024e749043ea7f605d6dc37d6d1d599f131da3ea76b1b5196f6637626b965a",
        16312980, "1d220239a1c24410f7686fbdb9b14ca7f1ca5a434257e886f876301ec5258165"),
    4: (8550, 616129, 552024, 25086759,
        "21a39248ace49248bbb16171b757f4488b1dae7918192aad04ef036e6ac3f17b",
        20367008, "b03f122c0f3468700e89de12e193928f25eae701a4d5aec2077732e6d8547965"),
}
FIXTURE_SHA256 = "3acac6e84e1a9fdce9a2225d71568877cb352220ffdd1f4f6f050d070e32d659"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1 << 20):
            digest.update(block)
    return digest.hexdigest()


def advance(vertex: int) -> int:
    return 3 * (vertex // 3) + (vertex + 1) % 3 if vertex < 27 else vertex


def orbit_representative(a: int, b: int) -> tuple[int, int]:
    images = []
    for _ in range(3):
        images.append(tuple(sorted((a, b))))
        a, b = advance(a), advance(b)
    return min(images)


def orbit_labels() -> tuple[dict[tuple[int, int], int], dict[tuple[int, int], list[tuple[int, int]]]]:
    groups: dict[tuple[int, int], list[tuple[int, int]]] = {}
    for a, b in itertools.combinations(range(43), 2):
        groups.setdefault(orbit_representative(a, b), []).append((a, b))
    require(len(groups) == 381, "edge-orbit count")
    require(sum(map(len, groups.values())) == 903, "unordered-pair coverage")
    for representative, orbit in groups.items():
        require(len(orbit) == (1 if representative[0] >= 27 else 3),
                "edge-orbit length")

    internal = [rep for rep in groups if rep[1] < 27 and rep[0] // 3 == rep[1] // 3]
    cross = sorted(rep for rep in groups if rep[1] < 27 and rep[0] // 3 != rep[1] // 3)
    fixed = sorted(rep for rep in groups if rep[0] >= 27)
    links = sorted((rep for rep in groups if rep[0] < 27 <= rep[1]),
                   key=lambda rep: (rep[1], rep[0]))
    require((len(internal), len(cross), len(fixed), len(links)) == (9, 108, 120, 144),
            "edge-orbit categories")
    labels = {rep: index for index, rep in enumerate(cross + fixed + links, 1)}
    require(set(labels.values()) == set(range(1, PRIMARY_VARIABLES + 1)),
            "primary variable labels")
    return labels, groups


def edge_table(labels: dict[tuple[int, int], int], red_cycles: int) -> list[list[int]]:
    # Positive integers are variables; -1 and 0 are constant red and blue.
    edges = [[0] * 43 for _ in range(43)]
    for a, b in itertools.combinations(range(43), 2):
        representative = orbit_representative(a, b)
        if b < 27 and a // 3 == b // 3:
            token = -1 if a // 3 < red_cycles else 0
        else:
            token = labels[representative]
        edges[a][b] = edges[b][a] = token
    return edges


def canonical(literals: list[int]) -> tuple[int, ...] | None:
    values = set(literals)
    if any(-literal in values for literal in values):
        return None
    return tuple(sorted(values))


def projected_clause(vertices: tuple[int, ...], red: bool,
                     edges: list[list[int]]) -> tuple[int, ...] | None:
    literals: list[int] = []
    for a, b in itertools.combinations(vertices, 2):
        token = edges[a][b]
        if token <= 0:
            if (token == -1) != red:
                return None
        else:
            literals.append(-token if red else token)
    return canonical(literals)


def primary_formula(red_cycles: int,
                    labels: dict[tuple[int, int], int]) -> tuple[set[tuple[int, ...]], int]:
    edges = edge_table(labels, red_cycles)
    clauses: set[tuple[int, ...]] = set()
    five_sets = 0
    for vertices in itertools.combinations(range(43), 5):
        five_sets += 1
        for red in (False, True):
            clause = projected_clause(vertices, red, edges)
            if clause is not None:
                clauses.add(clause)
    require(five_sets == 962598, "five-set coverage")
    ramsey_count = len(clauses)

    # Phases of cycles 1,...,8 sort their three-bit words against cycle 0.
    for cycle in range(1, 9):
        bits = [edges[0][3 * cycle + phase] for phase in range(3)]
        require(all(bit > 0 for bit in bits), "anchor variable")
        for row in ([-bits[1], bits[0]], [-bits[2], bits[1]]):
            clause = canonical(row)
            require(clause is not None, "anchor tautology")
            clauses.add(clause)

    # Sort the sixteen fixed vertices by their nine moving-incidence bits.
    for fixed in range(27, 42):
        left = [edges[3 * cycle][fixed] for cycle in range(9)]
        right = [edges[3 * cycle][fixed + 1] for cycle in range(9)]
        for position in range(9):
            for prefix in itertools.product((0, 1), repeat=position):
                row: list[int] = []
                for index, value in enumerate(prefix):
                    row.extend((-left[index], -right[index]) if value
                               else (left[index], right[index]))
                row.extend((-left[position], right[position]))
                clause = canonical(row)
                require(clause is not None, "lexicographic tautology")
                clauses.add(clause)
    return clauses, ramsey_count


def update_clause_hash(digest: "hashlib._Hash", clause: tuple[int, ...]) -> None:
    digest.update(struct.pack(">I", len(clause)))
    for literal in clause:
        digest.update(struct.pack(">i", literal))


def parse_clause(line: str, variables: int) -> tuple[int, ...]:
    values = tuple(map(int, line.split()))
    require(values and values[-1] == 0 and 0 not in values[:-1], "DIMACS syntax")
    clause = values[:-1]
    require(all(1 <= abs(literal) <= variables for literal in clause), "literal range")
    require(len(set(clause)) == len(clause), "duplicate literal")
    require(not any(-literal in clause for literal in clause), "tautological clause")
    require(tuple(sorted(clause)) == clause, "noncanonical clause")
    return clause


def audit_formula(path: Path, variables: int, clause_count: int,
                  expected_primary: set[tuple[int, ...]]) -> tuple[int, str]:
    actual_digest = hashlib.sha256()
    actual_count = 0
    previous = None
    seen = 0
    with path.open() as stream:
        header = next(stream).split()
        require(header[:2] == ["p", "cnf"] and len(header) == 4, "DIMACS header")
        require(tuple(map(int, header[2:])) == (variables, clause_count), "header values")
        for line in stream:
            clause = parse_clause(line, variables)
            key = (len(clause), clause)
            require(previous is None or previous < key, "clause stream ordering")
            previous = key
            seen += 1
            if all(abs(literal) <= PRIMARY_VARIABLES for literal in clause):
                update_clause_hash(actual_digest, clause)
                actual_count += 1
    require(seen == clause_count, "clause line count")

    expected_digest = hashlib.sha256()
    for clause in sorted(expected_primary, key=lambda row: (len(row), row)):
        update_clause_hash(expected_digest, clause)
    require(actual_count == len(expected_primary), "primary clause count")
    require(actual_digest.digest() == expected_digest.digest(), "primary semantic mismatch")
    return actual_count, actual_digest.hexdigest()


def analytic_audit() -> None:
    feasible = 0
    by_complete = {0: 0, 1: 0}
    budget_only_false = 0
    for weights in itertools.product(range(4), repeat=8):
        complete = weights.count(3)
        deficit = sum(2 - weight + 3 * (weight == 3) for weight in weights)
        allowed = [fixed for fixed in range(17)
                   if fixed + 3 * complete <= 4
                   and 18 <= 2 + fixed + sum(weights) <= 24]
        require(bool(allowed) == (deficit <= 4 and complete <= 1),
                "local feasibility equivalence")
        if deficit <= 4 and not allowed:
            budget_only_false += 1
            require(complete == 2 and sorted(weights) == [2] * 6 + [3] * 2,
                    "shape of budget-only false profile")
        feasible += len(allowed)
        if complete <= 1:
            by_complete[complete] += len(allowed)
    require((feasible, by_complete, budget_only_false) ==
            (987, {0: 635, 1: 352}, 28), "local profile totals")

    require({min(mask.bit_count(), 9 - mask.bit_count()) for mask in range(512)}
            == set(range(5)), "internal-color cases")
    canonical_words = {(0, 0, 0), (1, 0, 0), (1, 1, 0), (1, 1, 1)}
    for word in itertools.product((0, 1), repeat=3):
        require(any(word[offset:] + word[:offset] in canonical_words for offset in range(3)),
                "anchor phase coverage")

    # Exhaust a four-coordinate instance of the exact fixed-row ordering schema.
    lex_clauses = []
    for position in range(4):
        for prefix in itertools.product((0, 1), repeat=position):
            row = []
            for index, value in enumerate(prefix):
                row.extend((-(index + 1), -(index + 5)) if value
                           else (index + 1, index + 5))
            lex_clauses.append(tuple(row + [-(position + 1), position + 5]))
    for values in itertools.product((False, True), repeat=8):
        satisfied = all(any(values[abs(literal) - 1] == (literal > 0)
                            for literal in clause) for clause in lex_clauses)
        require(satisfied == (values[:4] <= values[4:]), "lexicographic schema")
    print("PASS analytic reduction: profiles=987 complete0=635 complete1=352 budget_only_false=28")
    print("PASS normalizations: internal_cases=5 anchor_words=8 lex_schema_assignments=256")


def fixture_audit(path: Path) -> None:
    require(sha256(path) == FIXTURE_SHA256, "fixture hash")
    rows = path.read_text().splitlines()
    require(rows[0] == "27 177", "fixture header")
    red = {tuple(map(int, row.split())) for row in rows[1:]}
    require(len(red) == 177 and all(0 <= a < b < 27 for a, b in red), "fixture edges")
    rotate = lambda vertex: 3 * (vertex // 3) + (vertex + 1) % 3
    require({tuple(sorted((rotate(a), rotate(b)))) for a, b in red} == red,
            "fixture rotation")
    for vertices in itertools.combinations(range(27), 5):
        colors = {tuple(sorted(pair)) in red for pair in itertools.combinations(vertices, 2)}
        require(len(colors) == 2, "fixture monochromatic five-set")
    for cycle in range(9):
        own_red = cycle < 4
        internal = list(itertools.combinations(range(3 * cycle, 3 * cycle + 3), 2))
        require(all((pair in red) == own_red for pair in internal), "fixture internal color")
        weights = []
        for other in range(9):
            if other != cycle:
                weights.append(sum(((tuple(sorted((3 * cycle, vertex))) in red) == own_red)
                                   for vertex in range(3 * other, 3 * other + 3)))
        require(sum(2 - weight + 3 * (weight == 3) for weight in weights) <= 4,
                "fixture deficit")
        require(weights.count(3) <= 1, "fixture complete-block cap")
    print("PASS positive control: vertices=27 red_edges=177 five_sets=80730")


def external_replay(binary: Path, formula: Path, proof: Path, red_cycles: int) -> None:
    process = subprocess.run([str(binary), str(formula), str(proof)], text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    output = process.stdout.replace("\r", "\n")
    require(process.returncode == 0 and "s VERIFIED" in output, "external DRAT replay")
    rats = re.search(r"(\d+) RAT lemmas in core", output)
    require(rats, "DRAT replay summary")
    print(f"PASS external DRAT r={red_cycles}: RAT_core_lemmas={rats.group(1)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True)
    parser.add_argument("--drat-trim", type=Path)
    args = parser.parse_args()
    target, work = args.target.resolve(), args.work.resolve()

    analytic_audit()
    labels, groups = orbit_labels()
    print(f"PASS actual edge orbits: pairs=903 orbits={len(groups)} primary={len(labels)}")
    fixture_audit(target / "moving27.edges")

    for red_cycles, expected in CASES.items():
        variables, clauses, expected_ramsey, formula_bytes, formula_hash, proof_bytes, proof_hash = expected
        formula, proof = work / f"full_r{red_cycles}.cnf", work / f"full_r{red_cycles}.drat"
        require(formula.stat().st_size == formula_bytes and sha256(formula) == formula_hash,
                "full formula bytes/hash")
        require(proof.stat().st_size == proof_bytes and sha256(proof) == proof_hash,
                "proof bytes/hash")
        expected_primary, ramsey_count = primary_formula(red_cycles, labels)
        require(ramsey_count == expected_ramsey, "Ramsey clause count")
        primary_count, primary_hash = audit_formula(
            formula, variables, clauses, expected_primary)
        print(f"PASS semantic CNF r={red_cycles}: five_sets=962598 ramsey={ramsey_count} "
              f"primary={primary_count} sha256={primary_hash}")
        if args.drat_trim:
            external_replay(args.drat_trim.resolve(), formula, proof, red_cycles)

    if args.drat_trim:
        print(f"DRAT_TRIM sha256={sha256(args.drat_trim.resolve())}")
    print("PASS: independently verified exclusion of order-three type 1^16 3^9")
    print("SCOPE: minimum ten additionally imports the previously reviewed exclusions for 1..8 cycles")


if __name__ == "__main__":
    main()
