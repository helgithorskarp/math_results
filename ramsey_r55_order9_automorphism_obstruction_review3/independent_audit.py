#!/usr/bin/env python3
"""Independent finite audit of the order-nine reduction and residual CNFs.

This file deliberately imports no code from the reviewed artifact.  It rebuilds
pair orbits, Ramsey clauses, and centralizer-normalization clauses directly.
It hashes the resulting DIMACS stream without retaining the roughly 20 MB
formulas in the repository.
"""

from __future__ import annotations

import hashlib
import itertools
import random


ORDER = 43
CASES = ((3, 5, 1), (4, 2, 1))
EXPECTED = {
    (3, 5, 1): (127, 210206, 1168, 211374,
                "263cb16b9558d9af6d45eef0195d9c224f64c4b9652fd2b28189fb70b439293d"),
    (4, 2, 1): (105, 211062, 1725, 212787,
                "cf358aadde89b8bed4943d11ae6419f7e824dcfe67ebad2f8d2598e13e1e4fbc"),
}


def cycles(case: tuple[int, int, int]) -> list[tuple[int, ...]]:
    answer = []
    first = 0
    for length, count in zip((9, 3, 1), case, strict=True):
        for _ in range(count):
            answer.append(tuple(range(first, first + length)))
            first += length
    assert first == ORDER
    return answer


def orbit_map(case: tuple[int, int, int]):
    successor = list(range(ORDER))
    for cycle in cycles(case):
        for index, vertex in enumerate(cycle):
            successor[vertex] = cycle[(index + 1) % len(cycle)]

    def representative(pair: tuple[int, int]) -> tuple[int, int]:
        u, v = pair
        images = []
        for _ in range(9):
            images.append((min(u, v), max(u, v)))
            u, v = successor[u], successor[v]
        return min(images)

    pairs = list(itertools.combinations(range(ORDER), 2))
    representatives = sorted({representative(pair) for pair in pairs})
    number = {pair: index + 1 for index, pair in enumerate(representatives)}
    mapping = {pair: number[representative(pair)] for pair in pairs}
    return mapping, successor


def blocking_clause(variables, values):
    # Preserve semantic variable order, as DIMACS permits; the reviewed
    # generator does likewise, so the final byte digest is also comparable.
    return tuple(-var if value else var
                 for var, value in zip(variables, values, strict=True))


def build(case: tuple[int, int, int]):
    mapping, successor = orbit_map(case)
    base = set()
    for vertices in itertools.combinations(range(ORDER), 5):
        variables = sorted({mapping[tuple(sorted(pair))]
                            for pair in itertools.combinations(vertices, 2)})
        base.add(tuple(variables))
        base.add(tuple(-variable for variable in reversed(variables)))

    groups = cycles(case)
    nines = [group for group in groups if len(group) == 9]
    threes = [group for group in groups if len(group) == 3]
    symmetry = set()
    for family, width in ((nines, 4), (threes, 1)):
        profiles = [[mapping[tuple(sorted((group[0], group[offset])))]
                     for offset in range(1, width + 1)] for group in family]
        values = list(itertools.product((0, 1), repeat=width))
        for left, right in zip(profiles, profiles[1:]):
            for a in values:
                for b in values:
                    if a > b:
                        symmetry.add(blocking_clause(left + right, a + b))

    anchor = nines[0][0]
    for group in nines[1:] + threes:
        word_variables = [mapping[tuple(sorted((anchor, vertex)))] for vertex in group]
        assert len(set(word_variables)) == len(group)
        for word in itertools.product((0, 1), repeat=len(group)):
            least = min(word[shift:] + word[:shift] for shift in range(len(group)))
            if word != least:
                symmetry.add(blocking_clause(word_variables, word))

    formula = sorted(base | symmetry, key=lambda clause: (len(clause), clause))
    digest = hashlib.sha256()
    digest.update(f"p cnf {len(set(mapping.values()))} {len(formula)}\n".encode("ascii"))
    for clause in formula:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return mapping, successor, symmetry, len(base), len(formula), digest.hexdigest()


def check_constructive_normalization(case, mapping, successor, symmetry):
    groups = cycles(case)
    rng = random.Random(0x90543 + sum(case))
    variable_count = len(set(mapping.values()))
    trials = [[0] * (variable_count + 1), [1] * (variable_count + 1)]
    trials += [[0] + [rng.randrange(2) for _ in range(variable_count)]
               for _ in range(40)]
    for assignment in trials:
        def color(u, v):
            return assignment[mapping[min(u, v), max(u, v)]]

        def profile(group):
            return tuple(color(group[0], group[d])
                         for d in range(1, (len(group) + 1) // 2))

        # Relabeling maps a new label to its old label.
        permutation = list(range(ORDER))
        for length in (9, 3):
            slots = [group for group in groups if len(group) == length]
            for slot, old in zip(slots, sorted(slots, key=profile), strict=True):
                for new_vertex, old_vertex in zip(slot, old, strict=True):
                    permutation[new_vertex] = old_vertex
        for group in groups:
            if group[0] == 0 or len(group) == 1:
                continue
            old = [permutation[vertex] for vertex in group]
            shift = min(range(len(group)), key=lambda amount: tuple(
                color(permutation[0], old[(j + amount) % len(group)])
                for j in range(len(group))))
            for j, vertex in enumerate(group):
                permutation[vertex] = old[(j + shift) % len(group)]

        assert sorted(permutation) == list(range(ORDER))
        assert all(permutation[successor[v]] == successor[permutation[v]]
                   for v in range(ORDER))
        relabeled = {}
        for (u, v), variable in mapping.items():
            value = color(permutation[u], permutation[v])
            assert variable not in relabeled or relabeled[variable] == value
            relabeled[variable] = value
        assert all(any(relabeled[abs(literal)] == (literal > 0)
                       for literal in clause) for clause in symmetry)
    return len(trials)


def main():
    surviving = {(a, b, ORDER - 9 * a - 3 * b)
                 for a in range(1, 5) for b in range(15)
                 if 9 * a + 3 * b <= ORDER and 3 * a >= 7}
    imported = {(3, b, 16 - 3 * b) for b in range(5)} | {(4, 0, 7), (4, 1, 4)}
    assert surviving == imported | set(CASES)
    print("cycle_types=9 imported=7 residual=2")
    for case in CASES:
        mapping, successor, symmetry, base, total, digest = build(case)
        variables = len(set(mapping.values()))
        observed = (variables, base, len(symmetry), total, digest)
        assert observed == EXPECTED[case], (case, observed)
        trials = check_constructive_normalization(
            case, mapping, successor, symmetry)
        print(f"case={case} variables={variables} base={base} "
              f"symmetry={len(symmetry)} total={total} sha256={digest} "
              f"normalization_trials={trials}")
    print("independent_order9_audit=true")


if __name__ == "__main__":
    main()
