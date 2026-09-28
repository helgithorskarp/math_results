"""Exact CNF for a four-class trade of the public 537-word.

Fix two old classes; recolour all other entries arbitrarily. Necessary
single-insertion domains for fixed output colours and sound free-palette
first-appearance symmetry reduce the full CNF without restricting models.
"""
import argparse
import hashlib
from itertools import combinations
from pathlib import Path

N = 537
SOURCE_HASH = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"


def make(seed, fixed):
    data = Path(seed).read_bytes()
    assert hashlib.sha256(data).hexdigest() == SOURCE_HASH
    word = data.decode("ascii").strip()
    assert len(word) == N and set(word) == set("123456")
    old = [0] + list(map(int, word))
    assert fixed[0] < fixed[1] and all(x in (1, 2, 3, 5, 6) for x in fixed)
    free_labels = tuple(c for c in range(1, 7) if c not in fixed)
    free = [v for v in range(1, N + 1) if old[v] not in fixed]
    free_set = set(free)
    domains = [set() for _ in range(N + 1)]
    for v in range(1, N + 1):
        domains[v] = set(free_labels) if v in free_set else {old[v]}
    for colour in fixed:
        B = {v for v in range(1, N + 1) if old[v] == colour}
        blocked = {x + y for x in B for y in B if x + y <= N}
        blocked.update(abs(x - y) for x in B for y in B)
        blocked.update(x // 2 for x in B if x % 2 == 0)
        assert not B & blocked
        for v in free:
            if v not in blocked:
                domains[v].add(colour)
    variables = {}
    for v in free:
        for colour in sorted(domains[v]):
            variables[v, colour] = len(variables) + 1
    clauses = []
    for v in free:
        choices = [variables[v, c] for c in sorted(domains[v])]
        clauses.append(choices)
        clauses.extend([-a, -b] for a, b in combinations(choices, 2))
    # Permute free output colours by first appearance on free vertices.
    for i, v in enumerate(free):
        for j in range(1, len(free_labels)):
            clauses.append([-variables[v, free_labels[j]]]
                           + [variables[u, free_labels[j - 1]] for u in free[:i]])
    triples = 0
    schur_clauses = 0
    for z in range(2, N + 1):
        for x in range(1, z // 2 + 1):
            y = z - x
            triples += 1
            vertices = sorted({x, y, z})
            common = set.intersection(*(domains[v] for v in vertices))
            for colour in sorted(common):
                clause = [-variables[v, colour] for v in vertices if v in free_set]
                assert clause
                clauses.append(clause)
                schur_clauses += 1
    assert triples == 72092
    return old, free, domains, variables, clauses, schur_clauses


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=Path, required=True)
    parser.add_argument("--fixed", type=str, required=True)
    parser.add_argument("--cnf", type=Path, required=True)
    args = parser.parse_args()
    assert len(args.fixed) == 2 and args.fixed.isdigit()
    fixed = tuple(map(int, args.fixed))
    old, free, domains, variables, clauses, schur_clauses = make(args.seed, fixed)
    with args.cnf.open("w", encoding="ascii", newline="\n") as out:
        out.write(f"p cnf {len(variables)} {len(clauses)}\n")
        for clause in clauses:
            out.write(" ".join(map(str, clause)) + " 0\n")
    print(f"fixed={args.fixed} free_vertices={len(free)} variables={len(variables)} "
          f"clauses={len(clauses)} schur_clauses={schur_clauses} "
          f"extra_fixed_colour_options={sum(len(domains[v])-4 for v in free)}",
          flush=True)


if __name__ == "__main__":
    main()
