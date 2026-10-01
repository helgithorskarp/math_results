#!/usr/bin/env python3
"""Literal finite controls for ordered search and both exact certificate layers."""
import argparse
from copy import deepcopy
from itertools import combinations
import json
from pathlib import Path
import subprocess
from audit import (Ordered, base, capacity, check_capacity_core, inputs,
                   mask, ordered_partitions, ownership, points, require, triples)
from color_certificate import check as check_color


def rejected(action):
    try:
        action()
    except RuntimeError:
        return
    raise RuntimeError('malformed evidence accepted')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--native', type=Path, required=True)
    parser.add_argument('--certificate', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    native = Ordered(args.native.resolve())
    decisions = 0
    try:
        edges = list(combinations(range(5), 2))
        for bits in range(1 << len(edges)):
            rows = [0]*5
            for k, (a, b) in enumerate(edges):
                if bits & (1 << k):
                    rows[a] |= 1 << b
                    rows[b] |= 1 << a
            for size in range(1, 6):
                literal = [q for q in combinations(range(5), size)
                           if all(rows[a] & (1 << b) for a, b in combinations(q, 2))]
                require(native.enumerate(rows, list(range(5)), size) == literal,
                        'small graph ordered census mismatch')
                decisions += 1
        boundaries = 0
        for n in (64, 65, 96, 128):
            for size in (9, 10):
                clique = list(range(n-size, n))
                rows = [0]*n
                for a, b in combinations(clique, 2):
                    rows[a] |= 1 << b
                    rows[b] |= 1 << a
                result = native.enumerate(rows, list(range(n)), 9)
                require(result == list(combinations(clique, 9)), 'bit boundary census mismatch')
                boundaries += 1
    finally:
        native.close()
    malformed = ['129 9\n', '1 0\n0\n', '2 1\n1 1\n0\n',
                 '2 1\n2 1 1\n1 0\n', '1 1\n0\nBROKEN\n']
    for text in malformed:
        p = subprocess.run([str(args.native.resolve())], input=text, text=True,
                           capture_output=True, timeout=5)
        require(p.returncode != 0, 'malformed graph stream accepted')
    tails = [mask(q) for q in combinations(range(6), 3)]
    # Six-point partition fixture padded with three disjoint mandatory triples.
    tail_fixture = tails + [mask(range(a, a+3)) for a in (6, 9, 12)]
    actual, _ = ordered_partitions(tail_fixture)
    literal = sorted(tuple(sorted(tail_fixture[i] for i in q))
                     for q in combinations(range(len(tail_fixture)), 5)
                     if sum(tail_fixture[i].bit_count() for i in q) ==
                     mask(x for x in range(15) if any(tail_fixture[i] & (1 << x) for i in q)).bit_count())
    require(actual == literal and len(actual) == 10, 'ordered partition control mismatch')
    cores = [c for k in range(6) for c in json.loads((args.work/f'joints-{k}.json').read_text())]
    certificates = json.loads(args.certificate.read_text())['certificates']
    lookup = {c['core_sha256']: c for c in certificates}
    core = cores[0]
    original = lookup[core['core_sha256']]
    check_capacity_core(core, original)
    changes = []
    changed = deepcopy(original); changed['weights'][0][3] = -1; changes.append(changed)
    changed = deepcopy(original); changed['weights'][0][3] = True; changes.append(changed)
    changed = deepcopy(original); changed['weights'].append(changed['weights'][0]); changes.append(changed)
    changed = deepcopy(original); changed['weights'] = []; changes.append(changed)
    changed = deepcopy(original); changed['numerator'] += 1; changes.append(changed)
    changed = deepcopy(original); changed['candidate_sha256'] = '0'*64; changes.append(changed)
    changed = deepcopy(original); changed['core_sha256'] = '0'*64; changes.append(changed)
    changed = deepcopy(original); changed['denominator'] = 999; changes.append(changed)
    old_triple = next(t for w in core['blocks'] for t in combinations(points(w), 3) if max(t) < 15)
    changed = deepcopy(original); changed['weights'].append(list(old_triple)+[1]); changes.append(changed)
    for changed in changes:
        rejected(lambda: check_capacity_core(core, changed))
    rejected(lambda: capacity(cores[:-1], args.certificate))
    rejected(lambda: capacity(cores[:-1]+[cores[0]], args.certificate))
    stars = inputs()[1]
    original_words = base(15, ownership(stars[0]['fixed'], 19))[0]
    removed = next(w for w in stars[0]['fixed'] if w & (1 << 16))
    faulty = base(15, ownership([w for w in stars[0]['fixed'] if w != removed], 18))[0]
    extra = set(faulty)-set(original_words)
    require(extra and any(triples(w) & triples(removed) for w in extra),
            'missing xz anchor constraint was not exposed')
    color_cert = json.loads(Path(__file__).with_name('COLOR_CERT.json').read_text())
    universe = next(words for h, words, bound in json.loads((args.work/'residual-universes.json').read_text())
                    if h == color_cert['core_sha256'])
    positive = check_color(color_cert, color_cert['core_sha256'], universe)
    damaged = []
    changed = deepcopy(color_cert); changed['tree']['branches'].pop(); damaged.append(changed)
    changed = deepcopy(color_cert); changed['tree']['branches'] = []; damaged.append(changed)
    changed = deepcopy(color_cert); changed['nodes'] += 1; damaged.append(changed)
    changed = deepcopy(color_cert); changed['candidate_sha256'] = '0'*64; damaged.append(changed)
    changed = deepcopy(color_cert); changed['tree']['branches'][0][1]['color'] = changed['tree']['color']; damaged.append(changed)
    i, j = next((i, j) for i, j in combinations(range(len(universe)), 2)
                if (universe[i] & universe[j]).bit_count() <= 2)
    changed = deepcopy(color_cert); changed['colors'][i] = changed['colors'][j]; damaged.append(changed)
    for changed in damaged:
        rejected(lambda: check_color(changed, color_cert['core_sha256'], universe))
    print(json.dumps({'status': 'COMPLETE', 'small_graph_decisions': decisions,
                      'bit_boundary_graphs': boundaries, 'malformed_native_streams': len(malformed),
                      'literal_partition_control_count': len(actual),
                      'malformed_weight_or_binding_controls': len(changes)+2,
                      'missing_xz_constraint_exposed': True,
                      'malformed_color_certificate_controls': len(damaged),
                      'positive_color_check': positive}, indent=2))


if __name__ == '__main__':
    main()
