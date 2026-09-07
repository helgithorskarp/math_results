#!/usr/bin/env python3
"""Exhaustive controls for the residual block lexicographic comparator."""
from itertools import product
from pathlib import Path
import argparse
import json
import sys


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from block_symmetry import lex_geq


def holds(clause, assignment):
    return any(assignment[abs(x)] == (x > 0) for x in clause)


def comparator_controls():
    tested = 0
    for length in range(1, 6):
        xs = tuple(range(2, 2 + length))
        ys = tuple(range(2 + length, 2 + 2 * length))
        first_aux = 2 + 2 * length
        clauses, stop = lex_geq(xs, ys, first_aux)
        auxiliaries = tuple(range(first_aux, stop))
        for xbits in product((False, True), repeat=length):
            for ybits in product((False, True), repeat=length):
                satisfying = 0
                for abits in product((False, True), repeat=len(auxiliaries)):
                    assignment = {1: True}
                    assignment.update(zip(xs, xbits)); assignment.update(zip(ys, ybits))
                    assignment.update(zip(auxiliaries, abits))
                    satisfying += all(holds(c, assignment) for c in clauses)
                wanted = int(xbits >= ybits)
                if satisfying != wanted:
                    raise ValueError((length, xbits, ybits, satisfying, wanted))
                tested += 1
    return tested


def tuple_key_controls():
    checked = 0
    for size in (3, 4):
        tuples = list(product(range(16), repeat=size))
        samples = tuples[::max(1, len(tuples) // 257)] + tuples[-1:]
        for a in samples:
            abit = tuple((value >> bit) & 1 for value in a for bit in range(3, -1, -1))
            for b in samples:
                bbit = tuple((value >> bit) & 1 for value in b for bit in range(3, -1, -1))
                if (a >= b) != (abit >= bbit):
                    raise ValueError('signature tuple bit order')
                checked += 1
    return checked


def run():
    return {'status': 'VERIFIED_IDENTICAL_BLOCK_COMPARATOR_CONTROLS',
            'comparator_assignments': comparator_controls(),
            'tuple_key_pairs': tuple_key_controls(),
            'tested_lengths': [1, 2, 3, 4, 5]}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output')
    args = parser.parse_args(); result = run()
    text = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output: Path(args.output).write_text(text)
    print(text, end='')
