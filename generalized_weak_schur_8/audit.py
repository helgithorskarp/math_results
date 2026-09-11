#!/usr/bin/env python3
"""Audit every input clause by its arithmetic meaning, without importing encode.

This checks soundness: every avoiding coloring extends to a model of every
accepted clause. It intentionally permits omissions and duplicate valid clauses;
these cannot create a false UNSAT upper bound. See the proof in README.md.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path


def symbols(n, k, r):
    meaning = [None] * (n + 1)
    for color in (0, 1):
        for prefix in range(1, r + 1):
            for count in range(1, min(k, prefix) + 1):
                low = sum(range(1, count + 1))
                high = min(n, sum(range(prefix - count + 1, prefix + 1)))
                for total in range(low, high + 1):
                    meaning.append((color, prefix, count, total))
    return meaning


def require(condition, message):
    if not condition:
        raise ValueError(message)


def clause_kind(clause, meaning, n, k, r):
    require(len(clause) in (2, 3), 'invalid clause length')
    require(all(0 < abs(lit) < len(meaning) for lit in clause), 'invalid variable')
    # A positive auxiliary head means a valid subset-sum implication.
    if clause[-1] > n:
        color, prefix, count, total = meaning[clause[-1]]
        not_color = -prefix if color else prefix
        if len(clause) == 2 and abs(clause[0]) <= n:
            require(clause[0] == not_color and count == 1 and total == prefix,
                    'invalid singleton implication')
            return 'singleton'
        require(clause[0] < -n, 'missing negative auxiliary antecedent')
        antecedent = meaning[-clause[0]]
        if len(clause) == 2:
            require(antecedent == (color, prefix - 1, count, total),
                    'invalid carry implication')
            return 'carry'
        require(clause[1] == not_color and
                antecedent == (color, prefix - 1, count - 1, total - prefix),
                'invalid distinct-element extension')
        return 'extend'
    require(clause[0] < -n, 'missing reachable-sum antecedent')
    color, prefix, count, total = meaning[-clause[0]]
    require(prefix == r, 'forbidden-sum clause uses wrong prefix')
    if len(clause) == 2:
        require(count == k and clause[1] == (-total if color else total),
                'invalid all-prefix forbidden sum')
        return 'forbid_prefix'
    x, y = abs(clause[1]), abs(clause[2])
    require(count == k - 1 and r < x < y <= n and y == x + total and
            clause[1] == (-x if color else x) and
            clause[2] == (-y if color else y), 'invalid tail forbidden sum')
    return 'forbid_tail'


def audit(path, n, k, r):
    meaning = symbols(n, k, r)
    counts = collections.Counter()
    with path.open() as stream:
        header = stream.readline().split()
        require(header[:2] == ['p', 'cnf'] and len(header) == 4, 'bad header')
        require(int(header[2]) == len(meaning) - 1, 'wrong variable count')
        for line_number, line in enumerate(stream, 2):
            row = list(map(int, line.split()))
            require(row and row[-1] == 0 and 0 not in row[:-1],
                    f'bad clause terminator on line {line_number}')
            try:
                counts[clause_kind(row[:-1], meaning, n, k, r)] += 1
            except ValueError as error:
                raise ValueError(f'line {line_number}: {error}') from error
        require(sum(counts.values()) == int(header[3]), 'wrong clause count')
    return {'status': 'ALL_CLAUSES_ARITHMETICALLY_SOUND', 'n': n, 'k': k, 'r': r,
            'variables': len(meaning) - 1, 'clauses': sum(counts.values()),
            'clause_kinds': dict(sorted(counts.items())),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf', type=Path)
    parser.add_argument('--n', type=int, default=365)
    parser.add_argument('--k', type=int, default=8)
    parser.add_argument('--r', type=int, default=171)
    args = parser.parse_args()
    print(json.dumps(audit(args.cnf, args.n, args.k, args.r), indent=2))
