"""Literal marked-packing identity/control checker; six-code-1, researcher.

The ordinary theorem in PROOF.md supplies the negative inference.
No producer, classification, solver, or external mathematical module is imported.
"""
import argparse
from collections import Counter
import copy
import hashlib
from itertools import combinations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encode(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'))+'\n').encode()


def literal(data):
    require(data['points'] == 17, 'the lemma uses17 points')
    masks = data['quadruple_masks']
    require(isinstance(masks, list) and masks, 'nonempty literal packing')
    require(all(type(m) is int and m > 0 and m >> 17 == 0 and m.bit_count() == 4
                for m in masks), 'four-subsets on17 points')
    require(len(masks) == len(set(masks)), 'distinct quadruples')
    blocks = [frozenset(i for i in range(17) if m >> i & 1) for m in masks]
    require(all(len(a & b) <= 1 for a, b in combinations(blocks, 2)),
            'quadruple pair packing')
    pairs = data['leave_pairs']
    require(isinstance(pairs, list) and 1 <= len(pairs) <= 3, 'one to three pairs')
    require(all(isinstance(p, list) and len(p) == 2 and
                all(type(t) is int and 0 <= t < 17 for t in p) for p in pairs),
            'literal pair domain')
    endpoints = [t for p in pairs for t in p]
    require(len(endpoints) == len(set(endpoints)), 'disjoint endpoint pairs')
    leave = {frozenset(p) for p in pairs}
    covered = {frozenset(p) for b in blocks for p in combinations(b, 2)}
    require(not (leave & covered), 'chosen pairs really uncovered')
    rho = {t: sum(t in b for b in blocks) for t in endpoints}
    require(set(rho.values()) == {5}, 'endpoint replication five')
    chosen = frozenset(endpoints)
    actual_pairs = {frozenset(p) for p in combinations(chosen, 2)}
    require(actual_pairs - covered == leave, 'every other endpoint pair covered')
    q = len(pairs)
    sizes = [len(b & chosen) for b in blocks]
    require(max(sizes) <= q, 'at most one endpoint of each pair')
    counts = Counter(sizes)
    point_total = sum(sizes)
    pair_total = sum(k*(k-1)//2 for k in sizes)
    require(point_total == 10*q, 'point incidence count')
    require(pair_total == 2*q*(q-1), 'endpoint pair count')
    require(counts[1] + counts[2] == 2*q*(6-q), 'inclusion-exclusion identity')
    require(len(blocks) == 2*q*(6-q) + counts[0] + counts[3],
            'complete block partition')
    return dict(
        points=17, blocks=len(blocks), selected_leave_pairs=q,
        endpoint_replications=[[t, rho[t]] for t in sorted(rho)],
        point_incidence_sum=point_total, endpoint_pair_incidence_sum=pair_total,
        intersection_histogram=[[k, counts[k]] for k in range(q+1)],
        exact_counting_lower=2*q*(6-q),
        literal_fixture_sha256=hashlib.sha256(encode(dict(
            masks=sorted(masks), pairs=sorted(sorted(p) for p in pairs)))).hexdigest())


def controls(data):
    variants = []
    def changed(name, edit):
        value = copy.deepcopy(data)
        edit(value)
        variants.append((name, value))
    changed('wrong point universe', lambda d: d.__setitem__('points', 18))
    changed('duplicate quadruple', lambda d: d['quadruple_masks'].append(d['quadruple_masks'][0]))
    changed('boolean mask', lambda d: d['quadruple_masks'].__setitem__(0, True))
    changed('outside point', lambda d: d['quadruple_masks'].__setitem__(0, (1 << 17) | 7))
    changed('nondisjoint pairs', lambda d: d['leave_pairs'][1].__setitem__(0, d['leave_pairs'][0][0]))
    changed('covered purported leave', lambda d: d['leave_pairs'].__setitem__(0,
        [d['leave_pairs'][0][0], d['leave_pairs'][1][0]]))
    endpoint = data['leave_pairs'][0][0]
    index = next(i for i, m in enumerate(data['quadruple_masks']) if m >> endpoint & 1)
    changed('endpoint degree below five', lambda d: d['quadruple_masks'].pop(index))
    rejected = []
    for name, value in variants:
        try:
            literal(value)
        except (ValueError, KeyError, TypeError):
            rejected.append(name)
        else:
            raise ValueError('accepted damaged input: '+name)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--fixture', type=Path, default=HERE/'positive16.json')
    parser.add_argument('--write-expected', type=Path)
    args = parser.parse_args()
    fixture = json.loads(args.fixture.read_bytes())
    values = literal(fixture)
    require((values['selected_leave_pairs'], values['blocks']) == (2, 16),
            'the published positive control is the two-pair16 example')
    require(values['intersection_histogram'] == [[0, 0], [1, 12], [2, 4]],
            'positive exact inventory')
    report = dict(actual_agent='six-code-1', role='researcher',
                  status='COMPLETE literal positive control and identity validation',
                  positive_fixture=values,
                  rejected_controls=controls(fixture),
                  coefficient_identity=[k-k*(k-1)//2 for k in range(4)],
                  three_pair_counting_lower=18,
                  scope='Theorem is the ordinary proof; this verifies no classification or whole-code nonexistence.')
    require(report['coefficient_identity'] == [0, 1, 1, 0], 'finite coefficient identity')
    if args.write_expected:
        args.write_expected.write_bytes(encode(report))
    else:
        require(report == json.loads((HERE/'expected.json').read_bytes()), 'expected record differs')
    print(json.dumps(dict(status=report['status'], positive_blocks=16,
                          rejected_controls=len(report['rejected_controls']),
                          stable_readout_sha256=hashlib.sha256(encode(report)).hexdigest())))


if __name__ == '__main__':
    main()
