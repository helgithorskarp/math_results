"""Regenerate a compact certificate for the ninety conditional HIGH branches.
Weighted partitions/route DFS and packed columns are the producer. Generic
carrier pruning credits actual8999 and actual9285; packed profiles and anchors
are the copied six-sorting-2 sources listed in SOURCE-CREDITS.md. No solver.
"""
import argparse
from functools import lru_cache
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import resource
import time

ROOT = Path(__file__).resolve().parent
FIXTURE_SHA256 = 'c08176afb29259b1fa371ac88895f8ce73df51c5792d7babe870aae00d5e770c'
PINS = {'profile.py': 'dca9c8d6331c3fc548c514ca8f5f1cd170f4a0bb39a3c05250876247d0362719',
        'anchors.py': '0b95573e7e3c446d0b7ca5352f6b5f4b8d92b91d6f3c72e7b4f783cd99d89902'}
LEAVES = (5, 6, 7, 9, 10, 11)


def need(test, message):
    if not test:
        raise ValueError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, separators=(',', ':')).encode()).hexdigest()


def canonical_words():
    unit = LEAVES[:-1]
    gate = lambda a, b: sorted((a, b))
    words = []
    for single in unit:
        rest = [p for p in unit if p != single]
        for other in rest[1:]:
            left = (rest[0], other)
            right = tuple(p for p in rest if p not in left)
            words.append([gate(single, 11), gate(*left), gate(*right),
                          gate(max(left), max(right)), gate(max(rest), 11)])
    for single in unit:
        rest = [p for p in unit if p != single]
        for child in combinations(rest, 2):
            other = tuple(p for p in rest if p not in child)
            words.append([gate(*child), gate(single, max(child)), gate(*other),
                          gate(max(other), 11), gate(max(single, *child), 11)])
    need(len(words) == 45, 'weighted partition count differs')
    return words


def function(word):
    index = {p: i for i, p in enumerate(LEAVES)}
    out = [sum(1 << x for x in range(64) if x >> i & 1) for i in range(6)]
    for a, b in word:
        a, b = index[a], index[b]
        out[a], out[b] = out[a] & out[b], out[a] | out[b]
    return tuple(out)


def event_cover(words):
    controls = orders = 0
    functions = set()

    def explore(state, word):
        nonlocal controls, orders
        if len(state) == 1:
            need(state == ((11, 9),) and len(word) == 5, 'terminal HIGH route differs')
            orders += 1
            functions.add(function(word))
            return
        for (a, da), (b, db) in combinations(state, 2):
            controls += 1
            gate = sorted((a, b))
            child = tuple(sorted([(p, d) for p, d in state if p not in gate]
                                 + [(gate[1], 1 + max(da, db))]))
            if sum(1 << d for p, d in child) <= 512:
                explore(child, word + [gate])

    explore(tuple([(p, 6) for p in LEAVES[:-1]] + [(11, 7)]), [])
    need((orders, controls, len(functions)) == (300, 2145, 45), 'route census differs')
    need(functions == {function(w) for w in words}, 'weighted cover misses a route function')
    return {'valid_event_orders': orders, 'local_controls': controls,
            'distinct_six_input_functions': len(functions)}


def boolean_image(gates, semantic):
    columns = list(semantic.truth_columns(13))
    for a, b in gates:
        need(0 <= a < b < 13, 'nonstandard literal comparator')
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    return sorted({sum((columns[p] >> x & 1) << p for p in range(13))
                   for x in range(8192)})


def nine_image(base, suffix):
    columns = [sum(1 << j for j, x in enumerate(base) if x >> p & 1) for p in range(13)]
    for a, b in suffix:
        columns[a], columns[b] = columns[a] & columns[b], columns[a] | columns[b]
    for p in (0, 1, 11, 12):
        expected = sum(1 << j for j, x in enumerate(base) if p >= 13 - x.bit_count())
        need(columns[p] == expected, 'four held ranks differ')
    return sorted({sum((columns[p] >> j & 1) << (p - 2) for p in range(2, 11))
                   for j in range(len(base))})


def pruning(gates, low, high, semantic):
    free = [i for i in range(13) if not (low | high) >> i & 1]
    columns = iter(semantic.truth_columns(len(free)))
    values = ['L' if low >> i & 1 else 'H' if high >> i & 1 else next(columns)
              for i in range(13)]
    carrier = [free.index(i) if i in free else None for i in range(13)]
    word = []
    d = r = redundant = touches = 0
    for t, (a, b) in enumerate(gates):
        x, y = values[a], values[b]
        if isinstance(x, str) or isinstance(y, str):
            d += 1
            touches |= 1 << t
            rank = lambda z: -1 if z == 'L' else 1 if z == 'H' else 0
            if rank(x) > rank(y):
                values[a], values[b] = y, x
                carrier[a], carrier[b] = carrier[b], carrier[a]
        else:
            if not x & ~y:
                r += 1
                redundant |= 1 << t
            else:
                word.append([carrier[a], carrier[b]])
            values[a], values[b] = x & y, x | y
    current = semantic.marked_ports(values)
    output = [i for i in range(13) if isinstance(values[i], int)]
    rename = {carrier[i]: j for j, i in enumerate(output)}
    record = [low, high, *current, d, r, redundant]
    return {'outer_record': record, 'marked_touch_mask': touches,
            'input_free_wires': free, 'output_free_wires': output,
            'input_to_output_wire': [rename[i] for i in range(len(free))],
            'retained_prefix': [[rename[a], rename[b]] for a, b in word]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / 'certificate.json')
    args = parser.parse_args()
    start = time.monotonic()
    raw = (ROOT / 'fixture.json').read_bytes()
    need(hashlib.sha256(raw).hexdigest() == FIXTURE_SHA256, 'fixed fixture differs')
    f = json.loads(raw)
    for name, pin in PINS.items():
        need(hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == pin, 'credited source differs')
    spec = importlib.util.spec_from_file_location('binary_front_packed_anchors', ROOT / 'anchors.py')
    anchors = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(anchors)

    @lru_cache(None)
    def inner(word):
        data = anchors.semantic.analyze(7, [list(g) for g in word])
        bounds = anchors.both(7, data)
        return max(16, *(r['lower_bound'] for r in bounds.values())), data, bounds

    words = canonical_words()
    route = event_cover(words)
    base = boolean_image(f['B23'], anchors.semantic)
    need(len(base) == 179, 'base image size differs')
    rows = []
    replay = []
    masses = []
    number = 0
    for partner in (1, 4):
        for tree_id, high_word in enumerate(words):
            suffix = f['LOW_suffixes'][str(partner)] + high_word
            gates = f['B23'] + suffix
            selector = f['root_selectors'][number]
            need((selector['partner'], selector['tree_id']) == (partner, tree_id), 'root selection differs')
            need(selector['prefix_sha256'] == digest(gates) and len(gates) == 31, 'literal prefix differs')
            image = nine_image(base, suffix)
            selected = []
            classes = set()
            mass = 0
            for lo, hi in selector['original_clampings']:
                need(lo.bit_count() == hi.bit_count() == 3 and not lo & hi and lo | hi < 8192,
                     'selected original cube differs')
                pruned = pruning(gates, lo, hi, anchors.semantic)
                record = pruned['outer_record']
                q = tuple(tuple(g) for g in pruned['retained_prefix'])
                b, data, bounds = inner(q)
                z = tuple(record[2:4])
                need(z not in classes, 'selected current class repeats')
                classes.add(z)
                label = sum(record[4:6]) + b
                mass += 1 << label
                selected.append(record + [b])
                replay.append({'partner': partner, 'tree_id': tree_id, 'record': record,
                               'Q_sha256': digest(q), 'pruning_sha256': digest(pruned),
                               'inner_record_hashes': {n: digest(r['records']) for n, r in data.items()},
                               'inner_anchor_bounds': {side: r['lower_bound'] for side, r in bounds.items()},
                               'B7': b, 'label': label})
            need(mass > 1 << 44, 'strict root inequality failed')
            rows.append({'partner': partner, 'tree_id': tree_id, 'HIGH_word': high_word,
                         'nine_core_image_size': len(image), 'nine_core_image_sha256': digest(image),
                         'selected_records': selected, 'selected_mass': mass})
            masses.append({'partner': partner, 'tree_id': tree_id, 'mass': mass})
            number += 1
    need(number == 90 and len(replay) == 582 and inner.cache_info().currsize == 449,
         'complete selected proof census differs')
    need(digest(replay) == '7a2d35ac07b2beadd86a80d38d8e02c16be4f76a9d498a7927bcf24b54dee14b',
         'prior independently checked complete replay differs')
    middle = pruning(f['B23'] + f['LOW_suffixes']['2'], 40, 0, anchors.semantic)
    need(middle['outer_record'][4:6] == [9, 1] and len(middle['retained_prefix']) == 16,
         'published middle-LOW obstruction differs')
    packet = {'schema': 'b23-both-first-binary-certificate-v1', 'agent': 'six-sorting-1',
              'role': 'researcher', 'fixture_sha256': FIXTURE_SHA256, 'total_budget': 44,
              'base_image_size': len(base), 'base_image_sha256': digest(base), 'route_census': route,
              'root_records': rows, 'selected_occurrences': len(replay),
              'distinct_inner_words': inner.cache_info().currsize, 'replay_sha256': digest(replay),
              'root_masses_sha256': digest(masses), 'minimum_selected_mass': min(r['mass'] for r in masses),
              'middle_LOW_record': middle['outer_record'],
              'middle_LOW_pruning_sha256': digest(middle), 'middle_LOW_retained_length': 16,
              'conditional_HIGH_first_binary_branches': 90,
              'scope': 'First HIGH strict binary after LOW partners1/4; conditional both-first-binary B23 corollary.'}
    args.output.write_text(json.dumps(packet, separators=(',', ':')) + '\n')
    print(json.dumps({'agent': 'six-sorting-1', 'role': 'researcher',
                      'status': 'BOTH_FIRST_BINARY_CERTIFICATE_REGENERATED',
                      'certificate_bytes': args.output.stat().st_size,
                      'certificate_sha256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
                      'roots': 90, 'selected_occurrences': len(replay), 'distinct_inner_words': 449,
                      'minimum_selected_mass': packet['minimum_selected_mass'],
                      'replay_sha256': digest(replay), 'seconds': time.monotonic() - start,
                      'maximum_rss_kib': resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == '__main__':
    main()
