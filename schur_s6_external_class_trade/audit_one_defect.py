"""Directly audit the selector and counter semantics on small controls."""

import itertools
import random

from verify import N, load_seed
from verify_one_defect import encode


def direct_defects(word):
    count = 0
    for x in range(1, N + 1):
        for y in range(x, N + 1 - x):
            if word[x] == word[y] == word[x + y]:
                count += 1
    return count


def check_counter():
    # Independent truth-table audit of the Sinz clauses for up to five inputs.
    for n in range(1, 6):
        for selected in itertools.product((False, True), repeat=n):
            accepts = False
            for prefixes in itertools.product((False, True), repeat=n - 1):
                valid = True
                for i, t in enumerate(selected):
                    if i < n - 1 and t and not prefixes[i]:
                        valid = False
                    if i > 0 and t and prefixes[i - 1]:
                        valid = False
                    if 0 < i < n - 1 and prefixes[i - 1] and not prefixes[i]:
                        valid = False
                accepts |= valid
            assert accepts == (sum(selected) <= 1)


def check_actual_edges():
    old = load_seed()
    rng = random.Random(20260928)
    cases = 0
    for group in ({1, 2, 4}, {4, 5, 6}):
        clauses, free_count, active_count, _ = encode(old, group)
        free = [v for v in range(1, N + 1) if old[v] in group]
        assert len(free) == free_count
        # One-hot clauses precede edge clauses; counter clauses follow them.
        counter_count = 3 * active_count - 4
        edge_clauses = clauses[16 * free_count:len(clauses) - counter_count]
        for edits in range(11):
            word = old[:]
            for v in rng.sample(free, edits):
                word[v] = rng.choice([c for c in range(1, 7) if c != word[v]])
            forced = set()
            for clause in edge_clauses:
                selector = clause[0]
                if all(word[(-lit - 1) // 6 + 1] == (-lit - 1) % 6 + 1 for lit in clause[1:]):
                    forced.add(selector)
            assert len(forced) == direct_defects(word)
            cases += 1
    return cases


if __name__ == "__main__":
    check_counter()
    cases = check_actual_edges()
    print(f"PASS counter_truth_tables_n_le_5=yes actual_seed_assignments={cases}")
