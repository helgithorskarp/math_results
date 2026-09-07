#!/usr/bin/env python3
"""Independent literal audit of normalized branch (7,4,3); no target imports."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json


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
        for a, b in zip(range(len(block) - 1), range(1, len(block))):
            for left in range(16):
                for right in range(left + 1, 16):
                    clause = []
                    for position, value in ((a, left), (b, right)):
                        for row in range(4):
                            variable = VARIABLES[root[row], block[position]]
                            clause.append(-variable if (value >> row) & 1 else variable)
                    yield tuple(clause)


def physical_clauses():
    for vertices in combinations(range(43), 5):
        edges = list(combinations(vertices, 2))
        for color in (1, 0):
            if any(FIXED[pair] != color for pair in edges if pair in FIXED):
                continue
            yield tuple((-1 if color else 1) * VARIABLES[pair]
                        for pair in edges if pair in VARIABLES)


def signature_key(block_index):
    root = BLOCKS[0]
    return tuple(VARIABLES[root[row], vertex]
                 for vertex in BLOCKS[block_index]
                 for row in (3, 2, 1, 0))


def symmetry_clauses():
    next_variable = 848
    # Remaining R4 blocks, then all R3 blocks: independent identical-atom classes.
    for group in (list(range(1, 7)), list(range(7, 12))):
        for left, right in zip(group, group[1:]):
            xs, ys = signature_key(left), signature_key(right)
            prefix = 1
            for position, (x, y) in enumerate(zip(xs, ys)):
                yield (-prefix, x, -y)
                if position + 1 < len(xs):
                    updated = next_variable
                    next_variable += 1
                    yield (-updated, prefix)
                    yield (-updated, -x, y)
                    yield (-updated, x, -y)
                    yield (-prefix, -x, -y, updated)
                    yield (-prefix, x, y, updated)
                    prefix = updated
    if next_variable != 967:
        raise ValueError('auxiliary variable census')


def expected():
    yield (1,)
    yield from root_clauses()
    yield from physical_clauses()
    yield from symmetry_clauses()


def audit(path):
    path = Path(path); digest = hashlib.sha256(); histogram = {}; wanted = expected()
    with path.open('rb') as stream:
        header = stream.readline(); digest.update(header); words = header.split()
        if words[:2] != [b'p', b'cnf'] or len(words) != 4:
            raise ValueError('header')
        variables, declared = map(int, words[2:])
        if variables != 966:
            raise ValueError('variables')
        count = 0
        for count, line in enumerate(stream, 1):
            digest.update(line); fields = list(map(int, line.split()))
            if not fields or fields[-1] != 0 or 0 in fields[:-1]:
                raise ValueError(f'syntax {count}')
            clause = tuple(fields[:-1])
            if any(abs(x) > variables for x in clause):
                raise ValueError(f'range {count}')
            try: expected_clause = next(wanted)
            except StopIteration as exc: raise ValueError('extra clause') from exc
            if clause != expected_clause:
                raise ValueError(f'literal mismatch {count}')
            histogram[len(clause)] = histogram.get(len(clause), 0) + 1
        try: next(wanted)
        except StopIteration: pass
        else: raise ValueError('missing clause')
    if count != declared or declared != 1426489:
        raise ValueError('clause census')
    return {'status': 'INDEPENDENT_LITERAL_AUDIT_BLOCK_NORMALIZED_R7_S4_T3',
            'branch': [7, 4, 3], 'vertices': 43,
            'five_sets_checked': 962598, 'fixed_red_edges': 57,
            'free_physical_edges': 846, 'variables': variables,
            'base_variables': 847, 'auxiliary_prefix_variables': 119,
            'clauses': declared, 'base_clauses': 1425766,
            'symmetry_clauses': 723, 'block_comparisons': 9,
            'block_action': 'S6 x S5',
            'clause_lengths': dict(sorted(histogram.items())),
            'bytes': path.stat().st_size, 'sha256': digest.hexdigest()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('cnf'); parser.add_argument('--output')
    args = parser.parse_args(); result = audit(args.cnf)
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output: Path(args.output).write_text(text)
    print(text, end='')
