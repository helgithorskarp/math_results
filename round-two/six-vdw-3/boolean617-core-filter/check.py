#!/usr/bin/env python3
"""Independent square-set / truth-bit intersection replay. No generator import."""
import argparse
import hashlib
import json
import struct
from pathlib import Path


def demand(condition, message):
    if not condition:
        raise ValueError(message)


def check(record):
    p = 617
    roots = record['roots']
    demand(record['schema'] == 'boolean617-regular-core-v1', 'schema')
    demand(record['prime'] == p, 'prime')
    demand(len(roots) == 3 and roots[:2] == [0, 1] and type(roots[2]) is int and 2 <= roots[2] < p, 'roots')
    demand(record['gauge'] == 'F(000)=0' and record['truth_index'] == 'b0+2*b1+4*b2', 'truth convention')
    demand(record['original_roots_all_free'] is True, 'all original roots must be free')
    demand(record['domain'] == {'starts': [0, 616], 'steps': [1, 308], 'pairs': 190036,
                               'reversal_covers_all_nonzero_field_steps': True}, 'domain')
    # Independently construct the character by actual squares, never Euler powers.
    squares = {x*x % p for x in range(1, 309)}
    demand(len(squares) == 308 and 0 not in squares, 'square count')
    demand(all(p % d for d in range(2, 25)), 'prime617 trial divisions')

    def argument(x):
        if x in roots:
            return None
        answer = 0
        for i, r in enumerate(roots):
            answer += (0 if (x-r) % p in squares else 1) * (2 ** i)
        return answer

    args = [argument(x) for x in range(p)]
    words = tuple(range(0, 256, 2))
    # Columns are truth-table evaluations, built independently from label-set masks.
    one_columns = tuple(sum(1 << j for j, w in enumerate(words) if w & (2 ** i)) for i in range(8))
    universe = (1 << 128) - 1
    histogram = [0] * 256
    transcript = hashlib.sha256()
    blocked = 0
    first = {}
    for d in range(1, 309):
        for a in range(p):
            zero, one = universe, universe
            labels = 0
            x = a
            for _ in range(7):
                i = args[x]
                if i is None:
                    labels = 0
                    zero = one = 0
                    break
                labels |= 2 ** i
                one &= one_columns[i]
                zero &= universe ^ one_columns[i]
                x = (x+d) % p
            histogram[labels] += 1
            transcript.update(struct.pack('>HHB', a, d, labels))
            hit = zero | one
            newly = hit & ~blocked
            while newly:
                lo = newly & -newly
                j = lo.bit_length() - 1
                first[str(words[j])] = [a, d]
                newly -= lo
            blocked |= hit
    expected_blocked = [w for j, w in enumerate(words) if blocked & (1 << j)]
    expected_survivors = [w for j, w in enumerate(words) if not blocked & (1 << j)]
    demand(record['histogram'] == histogram and sum(histogram) == 190036, 'complete AP histogram')
    demand(record['transcript_sha256'] == transcript.hexdigest(), 'every AP transcript')
    demand(record['blocked_words'] == expected_blocked, 'blocked truth-word cover')
    demand(record['survivor_words'] == expected_survivors, 'exact survivor list')
    demand(record['witnesses'] == first, 'deterministic first witness list')
    literal_points = 0
    for w in expected_blocked:
        a, d = record['witnesses'][str(w)]
        demand(type(a) is int and type(d) is int and 0 <= a < p and 1 <= d <= 308, 'witness pair')
        colors = []
        for k in range(7):
            x = (a + k*d) % p
            demand(x not in roots, 'witness visits a free root')
            index = sum((0 if (x-r) % p in squares else 1) * (2 ** j) for j, r in enumerate(roots))
            colors.append((w // (2 ** index)) % 2)
            literal_points += 1
        demand(len(set(colors)) == 1, 'literal positive witness is not monochromatic')
    reversal_coordinates = 0
    for d in range(309, 617):
        shorter = p-d
        demand(1 <= shorter <= 308, 'short-step reversal range')
        for a in range(p):
            b = (a+6*d) % p
            for k in range(7):
                demand((a+k*d) % p == (b+(6-k)*shorter) % p, 'literal reversal identity')
                reversal_coordinates += 1
    return {'schema': 'boolean617-regular-core-check-v1', 't': roots[2],
            'complete_pairs_replayed': 190036, 'root_avoiding_pairs': sum(histogram[1:]),
            'blocked_words': expected_blocked, 'survivor_words': expected_survivors,
            'literal_witness_points_checked': literal_points,
            'literal_reversal_coordinates_checked': reversal_coordinates,
            'transcript_sha256': transcript.hexdigest(), 'status': 'EXACT_CORE_FILTER_CHECKED'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = check(json.loads(args.input.read_text()))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps({'t': receipt['t'], 'status': receipt['status'],
                      'blocked': len(receipt['blocked_words']), 'survivors': receipt['survivor_words'],
                      'complete_pairs_replayed': receipt['complete_pairs_replayed']}))


if __name__ == '__main__':
    main()
