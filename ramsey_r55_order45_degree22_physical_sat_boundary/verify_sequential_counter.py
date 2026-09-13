#!/usr/bin/env python3
"""Exhaustively verify the Sinz at-most encoding used by the CNF generator."""

from itertools import product


def encoding(n, k):
    clauses = []
    if k == n:
        return clauses, n
    if k == 0:
        return [[-i] for i in range(1, n+1)], n
    next_var = n
    s = []
    for _ in range(n-1):
        row = []
        for _ in range(k):
            next_var += 1
            row.append(next_var)
        s.append(row)
    for i in range(n-1):
        clauses.append([-(i+1), s[i][0]])
    for i in range(1, n-1):
        clauses.append([-s[i-1][0], s[i][0]])
    for i in range(1, n-1):
        for j in range(1, k):
            clauses.append([-(i+1), -s[i-1][j-1], s[i][j]])
            clauses.append([-s[i-1][j], s[i][j]])
    for i in range(1, n):
        clauses.append([-(i+1), -s[i-1][k-1]])
    return clauses, next_var


def unit_conflict(clauses, fixed):
    values = dict(fixed)
    while True:
        changed = False
        for clause in clauses:
            if any(values.get(abs(x)) == (x > 0) for x in clause):
                continue
            unset = [x for x in clause if abs(x) not in values]
            if not unset:
                return True
            if len(unset) == 1:
                lit = unset[0]
                variable, value = abs(lit), lit > 0
                if variable in values and values[variable] != value:
                    return True
                if variable not in values:
                    values[variable] = value
                    changed = True
        if not changed:
            return False


if __name__ == "__main__":
    tests = 0
    for n in range(1, 11):
        for k in range(n+1):
            clauses, _ = encoding(n, k)
            for bits in product((False, True), repeat=n):
                conflict = unit_conflict(clauses, {i+1: bits[i] for i in range(n)})
                assert conflict == (sum(bits) > k), (n, k, bits, conflict)
                tests += 1
    print("SEQUENTIAL_COUNTER_EXHAUSTIVE_OK", "fixed_assignments", tests)
