#!/usr/bin/env python3
"""Independent orbit reconstruction, elementary RUP replay, and fixture audit.

Imports neither the modular-difference generator nor the C++ enumerator.
RUP keeps all proved clauses; deletion instructions are unnecessary because
retaining valid clauses only strengthens unit propagation.
"""
from itertools import combinations, product
from pathlib import Path
import argparse
import hashlib

HERE = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def rebuild():
    pairs = list(combinations(range(21), 2))

    def advance(v):
        block = v // 3
        return 3*block + (v+1) % 3

    representative = {}
    for a, b in pairs:
        images = []
        for _ in range(3):
            images.append(tuple(sorted((a, b))))
            a, b = advance(a), advance(b)
        representative[images[0]] = min(images)
    orbits = {}
    for pair, rep in representative.items():
        orbits.setdefault(rep, []).append(pair)
    require(len(orbits) == 70 and all(len(es) == 3 for es in orbits.values()),
            "incorrect 21-vertex edge orbits")
    free = sorted(rep for rep in orbits
                  if rep[0] // 3 != rep[1] // 3 and rep[0] // 3 != 0)
    require(len(free) == 45, "incorrect free-orbit count")
    label = {rep: i+1 for i, rep in enumerate(free)}
    true = 1000
    for a, b in orbits:
        if a // 3 == b // 3:
            label[(a, b)] = -true
        elif a // 3 == 0:
            label[(a, b)] = true if a % 3 == b % 3 else -true
    edge_labels = {pair: label[rep] for pair, rep in representative.items()}
    groups = {}
    for rep in free:
        groups.setdefault((rep[0] // 3, rep[1] // 3), []).append(label[rep])
    formula = set()
    for group in groups.values():
        require(len(group) == 3, "matching-choice group size")
        formula.add(tuple(sorted(group)))
        for a, b in combinations(group, 2):
            formula.add(tuple(sorted((-a, -b))))
    count = 0
    for vertices in combinations(range(21), 5):
        count += 1
        for color in (0, 1):
            clause, tautology = set(), False
            for pair in combinations(vertices, 2):
                lit = edge_labels[pair] * (-1 if color else 1)
                if lit == true:
                    tautology = True
                elif lit != -true:
                    clause.add(lit)
            if not tautology:
                formula.add(tuple(sorted(clause)))
    require(count == 20349, "five-set coverage")
    clauses = sorted(formula, key=lambda c: (len(c), c))
    text = f"p cnf 45 {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return clauses, text


def unit_conflict(formula, assumptions):
    assignment = {}
    for lit in assumptions:
        variable, value = abs(lit), lit > 0
        if variable in assignment and assignment[variable] != value:
            return True
        assignment[variable] = value
    while True:
        changed = False
        for clause in formula:
            pending, satisfied = [], False
            for lit in clause:
                if abs(lit) not in assignment:
                    pending.append(lit)
                elif assignment[abs(lit)] == (lit > 0):
                    satisfied = True
                    break
            if satisfied:
                continue
            if not pending:
                return True
            if len(pending) == 1:
                lit = pending[0]
                assignment[abs(lit)] = lit > 0
                changed = True
        if not changed:
            return False


def replay(base, certificate):
    formula = list(base)
    require(certificate and certificate[-1] == (), "certificate must end in the empty clause")
    for index, clause in enumerate(certificate, 1):
        require(all(1 <= abs(lit) <= 45 for lit in clause), "literal outside range")
        require(len(set(clause)) == len(clause), "duplicate proof literal")
        require(unit_conflict(formula, [-lit for lit in clause]), f"non-RUP clause {index}")
        formula.append(clause)
    return len(certificate)


def audit_fixture(path):
    lines = path.read_text().splitlines()
    require(lines[0] == "18 45", "fixture header")
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    require(len(edges) == len(set(edges)) == 45, "fixture edge count")
    require(all(0 <= a < b < 18 for a, b in edges), "fixture edge endpoint")
    blue = set(edges)
    for vertices in combinations(range(18), 5):
        colors = {pair in blue for pair in combinations(vertices, 2)}
        require(len(colors) == 2, "fixture has a monochromatic five-set")
    for block in range(6):
        require(all(pair not in blue for pair in combinations(range(3*block, 3*block+3), 2)),
                "fixture fiber is not independent")
    for a, b in combinations(range(6), 2):
        for vertex in range(3*a, 3*a+3):
            require(sum((vertex, other) in blue for other in range(3*b, 3*b+3)) == 1,
                    "fixture lacks a matching")
        for vertex in range(3*b, 3*b+3):
            require(sum((other, vertex) in blue for other in range(3*a, 3*a+3)) == 1,
                    "fixture lacks a reverse matching")
    shift = [3*(v//3)+(v+1) % 3 for v in range(18)]
    require({tuple(sorted((shift[a], shift[b]))) for a, b in blue} == blue,
            "fixture is not cyclically invariant")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cnf", type=Path, required=True)
    args = parser.parse_args()
    clauses, expected = rebuild()
    require(args.cnf.read_bytes() == expected.encode("ascii"), "complete CNF mismatch")
    print(f"FORMULA_AUDIT variables=45 clauses={len(clauses)} edge_orbits=70 "
          f"five_sets=20349 sha256={hashlib.sha256(expected.encode()).hexdigest()}")
    certificate = []
    for line in (HERE / "certificate.rup").read_text().splitlines():
        tokens = tuple(map(int, line.split()))
        require(tokens and tokens[-1] == 0 and 0 not in tokens[:-1], "proof line syntax")
        certificate.append(tokens[:-1])
    additions = replay(clauses, certificate)
    for bad in ([(1,), ()], certificate[:-1], [(46,), ()]):
        try:
            replay(clauses, bad)
        except ValueError:
            pass
        else:
            raise ValueError("invalid proof was accepted")
    print(f"RUP_AUDIT additions={additions} invalid_proofs_rejected=3 PASS")
    survivors = []
    for a, weights in product(range(23), product(range(4), repeat=6)):
        full = weights.count(3)
        if a+3*full <= 4 and 18 <= 2+a+sum(weights) <= 24:
            survivors.append((a, weights))
    require(survivors == [(4, (2,)*6)], "equality-profile mismatch")
    print("EQUALITY_AUDIT tested=94208 survivors=1 fixed_neighbors=4 cross_weights=2,2,2,2,2,2 PASS")
    audit_fixture(HERE / "fixture18.edges")
    print("FIXTURE_AUDIT vertices=18 blue_edges=45 five_sets=8568 monochromatic=0 PASS")


if __name__ == "__main__":
    main()
