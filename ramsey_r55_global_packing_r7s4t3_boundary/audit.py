#!/usr/bin/env python3
"""Independent literal audit of h3835 branch (7,4,3); imports no h3835 code."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


BRANCH = [7, 4, 3]
BLOCKS = []
offset = 0
for size in [4] * 7 + [3] * 5:
    BLOCKS.append(list(range(offset, offset + size)))
    offset += size
assert offset == 43

FIXED = {pair: 1 for block in BLOCKS for pair in combinations(block, 2)}
PAIRS = list(combinations(range(43), 2))
VARIABLES = {pair: k + 2 for k, pair in enumerate(p for p in PAIRS if p not in FIXED)}
assert len(FIXED) == 57 and len(VARIABLES) == 846


def root_clauses():
    root = BLOCKS[0]
    for block in BLOCKS[1:]:
        adjacent = [(j, j + 1) for j in range(len(block) - 1)]
        for a, b in adjacent:
            for left in range(16):
                for right in range(left + 1, 16):
                    clause = []
                    for position, value in ((a, left), (b, right)):
                        for row in range(4):
                            variable = VARIABLES[root[row], block[position]]
                            clause.append(-variable if (value >> row) & 1 else variable)
                    yield tuple(clause)


def five_clauses(q):
    edges = list(combinations(q, 2))
    # The source emits red first, then blue.
    for color in (1, 0):
        if any(FIXED[pair] != color for pair in edges if pair in FIXED):
            continue
        yield tuple((-1 if color else 1) * VARIABLES[pair]
                    for pair in edges if pair in VARIABLES)


def expected_clauses():
    yield (1,)
    yield from root_clauses()
    for q in combinations(range(43), 5):
        yield from five_clauses(q)


def audit(path):
    path = Path(path)
    digest = hashlib.sha256()
    histogram = {}
    expected = expected_clauses()
    with path.open('rb') as stream:
        header = stream.readline()
        digest.update(header)
        words = header.split()
        if words[:2] != [b'p', b'cnf'] or len(words) != 4:
            raise ValueError('DIMACS header')
        variables, declared = map(int, words[2:])
        if variables != 847:
            raise ValueError('variable count')
        count = 0
        for count, line in enumerate(stream, 1):
            digest.update(line)
            fields = list(map(int, line.split()))
            if not fields or fields[-1] != 0 or 0 in fields[:-1]:
                raise ValueError(f'clause syntax at {count}')
            clause = tuple(fields[:-1])
            if any(abs(x) > variables for x in clause):
                raise ValueError(f'literal range at {count}')
            try:
                wanted = next(expected)
            except StopIteration as exc:
                raise ValueError('additional clause') from exc
            if clause != wanted:
                raise ValueError(f'literal mismatch at clause {count}')
            histogram[len(clause)] = histogram.get(len(clause), 0) + 1
        try:
            next(expected)
        except StopIteration:
            pass
        else:
            raise ValueError('missing clause')
    if count != declared:
        raise ValueError('declared clause count')
    red = 962598
    root = 120 * (6 * 3 + 5 * 2)
    blue = declared - 1 - root - red
    result = {
        'status': 'INDEPENDENT_LITERAL_AUDIT_R7_S4_T3',
        'branch': BRANCH,
        'vertices': 43,
        'five_sets_checked': 962598,
        'fixed_red_edges': len(FIXED),
        'free_physical_edges': len(VARIABLES),
        'variables': variables,
        'clauses': declared,
        'constant_clauses': 1,
        'root_order_clauses': root,
        'red_target_clauses': red,
        'blue_target_clauses': blue,
        'clause_lengths': dict(sorted(histogram.items())),
        'bytes': path.stat().st_size,
        'sha256': digest.hexdigest(),
    }
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('cnf')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = audit(args.cnf)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(text)
    print(text, end='')
