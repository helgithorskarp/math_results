"""Exact necessary quotient census at three red/five blue uniform pairs.
Author: six-books-2, role researcher. The finite domain bridge is in EIGHT.md.
Reuses this contribution's published fast page routine and canonicalizer.
"""
import argparse
from itertools import combinations
import json
from pathlib import Path
import time

from four_blue_census import BLUE_FORMS, PAIRS, add, inspect
from four_blue_independent import canonical_blue


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def generate_forms():
    forms = {}
    traversed = 0
    for _, edges in BLUE_FORMS:
        for edge in PAIRS:
            if edge in edges:
                continue
            key, canonical, _ = canonical_blue(tuple(sorted([*edges, edge])))
            forms.setdefault(key, canonical)
            traversed += 1
    require(traversed == 561 and len(forms) == 26, 'complete five-blue augmentation domain')
    return forms, traversed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--records', type=Path, required=True)
    args = parser.parse_args()
    start = time.monotonic()
    forms, traversed = generate_forms()
    records, cases = [], []
    for _, edges in sorted(forms.items()):
        blue = [0] * 11
        for edge in edges:
            add(blue, edge)
        candidates = [(i, j) for i, j in PAIRS if not (blue[i] >> j & 1)
                      and (blue[i] | blue[j]).bit_count() >= 3]
        counts = {'blue_pairs': edges, 'red_candidates': candidates,
                  'red_triples': 0, 'matching_pass': 0, 'necessary_survivors': 0,
                  'inside_flag_survivors': 0}
        for red_edges in combinations(candidates, 3):
            counts['red_triples'] += 1
            red = [0] * 11
            for edge in red_edges:
                add(red, edge)
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
              'red_uniform_pairs': 3, 'blue_uniform_pairs': 5,
              'five_blue_augmentations': traversed, 'blue_forms': len(forms),
              'red_triples': sum(c['red_triples'] for c in cases),
              'matching_pass': sum(c['matching_pass'] for c in cases),
              'necessary_survivors': len(records),
              'inside_flag_survivors': sum(c['inside_flag_survivors'] for c in cases),
              'cases': cases, 'degree_theorem_used': False,
              'full_matching_sign_enumeration': False, 'wall_seconds': time.monotonic() - start}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
