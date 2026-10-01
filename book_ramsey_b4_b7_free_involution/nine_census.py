"""Exact necessary quotient census at three red/six blue uniform pairs.
Author: six-books-2, role researcher. Coverage and trust boundary: NINE.md.
Reuses earlier fast page budgets and unrestricted component canonicalizer.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time

from eight_census import generate_forms as five_blue_forms
from four_blue_census import PAIRS, add, inspect
from four_blue_independent import canonical_blue


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def generate_forms():
    five, five_positions = five_blue_forms()
    forms = {}
    positions = 0
    for edges in five.values():
        for edge in PAIRS:
            if edge in edges:
                continue
            key, canonical, _ = canonical_blue(tuple(sorted([*edges, edge])))
            forms.setdefault(key, canonical)
            positions += 1
    require(five_positions == 561 and len(five) == 26, 'complete five-blue input')
    require(positions == 1300 and len(forms) == 67, 'complete six-blue augmentation domain')
    return forms, positions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    forms, positions = generate_forms()
    records, cases = [], []
    for _, edges in sorted(forms.items()):
        blue = [0] * 11
        for edge in edges:
            add(blue, edge)
        candidates = [(i, j) for i, j in PAIRS if not (blue[i] >> j & 1)
                      and (blue[i] | blue[j]).bit_count() >= 3]
        counts = {'blue_pairs': edges, 'red_candidates': candidates,
                  'red_triples': 0, 'support_pass': 0, 'matching_pass': 0,
                  'necessary_survivors': 0, 'inside_flag_survivors': 0}
        for red_edges in combinations(candidates, 3):
            counts['red_triples'] += 1
            red = [0] * 11
            for edge in red_edges:
                add(red, edge)
            if sum(bool(r | b) for r, b in zip(red, blue)) < 9:
                continue
            counts['support_pass'] += 1
            flags = inspect(red, blue)
            if flags is None:
                continue
            counts['matching_pass'] += 1
            if flags:
                counts['necessary_survivors'] += 1
                counts['inside_flag_survivors'] += len(flags)
                records.append({'blue_pairs': edges, 'red_pairs': red_edges, 'flags': flags})
        cases.append(counts)
    args.records.write_text(json.dumps(records, indent=2) + '\n')
    result = {'agent': 'six-books-2', 'role': 'researcher', 'complete': True,
              'red_uniform_pairs': 3, 'blue_uniform_pairs': 6,
              'uniform_support_minimum': 9, 'six_blue_augmentations': positions,
              'blue_forms': len(forms),
              'red_triples': sum(c['red_triples'] for c in cases),
              'support_pass': sum(c['support_pass'] for c in cases),
              'matching_pass': sum(c['matching_pass'] for c in cases),
              'necessary_survivors': len(records),
              'inside_flag_survivors': sum(c['inside_flag_survivors'] for c in cases),
              'cases': cases, 'degree_theorem_used': False,
              'full_matching_sign_enumeration': False, 'wall_seconds': time.monotonic() - start}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
