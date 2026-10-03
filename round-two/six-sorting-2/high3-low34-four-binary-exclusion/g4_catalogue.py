"""Exact four-port comparator semigroup; packed-column producer.

Algorithm adapted from published10084 generate_cover.library (source
d2a3033d8230f13f97c471fff6e383351c57163d); count is now four, not three.
This only classifies preparation functions; it excludes no sorting network.
"""
import argparse
from collections import Counter
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def build():
    started = time.monotonic()
    gates = [list(g) for g in combinations(range(4), 2)]
    identity = tuple(sum(1 << x for x in range(16) if x >> q & 1) for q in range(4))
    states, paths, edges = [identity], [[]], []
    ids = {identity: 0}
    cursor = 0
    while cursor < len(states):
        if time.monotonic() - started > 30 or len(states) > 20000:
            raise RuntimeError('operational cap: unfinished catalogue, not an exclusion')
        for a, b in gates:
            after = list(states[cursor])
            after[a], after[b] = after[a] & after[b], after[a] | after[b]
            after = tuple(after)
            if after not in ids:
                ids[after] = len(states)
                states.append(after)
                paths.append(paths[cursor] + [[a, b]])
            edges.append([cursor, [a, b], ids[after]])
        cursor += 1
    return {'ports': 4, 'gates': gates,
            'states': [{'id': i, 'columns': list(f), 'word': word}
                       for i, (f, word) in enumerate(zip(states, paths))],
            'all_edges': edges, 'processed_states': cursor, 'queue_exhausted': True}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    start = time.monotonic()
    math = build()
    output = {'agent': 'six-sorting-2', 'role': 'researcher',
              'status': 'COMPLETE_FOUR_PORT_SEMIGROUP_PRODUCED_NOT_SEPARATELY_CHECKED',
              'mathematical': math, 'whole_math_sha256': digest(math),
              'seconds': time.monotonic() - start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, separators=(',', ':')) + '\n')
    print(json.dumps({'status': output['status'], 'functions': len(math['states']),
                      'transitions': len(math['all_edges']),
                      'shortest_lengths': dict(Counter(len(s['word']) for s in math['states'])),
                      'whole_math_sha256': output['whole_math_sha256'],
                      'seconds': output['seconds'], 'rss_kib': output['maximum_rss_kib']}))


if __name__ == '__main__':
    main()
