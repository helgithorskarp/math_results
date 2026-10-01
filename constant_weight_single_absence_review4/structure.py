#!/usr/bin/env python3
"""Proved parallel-class restriction, checked against every unrestricted cover."""
import argparse
from itertools import combinations
import json
from pathlib import Path

from audit import digest, template
from covers import census, group_covers, need, pairs


def run():
    Q, x, y, absent = template()
    cases = []
    for a in absent:
        baseline, original = census(Q, x, y, a)
        tails = sorted(tuple(sorted(set(q)-{a})) for q in Q if a in q)
        T = set(range(18))-{a, x, y}
        classes = [[] for _ in tails]
        for q in original['legal_columns']:
            missing = [g for g, tail in enumerate(tails) if not (set(q) & set(tail))]
            need(len(missing) == 1, 'each transversal omits exactly one group')
            classes[missing[0]].append(q)
        U = frozenset(p for p in combinations(sorted(T), 2)
                      if not any(set(p) <= set(tail) for tail in tails))
        options = []
        for g, group in enumerate(classes):
            wanted = T-set(tails[g])
            partitions = []
            for triple in combinations(group, 3):
                union = set().union(*map(set, triple))
                if union == wanted and sum(map(len, triple)) == len(union):
                    partitions.append((triple, frozenset().union(*(pairs(q) for q in triple))))
            options.append(partitions)
        reduced, states = group_covers(options, U)
        need(reduced == baseline, 'every complete cover entry after proved partition restriction')
        checked = 0
        for cover in reduced:
            for g, tail in enumerate(tails):
                blocks = [q for q in cover if not (set(q) & set(tail))]
                need(len(blocks) == 3 and set().union(*map(set, blocks)) == T-set(tail)
                     and sum(map(len, blocks)) == 12, 'literal parallel class')
                checked += 1
        cases.append({'a': a, 'partition_options': list(map(len, options)),
                      'restricted_states': states, 'unrestricted_states': original['states'],
                      'covers_compared': len(reduced), 'parallel_classes_checked': checked,
                      'complete_cover_sha256': digest(reduced)})
    return {'cases': cases, 'complete_cover_entries_compared': 24,
            'parallel_classes_checked': 120, 'complete': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected', type=Path)
    args = parser.parse_args()
    result = run()
    if args.expected:
        need(result == json.loads(args.expected.read_text()), 'structure expected output')
    print(json.dumps(result, indent=2, sort_keys=True))
