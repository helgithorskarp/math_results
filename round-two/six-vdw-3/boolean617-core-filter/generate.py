#!/usr/bin/env python3
"""Necessary regular-core test only; positive APs refute individual rules."""
import argparse
import hashlib
import json
import struct
from pathlib import Path

P = 617


def generate(t):
    if type(t) is not int or not 2 <= t < P:
        raise ValueError('The distinct normalized roots must be 0,1,t')
    bits = [None] + [(0 if pow(x, 308, P) == 1 else 1) for x in range(1, P)]
    signature = []
    for x in range(P):
        values = [bits[(x - r) % P] for r in (0, 1, t)]
        signature.append(None if None in values else sum(v << i for i, v in enumerate(values)))
    words = list(range(0, 256, 2))
    library = [0] * 256
    for labels in range(1, 256):
        arguments = [i for i in range(8) if labels >> i & 1]
        for j, word in enumerate(words):
            colors = {(word >> i) & 1 for i in arguments}
            if len(colors) == 1:
                library[labels] |= 1 << j
    histogram = [0] * 256
    witnesses = {}
    transcript = hashlib.sha256()
    blocked = 0
    for d in range(1, 309):
        for a in range(P):
            labels = 0
            for k in range(7):
                s = signature[(a + k * d) % P]
                if s is None:
                    labels = 0
                    break
                labels |= 1 << s
            histogram[labels] += 1
            transcript.update(struct.pack('>HHB', a, d, labels))
            newly = library[labels] & ~blocked
            while newly:
                low = newly & -newly
                j = low.bit_length() - 1
                witnesses[str(words[j])] = [a, d]
                newly ^= low
            blocked |= library[labels]
    survivors = [word for j, word in enumerate(words) if not (blocked >> j & 1)]
    return {
        'schema': 'boolean617-regular-core-v1', 'agent': 'six-vdw-3',
        'role': 'researcher', 'prime': P, 'roots': [0, 1, t],
        'gauge': 'F(000)=0', 'truth_index': 'b0+2*b1+4*b2',
        'original_roots_all_free': True,
        'domain': {'starts': [0, 616], 'steps': [1, 308], 'pairs': 190036,
                   'reversal_covers_all_nonzero_field_steps': True},
        'histogram': histogram, 'transcript_sha256': transcript.hexdigest(),
        'blocked_words': sorted(map(int, witnesses)),
        'witnesses': {str(w): witnesses[str(w)] for w in sorted(map(int, witnesses))},
        'survivor_words': survivors,
        'meaning': 'Exact regular cyclic617 core filter, not an interval coloring or interval feasibility result.'
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--t', type=int, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    record = generate(args.t)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(record, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'t': args.t, 'covered_pairs': record['domain']['pairs'],
                      'root_avoiding_pairs': sum(record['histogram'][1:]),
                      'blocked': len(record['blocked_words']),
                      'survivors': record['survivor_words']}))


if __name__ == '__main__':
    main()
