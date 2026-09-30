#!/usr/bin/env python3
"""six-reviewer-1: separate predicate audit, sharing no tensor-checker code."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from math import lcm
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cover', type=Path,
                        default=Path(__file__).with_name('refined_cover.json'))
    parser.add_argument('--expected', type=Path,
                        default=Path(__file__).with_name('refined_expected.json'))
    parser.add_argument('--check-neighbors', action='store_true',
                        help='separately replay every listed two-phase cover')
    args = parser.parse_args()
    data = json.loads(args.cover.read_text())
    rows = data['congruences']
    if not rows or any(len(row) != 2 or any(type(n) is not int for n in row) or
                       row[1] < 8 or not 0 <= row[0] < row[1] for row in rows):
        raise ValueError('invalid classes')
    moduli = [m for a, m in rows]
    period = lcm(*moduli)
    if len(set(moduli)) != len(rows) or min(moduli) != 8 or \
            period != data['lcm'] or period > 100000:
        raise ValueError('invalid distinctness, minimum or actual period')
    counts, private = [], {m: 0 for m in moduli}
    for x in range(period):
        hits = [m for a, m in rows if x % m == a]
        if not hits:
            raise ValueError('uncovered point: '+str(x))
        counts.append(len(hits))
        if len(hits) == 1:
            private[hits[0]] += 1
    if not all(private.values()):
        raise ValueError('certificate is not irredundant')
    result = {'classes': len(rows), 'lcm': period, 'minimum_modulus': 8,
              'uncovered': 0,
              'coverage_multiplicities': {str(k): v for k, v in sorted(Counter(counts).items())},
              'multiplicity_bytes_sha256': sha256(bytes(counts)).hexdigest(),
              'private_points_by_modulus': [[m, private[m]] for a, m in rows]}
    expected = json.loads(args.expected.read_text())
    if any(result[k] != expected[k] for k in result):
        raise ValueError('predicate and tensor summaries differ')
    print('FULL LITERAL CHECK PASSED: '+str(len(rows))+' classes, exact minimum 8, LCM '+str(period))
    if args.check_neighbors:
        alternatives = expected['phase_neighborhood']['alternatives_as_modulus_old_new']
        original = {m: a for a, m in rows}
        for changes in alternatives:
            if len(changes) != 2 or len({m for m, old, new in changes}) != 2 or \
                    any(type(new) is not int or not 0 <= new < m or
                        original.get(m) != old or new == old for m, old, new in changes):
                raise ValueError('invalid sparse neighbor')
            altered = {m: new for m, old, new in changes}
            counts = [0]*period
            for a, m in rows:
                for x in range(altered.get(m, a), period, m):
                    counts[x] += 1
            if not all(counts):
                raise ValueError('a classified two-phase neighbor has holes')
        if len(alternatives) != expected['phase_neighborhood']['two_phase_alternatives']:
            raise ValueError('inconsistent neighbor count')
        print('ALL '+str(len(alternatives))+' CLASSIFIED NEIGHBORS PASS SEPARATE PROGRESSION REPLAY')


if __name__ == '__main__':
    main()
