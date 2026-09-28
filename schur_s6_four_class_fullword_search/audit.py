"""Independent semantic multiset audit for four-class Schur-trade CNFs."""
import argparse
import hashlib
from collections import Counter
from itertools import combinations
from pathlib import Path

SEED_HASH = "58c26704225562a6cde8346f0febe1e09f5604c18f9ec0397e8bf16b3e3497b3"
N = 537


def check(seed, fixed, cnf):
    source = Path(seed).read_bytes()
    assert hashlib.sha256(source).hexdigest() == SEED_HASH
    digits = source.decode("ascii").strip()
    assert len(digits) == N and set(digits) == set("123456")
    old = [0] + list(map(int, digits))
    fixed = set(fixed)
    assert len(fixed) == 2 and 4 not in fixed
    free = [v for v in range(1, N + 1) if old[v] not in fixed]
    free_set = set(free)
    fixed_sets = {d: {v for v in range(1, N + 1) if old[v] == d}
                  for d in fixed}
    triples = []
    defects = []
    blocked = {d: set() for d in fixed}
    for x in range(1, N + 1):
        for y in range(x, N + 1 - x):
            z = x + y
            vertices = set((x, y, z))
            triples.append((x, y, z))
            if old[x] == old[y] == old[z]:
                defects.append((x, y, z))
            for d, B in fixed_sets.items():
                for v in vertices & free_set:
                    if vertices - {v} <= B:
                        blocked[d].add(v)
    assert len(triples) == 72092
    assert defects == [(12, 12, 24), (12, 24, 36)]
    palette = sorted(set(range(1, 7)) - fixed)
    domains = [set() for _ in range(N + 1)]
    for v in range(1, N + 1):
        if v in free_set:
            domains[v] = set(palette) | {d for d in fixed if v not in blocked[d]}
        else:
            domains[v] = {old[v]}
    variable = {}
    for v in free:
        for d in sorted(domains[v]):
            variable[v, d] = len(variable) + 1
    expected = Counter()
    for v in free:
        positive = tuple(variable[v, d] for d in sorted(domains[v]))
        expected[positive] += 1
        for a, b in combinations(positive, 2):
            expected[(-a, -b)] += 1
    for i, v in enumerate(free):
        for j in range(1, 4):
            clause = tuple([-variable[v, palette[j]]]
                           + [variable[u, palette[j - 1]] for u in free[:i]])
            expected[clause] += 1
    schur_count = 0
    for x, y, z in triples:
        vertices = sorted({x, y, z})
        possible = set.intersection(*(domains[v] for v in vertices))
        for d in sorted(possible):
            clause = tuple(-variable[v, d] for v in vertices if v in free_set)
            assert clause
            expected[clause] += 1
            schur_count += 1
    actual = Counter()
    with Path(cnf).open(encoding="ascii") as stream:
        header = stream.readline().split()
        assert header == ["p", "cnf", str(len(variable)), str(sum(expected.values()))]
        for line in stream:
            parsed = tuple(map(int, line.split()))
            assert parsed and parsed[-1] == 0
            clause = parsed[:-1]
            assert all(1 <= abs(lit) <= len(variable) for lit in clause)
            actual[clause] += 1
    assert actual == expected, (sum((expected - actual).values()),
                                sum((actual - expected).values()))
    print(f"PASS fixed={''.join(map(str, sorted(fixed)))} "
          f"free={len(free)} variables={len(variable)} "
          f"clauses={sum(actual.values())} schur_clauses={schur_count} "
          "triples=72092 defects=2 exact_clause_multiset=yes", flush=True)
    return [(v, d) for v in free for d in sorted(fixed) if v not in blocked[d]]


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--seed", type=Path, required=True)
    p.add_argument("--fixed", type=str, required=True)
    p.add_argument("--cnf", type=Path, required=True)
    a = p.parse_args()
    check(a.seed, tuple(map(int, a.fixed)), a.cnf)
