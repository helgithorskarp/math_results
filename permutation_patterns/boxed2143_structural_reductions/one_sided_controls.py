#!/usr/bin/env python3
"""Exact finite controls for the one-sided interval obstruction."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path
import platform

from rectangle_checker import boxed_occurrences


def consecutive_2143(word):
    return tuple(i for i in range(len(word)-3) if word[i+1] < word[i] < word[i+3] < word[i+2])


def restrictions(p):
    return {
        'initial': [{'t': t, 'word': tuple(x for x in p if x <= t)} for t in range(1, len(p)+1)],
        'terminal': [{'t': t, 'word': tuple(x for x in p if x >= t)} for t in range(1, len(p)+1)],
    }


def one_sided_detects(p):
    return any(consecutive_2143(record['word']) for records in restrictions(p).values() for record in records)


def run():
    tested = 0
    minimal = None
    for n in range(7):
        for p in itertools.permutations(range(1, n+1)):
            tested += 1
            if boxed_occurrences(p) and not one_sided_detects(p):
                minimal = p
                break
        if minimal is not None:
            break
    if minimal != (3, 1, 2, 5, 6, 4):
        raise RuntimeError(f'Unexpected minimal counterexample: {minimal}')
    families = []
    for k in range(1, 7):
        for l in range(1, 7):
            p = (k+2,) + tuple(range(1, k+1)) + (k+1, k+4) + tuple(range(k+5, k+l+5)) + (k+3,)
            if not boxed_occurrences(p) or one_sided_detects(p):
                raise RuntimeError(f'Family control failed: {k}, {l}')
            families.append({'k': k, 'l': l, 'p': p, 'occurrences': boxed_occurrences(p)})
    stream = json.dumps(families, sort_keys=True, separators=(',', ':')).encode()
    return {
        'actor': 'literature-researcher-4', 'decision_message_id': 410,
        'claim_status': 'finite controls for written obstruction awaiting independent review',
        'full_target_solved': False, 'python': platform.python_version(),
        'permutations_tested_until_first_failure': tested,
        'minimal_counterexample': minimal, 'occurrences': boxed_occurrences(minimal),
        'one_sided_restrictions': restrictions(minimal),
        'family_scope': 'all 1<=k,l<=6', 'family_cases': len(families),
        'family_stream_sha256': hashlib.sha256(stream).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    rendered = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
