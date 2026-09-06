#!/usr/bin/env python3
"""Direct primary-only Core194 equations, without inherited search encodings."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
WORD = '100110110110110100'
T = 321


def need(condition, message):
    if not condition:
        raise ValueError(message)


def identity(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as stream:
        while block := stream.read(1 << 20):
            h.update(block)
    return dict(bytes=Path(path).stat().st_size, sha256=h.hexdigest())


def variable(a, b):
    need(0 <= a < b < 43, 'physical pair')
    if b < 33:
        i, s = divmod(a, 3)
        j, t = divmod(b, 3)
        if i == j:
            return T if i < 4 else -T
        rank = i * (21-i) // 2 + j-i-1
        return 1 + 3*rank + (t-s) % 3
    if a >= 33:
        i, j = a-33, b-33
        return 166 + i*(19-i)//2 + j-i-1
    return 211 + 11*(b-33) + a//3


def units(color):
    need(color in ('blue', 'red'), 'pair color')
    rows = {}
    for k, (i, j) in enumerate(combinations(range(4), 2)):
        for d in range(3):
            rows[variable(3*i, 3*j+d)] = WORD[3*k+d] == '1'
    for f in (33, 34):
        for i in range(4):
            rows[variable(3*i, f)] = False
    rows[variable(33, 34)] = color == 'red'
    need(len(rows) == 27, '18 core, eight empty, one pair')
    return rows


def make(color):
    fixed = units(color)
    edge = {}
    for a, b in combinations(range(43), 2):
        x = variable(a, b)
        edge[a, b] = (T if fixed[x] else -T) if x in fixed else x
    constraints = set()
    counts = dict(all_five_sets=0, possible_red=0, possible_blue=0)
    for q in combinations(range(43), 5):
        counts['all_five_sets'] += 1
        literals = {edge[e] for e in combinations(q, 2)}
        if -T not in literals:
            constraints.add(tuple(sorted(-x for x in literals if x != T)))
            counts['possible_red'] += 1
        if T not in literals:
            constraints.add(tuple(sorted(x for x in literals if x != -T)))
            counts['possible_blue'] += 1
    counts['distinct_ramsey_clauses'] = len(constraints)
    constraints.update((x if value else -x,) for x, value in fixed.items())
    counts['fixed_units'] = len(fixed)
    before = len(constraints)
    if color == 'blue':
        constraints.update((variable(33, f), variable(34, f)) for f in range(35, 43))
    counts['new_pair_consequences'] = len(constraints)-before
    counts['variables'] = 320
    counts['clauses'] = len(constraints)
    need(counts['all_five_sets'] == 962598, 'complete five-set domain')
    return sorted(constraints), counts


def write(color, path):
    rows, report = make(color)
    with Path(path).open('w') as stream:
        stream.write(f'p cnf 320 {len(rows)}\n')
        for row in rows:
            stream.write(' '.join(map(str, row)) + (' ' if row else '') + '0\n')
    return dict(color=color, census=report, formula=identity(path))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--color', choices=('blue', 'red'), required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(write(args.color, args.output), indent=2, sort_keys=True))
