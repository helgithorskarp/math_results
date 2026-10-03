"""Separate scalar-row reconstruction of every four-port preparation function.

The producer is not imported. Starting from the actual sixteen inputs,
the direct row algorithm applies six compare-exchanges and exhausts its
own queue. Counts alone are never accepted as equality.
"""
import argparse
from collections import Counter, deque
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path
import resource
import time


def need(ok, why):
    if not ok:
        raise ValueError(why)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def exchange(value, a, b):
    bits = [int(value >> q & 1) for q in range(4)]
    bits[a], bits[b] = min(bits[a], bits[b]), max(bits[a], bits[b])
    return sum(bit << q for q, bit in enumerate(bits))


def reconstruct():
    started = time.monotonic()
    identity = tuple(range(16))
    paths, ids = {identity: []}, {identity: 0}
    queue, states, edges = deque([identity]), [], []
    gates = [list(g) for g in combinations(range(4), 2)]
    while queue:
        if time.monotonic() - started > 30 or len(paths) > 20000:
            raise RuntimeError('operational cap: incomplete scalar reconstruction')
        rows = queue.popleft()
        source = ids[rows]
        columns = [sum(((y >> q) & 1) << x for x, y in enumerate(rows)) for q in range(4)]
        word = paths[rows]
        for x, expected in enumerate(rows):
            value = x
            for a, b in word:
                value = exchange(value, a, b)
            need(value == expected, 'shortest representative does not realize function')
        states.append({'id': source, 'columns': columns, 'word': word})
        for a, b in gates:
            after = tuple(exchange(y, a, b) for y in rows)
            if after not in ids:
                ids[after] = len(ids)
                paths[after] = word + [[a, b]]
                queue.append(after)
            edges.append([source, [a, b], ids[after]])
    need(len(states) == len(paths) and len(edges) == 6 * len(paths), 'unfinished scalar queue')
    return {'ports': 4, 'gates': gates, 'states': states, 'all_edges': edges,
            'processed_states': len(states), 'queue_exhausted': True}


def inspect(supplied, expected):
    need(digest(supplied['mathematical']) == supplied['whole_math_sha256'], 'packet digest mismatch')
    need(supplied['mathematical'] == expected, 'entire scalar semigroup/word/edge data differs')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--input', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    start = time.monotonic()
    supplied = json.loads(args.input.read_text())
    expected = reconstruct()
    inspect(supplied, expected)
    damages = []
    edits = ['omit_function', 'omit_transition', 'wrong_transition_target',
             'wrong_truth_bit', 'wrong_word', 'unfinished_queue']
    for kind in edits:
        d = copy.deepcopy(supplied)
        math = d['mathematical']
        if kind == 'omit_function': math['states'].pop()
        elif kind == 'omit_transition': math['all_edges'].pop()
        elif kind == 'wrong_transition_target': math['all_edges'][0][2] = 0
        elif kind == 'wrong_truth_bit': math['states'][0]['columns'][0] ^= 1
        elif kind == 'wrong_word': math['states'][1]['word'] = []
        else: math['queue_exhausted'] = False
        # Repair the storage hash; rejection must come from actual mathematics.
        d['whole_math_sha256'] = digest(math)
        try:
            inspect(d, expected)
        except ValueError:
            damages.append(kind)
        else:
            raise ValueError('accepted semantic corruption '+kind)
    mathematical = {'entire_reconstructed_semigroup': expected,
                    'rejected_semantic_damages': damages,
                    'arbitrary_preparation_words_covered_by_closed_queue': True,
                    'sorting_network_exclusion': False}
    output = {'agent': 'six-sorting-2', 'role': 'researcher',
              'status': 'COMPLETE_SEPARATE_SCALAR_FOUR_PORT_SEMIGROUP',
              'mathematical': mathematical, 'whole_math_sha256': digest(mathematical),
              'seconds': time.monotonic()-start,
              'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    args.output.write_text(json.dumps(output, separators=(',', ':'))+'\n')
    print(json.dumps({'status': output['status'], 'functions': len(expected['states']),
                      'transitions': len(expected['all_edges']), 'semantic_damages': len(damages),
                      'shortest_lengths': dict(Counter(len(s['word']) for s in expected['states'])),
                      'whole_math_sha256': output['whole_math_sha256'],
                      'seconds': output['seconds'], 'rss_kib': output['maximum_rss_kib']}))


if __name__ == '__main__':
    main()
