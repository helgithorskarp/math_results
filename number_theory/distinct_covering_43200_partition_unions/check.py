#!/usr/bin/env python3
"""Literal physical integer certificate. Standard library; no solver or private input.

The written binary/grouping argument supplies the necessary inequality.
Every eligible resource and every designated inside/outside choice is checked.
All full union loops keep a20-second cap; an incomplete replay proves nothing.
"""
import argparse
from copy import deepcopy
from fractions import Fraction
from hashlib import sha256
from itertools import product
import json
from pathlib import Path
from time import monotonic

N, Q, B, T, b, C, SCALE = 43200, 10800, 64, 32, 16, 675, 60
TOP = {B * d for d in range(1, C + 1) if C % d == 0}
ORDER = (8,9,10,12,15,16,18,20,24,25,30,36,40,45,48,50,75,54,60)
PHASES = (0,0,5,10,1,4,3,17,2,3,11,30,27,19,14,33,13,6,59)
GROUPS = [[3,5,9,15],[25,27],[45,75]]


def validate(data):
    if (set(data) != {'format','N','Q','moduli','residues','groups','boxes'}
            or data['format'] != 'literal-partition-union-boxes-v1'
            or type(data['N']) is not int or data['N'] != N
            or type(data['Q']) is not int or data['Q'] != Q
            or data['moduli'] != list(ORDER) or data['residues'] != list(PHASES)
            or any(type(v) is not int for v in data['moduli'] + data['residues'])
            or data['groups'] != GROUPS or not isinstance(data['boxes'], list)):
        raise ValueError('Input is not the stated nineteen-class certificate')
    row = {'Q': Q, 'residues': data['residues'], 'groups': data['groups'], 'boxes': data['boxes']}
    base = decode_boxes(Q, row['boxes'])
    if any(w and any(x % m == a for m, a in zip(ORDER, PHASES)) for x, w in enumerate(base)):
        raise ValueError('Weight on a prescribed class')
    return row


def decode_boxes(period, boxes):
    if period != Q:
        raise ValueError('This new literal decoder supports Q10800 only')
    axes = (16, 27, 25)
    coordinates = {tuple(x % d for d in axes): x for x in range(Q)}
    if len(coordinates) != Q:
        raise ValueError('Ordinary-remainder coordinates are not bijective')
    weights = [0] * Q
    for box in boxes:
        if (len(box) != 4 or any(type(v) is not int for v in box)
                or box[3] <= 0 or any(not 0 < m < 1 << d for m, d in zip(box[:3], axes))):
            raise ValueError('Malformed physical box')
        leaves = [[a for a in range(d) if m >> a & 1] for m, d in zip(box[:3], axes)]
        for key in product(*leaves):
            x = coordinates[key]
            if weights[x]:
                raise ValueError('Overlapping boxes')
            weights[x] = box[3]
    if not any(weights):
        raise ValueError('Empty supported weight')
    return weights


def physical(row, order):
    start = monotonic()
    base = decode_boxes(Q, row['boxes'])
    vector = base * (N // Q)
    known = tuple(zip(order, row['residues']))
    if (row['Q'] != Q or len(known) != len(row['residues'])
            or any(type(a) is not int or not 0 <= a < m for m, a in known)
            or any(w and any(x % m == a for m, a in known) for x, w in enumerate(vector))):
        raise ValueError('Weight/phase/support mismatch')
    resources = [n for n in range(8, N + 1) if N % n == 0 and n not in order]
    if not TOP <= set(resources):
        raise ValueError('All top resources must be free')
    groups = tuple(tuple(group) for group in row['groups'])
    flat = tuple(d for group in groups for d in group)
    if (not groups or any(not group for group in groups) or len(flat) != len(set(flat))
            or any(type(d) is not int or d <= 1 or C % d for d in flat)):
        raise ValueError('Groups must be disjoint eligible cofactor resources')
    grouped = set(flat)
    capacities, restricted = {}, {}
    nonzero = [(x, w) for x, w in enumerate(vector) if w]
    phase_digest = sha256()
    actual_phases = 0
    for n in resources:
        populations = [0] * n
        for x, w in nonzero:
            populations[x % n] += w
        capacities[n] = max(populations)
        actual_phases += n
        phase_digest.update(json.dumps([n, populations], separators=(',', ':')).encode() + b'\n')
        if n in TOP and n != B:
            restricted[n // B] = [max(populations[t::b]) for t in range(b)]
    M = {d: capacities[B * d] for d in restricted}
    group_totals = [[] for _ in groups]
    digests = [sha256() for _ in groups]
    counts = [0] * len(groups)
    labels = []
    for t in range(b):
        if monotonic() - start >= 20:
            raise RuntimeError('Physical union replay hit20s; incomplete is no exclusion')
        points = [(x, vector[x]) for x in range(t + T, N, B) if vector[x]]
        for j, group in enumerate(groups):
            upper = None
            for k, phases in enumerate(product(*(range(-1, d) for d in group))):
                if k % 128 == 0 and monotonic() - start >= 20:
                    raise RuntimeError('Physical union replay hit20s; incomplete is no exclusion')
                inside = tuple((d, a) for d, a in zip(group, phases) if a >= 0)
                value = 2 * sum(w for x, w in points if any(x % d == a for d, a in inside))
                value += sum(M[d] for d, a in zip(group, phases) if a < 0)
                digests[j].update(json.dumps([t, phases, value], separators=(',', ':')).encode() + b'\n')
                counts[j] += 1
                upper = value if upper is None else max(upper, value)
            group_totals[j].append(upper)
        labels.append(sum(totals[t] for totals in group_totals)
                      + sum(max(M[d], 2 * restricted[d][t]) for d in restricted if d not in grouped))
    G = max(labels)
    outside = sum(capacities[n] for n in resources if n not in TOP)
    total = outside + G
    factor = Fraction(SCALE * Q, N)
    if total >= sum(vector):
        raise ValueError('The full physical integer inequality is not strict')
    first_group = set(groups[0])
    single_group = outside + max(group_totals[0][t]
        + sum(max(M[d], 2 * restricted[d][t]) for d in restricted if d not in first_group)
        for t in range(b))
    return {'residues': row['residues'], 'Q': Q, 'groups': [list(g) for g in groups],
            'physical_demand': sum(vector), 'physical_G': G, 'physical_outside_capacity': outside,
            'physical_total': total, 'strict_physical_gap': sum(vector) - total,
            'ordinary_physical_capacity': sum(capacities.values()),
            'actual_resources': len(resources), 'actual_phases_evaluated': actual_phases,
            'all_physical_phase_values_sha256': phase_digest.hexdigest(),
            'group_union_cases': counts, 'total_union_cases': sum(counts),
            'group_case_values_sha256': [d.hexdigest() for d in digests],
            'weight_sha256': sha256(json.dumps(base, separators=(',', ':')).encode()).hexdigest(),
            'single_group_physical_capacity': single_group,
            'single_group_strict_physical_gap': sum(vector) - single_group}


def controls(data):
    cases = []
    def case(label, change):
        item = deepcopy(data)
        change(item)
        cases.append((label,item))
    case('wrong-period',lambda d:d.update(N=21600))
    case('missing-modulus',lambda d:d['moduli'].pop())
    case('wrong-raw-phase',lambda d:d['residues'].__setitem__(-1,58))
    case('boolean-phase',lambda d:d['residues'].__setitem__(0,False))
    case('repeated-resource-group',lambda d:d['groups'].append([3]))
    case('empty-weight',lambda d:d.update(boxes=[]))
    case('nonpositive-weight',lambda d:d['boxes'][0].__setitem__(-1,0))
    case('boolean-weight',lambda d:d['boxes'][0].__setitem__(-1,True))
    case('overlapping-boxes',lambda d:d['boxes'].append(deepcopy(d['boxes'][0])))
    case('mask-out-of-range',lambda d:d['boxes'][0].__setitem__(0,1<<16))
    case('weight-on-known-class',lambda d:d.update(boxes=[[1,1,1,1]]))
    rejected = []
    for label, item in cases:
        try:
            validate(item)
        except (ValueError,TypeError,KeyError,IndexError):
            rejected.append(label)
        else:
            raise RuntimeError('Malformed control was accepted: '+label)
    return rejected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls',action='store_true')
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    raw = (here/'input.json').read_bytes()
    data = json.loads(raw)
    expected = json.loads((here/'expected.json').read_text())
    row = validate(data)
    answer = physical(row, ORDER)
    if (sha256(raw).hexdigest() != expected['input_sha256'] or answer != expected['physical_result']
            or expected['scope'] != 'Only the explicit nineteen-class prefix'
            or not expected['child_exclusion'] or expected['root_exclusion']):
        raise ValueError('Physical integer evidence differs from expected.json')
    result = {'agent':'six-covering-3','role':'researcher','child_exclusion':True,
              'root_exclusion':False,'independent_review':False,'input_sha256':expected['input_sha256'],
              'physical_result':answer,'threads':1,'whole_union_cap_seconds':20}
    if args.controls:
        result['rejected_controls'] = controls(data)
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
