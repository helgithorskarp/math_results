"""Per-truth literal positive AP search; no native bit-mask library."""
import argparse
import json
from field import P, PROJECTIONS, bit, colors, cover, gauss, need, squares, transport

def generate(t):
    table = gauss()
    witnesses = []
    tested = 0
    for word in range(0, 256, 2):
        if word in PROJECTIONS:
            continue
        coloring = colors(t, word, table)
        answer = None
        for d in range(1, (P+1)//2):
            for a in range(P):
                tested += 1
                color = coloring[a]
                if color is None:
                    continue
                if all(coloring[(a+j*d) % P] == color for j in range(1, 7)):
                    answer = [word, a, d]
                    break
            if answer is not None:
                break
        need(answer is not None, 'positive search incomplete; not a classification verdict')
        witnesses.append(answer)
    return {'t': t, 'witnesses': witnesses, 'candidate_pairs_tested': tested}

def validate(record, expected_t):
    need(type(record) is dict and record['t'] == expected_t, 'geometry identity')
    witnesses = record['witnesses']
    expected = [w for w in range(0, 256, 2) if w not in PROJECTIONS]
    need([row[0] for row in witnesses] == expected, 'entire truth domain')
    table = squares()
    for word, a, d in witnesses:
        need(type(a) is int and type(d) is int and 0 <= a < P and 1 <= d <= P//2, 'field AP coordinates')
        points = [(a+j*d) % P for j in range(7)]
        need(len(set(points)) == 7 and not set(points) & {0, 1, expected_t}, 'all original roots avoided')
        actual = [bit(word, [table[(x-r) % P] for r in (0, 1, expected_t)]) for x in points]
        need(len(set(actual)) == 1, 'literal monochromatic field AP')
    return len(witnesses)

def raw_check(records):
    table = gauss()
    lookup = {r['t']: {w: (a, d) for w, a, d in r['witnesses']} for r in records}
    need(sorted(lookup) == [r[0] for r in cover()], 'entire geometry inventory')
    states = 0
    checksum = 0
    for t in range(2, P):
        for word in range(0, 256, 2):
            representative, new_word, offset, scale, order, gauge = transport(t, word, table)
            for index in range(8):
                canonical = [(index >> k) & 1 for k in range(3)]
                original = [None]*3
                for k in range(3):
                    original[order[k]] = canonical[k] ^ table[scale]
                need(bit(word, original) == (bit(new_word, canonical) ^ gauge), 'entire abstract truth pullback')
            if word in PROJECTIONS:
                need(new_word in PROJECTIONS, 'projection transport')
                continue
            need(new_word not in PROJECTIONS, 'nonprojection transport')
            a, d = lookup[representative][new_word]
            original_a, original_d = (offset+scale*a) % P, scale*d % P
            if original_d > P//2:
                original_a = (original_a+6*original_d) % P
                original_d = P-original_d
            need(1 <= original_d <= P//2, 'short positive lift step')
            first = original_a or P
            integer_points = [first+j*original_d for j in range(7)]
            need(integer_points[-1] <= P+6*(P//2), 'lift endpoint')
            values = []
            for n in integer_points:
                x = n % P
                need(x not in (0, 1, t), 'raw ignored root avoidance')
                y = (x-offset)*pow(scale, -1, P) % P
                source = [table[(x-r) % P] for r in (0, 1, t)]
                canonical = [table[(y-r) % P] for r in (0, 1, representative)]
                need(all(source[order[k]] == (canonical[k] ^ table[scale]) for k in range(3)), 'character transport identity')
                value = bit(word, source)
                need(value == (bit(new_word, canonical) ^ gauge), 'truth transport identity')
                values.append(value)
            need(len(set(values)) == 1, 'raw positive witness')
            states += 1
            checksum += first+original_d+word+t
    return {'raw_nonprojection_states': states, 'raw_witness_points': 7*states,
            'positive_lift_endpoint_bound': P+6*(P//2), 'coordinate_checksum': checksum,
            'abstract_truth_entries_checked': (P-2)*128*8}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['generate', 'validate', 'raw'])
    parser.add_argument('value')
    args = parser.parse_args()
    if args.action == 'generate':
        print(json.dumps(generate(int(args.value)), sort_keys=True))
    elif args.action == 'validate':
        record = json.load(open(args.value))
        print(json.dumps({'t': record['t'], 'verified_positive_rules': validate(record, record['t'])}, sort_keys=True))
    else:
        print(json.dumps(raw_check(json.load(open(args.value))), sort_keys=True))
